#!/usr/bin/env python3
"""CoupeFab price fetcher.

Polite by design:
  * identifies itself (USER_AGENT below), honours robots.txt (incl. Crawl-delay),
  * public pages / public storefront JSON only: no login, no cart, no captcha or
    bot-wall bypass. A site that answers 403/challenge is recorded as "blocked".
  * one request at a time with a delay between requests.

Writes:
  data/prices/latest.json             all normalized rows + supplier status + FX
  data/prices/history/YYYY-MM.csv    dated price log (new rows + every price/stock change)
  data/prices/index.csv               daily median CAD $/lb per family/form (trend chart)

Every price row carries its source URL and fetch timestamp. Nothing is estimated
when a supplier does not publish a number: those suppliers are listed as
"sur demande" (quote only) in SUPPLIERS_STATIC.
"""
import argparse
import csv
import datetime as dt
import html
import io
import json
import re
import statistics
import sys
import time
import urllib.robotparser
from pathlib import Path
from zoneinfo import ZoneInfo

import requests
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).parent))
import normalize as N  # noqa: E402
import fetch_more as M  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "prices"
TZ = ZoneInfo("America/Toronto")
USER_AGENT = "Mozilla/5.0 (compatible; CoupeFabPrixBot/1.0; +https://coupefab.vercel.app/prix/)"
DEFAULT_DELAY = 1.5

S = requests.Session()
S.headers.update({"User-Agent": USER_AGENT, "Accept-Language": "fr-CA,fr;q=0.9,en;q=0.8"})
_robots = {}
_last_hit = {}


class Blocked(Exception):
    pass


def robots_for(base):
    if base not in _robots:
        rp = urllib.robotparser.RobotFileParser()
        try:
            r = S.get(base + "/robots.txt", timeout=20)
            rp.parse(r.text.splitlines() if r.status_code == 200 else [])
        except requests.RequestException:
            rp.parse([])
        _robots[base] = rp
    return _robots[base]


def get(url, *, method="GET", data=None, headers=None, timeout=40):
    m = re.match(r"(https?://[^/]+)", url)
    base = m.group(1)
    rp = robots_for(base)
    if not rp.can_fetch(USER_AGENT, url):
        raise Blocked(f"robots.txt disallows {url}")
    delay = max(DEFAULT_DELAY, float(rp.crawl_delay(USER_AGENT) or 0))
    wait = _last_hit.get(base, 0) + delay - time.time()
    if wait > 0:
        time.sleep(wait)
    try:
        r = S.request(method, url, data=data, headers=headers, timeout=timeout)
    finally:
        _last_hit[base] = time.time()
    if r.status_code in (401, 403, 429, 503) or "Just a moment" in r.text[:2000]:
        raise Blocked(f"HTTP {r.status_code} (bot protection or rate limit) at {url}")
    r.raise_for_status()
    return r


def dump_latest(d):
    """latest.json: metadata indented, one price row per line (compact yet diff-friendly)."""
    meta = {k: v for k, v in d.items() if k != "rows"}
    head = json.dumps(meta, ensure_ascii=False, indent=1)[:-2]
    rows = ",\n".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) for r in d.get("rows", []))
    return head + ',\n "rows": [\n' + rows + "\n ]\n}\n"


def now_iso():
    return dt.datetime.now(TZ).isoformat(timespec="seconds")


# ---------------------------------------------------------------------------
# FX: Bank of Canada Valet API
# ---------------------------------------------------------------------------
def fx_usdcad():
    url = "https://www.bankofcanada.ca/valet/observations/FXUSDCAD/json?recent=1"
    r = get(url)
    obs = r.json()["observations"][-1]
    return {"pair": "USD/CAD", "rate": float(obs["FXUSDCAD"]["v"]), "date": obs["d"],
            "source": "Banque du Canada — taux de change quotidien (Valet FXUSDCAD)",
            "url": "https://www.bankofcanada.ca/rates/exchange/daily-exchange-rates/"}


# ---------------------------------------------------------------------------
# Row builder
# ---------------------------------------------------------------------------
def make_row(*, supplier, text, price, currency, url, fx, unit="each", form_hint="",
             width_in=None, length_in=None, length_ft=None, weight_lb=None, size_label="",
             shipping="", notes="", source_updated="", availability="", family=None,
             grade=None, thickness_in=None):
    text = html.unescape(text)
    if N.EXCLUDE.search(text):
        return None
    family = family or N.detect_family(text)
    if not family:
        return None
    if grade is None:
        grade, in_cat = N.detect_grade(text, family)
    else:
        in_cat = bool(grade) and grade in N.CATALOGUE.get(family, [])
    form = N.detect_form(text, form_hint)
    if not form:
        return None
    gauge = None
    if form == "feuille":
        if thickness_in is None:
            thickness_in, gauge, _ = N.parse_thickness(text, family, grade)
        form = N.sheet_or_plate(thickness_in)
    price = float(price)
    if price <= 0:
        return None
    rate = 1.0 if currency == "CAD" else fx["rate"]
    price_cad = round(price * rate, 2)
    row = {
        "supplier": supplier["id"], "family": family, "grade": grade or "", "in_catalogue": bool(in_cat),
        "form": form, "description": text.strip()[:160], "size_label": size_label,
        "thickness_in": thickness_in, "thickness_mm": round(thickness_in * 25.4, 2) if thickness_in else None,
        "gauge": gauge, "width_in": width_in, "length_in": length_in, "length_ft": length_ft,
        "price": round(price, 2), "currency": currency, "unit": unit, "fx_rate": rate if currency != "CAD" else None,
        "price_cad": price_cad, "price_per_lb_cad": None, "price_per_kg_cad": None,
        "price_per_sqft_cad": None, "price_per_ft_cad": None, "weight_lb": None,
        "shipping": shipping or supplier.get("shipping", ""), "availability": availability,
        "url": url, "fetched_at": now_iso(), "source_updated": source_updated, "notes": notes,
    }
    # derived units (computed, labelled as such on the page)
    if unit == "each" and form in ("tole", "plaque"):
        area = (width_in * length_in / 144.0) if width_in and length_in else None
        if weight_lb is None:
            weight_lb = N.sheet_weight_lb(family, thickness_in, width_in, length_in)
        if area:
            row["price_per_sqft_cad"] = round(price_cad / area, 3)
    elif unit == "each" and length_ft:
        row["price_per_ft_cad"] = round(price_cad / length_ft, 3)
    elif unit == "sqft":
        row["price_per_sqft_cad"] = price_cad
        if thickness_in:
            lb_sqft = N.DENSITY[family] * thickness_in * 144
            row["price_per_lb_cad"] = round(price_cad / lb_sqft, 3)
    elif unit == "lb":
        row["price_per_lb_cad"] = price_cad
        if thickness_in:
            row["price_per_sqft_cad"] = round(price_cad * N.DENSITY[family] * thickness_in * 144, 3)
    elif unit == "ft":
        row["price_per_ft_cad"] = price_cad
    if weight_lb:
        row["weight_lb"] = round(weight_lb, 2)
        if unit == "each":
            row["price_per_lb_cad"] = round(price_cad / weight_lb, 3)
    if row["price_per_lb_cad"]:
        row["price_per_kg_cad"] = round(row["price_per_lb_cad"] * 2.20462, 3)
    return row


def dims_from_variant(title):
    """'Up to 48" width / Up to 96" length' -> (48, 96); '3 FT' -> (None, 36)."""
    w = re.search(r"([\d.]+)\"?\s*width", title)
    l = re.search(r"([\d.]+)\"?\s*length", title)
    if w or l:
        return (float(w.group(1)) if w else None, float(l.group(1)) if l else None)
    m = re.search(r"([\d.]+)\s*(FT|ft|')", title)
    if m:
        return None, float(m.group(1)) * 12
    m = re.search(r"([\d.]+)\s*(\"|in)", title)
    if m:
        return None, float(m.group(1))
    return None, None


def size_label_from_title(title):
    t = html.unescape(title)
    m = re.search(r"(\d[\d\-/. ]*(?:\"|mm|in)?(?:\s*(?:x|X)\s*[\d\-/. ]+(?:\"|mm|in)?)*(?:\s*NPS)?(?:\s*x?\s*Sch(?:edule)?\s*\d+)?)", t)
    return m.group(1).strip() if m else ""


# ---------------------------------------------------------------------------
# Suppliers with fetchers
# ---------------------------------------------------------------------------
SUPPLIERS = {
    "metalsrus": {"id": "metalsrus", "name": "Metals ’R’ Us", "city": "Dartmouth (N.-É.)", "region": "CA",
                  "site": "https://metalsrus.ca", "currency": "CAD", "ships_qc": "oui",
                  "shipping": "Livraison partout au Canada (tarifs transporteur au panier); coupe sur mesure.",
                  "shipping_en": "Ships across Canada (live carrier rates at checkout); cut to size.",
                  "method": "Vitrine Shopify publique (products.json des collections)"},
    "metalsdepot": {"id": "metalsdepot", "name": "Metals Depot", "city": "Winchester (KY, É.-U.)", "region": "US",
                    "site": "https://www.metalsdepot.com", "currency": "USD", "ships_qc": "oui",
                    "shipping": "Prix en USD convertis en CAD (Banque du Canada). Transport, droits et courtage vers le Québec en sus.",
                    "shipping_en": "USD prices converted to CAD (Bank of Canada). Freight, duties and brokerage to Quebec extra.",
                    "method": "Page catalogue publique + requête de prix publique du site (qté 1)"},
    "unitedstainless": {"id": "unitedstainless", "name": "United Stainless", "city": "Saint-Hubert (QC)", "region": "QC",
                        "site": "https://unitedstainless.ca", "currency": "CAD", "ships_qc": "indicatif",
                        "shipping": "Liste indicative d’un atelier de fabrication : on ne commande pas la matière seule.",
                        "shipping_en": "Indicative list from a fabrication shop: material is not sold on its own.",
                        "method": "Page publique « Indicative Material Costs »"},
    "mercier40": {"id": "mercier40", "name": "Mercier 40", "city": "Champlain (QC)", "region": "QC",
                  "site": "https://mercier40.ca", "currency": "CAD", "ships_qc": "cueillette",
                  "shipping": "Cueillette à Champlain (Mauricie). Plaques neuves « coin rouge » (décapé huilé), nuance non précisée. Classé « Surplus / indicatif » : affiché, mais exclu de la médiane et du « Meilleur prix ».",
                  "shipping_en": "Pickup in Champlain (Mauricie). New ‘red corner’ plates (pickled & oiled), grade not stated. Tagged ‘Surplus / indicative’: shown, but excluded from the median and from ‘Best price’.",
                  "method": "Page catégorie publique"},
    "princessauto": {"id": "princessauto", "name": "Princess Auto", "city": "Magasins au Canada (dont QC)", "region": "CA",
                     "site": "https://www.princessauto.com", "currency": "CAD", "ships_qc": "oui",
                     "shipping": "Petites feuilles 24 × 48 po; cueillette en magasin ou expédition.",
                     "shipping_en": "Small 24 × 48 in sheets; store pickup or shipping.",
                     "method": "Pages produit publiques"},
    "millennium": {"id": "millennium", "name": "Millennium Alloys", "city": "Colombie-Britannique", "region": "CA",
                   "site": "https://millenniumalloys.ca", "currency": "CAD", "ships_qc": "repere",
                   "shipping": "Repère de prix canadien (masqué par défaut) : prix publiés, commande par téléphone, expédition vers le Québec non confirmée.",
                   "shipping_en": "Canadian price benchmark (hidden by default): published prices, order by phone, shipping to Quebec not confirmed.",
                   "method": "API publique WooCommerce Store (Crawl-delay 30 s respecté)"},
    "nationalsalvage": {"id": "nationalsalvage", "name": "National Salvage", "city": "Lethbridge (AB)", "region": "CA",
                        "site": "https://shop.nationalsalvage.ca", "currency": "CAD", "ships_qc": "repere",
                        "shipping": "Cueillette à Lethbridge (Alberta) seulement : repère de prix canadien, pas une source d’achat au Québec.",
                        "shipping_en": "Pickup in Lethbridge (Alberta) only: a Canadian price benchmark, not a Quebec buying option.",
                        "method": "Vitrine Shopify publique (products.json)"},
    # --- added by the 26 Nov 2026 coverage sweep (data/sources/discovery-log.csv) ---
    "aluminox": {"id": "aluminox", "name": "Aluminox Canada", "city": "Lachine, Montréal (QC)", "region": "QC",
                 "site": "https://aluminox.ca", "currency": "CAD", "ships_qc": "oui",
                 "shipping": "Coupe sur mesure à Montréal; expédition au Canada (vitrine Shopify).",
                 "shipping_en": "Cut to size in Montreal; ships within Canada (Shopify storefront).",
                 "method": "Vitrine Shopify publique (products.json)"},
    "forcesinc": {"id": "forcesinc", "name": "Forces Inc", "city": "Blainville (QC)", "region": "QC",
                  "site": "https://shop.forcesinc.ca", "currency": "CAD", "ships_qc": "oui",
                  "shipping": "Fournisseur industriel de Blainville; petits formats (jusqu’à 24 × 24 po) expédiés.",
                  "shipping_en": "Industrial supplier in Blainville; small sizes (up to 24 × 24 in) shipped.",
                  "method": "Vitrine Shopify publique (collection Raw Materials)"},
    "valmont": {"id": "valmont", "name": "Valmont Metal", "city": "Montréal (QC)", "region": "QC",
                "site": "https://valmontmetal.com", "currency": "CAD", "ships_qc": "oui",
                "shipping": "Barres inox métriques de 6 pi; expédition au Canada.",
                "shipping_en": "Metric 6 ft stainless bars; ships within Canada.",
                "method": "Vitrine Shopify publique (products.json)"},
    "acierterrebonne": {"id": "acierterrebonne", "name": "Acier Terrebonne", "city": "Terrebonne (QC)", "region": "QC",
                        "site": "https://acierterrebonne.com", "currency": "CAD", "ships_qc": "cueillette",
                        "shipping": "Boutique en ligne; cueillette ou livraison dans la grande région de Montréal.",
                        "shipping_en": "Online shop; pickup or delivery in Greater Montreal.",
                        "method": "API publique WooCommerce Store (variations)"},
    "wemachine": {"id": "wemachine", "name": "WeMachine & Fabricate", "city": "Aylmer (ON)", "region": "CA",
                  "site": "https://wemachine.ca", "currency": "CAD", "ships_qc": "oui",
                  "shipping": "Ontario; expédie au Canada. Coupe à la longueur.",
                  "shipping_en": "Ontario; ships within Canada. Cut to length.",
                  "method": "Vitrine Shopify publique (products.json)"},
    "smithmetal": {"id": "smithmetal", "name": "Smith Metal Shop", "city": "Severn (ON)", "region": "CA",
                   "site": "https://smithmetalshop.com", "currency": "CAD", "ships_qc": "oui",
                   "shipping": "Ontario; expédie au Canada. Aluminium 6061-T6 coupé à la longueur.",
                   "shipping_en": "Ontario; ships within Canada. 6061-T6 aluminum cut to length.",
                   "method": "Vitrine Shopify publique (products.json)"},
    "recyborg": {"id": "recyborg", "name": "Coop Recyborg", "city": "Montréal (QC)", "region": "QC",
                 "site": "https://recyborg.com", "currency": "CAD", "ships_qc": "cueillette",
                 "shipping": "Ressourcerie, cueillette à Montréal (Pointe-Saint-Charles). Prix « neuf » au pied publiés; stock variable, nuance non précisée. Classé « Surplus / indicatif » : affiché, mais exclu de la médiane et du « Meilleur prix ».",
                 "shipping_en": "Reuse centre, pickup in Montreal (Pointe-Saint-Charles). Published ‘new’ prices per foot; stock varies, grade not stated. Tagged ‘Surplus / indicative’: shown, but excluded from the median and from ‘Best price’.",
                 "method": "Tableau de prix public (page HTML)"},
    "optikutz": {"id": "optikutz", "name": "OptiKutz", "city": "Niagara Falls (ON)", "region": "CA",
                 "site": "https://optikutz.com", "currency": "CAD", "ships_qc": "oui",
                 "shipping": "Ontario; tôles coupées au laser jusqu’à 2 × 4 pi, expédiées au Canada.",
                 "shipping_en": "Ontario; laser-cut sheets up to 2 × 4 ft, shipped within Canada.",
                 "method": "Vitrine Shopify publique (products.json)"},
    "lasersupply": {"id": "lasersupply", "name": "Canadian Laser Supply", "city": "Kingsville (ON)", "region": "CA",
                    "site": "https://lasersupply.ca", "currency": "CAD", "ships_qc": "oui",
                    "shipping": "Ontario; petites tôles (jusqu’à 24 × 24 po) expédiées au Canada.",
                    "shipping_en": "Ontario; small sheets (up to 24 × 24 in) shipped within Canada.",
                    "method": "Vitrine Shopify publique (products.json)"},
}

# Suppliers we checked that do not publish prices, or that we cannot read politely.
SUPPLIERS_STATIC = [
    {"name": "Metal Supermarkets", "city": "Ottawa (ON), dessert Gatineau — aucun magasin au Québec", "status": "sur_demande",
     "url": "https://www.metalsupermarkets.com/location/ottawa/", "note": "Aucun magasin au Québec (localisateur officiel); le plus proche est à Ottawa. Pas de prix publics lisibles : soumission en magasin ou en ligne.",
     "note_en": "No Quebec store (official locator); closest is Ottawa. No readable public prices: quote in store or online."},
    {"name": "Russel Metals", "city": "Québec (plusieurs centres)", "status": "sur_demande",
     "url": "https://www.russelmetals.com/", "note": "Centre de service : prix sur soumission.", "note_en": "Service centre: quoted prices."},
    {"name": "Acier Leroux (Leroux Steel)", "city": "Boucherville et régions", "status": "sur_demande",
     "url": "https://www.leroux-steel.com/", "note": "Prix sur demande.", "note_en": "Quote only."},
    {"name": "Acier Picard", "city": "Lévis", "status": "sur_demande",
     "url": "https://www.acierpicard.com/", "note": "Prix sur demande.", "note_en": "Quote only."},
    {"name": "Marmen", "city": "Trois-Rivières", "status": "sur_demande",
     "url": "https://www.marmeninc.com/", "note": "Fabricant; pas de vente de matière en ligne.", "note_en": "Fabricator; no online material sales."},
    {"name": "Acier Lachine", "city": "Montréal", "status": "sur_demande",
     "url": "https://www.acierlachine.com/produits/plaques-et-feuilles-en-acier/", "note": "Tableaux de calibres, prix sur demande.",
     "note_en": "Gauge tables, quote only."},
    {"name": "Multi-Plis", "city": "Repentigny", "status": "sur_demande",
     "url": "https://www.multiplis.qc.ca/metal-en-feuille/", "note": "Métal en feuille : prix sur demande.", "note_en": "Sheet metal: quote only."},
    {"name": "Arcan Aluminium", "city": "Laval / Montréal", "status": "sur_demande",
     "url": "https://arcanaluminium.com/produit/feuilles-dacier/", "note": "Feuilles en stock, aucun prix affiché.", "note_en": "Sheets in stock, no prices shown."},
    {"name": "North York Iron", "city": "Toronto (ON)", "status": "sur_demande",
     "url": "https://northyorkiron.com/steel-sheets/", "note": "Boutique en ligne, mais prix à 0 $ (« Add to Quote »).", "note_en": "Web shop, but $0 prices (“Add to Quote”)."},
    {"name": "GTA Steel", "city": "Toronto (ON)", "status": "sur_demande",
     "url": "https://gtasteel.com/products/hot-rolled-sheets", "note": "Tailles et poids publiés, prix par soumission.", "note_en": "Sizes and weights published, quoted prices."},
    {"name": "OnlineMetals", "city": "É.-U. (expédie au Canada)", "status": "bloque",
     "url": "https://www.onlinemetals.com/", "note": "Prix publics sur le site, mais HTTP 403 (protection anti-robot) pour notre robot : non lu, pas de contournement.",
     "note_en": "Public prices on the site, but HTTP 403 (bot protection) for our bot: not read, no workaround."},
    {"name": "Speedy Metals", "city": "É.-U.", "status": "bloque",
     "url": "https://www.speedymetals.com/", "note": "Prix publics sur le site, mais connexion refusée à notre robot : non lu, pas de contournement.", "note_en": "Public prices on the site, but connection refused to our bot: not read, no workaround."},
    {"name": "Home Depot Canada", "city": "Magasins QC", "status": "bloque",
     "url": "https://www.homedepot.ca/", "note": "Protection anti-robot (aucune réponse) : non lu.", "note_en": "Bot protection (no response): not read."},
    {"name": "Cangard Supplies", "city": "Canada", "status": "bloque",
     "url": "https://cangardsupplies.com/", "note": "robots.txt interdit les robots génériques : non lu.", "note_en": "robots.txt disallows generic bots: not read."},
    {"name": "RONA / Lowe’s / BMR", "city": "Magasins QC", "status": "bloque",
     "url": "https://www.rona.ca/", "note": "Prix publics, mais protection anti-robot (RONA et Lowe’s refusent la connexion, BMR répond 403) : non lus, pas de contournement.",
     "note_en": "Public prices, but bot protection (RONA and Lowe’s refuse the connection, BMR answers 403): not read, no workaround."},
    {"name": "Canac", "city": "Magasins QC", "status": "bloque",
     "url": "https://www.canac.ca/", "note": "robots.txt interdit les pages produits (/canac/fr/) : non lu.",
     "note_en": "robots.txt disallows product pages (/canac/fr/): not read."},
    {"name": "Potvin & Bouchard", "city": "Magasins QC", "status": "bloque",
     "url": "https://www.potvinbouchard.ca/", "note": "Prix publics, mais HTTP 403 (Cloudflare) pour notre robot : non lu.",
     "note_en": "Public prices, but HTTP 403 (Cloudflare) for our bot: not read."},
    {"name": "Patrick Morin", "city": "Magasins QC", "status": "non_couvert",
     "url": "https://patrickmorin.com/", "note": "Prix publics, mais les fiches de barres/tubes n’indiquent pas l’épaisseur : non comparables pour l’instant.",
     "note_en": "Public prices, but bar/tube pages do not state the thickness: not comparable yet."},
    {"name": "Public Metal", "city": "Welland (ON)", "status": "non_couvert",
     "url": "https://publicmetal.ca/", "note": "≈1 500 prix publics, mais l’unité (pied? barre?) n’est indiquée nulle part : non ajoutés plutôt que deviner.",
     "note_en": "≈1,500 public prices, but the unit (per foot? per bar?) is not stated anywhere: not added rather than guess."},
    {"name": "Metal Pros", "city": "Ottawa (ON)", "status": "bloque",
     "url": "https://www.metalpros.com/", "note": "Outil de prix en ligne (quote.metalpros.com) en erreur HTTP 500 pour notre robot : non lu.",
     "note_en": "Online pricing tool (quote.metalpros.com) returns HTTP 500 to our bot: not read."},
    {"name": "Amazon.ca", "city": "En ligne", "status": "non_couvert",
     "url": "https://www.amazon.ca/", "note": "Pas d’aspiration (conditions d’Amazon). Liens affiliés possibles plus tard, si approuvés.",
     "note_en": "Not scraped (Amazon terms). Affiliate links possible later, if approved."},
]

MRU_COLLECTIONS = [
    ("sheet", "feuille"), ("carbon-plate", "feuille"),
    ("round-bar", "round bar"), ("flat-bar", "flat bar"), ("square-bar", "square bar"), ("hex-bar", "hex bar"),
    ("pipe", "pipe"), ("tube", "tube"), ("square-tube", "square tube"), ("rectangle-tube", "rectangular tube"),
    ("rotocast-bronze", ""), ("drill-rod", "round bar"),
]


WITH_BARS = False  # set by --with-bars (weekly): bar/tube/pipe collections are large


def fetch_metalsrus(fx, quick=False):
    sup = SUPPLIERS["metalsrus"]
    rows, seen = [], set()
    cols = MRU_COLLECTIONS if (WITH_BARS and not quick) else MRU_COLLECTIONS[:2]
    for coll, hint in cols:
        page = 1
        while True:
            url = f"{sup['site']}/collections/{coll}/products.json?limit=250&page={page}"
            prods = get(url).json().get("products", [])
            if not prods:
                break
            for p in prods:
                if p["id"] in seen:
                    continue
                seen.add(p["id"])
                title = html.unescape(p["title"])
                ptype = p.get("product_type", "")
                purl = f"{sup['site']}/products/{p['handle']}"
                vs = [v for v in p["variants"] if float(v["price"]) > 0]
                if not vs:
                    continue
                form_hint = (hint + " " + ptype) if hint != "feuille" else ("sheet " + ptype)
                if hint == "feuille" or "sheet" in ptype.lower() or "plate" in ptype.lower():
                    best = None
                    for v in vs:
                        w, l = dims_from_variant(v["title"])
                        if w and l:
                            if best is None or w * l > best[0]:
                                best = (w * l, w, l, v)
                    if not best:
                        continue
                    _, w, l, v = best
                    trunc = len(p["variants"]) >= 250
                    if trunc:
                        continue  # variant list truncated by the storefront: largest size unknown, skip
                    r = make_row(supplier=sup, text=title, price=v["price"], currency="CAD", url=purl, fx=fx,
                                 form_hint=form_hint, width_in=w, length_in=l,
                                 weight_lb=(v["grams"] / 453.592) if v.get("grams") else None,
                                 size_label=f'{w:g} × {l:g} po',
                                 notes=("Plus grand format offert en ligne (coupe sur mesure)"
                                        + ("; liste de variantes tronquée à 250" if trunc else "")),
                                 availability="en ligne" if v.get("available", True) else "rupture")
                else:
                    best = None
                    for v in vs:
                        _, l = dims_from_variant(v["title"])
                        if l and (best is None or l > best[0]):
                            best = (l, v)
                    if not best:
                        continue
                    l, v = best
                    r = make_row(supplier=sup, text=title, price=v["price"], currency="CAD", url=purl, fx=fx,
                                 form_hint=form_hint, length_ft=l / 12.0,
                                 weight_lb=(v["grams"] / 453.592) if v.get("grams") else None,
                                 size_label=size_label_from_title(title) + f" — {l:g} po",
                                 notes="Plus grande longueur offerte en ligne",
                                 availability="en ligne" if v.get("available", True) else "rupture")
                if r:
                    rows.append(r)
            if len(prods) < 250:
                break
            page += 1
    return rows


MD_PAGES = [
    "/steel-products/steel-sheet", "/steel-products/steel-plate",
    "/galvanized-steel-products/galvanized-sheet-plate",
    "/aluminum-products/aluminum-sheet", "/aluminum-products/6061-aluminum-sheet-plate",
    "/stainless-steel-products/stainless-steel-sheet-plate", "/stainless-steel-products/stainless-sheet-316",
]


# Bars, tubes, pipe and angles (weekly, --with-bars): one public price request per product.
MD_BAR_PAGES = [
    "/steel-products/steel-angle", "/steel-products/steel-flat-bar", "/steel-products/steel-square-bar",
    "/steel-products/steel-round-bar", "/steel-products/steel-square-tube", "/steel-products/steel-rectangle-tube",
    "/steel-products/steel-round-tube-dom", "/steel-products/steel-round-tube-welded", "/steel-products/steel-pipe",
    "/cold-finish-steel-products/cold-finish-steel-flat", "/cold-finish-steel-products/cold-finish-steel-round",
    "/cold-finish-steel-products/cold-finish-steel-square", "/cold-finish-steel-products/cold-finish-steel-hexagon",
    "/galvanized-steel-products/galvanized-angle-", "/galvanized-steel-products/galvanized-square-tube",
    "/galvanized-steel-products/galvanized-pipe", "/galvanized-steel-products/galvanized-flat-bar-",
    "/aluminum-products/aluminum-angle-6061", "/aluminum-products/aluminum-angle-6063",
    "/aluminum-products/aluminum-flat-bar", "/aluminum-products/aluminum-square-bar",
    "/aluminum-products/aluminum-round-bar", "/aluminum-products/aluminum-square-tube",
    "/aluminum-products/aluminum-rectangle-tube", "/aluminum-products/aluminum-round-tube",
    "/aluminum-products/aluminum-pipe",
    "/stainless-steel-products/stainless-steel-angle", "/stainless-steel-products/stainless-steel-flat",
    "/stainless-steel-products/stainless-steel-square", "/stainless-steel-products/stainless-steel-round",
    "/stainless-steel-products/stainless-steel-round-316-", "/stainless-steel-products/stainless-steel-square-tube",
    "/stainless-steel-products/stainless-rectangle-tube", "/stainless-steel-products/stainless-steel-round-tube",
    "/stainless-steel-products/stainless-steel-pipe",
    "/brass-products/brass-flat-bar", "/brass-products/brass-round-bar",
    "/brass-products/copper-flat-bar", "/brass-products/copper-round-bar",
]
MD_HINT = [("galvanized", "Galvanized steel"), ("cold-finish", "Cold finish steel"), ("aluminum", "Aluminum"),
           ("316", "Stainless 316"), ("stainless", "Stainless"), ("copper", "Copper"), ("brass", "Brass"), ("steel", "Steel")]
MD_FORM = [("angle", "angle"), ("pipe", "pipe"), ("rectangle-tube", "rectangular tube"), ("square-tube", "square tube"),
           ("round-tube", "round tube"), ("flat", "flat bar"), ("square", "square bar"), ("hexagon", "hex bar"),
           ("round", "round bar")]


def fetch_metalsdepot_bars(fx, quick=False):
    sup = SUPPLIERS["metalsdepot"]
    rows = []
    for path in (MD_BAR_PAGES[:2] if quick else MD_BAR_PAGES):
        url = sup["site"] + path
        try:
            soup = BeautifulSoup(get(url).text, "lxml")
        except requests.HTTPError:
            continue
        fam_hint = next(h for k, h in MD_HINT if k in path)
        form_hint = next(h for k, h in MD_FORM if k in path)
        for pr in soup.select(".product-row[data-product-id]"):
            ps = pr.select_one(".product-size")
            if not ps:
                continue
            text = ps.get_text(" ", strip=True)
            opts = []
            for o in pr.select("select.length-select option[data-skuid]"):
                m = re.search(r"([\d.]+)\s*Ft", o.get_text(strip=True), re.I)
                if m:
                    opts.append((float(m.group(1)), o["data-skuid"]))
            if not opts:
                continue
            L, sku = max(opts)
            resp = get(sup["site"] + "/system/modrequest", method="POST",
                       data={"request": "metals.getPrice", "data[product_id]": pr["data-product-id"],
                             "data[qty]": "1", "data[sku_id]": sku},
                       headers={"X-Requested-With": "XMLHttpRequest", "Referer": url})
            try:
                price = float(resp.text.strip().strip('"'))
            except ValueError:
                continue
            full = text if N.detect_family(text) and ("galv" not in path or "galv" in text.lower()) else f"{fam_hint} {text}"
            r = make_row(supplier=sup, text=full, price=price, currency="USD", url=url, fx=fx, form_hint=form_hint,
                         length_ft=L, size_label=f"{text} — {L * 12:g} po",
                         notes="Prix à l’unité (qté 1), plus grande longueur offerte")
            if r:
                r["buy_url"] = f"{url}#{pr['data-product-id']}"
                rows.append(r)
    return rows


def _md_size(label):
    m = re.search(r"([\d.]+)\s*(Ft|In)\.?\s*x\s*([\d.]+)\s*(Ft|In)", label, re.I)
    if not m:
        return None
    a = float(m.group(1)) * (12 if m.group(2).lower() == "ft" else 1)
    b = float(m.group(3)) * (12 if m.group(4).lower() == "ft" else 1)
    return min(a, b), max(a, b)


def fetch_metalsdepot(fx, quick=False):
    sup = SUPPLIERS["metalsdepot"]
    rows = []
    for path in MD_PAGES:
        url = sup["site"] + path
        soup = BeautifulSoup(get(url).text, "lxml")
        for pr in soup.select(".product-row[data-product-id]"):
            ps = pr.select_one(".product-size")
            if not ps:
                continue
            text = ps.get_text(" ", strip=True)
            opts = []
            for o in pr.select("select.length-select option[data-skuid]"):
                d = _md_size(o.get_text(strip=True))
                if d:
                    opts.append((d, o["data-skuid"]))
            if not opts:
                continue
            pick = next((x for x in opts if x[0] == (48, 96)), None) or max(opts, key=lambda x: x[0][0] * x[0][1])
            (w, l), sku = pick
            resp = get(sup["site"] + "/system/modrequest", method="POST",
                       data={"request": "metals.getPrice", "data[product_id]": pr["data-product-id"],
                             "data[qty]": "1", "data[sku_id]": sku},
                       headers={"X-Requested-With": "XMLHttpRequest", "Referer": url})
            try:
                price = float(resp.text.strip().strip('"'))
            except ValueError:
                continue
            r = make_row(supplier=sup, text=text, price=price, currency="USD", url=url, fx=fx,
                         form_hint="sheet", width_in=w, length_in=l, size_label=f"{w:g} × {l:g} po",
                         notes="Prix à l’unité (qté 1), format standard")
            if r:
                r["buy_url"] = f"{url}#{pr['data-product-id']}"  # the product's own row on the category page
                rows.append(r)
            if quick and len(rows) > 10:
                break
    if WITH_BARS:
        rows += fetch_metalsdepot_bars(fx, quick)
    return rows


def fetch_unitedstainless(fx, quick=False):
    sup = SUPPLIERS["unitedstainless"]
    url = sup["site"] + "/live-prices"
    soup = BeautifulSoup(get(url).text, "lxml")
    txt = soup.get_text("\n", strip=True)
    m = re.search(r"Last updated:\s*([A-Z][a-z]+ \d{1,2}, \d{4})", txt)
    updated = dt.datetime.strptime(m.group(1), "%B %d, %Y").date().isoformat() if m else ""
    lines = [l for l in txt.split("\n")]
    rows, cat, seen = [], "", set()
    for i, l in enumerate(lines):
        if re.search(r"·\s*Per ", l):
            cat = lines[i - 2] if lines[i - 1].startswith("Min. order") else lines[i - 1]
        mp = re.fullmatch(r"\$([\d,]+\.\d{2})/(sq ft|lb|ft|pc|piece|ea)", l)
        if not (mp and i):
            continue
        desc = lines[i - 1]
        unit = {"sq ft": "sqft", "lb": "lb", "ft": "ft"}.get(mp.group(2), "each")
        key = (cat, desc, mp.group(1))
        if key in seen or cat.startswith("Flat-Angle"):
            continue  # flat bar and angle are mixed in that list: skipped
        seen.add(key)
        fam = "inox" if cat.endswith("SS") else ("aluminium" if cat.endswith("AL") else None)
        if not fam:
            continue
        grade, _ = N.detect_grade(desc, fam)
        thk, size, hint = None, desc, ""
        d = desc.replace(",", ".")
        if cat.startswith("Plaque"):
            hint = "sheet"
            thk, _, _ = N.parse_thickness(d, fam, grade)
            if thk is None:
                m = re.match(r"\s*(\d+[ -]\d+/\d+|\d+/\d+)", d)
                thk = N._num(m.group(1)) if m else None
            if thk is None or thk > 3:
                continue  # unusual rows (e.g. 6061 "Plate 7.048") left out until reviewed
        elif cat.startswith("Barre"):
            hint = "round bar"
        elif cat.startswith("Tube"):
            n = len(re.findall(r"x", d, re.I)) + 1
            hint = "square tube" if n >= 3 else "tube"
            if n >= 3:
                parts = [p.strip() for p in re.split(r"x", d, flags=re.I)]
                if len(parts) >= 2 and parts[0] != parts[1]:
                    hint = "rectangular tube"
        r = make_row(supplier=sup, text=f"{cat} {desc}", price=mp.group(1).replace(",", ""), currency="CAD", url=url,
                     fx=fx, unit=unit, form_hint=hint, family=fam, grade=grade or "", thickness_in=thk,
                     size_label=desc, source_updated=updated,
                     notes="Coût indicatif publié par un atelier de fabrication; pas un prix de vente de matière"
                           + ("; min. 10 pi linéaires" if unit == "ft" else ""))
        if r:
            rows.append(r)
    return rows


def fetch_mercier40(fx, quick=False):
    sup = SUPPLIERS["mercier40"]
    rows = []
    for page in (1, 2, 3):
        url = sup["site"] + "/acier-en-plaque" + (f"?page={page}" if page > 1 else "")
        soup = BeautifulSoup(get(url).text, "lxml")
        lines = soup.get_text("\n", strip=True).split("\n")
        found = 0
        for i, l in enumerate(lines):
            if not l.startswith("ACIER PLAQUE NEUF"):
                continue
            found += 1
            block = lines[i:i + 12]
            price = next((re.match(r"([\d\s]+,\d{2})\$ CAD", b) for b in block if re.match(r"[\d\s]+,\d{2}\$ CAD", b)), None)
            if not price:
                continue
            dims = re.search(r"(\d+)PO X (\d+)PO X (?:\d+ JAUGES )?([\d,]+)PO", l)
            if not dims:
                continue
            w, ln = float(dims.group(1)), float(dims.group(2))
            thk = float(dims.group(3).replace(",", "."))
            avail = next((b.split(":", 1)[1].strip() for b in block if b.startswith("Disponibilité")), "")
            code = next((block[j + 1] for j, b in enumerate(block[:-1]) if b.startswith("Code")), "")
            href = soup.find("a", href=re.compile(re.escape(code.lower()) + "$")) if code else None
            purl = (sup["site"] + href["href"]) if href and href["href"].startswith("/") else (href["href"] if href else url)
            r = make_row(supplier=sup, text=l, price=price.group(1).replace(" ", "").replace(",", "."),
                         currency="CAD", url=purl, fx=fx, form_hint="plaque", family="acier", grade="HRPO (nuance non précisée)",
                         thickness_in=thk, width_in=min(w, ln), length_in=max(w, ln), size_label=f"{min(w,ln):g} × {max(w,ln):g} po",
                         availability=avail, notes="Plaque neuve « coin rouge » (décapé huilé) selon la fiche")
            if r:
                rows.append(r)
        if not found:
            break
    return rows


def fetch_princessauto(fx, quick=False):
    sup = SUPPLIERS["princessauto"]
    base = sup["site"] + "/en/product/cold-rolled-steel-sheets/PA1000003097"
    page = get(base).text.replace('\\"', '"')
    variants = re.findall(r'\{"sku":"(\d+)","option":\[\{"option_display_name":"[^"]+","label":"([^"]+)"\},\{"option_display_name":"[^"]+","label":"(\d+)"\}\]\}', page)
    rows = []
    for sku, finish, gauge in dict(((v[0], v) for v in variants)).values():
        url = f"{base}/{sku}"
        p = get(url).text.replace('\\"', '"')
        m = re.search(r'"sku":"' + sku + r'".{0,3000}?"price":\{"currencyCode":"CAD","value":([\d.]+)', p, re.S)
        if not m:
            continue
        galv = finish.lower().startswith(("galv",))
        text = f"{'Galvanized' if galv else 'Cold rolled'} steel sheet {gauge} gauge 24 x 48 in"
        grade = "Galvanisé A653" if galv else "CR (nuance non précisée)"
        thk = (N.GAUGE_GALV if galv else N.GAUGE_STEEL).get(int(gauge))
        r = make_row(supplier=sup, text=text, price=m.group(1), currency="CAD", url=url, fx=fx, form_hint="sheet",
                     family="acier", grade=grade, thickness_in=thk, width_in=24, length_in=48, size_label="24 × 48 po",
                     notes="Powerfist; épaisseur déduite du calibre (table MSG)")
        if r:
            r["gauge"] = int(gauge)
            rows.append(r)
    return rows


def fetch_millennium(fx, quick=False):
    sup = SUPPLIERS["millennium"]
    rows = []
    page = 1
    while page < 6:
        url = f"{sup['site']}/wp-json/wc/store/v1/products?category=62&per_page=100&page={page}"
        data = get(url).json()
        if not data:
            break
        for p in data:
            name = html.unescape(p["name"])
            pr = p["prices"]
            div = 10 ** pr.get("currency_minor_unit", 2)
            price, note = None, ""
            if p["type"] == "simple":
                price = int(pr["price"]) / div
            elif pr.get("price_range"):
                lo, hi = int(pr["price_range"]["min_amount"]) / div, int(pr["price_range"]["max_amount"]) / div
                terms = [t["name"].lower() for a in p.get("attributes", []) for t in a.get("terms", [])]
                if lo and set(terms) == {"full sheet", "half sheet"} and abs(hi / lo - 2) < 0.02:
                    price, note = hi, "Variante « Full Sheet » (le haut de la fourchette publiée; la demi-feuille vaut la moitié)"
            if not price:
                continue
            d = re.search(r"([\d.]+)\s*ft\s*X\s*([\d.]+)\s*ft", name, re.I)
            w, l = (float(d.group(1)) * 12, float(d.group(2)) * 12) if d else (None, None)
            r = make_row(supplier=sup, text=name, price=price, currency="CAD", url=p["permalink"], fx=fx,
                         form_hint="sheet", width_in=w and min(w, l), length_in=l and max(w, l),
                         size_label=f"{min(w,l):g} × {max(w,l):g} po" if w else "", notes=note)
            if r:
                rows.append(r)
        if len(data) < 100:
            break
        page += 1
    return rows


def fetch_nationalsalvage(fx, quick=False):
    sup = SUPPLIERS["nationalsalvage"]
    rows = []
    data = get(sup["site"] + "/products.json?limit=250").json()["products"]
    for p in data:
        title = html.unescape(p["title"])
        if not re.search(r"sheet|plate", title, re.I):
            continue
        full = next((v for v in p["variants"] if "full" in v["title"].lower()), None)
        if not full:
            continue
        d = re.search(r"(\d+)\s*×\s*(\d+)\s*ft", title)
        w, l = (int(d.group(1)) * 12, int(d.group(2)) * 12) if d else (None, None)
        # grade is not stated on the listing: hot-rolled carbon steel assumed only as a family
        r = make_row(supplier=sup, text="Steel " + title.replace("—", " "), price=full["price"], currency="CAD",
                     url=f"{sup['site']}/products/{p['handle']}", fx=fx, form_hint="sheet", family="acier",
                     grade="Acier carbone (nuance non précisée)", width_in=w, length_in=l,
                     size_label=f"{w} × {l} po" if w else "", notes="Feuille pleine; cueillette Lethbridge (AB)")
        if r:
            rows.append(r)
    return rows


def fetch_aluminox(fx, quick=False):
    sup = SUPPLIERS["aluminox"]
    return M.shopify_rows(make_row, sup, M.shopify_products(get, sup["site"]), fx,
                          exclude=r"drain|dock|configurat|base plate|frame|beam|channel|column|cover|garage")


def fetch_forcesinc(fx, quick=False):
    sup = SUPPLIERS["forcesinc"]
    prods = M.shopify_products(get, sup["site"], ["raw-material-sheets-and-plates", "angle-stocks"])
    return M.shopify_rows(make_row, sup, prods, fx)


def fetch_valmont(fx, quick=False):
    sup = SUPPLIERS["valmont"]
    return M.shopify_rows(make_row, sup, M.shopify_products(get, sup["site"]), fx, exclude=r"\d+\s*bars?\s.*&")


def fetch_acierterrebonne(fx, quick=False):
    return M.woo_variable_rows(get, make_row, SUPPLIERS["acierterrebonne"], fx)


def fetch_wemachine(fx, quick=False):
    sup = SUPPLIERS["wemachine"]
    rows = M.shopify_rows(make_row, sup, M.shopify_products(get, sup["site"]), fx, family="acier",
                          note="Acier, nuance non précisée par le vendeur.")
    return rows


def fetch_smithmetal(fx, quick=False):
    sup = SUPPLIERS["smithmetal"]
    return M.shopify_rows(make_row, sup, M.shopify_products(get, sup["site"]), fx,
                          keep=r"^(Round|Square|Rectangular|Flat|Hex)?\s*(Tube|Bar|Angle|Sheet|Plate|Pipe)\s*-")


def fetch_optikutz(fx, quick=False):
    sup = SUPPLIERS["optikutz"]
    return M.shopify_rows(make_row, sup, M.shopify_products(get, sup["site"]), fx, keep=r"sheet")


def fetch_lasersupply(fx, quick=False):
    sup = SUPPLIERS["lasersupply"]
    return M.shopify_rows(make_row, sup, M.shopify_products(get, sup["site"]), fx,
                          keep=r"(stainless|alumin|steel|copper|brass).*sheet", exclude=r"acrylic|rowmark|2-ply")


def fetch_recyborg(fx, quick=False):
    """Coop Recyborg publishes one HTML table: description, metal, size, used $/lb, new $/ft.
    Some cells hold two items stacked with <br>; they are split and zipped. Only the 'new' per-foot
    price is kept (used per-lb scrap is not comparable stock)."""
    sup = SUPPLIERS["recyborg"]
    url = sup["site"] + "/fr/metal-neuf-et-doccasion/"
    soup = BeautifulSoup(get(url).text, "lxml")
    rows = []
    for tr in soup.select("table tr"):
        cells = [[x.strip() for x in c.get_text("\n").split("\n") if x.strip()] for c in tr.find_all("td")]
        if len(cells) < 5:
            continue
        n = max(len(c) for c in cells)
        for i in range(n):
            pick = [c[i] if i < len(c) else (c[0] if len(c) == 1 else "") for c in cells]
            desc, metal, dims, _, new = pick[:5]
            m = re.search(r"([\d]+(?:[.,]\d+)?)\s*(?:\$|€)\s*(?:/|par)\s*pieds?", new, re.I)
            if not m or "paire" in new:
                continue
            fam = {"acier": "acier", "aluminium": "aluminium", "inox": "inox"}.get(metal.lower().strip())
            if not fam or re.search(r"plaque|t[ôo]le", desc, re.I):   # plate sold per foot, width not stated
                continue
            text = f"{desc} {metal} {dims}"
            r = make_row(supplier=sup, text=text, price=float(m.group(1).replace(",", ".")), currency="CAD",
                         url=url, fx=fx, unit="ft", family=fam, size_label=f"{dims} po",
                         notes="Prix « neuf » au pied; ressourcerie, stock variable")
            if r:
                rows.append(r)
    return rows


FETCHERS = {
    "metalsrus": fetch_metalsrus, "metalsdepot": fetch_metalsdepot, "unitedstainless": fetch_unitedstainless,
    "mercier40": fetch_mercier40, "princessauto": fetch_princessauto, "millennium": fetch_millennium,
    "nationalsalvage": fetch_nationalsalvage,
    "aluminox": fetch_aluminox, "forcesinc": fetch_forcesinc, "valmont": fetch_valmont,
    "acierterrebonne": fetch_acierterrebonne, "wemachine": fetch_wemachine, "smithmetal": fetch_smithmetal,
    "optikutz": fetch_optikutz, "recyborg": fetch_recyborg, "lasersupply": fetch_lasersupply,
}
# Weekly set (bars/tubes, many requests): on a daily run their rows are kept from the last weekly run.
WEEKLY = {"acierterrebonne", "recyborg"}

CSV_FIELDS = ["supplier", "family", "grade", "in_catalogue", "form", "description", "size_label", "thickness_in",
              "thickness_mm", "gauge", "width_in", "length_in", "length_ft", "price", "currency", "unit", "fx_rate",
              "price_cad", "price_per_lb_cad", "price_per_kg_cad", "price_per_sqft_cad", "price_per_ft_cad",
              "weight_lb", "shipping", "availability", "url", "fetched_at", "source_updated", "notes"]


HIST_FIELDS = ["date", "change", "supplier", "family", "grade", "form", "description", "size_label", "thickness_in",
               "width_in", "length_in", "length_ft", "price", "currency", "unit", "price_cad", "price_per_lb_cad",
               "price_per_sqft_cad", "price_per_ft_cad", "availability", "url", "fetched_at"]


def row_key(r):
    return "|".join(str(r.get(k) or "") for k in ("supplier", "url", "description", "size_label"))


def write_history(prev_rows, rows, today):
    """Dated price log, one CSV per month: every row seen for the first time, and every price change.

    Replaying the log up to a date gives the full price list on that date, without
    storing ~2,000 unchanged rows every day."""
    path = OUT / "history" / f"{today[:7]}.csv"
    old = {row_key(r): r for r in prev_rows}
    new_file = not path.exists()
    out = []
    for r in rows:
        o = old.get(row_key(r))
        if new_file or o is None:
            out.append(dict(r, date=today, change="nouveau" if o is None else "debut_mois"))
        elif abs((o.get("price") or 0) - (r.get("price") or 0)) > 0.004 or o.get("availability") != r.get("availability"):
            out.append(dict(r, date=today, change="prix" if abs((o.get("price") or 0) - (r.get("price") or 0)) > 0.004 else "dispo",
                            previous_price=o.get("price")))
    with path.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HIST_FIELDS, extrasaction="ignore", lineterminator="\n")
        if new_file:
            w.writeheader()
        for x in out:
            w.writerow(x)
    print(f"history: {len(out)} lines -> {path.name}")


def write_index(rows, today):
    """Daily median CAD $/lb per family x form-group. Appends/replaces today's lines."""
    groups = {}
    for r in rows:
        if not r["price_per_lb_cad"] or r["supplier"] == "unitedstainless":
            continue
        fg = "feuille_plaque" if r["form"] in ("tole", "plaque") else ("tube_tuyau" if r["form"].startswith(("tube", "tuyau")) else "barre")
        groups.setdefault((r["family"], fg), []).append(r["price_per_lb_cad"])
    path = OUT / "index.csv"
    old = []
    if path.exists():
        with path.open() as f:
            old = [x for x in csv.DictReader(f) if x["date"] != today]
    new = [{"date": today, "family": fam, "form_group": fg, "median_cad_per_lb": round(statistics.median(v), 3),
            "n_rows": len(v)} for (fam, fg), v in sorted(groups.items()) if len(v) >= 2]
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["date", "family", "form_group", "median_cad_per_lb", "n_rows"], lineterminator="\n")
        w.writeheader()
        for x in old + new:
            w.writerow(x)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", help="supplier ids to refresh (others kept from latest.json)")
    ap.add_argument("--quick", action="store_true", help="small sample, for testing")
    ap.add_argument("--with-bars", action="store_true",
                    help="also refresh bar/tube/pipe (weekly); otherwise those rows are kept from the last weekly run")
    ap.add_argument("--rederive", action="store_true", help="recompute thickness/derived units of stored rows, no fetch")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "history").mkdir(exist_ok=True)
    today = dt.datetime.now(TZ).date().isoformat()
    prev = {}
    if (OUT / "latest.json").exists():
        prev = json.loads((OUT / "latest.json").read_text())
    global WITH_BARS
    WITH_BARS = args.with_bars
    if args.rederive:
        n = 0
        for r in prev.get("rows", []):
            if r["form"] in ("tole", "plaque") and not r.get("thickness_in"):
                t, g, _ = N.parse_thickness(r["description"], r["family"], r["grade"])
                if t:
                    n += 1
                    r["thickness_in"], r["thickness_mm"] = t, round(t * 25.4, 2)
                    r["gauge"] = r.get("gauge") or g
                    r["form"] = N.sheet_or_plate(t)
                    wl = N.sheet_weight_lb(r["family"], t, r.get("width_in"), r.get("length_in"))
                    if wl and r["unit"] == "each":
                        r["weight_lb"] = round(wl, 2)
                        r["price_per_lb_cad"] = round(r["price_cad"] / wl, 3)
                        r["price_per_kg_cad"] = round(r["price_per_lb_cad"] * 2.20462, 3)
        (OUT / "latest.json").write_text(dump_latest(prev))
        print(f"rederived {n} rows")
        return
    fx = fx_usdcad()
    all_rows, status = [], {}
    for sid, fn in FETCHERS.items():
        if (args.only and sid not in args.only) or (sid in WEEKLY and not WITH_BARS and not args.only
                                                    and any(r["supplier"] == sid for r in prev.get("rows", []))):
            all_rows += [r for r in prev.get("rows", []) if r["supplier"] == sid]
            if sid in prev.get("status", {}):
                status[sid] = prev["status"][sid]
            continue
        t0 = time.time()
        try:
            rows = fn(fx, quick=args.quick)
            if sid in ("metalsrus", "metalsdepot") and not WITH_BARS:
                kept = [r for r in prev.get("rows", []) if r["supplier"] == sid and r["form"] not in ("tole", "plaque")]
                rows += kept  # weekly bar/tube/pipe rows keep their own fetched_at date
            status[sid] = {"ok": True, "rows": len(rows), "fetched_at": now_iso(), "error": ""}
            all_rows += rows
            print(f"{sid}: {len(rows)} rows ({time.time()-t0:.0f}s)", flush=True)
        except Exception as e:  # keep yesterday's rows but flag them stale
            stale = [dict(r, notes=(r.get("notes", "") + " [relevé précédent]").strip()) for r in prev.get("rows", []) if r["supplier"] == sid]
            all_rows += stale
            status[sid] = {"ok": False, "rows": len(stale), "fetched_at": now_iso(),
                           "error": f"{type(e).__name__}: {e}"[:300], "blocked": isinstance(e, Blocked)}
            print(f"{sid}: FAILED {e}", file=sys.stderr, flush=True)
    latest = {"generated_at": now_iso(), "date": today, "fx": fx, "suppliers": SUPPLIERS,
              "suppliers_static": SUPPLIERS_STATIC, "status": status, "catalogue": N.CATALOGUE,
              "rows": all_rows}
    (OUT / "latest.json").write_text(dump_latest(latest))
    write_history(prev.get("rows", []), all_rows, today)
    write_index(all_rows, today)
    print(f"total {len(all_rows)} rows -> {OUT/'latest.json'}")


if __name__ == "__main__":
    main()

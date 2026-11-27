#!/usr/bin/env python3
"""CoupeFab price fetcher.

Polite by design:
  * identifies itself (USER_AGENT below), honours robots.txt (incl. Crawl-delay),
  * public pages / public storefront JSON only: no login, no cart, no captcha or
    bot-wall bypass. A site that answers 403/challenge is recorded as "blocked".
  * one request at a time with a delay between requests.

Writes:
  data/prices/latest.json             supplier status + FX + list of row shards (prices/store.py)
  data/prices/latest-rows/*.jsonl     all normalized rows, one per line, ≤ 4 MB per shard
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
import fetch_sweep5 as S5  # noqa: E402
from store import read_latest, write_latest  # noqa: E402

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
        # weight_lb is the mass of the priced unit (per piece if unit=each, per foot if unit=ft)
        if unit in ("each", "ft") and not row["price_per_lb_cad"]:
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
    "aircraftspruce": {"id": "aircraftspruce", "name": "Aircraft Spruce Canada", "city": "Brantford (ON)", "region": "CA",
                       "site": "https://www.aircraftspruce.ca", "currency": "CAD", "ships_qc": "oui",
                       "shipping": "Prix en CAD sur les pages catalogue publiques. Entrepôt à Brantford (ON); expédition au Canada (frais en sus). Le PDF 2026/2027 imprime « --- » et renvoie au site pour les prix courants.",
                       "shipping_en": "CAD prices on public catalog pages. Warehouse in Brantford, ON; ships across Canada (freight extra). The 2026/2027 PDF catalog prints ‘---’ and points to the website for current prices.",
                       "method": "Pages catalogue publiques (tableaux HTML avec prix CAD); PDF sans montants"},
    "cobalt": {"id": "cobalt", "name": "Cobalt Industrial", "city": "Barrie (ON) et Calgary (AB)", "region": "CA",
               "site": "https://cobaltindustrial.ca", "currency": "CAD", "ships_qc": "oui",
               "shipping": "Quincaillerie H. Paulin : petites barres, cornières et feuilles. Expédition par transporteur (tarifs au panier) ou cueillette à Barrie et Calgary.",
               "shipping_en": "H. Paulin hardware-store stock: small bars, angles and sheets. Carrier shipping (rates at checkout) or pickup in Barrie and Calgary.",
               "method": "Pages catégorie publiques (prix CAD affichés)"},
    "metalpros": {"id": "metalpros", "name": "Metal Pros", "city": "Ottawa (ON)", "region": "CA",
                  "site": "https://www.metalpros.com", "currency": "CAD", "ships_qc": "oui",
                  "shipping": "Entrepôt à Ottawa; livraison partout au Canada (frais en sus). Prix du catalogue public au pied ou au pi²; coupe et autres frais en sus. Chutes / offcuts et lots aléatoires non ajoutés (surplus).",
                  "shipping_en": "Warehouse in Ottawa; ships across Canada (freight extra). Public catalogue prices per foot or per sq ft; cutting and other fees extra. Offcuts and random-length bundles not added (surplus).",
                  "method": "Outil de prix public (quote.metalpros.com) : GET /api/materials/getdbmaterial, le même que la page catalogue"},
    "pmabitibi": {"id": "pmabitibi", "name": "Pièces et Matériaux Abitibi", "city": "Rivière-Héva (QC)", "region": "QC",
                  "site": "https://www.pmabitibi.com", "currency": "CAD", "ships_qc": "cueillette",
                  "shipping": "Cueillette à Rivière-Héva (Abitibi). Prix affichés avant taxes, coupe comprise sur l’acier. Largeur de la tôle profilée non publiée.",
                  "shipping_en": "Pickup in Rivière-Héva (Abitibi). Posted prices before tax; cutting included on bar and tube. Profiled-sheet width is not published.",
                  "method": "Tableaux de prix publics (pages HTML /tole et /acier)"},
    "knifemaker": {"id": "knifemaker", "name": "KnifeMaker", "city": "Brisco (C.-B.)", "region": "CA",
                   "site": "https://www.knifemaker.ca", "currency": "CAD", "ships_qc": "oui",
                   "shipping": "Barres et feuilles de spécialité (aciers à outils, titane, laiton, cuivre). Expédition au Canada depuis Brisco (C.-B.).",
                   "shipping_en": "Specialty bar and sheet (tool steels, titanium, brass, copper). Ships across Canada from Brisco, BC.",
                   "method": "Vitrine Shopify publique (products.json des collections métal)"},

}

# Suppliers we checked that do not publish prices, or that we cannot read politely.
SUPPLIERS_STATIC = [
    {"name": "Metal Supermarkets", "city": "Ottawa (ON), dessert Gatineau — aucun magasin au Québec", "status": "sur_demande",
     "url": "https://www.metalsupermarkets.com/location/ottawa/", "note": "Aucun magasin au Québec (localisateur officiel); le plus proche est à Ottawa. Pas de prix publics lisibles : soumission en magasin ou en ligne.",
     "note_en": "No Quebec store (official locator); closest is Ottawa. No readable public prices: quote in store or online."},
    {"name": "Russel Metals", "city": "Québec (plusieurs centres)", "status": "sur_demande",
     "url": "https://www.russelmetals.com/", "note": "Centre de service : prix sur soumission. Le Guide des produits Acier Leroux / Métaux Russel (PDF public) donne dimensions et poids, sans prix.",
     "note_en": "Service centre: quoted prices. The public Acier Leroux / Russel Metals Products Guide PDF lists sizes and weights, not prices."},
    {"name": "Acier Leroux (Leroux Steel)", "city": "Boucherville et régions", "status": "sur_demande",
     "url": "https://www.russelmetals.com/wp-content/uploads/centres-de-service-guide-des-produits.pdf", "note": "Guide de produits PDF public (dimensions/poids seulement, aucun prix). Prix sur soumission.",
     "note_en": "Public product-guide PDF (sizes/weights only, no prices). Quote only."},
    {"name": "Acier Picard", "city": "Lévis", "status": "sur_demande",
     "url": "https://www.acierpicard.com/", "note": "Prix sur demande. Le carnet de références AQM / Acier Majeau (PDF) est un guide de dimensions, sans prix.",
     "note_en": "Quote only. The AQM / Acier Majeau reference catalog PDF is a dimension guide, with no prices."},
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
     "url": "https://www.homedepot.ca/", "note": "Protection anti-robot (aucune réponse) : non lu, pas de contournement. Pas de catalogue PDF de métal en stock trouvé; les extraits des moteurs de recherche ne sont pas ingérés.",
     "note_en": "Bot protection (no response): not read, no workaround. No metal-stock price-list PDF found; search-engine snippets are not ingested."},
    {"name": "Cangard Supplies", "city": "Canada", "status": "bloque",
     "url": "https://cangardsupplies.com/", "note": "robots.txt interdit les robots génériques : non lu.", "note_en": "robots.txt disallows generic bots: not read."},
    {"name": "RONA / Lowe’s / BMR", "city": "Magasins QC", "status": "bloque",
     "url": "https://www.rona.ca/", "note": "Prix publics, mais protection anti-robot (RONA et Lowe’s refusent la connexion, BMR répond 403) : non lus, pas de contournement. Pas de catalogue PDF de métal en stock trouvé.",
     "note_en": "Public prices, but bot protection (RONA and Lowe’s refuse the connection, BMR answers 403): not read, no workaround. No metal-stock price-list PDF found."},
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
    {"name": "Amazon.ca", "city": "En ligne", "status": "non_couvert",
     "url": "https://www.amazon.ca/", "note": "Pas d’aspiration (conditions d’Amazon). Liens affiliés possibles plus tard, si approuvés.",
     "note_en": "Not scraped (Amazon terms). Affiliate links possible later, if approved."},
    {"name": "McMaster-Carr", "city": "Elmhurst (IL, É.-U.), expédie au Canada en USD", "status": "bloque",
     "url": "https://www.mcmaster.com/", "note": "Ils indiquent que les prix sont dans leurs catalogues. Le catalogue imprimé 132 (2026, ~4 500 p.) n’est pas un PDF public (envoi sélectif aux clients). Le « catalogue en ligne » est le site : robots.txt interdit /catalog/, les PDF (/*/pdf) et les points de prix dynamiques (ItmPrsnttnDynamicDat.aspx, /mv). L’API et le punchout exigent un compte client approuvé. Non lu, pas de contournement.",
     "note_en": "They say pricing is in their catalogs. Printed Catalog 132 (2026, ~4,500 pp.) is not a public PDF (mailed selectively to customers). The ‘online catalog’ is the website: robots.txt disallows /catalog/, PDFs (/*/pdf) and the dynamic price endpoints (ItmPrsnttnDynamicDat.aspx, /mv). The API and punchout need an approved customer account. Not read, no workaround."},
    {"name": "Midwest Steel & Aluminum", "city": "Minneapolis (MN, É.-U.)", "status": "non_couvert",
     "url": "https://www.midweststeelsupply.com/", "note": "Boutique de coupe sur mesure; robots OK, mais le prix n’apparaît pas dans le HTML public (calculé après choix des dimensions). Pas de liste PDF. Non ajouté plutôt que deviner.",
     "note_en": "Cut-to-size shop; robots OK, but the price is not in the public HTML (calculated after size is chosen). No PDF price list. Not added rather than guess."},
    {"name": "Canadian Tire", "city": "Magasins au Canada (dont QC)", "status": "bloque",
     "url": "https://www.canadiantire.ca/", "note": "Prix publics en magasin/ligne, mais protection Akamai pour notre robot : non lu, pas de contournement. Pas de catalogue PDF de métal en stock trouvé.",
     "note_en": "Public in-store/online prices, but Akamai bot protection for our bot: not read, no workaround. No metal-stock price-list PDF found."},
    {"name": "Lordco Auto Parts", "city": "C.-B. (magasins à l’ouest)", "status": "non_couvert",
     "url": "https://lordco.com/", "note": "Quelques pièces de métal de quincaillerie (ex. cornière Paulin 1/8 × 1 × 36 po à 13,99 $ CAD) ont un prix public sur la fiche, sans catalogue ou liste téléchargeable. Non aspiré en masse.",
     "note_en": "A few hardware-store metal SKUs (e.g. Paulin 1/8 × 1 × 36 in angle at CA$13.99) have a public product-page price, but no downloadable catalog. Not bulk-crawled."},
    {"name": "ArcelorMittal Dofasco", "city": "Hamilton (ON) — usine", "status": "non_couvert",
     "url": "https://ec.dofasco.ca/EC-B2B-Public-Files/Price%20Book%20-%20ENGLISH.pdf", "note": "Livre « Products & Prices » public (en vigueur 1er janv. 2027) : extra en CAD/cwt FOB usine pour bobines (commande typique ≥ 2 master coils). Pas de prix de base publié, donc pas un prix de tôle au détail comparable.",
     "note_en": "Public ‘Products & Prices’ book (effective 1 Jan 2027): CAD/cwt extras FOB mill for coils (typical order ≥ 2 master coils). No published base selling price, so not a comparable retail sheet price."},
    {"name": "AQM / Acier Majeau", "city": "Québec", "status": "sur_demande",
     "url": "https://www.aciermajeau.com/", "note": "Carnet de références (éd. 2, 2008/2020) : guide de dimensions et de poids, aucun prix de vente. Prix sur soumission.",
     "note_en": "Reference handbook (ed. 2, 2008/2020): size and weight guide, no selling prices. Quote only."},
    {"name": "Fraser Valley Steel & Wire", "city": "Abbotsford (C.-B.)", "status": "bloque",
     "url": "https://fvstar.ca/wp-content/uploads/2026/06/SteelProductsCatalog_v2026.4.pdf", "note": "Catalogue produits 2026 annoncé (dimensions/poids, pas une liste de prix). Notre GET du catalogue et du guide de référence PDF (FVSTAR_SteelRefGuide_v2.0.pdf) a reçu HTTP 202 (défi) : non contourné. Liste mensuelle de rebar sur demande seulement.",
     "note_en": "2026 product catalog is advertised (sizes/weights, not a price list). Our GET of the catalog and of the reference-guide PDF (FVSTAR_SteelRefGuide_v2.0.pdf) received HTTP 202 (challenge): not bypassed. Monthly rebar list is request-only."},
    {"name": "Nova Metals Ltd", "city": "Stony Plain (AB)", "status": "sur_demande",
     "url": "https://novametals.ca/", "note": "Fourniture de métal sur place, aucun catalogue ou prix public. À ne pas confondre avec l’atelier Novametal de Lévis (QC).",
     "note_en": "Walk-in metal supply, no public catalog or prices. Not the Novametal machine shop in Lévis, QC."},
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


# ---------------------------------------------------------------------------
# Aircraft Spruce Canada — public catalog pages (the PDF prints "---")
# ---------------------------------------------------------------------------
AS_PAGES = [
    # aluminum sheet
    ("/catalog/mepages/3003_alsheet.php", "sheet"),
    ("/catalog/mepages/5052H_alsheet.php", "sheet"),
    ("/catalog/mepages/alumsheet_6061.php", "sheet"),
    ("/catalog/mepages/alumsheet_6061t4.php", "sheet"),
    ("/catalog/mepages/alumsheet_6061t6.php", "sheet"),
    ("/catalog/mepages/alumsheet_2024.php", "sheet"),
    ("/catalog/mepages/alumsheet_2024t3.php", "sheet"),
    ("/catalog/mepages/alumsheet_7075.php", "sheet"),
    ("/catalog/mepages/alumsheet_7075t6.php", "sheet"),
    # aluminum bar / tube / angle
    ("/catalog/mepages/6061t6.php", "flat bar"),
    ("/catalog/mepages/alumround6061t6.php", "round bar"),
    ("/catalog/mepages/alumtube_6061t6.php", "tube"),
    ("/catalog/mepages/alumtubing-sq.php", "square tube"),
    ("/catalog/mepages/alumtube_6061_0.php", "tube"),
    ("/catalog/mepages/alumtube_5052.php", "tube"),
    ("/catalog/mepages/3003versatube.php", "tube"),
    ("/catalog/mepages/alumangle3.php", "angle"),
    ("/catalog/mepages/alumbar.php", "flat bar"),
    ("/catalog/mepages/alumround.php", "round bar"),
    ("/catalog/mepages/alumtube_2024.php", "tube"),
    ("/catalog/mepages/alumangle.php", "angle"),
    # steel / stainless
    ("/catalog/mepages/4130sheet.php", "sheet"),
    ("/catalog/mepages/4130strips.php", "flat bar"),
    ("/catalog/mepages/4130rod.php", "round bar"),
    ("/catalog/mepages/4130square.php", "tube"),
    ("/catalog/mepages/4130tubing_un1.php", "tube"),
    ("/catalog/mepages/stainlesstubing.php", "tube"),
    ("/catalog/mepages/stainlessrod304.php", "round bar"),
    ("/catalog/mepages/4340rod.php", "round bar"),
    ("/catalog/mepages/e4340flatsteel.php", "flat bar"),
]


def _as_money(cell):
    m = re.search(r"\$\s*([\d,]+(?:\.\d{1,2})?)", cell or "")
    return float(m.group(1).replace(",", "")) if m else None


def _as_decode(resp):
    """Aircraft Spruce pages declare iso-8859-1 and use Windows-1252 foot marks (0x92)."""
    raw = resp.content
    if re.search(br"charset\s*=\s*(iso-8859-1|windows-1252)", raw[:4000], re.I):
        return raw.decode("windows-1252", errors="replace")
    return resp.text


def _as_sheet_size(s):
    """Parse sheet sizes like 4x12 feet, including typographic foot marks, as inches."""
    if not s:
        return None, None
    t = (s.replace("\u00d7", "x").replace("X", "x")
         .replace("\u2032", "'").replace("\u2019", "'").replace("\u2018", "'").replace("\u00b4", "'")
         .replace("\u2033", '"').replace("\u201d", '"').replace("\ufffd", "'"))
    # Feet only when a foot mark or the word ft/feet is present (4130 "6 x 12" is inches).
    m = re.search(r"(\d+(?:\.\d+)?)\s*'\s*x\s*(\d+(?:\.\d+)?)\s*'?", t, re.I)
    if m:
        a, b = float(m.group(1)) * 12, float(m.group(2)) * 12
        return min(a, b), max(a, b)
    m = re.search(r"(\d+(?:\.\d+)?)\s*x\s*(\d+(?:\.\d+)?)\s*(?:ft|feet)\b", t, re.I)
    if m:
        a, b = float(m.group(1)) * 12, float(m.group(2)) * 12
        return min(a, b), max(a, b)
    m = re.search(r"(\d+(?:\.\d+)?)\s*(?:in|\")?\s*x\s*(\d+(?:\.\d+)?)\s*(?:in|\")?", t, re.I)
    if m:
        a, b = float(m.group(1)), float(m.group(2))
        if 0 < a <= 144 and 0 < b <= 144:
            return min(a, b), max(a, b)
    return None, None


def _as_length_in(s):
    if not s:
        return None
    t = s.replace("′", "'").replace("’", "'")
    m = re.search(r"(\d+(?:\.\d+)?)\s*(?:ft|feet|')\b", t, re.I)
    if m:
        return float(m.group(1)) * 12
    m = re.search(r"(\d+(?:\.\d+)?)\s*(?:in|\"|po)\b", t, re.I)
    if m:
        return float(m.group(1))
    return None


def fetch_aircraftspruce(fx, quick=False):
    """Public HTML catalog pages on aircraftspruce.ca (CAD). The downloadable PDF
    catalog leaves every price as '---' and tells the reader to use the website."""
    sup = SUPPLIERS["aircraftspruce"]
    pages = AS_PAGES[:1] if quick else AS_PAGES
    rows = []
    note = "Prix courant sur la page catalogue publique (le PDF imprime « --- »)"
    for path, hint in pages:
        url = sup["site"] + path
        soup = BeautifulSoup(_as_decode(get(url)), "lxml")
        h = soup.find("h1") or soup.find("title")
        title = (h.get_text(" ", strip=True) if h else path).split("|")[0].strip()
        for table in soup.find_all("table"):
            headers = []
            for tr in table.find_all("tr"):
                cells = [c.get_text(" ", strip=True) for c in tr.find_all(["th", "td"])]
                if not cells:
                    continue
                lows = [c.lower() for c in cells]
                if any("price" in c or c == "pn" or "part no" in c or "part number" in c for c in lows) and not any(_as_money(c) for c in cells):
                    headers = lows
                    continue
                price = next((p for c in cells if (p := _as_money(c))), None)
                if not price:
                    continue
                blob = " ".join(cells)
                if re.search(r"please (?:note|call)|call for price|discount of|hardenability|sold in the thicknesses|cosmetic blemish|cutting charges", blob, re.I):
                    continue
                if max((len(c) for c in cells), default=0) > 120:
                    continue
                col = {headers[i]: cells[i] for i in range(min(len(headers), len(cells)))} if headers else {}
                size = col.get("size") or col.get("dimensions") or ""
                thk_cell = next((col[k] for k in col if "thickness" in k or k in ("in.", "thk", "thick")), "")
                length_cell = next((col[k] for k in col if "length" in k or k in ("lg", "long")), "")
                pn = next((col[k] for k in col if k in ("pn", "p/n", "part no.", "part no", "part number")), "")
                text = " ".join(x for x in (title, *cells) if x and x.lower() not in ("quantity", "buy", "add"))
                w_in = l_in = length_ft = thickness_in = None
                if "sheet" in hint or "sheet" in title.lower() or "plate" in title.lower():
                    w_in, l_in = _as_sheet_size(size)
                    if w_in is None:
                        w_in, l_in = _as_sheet_size(" ".join(cells))
                    if thk_cell:
                        thickness_in, _, _ = N.parse_thickness(thk_cell, N.detect_family(title) or "aluminium")
                    if w_in and l_in:
                        # small pieces (typical 4130 coupons) are labelled in inches
                        if max(w_in, l_in) <= 24:
                            size_label = f"{w_in:g} × {l_in:g} po"
                        else:
                            size_label = f"{w_in/12:g} × {l_in/12:g} pi"
                    else:
                        size_label = size or ""
                    form_hint = "sheet"
                else:
                    form_hint = hint
                    length_in = _as_length_in(length_cell) or _as_length_in(size) or _as_length_in(text)
                    if length_in:
                        length_ft = length_in / 12.0
                    size_label = size or (length_cell and f"{length_cell}") or size_label_from_title(text)
                r = make_row(supplier=sup, text=text, price=price, currency="CAD", url=url, fx=fx,
                             form_hint=form_hint, thickness_in=thickness_in, width_in=w_in, length_in=l_in,
                             length_ft=length_ft, size_label=size_label, notes=note + (f"; PN {pn}" if pn else ""))
                if r:
                    rows.append(r)
    return rows


# ---------------------------------------------------------------------------
# Cobalt Industrial — public category pages (H. Paulin hardware-store stock)
# ---------------------------------------------------------------------------
COBALT_CATEGORIES = [
    "/categories/fasteners-hardware/metal-stock-tubing/aluminum-angles",
    "/categories/fasteners-hardware/metal-stock-tubing/flat-aluminum",
    "/categories/fasteners-hardware/metal-stock-tubing/flat-steel",
    "/categories/fasteners-hardware/metal-stock-tubing/flat-tubing-aluminum",
    "/categories/fasteners-hardware/metal-stock-tubing/sheet-metal",
    "/categories/fasteners-hardware/metal-stock-tubing/steel-angles",
    "/categories/fasteners-hardware/metal-stock-tubing/square-tubing-aluminum",
    "/categories/fasteners-hardware/metal-stock-tubing/square-tubing-zinc",
    "/categories/fasteners-hardware/metal-stock-tubing/square-tubes-zinc",
    "/categories/fasteners-hardware/metal-stock-tubing/round-tubing-zinc",
    "/categories/fasteners-hardware/metal-stock-tubing/slotted-steel-angles",
]


def _cobalt_dims(title):
    """Parse '1/8" X 1" X 36"' or '6X18 16GA' or '24" X 0.025" X 8"' style titles."""
    t = title.replace("×", "x").replace("X", "x")
    # 24" X 0.025" X 8" aluminum sheet: mid value is thickness if it's a small decimal
    m = re.search(
        r"(\d+(?:\s+\d+/\d+|\.\d+|/\d+)?)\s*(?:\"|''|in)?\s*x\s*"
        r"(\d+(?:\s+\d+/\d+|\.\d+|/\d+)?)\s*(?:\"|''|in)?\s*x\s*"
        r"(\d+(?:\s+\d+/\d+|\.\d+|/\d+)?)\s*(?:\"|''|in|ft|FT)?",
        t, re.I)
    if not m:
        m = re.search(
            r"(\d+(?:\s+\d+/\d+|\.\d+|/\d+)?)\s*(?:\"|''|in)?\s*x\s*"
            r"(\d+(?:\s+\d+/\d+|\.\d+|/\d+)?)\s*(?:\"|''|in|ft|FT)?",
            t, re.I)
        nums = [N._num(x) for x in m.groups()] if m else []
    else:
        nums = [N._num(x) for x in m.groups()]
    gauge = None
    gm = re.search(r"(\d+)\s*(?:GA|GAUGE|ga)\b", t, re.I)
    if gm:
        gauge = int(gm.group(1))
    length_in = None
    fm = re.search(r"(\d+(?:\.\d+)?)\s*(?:FT|feet)\b", t, re.I)
    if fm:
        length_in = float(fm.group(1)) * 12
    return nums, gauge, length_in


def fetch_cobalt(fx, quick=False):
    sup = SUPPLIERS["cobalt"]
    cats = COBALT_CATEGORIES[:2] if quick else COBALT_CATEGORIES
    rows, seen = [], set()
    for path in cats:
        url = sup["site"] + path
        soup = BeautifulSoup(get(url).text, "lxml")
        for art in soup.select("article.product-item"):
            a = art.select_one(".product-item-title a") or art.find("a", href=True)
            price_el = art.select_one(".product-item-price")
            if not (a and price_el):
                continue
            title = a.get_text(" ", strip=True)
            href = a.get("href") or ""
            purl = href if href.startswith("http") else (sup["site"] + href)
            if purl in seen:
                continue
            seen.add(purl)
            pm = re.search(r"([\d]+(?:[.,]\d{2})?)", price_el.get_text())
            if not pm:
                continue
            price = float(pm.group(1).replace(",", "."))
            avail = " ".join(p.get_text(" ", strip=True) for p in art.select(".product-item-availability, .product-item-pickup-note"))
            nums, gauge, length_from_ft = _cobalt_dims(title)
            family = N.detect_family(title)
            if family is None and re.search(r"\bzinc\b", title, re.I) and not re.search(r"alumin", title, re.I):
                family = "acier"
                text = title + " zinc-plated steel"
            else:
                text = title
            thickness_in = width_in = length_in = length_ft = None
            hint = ""
            low = title.lower()
            if "sheet" in low or "sheet metal" in low:
                hint = "sheet"
                if gauge:
                    gauges = (N.GAUGE_GALV if "galv" in low else
                              N.GAUGE_STEEL if family == "acier" else
                              N.GAUGE_AL if family == "aluminium" else N.GAUGE_STEEL)
                    thickness_in = gauges.get(gauge)
                if len(nums) >= 2 and nums[0] is not None:
                    # 6x18 16ga, or 24 x 0.025 x 8
                    if len(nums) == 3 and nums[1] is not None and nums[1] < 1:
                        thickness_in = thickness_in or nums[1]
                        width_in, length_in = nums[0], nums[2]
                    else:
                        width_in, length_in = nums[0], nums[1]
                        if width_in and length_in and width_in > length_in:
                            width_in, length_in = length_in, width_in
            elif "angle" in low:
                hint = "angle"
                if nums:
                    thickness_in = nums[0]
                if length_from_ft:
                    length_ft = length_from_ft / 1.0 if length_from_ft > 15 else length_from_ft  # already inches
                    length_ft = length_from_ft / 12.0
                elif len(nums) >= 3 and nums[-1] and nums[-1] >= 12:
                    length_in = nums[-1]
                    length_ft = length_in / 12.0
            elif "flat tube" in low or "flat tubing" in low:
                hint = "rectangular tube"
                if length_from_ft:
                    length_ft = length_from_ft / 12.0
                elif len(nums) >= 3:
                    length_ft = (nums[-1] / 12.0) if nums[-1] >= 12 else nums[-1]
            elif "flat" in low:
                hint = "flat bar"
                if nums:
                    thickness_in = nums[0]
                if length_from_ft:
                    length_ft = length_from_ft / 12.0
                elif len(nums) >= 3 and nums[-1] and nums[-1] >= 12:
                    length_ft = nums[-1] / 12.0
            elif "tube" in low or "tubing" in low:
                hint = "square tube" if "square" in low else "tube"
                if length_from_ft:
                    length_ft = length_from_ft / 12.0
                elif len(nums) >= 3 and nums[-1] and nums[-1] >= 12:
                    length_ft = nums[-1] / 12.0
            size_label = size_label_from_title(title)
            if width_in and length_in:
                size_label = f"{width_in:g} × {length_in:g} po"
            elif length_ft and not size_label:
                size_label = f"{length_ft:g} pi"
            size_label = size_label or title
            r = make_row(supplier=sup, text=text, price=price, currency="CAD", url=purl, fx=fx,
                         form_hint=hint, family=family, thickness_in=thickness_in, width_in=width_in,
                         length_in=length_in, length_ft=length_ft, size_label=size_label,
                         availability=avail, notes="H. Paulin; quincaillerie, petites longueurs")
            if r:
                if gauge and not r.get("gauge"):
                    r["gauge"] = gauge
                rows.append(r)
    return rows


MP_MATERIALS = [
    "ALUMINUM", "BRASS", "BRONZE", "CHROME", "COPPER", "GALVANIZED/ SATIN",
    "STAINLESS", "STEEL", "TOOL/ KNIFE MAKING",
]
MP_SKIP = re.compile(
    r"NO AVAILABILITY|NOT AVAILABLE|\*{0,2}OFFCUT\b|HONEYCOMB|GRATING|GRIP STRUT|SHUR GRIP|LADDER RUNGS",
    re.I,
)
_MP_DIM = re.compile(r"(\d+(?:\.\d+)?)\s*(mm\b|\")", re.I)


def _mp_num(text, *labels):
    for lab in labels:
        m = re.search(r"(\d+(?:\.\d+)?)\s*(mm\b|\"?)\s*" + lab, text, re.I)
        if m:
            v = float(m.group(1))
            if (m.group(2) or "").lower().startswith("mm"):
                v /= 25.4
            return v
    return None


def _mp_nums(text):
    out = []
    for m in _MP_DIM.finditer(text):
        v = float(m.group(1))
        if m.group(2).lower().startswith("mm"):
            v /= 25.4
        out.append(v)
    return out


def _mp_dims(desc, form):
    """Parse published inches (or mm) into thickness / size_label / weight-per-foot args."""
    nums = _mp_nums(desc)
    dia = _mp_num(desc, r"DIA\.?")
    af = _mp_num(desc, r"ACROSS\s+FLATS")
    od = _mp_num(desc, r"OD")
    id_ = _mp_num(desc, r"ID")
    wall = _mp_num(desc, r"WALL")
    thick = _mp_num(desc, r"THICK")
    weight_args = {}
    thickness_in = None
    width_in = None
    size_label = ""
    if form in ("tole", "plaque", "feuille"):
        thickness_in = thick or (nums[-1] if nums else None)
        if thickness_in:
            size_label = f"{thickness_in:g} po"
    elif form == "barre_ronde":
        dia = dia or (nums[0] if nums else None)
        if dia:
            thickness_in = dia
            size_label = f"{dia:g} po dia"
            weight_args = {"dia": dia}
    elif form == "barre_hex":
        af = af or (nums[0] if nums else None)
        if af:
            thickness_in = af
            size_label = f"{af:g} po plats"
            weight_args = {"af": af}
    elif form in ("barre_plate", "barre_carree"):
        if len(nums) >= 2:
            thickness_in, width_in = nums[0], nums[1]
            size_label = f"{thickness_in:g} × {width_in:g} po"
            weight_args = {"t": thickness_in, "w": width_in}
        elif len(nums) == 1 and form == "barre_carree":
            thickness_in = width_in = nums[0]
            size_label = f"{thickness_in:g} × {width_in:g} po"
            weight_args = {"t": thickness_in, "w": width_in}
    elif form == "corniere" and len(nums) >= 3:
        leg1, leg2, thk = nums[0], nums[1], nums[2]
        thickness_in = thk
        size_label = f"{leg1:g} × {leg2:g} × {thk:g} po"
        weight_args = {"leg1": leg1, "leg2": leg2, "t": thk}
    elif form in ("tube_rond", "tuyau"):
        if od and (id_ or wall):
            thickness_in = wall or ((od - id_) / 2 if id_ else None)
            parts = [f"{od:g} po OD"]
            if id_:
                parts.append(f"{id_:g} po ID")
            if wall:
                parts.append(f"paroi {wall:g} po")
            size_label = ", ".join(parts)
            weight_args = {"od": od, "id_": id_, "wall": wall}
        elif len(nums) >= 2:
            od, id_ = nums[0], nums[1]
            wall = nums[2] if len(nums) >= 3 else (od - id_) / 2
            thickness_in = wall
            size_label = f"{od:g} po OD, {id_:g} po ID"
            weight_args = {"od": od, "id_": id_, "wall": wall}
    elif form == "tube_carre" and len(nums) >= 3:
        w, _, wall = nums[0], nums[1], nums[2]
        thickness_in = wall
        size_label = f"{nums[0]:g} × {nums[1]:g} × {wall:g} po"
        weight_args = {"w": w, "wall": wall}
    elif form == "tube_rect" and len(nums) >= 3:
        w, h, wall = nums[0], nums[1], nums[2]
        thickness_in = wall
        size_label = f"{w:g} × {h:g} × {wall:g} po"
        weight_args = {"w": w, "h": h, "wall": wall}
    elif nums:
        size_label = " × ".join(f"{n:g}" for n in nums[:4]) + " po"
        thickness_in = nums[-1] if form in ("tole", "plaque") else nums[0]
    return thickness_in, width_in, size_label, weight_args


def _mp_price(val):
    try:
        t = str(val or "").replace(",", "").strip()
        m = re.match(r"-?\d+(?:\.\d+)?", t)
        return float(m.group(0)) if m else 0.0
    except (TypeError, ValueError):
        return 0.0


def fetch_metalpros(fx, quick=False):
    """Public quote-tool catalogue: GET /api/materials/getdbmaterial (no POST)."""
    from urllib.parse import quote, urlencode
    sup = SUPPLIERS["metalpros"]
    quote_home = "https://quote.metalpros.com/"
    page = get(quote_home)
    m = re.search(r'data-version=["\']([^"\']+)["\']', page.text)
    ver = m.group(1) if m else ""
    mats = MP_MATERIALS[:2] if quick else MP_MATERIALS
    rows, seen = [], set()
    for material in mats:
        params = {"material": material}
        if ver:
            params["v"] = ver
        url = "https://quote.metalpros.com/api/materials/getdbmaterial?" + urlencode(params)
        data = get(url, timeout=60).json()
        for item in data.get("results") or []:
            iid = item.get("id")
            if iid in seen:
                continue
            seen.add(iid)
            desc = html.unescape(str(item.get("description") or "")).strip()
            unit_raw = str(item.get("unit") or "").strip().lower()
            price = _mp_price(item.get("price"))
            if not desc or price <= 0 or MP_SKIP.search(desc):
                continue
            if N.EXCLUDE.search(desc):
                continue
            if unit_raw == "sq ft":
                if not re.search(r"\b(sheet|plate|sht|t[ôo]le|plaque)\b", desc, re.I):
                    continue
                unit = "sqft"
            elif unit_raw == "ft":
                unit = "ft"
            else:
                # Offcuts (PC), random bundles (BDL) and specialty each-pieces are not regular stock.
                continue
            form = N.detect_form(desc)
            if not form:
                continue
            thickness_in, width_in, size_label, wargs = _mp_dims(desc, form)
            # "SHEET 7.000\"" is not a usable thickness (likely a typo or a different field).
            if (re.search(r"\bsheet\b", desc, re.I) and not re.search(r"\bplate\b", desc, re.I)
                    and thickness_in and thickness_in > 1.01):
                continue
            family = N.detect_family(desc)
            weight_lb = N.weight_per_ft_lb(family, form, **wargs) if (unit == "ft" and family and wargs) else None
            stock = _mp_price(item.get("stock"))
            sku = item.get("internalId") or iid
            purl = f"https://quote.metalpros.com/?search={quote(str(sku))}"
            r = make_row(
                supplier=sup, text=desc, price=price, currency="CAD", url=purl, fx=fx,
                unit=unit, form_hint="", family=family, thickness_in=thickness_in,
                width_in=width_in, size_label=size_label or desc, weight_lb=weight_lb,
                availability="en stock" if stock > 0 else "stock 0",
                source_updated=f"catalogue en ligne {ver}" if ver else "",
                notes="Prix catalogue public (au pied ou au pi²); coupe en sus",
            )
            # Drop derived $/lb that can only be a placeholder or a bad size parse
            # (e.g. $1.00/ft on 7.5" DOM, $31/ft on 14" stainless), not typical retail.
            if r and r.get("price_per_lb_cad") is not None and r["price_per_lb_cad"] < 1.00:
                continue
            if r:
                rows.append(r)
    return rows



def fetch_pmabitibi(fx, quick=False):
    return S5.fetch_pmabitibi(get, make_row, SUPPLIERS["pmabitibi"], fx, quick=quick)


def fetch_knifemaker(fx, quick=False):
    return S5.fetch_knifemaker(get, make_row, SUPPLIERS["knifemaker"], fx, quick=quick)


FETCHERS = {
    "metalsrus": fetch_metalsrus, "metalsdepot": fetch_metalsdepot, "unitedstainless": fetch_unitedstainless,
    "mercier40": fetch_mercier40, "princessauto": fetch_princessauto, "millennium": fetch_millennium,
    "nationalsalvage": fetch_nationalsalvage,
    "aluminox": fetch_aluminox, "forcesinc": fetch_forcesinc, "valmont": fetch_valmont,
    "acierterrebonne": fetch_acierterrebonne, "wemachine": fetch_wemachine, "smithmetal": fetch_smithmetal,
    "optikutz": fetch_optikutz, "recyborg": fetch_recyborg, "lasersupply": fetch_lasersupply,
    "aircraftspruce": fetch_aircraftspruce, "cobalt": fetch_cobalt,
    "metalpros": fetch_metalpros,
    "pmabitibi": fetch_pmabitibi, "knifemaker": fetch_knifemaker,
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
        if not r["price_per_lb_cad"] or r["supplier"] == "unitedstainless" or not r.get("in_catalogue"):
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
        prev = read_latest(OUT)
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
        write_latest(OUT, prev)
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
    write_latest(OUT, latest)
    write_history(prev.get("rows", []), all_rows, today)
    write_index(all_rows, today)
    print(f"total {len(all_rows)} rows -> {OUT/'latest.json'}")


if __name__ == "__main__":
    main()

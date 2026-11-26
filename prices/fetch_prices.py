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
                  "shipping": "Cueillette à Champlain (Mauricie). Plaques neuves « coin rouge » (décapé huilé), nuance non précisée.",
                  "shipping_en": "Pickup in Champlain (Mauricie). New ‘red corner’ plates (pickled & oiled), grade not stated.",
                  "method": "Page catégorie publique"},
    "princessauto": {"id": "princessauto", "name": "Princess Auto", "city": "Magasins au Canada (dont QC)", "region": "CA",
                     "site": "https://www.princessauto.com", "currency": "CAD", "ships_qc": "oui",
                     "shipping": "Petites feuilles 24 × 48 po; cueillette en magasin ou expédition.",
                     "shipping_en": "Small 24 × 48 in sheets; store pickup or shipping.",
                     "method": "Pages produit publiques"},
    "millennium": {"id": "millennium", "name": "Millennium Alloys", "city": "Colombie-Britannique", "region": "CA",
                   "site": "https://millenniumalloys.ca", "currency": "CAD", "ships_qc": "a_confirmer",
                   "shipping": "Prix publiés, commande par téléphone; expédition vers le Québec à confirmer.",
                   "shipping_en": "Published prices, order by phone; shipping to Quebec to be confirmed.",
                   "method": "API publique WooCommerce Store (Crawl-delay 30 s respecté)"},
    "nationalsalvage": {"id": "nationalsalvage", "name": "National Salvage", "city": "Lethbridge (AB)", "region": "CA",
                        "site": "https://shop.nationalsalvage.ca", "currency": "CAD", "ships_qc": "non",
                        "shipping": "Cueillette à Lethbridge (Alberta) seulement : repère de prix canadien, pas une source d’achat au Québec.",
                        "shipping_en": "Pickup in Lethbridge (Alberta) only: a Canadian price benchmark, not a Quebec buying option.",
                        "method": "Vitrine Shopify publique (products.json)"},
}

# Suppliers we checked that do not publish prices, or that we cannot read politely.
SUPPLIERS_STATIC = [
    {"name": "Metal Supermarkets", "city": "Montréal, Laval, Québec…", "status": "sur_demande",
     "url": "https://www.metalsupermarkets.com/", "note": "Pas de prix en ligne : soumission en magasin ou en ligne.",
     "note_en": "No online prices: quote in store or online."},
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
     "url": "https://www.onlinemetals.com/", "note": "HTTP 403 (protection anti-robot) : non lu, pas de contournement.",
     "note_en": "HTTP 403 (bot protection): not read, no workaround."},
    {"name": "Speedy Metals", "city": "É.-U.", "status": "bloque",
     "url": "https://www.speedymetals.com/", "note": "Connexion refusée à notre robot : non lu.", "note_en": "Connection refused to our bot: not read."},
    {"name": "Home Depot Canada", "city": "Magasins QC", "status": "bloque",
     "url": "https://www.homedepot.ca/", "note": "Protection anti-robot (aucune réponse) : non lu.", "note_en": "Bot protection (no response): not read."},
    {"name": "Cangard Supplies", "city": "Canada", "status": "bloque",
     "url": "https://cangardsupplies.com/", "note": "robots.txt interdit les robots génériques : non lu.", "note_en": "robots.txt disallows generic bots: not read."},
    {"name": "RONA / Canac / BMR", "city": "Magasins QC", "status": "non_couvert",
     "url": "https://www.rona.ca/", "note": "Petites feuilles de quincaillerie (24 × 36 po ou moins); pas encore relevées.",
     "note_en": "Small hardware-store sheets (24 × 36 in or less); not tracked yet."},
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


def fetch_metalsrus(fx, quick=False):
    sup = SUPPLIERS["metalsrus"]
    rows, seen = [], set()
    cols = MRU_COLLECTIONS[:2] if quick else MRU_COLLECTIONS
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
                rows.append(r)
            if quick and len(rows) > 10:
                break
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


FETCHERS = {
    "metalsrus": fetch_metalsrus, "metalsdepot": fetch_metalsdepot, "unitedstainless": fetch_unitedstainless,
    "mercier40": fetch_mercier40, "princessauto": fetch_princessauto, "millennium": fetch_millennium,
    "nationalsalvage": fetch_nationalsalvage,
}

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
    ap.add_argument("--rederive", action="store_true", help="recompute thickness/derived units of stored rows, no fetch")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "history").mkdir(exist_ok=True)
    today = dt.datetime.now(TZ).date().isoformat()
    prev = {}
    if (OUT / "latest.json").exists():
        prev = json.loads((OUT / "latest.json").read_text())
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
        (OUT / "latest.json").write_text(json.dumps(prev, ensure_ascii=False, indent=1))
        print(f"rederived {n} rows")
        return
    fx = fx_usdcad()
    all_rows, status = [], {}
    for sid, fn in FETCHERS.items():
        if args.only and sid not in args.only:
            all_rows += [r for r in prev.get("rows", []) if r["supplier"] == sid]
            if sid in prev.get("status", {}):
                status[sid] = prev["status"][sid]
            continue
        t0 = time.time()
        try:
            rows = fn(fx, quick=args.quick)
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
    (OUT / "latest.json").write_text(json.dumps(latest, ensure_ascii=False, indent=1))
    write_history(prev.get("rows", []), all_rows, today)
    write_index(all_rows, today)
    print(f"total {len(all_rows)} rows -> {OUT/'latest.json'}")


if __name__ == "__main__":
    main()

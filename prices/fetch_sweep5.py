"""Sweep-5 public price fetchers (26 Nov 2026).

  * Pièces et Matériaux Abitibi (pmabitibi.com) — HTML price tables in Rivière-Héva, QC
  * KnifeMaker (knifemaker.ca) — Shopify products.json, metal-stock collections only

Same rules as fetch_prices.py: public pages only, robots.txt honoured through
fetch_prices.get(), no login, no cart, no bot-wall bypass. Nothing is estimated:
"Prix sur demande" cells and per-foot custom rates without a length are skipped.
"""
import html
import re

from bs4 import BeautifulSoup

import fetch_more as M
import normalize as N

MONEY = re.compile(r"(\d+(?:[.,]\d+)?)\s*\$")
LEN_FT = re.compile(r"(\d+(?:[.,]\d+)?)\s*pi\b", re.I)

# Blade/tool steels, titanium sheet, brass/copper bar — not pins, belts, G10, kydex.
KM_COLLECTIONS = [
    "1075-carbon-steel", "1084-carbon-steel", "1095-carbon-steel",
    "154cm-stainless-blade-steel", "15n20", "416-stainless-bar", "440c-stainless",
    "80crv2-high-carbon-steel", "aeb-l-razor-steel", "cpm-s35vn-stainless",
    "brass-bar", "nitro-v", "o1-tool-steel", "stainless-blade-steel",
    "titanium", "tool-and-carbon-blade-steel", "w2", "copper-bar-and-pins",
]


def _money(s):
    s = (s or "").replace("\xa0", " ")
    if "demande" in s.lower() or not s.strip():
        return None
    m = MONEY.search(s)
    return float(m.group(1).replace(",", ".")) if m else None


def _header_len_ft(h):
    h = (h or "").replace("\xa0", " ")
    if re.search(r"l[\'’]unité|unite|unité", h, re.I):
        return "each"
    m = LEN_FT.search(h)
    return float(m.group(1).replace(",", ".")) if m else None


def parse_pma_tables(html_text, url, kind):
    """Yield dicts with desc, price, url, and length_ft or unit=each."""
    soup = BeautifulSoup(html_text, "lxml")
    rows = []
    for table in soup.find_all("table"):
        heading = ""
        prev = table.find_previous(["h2", "h3", "h4"])
        if prev:
            heading = prev.get_text(" ", strip=True)
        trs = table.find_all("tr")
        if len(trs) < 2:
            continue
        headers = [c.get_text(" ", strip=True) for c in trs[0].find_all(["th", "td"])]
        blob = " ".join(headers) + " " + heading
        if re.search(r"^vis à tôle$|^accessoires|^moulures", heading, re.I):
            continue
        if re.search(r"sur mesure", heading, re.I) and "pied linéaire" in blob.lower():
            continue
        col_kinds = [_header_len_ft(h) for h in headers]
        for tr in trs[1:]:
            cells = [c.get_text(" ", strip=True) for c in tr.find_all(["th", "td"])]
            if len(cells) < 2:
                continue
            if (kind == "tole"
                    and headers and headers[0].lower().startswith("longueur")):
                L = _header_len_ft(cells[0])
                p = _money(cells[1] if len(cells) > 1 else "")
                if L in (None, "each") or p is None:
                    continue
                rows.append({"heading": heading, "desc": heading, "length_ft": L,
                             "price": p, "url": url})
                continue
            name = " ".join(x for x in cells[:2] if x).strip() or heading
            if re.search(r"^treillis\b", name, re.I):
                continue
            for i, cell in enumerate(cells):
                if i < 2:
                    continue
                ck = col_kinds[i] if i < len(col_kinds) else None
                p = _money(cell)
                if p is None or ck is None:
                    continue
                rec = {"heading": heading, "desc": name, "price": p, "url": url}
                if ck == "each":
                    rec["unit"] = "each"
                else:
                    rec["length_ft"] = ck
                rows.append(rec)
    return rows



PMA_HINT = {
    "tube carré": ("acier", "square tube"),
    "tube rectangle": ("acier", "rectangular tube"),
    "tube rond": ("acier", "round tube"),
    "fer angle": ("acier", "angle"),
    "flat bar": ("acier", "flat bar"),
    "tige ronde": ("acier", "round bar"),
    "feuille": ("acier", "sheet"),
    "tôle": ("acier", "sheet"),
}


def _pma_hint(heading, desc):
    blob = f"{heading} {desc}".lower()
    if re.search(r"channel|armature|^grillage\b", blob):
        return None
    for key, val in PMA_HINT.items():
        if key in blob:
            return val
    return None


def fetch_pmabitibi(get, make_row, sup, fx, quick=False):
    rows = []
    pages = [("tole", "https://www.pmabitibi.com/tole")]
    if not quick:
        pages.append(("acier", "https://www.pmabitibi.com/acier"))
    for kind, url in pages:
        for item in parse_pma_tables(get(url).text, url, kind):
            desc = item["desc"]
            heading = item.get("heading") or desc
            # Spell out painted vs galvanized so EXCLUDE / detect_family stay consistent.
            if kind == "tole":
                if re.search(r"galvanis", heading, re.I):
                    desc = f"Tôle d'acier galvanisée {heading}"
                else:
                    desc = f"Tôle d'acier prépeinte {heading}"  # dropped by N.EXCLUDE on purpose
            hint = _pma_hint(heading, desc)
            if not hint:
                continue
            family, form_hint = hint
            kw = dict(
                supplier=sup, text=desc, price=item["price"], currency="CAD",
                url=item["url"], fx=fx, family=family, form_hint=form_hint,
                notes="Prix affiché avant taxes; cueillette à Rivière-Héva. Largeur de la tôle profilée non publiée.",
            )
            if item.get("length_ft"):
                kw["length_ft"] = item["length_ft"]
                kw["size_label"] = f"{item['desc']} — {item['length_ft']:g} pi"
            elif item.get("unit") == "each":
                area = M.parse_area(desc)
                if area:
                    kw["width_in"], kw["length_in"] = area
                    kw["size_label"] = f"{area[0]:g} × {area[1]:g} po"
            r = make_row(**kw)
            if r:
                rows.append(r)
    return rows


# thickness x width x length, optional "sheet" / "bar"
_KM_DIM = re.compile(
    r"(?P<t>\d+/\d+|\d+(?:\.\d+)?|\.\d+)\s*\"?\s*x\s*"
    r"(?P<w>\d+/\d+|\d+(?:\.\d+)?)\s*\"?\s*x\s*"
    r"(?P<l>\d+/\d+|\d+(?:\.\d+)?)\s*\"?",
    re.I,
)


def fetch_knifemaker(get, make_row, sup, fx, quick=False):
    """Parse KnifeMaker size variants (e.g. 1/8\" x 1.5\" x 12\") as flat bar or sheet.

    Titanium is published on the store but has no family in the CoupeFab catalogue, so it is skipped.
    Pins and kits are skipped. Nothing is estimated.
    """
    cols = KM_COLLECTIONS[:3] if quick else KM_COLLECTIONS
    products = M.shopify_products(get, sup["site"], cols)
    rows = []
    for p in products:
        title = html.unescape(p["title"]).strip()
        blob = f"{title} {p.get('product_type') or ''} {p.get('tags') or ''}"
        if re.search(r"\bpin\b|pinstock|washer|foil wrap|kit\b|powder\b|g-?10|kydex|micarta|titanium|6al", blob, re.I):
            continue
        family = N.detect_family(blob + " steel bar")  # "bar" alone is not a family; steel/stainless/brass/copper is
        if "brass" in blob.lower() or "laiton" in blob.lower():
            family = "laiton"
        elif "copper" in blob.lower() or "cuivre" in blob.lower():
            family = "cuivre"
        elif re.search(r"stainless|inox|\b440|\b154\b|aeb-l|magnacut|nitro-?v|s35", blob, re.I):
            family = "inox"
        elif re.search(r"steel|acier|carbon|1095|1084|1075|15n20|o-?1\b|d-?2\b", blob, re.I):
            family = "acier"
        if not family:
            continue
        purl = f"{sup['site']}/products/{p['handle']}"
        for v in p.get("variants") or []:
            try:
                price = float(v.get("price") or 0)
            except (TypeError, ValueError):
                continue
            if price <= 0:
                continue
            vt = html.unescape(v.get("title") or "")
            if vt in ("Default Title", "Default"):
                vt = ""
            text = f"{title} {vt}".strip()
            if re.search(r"\bpin\b", text, re.I):
                continue
            m = _KM_DIM.search(text.replace("″", '"').replace("“", '"').replace("”", '"'))
            if not m:
                continue
            t_in = N._num(m.group("t"))
            w_in = N._num(m.group("w"))
            l_in = N._num(m.group("l"))
            if not t_in or not w_in or not l_in or l_in < 6:
                continue
            is_sheet = bool(re.search(r"sheet|feuille", text, re.I)) or (w_in >= 6 and l_in >= 24)
            if is_sheet:
                r = make_row(
                    supplier=sup, text=text + " sheet", price=price, currency="CAD", url=purl, fx=fx,
                    family=family, form_hint="sheet", thickness_in=t_in, width_in=min(w_in, l_in),
                    length_in=max(w_in, l_in), size_label=f"{min(w_in,l_in):g} × {max(w_in,l_in):g} po",
                    notes="Feuille de spécialité (coutellerie); expédition au Canada depuis la C.-B.",
                    availability="en ligne" if v.get("available", True) else "rupture",
                )
            else:
                r = make_row(
                    supplier=sup, text=text + " flat bar", price=price, currency="CAD", url=purl, fx=fx,
                    family=family, form_hint="flat bar", thickness_in=t_in, width_in=w_in,
                    length_ft=l_in / 12.0, size_label=f"{t_in:g} × {w_in:g} × {l_in:g} po",
                    notes="Barre plate de spécialité (coutellerie); expédition au Canada depuis la C.-B.",
                    availability="en ligne" if v.get("available", True) else "rupture",
                )
            if r:
                r["buy_url"] = f"{purl}?variant={v['id']}"
                rows.append(r)
    return rows

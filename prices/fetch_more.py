"""Generic fetchers for public storefronts (Shopify products.json, WooCommerce Store API).

Added 26 Nov 2026 (coverage sweep). Same rules as fetch_prices.py: public JSON only,
robots.txt and Crawl-delay honoured through fetch_prices.get(), no login, no cart.
A product is kept only when the store publishes enough to identify it (metal family,
shape, size) and a length or sheet size, so a unit price can be computed. Nothing is
estimated: rows that would need a guess are skipped.
"""
import html
import re

import normalize as N

FORM_HINT = {"barre_ronde": "round bar", "barre_plate": "flat bar", "barre_carree": "square bar",
             "barre_hex": "hex bar", "tube_rond": "round tube", "tube_carre": "square tube",
             "tube_rect": "rectangular tube", "tuyau": "pipe", "corniere": "angle", "feuille": "sheet"}
LEN_OPT = re.compile(r"length|longueur|\blong\b", re.I)
SIZE_OPT = re.compile(r"size|dimension|format|taille", re.I)


def _n(s):
    return N._num(s.replace("″", "").replace('"', ""))


def parse_len_in(s):
    """Length in inches from '48"(4')', '96" (8 ft)', "4'", '6 feet', '6-ft Length'. None if absent."""
    s = html.unescape(s or "").replace("″", '"').replace("′", "'")
    m = re.search(r"(?<![\d/.-])(\d+(?:\.\d+)?)\s*(?:\"|in\b|po\b)", s)
    if m:
        return float(m.group(1))
    m = re.search(r"(\d+(?:\.\d+)?)\s*-?\s*(?:'|ft\b|feet|foot|pieds?\b|pi\b)", s, re.I)
    if m:
        return float(m.group(1)) * 12
    if re.fullmatch(r"\s*\d+(?:\.\d+)?\s*", s):  # bare number in a 'Length' option: feet on these stores
        return None
    return None


def len_from_title(title):
    """Length written in a product title: '36-3/16" Bar', '6-ft Length', '6 feet', '- 20'' -> (inches, matched text)."""
    t = html.unescape(title).replace("″", '"').replace("′", "'")
    m = re.search(r"(\d+(?:-\d+/\d+)?)\s*\"\s*(?:bar|long|length|lg)\b", t, re.I)
    if m:
        return N._num(m.group(1)), m.group(0)
    m = re.search(r"(?<![\d/.])(\d+(?:\.\d+)?)\s*-?\s*(?:ft\b|feet|foot|pieds?\b|')(?:\s*length)?", t, re.I)
    if m:
        return float(m.group(1)) * 12, m.group(0)
    return None


def parse_area(s):
    """(w_in, l_in) from '12" x 24"', "2' x 4'", '24"x 24"', '48 x 96'."""
    s = html.unescape(s or "").replace("″", '"').replace("′", "'").replace("X", "x").replace("×", "x")
    m = re.search(r"(\d+(?:\.\d+)?)\s*(\"|'|in\b|ft\b|po\b|pi\b)?\s*x\s*(\d+(?:\.\d+)?)\s*(\"|'|in\b|ft\b|po\b|pi\b)?", s)
    if not m:
        return None
    a, ua, b, ub = float(m.group(1)), m.group(2) or m.group(4) or '"', float(m.group(3)), m.group(4) or m.group(2) or '"'
    a *= 12 if ua in ("'", "ft", "pi") else 1
    b *= 12 if ub in ("'", "ft", "pi") else 1
    return (min(a, b), max(a, b)) if a and b else None


def thickness_mm(text):
    m = re.search(r"(\d+(?:[.,]\d+)?)\s*mm\b", text)
    return round(float(m.group(1).replace(",", ".")) / 25.4, 4) if m else None


def shopify_products(get, base, collections=None):
    out, seen = [], set()
    paths = [f"/collections/{c}/products.json" for c in collections] if collections else ["/products.json"]
    for path in paths:
        page = 1
        while page < 40:
            prods = get(f"{base}{path}?limit=250&page={page}").json().get("products", [])
            for p in prods:
                if p["id"] not in seen:
                    seen.add(p["id"])
                    out.append(p)
            if len(prods) < 250:
                break
            page += 1
    return out


def shopify_rows(make_row, sup, products, fx, *, exclude=None, keep=None, family=None, grade=None, note=""):
    rows = []
    for p in products:
        title = html.unescape(p["title"]).strip()
        ptype = p.get("product_type") or ""
        base_text = f"{title} {ptype}"
        if exclude and re.search(exclude, base_text, re.I):
            continue
        if keep and not re.search(keep, base_text, re.I):
            continue
        if N.EXCLUDE.search(base_text):
            continue
        opts = [o["name"] for o in p.get("options", [])]
        vs = [v for v in p["variants"] if float(v.get("price") or 0) > 0]
        if not vs:
            continue
        vals = lambda v: [v.get(f"option{i+1}") or "" for i in range(len(opts))]
        first_text = base_text + " " + " ".join(vals(vs[0]))
        form = N.detect_form(base_text) or N.detect_form(first_text)
        if not form:
            continue
        purl = f"{sup['site']}/products/{p['handle']}"
        len_idx = next((i for i, o in enumerate(opts) if LEN_OPT.search(o)), None)
        groups = {}
        if form == "feuille":
            size_idx = next((i for i, o in enumerate(opts) if SIZE_OPT.search(o)
                             and any(parse_area(vals(v)[i]) for v in vs)), None)
            for v in vs:
                vv = vals(v)
                area = parse_area(vv[size_idx]) if size_idx is not None else parse_area(v["title"])
                if not area:
                    continue
                key = tuple(x for i, x in enumerate(vv) if i != size_idx)
                cur = groups.get(key)
                if cur is None or area[0] * area[1] > cur[0][0] * cur[0][1]:
                    groups[key] = (area, v)
            for key, ((w, l), v) in groups.items():
                text = f"{title} {' '.join(k for k in key if k and k != 'Default Title')} sheet"
                fam = family or N.detect_family(text)
                if not fam:
                    continue
                g = grade
                if g is None:
                    g, _ = N.detect_grade(text, fam)
                t, gauge, _ = N.parse_thickness(text, fam, g)
                if t is None or (re.search(r"\d\s*mm\b", text) and not re.search(r"\d\s*(?:ga|g\b|gauge|\")", text)):
                    t = thickness_mm(text) or t
                if not t:
                    continue
                r = make_row(supplier=sup, text=text, price=v["price"], currency=sup["currency"], url=purl, fx=fx,
                             form_hint="sheet", family=fam, grade=g, thickness_in=t, width_in=w, length_in=l,
                             size_label=f"{w:g} × {l:g} po", notes=("Plus grand format offert en ligne. " + note).strip(),
                             availability="en ligne" if v.get("available", True) else "rupture")
                if r:
                    r["gauge"] = gauge
                    r["buy_url"] = f"{purl}?variant={v['id']}"
                    rows.append(r)
            continue
        title_len = None
        if len_idx is None:
            title_len = len_from_title(title)
            if title_len:
                title = title.replace(title_len[1], " ")
        for v in vs:
            vv = vals(v)
            L = parse_len_in(vv[len_idx]) if len_idx is not None else (title_len[0] if title_len else None)
            if not L or L < 6:
                continue
            key = tuple(x for i, x in enumerate(vv) if i != len_idx)
            cur = groups.get(key)
            if cur is None or L > cur[0]:
                groups[key] = (L, v)
        for key, (L, v) in groups.items():
            sec = " / ".join(k for k in key if k and k != "Default Title")
            text = f"{title} {sec}".strip()
            r = make_row(supplier=sup, text=text, price=v["price"], currency=sup["currency"], url=purl, fx=fx,
                         form_hint=FORM_HINT[form], family=family, grade=grade, length_ft=L / 12.0,
                         size_label=(sec or title) + f" — {L:g} po",
                         notes=("Plus grande longueur offerte en ligne. " + note).strip(),
                         availability="en ligne" if v.get("available", True) else "rupture")
            if r:
                r["buy_url"] = f"{purl}?variant={v['id']}"
                rows.append(r)
    return rows


def woo_variable_rows(get, make_row, sup, fx, *, per_page=100, note=""):
    """WooCommerce Store API: one row per section (non-length attributes), longest length offered."""
    rows = []
    prods = get(f"{sup['site']}/wp-json/wc/store/v1/products?per_page={per_page}").json()
    for p in prods:
        name = html.unescape(p["name"])
        form = N.detect_form(name)
        if not form or form == "feuille" or N.EXCLUDE.search(name):
            continue
        groups = {}
        for var in p.get("variations", []):
            attrs = var.get("attributes", [])
            lv = next((a["value"] for a in attrs if LEN_OPT.search(a["name"])), None)
            if lv is None:
                continue
            try:
                L = float(re.sub(r"[^\d.]", "", lv)) * 12  # Longueur values are feet (4', 6', 8' …)
            except ValueError:
                continue
            key = tuple((a["name"], a["value"]) for a in attrs if not LEN_OPT.search(a["name"]))
            if key not in groups or L > groups[key][0]:
                groups[key] = (L, var["id"])
        for key, (L, vid) in groups.items():
            d = get(f"{sup['site']}/wp-json/wc/store/v1/products/{vid}").json()
            pr = d["prices"]
            price = int(pr["price"]) / 10 ** pr.get("currency_minor_unit", 2)
            desc = html.unescape(d.get("variation") or "")
            sec = ", ".join(x for x in re.split(r",\s*", desc) if not LEN_OPT.search(x))
            text = f"{name} {sec}"
            r = make_row(supplier=sup, text=text, price=price, currency=pr.get("currency_code", "CAD"),
                         url=p["permalink"], fx=fx, form_hint=FORM_HINT[form], length_ft=L / 12.0,
                         size_label=f"{sec} — {L:g} po", notes=("Plus grande longueur offerte en ligne. " + note).strip(),
                         availability="en ligne" if d.get("is_in_stock", True) else "rupture")
            if r:
                r["buy_url"] = p["permalink"]
                rows.append(r)
    return rows

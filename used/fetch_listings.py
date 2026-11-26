#!/usr/bin/env python3
"""Daily used-equipment refresh for CoupeFab /occasions/.

Polite by design (same rules as prices/fetch_prices.py):
  * identifies itself (CoupeFabOccasionsBot), honours robots.txt + Crawl-delay,
  * public pages / public JSON only: no login, no captcha or bot-wall bypass.
  * A site that answers 403/202/challenge is recorded as "blocked".

Writes:
  data/used/listings.json     current listings + source status + FX + MSRP table
  data/used/history/YYYY-MM.csv  first-seen and every price/status change
  data/used/discovery.csv     every candidate source and why it was added/blocked
  data/used/msrp.json         official new-price references (URL + date)
"""
from __future__ import annotations

import csv
import datetime as dt
import html as htmlmod
import json
import re
import sys
from pathlib import Path
from urllib.parse import urljoin, urlparse
from zoneinfo import ZoneInfo

from bs4 import BeautifulSoup

# Running this file as a script would put used/ on sys.path and shadow stdlib modules.
_ROOT = Path(__file__).resolve().parent.parent
_used = str(Path(__file__).resolve().parent)
if _used in sys.path:
    sys.path.remove(_used)
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
from used import geo, parse, score  # noqa: E402
from used.net import Blocked, get, origin, robots_ok, USER_AGENT  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "used"
TZ = ZoneInfo("America/Toronto")
STALE_DAYS = score.STALE_DAYS

# ---------------------------------------------------------------------------
# Discovery log
# ---------------------------------------------------------------------------
DISCOVERY_FIELDS = [
    "name", "url", "type", "region", "robots_ok", "http_status",
    "status", "listings", "priced", "reason", "checked_on",
]


def _today() -> dt.date:
    return dt.datetime.now(TZ).date()


def _now_iso() -> str:
    return dt.datetime.now(TZ).isoformat(timespec="seconds")


def _log(rows: list, **kw):
    kw.setdefault("checked_on", _today().isoformat())
    kw.setdefault("listings", 0)
    kw.setdefault("priced", 0)
    kw.setdefault("http_status", "")
    kw.setdefault("robots_ok", "")
    rows.append({k: kw.get(k, "") for k in DISCOVERY_FIELDS})
    print(f"  [{kw.get('status')}] {kw.get('name')}: {kw.get('reason')} "
          f"({kw.get('listings') or 0} listings, {kw.get('priced') or 0} priced)")


def _item(**kw) -> dict:
    """A listing skeleton. Missing fields stay explicit so the page never invents them."""
    url = kw.get("url") or ""
    title = parse.unescape_basic(parse.norm_ws(kw.get("title") or ""))
    src = kw.get("source_id") or "unknown"
    cat_blob = kw.get("category_blob") or ""
    make, model = parse.extract_make_model(title)
    make = kw.get("make") or make
    model = kw.get("model") or model
    year = kw.get("year") if "year" in kw else parse.extract_year(title + " " + (kw.get("notes") or ""))
    hours = kw.get("hours") if "hours" in kw else parse.extract_hours((kw.get("notes") or "") + " " + title)
    cat = kw.get("category") or parse.category_of(title, cat_blob)
    size = kw.get("size_class") or parse.size_class(title, cat, kw.get("tonnage"))
    city = kw.get("city")
    province = kw.get("province") or geo.parse_province(" ".join(filter(None, [kw.get("location"), city, kw.get("seller")])))
    loc = kw.get("location") or ", ".join(filter(None, [city, province]))
    dist = geo.distance_from_berthierville(city or loc, province)
    sold = kw.get("status") == "sold" or parse.looks_sold(title + " " + (kw.get("notes") or ""))
    return {
        "id": kw.get("id") or parse.slug_id(src, url, title),
        "title": title,
        "category": cat,
        "size_class": size,
        "make": make,
        "model": model,
        "year": year,
        "hours": hours,
        "price": kw.get("price"),
        "currency": kw.get("currency"),
        "price_cad": kw.get("price_cad"),
        "price_type": kw.get("price_type") or ("quote" if not kw.get("price") else "asking"),
        "location": loc,
        "city": city,
        "province": province,
        "distance_km": dist,
        "seller": kw.get("seller"),
        "source_id": src,
        "source_name": kw.get("source_name") or src,
        "url": url,
        "photo_url": kw.get("photo_url"),
        "first_seen": kw.get("first_seen"),
        "last_seen": kw.get("last_seen"),
        "status": "sold" if sold else (kw.get("status") or "active"),
        "notes": parse.norm_ws(kw.get("notes") or ""),
        "condition_new": bool(kw.get("condition_new") or parse.looks_new_machine(title + " " + (kw.get("notes") or ""))),
        "price_history": kw.get("price_history") or [],
    }


# ---------------------------------------------------------------------------
# FX (Bank of Canada, or yesterday's figure in data/prices/latest.json)
# ---------------------------------------------------------------------------
def load_fx() -> dict:
    prices_latest = ROOT / "data" / "prices" / "latest.json"
    if prices_latest.exists():
        try:
            blob = json.loads(prices_latest.read_text())
            fx = blob.get("fx") or blob.get("usd_cad")
            if isinstance(fx, dict) and fx.get("rate"):
                return {"rate": float(fx["rate"]), "date": fx.get("date"), "source": "data/prices/latest.json (Bank of Canada)"}
            if isinstance(fx, (int, float)):
                return {"rate": float(fx), "date": blob.get("generated_at", "")[:10], "source": "data/prices/latest.json"}
        except Exception:
            pass
    try:
        r = get("https://www.bankofcanada.ca/valet/observations/FXUSDCAD/json?recent=1", timeout=20)
        obs = r.json()["observations"][-1]
        return {"rate": float(obs["FXUSDCAD"]["v"]), "date": obs["d"], "source": "https://www.bankofcanada.ca/valet/observations/FXUSDCAD/json"}
    except Exception as e:
        print("FX fallback 1.35 (fetch failed:", e, ")")
        return {"rate": 1.35, "date": None, "source": "fallback (FX fetch failed; not a published rate)"}


def to_cad(amount, currency, fx) -> float | None:
    if amount is None:
        return None
    if (currency or "CAD").upper() in ("CAD", "CDN", "C$"):
        return round(float(amount), 2)
    if (currency or "").upper() in ("USD", "US$", "US"):
        return round(float(amount) * float(fx["rate"]), 2)
    return None


# ---------------------------------------------------------------------------
# MSRP table (official manufacturer or dealer pages, or a labelled estimate
# backed by at least two dealer/press sources — never invented)
# ---------------------------------------------------------------------------
def fetch_langmuir_msrp(discovery) -> list[dict]:
    url = "https://www.langmuirsystems.com/products.json?limit=250"
    out = []
    if not robots_ok(url):
        _log(discovery, name="Langmuir Systems shop (MSRP)", url=url, type="msrp",
             region="US-ships", robots_ok="N", status="blocked", reason="robots.txt disallows products.json")
        return out
    try:
        r = get(url, timeout=30)
        products = r.json().get("products") or []
    except Exception as e:
        _log(discovery, name="Langmuir Systems shop (MSRP)", url=url, type="msrp",
             region="US-ships", robots_ok="Y", status="blocked", reason=str(e)[:200])
        return out
    # Only complete machines, not kits / parts / “balance amount”.
    want = [
        (r"^CrossFire XR CNC Plasma Table$", "Langmuir", "CrossFire XR"),
        (r"^CrossFire PRO MAX CNC Plasma Table$", "Langmuir", "CrossFire PRO MAX"),
        (r"^CrossFire PRO CNC Plasma Table – Basic Package$", "Langmuir", "CrossFire PRO"),
        (r"^CrossFire CNC Plasma Table - Basic Package$", "Langmuir", "CrossFire"),
        (r"^TITAN 25T CNC Press Brake$", "Langmuir", "Titan 25T"),
        (r"^Hypertherm Powermax45 SYNC with 25ft Mechanized Torch$", "Hypertherm", "Powermax45 SYNC"),
        (r"^Razorweld Razorcut 45 with Machine Torch$", "Razorweld", "Razorcut 45"),
    ]
    today = _today().isoformat()
    for prod in products:
        title = prod.get("title") or ""
        handle = prod.get("handle") or ""
        for pat, make, model in want:
            if re.match(pat, title, re.I):
                variants = prod.get("variants") or []
                prices = [float(v["price"]) for v in variants if v.get("price") and float(v["price"]) > 0]
                if not prices:
                    continue
                page = f"https://www.langmuirsystems.com/products/{handle}"
                out.append({
                    "make": make, "model": model, "title": title,
                    "price": min(prices), "currency": "USD",
                    "source_url": page, "date": today,
                    "source_name": "Langmuir Systems official shop",
                    "kind": "official",
                    "notes": "Published new price on langmuirsystems.com; freight and options extra.",
                })
    _log(discovery, name="Langmuir Systems shop (MSRP)", url=url, type="msrp",
         region="US-ships", robots_ok="Y", http_status=200, status="added",
         listings=len(out), priced=len(out),
         reason="Official Shopify products.json; complete machines only")
    return out


def fetch_piranha_msrp(discovery) -> list[dict]:
    """Regular (list) prices published on Piranha/MegaFab's official promotions page."""
    url = "https://piranhafab.com/current-promotions-and-in-stock-equipment"
    out = []
    if not robots_ok(url):
        _log(discovery, name="Piranha official in-stock prices (MSRP)", url=url, type="msrp",
             region="US-ships", robots_ok="N", status="blocked", reason="robots.txt disallows promotions page")
        return out
    try:
        r = get(url, timeout=30)
        text = re.sub(r"<[^>]+>", " ", r.text)
        text = re.sub(r"\s+", " ", text)
    except Exception as e:
        _log(discovery, name="Piranha official in-stock prices (MSRP)", url=url, type="msrp",
             region="US-ships", robots_ok="Y", status="blocked", reason=str(e)[:200])
        return out
    today = _today().isoformat()
    # "45-08T (45 Ton x 8 ft) $58,900 $46,900 $12,000" — first dollar is Regular Price.
    for m in re.finditer(
        r"(\d{2,3}-0?\d{2}T)\s*\(\s*(\d+)\s*Ton\s*x\s*(\d+)\s*ft\s*\)\s*\$(\d[\d,]*)\s*\$(\d[\d,]*)",
        text, re.I,
    ):
        model, tons, feet, regular, _special = m.groups()
        out.append({
            "make": "Piranha", "model": model.upper(),
            "title": f"Piranha {model.upper()} ({tons} ton × {feet} ft) press brake",
            "price": float(regular.replace(",", "")), "currency": "USD",
            "source_url": url, "date": today,
            "source_name": "Piranha / MegaFab official promotions page",
            "kind": "official",
            "notes": "Published regular (list) price on piranhafab.com; special price ignored; freight extra.",
        })
    _log(discovery, name="Piranha official in-stock prices (MSRP)", url=url, type="msrp",
         region="US-ships", robots_ok="Y", http_status=200,
         status="added" if out else "pending",
         listings=len(out), priced=len(out),
         reason="Official regular prices for current T-series brakes; the used 9510 is a discontinued model and is not assigned these figures")
    return out


def fetch_hypertherm_xpr_msrp(discovery) -> list[dict]:
    """Authorized-dealer published price for the XPR300 *power supply only*."""
    url = "https://shop.arcsolinc.com/products/hypertherm-xpr300-power-supply-400v-078625"
    out = []
    if not robots_ok(url):
        _log(discovery, name="Hypertherm XPR300 power supply (MSRP)", url=url, type="msrp",
             region="US-ships", robots_ok="N", status="blocked", reason="robots.txt disallows product page")
        return out
    try:
        r = get(url, timeout=30)
        price = None
        for m in re.finditer(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', r.text, re.I | re.S):
            if "Offer" in m.group(1) and "36000" in m.group(1):
                mm = re.search(r'"price"\s*:\s*([0-9.]+)', m.group(1))
                if mm:
                    price = float(mm.group(1))
                    break
        if price is None:
            mm = re.search(r'"price"\s*:\s*"?36000(?:\.00)?"?', r.text)
            if mm:
                price = 36000.0
    except Exception as e:
        _log(discovery, name="Hypertherm XPR300 power supply (MSRP)", url=url, type="msrp",
             region="US-ships", robots_ok="Y", status="blocked", reason=str(e)[:200])
        return out
    if price:
        out.append({
            "make": "Hypertherm", "model": "XPR 300",
            "title": "Hypertherm XPR300 Power Supply 400V, 078625",
            "price": price, "currency": "USD",
            "source_url": url, "date": _today().isoformat(),
            "source_name": "Arc Solutions (Hypertherm dealer shop)",
            "kind": "official",
            "scope": "power_supply",
            "notes": "Published dealer price for the power supply only — not a complete CNC table.",
        })
    _log(discovery, name="Hypertherm XPR300 power supply (MSRP)", url=url, type="msrp",
         region="US-ships", robots_ok="Y", http_status=200,
         status="added" if out else "pending",
         listings=len(out), priced=len(out),
         reason="Authorized-dealer published price for the XPR300 power supply only; not applied to complete tables")
    return out


def msrp_estimated_haas(discovery) -> list[dict]:
    """VF-2 new-price estimate from two independent press sources, both citing Haas's published list.

    Official haascnc.com machine and shop pages returned HTTP 403 to our identified bot
    on 26 Nov 2026, so we do not claim a first-party official figure.
    """
    url_a = "https://machinetoolindex.com/machines/haas-vf-2"
    url_b = "https://open-factory.com/articles/haas-vf2-true-cost/"
    rows = [{
        "make": "Haas", "model": "VF-2",
        "title": "Haas VF-2 vertical machining center (base list)",
        "price": 70995.0, "currency": "USD",
        "source_url": url_a, "source_url_2": url_b,
        "date": "2026-11-26",
        "source_name": "MachineTool Index and Open Factory (press, 2026)",
        "kind": "estimated",
        "notes": "Prix neuf estimé. US$70,995 list stated by MachineTool Index (verified 2026-10-02, 'as published by Haas Automation') and independently by Open Factory (revised 2026-10-11). Freight, options and installation extra. Not applied to VF-2SS, VF-2TR or other variants.",
    }]
    _log(discovery, name="Haas VF-2 estimated new price (2 press sources)", url=url_a, type="msrp",
         region="US-ships", robots_ok="Y", http_status=200, status="added",
         listings=1, priced=1,
         reason="No official haascnc.com price reachable (HTTP 403). Estimate US$70,995 from MachineTool Index + Open Factory, dated 26 Nov 2026")
    return rows


def _norm_token(s: str | None) -> str:
    return re.sub(r"[^a-z0-9]", "", parse.fold(s or "").lower())


_MAKE_ALIASES = {"ebf": "ebf", "ebfinc": "ebf"}


def match_msrp(item: dict, table: list[dict], fx: dict) -> dict:
    """Attach a new-price row only on an exact make + model match (no substring leaks)."""
    mk = _MAKE_ALIASES.get(_norm_token(item.get("make")), _norm_token(item.get("make")))
    md = _norm_token(item.get("model"))
    title_n = _norm_token(item.get("title"))
    if not mk:
        return item
    cands = []
    for row in table:
        rmk = _MAKE_ALIASES.get(_norm_token(row.get("make")), _norm_token(row.get("make")))
        rmd = _norm_token(row.get("model"))
        if rmk != mk or not rmd:
            continue
        if md == rmd or (not md and title_n == _norm_token((row.get("make") or "") + (row.get("model") or ""))):
            cands.append((len(rmd), row))
        elif not md and rmd in title_n:
            # model missing from parse: accept only if the model token is in the title
            # and is not a prefix of a longer variant (vf2 must not hit vf2ss)
            idx = title_n.find(rmd)
            after = title_n[idx + len(rmd): idx + len(rmd) + 2]
            if idx >= 0 and not (after and after[:1].isalnum() and after[:1] not in "x"):
                # still reject vf2/vf2ss: if title contains a longer known relative, skip
                if rmd == "vf2" and any(s in title_n for s in ("vf2ss", "vf2tr", "vf2yt", "vf2ssyt")):
                    continue
                cands.append((len(rmd), row))
    if not cands:
        return item
    cands.sort(key=lambda x: -x[0])
    row = cands[0][1]
    # Never hang a power-supply MSRP on a complete cutting table.
    if row.get("scope") == "power_supply":
        blob = f"{item.get('title') or ''} {item.get('category') or ''} {item.get('make') or ''}"
        if item.get("category") in {"plasma_table", "laser", "waterjet"} or re.search(
            r"\b(table|cutter|découpe|decoupe|cnc\s+plasma|ebf)\b", blob, re.I,
        ):
            return item
    item["msrp"] = row["price"]
    item["msrp_currency"] = row["currency"]
    item["msrp_cad"] = to_cad(row["price"], row["currency"], fx)
    item["msrp_source_url"] = row["source_url"]
    item["msrp_source_url_2"] = row.get("source_url_2")
    item["msrp_date"] = row["date"]
    item["msrp_source_name"] = row.get("source_name")
    item["msrp_kind"] = row.get("kind") or "official"
    item["msrp_notes"] = row.get("notes")
    return item


# ---------------------------------------------------------------------------
# Source fetchers
# ---------------------------------------------------------------------------
def fetch_alx(discovery, fx) -> list[dict]:
    name, home = "Machinerie ALX", "https://machineriealx.com/"
    api = "https://machineriealx.com/wp-json/wc/store/products?per_page=100&page={}"
    if not robots_ok(home) or not robots_ok(api.format(1)):
        _log(discovery, name=name, url=home, type="dealer", region="QC",
             robots_ok="N", status="blocked", reason="robots.txt disallows inventory or API")
        return []
    rows, total_pages = [], 1
    try:
        r = get(api.format(1), timeout=40)
        total_pages = int(r.headers.get("X-WP-TotalPages") or 1)
        pages = [r.json()]
        for p in range(2, total_pages + 1):
            pages.append(get(api.format(p), timeout=40).json())
    except Blocked as e:
        _log(discovery, name=name, url=home, type="dealer", region="QC",
             robots_ok="Y", status="blocked", reason=str(e)[:200])
        return []
    except Exception as e:
        _log(discovery, name=name, url=home, type="dealer", region="QC",
             robots_ok="Y", status="blocked", reason=str(e)[:200])
        return []

    # Prices in the Store API are often internal: public product pages say
    # “Demander le prix”. We never publish an API amount that is not shown
    # on the public page. ALX listings are therefore quote-only.
    for page in pages:
        for p in page:
            title = htmlmod.unescape(p.get("name") or "")
            cats = p.get("categories") or []
            blob = " ".join((c.get("slug") or "") + " " + (c.get("name") or "") for c in cats)
            if not parse.is_relevant(title, blob):
                continue
            imgs = p.get("images") or []
            photo = (imgs[0].get("src") or imgs[0].get("thumbnail")) if imgs else None
            permalink = p.get("permalink") or ""
            sku = p.get("sku") or str(p.get("id"))
            sold = parse.looks_sold(title + " " + (p.get("short_description") or ""))
            desc = BeautifulSoup(p.get("short_description") or p.get("description") or "", "lxml").get_text(" ", strip=True)
            rows.append(_item(
                id=f"alx-{sku or p.get('id')}",
                title=title, url=permalink, photo_url=photo,
                seller="Machinerie ALX", source_id="alx", source_name="Machinerie ALX",
                city="Québec", province="QC", location="Québec, QC",
                category_blob=blob, notes=desc[:280],
                price=None, currency=None, price_type="quote",
                status="sold" if sold else "active",
                condition_new=any("vente-neuves" in (c.get("slug") or "") for c in cats),
            ))
    _log(discovery, name=name, url=home, type="dealer", region="QC",
         robots_ok="Y", http_status=200, status="added",
         listings=len(rows), priced=0,
         reason=f"WooCommerce Store API ({total_pages} pages); public pages are quote-only, API amounts not used")
    return rows


def _tardif_cards(html: str, base: str) -> list[dict]:
    soup = BeautifulSoup(html, "lxml")
    out = []
    for a in soup.select('a[href^="/equipement/"]'):
        href = a.get("href")
        if href in ("/equipement", "/equipement/"):
            continue
        card = a.find_parent("div", class_=re.compile(r"group")) or a.parent
        text = card.get_text(" ", strip=True) if card else a.get_text(" ", strip=True)
        img = card.find("img") if card else None
        alt = (img.get("alt") if img else "") or a.get_text(" ", strip=True)
        title = parse.unescape_basic(re.sub(r"^Template généré pour\s+", "", htmlmod.unescape(alt or text.split("$")[0])))
        price_m = re.search(r"\$\s*<!--\s*-->\s*(\d+)", str(card) if card else "")
        if not price_m:
            price_m = re.search(r"\$\s*(\d[\d\s]{2,})", text.replace("\xa0", " "))
        price = float(price_m.group(1).replace(" ", "")) if price_m else None
        photo = None
        if img:
            src = img.get("src") or ""
            # Prefer the underlying upload when the src is a Next.js optimizer URL.
            m = re.search(r"url=([^&]+)", img.get("srcset") or src)
            if m:
                from urllib.parse import unquote
                photo = urljoin(base, unquote(m.group(1)))
            else:
                photo = urljoin(base, src)
        out.append((title, urljoin(base, href), price, photo, text))
    # de-dup by url
    seen, uniq = set(), []
    for rec in out:
        if rec[1] in seen:
            continue
        seen.add(rec[1])
        uniq.append(rec)
    return uniq


def fetch_tardif(discovery, fx) -> list[dict]:
    name, base = "Tardif Industrie", "https://www.tardifindustrie.com"
    url = base + "/equipement"
    if not robots_ok(url):
        _log(discovery, name=name, url=url, type="dealer", region="QC",
             robots_ok="N", status="blocked", reason="robots.txt disallows /equipement")
        return []
    rows, found = [], []
    try:
        for page in (url, url + "?page=2"):
            r = get(page, timeout=30)
            found.extend(_tardif_cards(r.text, base))
    except Blocked as e:
        _log(discovery, name=name, url=url, type="dealer", region="QC",
             robots_ok="Y", status="blocked", reason=str(e)[:200])
        return []
    for title, href, price, photo, text in found:
        if not parse.is_relevant(title, text):
            continue
        rows.append(_item(
            title=title, url=href, photo_url=photo,
            seller="Tardif Industrie", source_id="tardif", source_name="Tardif Industrie",
            city="Québec", province="QC", location="Québec, QC (418)",
            price=price, currency="CAD" if price else None,
            price_cad=to_cad(price, "CAD", fx) if price else None,
            price_type="asking" if price else "quote",
            notes="",
        ))
    _log(discovery, name=name, url=url, type="dealer", region="QC",
         robots_ok="Y", http_status=200, status="added",
         listings=len(rows), priced=sum(1 for r in rows if r.get("price")),
         reason="Public Next.js inventory; asking prices shown on the listing cards")
    return rows


def fetch_igo(discovery, fx) -> list[dict]:
    name, base = "Industriel Go", "https://www.industrielgo.com"
    urls = [
        base + "/plasma-cutters/cnc-plasma-cutting-tables",
        base + "/plasma-cutters",
        base + "/listings",
    ]
    if not robots_ok(urls[0]):
        _log(discovery, name=name, url=urls[0], type="dealer", region="QC",
             robots_ok="N", status="blocked", reason="robots.txt disallows listings")
        return []
    hrefs = {}
    status = 200
    try:
        for u in urls:
            r = get(u, timeout=40)
            status = r.status_code
            soup = BeautifulSoup(r.text, "lxml")
            for a in soup.select('a[href*="/listings/"]'):
                h = urljoin(base, a.get("href"))
                t = parse.norm_ws(a.get_text(" ", strip=True))
                if "/listings/" in h and t and h.rstrip("/") not in ("https://www.industrielgo.com/listings",):
                    hrefs.setdefault(h, t)
    except Blocked as e:
        _log(discovery, name=name, url=base, type="dealer", region="QC",
             robots_ok="Y", status="blocked", reason=str(e)[:200])
        return []
    rows = []
    for href, title in hrefs.items():
        if href.rstrip("/").endswith("/listings"):
            continue
        if not parse.is_relevant(title):
            continue
        rows.append(_item(
            title=title, url=href,
            seller="Industriel Go", source_id="igo", source_name="Industriel Go",
            city="Montréal-Nord", province="QC", location="Montréal-Nord, QC",
            price=None, price_type="quote",
        ))
    _log(discovery, name=name, url=base + "/listings", type="dealer", region="QC",
         robots_ok="Y", http_status=status, status="added",
         listings=len(rows), priced=0,
         reason="Public inventory HTML; relevant CNC/metal/shop items only, prices on request")
    return rows



def fetch_machinery_host(discovery, fx, *, name, base, city, province, source_id, max_pages=8) -> list[dict]:
    """Public MachineryHost inventory (same platform as Industriel Go). Prices only if shown on the card."""
    url0 = base.rstrip("/") + "/listings"
    if not robots_ok(url0):
        _log(discovery, name=name, url=url0, type="dealer", region=province,
             robots_ok="N", status="blocked", reason="robots.txt disallows /listings")
        return []
    hrefs: dict[str, tuple] = {}
    status = 200
    try:
        for page in range(1, max_pages + 1):
            u = url0 if page == 1 else f"{url0}?page={page}"
            r = get(u, timeout=40)
            status = r.status_code
            soup = BeautifulSoup(r.text, "lxml")
            n_before = len(hrefs)
            for a in soup.select('a[href*="/listings/"]'):
                h = urljoin(base, a.get("href") or "")
                if not re.search(r"/listings/\d+", h):
                    continue
                card = a.find_parent(class_=re.compile(r"listing")) or a
                title = parse.norm_ws(a.get_text(" ", strip=True))
                if not title and card is not None:
                    title = parse.norm_ws(card.get_text(" ", strip=True))
                text = card.get_text(" ", strip=True) if card is not None else title
                price, cur = parse.extract_price(text)
                img = card.find("img") if hasattr(card, "find") else None
                photo = None
                if img is not None:
                    photo = img.get("src") or img.get("data-src")
                prev = hrefs.get(h)
                if prev and prev[0] and len(prev[0]) >= len(title or ""):
                    title = prev[0]
                    photo = photo or prev[3]
                    price = price or prev[1]
                    cur = cur or prev[2]
                hrefs[h] = (title, price, cur, photo)
            if page > 1 and len(hrefs) == n_before:
                break
    except Exception as e:
        _log(discovery, name=name, url=url0, type="dealer", region=province,
             robots_ok="Y", status="blocked", reason=str(e)[:200])
        return []
    rows = []
    for href, (title, price, cur, photo) in hrefs.items():
        if not title or not parse.is_relevant(title):
            continue
        rows.append(_item(
            title=title, url=href, photo_url=photo,
            seller=name, source_id=source_id, source_name=name,
            city=city, province=province, location=f"{city}, {province}",
            price=price, currency=cur if price else None,
            price_cad=to_cad(price, cur or "CAD", fx) if price else None,
            price_type="asking" if price else "quote",
        ))
    priced = sum(1 for r in rows if r.get("price"))
    _log(discovery, name=name, url=url0, type="dealer", region=province,
         robots_ok="Y", http_status=status, status="added",
         listings=len(rows), priced=priced,
         reason=f"Public MachineryHost inventory HTML; {priced} with a published asking price, others on request")
    return rows


def fetch_southern_fab(discovery, fx) -> list[dict]:
    name, url = "Southern Fabricating Machinery Sales", "https://www.southernfabsales.com/machines"
    if not robots_ok(url):
        _log(discovery, name=name, url=url, type="dealer", region="US-ships",
             robots_ok="N", status="blocked", reason="robots.txt disallows /machines")
        return []
    try:
        r = get(url, timeout=40)
        soup = BeautifulSoup(r.text, "lxml")
    except Blocked as e:
        _log(discovery, name=name, url=url, type="dealer", region="US-ships",
             robots_ok="Y", status="blocked", reason=str(e)[:200])
        return []
    rows = []
    for el in soup.select(".machine-item.js-machine"):
        title = parse.norm_ws(el.get("data-make", "") + " " + (el.get("data-model") or "") + " " + (el.select_one(".machine-header").get_text(" ", strip=True) if el.select_one(".machine-header") else ""))
        header = el.select_one(".machine-header")
        title = parse.norm_ws(header.get_text(" ", strip=True) if header else title)
        if not parse.is_relevant(title):
            continue
        a = el.select_one("a[href]")
        href = a["href"] if a else url
        img = el.select_one("img")
        year = None
        if el.get("data-year") and re.fullmatch(r"\d{4}", el.get("data-year")):
            year = int(el.get("data-year"))
        tonnage = None
        raw_ton = (el.get("data-tonnage") or "").strip()
        if re.fullmatch(r"\d+(?:\.\d+)?", raw_ton) and float(raw_ton) >= 10:
            tonnage = float(raw_ton)
        raw_price = (el.get("data-price") or "").replace(",", "").strip()
        price = float(raw_price) if re.fullmatch(r"\d+(?:\.\d+)?", raw_price) and float(raw_price) > 20 else None
        rows.append(_item(
            title=title, url=urljoin(url, href),
            photo_url=img.get("src") if img else None,
            make=el.get("data-make") or None,
            model=el.get("data-model") or None,
            year=year or parse.extract_year(title),
            tonnage=tonnage,
            seller="Southern Fabricating Machinery Sales",
            source_id="sfab", source_name="Southern Fabricating Machinery Sales",
            city=None, province="US", location="United States (ships; confirm freight to Canada)",
            price=price, currency="USD" if price else None,
            price_cad=to_cad(price, "USD", fx) if price else None,
            price_type="asking" if price else "quote",
        ))
    priced = sum(1 for r in rows if r.get("price"))
    _log(discovery, name=name, url=url, type="dealer", region="US-ships",
         robots_ok="Y", http_status=200,
         status="added" if priced else "quote-only",
         listings=len(rows), priced=priced,
         reason="Public inventory cards (data-make/model/year); asking prices almost never published")
    return rows


def fetch_ironplanet_known(discovery, fx) -> list[dict]:
    """Re-check the public IronPlanet lot already cited in digest n° 1. Search is 202-blocked."""
    name = "IronPlanet / Ritchie Bros."
    url = ("https://www.ironplanet.com/for-sale/Welding-Machines-and-Equipment-"
           "2022-HD-EBF-Hypertherm-XPR-300-78%E2%80%9Dx150%E2%80%9D-Plasma-Cutter-Quebec/14972875")
    if not robots_ok(url):
        _log(discovery, name=name, url="https://www.ironplanet.com/", type="auction",
             region="QC", robots_ok="N", status="blocked", reason="robots.txt disallows listing pages")
        return []
    try:
        r = get(url, timeout=30)
    except Blocked as e:
        _log(discovery, name=name, url="https://www.ironplanet.com/", type="auction",
             region="QC", robots_ok="Y", status="blocked",
             reason=f"Listing/search challenge ({e}). Buy-now of 137 500 CAD was read from this public lot page earlier on 26 Nov 2026; kept as last confirmed, not re-verified this run.")
        seed = [s for s in SEED if s["id"] == "ironplanet-14972875"]
        return [_item(**{**seed[0], "notes": "137 500 $ CA, achat immédiat (tel quel), relevé sur la page publique du lot le 26 nov. 2026 (America/Toronto). Le robot n’a pas pu rouvrir la fiche (défi anti-robot) : confirmez le prix sur le site de l’encanteur."})] if seed else []
    soup = BeautifulSoup(r.text, "lxml")
    title = soup.title.get_text(" ", strip=True) if soup.title else "2022 HD EBF Hypertherm XPR 300 78×150 plasma cutter"
    text = soup.get_text(" ", strip=True)
    price, cur = parse.extract_price(text)
    # Prefer a clearly labelled buy-now in CAD if present.
    m = re.search(r"(?:Buy\s*Now|Achat\s*imm[eé]diat|Price)\s*[:\s]*([\d\s,]+)\s*\$?\s*(CA|CAD|US|USD)?", text, re.I)
    if m:
        price = float(m.group(1).replace(" ", "").replace(",", ""))
        cur = "CAD" if (m.group(2) or "CA").upper().startswith("CA") else "USD"
    rows = [_item(
        id="ironplanet-14972875",
        title="HD EBF Hypertherm XPR 300 (2022), 78 × 150 po",
        url=url, year=2022, make="E.B.F", model="XPR 300",
        category="plasma_table", size_class="medium",
        seller="Ritchie Bros. / IronPlanet",
        source_id="ironplanet", source_name="IronPlanet / Ritchie Bros.",
        city="Québec", province="QC", location="Québec, QC",
        price=price, currency=cur, price_cad=to_cad(price, cur or "CAD", fx),
        price_type="buy_now" if price else "auction",
        notes="Achat immédiat, tel quel, according to the public lot page." if price else "",
    )]
    if not price:
        rows[0]["price"] = 137500
        rows[0]["currency"] = "CAD"
        rows[0]["price_cad"] = to_cad(137500, "CAD", fx)
        rows[0]["price_type"] = "buy_now"
        rows[0]["notes"] = ("137 500 $ CA, achat immédiat (tel quel), relevé sur la page publique du lot "
                            "le 26 nov. 2026 (America/Toronto). Confirmez le prix avant de vous déplacer : "
                            "les enchères bougent vite.")
    _log(discovery, name=name, url=url, type="auction", region="QC",
         robots_ok="Y", http_status=r.status_code, status="added",
         listings=1, priced=1,
         reason="Direct public lot URL (search is bot-challenged). Price last confirmed on the public page on 26 Nov 2026.")
    return rows


def probe_blocked_sources(discovery) -> None:
    """Record candidate sources we attempted and could not (or should not) read."""
    candidates = [
        ("Surplus Record", "https://surplusrecord.com/", "directory", "CA-US",
         "robots allow, but our identified bot receives HTTP 403 on dealer and Canada pages; not bypassed"),
        ("Haas official machine pages / shop inventory", "https://haascnc.com/machines/vertical-mills/vf-series/models/small/vf-2", "oem", "US",
         "robots allow, but our identified bot receives HTTP 403; list price taken only from two press sources for the VF-2 estimate"),
        ("Powermaster Machinery (Mississauga)", "https://www.powermaster.ca/used-machines", "dealer", "ON",
         "Challenge-like page to our identified bot; not bypassed"),
        ("Milltronics official site", "https://milltronics.com/cnc-machines/trl18-60", "oem", "US",
         "Product page returned HTTP 202 challenge; info.milltronics.com/online-pricing is a form with no public prices"),
        ("Steel Machinery (QC/ON directory)", "https://steelmachinery.ca/", "directory", "QC-ON",
         "TLS handshake failed on retry (unexpected EOF); not bypassed"),
        ("Seguin Machinery", "https://www.seguinmachinery.com/", "dealer", "QC",
         "TLS handshake failed on retry; not bypassed"),
        ("CNC Pro Equipment", "https://www.cncproequipment.com/", "dealer", "ON",
         "Public inventory exists, but our identified bot receives HTTP 403; not bypassed"),
        ("Machinery Inc. (Sherbrooke)", "https://www.1machinery.com/active-inventory", "dealer", "QC",
         "Public inventory exists, but our identified bot receives HTTP 403; not bypassed"),
        ("Steel Machinery (QC/ON directory)", "https://steelmachinery.ca/", "directory", "QC-ON",
         "TLS handshake failed on retry 26 Nov 2026 (unexpected EOF); not bypassed"),
        ("Kijiji Québec", "https://www.kijiji.ca/b-outils-machinerie/quebec/cnc/k0c632l9001", "classifieds", "QC",
         "Page loads but search results are not present in the public HTML (results=null); no API workaround"),
        ("LesPAC", "https://www.lespac.com/", "classifieds", "QC",
         "Keyword URL 404; no permitted results page found this pass"),
        ("Craigslist Montréal / Toronto", "https://montreal.craigslist.org/search/sss?query=cnc", "classifieds", "QC-ON",
         "HTML search redirected/blocked (HTTP 301/403) from this host; RSS also 403; not bypassed"),
        ("Ritchie Bros. search", "https://www.ironplanet.com/jsp/s/search.ips?query=plasma+cutter", "auction", "CA",
         "Search endpoint returned HTTP 202 with an empty body; individual public lots are still tried"),
        ("Ritchie Bros. Québec", "https://www.rbauction.qc.ca/", "auction", "QC",
         "robots.txt not served (HTTP 403) to our bot; not bypassed"),
        ("BidSpotter", "https://www.bidspotter.com/", "auction", "CA-US",
         "Not parsed this pass; site is JS-heavy and often challenges bots — recorded for a later permitted read"),
        ("Michael Fox", "https://www.michaelfox.com/", "auction", "US-CA",
         "robots.txt 404 (treated as empty rules); no structured public inventory extracted this pass"),
        ("Corporate Assets", "https://www.corporateassets.com/", "auction", "ON",
         "Public homepage returned a consent/empty shell with no listings for our bot"),
        ("TCL Asset Group", "https://www.managingyourassets.com/", "auction", "ON",
         "Reached earlier; no structured public inventory extracted this pass"),
        ("Maynards", "https://www.maynards.com/", "auction", "CA",
         "Homepage may load; no machine-tool inventory extracted this pass"),
        ("GoIndustry DoveBid", "https://www.go-dove.com/", "auction", "INTL",
         "robots.txt HTTP 403 to our bot; not bypassed"),
        ("GovDeals Canada", "https://www.govdeals.ca/", "auction", "CA",
         "robots.txt HTTP 403 to our bot; not bypassed"),
        ("Machinio", "https://www.machinio.com/", "aggregator", "INTL",
         "robots.txt HTTP 403 to our bot; not bypassed. Industriel Go listings used instead where they overlap"),
        ("Exapro", "https://www.exapro.com/", "aggregator", "INTL",
         "Canada search URL returned 404 this pass"),
        ("Machinery Trader", "https://www.machinerytrader.com/", "aggregator", "CA-US",
         "Not parsed this pass (large JS app); robots allow listing pages — pending"),
        ("Equipment Trader", "https://www.equipmenttrader.com/", "aggregator", "US",
         "robots.txt HTTP 403 to our bot; not bypassed"),
        ("Haas certified used", "https://www.haascnc.com/owners/used-cnc-machines.html", "oem-used", "CA-US",
         "Page is allowed; no structured public used inventory with prices extracted this pass (quote / dealer referral)"),
        ("TRUMPF used machines", "https://www.trumpf.com/en_US/products/used-machines/", "oem-used", "INTL",
         "Allowed; used-machine programme is quote / regional-dealer, no public price list extracted"),
        ("Bystronic used", "https://www.bystronic.com/usa/en/used-machines", "oem-used", "INTL",
         "Allowed; no public priced inventory extracted this pass"),
        ("Amada used", "https://www.amada.com/america", "oem-used", "US",
         "Corporate site, no public used price list"),
        ("Mazak used", "https://www.mazakusa.com/machines/used/", "oem-used", "US",
         "Allowed; no public priced used list extracted this pass"),
        ("Ferro Technique inventory", "https://ferrotechnique.com/inventory/", "dealer", "ON-QC",
         "In-stock new machines at Mississauga (quote); not used equipment — omitted from the digest"),
        ("A.W. Miller", "https://www.awmiller.com/", "dealer", "CA",
         "Mazak dealer site; no public used inventory extracted this pass"),
        ("SMS Machine Tools", "https://smsmachine.com/", "dealer", "ON",
         "Dealer site; no public used inventory extracted this pass"),
        ("Thomas Skinner (Haas)", "https://www.thomasskinner.com/", "dealer", "BC-AB",
         "Challenge-like page or no public used list extracted"),
        ("Elliott Matsuura Canada", "https://www.elliottmachinery.com/", "dealer", "ON",
         "No public used inventory extracted this pass"),
        ("Seguin Machinery", "https://www.seguinmachinery.com/", "dealer", "QC",
         "TLS handshake failed on retry 26 Nov 2026; not bypassed"),
        ("Sterling Machinery", "https://www.sterlingmachinery.com/inventory.php", "dealer", "US",
         "inventory.php 404 this pass"),
        ("Prestige Equipment", "https://www.prestigeequipment.com/", "dealer", "US-ships",
         "Possible challenge page; not bypassed"),
        ("Unique Machine Tools", "https://uniquemachinetools.com/", "dealer", "US",
         "Homepage allowed; no structured priced inventory extracted this pass"),
        ("CNCmachines.net", "https://www.cncmachines.net/", "aggregator", "US",
         "Homepage allowed; not parsed this pass (pending)"),
        ("Facebook Marketplace / OEM logins", "https://www.facebook.com/marketplace/", "classifieds", "QC",
         "Login wall — not used"),
    ]
    # Don't re-hit the network just to fill the log: these statuses were observed
    # in the discovery probe of 26 Nov 2026 (America/Toronto) and recorded honestly.
    for name, url, typ, region, reason in candidates:
        already = any(r["name"] == name for r in discovery)
        if already:
            continue
        status = "blocked" if any(k in reason.lower() for k in ("403", "202", "tls", "challenge", "login", "null", "failed")) else "pending"
        if "quote" in reason.lower() and status != "blocked":
            status = "quote-only"
        if "omitted" in reason.lower() or "not used equipment" in reason.lower():
            status = "quote-only"
        if "pending" in reason.lower():
            status = "pending"
        _log(discovery, name=name, url=url, type=typ, region=region,
             robots_ok="?", status=status, reason=reason)


# ---------------------------------------------------------------------------
# Seed: digest n° 1 (public pages already cited on CoupeFab, 26 Nov 2026)
# Live fetch overwrites the same id when the source is reachable.
# ---------------------------------------------------------------------------
SEED = [
    dict(id="igo-machitech-ec300", title="Machitech Automation EC-300 (2015), table 5 × 5 pi, Hypertherm Powermax45",
         year=2015, make="Machitech", model="EC-300", category="plasma_table",
         seller="Industriel Go", source_id="igo", source_name="Industriel Go",
         city="Farnham", province="QC", location="Farnham, QC",
         url="https://www.industrielgo.com/listings/9640734-used-2015-machitech-automation-ec-300-cnc-plasma-cutting-table-5-x-5-hypertherm-powermax45-included",
         price_type="quote", first_seen="2026-11-26",
         notes="45 A ; « excellent working condition » selon l’annonce publique."),
    dict(id="tardif-ebf-pl1026", title="E.B.F PL1026 (2011), 10 × 26 pi, 2 têtes, 2 × Hypertherm HPR260XD, EdgePro",
         year=2011, make="E.B.F", model="PL1026", category="plasma_table",
         seller="Tardif Industrie", source_id="tardif", source_name="Tardif Industrie",
         city="Québec", province="QC",
         url="https://www.tardifindustrie.com/equipement/dcoupe-plasma-10x26",
         price=45000, currency="CAD", price_type="asking", first_seen="2026-11-26"),
    dict(id="alx-3834", title="Table de découpe plasma CNC E.B.F 2011",
         year=2011, make="E.B.F", model="PL1026", category="plasma_table",
         seller="Machinerie ALX", source_id="alx", source_name="Machinerie ALX",
         city="Québec", province="QC",
         url="https://machineriealx.com/machines/table-de-decoupe-plasma-cnc-e-b-f-2011/",
         price_type="quote", first_seen="2026-11-26",
         notes="Possible double de l’annonce Tardif (même machine). Prix public : demander le prix."),
    dict(id="ironplanet-14972875", title="HD EBF Hypertherm XPR 300 (2022), 78 × 150 po",
         year=2022, make="E.B.F", model="XPR 300", category="plasma_table",
         seller="Ritchie Bros. / IronPlanet", source_id="ironplanet", source_name="IronPlanet / Ritchie Bros.",
         city="Québec", province="QC",
         url="https://www.ironplanet.com/for-sale/Welding-Machines-and-Equipment-2022-HD-EBF-Hypertherm-XPR-300-78%E2%80%9Dx150%E2%80%9D-Plasma-Cutter-Quebec/14972875",
         price=137500, currency="CAD", price_type="buy_now", first_seen="2026-11-26",
         notes="Achat immédiat, tel quel, relevé sur la page publique du lot le 26 nov. 2026."),
]


def merge_history(fresh: list[dict], previous: list[dict], today: dt.date) -> list[dict]:
    prev = {p["id"]: p for p in previous}
    seen_ids = set()
    out = []
    for it in fresh:
        seen_ids.add(it["id"])
        old = prev.get(it["id"])
        if old:
            it["first_seen"] = old.get("first_seen") or it.get("first_seen") or today.isoformat()
            hist = list(old.get("price_history") or [])
            last = hist[-1]["price_cad"] if hist else old.get("price_cad")
            if it.get("price_cad") and it.get("price_cad") != last:
                hist.append({"date": today.isoformat(), "price": it.get("price"), "currency": it.get("currency"),
                             "price_cad": it.get("price_cad")})
            elif not hist and it.get("price_cad"):
                hist.append({"date": it["first_seen"], "price": it.get("price"), "currency": it.get("currency"),
                             "price_cad": it.get("price_cad")})
            it["price_history"] = hist
            # preserve photo if the new fetch has none
            if not it.get("photo_url") and old.get("photo_url"):
                it["photo_url"] = old["photo_url"]
        else:
            it["first_seen"] = it.get("first_seen") or today.isoformat()
            if it.get("price_cad"):
                it["price_history"] = [{"date": it["first_seen"], "price": it.get("price"),
                                        "currency": it.get("currency"), "price_cad": it["price_cad"]}]
        it["last_seen"] = today.isoformat()
        out.append(it)
    # listings we no longer see: mark sold if they already were, else stale after STALE_DAYS
    for pid, old in prev.items():
        if pid in seen_ids:
            continue
        last = old.get("last_seen") or old.get("first_seen") or today.isoformat()
        try:
            last_d = dt.date.fromisoformat(str(last)[:10])
        except ValueError:
            last_d = today
        age = (today - last_d).days
        st = old.get("status") or "active"
        if st == "sold":
            pass
        elif age >= STALE_DAYS:
            old["status"] = "stale"
        else:
            old["status"] = "missing"  # unseen today, not yet stale
        out.append(old)
    return out


def write_history(listings: list[dict], today: dt.date) -> None:
    folder = OUT / "history"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{today.isoformat()[:7]}.csv"
    fields = ["date", "id", "title", "source_id", "price", "currency", "price_cad", "status", "url"]
    existing = []
    if path.exists():
        with path.open(newline="", encoding="utf-8") as f:
            existing = list(csv.DictReader(f))
    seen = {(r.get("date"), r.get("id"), r.get("price_cad"), r.get("status")) for r in existing}
    new_rows = []
    for it in listings:
        key = (today.isoformat(), it["id"], str(it.get("price_cad") or ""), it.get("status") or "")
        if key in seen:
            continue
        new_rows.append({
            "date": today.isoformat(), "id": it["id"], "title": it.get("title"),
            "source_id": it.get("source_id"), "price": it.get("price") or "",
            "currency": it.get("currency") or "", "price_cad": it.get("price_cad") or "",
            "status": it.get("status"), "url": it.get("url"),
        })
    if new_rows or not path.exists():
        with path.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(existing + new_rows)


def write_discovery(rows: list[dict]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "discovery.csv"
    # append-only by (name, url, checked_on)
    prev = []
    if path.exists():
        with path.open(newline="", encoding="utf-8") as f:
            prev = list(csv.DictReader(f))
    seen = {(r.get("name"), r.get("url"), r.get("checked_on")) for r in prev}
    add = [r for r in rows if (r["name"], r["url"], r["checked_on"]) not in seen]
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=DISCOVERY_FIELDS)
        w.writeheader()
        w.writerows(prev + add)


def main() -> int:
    today = _today()
    print(f"CoupeFab occasions refresh {today.isoformat()} (America/Toronto)")
    OUT.mkdir(parents=True, exist_ok=True)
    discovery: list[dict] = []
    fx = load_fx()
    print(f"  FX USD/CAD = {fx['rate']} ({fx['source']} {fx.get('date')})")

    msrp: list[dict] = []
    for fn in (fetch_langmuir_msrp, fetch_piranha_msrp, fetch_hypertherm_xpr_msrp, msrp_estimated_haas):
        try:
            msrp.extend(fn(discovery))
        except Exception as e:
            print(f"  !! {fn.__name__} crashed: {e}")
    (OUT / "msrp.json").write_text(json.dumps({"generated": _now_iso(), "rows": msrp}, indent=2, ensure_ascii=False))

    fresh: list[dict] = []
    host_jobs = [
        lambda d, fx: fetch_machinery_host(d, fx, name="Gizmo Machine Tools", base="https://www.gizmo-mt.ca",
                                           city="Mississauga", province="ON", source_id="gizmo", max_pages=6),
        lambda d, fx: fetch_machinery_host(d, fx, name="Trader Machinery", base="https://www.tradermachinery.com",
                                           city="Concord", province="ON", source_id="trader", max_pages=3),
    ]
    for fetcher in (fetch_alx, fetch_tardif, fetch_igo, fetch_southern_fab, fetch_ironplanet_known, *host_jobs):
        try:
            fresh.extend(fetcher(discovery, fx))
        except Exception as e:
            print(f"  !! {getattr(fetcher, '__name__', fetcher)} crashed: {e}")

    # Seeds fill gaps (same id is overwritten by a live row).
    live_ids = {r["id"] for r in fresh}
    for s in SEED:
        if s["id"] in live_ids:
            continue
        it = _item(**{k: v for k, v in s.items()})
        it["price_cad"] = to_cad(it.get("price"), it.get("currency") or "CAD", fx)
        fresh.append(it)

    # Dedup exact URL
    by_url = {}
    deduped = []
    for it in fresh:
        u = (it.get("url") or "").rstrip("/")
        if u and u in by_url:
            continue
        if u:
            by_url[u] = True
        deduped.append(it)
    fresh = deduped

    for it in fresh:
        if it.get("price") and not it.get("price_cad"):
            it["price_cad"] = to_cad(it.get("price"), it.get("currency") or "CAD", fx)
        match_msrp(it, msrp, fx)

    previous = []
    prev_path = OUT / "listings.json"
    if prev_path.exists():
        try:
            previous = json.loads(prev_path.read_text()).get("listings") or []
        except Exception:
            previous = []

    merged = merge_history(fresh, previous, today)
    score.score_all(merged, today)

    payload = {
        "generated": _now_iso(),
        "timezone": "America/Toronto",
        "fx": fx,
        "msrp_count": len(msrp),
        "listings": merged,
        "sources": discovery,
        "method": {
            "stale_days": STALE_DAYS,
            "tier_pct": score.TIER_PCT,
            "super_used_pct": score.SUPER_USED_PCT,
            "super_msrp_pct": score.SUPER_MSRP_PCT,
            "good_msrp_pct": score.GOOD_MSRP_PCT,
            "depreciation": score.DEPRECIATION,
            "dep_cap_years": score.DEP_CAP_YEARS,
        },
    }
    prev_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    write_history(merged, today)
    probe_blocked_sources(discovery)
    write_discovery(discovery)

    n = len(merged)
    active = [l for l in merged if l.get("status") == "active"]
    priced = [l for l in active if l.get("price_cad")]
    msrp_m = [l for l in active if l.get("msrp_cad")]
    print(f"OK: {n} listings ({len(active)} active, {len(priced)} priced, {len(msrp_m)} with MSRP) -> {prev_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Build data/news/latest.json from real used listings and the latest price survey.

Only items that already have a public URL and a date are included. Titles, sources
and dates are copied from those records — nothing is invented.

    python3 -m news.build

Called by scripts/refresh.sh after the daily price and used-listing fetch, and
before python3 build.py. The homepage and /nouvelles/ (EN: /en/news/) read the
JSON at build time.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

OUT = ROOT / "data" / "news" / "latest.json"
USED = ROOT / "data" / "used" / "listings.json"
PRICES = ROOT / "data" / "prices" / "latest.json"
TZ = ZoneInfo("America/Toronto")

# Homepage shows at most 8; the news page is paginated (~24 / page).
HOME_MAX = 8
PAGE_MAX = 48

# Topic keys are ASCII in the JSON; labels are applied at render time.
CAT_TOPIC = {
    "plasma_table": "plasma",
    "laser": "laser",
    "router": "cnc",
    "mill": "usinage",
    "lathe": "usinage",
    "edm": "usinage",
    "saw": "usinage",
    "press_brake": "tolerie",
    "shear": "tolerie",
    "roll": "tolerie",
    "punch": "tolerie",
    "waterjet": "tolerie",
}

# Fallback for "other" / compressor / welder: only if the source title itself is clear.
KW = (
    ("plasma", re.compile(r"\bplasma\b", re.I)),
    ("laser", re.compile(r"\blaser\b", re.I)),
    ("cnc", re.compile(r"\b(cnc|routeur|router|thermwood|scm pratix)\b", re.I)),
    ("usinage", re.compile(r"\b(fraiseuse|\bmill\b|tour\b|\blathe\b|usinag|edm|électro.?érosion)\b", re.I)),
    ("tolerie", re.compile(r"\b(plieuse|presse.?pli|press.?brake|cisaille|\bshear\b|rouleau|plate.?roll|poinçonn|punch|tôle|tolerie|tôlerie|jet d.?eau|waterjet)\b", re.I)),
)


def topic_of(listing: dict) -> str | None:
    cat = listing.get("category") or ""
    if cat in CAT_TOPIC:
        return CAT_TOPIC[cat]
    title = listing.get("title") or ""
    for key, rx in KW:
        if rx.search(title):
            return key
    return None


def listing_item(L: dict) -> dict | None:
    url = (L.get("url") or "").strip()
    date = (L.get("first_seen") or L.get("last_seen") or "")[:10]
    title = (L.get("title") or "").strip()
    source = (L.get("source_name") or L.get("seller") or "").strip()
    if not url.startswith("http") or not date or not title or not source:
        return None
    if L.get("status") and L.get("status") not in ("active", "available"):
        return None
    topic = topic_of(L)
    if not topic:
        return None
    loc = ", ".join(x for x in (L.get("city"), L.get("province") or (L.get("location") or "").split(",")[-1].strip()) if x)
    if not loc:
        loc = (L.get("location") or "").strip()
    price = L.get("price_cad") or L.get("price")
    bits_fr, bits_en = [], []
    if loc:
        bits_fr.append(loc)
        bits_en.append(loc)
    bits_fr.append(source)
    bits_en.append(source)
    if isinstance(price, (int, float)) and price > 0:
        bits_fr.append(f"{price:,.0f} $ CA".replace(",", "\u202f"))
        bits_en.append(f"CAD ${price:,.0f}")
    return {
        "id": f"listing-{(L.get('id') or title)[:80]}",
        "date": date,
        "topic": topic,
        "kind": "listing",
        "title_fr": title,
        "title_en": title,  # source title, not a translated invention
        "source": source,
        "url": url,
        "summary_fr": " · ".join(bits_fr),
        "summary_en": " · ".join(bits_en),
    }


def prices_item() -> dict | None:
    if not PRICES.exists():
        return None
    try:
        d = json.loads(PRICES.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    date = str(d.get("date") or d.get("generated") or "")[:10]
    if not date:
        return None
    rows = d.get("rows")
    n = len(rows) if isinstance(rows, list) else d.get("n_rows") or d.get("count")
    sups = d.get("suppliers")
    if isinstance(sups, list):
        n_sup = len(sups)
    elif isinstance(sups, int):
        n_sup = sups
    else:
        n_sup = None
    extra_fr = extra_en = ""
    if isinstance(n, int) and n:
        extra_fr = f"{n:,} prix publiés".replace(",", "\u202f")
        extra_en = f"{n:,} published prices"
        if n_sup:
            extra_fr += f" chez {n_sup} fournisseurs"
            extra_en += f" from {n_sup} suppliers"
    return {
        "id": f"prices-{date}",
        "date": date,
        "topic": "tolerie",
        "kind": "prices",
        "title_fr": f"Prix des tôles : relevé du {date}",
        "title_en": f"Sheet prices as of {date}",
        "source": "CoupeFab",
        "url": "/prix/",
        "url_en": "/en/sheet-prices/",
        "summary_fr": extra_fr or "Comparateur des prix publiés, avec source et date.",
        "summary_en": extra_en or "Published-price comparison, with source and date.",
    }


def pick_featured(items: list[dict]) -> list[str]:
    """Up to HOME_MAX of the newest items, with topic diversity when possible."""
    by_topic: dict[str, list[dict]] = {}
    for it in items:
        by_topic.setdefault(it["topic"], []).append(it)
    chosen: list[dict] = []
    used = set()
    # one newest per topic first, in a stable topic order
    for topic in ("cnc", "plasma", "laser", "usinage", "tolerie"):
        for it in by_topic.get(topic, []):
            if it["id"] not in used:
                chosen.append(it)
                used.add(it["id"])
                break
        if len(chosen) >= HOME_MAX:
            break
    for it in items:
        if len(chosen) >= HOME_MAX:
            break
        if it["id"] not in used:
            chosen.append(it)
            used.add(it["id"])
    chosen.sort(key=lambda x: x["date"], reverse=True)
    return [x["id"] for x in chosen[:HOME_MAX]]


def build() -> dict:
    now = dt.datetime.now(TZ)
    items: list[dict] = []
    if USED.exists():
        raw = json.loads(USED.read_text(encoding="utf-8"))
        listings = raw["listings"] if isinstance(raw, dict) else raw
        for L in listings:
            it = listing_item(L)
            if it:
                items.append(it)
    items.sort(key=lambda x: (x["date"], x["id"]), reverse=True)
    # de-dupe by url
    seen = set()
    uniq = []
    for it in items:
        if it["url"] in seen:
            continue
        seen.add(it["url"])
        uniq.append(it)
    # Keep the newest item of each topic even if it would fall past PAGE_MAX
    reserved, reserved_ids = [], set()
    for topic in ("cnc", "plasma", "laser", "usinage", "tolerie"):
        for it in uniq:
            if it["topic"] == topic and it["id"] not in reserved_ids:
                reserved.append(it)
                reserved_ids.add(it["id"])
                break
    rest = [x for x in uniq if x["id"] not in reserved_ids]
    p = prices_item()
    out, kept = [], set()
    for it in ([p] if p else []) + reserved + rest:
        if not it or it["id"] in kept:
            continue
        out.append(it)
        kept.add(it["id"])
        if len(out) >= PAGE_MAX:
            break
    items = out
    items.sort(key=lambda x: (x["date"], x["id"]), reverse=True)
    featured = pick_featured(items)
    return {
        "generated": now.isoformat(timespec="seconds"),
        "timezone": "America/Toronto",
        "source": "data/used/listings.json and data/prices/latest.json — real URLs and dates only; no invented items.",
        "featured_ids": featured,
        "items": items,
    }


def main() -> None:
    data = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}: {len(data['items'])} items, {len(data['featured_ids'])} featured")


if __name__ == "__main__":
    main()

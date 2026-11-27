#!/usr/bin/env python3
"""Build data/news/latest.json from trade-outlet RSS feeds.

Worldwide CNC, machining, laser, plasma and fabrication industry news and new
technology. Titles, dates, source names and short excerpts are taken from the
feeds — full articles are never copied, and nothing is invented.

    python3 -m news.build

Called by scripts/refresh.sh before python3 build.py. The homepage and
/nouvelles/ (EN: /en/news/) read the JSON at build time.
"""
from __future__ import annotations

import datetime as dt
import email.utils
import hashlib
import html
import json
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

OUT = ROOT / "data" / "news" / "latest.json"
TZ = ZoneInfo("America/Toronto")
UA = "CoupeFabNews/1.0 (+https://coupefab.ca/)"
TIMEOUT = 15

# Homepage shows at most 6; the news page is paginated (~24 / page).
HOME_MAX = 6
PAGE_MAX = 48

# Specialized trade outlets are already on-topic; broader feeds are filtered.
FEEDS = [
    {"name": "Modern Machine Shop", "url": "https://www.mmsonline.com/rss/articles", "strict": False},
    {"name": "Cutting Tool Engineering", "url": "https://www.ctemag.com/rss", "strict": False},
    {"name": "Canadian Metalworking", "url": "https://www.canadianmetalworking.com/rss", "strict": False},
    {"name": "Production Machining", "url": "https://www.productionmachining.com/rss/articles", "strict": False},
    {"name": "The Fabricator", "url": "https://www.thefabricator.com/rss/articles", "strict": False},
    {"name": "Fabricating & Metalworking", "url": "https://www.fabricatingandmetalworking.com/feed/", "strict": False},
    {"name": "Manufacturing Tomorrow", "url": "https://www.manufacturingtomorrow.com/rss.xml", "strict": True},
    {"name": "Manufacturing Tomorrow", "url": "https://www.manufacturingtomorrow.com/feed/", "strict": True},
    {"name": "Additive Manufacturing", "url": "https://www.additivemanufacturing.media/rss/articles", "strict": True},
    {"name": "Hypertherm", "url": "https://blog.hypertherm.com/feed/", "strict": True},
]

TOPIC_RX = (
    ("plasma", re.compile(r"\bplasma\b", re.I)),
    ("laser", re.compile(r"\b(laser|fibre.?laser|fiber.?laser|co2 laser)\b", re.I)),
    ("tolerie", re.compile(r"\b(fabricat|sheet metal|press.?brake|plieuse|t[oô]le|weld|soudure|waterjet|jet d.?eau|punch|shear|cisaille|bending|pliage)\b", re.I)),
    ("usinage", re.compile(r"\b(machin(e|ing)|mill|lathe|turning|fraiseuse|usinage|spindle|cutting tool|toolholder|edm|broach|tap(?:ping)?|insert)\b", re.I)),
    ("cnc", re.compile(r"\b(cnc|cam\b|cad/cam|controller|five.?axis|5-axis|robot|automat|additive|machine tool)\b", re.I)),
)

# Items must look like industry/tech news. Off-topic even from a trade magazine is dropped.
ON_TOPIC = re.compile(
    r"\b(cnc|machin(e|ing)|mill|lathe|laser|plasma|fabricat|sheet metal|press.?brake|"
    r"cutting tool|tooling|spindle|cam\b|cad\b|weld|automat|robot|additive|"
    r"metalwork|machine tool|turning|milling|usinage|t[oô]le|plieuse|soudure|"
    r"waterjet|hypertherm|haas|trumpf|bystronic|mazak|okuma|dmu|fanuc|siemens|"
    r"mastercam|solidworks|fusion 360|metrology|probe|coolant|toolholder)\b",
    re.I,
)
OFF_TOPIC = re.compile(
    r"\b(recipe|celebrity|sports?|football|nba|nfl|horoscope|coupon)\b",
    re.I,
)
TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")
NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "content": "http://purl.org/rss/1.0/modules/content/",
    "dc": "http://purl.org/dc/elements/1.1/",
}


def _text(el: ET.Element | None) -> str:
    if el is None:
        return ""
    parts = [el.text or ""]
    for c in el:
        parts.append(_text(c))
        parts.append(c.tail or "")
    return "".join(parts)


def excerpt(raw: str, limit: int = 220) -> str:
    if not raw:
        return ""
    t = html.unescape(TAG_RE.sub(" ", raw))
    t = WS_RE.sub(" ", t).strip()
    if len(t) <= limit:
        return t
    cut = t[: limit + 1]
    sp = cut.rfind(" ")
    return (cut[:sp] if sp > 80 else t[:limit]).rstrip(" ,;:-") + "…"


def parse_date(raw: str) -> str:
    raw = (raw or "").strip()
    if not raw:
        return ""
    # ISO-like
    m = re.match(r"(\d{4}-\d{2}-\d{2})", raw)
    if m:
        return raw[:10]
    try:
        d = email.utils.parsedate_to_datetime(raw)
        if d.tzinfo is None:
            d = d.replace(tzinfo=dt.timezone.utc)
        return d.astimezone(TZ).date().isoformat()
    except (TypeError, ValueError, OverflowError):
        pass
    m = re.search(r"(\d{4}-\d{2}-\d{2})", raw)
    return m.group(1) if m else ""


def topic_of(title: str, excerpt_txt: str) -> str:
    blob = f"{title} {excerpt_txt}"
    for key, rx in TOPIC_RX:
        if rx.search(blob):
            return key
    return "cnc"


def relevant(title: str, excerpt_txt: str, strict: bool) -> bool:
    blob = f"{title} {excerpt_txt}"
    if OFF_TOPIC.search(blob) and not ON_TOPIC.search(blob):
        return False
    if strict:
        return bool(ON_TOPIC.search(blob))
    return True


def fetch(url: str) -> bytes | None:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": UA,
            "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml, */*",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return r.read()
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as e:
        print(f"WARN: feed failed {url}: {e}", file=sys.stderr)
        return None


def local(tag: str) -> str:
    return tag.split("}", 1)[-1] if tag.startswith("{") else tag


def entries_from(root: ET.Element) -> list[dict]:
    out = []
    # RSS 2
    for item in root.findall("./channel/item") + root.findall("channel/item"):
        out.append({
            "title": _text(item.find("title")),
            "url": _text(item.find("link")) or _text(item.find("guid")),
            "date": parse_date(_text(item.find("pubDate")) or _text(item.find("{http://purl.org/dc/elements/1.1/}date"))),
            "summary": _text(item.find("description")) or _text(item.find("{http://purl.org/rss/1.0/modules/content/}encoded")),
        })
    # Atom
    for item in root.findall("{http://www.w3.org/2005/Atom}entry") + root.findall("entry"):
        link = ""
        for ln in list(item):
            if local(ln.tag) == "link":
                href = ln.attrib.get("href") or _text(ln)
                typ = ln.attrib.get("rel", "alternate")
                if href and typ in ("alternate", ""):
                    link = href
                    break
                if href and not link:
                    link = href
        out.append({
            "title": _text(item.find("{http://www.w3.org/2005/Atom}title")) or _text(item.find("title")),
            "url": link,
            "date": parse_date(
                _text(item.find("{http://www.w3.org/2005/Atom}updated"))
                or _text(item.find("{http://www.w3.org/2005/Atom}published"))
                or _text(item.find("updated"))
                or _text(item.find("published"))
            ),
            "summary": _text(item.find("{http://www.w3.org/2005/Atom}summary"))
            or _text(item.find("{http://www.w3.org/2005/Atom}content"))
            or _text(item.find("summary")),
        })
    return out


def items_from_feed(feed: dict) -> list[dict]:
    raw = fetch(feed["url"])
    if not raw:
        return []
    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        try:
            from lxml import etree
            recovered = etree.tostring(etree.fromstring(raw, etree.XMLParser(recover=True)))
            root = ET.fromstring(recovered)
        except Exception as e:
            print(f"WARN: bad XML {feed['url']}: {e}", file=sys.stderr)
            return []
    items = []
    for e in entries_from(root):
        title = WS_RE.sub(" ", html.unescape(e["title"] or "")).strip()
        url = (e["url"] or "").strip()
        date = e["date"]
        summary = excerpt(e["summary"] or "")
        if not title or not date or not url.startswith("http"):
            continue
        if not relevant(title, summary, feed["strict"]):
            continue
        source = feed["name"]
        items.append({
            "id": f"{re.sub(r'[^a-z0-9]+', '-', source.lower())}-{date}-{hashlib.sha1(url.encode()).hexdigest()[:10]}",
            "date": date,
            "topic": topic_of(title, summary),
            "kind": "industry",
            "title_fr": title,
            "title_en": title,
            "source": source,
            "url": url,
            "summary_fr": summary,
            "summary_en": summary,
        })
    return items


def pick_featured(items: list[dict]) -> list[str]:
    by_topic: dict[str, list[dict]] = {}
    for it in items:
        by_topic.setdefault(it["topic"], []).append(it)
    chosen: list[dict] = []
    used = set()
    used_sources: set[str] = set()
    for topic in ("cnc", "plasma", "laser", "usinage", "tolerie"):
        cands = by_topic.get(topic, [])
        pick = next((it for it in cands if it["source"] not in used_sources and it["id"] not in used), None)
        if pick is None:
            pick = next((it for it in cands if it["id"] not in used), None)
        if pick:
            chosen.append(pick)
            used.add(pick["id"])
            used_sources.add(pick["source"])
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
    seen_urls = set()
    seen_names = set()
    for feed in FEEDS:
        if feed["name"] in seen_names and not items:
            pass
        # Skip a second URL for a source that already yielded items
        if feed["name"] in seen_names:
            # still try only if that source produced nothing
            if any(it["source"] == feed["name"] for it in items):
                continue
        got = items_from_feed(feed)
        if got:
            seen_names.add(feed["name"])
        for it in got:
            key = it["url"].split("?")[0].rstrip("/")
            if key in seen_urls:
                continue
            seen_urls.add(key)
            items.append(it)
    items.sort(key=lambda x: (x["date"], x["id"]), reverse=True)
    items = items[:PAGE_MAX]
    featured = pick_featured(items)
    sources = sorted({it["source"] for it in items})
    return {
        "generated": now.isoformat(timespec="seconds"),
        "timezone": "America/Toronto",
        "source": "Trade-outlet RSS (CNC, machining, laser, plasma, fabrication). Titles, dates and short excerpts only; no full articles.",
        "feeds": sources,
        "featured_ids": featured,
        "items": items,
    }


def main() -> None:
    data = build()
    if not data["items"] and OUT.exists():
        print("WARN: no live items; keeping previous data/news/latest.json", file=sys.stderr)
        return
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}: {len(data['items'])} items, {len(data['featured_ids'])} featured from {', '.join(data['feeds']) or '—'}")


if __name__ == "__main__":
    main()

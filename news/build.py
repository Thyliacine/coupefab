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
import urllib.parse
import time
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
    {"name": "Modern Machine Shop", "url": "https://www.mmsonline.com/rss/articles", "strict": False, "lang": "en"},
    {"name": "Cutting Tool Engineering", "url": "https://www.ctemag.com/rss", "strict": False, "lang": "en"},
    {"name": "Canadian Metalworking", "url": "https://www.canadianmetalworking.com/rss", "strict": False, "lang": "en"},
    {"name": "Production Machining", "url": "https://www.productionmachining.com/rss/articles", "strict": False, "lang": "en"},
    {"name": "The Fabricator", "url": "https://www.thefabricator.com/rss/articles", "strict": False, "lang": "en"},
    {"name": "Fabricating & Metalworking", "url": "https://www.fabricatingandmetalworking.com/feed/", "strict": False, "lang": "en"},
    {"name": "Manufacturing Tomorrow", "url": "https://www.manufacturingtomorrow.com/rss.xml", "strict": True, "lang": "en"},
    {"name": "Manufacturing Tomorrow", "url": "https://www.manufacturingtomorrow.com/feed/", "strict": True, "lang": "en"},
    {"name": "Additive Manufacturing", "url": "https://www.additivemanufacturing.media/rss/articles", "strict": True, "lang": "en"},
    {"name": "Hypertherm", "url": "https://blog.hypertherm.com/feed/", "strict": True, "lang": "en"},
    {"name": "Metal-Interface", "url": "https://www.metal-interface.com/rss.xml", "strict": False, "lang": "fr"},
    {"name": "Techniques de l’Ingénieur", "url": "https://www.techniques-ingenieur.fr/actualite/rss/", "strict": True, "lang": "fr"},
    {"name": "A3DM Magazine", "url": "https://www.a3dm-magazine.fr/feed/", "strict": True, "lang": "fr"},
    {"name": "Mesures", "url": "https://www.mesures.com/feed/", "strict": True, "lang": "fr"},
    {"name": "Actualité machine-outil", "url": "https://news.google.com/rss/search?q=%22machine-outil%22+OR+usinage+OR+t%C3%B4lerie+OR+%22d%C3%A9coupe+laser%22+OR+%22d%C3%A9coupe+plasma%22+OR+%22fabrication+m%C3%A9tallique%22+OR+%22centre+d%27usinage%22+-cin%C3%A9ma+-film+-audiovisuel&hl=fr&gl=FR&ceid=FR:fr", "strict": False, "lang": "fr", "google": True},
    {"name": "Usine Nouvelle", "url": "https://news.google.com/rss/search?q=site:usinenouvelle.com+(usinage+OR+machine-outil+OR+%22d%C3%A9coupe+laser%22+OR+plasma+OR+t%C3%B4lerie+OR+CNC)&hl=fr&gl=FR&ceid=FR:fr", "strict": True, "lang": "fr", "google": True},
    {"name": "Machines Production", "url": "https://news.google.com/rss/search?q=site:machinesproduction.fr+(machine+OR+usinage+OR+CNC+OR+laser+OR+robot+OR+fraise+OR+outil)&hl=fr&gl=FR&ceid=FR:fr", "strict": True, "lang": "fr", "google": True},
    {"name": "Industrie & Technologies", "url": "https://news.google.com/rss/search?q=site:industrie-techno.com+(CNC+OR+machine+OR+usinage+OR+laser+OR+robot)&hl=fr&gl=FR&ceid=FR:fr", "strict": True, "lang": "fr", "google": True},
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
    r"mastercam|solidworks|fusion 360|metrology|probe|coolant|toolholder|"
    r"machine-?outil|m[eé]tallurgie|d[eé]coupe|t[oô]lerie|fabrication additive|"
    r"outillage|fraisage|tournage)\b",
    re.I,
)
OFF_TOPIC = re.compile(
    r"\b(recipe|celebrity|sports?|football|nba|nfl|horoscope|coupon|"
    r"cin[eé]ma|cin[eé]matograph|documentaire|audiovisuel|arcom|"
    r"filmoth[eè]que|coproduction|festival de (film|cin[eé])|aviron)\b",
    re.I,
)
GENERIC_TITLE = re.compile(
    r"^(entreprise|le contenu à la une|à la une|actualités?|emplois?|"
    r"newsletter|accueil|offre d.emploi|les offres)\b",
    re.I,
)
CINEMA_SOURCE = re.compile(r"cnc\.fr|ecran total|écran total", re.I)
MAX_PER_SOURCE = 8
LOOKS_FRENCH = re.compile(
    r"[àâäéèêëïîôùûüçœ]|\b(le|la|les|un|une|des|du|de la|et|pour|dans|avec|sur|cette|comment|pourquoi|quels?|une|aux)\b",
    re.I,
)
LOOKS_ENGLISH = re.compile(
    r"\b(the|and|for|with|from|how|why|when|what|this|that|into|showcase|manual|reshaping|reclaiming|welding)\b",
    re.I,
)
PRODUCT_LISTING = re.compile(r"(?i)(machine de d[eé]coupe.*\|\s*\S+|per[cç]age,\s*taraudage.*\|)")
TRADE_SOURCE = re.compile(
    r"usine nouvelle|machines production|metal-interface|techniques de l.ing|"
    r"a3dm|mesures|industrie.{0,12}techno|magazine mci|canadian metalworking|"
    r"3dnatives|les echos|bref eco|fabrication industrielle|modern machine shop|"
    r"cutting tool|production machining|the fabricator|additive manufacturing",
    re.I,
)
BLOCK_SOURCE = re.compile(
    r"youtube|dreamjob|pressreader|fortune business|dakaractu|guineelive|"
    r"guin[eé]enews|notebookcheck|recrut|emploi|job\b",
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


def relevant(title: str, excerpt_txt: str, strict: bool, source: str = "") -> bool:
    title = (title or "").strip()
    if len(title) < 18 or GENERIC_TITLE.match(title) or PRODUCT_LISTING.search(title):
        return False
    if CINEMA_SOURCE.search(source or ""):
        return False
    blob = f"{title} {excerpt_txt} {source}"
    if OFF_TOPIC.search(blob) and not ON_TOPIC.search(blob):
        return False
    # Bare "CNC" in French is usually the film-funding body, not a machine tool.
    if re.search(r"\bcnc\b", blob, re.I) and not re.search(
        r"machine|usinage|laser|plasma|outil|frais|tournage|t[oô]l|fabricat|m[eé]tal",
        blob,
        re.I,
    ):
        return False
    if strict:
        return bool(ON_TOPIC.search(blob))
    return True


def cap_sources(items: list[dict], n: int = MAX_PER_SOURCE) -> list[dict]:
    counts: dict[str, int] = {}
    out: list[dict] = []
    for it in items:
        src = it.get("source") or ""
        if counts.get(src, 0) >= n:
            continue
        counts[src] = counts.get(src, 0) + 1
        out.append(it)
    return out


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
        src_el = item.find("source")
        out.append({
            "title": _text(item.find("title")),
            "url": _text(item.find("link")) or _text(item.find("guid")),
            "date": parse_date(_text(item.find("pubDate")) or _text(item.find("{http://purl.org/dc/elements/1.1/}date"))),
            "summary": _text(item.find("description")) or _text(item.find("{http://purl.org/rss/1.0/modules/content/}encoded")),
            "source": _text(src_el).strip() if src_el is not None else "",
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
        if not relevant(title, summary, feed["strict"], source=(e.get("source") or "") or feed["name"]):
            continue
        source = (e.get("source") or "").strip() or feed["name"]
        if feed.get("google") and " - " in title:
            title, maybe = title.rsplit(" - ", 1)
            title, maybe = title.strip(), maybe.strip()
            if maybe:
                source = maybe
        lang = feed.get("lang") or "en"
        items.append({
            "id": f"{re.sub(r'[^a-z0-9]+', '-', source.lower())}-{date}-{hashlib.sha1(url.encode()).hexdigest()[:10]}",
            "date": date,
            "topic": topic_of(title, summary),
            "kind": "industry",
            "lang": lang,
            "translated": False,
            "via_google": bool(feed.get("google")),
            "title_fr": title,
            "title_en": title,
            "source": source,
            "url": url,
            "summary_fr": summary,
            "summary_en": summary,
        })
    return items



def translate_to_fr(text: str) -> str | None:
    """Machine-translate a short title or excerpt. Returns None on failure — never invent."""
    text = (text or "").strip()
    if not text:
        return ""
    try:
        from deep_translator import GoogleTranslator
        out = GoogleTranslator(source="en", target="fr").translate(text)
        time.sleep(0.35)
        return (out or "").strip() or None
    except Exception as e:
        print(f"WARN: translate failed: {e}", file=sys.stderr)
        return None


def translated_item(it: dict) -> dict | None:
    title = translate_to_fr(it.get("title_en") or it.get("title_fr") or "")
    if not title:
        return None
    summary_src = it.get("summary_en") or it.get("summary_fr") or ""
    summary = translate_to_fr(summary_src) if summary_src else ""
    if summary is None:
        summary = ""
    out = dict(it)
    out["id"] = it["id"] + "-tr"
    out["lang"] = "fr"
    out["translated"] = True
    out["title_fr"] = title
    out["summary_fr"] = summary
    return out


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
    for it in items:
        title = it.get("title_fr") or it.get("title_en") or ""
        if it.get("lang") == "fr" and not LOOKS_FRENCH.search(title) and LOOKS_ENGLISH.search(title):
            it["lang"] = "en"
            it["title_en"] = title
            it["summary_en"] = it.get("summary_en") or it.get("summary_fr") or ""
    def keep_fr(it: dict) -> bool:
        src = it.get("source") or ""
        title = it.get("title_fr") or ""
        if BLOCK_SOURCE.search(src):
            return False
        if it.get("via_google") and not TRADE_SOURCE.search(src):
            return False
        if (it.get("date") or "")[:4] < "2025":
            return False
        if not LOOKS_FRENCH.search(title):
            return False
        if re.search(r"d[eé]coupe laser.*\|", title, re.I):
            return False
        if re.search(r"toute l['’]actualité", title, re.I):
            return False
        return True
    fr_items = cap_sources([it for it in items if it.get("lang") == "fr" and keep_fr(it)])[:PAGE_MAX]
    en_items = cap_sources([it for it in items if it.get("lang") != "fr"])[:PAGE_MAX]
    # Only translate when French copy is short of a full home+page set.
    fr_target = max(HOME_MAX, 12)
    if len(fr_items) < fr_target:
        for it in en_items:
            if len(fr_items) >= fr_target:
                break
            tr = translated_item(it)
            if tr:
                fr_items.append(tr)
    all_items = fr_items + [it for it in en_items if it["id"] not in {x["id"] for x in fr_items}]
    featured_fr = pick_featured(fr_items)
    featured_en = pick_featured(en_items)
    sources = sorted({it["source"] for it in all_items})
    return {
        "generated": now.isoformat(timespec="seconds"),
        "timezone": "America/Toronto",
        "source": "Trade-outlet RSS in French and English (CNC, machining, laser, plasma, fabrication). Titles, dates and short excerpts only; no full articles. English fillers on the FR site are machine-translated and marked.",
        "feeds": sources,
        "featured_ids": featured_fr,
        "featured_ids_fr": featured_fr,
        "featured_ids_en": featured_en,
        "items": all_items,
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

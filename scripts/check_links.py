#!/usr/bin/env python3
"""CoupeFab outbound link checker.

Finds every outbound (http/https) link shipped by the built site -- HTML pages, the JSON data
files (prices, tooling, parts, used equipment, machine cards, coolant sources), JS bundles --
checks each unique URL with a real browser-like GET, and reports the ones that are broken.

A link is BAD when:
  broken    404 / 410 / 5xx that persists / dead domain / TLS failure / timeout
  soft404   200 but the page says "not found", "page introuvable", "discontinued",
            "product unavailable" ..., or it redirected to the home page / a search page
  pointless it loads but shows nothing useful for the item (empty search, empty category,
            generic homepage behind a buy link, Shopify variant that does not exist,
            search page with no product matching the item). See --render.
403 / 429 / Cloudflare challenge are "blocked", NOT broken; they are retried once in a headless
browser (Playwright) when --browser is given, otherwise only reported.

Usage (from the repo root, after `python3 build.py`):
  python3 scripts/check_links.py                 # buy links only (fast: prices, tooling, parts, used)
  python3 scripts/check_links.py --all           # every outbound link, incl. spec sources and guides
  python3 scripts/check_links.py --render        # also render search-URL / seller pages in Playwright
  python3 scripts/check_links.py --internal      # also verify internal links/anchors exist in the build
  python3 scripts/check_links.py --only-new      # reuse the cache (.link-cache.json): re-check only
                                                 # URLs not checked in the last 7 days
  python3 scripts/check_links.py --json out.json # machine-readable report

Exit status: 1 when a BUY link is broken / soft404 / pointless and is not listed in
scripts/link_baseline.json ("known" exceptions); 0 otherwise. Reference (non-buy) links
are reported but only fail the run with --strict.

Needs: python3, requests.  Optional: playwright (+ chromium) for --render / --browser.
"""
from __future__ import annotations

import argparse
import collections
import concurrent.futures as cf
import html as htmlmod
import json
import re
import sys
import threading
import time
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, unquote, parse_qs

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124.0 Safari/537.36")
HEADERS = {"User-Agent": UA, "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Language": "fr-CA,fr;q=0.9,en;q=0.8"}
SKIP_HOSTS = re.compile(r"^(www\.)?(coupefab\.ca|coupefab\.vercel\.app|schema\.org|w3\.org|sitemaps\.org|"
                        r"vercel\.com|localhost)$|^(www\.)?(w3|sitemaps)\.org$", re.I)
URL_RE = re.compile(r"https?://[^\s\"'<>\\)\]}]+")
# Data files whose URLs are product / buy links (the thing a visitor clicks to buy or see a price).
BUY_FILES = {"prix/donnees.json", "prix/donnees-toles.json", "outillage/donnees.json",
             "pieces/donnees.json", "occasions/donnees.json"}
SCAN_EXT = (".html", ".json", ".js", ".csv", ".txt", ".xml", ".webmanifest")
SKIP_FILES = {"sitemap.xml", "robots.txt", "sw.js"}

SOFT_TITLE = re.compile(r"(page\s+not\s+found|page\s+introuvable|not\s+found|introuvable|404|"
                        r"n['’]existe\s+pas|does\s+not\s+exist|oops|no\s+longer\s+available|"
                        r"plus\s+disponible|discontinued|produit\s+non\s+disponible|"
                        r"product\s+(is\s+)?unavailable|unavailable)", re.I)
SOFT_BODY = re.compile(r"(page\s+not\s+found|page\s+introuvable|we\s+couldn['’]t\s+find\s+(that|the)\s+page|"
                       r"this\s+page\s+(doesn['’]t|does\s+not)\s+exist|cette\s+page\s+n['’]existe\s+pas|"
                       r"the\s+page\s+you\s+(were\s+)?looking\s+for|product\s+(is\s+)?(no\s+longer|unavailable)|"
                       r"this\s+product\s+is\s+(currently\s+)?unavailable|has\s+been\s+discontinued|"
                       r"produit\s+(n['’]est\s+plus|non)\s+disponible|ce\s+produit\s+n['’]existe\s+plus|"
                       r"no\s+products?\s+(were\s+)?found|aucun\s+produit\s+(trouv|ne\s+correspond)|"
                       r"0\s+results?\s+(found|for)|no\s+results?\s+(found|for)|aucun\s+r[ée]sultat)", re.I)
CHALLENGE = re.compile(r"(just\s+a\s+moment|un\s+instant,?\s+s['’]il|verifying\s+your\s+connection|v[ée]rification\s+de\s+votre|cf-chl|challenge-platform|attention\s+required|"
                       r"enable\s+javascript\s+and\s+cookies|captcha|access\s+denied|px-captcha|"
                       r"checking\s+your\s+browser)", re.I)
SEARCHY = re.compile(r"([?&](s|q|search|query|keyword|keywords|text|searchterm)=)|/(search|recherche|catalogsearch)(/|\?|$)", re.I)


# --------------------------------------------------------------------------- collection

def site_files():
    """Files that are shipped (same set as deploy_manifest) -- falls back to a walk."""
    try:
        import deploy_manifest as dm  # type: ignore
        return [p for p in dm.site_files()]
    except Exception:  # pragma: no cover
        return [p for p in ROOT.rglob("*") if p.is_file()]


def clean(u: str) -> str:
    u = htmlmod.unescape(u).rstrip(".,;:'\"")
    return u


def collect(root: Path, include_data: bool = True):
    """Return {url: {"kind": "buy"|"ref", "files": set, "names": list[str]}}."""
    out: dict[str, dict] = {}

    def add(url, kind, where, name=None):
        url = clean(url)
        m = urlsplit(url)
        if not m.netloc or SKIP_HOSTS.match(m.hostname or ""):
            return
        e = out.setdefault(url, {"kind": "ref", "files": set(), "names": []})
        if kind == "buy":
            e["kind"] = "buy"
        if len(e["files"]) < 4:
            e["files"].add(where)
        if name and len(e["names"]) < 3 and name not in e["names"]:
            e["names"].append(name)

    paths = list(site_files())
    if include_data:
        paths += [root / "data/tooling/prices.json"]  # not shipped itself, but feeds /outillage/
    for p in paths:
        p = Path(p)
        if not p.is_file() or p.name in SKIP_FILES or not p.name.endswith(SCAN_EXT):
            continue
        rel = p.relative_to(root).as_posix()
        try:
            text = p.read_text(errors="ignore")
        except OSError:
            continue
        if rel in BUY_FILES:
            try:
                data = json.loads(text)
            except ValueError:
                data = None
            if data is not None:
                _structured(rel, data, add)
                continue
        for u in set(URL_RE.findall(text)):
            add(u, "ref", rel)
    return out


def _structured(rel, data, add):
    if rel.startswith("prix/"):
        keys = data.get("keys") or []
        iu, idn = keys.index("url"), keys.index("description")
        ib = keys.index("buy_url") if "buy_url" in keys else None
        isup = keys.index("supplier")
        for r in data.get("rows", []):
            for i in (iu, ib):
                if i is not None and r[i]:
                    add(r[i], "buy", rel, f"{r[idn]}")
        for s in (data.get("suppliers") or {}).values():
            for k in ("site", "quote_url"):
                if s.get(k):
                    add(s[k], "ref", rel)
    elif rel.startswith("outillage/"):
        cols = data["cols"]
        iu, inm, isku = cols.index("url"), cols.index("name"), cols.index("sku")
        for r in data["rows"]:
            if r[iu]:
                add(r[iu], "buy", rel, f"{r[inm]} {r[isku] or ''}".strip())
    elif rel.startswith("pieces/"):
        for it in data["items"]:
            if it.get("source_url"):
                add(it["source_url"], "buy", rel, f"{it['name']} {it.get('sku') or ''}".strip())
    elif rel.startswith("occasions/"):
        for it in data["listings"]:
            if it.get("url"):
                add(it["url"], "buy", rel, it.get("title"))
            for k in ("msrp_source_url", "msrp_source_url_2", "photo_url"):
                if it.get(k):
                    add(it[k], "ref", rel)
    # any other URL in the file is a reference
    for u in set(URL_RE.findall(json.dumps(data, ensure_ascii=False))):
        add(u, "ref", rel)


# --------------------------------------------------------------------------- HTTP check

_tls = threading.local()


def session():
    import requests
    s = getattr(_tls, "s", None)
    if s is None:
        s = requests.Session()
        s.headers.update(HEADERS)
        a = requests.adapters.HTTPAdapter(pool_connections=4, pool_maxsize=4, max_retries=0)
        s.mount("http://", a)
        s.mount("https://", a)
        _tls.s = s
    return s


def page_text(body: str):
    title = re.search(r"<title[^>]*>(.*?)</title>", body, re.I | re.S)
    h1 = re.findall(r"<h1[^>]*>(.*?)</h1>", body, re.I | re.S)
    strip = lambda s: re.sub(r"\s+", " ", htmlmod.unescape(re.sub(r"<[^>]+>", " ", s))).strip()
    t = strip(title.group(1)) if title else ""
    h = strip(" ".join(h1[:3]))
    vis = re.sub(r"<(script|style|noscript)[^>]*>.*?</\1>", " ", body, flags=re.I | re.S)
    return t, h, strip(vis)


def _is_home(u: str) -> bool:
    """Site root, optionally behind a language / market prefix (/fr, /en-us ...), query ignored."""
    return bool(re.fullmatch(r"/?(?:[a-z]{2}(?:[-_][a-z]{2})?)?/?", urlsplit(u).path, re.I))


def norm_path(u):
    m = urlsplit(u)
    return m.path.rstrip("/") or "/"


def check_http(url: str, timeout=20):
    """Return dict(status, final, verdict, reason)."""
    import requests
    base = url.split("#")[0]
    last = None
    for attempt in range(2):
        try:
            r = session().get(base, timeout=timeout, allow_redirects=True, stream=True)
            body = r.raw.read(400_000, decode_content=True).decode(r.encoding or "utf-8", "ignore")
            r.close()
            break
        except requests.exceptions.SSLError as e:
            return {"status": 0, "final": base, "verdict": "broken", "reason": "tls: " + str(e)[:80]}
        except requests.exceptions.ConnectionError as e:
            msg = str(e)
            if re.search(r"Name or service not known|NameResolution|getaddrinfo|No address", msg):
                return {"status": 0, "final": base, "verdict": "broken", "reason": "dead domain (DNS)"}
            last = "connection: " + msg[:80]
        except requests.exceptions.RequestException as e:
            last = type(e).__name__
        time.sleep(1.5)
    else:
        return {"status": 0, "final": base, "verdict": "broken", "reason": last or "unreachable"}

    st, final = r.status_code, r.url
    title, h1, vis = page_text(body)
    out = {"status": st, "final": final, "title": title[:100]}
    if st in (404, 410):
        return {**out, "verdict": "broken", "reason": f"HTTP {st}"}
    if st in (403, 429, 503, 401, 202) or (st == 200 and CHALLENGE.search(body[:6000]) and len(vis) < 600):
        return {**out, "verdict": "blocked", "reason": f"HTTP {st} / challenge"}
    if st >= 500:
        return {**out, "verdict": "broken", "reason": f"HTTP {st}"}
    if st >= 400:
        return {**out, "verdict": "broken", "reason": f"HTTP {st}"}
    # soft 404 heuristics
    ob, fb = urlsplit(base), urlsplit(final)
    if not _is_home(base) and _is_home(final):
        return {**out, "verdict": "soft404", "reason": "redirects to the home page"}
    if SEARCHY.search(final) and not SEARCHY.search(base):
        return {**out, "verdict": "soft404", "reason": "redirects to a search page"}
    if re.search(r"/(404|not-?found|page-?introuvable|error)(/|\.|$)", fb.path, re.I):
        return {**out, "verdict": "soft404", "reason": "redirects to an error page"}
    if SOFT_TITLE.search(title) or SOFT_TITLE.search(h1[:120]):
        # "404" in a numeric part number title is fine: only flag when it reads like an error
        if re.search(r"(not\s+found|introuvable|n['’]existe\s+pas|does\s+not\s+exist|oops|no\s+longer|plus\s+disponible|discontinued|unavailable|^404\b|\b404\b\s*[-–—:|]|error\s*404)", title + " " + h1, re.I):
            return {**out, "verdict": "soft404", "reason": f"page says: {(h1 or title)[:70]}"}
    if len(vis) < 4000 and SOFT_BODY.search(vis):
        return {**out, "verdict": "soft404", "reason": "page text says not found / no products / unavailable"}
    out.update(verdict="ok", reason="", _body=body if len(body) < 400_000 else body[:400_000])
    return out


# ------------------------------------------------------------------ "useful result" checks

STOP = {"the", "and", "for", "with", "pour", "avec", "des", "les", "une", "mm", "in", "po", "x", "pack", "pcs",
        "unit", "each", "inch", "ft", "black", "noir", "sheet", "feuille"}


def tokens(s: str):
    return {t for t in re.findall(r"[a-z0-9]{3,}", unquote(s or "").lower()) if t not in STOP}


METALPROS = {"ver": "", "cat": None}
_mp_lock = threading.Lock()
MP_MATERIALS = ["ALUMINUM", "BRASS", "BRONZE", "CHROME", "COPPER", "GALVANIZED/ SATIN", "STAINLESS", "STEEL",
                "TOOL/ KNIFE MAKING"]


def _mp_norm(t: str) -> str:
    return re.sub(r"\s+", " ", htmlmod.unescape(t or "")).strip().lower()


def metalpros_catalogue():
    """Whole public catalogue (9 API calls), cached for the run. The quote tool's ?search= is a
    case-insensitive substring match on the item DESCRIPTION (never on the internal SKU)."""
    import requests
    with _mp_lock:
        if METALPROS["cat"] is not None:
            return METALPROS["cat"]
        try:
            r = requests.get("https://quote.metalpros.com/", headers=HEADERS, timeout=30)
            m = re.search(r'data-version=["\']([^"\']+)["\']', r.text)
            METALPROS["ver"] = m.group(1) if m else ""
        except requests.RequestException:
            pass
        cat, ok = [], True
        for mat in MP_MATERIALS:
            for attempt in range(3):
                try:
                    j = requests.get("https://quote.metalpros.com/api/materials/getdbmaterial",
                                     params={"material": mat, "v": METALPROS["ver"]}, headers=HEADERS, timeout=90).json()
                    cat += [(x["internalId"], _mp_norm(x["description"])) for x in j.get("results") or []]
                    break
                except Exception:
                    time.sleep(3)
            else:
                ok = False
        METALPROS["cat"] = cat if ok and cat else []
        return METALPROS["cat"]


def metalpros_search_ok(url: str):
    """Does quote.metalpros.com/?search=... show at least one product, and is it narrow enough to be THE item?"""
    q = _mp_norm(parse_qs(urlsplit(url).query).get("search", [""])[0])
    if not q:
        return "pointless", "Metal Pros page without a product search (empty catalogue)"
    cat = metalpros_catalogue()
    if not cat:
        return "blocked", "Metal Pros catalogue API unreachable"
    words = q.split()
    hits = [i for i, d in cat if all(w in d for w in words)]  # the server ANDs the words
    if not hits:
        return "pointless", "Metal Pros search shows 0 products"
    if len(hits) > 25:
        return "pointless", f"Metal Pros search too broad ({len(hits)} products, item not isolated)"
    return "ok", f"{len(hits)} product(s)"


def shopify_variant_ok(url: str, body: str):
    """?variant=ID must exist on the product (handle.js lists variants)."""
    import requests
    m = urlsplit(url)
    v = parse_qs(m.query).get("variant", [""])[0]
    if not v or "/products/" not in m.path:
        return None
    js = f"{m.scheme}://{m.netloc}{m.path.rstrip('/')}.js"
    try:
        r = requests.get(js, headers=HEADERS, timeout=25)
        if r.status_code in (404, 410):
            return "broken", "Shopify product removed (.js 404)"
        d = r.json()
    except Exception:
        return None
    ids = {str(x.get("id")) for x in d.get("variants", [])}
    if v not in ids:
        return "pointless", "variant id no longer exists on the product"
    return None


def _shopify_parts(url: str):
    m = urlsplit(url)
    mm = re.match(r"^((?:/[a-z]{2}(?:-[a-z]{2})?)?)/products/([^/?#]+)/?$", m.path)
    if not mm:
        return None
    return m, mm.group(1), mm.group(2)


def shopify_confirm(url: str):
    """Authoritative check for a Shopify product URL: <handle>.js is JSON when the product exists
    (404 when removed). Returns (verdict, reason) or None when it cannot tell (429 etc.)."""
    import requests
    sp = _shopify_parts(url)
    if not sp:
        return None
    m, lang, handle = sp
    try:
        r = requests.get(f"{m.scheme}://{m.netloc}{lang}/products/{handle}.js", headers=HEADERS, timeout=25)
    except requests.RequestException:
        return None
    if r.status_code in (404, 410):
        return "broken", "Shopify product removed (.js 404)"
    if r.status_code != 200:
        return None
    try:
        d = r.json()
    except ValueError:
        return None
    v = parse_qs(m.query).get("variant", [""])[0]
    if v and v not in {str(x.get("id")) for x in d.get("variants", [])}:
        return "pointless", "variant id no longer exists on the product"
    return "ok", "product exists (.js)"


def shopify_feed(host: str, max_pages=150):
    """{handle: set(variant ids)} from the public /products.json feed (1 request / 0.6 s)."""
    import requests
    out = {}
    for page in range(1, max_pages + 1):
        for attempt in range(4):
            try:
                r = requests.get(f"https://{host}/products.json", params={"limit": 250, "page": page},
                                 headers=HEADERS, timeout=120)
                if r.status_code == 200:
                    prods = r.json().get("products", [])
                    break
                time.sleep(5 * (attempt + 1))
            except Exception:
                time.sleep(5)
        else:
            return out or None
        if not prods:
            break
        for p in prods:
            out[p["handle"]] = {str(v["id"]) for v in p.get("variants", [])}
        time.sleep(0.6)
    return out


def name_match(names, title, h1, vis):
    """Weak signal for 'this page is not the item': the item's part numbers / sizes (tokens that
    contain a digit, 4+ chars) must appear on the page. Words are ignored (FR/EN pages differ)."""
    if not names:
        return None
    want = set()
    for n in names:
        want |= {t for t in tokens(n) if re.search(r"\d", t) and len(t) >= 4 and re.search(r"[a-z]", t) or re.fullmatch(r"\d{5,}", t)}
    if not want:
        return None
    have = tokens(title + " " + h1 + " " + vis[:40000])
    if not (want & have):
        return f"page shows none of: {', '.join(sorted(want)[:6])}"
    return None


# --------------------------------------------------------------------------- rendering

def _render_chunk(items):
    """items: list of (base_url, fragments, names, mode); mode in {'blocked','search'}.
    Returns ({base_url: (verdict, reason)}, {full_url_with_fragment: reason})."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("playwright not installed: skipping rendered checks", file=sys.stderr)
        return {}, {}
    res, frag_bad = {}, {}
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=["--disable-blink-features=AutomationControlled"])
        for url, frags, names, mode in items:
            time.sleep(0.3)
            # a fresh context per page: bot walls (Cloudflare) challenge a context after a few quick pages
            ctx = br.new_context(user_agent=UA, locale="en-CA", viewport={"width": 1366, "height": 800})
            pg = ctx.new_page()
            try:
                r = pg.goto(url, wait_until="domcontentloaded", timeout=40000)
                pg.wait_for_timeout(2000)
                st = r.status if r else 0
                body = pg.inner_text("body")
                title = pg.title()
            except Exception as e:
                res[url] = ("blocked" if mode == "blocked" else "broken", f"browser: {type(e).__name__}")
                ctx.close()
                continue
            if st in (404, 410):
                res[url] = ("broken", f"HTTP {st} (browser)")
            elif st in (403, 429) or (CHALLENGE.search(body[:3000]) and len(body) < 600):
                res[url] = ("blocked", f"still blocked in browser (HTTP {st})")
            elif (SOFT_BODY.search(body[:3000]) and len(body) < 4000) or (
                    SOFT_TITLE.search(title) and re.search(r"not\s+found|introuvable|404", title, re.I)):
                res[url] = ("soft404", f"browser: {title[:60]}")
            elif mode in ("search", "product"):
                nm = name_match(names, title, "", body)
                res[url] = ("pointless", "rendered page shows no matching product: " + nm) if nm else ("ok", "")
            else:
                res[url] = ("ok", "browser OK")
            if res[url][0] == "ok":
                for fr in frags:  # "#1511" must be a product row that exists on the rendered page
                    if re.fullmatch(r"[A-Za-z0-9_\-]+", fr) and not pg.query_selector(f'[id="{fr}"]'):
                        frag_bad[url + "#" + fr] = f"item #{fr} is no longer on the page"
            ctx.close()
        br.close()
    return res, frag_bad


def render_checks(items, workers=4):
    """Render in parallel browsers (one per worker); items are spread by host so one host is not hammered."""
    if not items:
        return {}, {}
    items = sorted(items, key=lambda it: urlsplit(it[0]).netloc)
    chunks = [items[i::workers] for i in range(workers)]
    res, fb = {}, {}
    with cf.ThreadPoolExecutor(max_workers=workers) as ex:
        for r, f in ex.map(_render_chunk, [c for c in chunks if c]):
            res.update(r)
            fb.update(f)
    return res, fb


# --------------------------------------------------------------------------- internal links

def internal_check(root: Path):
    bad = collections.defaultdict(set)

    def exists(p):
        p = p.split("#")[0].split("?")[0]
        if not p or p == "/":
            return (root / "index.html").exists()
        f = root / p.lstrip("/")
        return f.is_file() or (f.is_dir() and (f / "index.html").exists()) or (root / (p.lstrip("/") + ".html")).exists()

    for f in root.rglob("*.html"):
        if any(x in f.parts for x in ("node_modules", ".git")):
            continue
        t = f.read_text(errors="ignore")
        for h in re.findall(r'(?:href|src)="(/[^"]*)"', t):
            if h.startswith("//") or h.startswith("/api/") or h.startswith("/_vercel"):
                continue
            if not exists(h):
                bad[h].add(f.relative_to(root).as_posix())
    return bad


# --------------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--all", action="store_true", help="check reference links too (spec sources, guides, directory)")
    ap.add_argument("--render", action="store_true", help="render search URLs and blocked pages with Playwright")
    ap.add_argument("--browser", action="store_true", help="alias of --render")
    ap.add_argument("--sample", type=int, default=6, help="with --render: product pages rendered per seller to confirm they show the item")
    ap.add_argument("--confirm-limit", type=int, default=2500, help="max failing pages re-opened in the browser")
    ap.add_argument("--internal", action="store_true", help="also check internal links exist in the build")
    ap.add_argument("--only-new", "--resume", action="store_true", help="reuse the cache: skip URLs checked < 7 days ago (also resumes an interrupted run)")
    ap.add_argument("--strict", action="store_true", help="reference links failing also fails the run")
    ap.add_argument("--host", help="only URLs whose host contains this text")
    ap.add_argument("--limit", type=int, default=0, help="debug: only the first N URLs")
    ap.add_argument("--workers", type=int, default=150)
    ap.add_argument("--per-host", type=int, default=6, help="max concurrent requests per host")
    ap.add_argument("--cache", default=str(ROOT / ".link-cache.json"))
    ap.add_argument("--baseline", default=str(ROOT / "scripts" / "link_baseline.json"))
    ap.add_argument("--json", help="write the full report as JSON")
    ap.add_argument("--root", default=str(ROOT))
    a = ap.parse_args()
    a.render = a.render or a.browser
    root = Path(a.root)

    found = collect(root)
    urls = {u: e for u, e in found.items() if (a.all or e["kind"] == "buy")
            and (not a.host or a.host in (urlsplit(u).hostname or ""))}
    # fetch each URL once (fragments only matter to the browser)
    groups: dict[str, list[str]] = collections.defaultdict(list)
    for u in urls:
        groups[u.split("#")[0]].append(u)
    todo = sorted(groups)
    import random
    random.Random(7).shuffle(todo)  # spread hosts so per-host limits do not serialise the run
    if a.limit:
        todo = todo[: a.limit]
    print(f"{len(urls)} outbound links ({sum(e['kind']=='buy' for e in urls.values())} buy), "
          f"{len(todo)} unique pages to GET", file=sys.stderr)

    cache = {}
    cp = Path(a.cache)
    if a.only_new and cp.exists():
        cache = json.loads(cp.read_text())
    now = time.time()
    results: dict[str, dict] = {}
    host_sem: dict[str, threading.Semaphore] = collections.defaultdict(lambda: threading.Semaphore(a.per_host))
    lock = threading.Lock()

    def work(u):
        c = cache.get(u)
        if c and now - c.get("t", 0) < 7 * 86400 and c.get("verdict") == "ok":
            return u, c
        host = urlsplit(u).netloc
        first = groups[u][0]
        if host == "quote.metalpros.com" and "search" in urlsplit(u).query:
            v, why = metalpros_search_ok(u)
            r = {"status": 200, "final": u, "verdict": v, "reason": why}
        elif host == "quote.metalpros.com" and urlsplit(u).path.strip("/") == "":
            r = {"status": 200, "final": u, "verdict": "pointless", "reason": "Metal Pros catalogue home page (nothing selected)"}
        else:
            r = check_http(u)
            body = r.pop("_body", None)
            if r["verdict"] in ("blocked", "soft404", "broken") and _shopify_parts(u):
                sc = shopify_confirm(u)
                if sc:  # .js is authoritative: a product page that "says" not found may just be a hidden template
                    r["verdict"], r["reason"] = sc
            if r["verdict"] == "ok":
                if "variant=" in u:
                    sv = shopify_variant_ok(u, body or "")
                    if sv:
                        r["verdict"], r["reason"] = sv
                p = urlsplit(u)
                if r["verdict"] == "ok" and urls[first]["kind"] == "buy" and (p.path.strip("/") == "") and not p.query:
                    r["verdict"], r["reason"] = "pointless", "generic home page behind a buy link"
                if r["verdict"] == "ok" and urls[first]["kind"] == "buy" and body and SEARCHY.search(u):
                    t, h, vis = page_text(body)
                    nm = name_match(urls[first]["names"], t, h, vis)
                    if nm:
                        r["verdict"], r["reason"] = "pointless", "search page, " + nm
        r["t"] = now
        return u, r

    # Scheduler: every host gets at most --per-host requests in flight, all hosts run in parallel.
    pending: dict[str, collections.deque] = collections.defaultdict(collections.deque)
    for u in todo:
        pending[urlsplit(u).netloc].append(u)
    active: collections.Counter = collections.Counter()
    cond = threading.Condition()
    state = {"done": 0}

    def worker():
        while True:
            with cond:
                while True:
                    if not any(pending.values()):
                        return
                    pick = next((h for h, q in pending.items() if q and active[h] < a.per_host), None)
                    if pick:
                        break
                    cond.wait(1.0)
                u = pending[pick].popleft()
                active[pick] += 1
            try:
                _, r = work(u)
            except Exception as e:  # never lose the whole run on one odd URL
                r = {"status": 0, "final": u, "verdict": "broken", "reason": f"checker error {type(e).__name__}", "t": now}
            with cond:
                results[u] = r
                active[pick] -= 1
                state["done"] += 1
                if state["done"] % 1000 == 0:
                    print(f"  {state['done']}/{len(todo)}", file=sys.stderr, flush=True)
                    try:  # checkpoint so an interrupted run can --resume
                        cp.write_text(json.dumps({**cache, **results}))
                    except OSError:
                        pass
                cond.notify_all()

    threads = [threading.Thread(target=worker, daemon=True) for _ in range(a.workers)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # retry blocked pages in a headless browser; render search-style pages to confirm a product shows
    frag_bad: dict[str, str] = {}

    def frags_of(base):
        return sorted({g.split("#", 1)[1] for g in groups[base] if "#" in g})

    # rate-limited Shopify hosts: verify against the public product feed instead of hammering product pages
    by_host = collections.defaultdict(list)
    for u, r in results.items():
        if r["verdict"] == "blocked" and _shopify_parts(u):
            by_host[urlsplit(u).netloc].append(u)
    for host, us in by_host.items():
        print(f"feed check {host}: {len(us)} product URLs", file=sys.stderr, flush=True)
        feed = shopify_feed(host)
        if not feed:
            continue
        for u in us:
            m, lang, handle = _shopify_parts(u)
            if handle not in feed:
                sc = shopify_confirm(u)
                if sc and sc[0] != "ok":
                    results[u].update(verdict=sc[0], reason="not in the shop's product feed; " + sc[1])
                elif sc:
                    results[u].update(verdict="ok", reason="exists (.js)")
                continue
            v = parse_qs(m.query).get("variant", [""])[0]
            if v and v not in feed[handle]:
                results[u].update(verdict="pointless", reason="variant id no longer exists on the product")
            else:
                results[u].update(verdict="ok", reason="in product feed")

    # Bot walls sometimes answer plain GETs with a fake 404: every "broken"/"soft404" is re-opened in a
    # real browser before it is reported (dead domains and TLS errors excepted).
    blocked = [u for u, r in results.items() if r["verdict"] == "blocked" or
               (r["verdict"] in ("broken", "soft404") and not r["reason"].startswith(("dead domain", "tls")))]
    blocked = blocked[: a.confirm_limit]
    if a.render:  # "#1511"-style anchors (Metals Depot product rows) must exist on the rendered page
        have = set(blocked)
        blocked += [u for u in results if u not in have and frags_of(u) and results[u]["verdict"] == "ok"
                    and urls[groups[u][0]]["kind"] == "buy"]
    if a.render and blocked:
        print(f"re-checking {len(blocked)} blocked / failing pages in a browser", file=sys.stderr)
        rr, fb = render_checks([(u, frags_of(u), urls[groups[u][0]]["names"], "blocked") for u in blocked])
        frag_bad.update(fb)
        for u, (v, why) in rr.items():
            results[u].update(verdict=v, reason=why)
    if a.render:
        by_host = collections.defaultdict(list)
        for u, r in results.items():
            e = urls[groups[u][0]]
            if e["kind"] == "buy" and r["verdict"] == "ok" and SEARCHY.search(u):
                by_host[urlsplit(u).netloc].append(u)
        items = [(u, [], urls[groups[u][0]]["names"], "search") for us in by_host.values() for u in us[:40]]
        # product pages: a random sample per seller is rendered and must show the item's part number / size
        import random
        per = collections.defaultdict(list)
        for u, r in results.items():
            e = urls[groups[u][0]]
            if e["kind"] == "buy" and r["verdict"] == "ok" and e["names"] and not SEARCHY.search(u):
                per[urlsplit(u).netloc].append(u)
        for h, us in per.items():
            items += [(u, [], urls[groups[u][0]]["names"], "product") for u in random.Random(1).sample(us, min(a.sample, len(us)))]
        if items:
            rr, _ = render_checks(items)
            for u, (v, why) in rr.items():
                if v != "ok":
                    results[u].update(verdict=v, reason=why)

    cp.write_text(json.dumps({**cache, **results}))
    # ---- report
    try:
        baseline = set(json.loads(Path(a.baseline).read_text()).get("known", {}))
    except (OSError, ValueError):
        baseline = set()
    bad = {u: r for u, r in results.items() if r["verdict"] in ("broken", "soft404", "pointless")}
    for full, why in frag_bad.items():
        base = full.split("#")[0]
        results.setdefault(base, {"verdict": "ok", "reason": ""})
        bad.setdefault(full, {"verdict": "pointless", "reason": why, "status": 200, "final": base})
        groups.setdefault(full, [full])
    counts = collections.Counter(r["verdict"] for r in results.values())
    new_buy, new_ref = [], []
    rep = []
    for u, r in sorted(bad.items()):
        for full in groups[u]:
            e = urls[full]
            line = {"url": full, "kind": e["kind"], "verdict": r["verdict"], "reason": r["reason"],
                    "status": r.get("status"), "final": r.get("final"), "files": sorted(e["files"]), "names": e["names"]}
            rep.append(line)
            known = full in baseline or u in baseline
            if not known:
                (new_buy if e["kind"] == "buy" else new_ref).append(line)
    print(f"\nChecked {len(results)} unique pages ({len(urls)} links): " +
          ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    for title, lst in (("BROKEN / SOFT-404 / POINTLESS buy links", new_buy), ("reference links failing", new_ref)):
        print(f"\n== {title}: {len(lst)}")
        for l in lst[:200]:
            print(f"  [{l['verdict']}] {l['url']}\n      {l['reason']}  <- {', '.join(l['files'])}  {('· ' + l['names'][0][:60]) if l['names'] else ''}")
        if len(lst) > 200:
            print(f"  ... {len(lst) - 200} more (use --json)")
    if a.internal:
        ib = internal_check(root)
        print(f"\n== broken internal links: {len(ib)}")
        for h, fs in sorted(ib.items())[:50]:
            print(f"  {h} <- {sorted(fs)[:2]}")
    if a.json:
        Path(a.json).write_text(json.dumps({"counts": counts, "bad": rep}, indent=1, default=list, ensure_ascii=False))
    fail = bool(new_buy) or (a.strict and bool(new_ref)) or (a.internal and bool(ib))
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()

"""Mobile app shell (PWA) for phones: bottom tab bar, « Plus » sheet, install prompt,
web app manifests, service worker and FR/EN offline pages.

Desktop is untouched: every visual rule lives in css/app.css under the phone media query
(see APP_MQ), and the markup added here is display:none outside it.
"""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

from .taxonomy import T, PATHS

ROOT = Path(__file__).resolve().parent.parent
INK = "#15191c"
BG = "#f6f5f1"
# Phones: portrait up to 768px, and landscape phones (short and not desktop-wide). Keep in sync with css/app.css + js/app.js.
APP_MQ = "(max-width: 768px), (orientation: landscape) and (max-height: 520px) and (max-width: 1023px)"

_P = 'fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"'
ICONS = {
    "home": f'<path {_P} d="M3.5 10.2 12 3.5l8.5 6.7V19a1.5 1.5 0 0 1-1.5 1.5h-4.2v-5.8H9.2v5.8H5A1.5 1.5 0 0 1 3.5 19z"/>',
    "suppliers": f'<path {_P} d="M3 20.5V8.6L12 3.5l9 5.1v11.9"/><path {_P} d="M7 20.5v-7.3h10v7.3M7 16.8h10"/>',
    "prices": f'<path {_P} d="M20.3 13.3 13.3 20.3a1.8 1.8 0 0 1-2.5 0L3.5 13V3.5H13l7.3 7.3a1.8 1.8 0 0 1 0 2.5z"/><circle cx="8" cy="8" r="1.6" fill="currentColor"/>',
    "tools": f'<path {_P} d="M14.6 6.4a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.6-3.6a6 6 0 0 1-7.9 7.9l-6.6 6.6a2.1 2.1 0 0 1-3-3l6.6-6.6a6 6 0 0 1 7.9-7.9z"/>',
    "more": '<rect x="4" y="4" width="6.5" height="6.5" rx="1.8" fill="none" stroke="currentColor" stroke-width="1.9"/><rect x="13.5" y="4" width="6.5" height="6.5" rx="1.8" fill="none" stroke="currentColor" stroke-width="1.9"/><rect x="4" y="13.5" width="6.5" height="6.5" rx="1.8" fill="none" stroke="currentColor" stroke-width="1.9"/><rect x="13.5" y="13.5" width="6.5" height="6.5" rx="1.8" fill="none" stroke="currentColor" stroke-width="1.9"/>',
    "guides": f'<path {_P} d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5zM4 20.5A2.5 2.5 0 0 0 6.5 23H20v-5"/>',
    "used": f'<path {_P} d="M3 7h11v9H3zM14 10h4l3 3v3h-7"/><circle {_P} cx="7" cy="18" r="2"/><circle {_P} cx="17.5" cy="18" r="2"/>',
    "parts": f'<circle {_P} cx="12" cy="12" r="3"/><path {_P} d="M12 2.8v2.6M12 18.6v2.6M21.2 12h-2.6M5.4 12H2.8M18.5 5.5l-1.8 1.8M7.3 16.7l-1.8 1.8M18.5 18.5l-1.8-1.8M7.3 7.3 5.5 5.5"/>',
    "tooling": f'<path {_P} d="M9 3h6v4l-1.5 2v11.5L12 22l-1.5-1.5V9L9 7zM10.5 13h3M10.5 16.5h3"/>',
    "news": f'<path {_P} d="M4 4.5h13v15H6a2 2 0 0 1-2-2zM17 8.5h3v9a2 2 0 0 1-2 2M7.5 8h6M7.5 11.5h6M7.5 15h4"/>',
    "codes": f'<path {_P} d="M12 3.5 21.5 20h-19zM12 10v4.5"/><circle cx="12" cy="17.2" r="1.1" fill="currentColor"/>',
    "coolant": f'<path {_P} d="M12 3.2s6 6.6 6 11a6 6 0 0 1-12 0c0-4.4 6-11 6-11z"/>',
    "add": f'<circle {_P} cx="12" cy="12" r="8.5"/><path {_P} d="M12 8v8M8 12h8"/>',
    "announce": f'<path {_P} d="M4 10v4h3l6 4V6l-6 4zM16.5 9a4 4 0 0 1 0 6M19 6.5a7.5 7.5 0 0 1 0 11"/>',
    "about": f'<circle {_P} cx="12" cy="12" r="8.5"/><path {_P} d="M12 11v5.5"/><circle cx="12" cy="7.8" r="1.1" fill="currentColor"/>',
    "mail": f'<rect {_P} x="3" y="5" width="18" height="14" rx="2.5"/><path {_P} d="m4 7 8 6 8-6"/>',
    "install": f'<path {_P} d="M12 3.5v11M7.5 10.5 12 15l4.5-4.5M4.5 16.5v2A2 2 0 0 0 6.5 20.5h11a2 2 0 0 0 2-2v-2"/>',
    "share": f'<path {_P} d="M12 15V3.5M8 7.5l4-4 4 4M6 10.5H5a1.5 1.5 0 0 0-1.5 1.5v7A1.5 1.5 0 0 0 5 20.5h14a1.5 1.5 0 0 0 1.5-1.5v-7A1.5 1.5 0 0 0 19 10.5h-1"/>',
    "plusbox": f'<rect {_P} x="3.5" y="3.5" width="17" height="17" rx="3.5"/><path {_P} d="M12 8v8M8 12h8"/>',
    "close": f'<path {_P} d="M6 6l12 12M18 6 6 18"/>',
    "search": f'<circle {_P} cx="11" cy="11" r="7"/><path {_P} d="m20 20-3.6-3.6"/>',
}


def icon(name: str, cls: str = "cf-ico") -> str:
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true" focusable="false">{ICONS[name]}</svg>'


def head_tags(lang: str) -> str:
    """Extra <head> tags for the installable app (manifest per language, iOS meta, icons)."""
    fr = lang == "fr"
    manifest = "/manifest.webmanifest" if fr else "/en/manifest.webmanifest"
    return f"""<link rel="manifest" href="{manifest}">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="CoupeFab">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="application-name" content="CoupeFab">
<meta name="format-detection" content="telephone=no">
<link rel="icon" type="image/png" sizes="192x192" href="/icons/icon-192.png">
<script type="speculationrules">{{"prefetch":[{{"where":{{"and":[{{"href_matches":"/*"}},{{"not":{{"href_matches":["/api/*","/admin/*","/*.json","/*.csv"]}}}}]}},"eagerness":"moderate"}}]}}</script>"""


def _tab(href, name, label, active, extra=""):
    cur = ' aria-current="page"' if active else ""
    return f'<a class="cf-tab" href="{href}"{cur}{extra}>{icon(name)}<span class="cf-tab-l">{label}</span></a>'


def shell(lang: str, path: str, fr_href: str, en_href: str) -> str:
    """Bottom tab bar + « Plus » sheet + install banner + iOS instructions (phones only)."""
    fr = lang == "fr"
    t, p = T[lang], PATHS[lang]
    tools_paths = ("/outils/", "/en/tools/")
    is_home = path == p["home"]
    is_sup = path.startswith(p["suppliers"])
    is_px = path.startswith(p["prices"])
    is_tools = path.startswith(tools_paths)
    is_more = not (is_home or is_sup or is_px or is_tools)
    tabs = "".join([
        _tab(p["home"], "home", t["home"], is_home),
        _tab(p["suppliers"], "suppliers", "Fournisseurs" if fr else "Suppliers", is_sup),
        _tab(p["prices"], "prices", t["prices_nav"], is_px),
        _tab(p["tools"], "tools", t["tools"], is_tools),
    ])
    more_label = "Plus" if fr else "More"
    more_cur = ' data-active="1"' if is_more else ""
    tabs += (f'<button class="cf-tab cf-tab-more" type="button" aria-haspopup="dialog" aria-expanded="false" '
             f'aria-controls="cf-sheet"{more_cur}>{icon("more")}<span class="cf-tab-l">{more_label}</span></button>')

    def tile(href, name, label, sub=""):
        cur = ' aria-current="page"' if path.startswith(href) and href not in ("/", "/en/") else ""
        sub_html = f'<small>{sub}</small>' if sub else ""
        return f'<li><a class="cf-tile" href="{href}"{cur}>{icon(name, "cf-ico cf-tile-ico")}<span>{label}{sub_html}</span></a></li>'

    coolant = "/outils/calculateur-liquide-de-coupe/" if fr else "/en/tools/coolant-calculator/"
    codes = "/codes-erreur/" if fr else "/en/error-codes/"
    tiles = "".join([
        tile(p["guides"], "guides", t["guides"], "CAO/FAO, plasma, laser" if fr else "CAD/CAM, plasma, laser"),
        tile(p["used"], "used", "Occasions" if fr else "Used equipment", "Machines au Québec" if fr else "Machines in Quebec"),
        tile(p["parts"], "parts", t["parts"], "Consommables, pièces" if fr else "Consumables, spares"),
        tile(p["tooling"], "tooling", t["tooling"], "Fraises, forets, inserts" if fr else "End mills, drills, inserts"),
        tile(p["headlines"], "news", t["headlines"], "CNC dans le monde" if fr else "CNC around the world"),
        tile(codes, "codes", "Codes d’erreur" if fr else "Error codes", "Alarmes Fanuc, Haas…" if fr else "Fanuc, Haas alarms…"),
        tile(coolant, "coolant", "Liquide de coupe" if fr else "Coolant calculator", "Calculateur" if fr else "Mix and refractometer"),
        tile(p["announce"], "announce", t["announce"], "Visibilité fournisseurs" if fr else "Supplier visibility"),
        tile(p["about"], "about", t["about"], "Contact" if fr else "Contact"),
    ])
    tiles += (f'<li><button class="cf-tile" type="button" data-search-open data-cf-close>{icon("search", "cf-ico cf-tile-ico")}'
              f'<span>{t["search"]}<small>{"Guides et machines" if fr else "Guides and machines"}</small></span></button></li>')
    news_cur = ' aria-current="page"' if path.startswith(p["news"]) else ""
    sheet_title = "Plus" if fr else "More"
    close = t["close"]
    install_l = "Installer l’app" if fr else "Install the app"
    install_s = "Plein écran, depuis l’écran d’accueil" if fr else "Full screen, from your home screen"
    return f"""
<nav class="cf-tabbar" aria-label="{'Navigation de l’app' if fr else 'App navigation'}">{tabs}</nav>
<div class="cf-sheet" id="cf-sheet" hidden>
  <div class="cf-sheet-scrim" data-cf-close></div>
  <div class="cf-sheet-panel" role="dialog" aria-modal="true" aria-labelledby="cf-sheet-h" tabindex="-1">
    <div class="cf-grab" data-cf-close aria-hidden="true"><span></span></div>
    <div class="cf-sheet-head">
      <h2 id="cf-sheet-h">{sheet_title}</h2>
      <button class="cf-x" type="button" data-cf-close aria-label="{close}">{icon("close")}</button>
    </div>
    <a class="cf-cta" href="{p['add_prices']}">{icon("add", "cf-ico")}<span><b>{t['add_prices']}</b><small>{'Fournisseurs : publiez vos prix gratuitement' if fr else 'Suppliers: list your prices for free'}</small></span></a>
    <ul class="cf-tiles">{tiles}</ul>
    <a class="cf-news" href="{p['news']}"{news_cur}>{icon("mail", "cf-ico")}<span><b>{t['news']}</b><small>{esc_(t['news_d'])}</small></span><i aria-hidden="true">→</i></a>
    <div class="cf-sheet-foot">
      <div class="cf-lang" role="group" aria-label="{t['lang']}"><a href="{fr_href}" hreflang="fr-CA" lang="fr-CA"{' aria-current="true"' if fr else ''}>Français</a><a href="{en_href}" hreflang="en-CA" lang="en-CA"{' aria-current="true"' if not fr else ''}>English</a></div>
      <button class="cf-install-btn" type="button" data-cf-install hidden>{icon("install")}<span>{install_l}</span></button>
    </div>
  </div>
</div>
<div class="cf-install" id="cf-install" hidden role="region" aria-label="{install_l}">
  <img src="/icons/icon-192.png" alt="" width="40" height="40">
  <p><b>{install_l}</b><span>{install_s}</span></p>
  <button class="cf-install-go" type="button" data-cf-install>{'Installer' if fr else 'Install'}</button>
  <button class="cf-x" type="button" data-cf-dismiss aria-label="{'Plus tard' if fr else 'Not now'}">{icon("close")}</button>
</div>
<div class="cf-sheet cf-ios" id="cf-ios" hidden>
  <div class="cf-sheet-scrim" data-cf-close></div>
  <div class="cf-sheet-panel" role="dialog" aria-modal="true" aria-labelledby="cf-ios-h" tabindex="-1">
    <div class="cf-grab" data-cf-close aria-hidden="true"><span></span></div>
    <div class="cf-sheet-head"><h2 id="cf-ios-h">{'Ajouter CoupeFab à l’écran d’accueil' if fr else 'Add CoupeFab to your Home Screen'}</h2>
      <button class="cf-x" type="button" data-cf-close aria-label="{close}">{icon("close")}</button></div>
    <ol class="cf-steps">
      <li>{icon("share")}<span>{'Touchez <b>Partager</b> dans la barre de Safari.' if fr else 'Tap <b>Share</b> in the Safari toolbar.'}</span></li>
      <li>{icon("plusbox")}<span>{'Choisissez <b>Sur l’écran d’accueil</b>.' if fr else 'Choose <b>Add to Home Screen</b>.'}</span></li>
      <li><img src="/icons/icon-192.png" alt="" width="24" height="24"><span>{'Touchez <b>Ajouter</b> : CoupeFab s’ouvre ensuite en plein écran, comme une app.' if fr else 'Tap <b>Add</b>: CoupeFab then opens full screen, like an app.'}</span></li>
    </ol>
  </div>
</div>
<div class="cf-navbar" aria-hidden="true"></div>"""


def esc_(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def _manifest(lang: str) -> dict:
    fr = lang == "fr"
    p = PATHS[lang]
    return {
        "id": "/" if fr else "/en/",
        "name": "CoupeFab — découpe CNC et métal au Québec" if fr else "CoupeFab — CNC cutting and metal in Quebec",
        "short_name": "CoupeFab",
        "description": ("Prix des métaux, fournisseurs, occasions et guides CNC, plasma, laser et tôlerie, en français d’abord."
                        if fr else "Metal prices, suppliers, used equipment and CNC, plasma, laser and sheet-metal guides."),
        "lang": "fr-CA" if fr else "en-CA",
        "dir": "ltr",
        "start_url": ("/?source=pwa" if fr else "/en/?source=pwa"),
        "scope": "/",
        "display": "standalone",
        "display_override": ["standalone", "minimal-ui"],
        "orientation": "any",
        "background_color": BG,
        "theme_color": INK,
        "categories": ["business", "productivity", "utilities"],
        "icons": [
            {"src": "/icons/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
            {"src": "/icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
            {"src": "/icons/maskable-192.png", "sizes": "192x192", "type": "image/png", "purpose": "maskable"},
            {"src": "/icons/maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
        ],
        "shortcuts": [
            {"name": T[lang]["prices_nav"], "url": p["prices"] + "?source=pwa", "icons": [{"src": "/icons/icon-192.png", "sizes": "192x192"}]},
            {"name": "Fournisseurs" if fr else "Suppliers", "url": p["suppliers"] + "?source=pwa", "icons": [{"src": "/icons/icon-192.png", "sizes": "192x192"}]},
            {"name": "Occasions" if fr else "Used equipment", "url": p["used"] + "?source=pwa", "icons": [{"src": "/icons/icon-192.png", "sizes": "192x192"}]},
            {"name": T[lang]["tools"], "url": p["tools"] + "?source=pwa", "icons": [{"src": "/icons/icon-192.png", "sizes": "192x192"}]},
        ],
    }


OFFLINE = {"fr": "/hors-ligne/", "en": "/en/offline/"}


def _offline_body(lang: str) -> str:
    fr = lang == "fr"
    p = PATHS[lang]
    return f"""
<section class="page cf-offline">
  <div class="cf-offline-ico" aria-hidden="true"><svg viewBox="0 0 24 24" class="cf-ico"><path fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" d="M2.5 8.5a14 14 0 0 1 19 0M5.5 12a9.5 9.5 0 0 1 13 0M8.6 15.4a5 5 0 0 1 6.8 0M3 3l18 18"/><circle cx="12" cy="19" r="1.3" fill="currentColor"/></svg></div>
  <h1>{'Vous êtes hors ligne' if fr else 'You’re offline'}</h1>
  <p class="lede">{'Pas de connexion pour le moment. Les pages déjà ouvertes restent consultables ; les prix et annonces se mettront à jour dès le retour du réseau.' if fr else 'No connection right now. Pages you already opened stay available; prices and listings refresh as soon as you are back online.'}</p>
  <p class="nf-actions"><button class="btn" type="button" onclick="location.reload()">{'Réessayer' if fr else 'Try again'}</button><a class="btn-ghost" href="{p['home']}">{T[lang]['home']}</a></p>
</section>"""


def _sw_source(version: str, precache: list[str]) -> str:
    return SW_TEMPLATE.replace("__VERSION__", version).replace("__PRECACHE__", json.dumps(precache))


def write_assets(layout, asset_v: str) -> str:
    """Write manifests, offline pages and /sw.js. Returns the service-worker version."""
    for lang in ("fr", "en"):
        m = json.dumps(_manifest(lang), ensure_ascii=False, indent=1) + "\n"
        dest = ROOT / ("manifest.webmanifest" if lang == "fr" else "en/manifest.webmanifest")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(m, encoding="utf-8")
        if lang == "fr":
            (ROOT / "site.webmanifest").write_text(m, encoding="utf-8")  # legacy URL, same content
        path = OFFLINE[lang]
        html = layout(lang=lang, title=("Hors ligne — CoupeFab" if lang == "fr" else "Offline — CoupeFab"),
                      description=("Vous êtes hors ligne." if lang == "fr" else "You are offline."),
                      path=path, alt=OFFLINE["en" if lang == "fr" else "fr"], body=_offline_body(lang), noindex=True)
        out = ROOT / path.strip("/") / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding="utf-8")
    shell_assets = [f"/css/{n}.css?v={asset_v}" for n in ("style", "site", "ux", "app")]
    shell_assets += [f"/js/{n}.js?v={asset_v}" for n in ("pager", "hot-news", "site", "app")]
    shell_assets += ["/fonts/plex-sans.woff2", "/favicon.svg", "/icons/icon-192.png", OFFLINE["fr"], OFFLINE["en"]]
    h = hashlib.sha1(asset_v.encode())
    for rel in sorted([*(ROOT / "css").glob("*.css"), *(ROOT / "js").glob("*.js")]):
        h.update(rel.read_bytes())
    # one version per build: a deploy always ships a new worker, which drops the previous caches
    version = time.strftime("%Y%m%d%H%M") + "-" + h.hexdigest()[:8]
    (ROOT / "sw.js").write_text(_sw_source(version, shell_assets), encoding="utf-8")
    return version


SW_TEMPLATE = r"""/* CoupeFab service worker (generated by sitekit/app.py, do not edit by hand).
 * Version __VERSION__. Each build ships a new version; activating it deletes every older cache.
 * Pages: stale-while-revalidate, but a cached page older than PAGE_MAX_AGE is never served while
 * the network answers (network-first with a short timeout, then the cached copy, then offline page).
 * Versioned assets (?v=): cache-first. Data (JSON/CSV): network-first. /api, /admin, /_vercel: never cached.
 */
const VERSION = "__VERSION__";
const SHELL = "cf-shell-" + VERSION;
const PAGES = "cf-pages-" + VERSION;
const ASSETS = "cf-assets-" + VERSION;
const PRECACHE = __PRECACHE__;
const PAGE_MAX_AGE = 30 * 60 * 1000;   // 30 min: older cached HTML is revalidated before use
const PAGE_LIMIT = 40, ASSET_LIMIT = 120;
const NET_TIMEOUT = 3500;

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(SHELL).then((c) => c.addAll(PRECACHE)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (e) => {
  e.waitUntil((async () => {
    const keep = [SHELL, PAGES, ASSETS];
    for (const k of await caches.keys()) if (!keep.includes(k)) await caches.delete(k);
    if (self.registration.navigationPreload) { try { await self.registration.navigationPreload.enable(); } catch (_) {} }
    await self.clients.claim();
  })());
});

self.addEventListener("message", (e) => { if (e.data === "skipWaiting") self.skipWaiting(); });

function bypass(url, req) {
  return req.method !== "GET" || url.origin !== self.location.origin ||
    /^\/(api|admin|_vercel)(\/|$)/.test(url.pathname) || url.pathname === "/sw.js";
}

async function trim(name, max) {
  const c = await caches.open(name); const keys = await c.keys();
  for (let i = 0; i < keys.length - max; i++) await c.delete(keys[i]);
}

function stamp(res) {
  const h = new Headers(res.headers); h.set("x-cf-cached", String(Date.now()));
  return res.blob().then((b) => new Response(b, { status: res.status, statusText: res.statusText, headers: h }));
}

function pageKey(url) { const u = new URL(url); u.search = ""; u.hash = ""; return u.href; }

async function putPage(req, res) {
  if (!res || !res.ok || res.type === "opaqueredirect" || res.redirected) return;
  const ct = res.headers.get("content-type") || "";
  if (!ct.includes("text/html")) return;
  const c = await caches.open(PAGES);
  await c.put(pageKey(req.url), await stamp(res));
  trim(PAGES, PAGE_LIMIT);
}

function timeout(ms) { return new Promise((r) => setTimeout(() => r(null), ms)); }

async function offline(req) {
  const en = new URL(req.url).pathname.startsWith("/en/");
  return (await caches.match(en ? "/en/offline/" : "/hors-ligne/")) || new Response("Offline", { status: 503, headers: { "content-type": "text/plain" } });
}

async function page(e) {
  const req = e.request;
  const cached = await caches.match(pageKey(req.url), { ignoreSearch: true, cacheName: PAGES });
  const age = cached ? Date.now() - Number(cached.headers.get("x-cf-cached") || 0) : Infinity;
  const net = (async () => {
    try {
      const pre = e.preloadResponse ? await e.preloadResponse : null;
      const res = pre || await fetch(req);
      await putPage(req, res.clone());
      return res;
    } catch (_) { return null; }
  })();
  e.waitUntil(net);
  if (cached && age < PAGE_MAX_AGE) return cached;            // fresh enough: instant, refreshed in background
  const res = await Promise.race([net, timeout(cached ? NET_TIMEOUT : 15000)]);
  if (res) return res;
  if (cached) return cached;                                  // slow or no network: last copy
  return (await net) || offline(req);
}

async function asset(e) {
  const req = e.request;
  const url = new URL(req.url);
  const c = await caches.open(ASSETS);
  const hit = (await caches.match(req, { cacheName: SHELL })) || (await c.match(req));
  const versioned = url.searchParams.has("v") || url.pathname.startsWith("/fonts/") || url.pathname.startsWith("/icons/");
  const fresh = fetch(req).then((res) => {
    if (res && res.ok && res.type === "basic") { c.put(req, res.clone()); trim(ASSETS, ASSET_LIMIT); }
    return res;
  }).catch(() => null);
  if (hit && versioned) return hit;
  if (hit) { e.waitUntil(fresh); return hit; }                // stale-while-revalidate
  return (await fresh) || new Response("", { status: 504 });
}

async function data(e) {
  try {
    const res = await fetch(e.request);
    if (res.ok) { const c = await caches.open(ASSETS); c.put(e.request, res.clone()); }
    return res;
  } catch (_) {
    return (await caches.match(e.request, { cacheName: ASSETS })) || new Response("[]", { status: 503, headers: { "content-type": "application/json" } });
  }
}

self.addEventListener("fetch", (e) => {
  const req = e.request;
  const url = new URL(req.url);
  if (bypass(url, req)) return;
  if (req.mode === "navigate" || (req.headers.get("accept") || "").includes("text/html")) { e.respondWith(page(e)); return; }
  if (/\.(json|csv|xml|webmanifest)$/.test(url.pathname)) { e.respondWith(data(e)); return; }
  e.respondWith(asset(e));
});
"""

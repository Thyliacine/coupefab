"""Shared page shell: head, mega-nav header, footer. Signature matches build.py's layout()."""
import json

from .taxonomy import T, PATHS, HUBS, HUB_ORDER, hub_path
from . import donate

SITE = "https://coupefab.ca"
YEAR = "2026"
ASSET_V = "20261127ux3"  # bump to bust CSS/JS caches


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def _icon(name):
    icons = {
        "search": '<svg viewBox="0 0 24 24" aria-hidden="true" class="ico"><circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" stroke-width="2"/><path d="M20 20l-3.6-3.6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
        "chev": '<svg viewBox="0 0 24 24" aria-hidden="true" class="ico ico-chev"><path d="M6 9l6 6 6-6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
        "menu": '<svg viewBox="0 0 24 24" aria-hidden="true" class="ico"><path d="M4 7h16M4 12h16M4 17h16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
    }
    return icons[name]


def brand_svg():
    # CoupeFab mark v3 ("Tôle tranchée"): a plate sliced by a glowing kerf, the two parts separating.
    return ('<svg class="brand-mark" viewBox="0 0 32 32" aria-hidden="true">'
            '<rect width="32" height="32" rx="8" fill="#15191c"/><path d="M7 7h15.2L9.4 24.6H7z" fill="#f4f2ec"/><path d="M25 25H9.8L22.6 7.4H25z" fill="#f4f2ec" opacity=".55"/><path d="M23.4 6.2L8.6 26" stroke="#ff5a1f" stroke-width="1.8" stroke-linecap="round"/><circle cx="8.6" cy="26" r="2.1" fill="#ff5a1f"/></svg>')


def mega_nav(lang: str, path: str) -> str:
    from . import guides as G  # lazy: avoid import cycle
    t, p = T[lang], PATHS[lang]
    reg = G.registry()
    def link(g):
        return f'<li><a href="{g.url(lang)}">{esc(g.nav(lang))}</a></li>'
    sw = [g for g in reg if g.hub == "software"]
    sw.sort(key=lambda g: (g.order, g.nav(lang).lower()))
    pr = sorted([g for g in reg if g.hub == "process"], key=lambda g: (g.order, g.nav(lang).lower()))
    topic_ids = ["gcode", "feeds-speeds", "kerf", "bend-allowance", "materials-grades", "dxf-best-practices"]
    topics = [g for tid in topic_ids for g in reg if g.id == tid]
    hubs_more = "".join(
        f'<li class="more"><a href="{hub_path(h, lang)}">{esc(HUBS[h][2] if lang == "fr" else HUBS[h][3])} →</a></li>'
        for h in ("fundamentals", "materials", "troubleshooting", "shop"))
    hubs_more += (f'<li class="more"><a href="{"/codes-erreur/" if lang == "fr" else "/en/error-codes/"}">'
                  f'{"Codes d’erreur et alarmes" if lang == "fr" else "Error codes and alarms"} →</a></li>')
    guides_active = path.startswith(p["guides"])
    def cur(key):
        return ' aria-current="page"' if path.startswith(p[key]) and (key != "home") else ""
    return f"""
<nav class="mainnav" id="mainnav" aria-label="{'Navigation principale' if lang == 'fr' else 'Main navigation'}">
  <ul class="nav-top">
    <li class="has-mega">
      <button class="nav-btn" type="button" aria-expanded="false" aria-controls="mega-guides"{' data-active="1"' if guides_active else ''}>{t['guides']}{_icon('chev')}</button>
      <div class="mega" id="mega-guides">
        <div class="mega-inner">
          <div class="mega-col mega-sw">
            <p class="mega-h"><a href="{hub_path('software', lang)}">{t['by_software']}</a></p>
            <ul class="mega-list two">{''.join(link(g) for g in sw[:18])}</ul>
            <p class="mega-all"><a href="{hub_path('software', lang)}">{t['all_software']} →</a></p>
          </div>
          <div class="mega-col">
            <p class="mega-h"><a href="{hub_path('process', lang)}">{t['by_process']}</a></p>
            <ul class="mega-list">{''.join(link(g) for g in pr)}</ul>
          </div>
          <div class="mega-col">
            <p class="mega-h"><a href="{hub_path('fundamentals', lang)}">{t['by_topic']}</a></p>
            <ul class="mega-list">{''.join(link(g) for g in topics)}{hubs_more}</ul>
          </div>
          <div class="mega-col mega-feature">
            <a class="feature-card" href="{p['prices']}">
              <span class="feature-k">{'Outil' if lang == 'fr' else 'Tool'}</span>
              <strong>{t['prices']}</strong>
              <span>{t['prices_cta_d']}</span>
            </a>
            <a class="feature-card" href="{'/outils/calculateur-liquide-de-coupe/' if lang == 'fr' else '/en/tools/coolant-calculator/'}">
              <span class="feature-k">{'Outil' if lang == 'fr' else 'Tool'}</span>
              <strong>{'Calculateur de liquide de coupe' if lang == 'fr' else 'Coolant calculator'}</strong>
              <span>{'Concentré, eau et réfractomètre pour votre machine' if lang == 'fr' else 'Concentrate, water and refractometer for your machine'}</span>
            </a>
            <a class="mega-allguides" href="{p['guides']}">{t['all_guides']} ({len(reg)}) →</a>
          </div>
        </div>
      </div>
    </li>
    <li><a class="nav-link nav-prices" href="{p['prices']}"{cur('prices')}><span class="nav-short">{t['prices_nav']}</span><span class="nav-full">{t['prices_nav']}</span></a></li>
    <li><a class="nav-link" href="{p['used']}"{cur('used')}><span class="nav-short">{'Occasions' if lang == 'fr' else 'Used'}</span><span class="nav-full">{t['used']}</span></a></li>
    <li class="nav-fold"><a class="nav-link" href="{p['parts']}"{cur('parts')}>{t['parts']}</a></li>
    <li class="nav-fold"><a class="nav-link" href="{p['tooling']}"{cur('tooling')}>{t['tooling']}</a></li>
    <li><a class="nav-link" href="{p['suppliers']}"{' aria-current="page"' if path.startswith((p['suppliers'],)) else ''}>{'Fournisseurs' if lang == 'fr' else 'Suppliers'}</a></li>
    <li class="nav-fold"><a class="nav-link" href="{p['tools']}"{' aria-current="page"' if path.startswith(('/outils/', '/en/tools/')) else ''}>{t['tools']}</a></li>
    <li class="nav-more">
      <details class="nav-more-box">
        <summary class="nav-btn"{' data-active="1"' if path.startswith((p['parts'], p['tooling'], p['tools'], p['add_prices'])) else ''}>{'Plus' if lang == 'fr' else 'More'}{_icon('chev')}</summary>
        <ul class="nav-more-menu">
          <li><a href="{p['parts']}"{cur('parts')}>{t['parts']}</a></li>
          <li><a href="{p['tooling']}"{cur('tooling')}>{t['tooling']}</a></li>
          <li><a href="{p['tools']}"{' aria-current="page"' if path.startswith(('/outils/', '/en/tools/')) else ''}>{t['tools']}</a></li>
          <li class="nav-more-cta"><a class="nav-cta" href="{p['add_prices']}"{' aria-current="page"' if path.startswith((p['add_prices'],)) else ''}>{t['add_prices']}</a></li>
        </ul>
      </details>
    </li>
    <li class="nav-cta-item"><a class="nav-cta" href="{p['add_prices']}"{' aria-current="page"' if path.startswith((p['add_prices'],)) else ''}>{t['add_prices']}</a></li>
  </ul>
</nav>"""


def layout(*, lang, title, description, path, alt, body, draft=False, article=False, crumbs="", noindex=False, **_):
    fr = lang == "fr"
    t, p = T[lang], PATHS[lang]
    in_lang = "fr-CA" if fr else "en-CA"
    alt_lang = "en-CA" if fr else "fr-CA"
    canonical = SITE + path
    alt_url = SITE + alt
    fr_url = canonical if fr else alt_url
    schema = ""
    if article:
        schema = '<script type="application/ld+json">' + json.dumps({
            "@context": "https://schema.org", "@type": "Article", "headline": title, "description": description,
            "inLanguage": in_lang, "dateModified": "2026-11-26", "url": canonical,
            "author": {"@type": "Organization", "name": "CoupeFab"},
            "publisher": {"@type": "Organization", "name": "CoupeFab", "url": SITE + "/"},
        }, ensure_ascii=False) + "</script>"
    if path in ("/", "/en/"):
        schema += '<script type="application/ld+json">' + json.dumps({
            "@context": "https://schema.org", "@graph": [
                {"@type": "Organization", "@id": SITE + "/#org", "name": "CoupeFab", "url": SITE + "/",
                 "logo": SITE + "/favicon.svg", "areaServed": ["Quebec", "Canada"]},
                {"@type": "WebSite", "@id": SITE + "/#site", "url": SITE + "/", "name": "CoupeFab",
                 "inLanguage": ["fr-CA", "en-CA"], "publisher": {"@id": SITE + "/#org"},
                 "potentialAction": {"@type": "SearchAction", "target": SITE + ("/guides/" if fr else "/en/guides/") + "?q={search_term_string}",
                                     "query-input": "required name=search_term_string"}},
            ]}, ensure_ascii=False) + "</script>"
    draft_banner = ""
    if draft:
        draft_banner = (f'<div class="draft-strip" role="note"><span class="pill pill-draft">{t["draft"]}</span> '
                        + ("Page en révision par Michaël. Les chiffres viennent des sources citées."
                           if fr else "Page under review by Michaël. Figures come from the cited sources.") + "</div>")
    is_guide = 'class="guide" data-guide=' in body
    progress_attr = ' class="is-guide"' if is_guide else ""
    progress = '<div class="readbar" aria-hidden="true"><span></span></div>' if is_guide else ""
    fr_href = path if fr else alt
    en_href = alt if fr else path
    year = YEAR
    return f"""<!DOCTYPE html>
<html lang="{in_lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="robots" content="{'noindex' if noindex else 'index,follow,max-image-preview:large'}">
<meta name="theme-color" content="#15191c">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="{in_lang}" href="{canonical}">
<link rel="alternate" hreflang="{alt_lang}" href="{alt_url}">
<link rel="alternate" hreflang="x-default" href="{fr_url}">
<meta property="og:site_name" content="CoupeFab">
<meta property="og:type" content="{'article' if article else 'website'}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="{'fr_CA' if fr else 'en_CA'}">
<meta property="og:locale:alternate" content="{'en_CA' if fr else 'fr_CA'}">
<meta property="og:image" content="{SITE}/og/og-{lang}.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{'CoupeFab — guides CNC et prix des tôles' if fr else 'CoupeFab — CNC guides and sheet prices'}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{SITE}/og/og-{lang}.png">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/fonts/plex-sans.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/css/style.css?v={ASSET_V}">
<link rel="stylesheet" href="/css/site.css?v={ASSET_V}">
<link rel="stylesheet" href="/css/ux.css?v={ASSET_V}">
<script src="/js/pager.js?v={ASSET_V}" defer></script>
{schema}
</head>
<body data-lang="{lang}"{progress_attr}>
{progress}
<a class="skip" href="#contenu">{t['skip']}</a>
<header class="hdr">
  <div class="hdr-inner">
    <a class="brand" href="{p['home']}" aria-label="CoupeFab — {t['home']}">{brand_svg()}<span class="brand-word">Coupe<b>Fab</b></span></a>
    {mega_nav(lang, path)}
    <div class="hdr-tools">
      <button class="search-btn" type="button" data-search-open aria-label="{t['search']}">{_icon('search')}<span class="search-btn-label">{t['search']}</span><kbd>/</kbd></button>
      <button class="menu-btn" type="button" aria-expanded="false" aria-controls="mainnav" aria-label="{t['menu']}">{_icon('menu')}</button>
      <div class="lang" role="group" aria-label="{t['lang']}">
        <a href="{fr_href}" hreflang="fr-CA" lang="fr-CA"{' aria-current="true"' if fr else ''}>FR</a><a href="{en_href}" hreflang="en-CA" lang="en-CA"{' aria-current="true"' if not fr else ''}>EN</a>
      </div>
      <a class="hdr-newsletter" href="{p['news']}"{' aria-current="page"' if path.startswith((p['news'],)) else ''}>{t['news']}</a>
    </div>
  </div>
</header>
<div class="search-dlg" id="search-dlg" hidden role="dialog" aria-modal="true" aria-label="{t['search']}">
  <div class="search-panel">
    <div class="search-field">{_icon('search')}<input type="search" id="search-input" placeholder="{esc(t['search_ph'])}" autocomplete="off" spellcheck="false" aria-controls="search-results"><button type="button" class="search-close" data-search-close>{t['close']}</button></div>
    <ul class="search-results" id="search-results" role="listbox"></ul>
    <p class="search-empty" hidden>{t['no_results']}</p>
  </div>
</div>
{draft_banner}
<main id="contenu">
{crumbs}
{body}
</main>
<footer class="ftr">
  <div class="ftr-inner">
    <div class="ftr-brand">
      <a class="brand" href="{p['home']}">{brand_svg()}<span class="brand-word">Coupe<b>Fab</b></span></a>
      <p>{'La référence francophone de la découpe CNC et de la fabrication métallique : guides vérifiés, prix des tôles comparés, occasions au Québec.' if fr else 'A French-first reference for CNC cutting and metal fabrication: sourced guides, compared sheet prices, used equipment in Quebec.'}</p>
      <p class="ftr-support">{donate.button(lang, 'btn-support')}</p>
    </div>
    <div>
      <p class="ftr-h">{t['guides']}</p>
      <ul>
        <li><a href="{hub_path('software', lang)}">{HUBS['software'][2] if fr else HUBS['software'][3]}</a></li>
        <li><a href="{hub_path('process', lang)}">{HUBS['process'][2] if fr else HUBS['process'][3]}</a></li>
        <li><a href="{hub_path('fundamentals', lang)}">{HUBS['fundamentals'][2] if fr else HUBS['fundamentals'][3]}</a></li>
        <li><a href="{hub_path('materials', lang)}">{HUBS['materials'][2] if fr else HUBS['materials'][3]}</a></li>
        <li><a href="{hub_path('troubleshooting', lang)}">{HUBS['troubleshooting'][2] if fr else HUBS['troubleshooting'][3]}</a></li>
        <li><a href="{hub_path('shop', lang)}">{HUBS['shop'][2] if fr else HUBS['shop'][3]}</a></li>
        <li><a href="{'/codes-erreur/' if fr else '/en/error-codes/'}">{'Codes d’erreur' if fr else 'Error codes'}</a></li>
      </ul>
    </div>
    <div>
      <p class="ftr-h">{t['explore']}</p>
      <ul>
        <li><a href="{p['prices']}">{t['prices_nav']}</a></li>
        <li><a href="{p['used']}">{t['used']}</a></li>
        <li><a href="{p['parts']}">{t['parts']}</a></li>
        <li><a href="{p['tooling']}">{t['tooling']}</a></li>
        <li><a href="{'/outils/calculateur-liquide-de-coupe/' if fr else '/en/tools/coolant-calculator/'}">{'Calculateur de liquide de coupe' if fr else 'Coolant calculator'}</a></li>
        <li><a href="{p['suppliers']}">{'Fournisseurs' if fr else 'Suppliers'}</a></li>
        <li><a href="{p['tools']}">{t['tools']}</a></li>
        <li><a href="{p['add_prices']}">{t['add_prices']}</a></li>
        <li><a href="{p['headlines']}">{t['headlines']}</a></li>
        <li><a href="{p['news']}">{t['news']}</a></li>
        <li><a href="{p['announce']}">{t['announce']}</a></li>
        <li><a href="{p['about']}">{t['about']}</a></li>
      </ul>
    </div>
    <div>
      <p class="ftr-h">{t['legal']}</p>
      <ul>
        <li><a href="{p['disc']}">{'Divulgation (aucune affiliation)' if fr else 'Disclosure (no affiliates)'}</a></li>
        <li><a href="{p['priv']}">{'Confidentialité (Loi 25)' if fr else 'Privacy (Law 25)'}</a></li>
        <li><a href="{'/conditions/' if fr else '/en/terms/'}">{'Conditions d’utilisation' if fr else 'Terms of use'}</a></li>
      </ul>
    </div>
  </div>
  <p class="ftr-legal">© {year} CoupeFab · {'Québec, Canada. Aucun lien d’affiliation ni publicité payante. Les marques citées appartiennent à leurs propriétaires et sont mentionnées à titre descriptif.' if fr else 'Quebec, Canada. No affiliate links or paid ads. Trademarks belong to their owners and are used descriptively.'} · <a class="ftr-admin" href="/admin/" rel="nofollow">{'Admin' if fr else 'Admin'}</a></p>
</footer>
<button class="totop" type="button" hidden aria-label="{'Retour en haut' if fr else 'Back to top'}"><svg viewBox="0 0 24 24" aria-hidden="true" class="ico"><path d="M12 19V5M5 12l7-7 7 7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
<script src="/js/hot-news.js?v={ASSET_V}" defer></script>
<script src="/js/site.js?v={ASSET_V}" defer></script>
<script>window.va=window.va||function(){{(window.vaq=window.vaq||[]).push(arguments);}};</script>
<script defer src="/_vercel/insights/script.js"></script>
</body>
</html>
"""

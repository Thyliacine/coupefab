"""Guides library: load content/guides/*.md, render guide pages, hubs, index and search index."""
import json
import re
from functools import lru_cache
from pathlib import Path

from .md import render, inline
from .taxonomy import HUBS, HUB_ORDER, SOFTWARE_GROUPS, LEVELS, T, PATHS, hub_path
from .layout import esc, SITE

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content" / "guides"
MONTHS_FR = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
MONTHS_EN = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def fmt_date(iso, lang):
    y, m, d = (int(x) for x in iso.split("-"))
    return f"{d} {MONTHS_FR[m-1]} {y}" if lang == "fr" else f"{MONTHS_EN[m-1]} {d}, {y}"


class Guide:
    def __init__(self, meta, body_fr, body_en):
        self.m = meta
        self.id = meta["id"]
        self.hub = meta["hub"]
        self.group = meta.get("group", "")
        self.order = int(meta.get("order", "50"))
        self.level = meta.get("level", "debutant")
        self.schema = meta.get("schema", "Article")
        self.related_ids = [x.strip() for x in meta.get("related", "").split(",") if x.strip()]
        self.tags = [x.strip() for x in meta.get("tags", "").split(",") if x.strip()]
        self.prices = meta.get("prices", "no").lower() in ("yes", "oui", "true", "1")
        self.reviewed = meta.get("reviewed", "2026-11-26")
        self.body = {"fr": body_fr, "en": body_en}
        self.featured = meta.get("featured", "no") == "yes"

    def slug(self, lang):
        return self.m[f"{lang}_slug"]

    def url(self, lang):
        return f"/guides/{self.slug('fr')}/" if lang == "fr" else f"/en/guides/{self.slug('en')}/"

    def title(self, lang):
        return self.m[f"{lang}_title"]

    def desc(self, lang):
        return self.m[f"{lang}_desc"]

    def nav(self, lang):
        n = self.m.get("nav")
        if n and "|" in n:
            a, b = n.split("|", 1)
            return (a if lang == "fr" else b).strip()
        return self.title(lang)

    def kicker(self, lang):
        k = self.m.get("kicker")
        if k and "|" in k:
            a, b = k.split("|", 1)
            return (a if lang == "fr" else b).strip()
        return HUBS[self.hub][2 if lang == "fr" else 3]

    def words(self, lang):
        return len(re.findall(r"\w+", self.body[lang]))


def _parse(path: Path) -> Guide:
    raw = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
    if not m:
        raise ValueError(f"{path}: missing front matter")
    meta = {}
    for line in m.group(1).split("\n"):
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    rest = m.group(2)
    parts = re.split(r"^=== (fr|en)\s*$", rest, flags=re.M)
    bodies = {}
    for i in range(1, len(parts), 2):
        bodies[parts[i]] = parts[i + 1].strip()
    for k in ("id", "hub", "fr_slug", "en_slug", "fr_title", "en_title", "fr_desc", "en_desc"):
        if k not in meta:
            raise ValueError(f"{path}: missing {k}")
    if meta["hub"] not in HUBS:
        raise ValueError(f"{path}: unknown hub {meta['hub']}")
    return Guide(meta, bodies.get("fr", ""), bodies.get("en", ""))


@lru_cache(maxsize=1)
def registry():
    guides = [_parse(p) for p in sorted(CONTENT.glob("*.md"))]
    ids = [g.id for g in guides]
    dup = {i for i in ids if ids.count(i) > 1}
    if dup:
        raise ValueError(f"duplicate guide ids: {dup}")
    _expand_wikilinks(guides)
    return guides


_WIKI = re.compile(r"\[\[([a-z0-9-]+)(?:\|([^\]]+))?\]\]")
_PENDING = {"siemens-sinumerik": "Siemens Sinumerik", "lathe-finish-chatter": "Tournage : fini et vibrations"}
_SPECIAL = {"prix": ("/prix/", "/en/sheet-prices/", "comparateur de prix", "price comparison tool")}


def _expand_wikilinks(guides):
    """[[guide-id]] or [[guide-id|label]] -> markdown link in the body's language."""
    idx = {g.id: g for g in guides}
    for g in guides:
        for lang in ("fr", "en"):
            def sub(m, lang=lang, g=g):
                gid, label = m.group(1), m.group(2)
                if gid in _SPECIAL:
                    fr_u, en_u, fr_l, en_l = _SPECIAL[gid]
                    return f"[{label or (fr_l if lang == 'fr' else en_l)}]({fr_u if lang == 'fr' else en_u})"
                if gid not in idx:  # guide not written yet: plain text for now
                    print(f"warning: {g.id}: pending wikilink [[{gid}]]")
                    return label or _PENDING.get(gid, gid.replace("-", " ").title())
                o = idx[gid]
                return f"[{label or o.nav(lang)}]({o.url(lang)})"
            g.body[lang] = _WIKI.sub(sub, g.body[lang])


def by_id():
    return {g.id: g for g in registry()}


def related(g, n=4):
    idx = by_id()
    out = [idx[i] for i in g.related_ids if i in idx and i != g.id]
    for other in registry():
        if len(out) >= n:
            break
        if other.id != g.id and other not in out and (other.hub == g.hub or set(other.tags) & set(g.tags)):
            out.append(other)
    return out[:n]


def card(g, lang, compact=False):
    lv = LEVELS.get(g.level, LEVELS["debutant"])[0 if lang == "fr" else 1]
    mins = max(3, round(g.words(lang) / 210))
    meta = f'<span class="card-meta">{esc(g.kicker(lang))} · {lv} · {mins} {T[lang]["read"]}</span>'
    if compact:
        return f'<a class="gcard gcard-sm" href="{g.url(lang)}"><strong>{esc(g.title(lang))}</strong>{meta}</a>'
    return (f'<a class="gcard" href="{g.url(lang)}" data-hub="{g.hub}">{meta}<strong>{esc(g.title(lang))}</strong>'
            f'<span class="card-desc">{esc(g.desc(lang))}</span></a>')


def breadcrumbs(lang, items):
    """items: list of (label, href or None)."""
    lis, ld = [], []
    for pos, (label, href) in enumerate(items, 1):
        if href:
            lis.append(f'<li><a href="{href}">{esc(label)}</a></li>')
            ld.append({"@type": "ListItem", "position": pos, "name": label, "item": SITE + href})
        else:
            lis.append(f'<li aria-current="page">{esc(label)}</li>')
            ld.append({"@type": "ListItem", "position": pos, "name": label})
    schema = json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": ld}, ensure_ascii=False)
    aria = "Fil d’Ariane" if lang == "fr" else "Breadcrumb"
    return f'<nav class="crumbs" aria-label="{aria}"><ol>{"".join(lis)}</ol></nav><script type="application/ld+json">{schema}</script>'


def _strip(html_text):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html_text)).strip()


def _faq_schema(body_html):
    m = re.search(r'<h2 id="faq[^"]*">.*?</h2>(.*?)(?=<h2 |\Z)', body_html, re.S)
    if not m:
        return None
    qa = re.findall(r"<h3[^>]*>(.*?)</h3>(.*?)(?=<h3|\Z)", m.group(1), re.S)
    ents = [{"@type": "Question", "name": _strip(q), "acceptedAnswer": {"@type": "Answer", "text": _strip(a)}} for q, a in qa if _strip(a)]
    if not ents:
        return None
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": ents}


def _howto_schema(g, lang, body_html, url):
    m = re.search(r'<ol class="steps">(.*?)</ol>', body_html, re.S)
    if not m:
        return None
    steps = re.findall(r"<li>(.*?)</li>", m.group(1), re.S)
    out = []
    for s in steps:
        txt = _strip(s)
        name = re.split(r"[.:]", txt, 1)[0][:110]
        out.append({"@type": "HowToStep", "name": name, "text": txt})
    if len(out) < 3:
        return None
    return {"@context": "https://schema.org", "@type": "HowTo", "name": g.title(lang), "description": g.desc(lang),
            "inLanguage": "fr-CA" if lang == "fr" else "en-CA", "step": out}


def _wrap_sections(body_html, lang):
    # Style "Sources" and "for Michaël to review" sections
    body_html = re.sub(r'(<h2 id="sources[^"]*">.*?</h2>)(.*?)(?=<h2 |\Z)',
                       r'<section class="sources">\1\2</section>', body_html, flags=re.S)
    body_html = re.sub(r'(<h2 id="(?:a-valider[^"]*|for-michael[^"]*)">.*?</h2>)(.*?)(?=<h2 |<section |\Z)',
                       r'<section class="review-box">\1\2</section>', body_html, flags=re.S)
    return body_html


def guide_page(g, lang, form_newsletter):
    t, p = T[lang], PATHS[lang]
    body_html, toc = render(g.body[lang], lang)
    body_html = _wrap_sections(body_html, lang)
    url = g.url(lang)
    lv = LEVELS.get(g.level, LEVELS["debutant"])[0 if lang == "fr" else 1]
    mins = max(3, round(g.words(lang) / 210))
    crumbs = breadcrumbs(lang, [(t["home"], p["home"]), (t["guides"], p["guides"]),
                                (HUBS[g.hub][2] if lang == "fr" else HUBS[g.hub][3], hub_path(g.hub, lang)),
                                (g.nav(lang), None)])
    toc_items = [(i, txt) for lvl, i, txt in toc if lvl == 2]
    toc_html = ""
    if len(toc_items) >= 3:
        lis = "".join(f'<li><a href="#{i}">{esc(txt)}</a></li>' for i, txt in toc_items)
        toc_html = (f'<details class="toc" open><summary>{t["on_page"]}</summary><ol>{lis}</ol></details>')
    rel = related(g)
    rel_html = ""
    if rel:
        rel_html = f'<section class="related"><h2>{t["related"]}</h2><div class="gcards">{"".join(card(r, lang) for r in rel)}</div></section>'
    price_cta = ""
    if g.prices:
        price_cta = (f'<aside class="price-cta"><div><p class="price-cta-k">{"Outil CoupeFab" if lang == "fr" else "CoupeFab tool"}</p>'
                     f'<p class="price-cta-t">{t["prices_cta_t"]}</p><p>{t["prices_cta_d"]}</p></div>'
                     f'<a class="btn" href="{p["prices"]}">{t["prices_cta_b"]}</a></aside>')
    schemas = []
    art = {"@context": "https://schema.org", "@type": "TechArticle" if g.hub != "shop" else "Article",
           "headline": g.title(lang), "description": g.desc(lang), "inLanguage": "fr-CA" if lang == "fr" else "en-CA",
           "dateModified": g.reviewed, "datePublished": g.m.get("published", "2026-11-26"), "url": SITE + url,
           "mainEntityOfPage": SITE + url, "proficiencyLevel": "Beginner" if g.level == "debutant" else ("Expert" if g.level == "avance" else "Intermediate"),
           "author": {"@type": "Organization", "name": "CoupeFab", "url": SITE + "/"},
           "publisher": {"@type": "Organization", "name": "CoupeFab", "url": SITE + "/", "logo": {"@type": "ImageObject", "url": SITE + "/favicon.svg"}},
           "about": g.tags}
    schemas.append(art)
    if g.schema.lower() == "howto":
        h = _howto_schema(g, lang, body_html, url)
        if h:
            schemas.append(h)
    f = _faq_schema(body_html)
    if f:
        schemas.append(f)
    ld = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)
    report_href = p["about"] + "#contact"
    body = f"""
{crumbs}
<article class="guide" data-guide="{g.id}">
  <header class="guide-head">
    <p class="kicker">{esc(g.kicker(lang))}</p>
    <h1>{esc(g.title(lang))}</h1>
    <p class="guide-lede">{inline(g.desc(lang))}</p>
    <p class="guide-meta">
      <span>{t['reviewed']} <time datetime="{g.reviewed}">{fmt_date(g.reviewed, lang)}</time></span>
      <span>{mins} {t['read']}</span>
      <span>{t['level']} : {lv}</span>
      <span class="pill pill-draft" tabindex="0" title="{esc(t['draft_tip'])}">{t['draft']}<span class="pill-tip" role="tooltip">{esc(t['draft_tip'])}</span></span>
    </p>
  </header>
  <div class="guide-grid">
    <aside class="guide-side">{toc_html}</aside>
    <div class="prose guide-body">
{body_html}
{price_cta}
      <p class="report"><a href="{report_href}">{t['report']} →</a></p>
    </div>
  </div>
  {rel_html}
  <section class="news-band">
    <div><p class="news-band-t">{t['news_t']}</p><p>{t['news_d']}</p></div>
    {form_newsletter(lang)}
  </section>
</article>
{ld}
"""
    return body


def hub_page(hub, lang):
    t, p = T[lang], PATHS[lang]
    fr = lang == "fr"
    title = HUBS[hub][2 if fr else 3]
    blurb = HUBS[hub][4 if fr else 5]
    gs = sorted([g for g in registry() if g.hub == hub], key=lambda g: (g.order, g.title(lang).lower()))
    crumbs = breadcrumbs(lang, [(t["home"], p["home"]), (t["guides"], p["guides"]), (title, None)])
    if hub == "software":
        sections = []
        for gid, lfr, len_ in SOFTWARE_GROUPS:
            items = [g for g in gs if g.group == gid]
            if items:
                sections.append(f'<h2 class="sec-h">{lfr if fr else len_}</h2><div class="gcards">{"".join(card(g, lang) for g in items)}</div>')
        rest = [g for g in gs if g.group not in {x[0] for x in SOFTWARE_GROUPS}]
        if rest:
            sections.append(f'<div class="gcards">{"".join(card(g, lang) for g in rest)}</div>')
        inner = "".join(sections)
    else:
        inner = f'<div class="gcards">{"".join(card(g, lang) for g in gs)}</div>'
    others = "".join(f'<a class="chip" href="{hub_path(h, lang)}">{esc(HUBS[h][2 if fr else 3])}</a>' for h in HUB_ORDER if h != hub)
    items_ld = [{"@type": "ListItem", "position": i + 1, "url": SITE + g.url(lang), "name": g.title(lang)} for i, g in enumerate(gs)]
    ld = json.dumps({"@context": "https://schema.org", "@type": "CollectionPage", "name": title, "description": blurb,
                     "inLanguage": "fr-CA" if fr else "en-CA", "mainEntity": {"@type": "ItemList", "itemListElement": items_ld}}, ensure_ascii=False)
    return f"""
<div class="page">
{crumbs}
<header class="page-head">
  <p class="kicker">{t['guides']} · {len(gs)}</p>
  <h1>{esc(title)}</h1>
  <p class="lede">{esc(blurb)}</p>
</header>
{inner}
<nav class="chips other-hubs" aria-label="{'Autres sections' if fr else 'Other sections'}">{others}</nav>
</div>
<script type="application/ld+json">{ld}</script>
"""


START_PATHS = {
    "fr": [
        ("Débuter en plasma CNC", ["plasma-cutting", "dxf-best-practices", "sheetcam", "lead-ins-pierce", "kerf", "plasma-troubleshooting"]),
        ("Concevoir de la tôle qui se plie bien", ["solidworks-sheet-metal", "bend-allowance", "press-brake", "tolerances"]),
        ("Fraiseuse et tour : premiers programmes", ["gcode", "work-offsets", "feeds-speeds", "mastercam-2d", "milling-troubleshooting"]),
    ],
    "en": [
        ("Getting started with CNC plasma", ["plasma-cutting", "dxf-best-practices", "sheetcam", "lead-ins-pierce", "kerf", "plasma-troubleshooting"]),
        ("Designing sheet metal that bends right", ["solidworks-sheet-metal", "bend-allowance", "press-brake", "tolerances"]),
        ("Mill and lathe: first programs", ["gcode", "work-offsets", "feeds-speeds", "mastercam-2d", "milling-troubleshooting"]),
    ],
}


def index_page(lang):
    t, p = T[lang], PATHS[lang]
    fr = lang == "fr"
    reg = registry()
    idx = by_id()
    crumbs = breadcrumbs(lang, [(t["home"], p["home"]), (t["guides"], None)])
    paths_html = []
    for name, ids in START_PATHS[lang]:
        steps = [idx[i] for i in ids if i in idx]
        if len(steps) < 2:
            continue
        lis = "".join(f'<li><a href="{g.url(lang)}">{esc(g.nav(lang))}</a></li>' for g in steps)
        paths_html.append(f'<div class="path"><p class="path-t">{esc(name)}</p><ol>{lis}</ol></div>')
    hubs_html = []
    for h in HUB_ORDER:
        gs = sorted([g for g in reg if g.hub == h], key=lambda g: (g.order, g.title(lang).lower()))
        if not gs:
            continue
        hubs_html.append(f"""
<section class="hub-sec" id="{HUBS[h][0] if fr else HUBS[h][1]}" data-hub-sec="{h}">
  <div class="hub-sec-head"><h2><a href="{hub_path(h, lang)}">{esc(HUBS[h][2 if fr else 3])}</a></h2><p>{esc(HUBS[h][4 if fr else 5])}</p></div>
  <div class="gcards">{''.join(card(g, lang) for g in gs)}</div>
</section>""")
    chips = f'<button type="button" class="chip" aria-pressed="true" data-filter="all">{"Tout" if fr else "All"} ({len(reg)})</button>' + "".join(
        f'<button type="button" class="chip" aria-pressed="false" data-filter="{h}">{esc(HUBS[h][2 if fr else 3].split(" ")[0] if h != "software" else ("Logiciels" if fr else "Software"))} ({sum(1 for g in reg if g.hub == h)})</button>'
        for h in HUB_ORDER)
    intro = ("Des guides pratiques, pas des brochures : étapes, tableaux, listes de vérification, erreurs fréquentes et FAQ. "
             "Chaque chiffre renvoie à une documentation officielle ou à une charte de fabricant. Tout est encore marqué <em>brouillon</em> jusqu’à la révision technique de Michaël."
             if fr else
             "Practical guides, not brochures: steps, tables, checklists, common mistakes and FAQs. Every number points to official documentation or a manufacturer chart. "
             "Everything is still marked <em>draft</em> until Michaël’s technical review.")
    return f"""
<div class="page">
{crumbs}
<header class="page-head">
  <p class="kicker">{t['guides']} · {len(reg)} {'guides FR + EN' if fr else 'guides, FR + EN'}</p>
  <h1>{'Bibliothèque de guides CNC' if fr else 'CNC guide library'}</h1>
  <p class="lede">{intro}</p>
  <div class="inline-search">
    <label class="vh" for="guide-filter">{t['search']}</label>
    <input type="search" id="guide-filter" placeholder="{esc(t['search_ph'])}" autocomplete="off">
  </div>
  <div class="chips" role="group" aria-label="{'Filtrer par section' if fr else 'Filter by section'}">{chips}</div>
</header>
<section class="paths" aria-label="{'Parcours suggérés' if fr else 'Suggested paths'}">
  <h2 class="sec-h">{'Par où commencer' if fr else 'Where to start'}</h2>
  <div class="paths-grid">{''.join(paths_html)}</div>
</section>
<p class="filter-empty" hidden>{t['no_results']}</p>
{''.join(hubs_html)}
</div>
"""


def search_index(lang):
    out = []
    for g in registry():
        _, toc = render(g.body[lang], lang)
        heads = " · ".join(txt for lvl, _, txt in toc if lvl == 2 and not txt.lower().startswith(("sources", "à valider", "for michaël")))
        out.append({"t": g.title(lang), "d": g.desc(lang), "u": g.url(lang), "h": heads,
                    "c": HUBS[g.hub][2 if lang == "fr" else 3], "k": " ".join(g.tags)})
    # non-guide destinations
    p = PATHS[lang]
    if lang == "fr":
        out += [
            {"t": "Prix des tôles et des métaux", "d": "Comparateur des prix publiés : tôle, plaque, barre, tube. Meilleur prix par spécification.", "u": p["prices"], "h": "", "c": "Outil", "k": "prix acier inox aluminium tôle plaque fournisseur"},
            {"t": "Occasions Québec", "d": "Digest d’équipements CNC et de fabrication usagés au Québec.", "u": p["used"], "h": "", "c": "Outil", "k": "usagé occasion table plasma kijiji encan"},
        ]
    else:
        out += [
            {"t": "Sheet-metal and metal prices", "d": "Published price comparison: sheet, plate, bar, tube. Best price per spec.", "u": p["prices"], "h": "", "c": "Tool", "k": "price steel stainless aluminum sheet plate supplier"},
            {"t": "Used equipment in Quebec", "d": "Digest of used CNC and fab equipment in Quebec.", "u": p["used"], "h": "", "c": "Tool", "k": "used plasma table auction"},
        ]
    return out


def write_search_indexes():
    for lang, dest in (("fr", ROOT / "guides" / "recherche.json"), ("en", ROOT / "en" / "guides" / "search.json")):
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(search_index(lang), ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

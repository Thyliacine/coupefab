"""Home pages (FR / EN)."""
from .guides import registry, by_id, card, START_PATHS
from .taxonomy import T, PATHS, HUBS, hub_path
from .layout import esc

FEATURED = ["sheetcam", "gcode", "bend-allowance", "fusion-cam", "plasma-troubleshooting", "solidworks-sheet-metal", "mastercam-2d", "feeds-speeds"]
QUICK = {"fr": ["SheetCam", "Mastercam", "K-factor", "scories", "G-code", "DXF", "Fusion"],
         "en": ["SheetCam", "Mastercam", "K-factor", "dross", "G-code", "DXF", "Fusion"]}


def home(lang, form_newsletter, prix_meta=None):
    fr = lang == "fr"
    t, p = T[lang], PATHS[lang]
    reg = registry()
    idx = by_id()
    pm = prix_meta or {}
    rows = pm.get("rows")
    sups = pm.get("suppliers")
    sw = sorted([g for g in reg if g.hub == "software"], key=lambda g: (g.order, g.nav(lang).lower()))
    pr = sorted([g for g in reg if g.hub == "process"], key=lambda g: (g.order, g.nav(lang).lower()))
    feat = [idx[i] for i in FEATURED if i in idx]
    quick = "".join(f'<button type="button" class="qchip" data-search-q="{esc(q)}">{esc(q)}</button>' for q in QUICK[lang])
    stat_rows = f"{rows:,}".replace(",", "\u202f") if isinstance(rows, int) else "—"
    stats = f"""
<ul class="stats" aria-label="{'CoupeFab en chiffres' if fr else 'CoupeFab in numbers'}">
  <li><b>{len(reg)}</b><span>{'guides en français et en anglais' if fr else 'guides in French and English'}</span></li>
  <li><b>{stat_rows}</b><span>{'prix de métaux publiés comparés' if fr else 'published metal prices compared'}</span></li>
  <li><b>{sups if sups else '—'}</b><span>{'fournisseurs suivis chaque jour ouvrable' if fr else 'suppliers tracked every business day'}</span></li>
  <li><b>0</b><span>{'lien d’affiliation, zéro chiffre inventé' if fr else 'affiliate links, zero invented numbers'}</span></li>
</ul>"""
    sw_tiles = "".join(
        f'<a class="tile" href="{g.url(lang)}"><span class="tile-mono" aria-hidden="true">{esc(g.m.get("mono", g.nav(lang)[:2]))}</span><span>{esc(g.nav(lang))}</span></a>'
        for g in sw)
    pr_tiles = "".join(
        f'<a class="ptile" href="{g.url(lang)}"><strong>{esc(g.nav(lang))}</strong><span>{esc(g.desc(lang)[:110].rsplit(" ", 1)[0])}…</span></a>'
        for g in pr)
    paths = []
    for name, ids in START_PATHS[lang]:
        steps = [idx[i] for i in ids if i in idx]
        lis = "".join(f'<li><a href="{g.url(lang)}">{esc(g.nav(lang))}</a></li>' for g in steps)
        paths.append(f'<div class="path"><p class="path-t">{esc(name)}</p><ol>{lis}</ol></div>')
    return f"""
<section class="hero2">
  <div class="hero2-inner">
    <p class="kicker kicker-light">{'CNC · plasma · laser · usinage · tôlerie — Québec et partout' if fr else 'CNC · plasma · laser · machining · sheet metal — Quebec and beyond'}</p>
    <h1>{'Couper, plier et usiner juste, du premier coup.' if fr else 'Cut, bend and machine it right the first time.'}</h1>
    <p class="hero2-lede">{'Des guides d’atelier appuyés sur des sources (Mastercam, SolidWorks, Fusion, SheetCam…), les prix des tôles comparés chez les fournisseurs et les machines d’occasion au Québec. En français d’abord, en anglais aussi.' if fr else 'Shop-floor guides backed by sources (Mastercam, SolidWorks, Fusion, SheetCam…), sheet-metal prices compared across suppliers, and used machines in Quebec. French-first, English too.'}</p>
    <button class="hero-search" type="button" data-search-open>
      <svg viewBox="0 0 24 24" aria-hidden="true" class="ico"><circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" stroke-width="2"/><path d="M20 20l-3.6-3.6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
      <span>{esc(t['search_ph'])}</span><kbd>/</kbd>
    </button>
    <div class="qchips"><span>{'Populaire :' if fr else 'Popular:'}</span>{quick}</div>
  </div>
</section>
<div class="page page-home">
{stats}
<section class="price-feature">
  <div class="price-feature-txt">
    <p class="kicker">{'Outil phare' if fr else 'Flagship tool'}</p>
    <h2>{'Prix des tôles : repérez d’un coup d’œil le bon prix… et le mauvais' if fr else 'Sheet prices: spot a good price, and a bad one, at a glance'}</h2>
    <p>{'Acier, inox, aluminium, en tôle, plaque, barre et tube. Les prix publiés par les fournisseurs sont convertis en $ CA par pi² et par lb, le meilleur prix par spécification est mis en évidence, et chaque ligne renvoie à sa source et à l’heure du relevé.' if fr else 'Steel, stainless and aluminum in sheet, plate, bar and tube. Published supplier prices are converted to CAD per sq ft and per lb, the best price for each spec is highlighted, and every row links to its source and capture time.'}</p>
    <div class="actions"><a class="btn btn-lg" href="{p['prices']}">{t['prices_cta_b']}</a><a class="btn btn-ghost" href="{idx['materials-grades'].url(lang) if 'materials-grades' in idx else p['guides']}">{'Comprendre les alliages' if fr else 'Understand alloys and grades'}</a></div>
  </div>
  <div class="price-feature-art" aria-hidden="true">
    <div class="pf-row pf-best"><span>A36 · 1/4"</span><b>{'meilleur' if fr else 'best'}</b></div>
    <div class="pf-row"><span>5052-H32 · 0.125"</span><i></i></div>
    <div class="pf-row pf-high"><span>304 2B · 16 ga</span><b>{'élevé' if fr else 'high'}</b></div>
    <div class="pf-row"><span>6061-T6 · 3/8"</span><i></i></div>
  </div>
</section>

<section class="home-sec">
  <div class="sec-head"><h2>{'Guides par logiciel' if fr else 'Guides by software'}</h2><a href="{hub_path('software', lang)}">{t['all_software']} →</a></div>
  <div class="tiles">{sw_tiles}</div>
</section>

<section class="home-sec">
  <div class="sec-head"><h2>{'Par procédé' if fr else 'By process'}</h2><a href="{hub_path('process', lang)}">{'Tous les procédés' if fr else 'All processes'} →</a></div>
  <div class="ptiles">{pr_tiles}</div>
</section>

<section class="home-sec">
  <div class="sec-head"><h2>{'Par où commencer' if fr else 'Where to start'}</h2><a href="{p['guides']}">{t['all_guides']} ({len(reg)}) →</a></div>
  <div class="paths-grid">{''.join(paths)}</div>
</section>

<section class="home-sec">
  <div class="sec-head"><h2>{'Guides essentiels' if fr else 'Essential guides'}</h2><a href="{hub_path('fundamentals', lang)}">{HUBS['fundamentals'][2 if fr else 3]} →</a></div>
  <div class="gcards">{''.join(card(g, lang) for g in feat)}</div>
</section>

<section class="home-split">
  <a class="split-card" href="{p['used']}">
    <p class="kicker">{t['used']}</p>
    <h2>{'Occasions CNC au Québec' if fr else 'Used CNC equipment in Quebec'}</h2>
    <p>{'Tables plasma, lasers, plieuses, fraiseuses : des centaines d’annonces publiques au Québec et au Canada, les super aubaines repérées et la liste de vérification avant d’acheter.' if fr else 'Plasma tables, lasers, press brakes, mills: hundreds of public listings in Quebec and Canada, the standout deals flagged, and the checklist to use before you buy.'}</p>
    <span class="more">{'Voir les annonces' if fr else 'Browse listings'} →</span>
  </a>
  <div class="split-card split-news">
    <p class="kicker">{t['news']}</p>
    <h2>{t['news_t']}</h2>
    <p>{t['news_d']}</p>
    {form_newsletter(lang)}
  </div>
</section>
</div>
"""

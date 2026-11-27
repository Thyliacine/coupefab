"""CoupeFab site kit: shared design (layout, mega-nav), guides library, home pages.

build.py wires this in with three lines (see the bottom of build.py):
    import sitekit
    layout = sitekit.layout
    PAGES = sitekit.extend_pages(PAGES, form_newsletter, PRIX_META)
and calls sitekit.write_assets() after writing pages. The price page (/prix/, prices/, js/prix.js)
is owned by prices/ and is only wrapped by the shared layout.
"""
from .layout import layout  # noqa: F401
from . import guides as _g
from .taxonomy import HUBS, HUB_ORDER, hub_path
from .home import home


def extend_pages(pages, form_newsletter, prix_meta=None):
    """Return PAGES with home/guides index replaced and the guides library + hubs added.

    Entries in `pages` whose path is regenerated here are replaced in place; everything else
    (price page, used equipment, newsletter, legal pages) is kept untouched.
    """
    gen = []
    gen.append(("/", "/en/", "fr", "CoupeFab — guides CNC, plasma, CAO/FAO et prix des tôles",
                "Guides d’atelier sourcés (Mastercam, SolidWorks, Fusion, SheetCam, plasma, laser, pliage) et comparateur des prix de tôle au Canada. En français d’abord.",
                home("fr", form_newsletter, prix_meta), False, False))
    gen.append(("/en/", "/", "en", "CoupeFab — CNC, plasma and CAD/CAM guides, plus sheet-metal prices",
                "Sourced shop-floor guides (Mastercam, SolidWorks, Fusion, SheetCam, plasma, laser, bending) and a Canadian sheet-metal price comparison. French-first.",
                home("en", form_newsletter, prix_meta), False, False))
    gen.append(("/guides/", "/en/guides/", "fr", "Guides CNC : CAO/FAO, plasma, laser, usinage et pliage — CoupeFab",
                "Bibliothèque de guides pratiques en français : Mastercam, SolidWorks, Fusion, SheetCam, G-code, avances et vitesses, kerf, pliage, dépannage.",
                _g.index_page("fr"), False, False))
    gen.append(("/en/guides/", "/guides/", "en", "CNC guides: CAD/CAM, plasma, laser, machining and bending — CoupeFab",
                "A library of practical guides: Mastercam, SolidWorks, Fusion, SheetCam, G-code, feeds and speeds, kerf, bending, troubleshooting.",
                _g.index_page("en"), False, False))
    for h in HUB_ORDER:
        fr_t, en_t = HUBS[h][2], HUBS[h][3]
        gen.append((hub_path(h, "fr"), hub_path(h, "en"), "fr", f"{fr_t} — Guides CoupeFab", HUBS[h][4], _g.hub_page(h, "fr"), False, False))
        gen.append((hub_path(h, "en"), hub_path(h, "fr"), "en", f"{en_t} — CoupeFab guides", HUBS[h][5], _g.hub_page(h, "en"), False, False))
    for g in _g.registry():
        for lang in ("fr", "en"):
            other = "en" if lang == "fr" else "fr"
            gen.append((g.url(lang), g.url(other), lang, f"{g.title(lang)} — CoupeFab", g.desc(lang),
                        _g.guide_page(g, lang, form_newsletter), False, False))
    from . import errorcodes as _ec
    if _ec.data()["codes"]:
        gen.append(("/codes-erreur/", "/en/error-codes/", "fr", "Codes d’erreur et alarmes CNC, plasma et laser (FANUC, Haas, Siemens, Hypertherm…) — CoupeFab",
                    "Chercher un code d’alarme : Haas, Siemens SINUMERIK, FANUC, Hypertherm Powermax et XPR, EDGE Connect, ESAB, Lincoln, Grbl. Sources officielles citées.",
                    _ec.page("fr"), False, False))
        gen.append(("/en/error-codes/", "/codes-erreur/", "en", "CNC, plasma and laser error codes and alarms (FANUC, Haas, Siemens, Hypertherm…) — CoupeFab",
                    "Look up an alarm code: Haas, Siemens SINUMERIK, FANUC, Hypertherm Powermax and XPR, EDGE Connect, ESAB, Lincoln, Grbl. Official sources cited.",
                    _ec.page("en"), False, False))
    gen_paths = {e[0] for e in gen}
    kept = [e for e in pages if e[0] not in gen_paths]
    # keep original order: home + guides first, then the rest of the site, then the library
    head = gen[:4]
    return head + kept + gen[4:]


def _not_found_page():
    """Bilingual 404 with search, hubs and popular guides (Vercel serves /404.html)."""
    from .layout import esc
    reg = {g.id: g for g in _g.registry()}
    pop = [reg[i] for i in ("plasma-cutting", "gcode", "sheetcam", "mastercam-2d", "bend-allowance", "feeds-speeds") if i in reg]
    cards = "".join(f'<a href="{g.url("fr")}"><strong>{esc(g.nav("fr"))}</strong><span>{esc(g.desc("fr")[:110].rsplit(" ", 1)[0])}…</span></a>' for g in pop)
    hubs = "".join(f'<a class="btn-ghost" href="{hub_path(h, "fr")}">{esc(HUBS[h][2])}</a>' for h in HUB_ORDER)
    body = f"""
<section class="nf">
  <p class="nf-code">ERREUR 404 · PAGE INTROUVABLE</p>
  <h1>Cette page n’existe pas (ou plus).</h1>
  <p class="lede">Le lien est peut-être ancien, ou l’adresse contient une faute. Cherchez un guide ou repartez d’une section. <span lang="en-CA">This page doesn’t exist. Try a search or the <a href="/en/">English home</a>.</span></p>
  <button class="nf-search" type="button" data-search-open><svg viewBox="0 0 24 24" aria-hidden="true" class="ico"><circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" stroke-width="2"/><path d="M20 20l-3.6-3.6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>Rechercher un guide (SheetCam, K-factor, scories…)<kbd style="margin-left:auto">/</kbd></button>
  <div class="nf-actions"><a class="btn" href="/">Accueil</a><a class="btn-ghost" href="/guides/">Tous les guides</a><a class="btn-ghost" href="/prix/">Prix des tôles</a></div>
  <h2 class="sec-h">Guides populaires</h2>
  <div class="nf-grid">{cards}</div>
  <h2 class="sec-h" style="margin-top:2rem">Sections</h2>
  <div class="nf-actions">{hubs}</div>
</section>"""
    return layout(lang="fr", title="Page introuvable — CoupeFab", description="Cette page n’existe pas sur CoupeFab.",
                  path="/404", alt="/404", body=body, noindex=True)


def write_assets():
    from pathlib import Path
    _g.write_search_indexes()
    import base64
    root = Path(__file__).resolve().parent.parent
    # binary assets (fonts, OG images, icons) are stored as base64 text under assets/bin/ and decoded here
    for b64 in sorted((root / "assets" / "bin").rglob("*.b64")):
        dest = root / b64.relative_to(root / "assets" / "bin").with_suffix("")
        data = base64.b64decode(b64.read_text())
        if not dest.exists() or dest.read_bytes() != data:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
    (root / "404.html").write_text(_not_found_page(), encoding="utf-8")

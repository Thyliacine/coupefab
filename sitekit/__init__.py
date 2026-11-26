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
    gen_paths = {e[0] for e in gen}
    kept = [e for e in pages if e[0] not in gen_paths]
    # keep original order: home + guides first, then the rest of the site, then the library
    head = gen[:4]
    return head + kept + gen[4:]


def write_assets():
    _g.write_search_indexes()

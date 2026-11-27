"""Tools hub: /outils/ (FR) and /en/tools/ (EN). Lists existing CoupeFab tools; does not modify them."""
from __future__ import annotations

import json
from pathlib import Path

from .layout import esc
from .taxonomy import PATHS, T

ROOT = Path(__file__).resolve().parent.parent
COOLANT = ROOT / "data" / "coolant-machines.json"

FR_PATH = "/outils/"
EN_PATH = "/en/tools/"
COOLANT_FR = "/outils/calculateur-liquide-de-coupe/"
COOLANT_EN = "/en/tools/coolant-calculator/"


def coolant_stats() -> tuple[int, int]:
    if not COOLANT.exists():
        return 0, 0
    try:
        d = json.loads(COOLANT.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return 0, 0
    return int(d.get("count") or 0), int(d.get("count_with_capacity") or 0)


def tools(lang: str) -> list[dict]:
    fr = lang == "fr"
    p = PATHS[lang]
    _n_all, n_cap = coolant_stats()
    cap = f"{n_cap}" if n_cap else ""
    if fr:
        cool_lede = (
            f"Concentré, eau, appoint et lecture du réfractomètre, avec {cap} capacités de réservoir sourcées (Haas, Makino, Okuma, Mazak…)."
            if cap else
            "Concentré, eau, appoint et lecture du réfractomètre pour le bassin de votre machine."
        )
        price_lede = "Prix publiés en $ CA / pi² et / lb, meilleur prix par spécification, et un calculateur de poids et de coût de pièce."
        codes_lede = "Recherchez un code Haas, FANUC, Siemens, Hypertherm, ESAB, Lincoln ou Grbl : signification et quoi vérifier, sources officielles."
    else:
        cool_lede = (
            f"Concentrate, water, top-up and refractometer reading, with {cap} sourced tank capacities (Haas, Makino, Okuma, Mazak…)."
            if cap else
            "Concentrate, water, top-up and refractometer reading for your machine’s sump."
        )
        price_lede = "Published prices in CAD per sq ft and per lb, the best price for each spec, and a part-weight and cost calculator."
        codes_lede = "Look up a Haas, FANUC, Siemens, Hypertherm, ESAB, Lincoln or Grbl code: meaning and what to check, from official sources."
    return [
        {
            "href": COOLANT_FR if fr else COOLANT_EN,
            "kicker": T[lang].get("tools", "Outils" if fr else "Tools"),
            "title": "Calculateur de liquide de coupe" if fr else "Coolant calculator",
            "lede": cool_lede,
            "cta": "Ouvrir le calculateur" if fr else "Open the calculator",
            "featured": True,
        },
        {
            "href": p["prices"],
            "kicker": T[lang]["prices"],
            "title": "Comparateur de prix des tôles" if fr else "Sheet-price comparison",
            "lede": price_lede,
            "cta": T[lang]["prices_cta_b"],
            "featured": False,
        },
        {
            "href": "/codes-erreur/" if fr else "/en/error-codes/",
            "kicker": "Dépannage" if fr else "Troubleshooting",
            "title": "Codes d’erreur et alarmes" if fr else "Error codes and alarms",
            "lede": codes_lede,
            "cta": "Chercher un code" if fr else "Look up a code",
            "featured": False,
        },
    ]


def card_html(t: dict, featured: bool = False) -> str:
    cls = "tool-card tool-card-lead" if featured or t.get("featured") else "tool-card"
    arrow = "\u2192"
    return (
        f'<a class="{cls}" href="{esc(t["href"])}">'
        f'<p class="kicker">{esc(t["kicker"])}</p>'
        f'<h2>{esc(t["title"])}</h2>'
        f'<p>{esc(t["lede"])}</p>'
        f'<span class="more">{esc(t["cta"])} {arrow}</span>'
        f"</a>"
    )


def home_card(lang: str) -> str:
    """Featured homepage card for the coolant calculator, plus a link to the tools hub."""
    fr = lang == "fr"
    items = tools(lang)
    if not items:
        return ""
    hub = PATHS[lang].get("tools", FR_PATH if fr else EN_PATH)
    all_lab = T[lang].get("all_tools", "Tous les outils" if fr else "All tools")
    arrow = "\u2192"
    return (
        f'<section class="home-tool" aria-labelledby="home-tool-title">'
        f"{card_html(items[0], True)}"
        f'<p class="home-tool-more"><a href="{hub}">{all_lab} {arrow}</a></p>'
        f"</section>"
    )


def hub_body(lang: str) -> str:
    fr = lang == "fr"
    cards = "".join(card_html(t) for t in tools(lang))
    lede = (
        "Calculateurs et comparateurs pour l’atelier : liquide de coupe, prix des tôles, codes d’erreur. Gratuit, sans compte, sourcé."
        if fr else
        "Shop calculators and comparators: coolant mix, sheet prices, error codes. Free, no account, sourced."
    )
    title = "Outils d’atelier CoupeFab" if fr else "CoupeFab shop tools"
    return (
        f'<div class="page tools-hub">'
        f'<header class="page-head">'
        f'<p class="kicker">{T[lang].get("tools", "Outils" if fr else "Tools")}</p>'
        f"<h1>{title}</h1>"
        f'<p class="lede">{lede}</p>'
        f"</header>"
        f'<div class="tool-grid">{cards}</div>'
        f"</div>"
    )


def pages():
    return [
        (FR_PATH, EN_PATH, "fr",
         "Outils d’atelier — calculateur de liquide de coupe, prix des tôles, codes d’erreur — CoupeFab",
         "Le calculateur de liquide de coupe (mélange, appoint, réfractomètre), le comparateur de prix des tôles et la recherche de codes d’erreur.",
         hub_body("fr"), False, False),
        (EN_PATH, FR_PATH, "en",
         "Shop tools — coolant calculator, sheet prices, error codes — CoupeFab",
         "The coolant calculator (mix, top-up, refractometer), the sheet-price comparison, and error-code lookup.",
         hub_body("en"), False, False),
    ]

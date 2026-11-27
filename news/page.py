"""Homepage hot-news band and the paginated /nouvelles/ (EN: /en/news/) page."""
from __future__ import annotations

import json
from pathlib import Path

from sitekit.layout import ASSET_V, esc
from sitekit.taxonomy import PATHS, T

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "news" / "latest.json"

TOPICS = [
    ("cnc", "CNC", "CNC"),
    ("plasma", "Plasma", "Plasma"),
    ("laser", "Laser", "Laser"),
    ("usinage", "Usinage", "Machining"),
    ("tolerie", "Tôlerie", "Sheet metal"),
]
TOPIC_LABEL = {k: (fr, en) for k, fr, en in TOPICS}


def load() -> dict:
    if not DATA.exists():
        return {"generated": "", "featured_ids": [], "items": []}
    try:
        return json.loads(DATA.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"generated": "", "featured_ids": [], "items": []}


def _date_label(iso: str, fr: bool) -> str:
    parts = (iso or "")[:10].split("-")
    if len(parts) != 3:
        return iso or ""
    y, m, d = parts
    months_fr = "janvier février mars avril mai juin juillet août septembre octobre novembre décembre".split()
    months_en = "January February March April May June July August September October November December".split()
    try:
        mi = int(m) - 1
        di = int(d)
    except ValueError:
        return iso
    if fr:
        return f"{di} {months_fr[mi]} {y}"
    return f"{months_en[mi]} {di}, {y}"


def _item_href(it: dict, fr: bool) -> str:
    if fr:
        return it.get("url") or "#"
    return it.get("url_en") or it.get("url") or "#"


def item_html(it: dict, fr: bool) -> str:
    title = it.get("title_fr" if fr else "title_en") or it.get("title_fr") or ""
    summary = it.get("summary_fr" if fr else "summary_en") or ""
    topic = it.get("topic") or ""
    lab = TOPIC_LABEL.get(topic, (topic, topic))
    tag = lab[0] if fr else lab[1]
    href = esc(_item_href(it, fr))
    ext = ' target="_blank" rel="noopener noreferrer"' if href.startswith("http") else ""
    sum_html = f'<span class="hn-sum">{esc(summary)}</span>' if summary else ""
    return (
        f'<li class="hn-item" data-topic="{esc(topic)}" data-kind="{esc(it.get("kind") or "")}">'
        f'<a href="{href}"{ext}>'
        f'<span class="hn-meta"><time datetime="{esc((it.get("date") or "")[:10])}">{esc(_date_label(it.get("date") or "", fr))}</time>'
        f'<span class="hn-tag">{esc(tag)}</span></span>'
        f'<strong class="hn-title">{esc(title)}</strong>'
        f"{sum_html}"
        f"</a></li>"
    )


def chips_html(fr: bool) -> str:
    bits = [
        f'<button type="button" class="hn-chip is-on" data-topic="" aria-pressed="true">{"Tout" if fr else "All"}</button>'
    ]
    for key, lab_fr, lab_en in TOPICS:
        bits.append(
            f'<button type="button" class="hn-chip" data-topic="{key}" aria-pressed="false">{lab_fr if fr else lab_en}</button>'
        )
    label = "Filtrer par sujet" if fr else "Filter by topic"
    return f'<div class="hn-chips" role="group" aria-label="{label}">{"".join(bits)}</div>'


def featured_items(data: dict | None = None) -> list[dict]:
    data = data or load()
    items = data.get("items") or []
    by_id = {it.get("id"): it for it in items}
    featured = [by_id[i] for i in (data.get("featured_ids") or []) if i in by_id]
    if not featured:
        featured = items[:8]
    return featured[:8]


def home_section(lang: str) -> str:
    fr = lang == "fr"
    items = featured_items()
    if not items:
        return ""
    p = PATHS[lang]
    lis = "".join(item_html(it, fr) for it in items)
    more = p.get("headlines", "/nouvelles/" if fr else "/en/news/")
    arrow = "\u2192"
    title = T[lang].get("hot_news", "Nouvelles chaudes" if fr else "Hot news")
    all_lab = T[lang].get("all_news", "Voir toutes les nouvelles" if fr else "See all news")
    return (
        f'<section class="home-hot" id="nouvelles-chaudes" data-hot-news="home" data-lang="{"fr" if fr else "en"}">'
        f'<div class="sec-head"><h2>{title}</h2><a href="{more}">{all_lab} {arrow}</a></div>'
        f"{chips_html(fr)}"
        f'<ul class="hn-list">{lis}</ul>'
        f"</section>"
    )


def index_body(lang: str) -> str:
    fr = lang == "fr"
    data = load()
    items = data.get("items") or []
    p = PATHS[lang]
    lis = "".join(item_html(it, fr) for it in items)
    gen = (data.get("generated") or "")[:10]
    note = ""
    if gen:
        sourced = (
            "Seules des nouvelles sourcées, avec lien et date, sont publiées ici."
            if fr else
            "Only sourced items with a link and a date appear here."
        )
        note = f'<p class="hn-note">{"Relevé du" if fr else "Survey of"} {_date_label(gen, fr)}. {sourced}</p>'
    empty = (
        "" if items else
        f'<p class="hn-empty">{"Aucune nouvelle sourcée pour le moment." if fr else "No sourced news items at the moment."}</p>'
    )
    lede = (
        "Occasions récemment relevées et mise à jour des prix publiés, classées par sujet (CNC, plasma, laser, usinage, tôlerie). Chaque item renvoie à sa source."
        if fr else
        "Recently surveyed used-equipment listings and the published-price update, tagged by topic (CNC, plasma, laser, machining, sheet metal). Every item links to its source."
    )
    arrow = "\u2192"
    return (
        f'<div class="page hn-page" data-hot-news="page" data-lang="{"fr" if fr else "en"}">'
        f'<header class="page-head">'
        f'<p class="kicker">{T[lang].get("headlines", "Nouvelles" if fr else "News")}</p>'
        f'<h1>{T[lang].get("hot_news", "Nouvelles chaudes" if fr else "Hot news")}</h1>'
        f'<p class="lede">{lede}</p>'
        f"</header>"
        f"{chips_html(fr)}{note}"
        f'<ul class="hn-list" id="hn-list">{lis}</ul>'
        f"{empty}"
        f'<nav class="cf-pager" id="hn-pager" hidden></nav>'
        f'<p class="hn-follow"><a href="{p["news"]}">{T[lang]["news"]} {arrow}</a></p>'
        f"</div>"
    )


def pages():
    return [
        ("/nouvelles/", "/en/news/", "fr",
         "Nouvelles chaudes — CNC, plasma, laser, usinage, tôlerie — CoupeFab",
         "Occasions récemment relevées et mise à jour des prix des tôles, avec source, date et filtre par sujet.",
         index_body("fr"), False, False),
        ("/en/news/", "/nouvelles/", "en",
         "Hot news — CNC, plasma, laser, machining, sheet metal — CoupeFab",
         "Recently surveyed used-equipment listings and the sheet-price update, with source, date and topic filters.",
         index_body("en"), False, False),
    ]

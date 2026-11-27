"""CoupeFab revenue features, dormant behind config/monetization.json (all false by default).

    featured_suppliers  « En vedette / Featured » block (paid spots, labelled « Commandité ») on
                        /fournisseurs/, /prix/, /pieces/, /outillage/ (+ EN). Status comes from payment
                        (data/revenue/featured.json, written by the payment hook) — see revenue/featured.py.
    affiliate_links     "Where to buy" affiliate slots from config/affiliate-links.json (empty url = hidden),
                        rel="sponsored nofollow", disclosure line, disclosure page + footer wording updated.
    digest_sponsor      one sponsor block per price-digest issue (scripts/digest.py, config/sponsors.json).
    quote_requests      /soumission/ + /en/quote/ form -> api/quote-request.js; footer link + CTA.
    advertise_page      /annoncer/ + /en/advertise/ (options, pricing marked TBD).

With a flag off, its pages are still generated so Michaël can preview them, but noindex, left out
of the sitemap and linked from nowhere; every other page is byte-for-byte what it was.
Build hooks used by build.py: hidden_paths(), page_entries(), inject(), postprocess().
Set COUPEFAB_REVENUE_DIR=config/demo to build with the demo config (all flags on, sample data).
"""
from __future__ import annotations

import html as _html
import json
import os
import re
from pathlib import Path

from . import featured as _feat
from . import routing as _route

ROOT = Path(__file__).resolve().parent.parent
FLAGS = ("featured_suppliers", "affiliate_links", "digest_sponsor", "quote_requests", "advertise_page")
P = {
    "advertise": ("/annoncer/", "/en/advertise/"),
    "quote": ("/soumission/", "/en/quote/"),
    "disc": ("/divulgation/", "/en/affiliate-disclosure/"),
}


def _dir() -> Path:
    d = os.environ.get("COUPEFAB_REVENUE_DIR")
    return (ROOT / d) if d and not os.path.isabs(d) else Path(d) if d else ROOT / "config"


def _json(name: str, fallback: Path | None = None) -> dict:
    p = _dir() / name
    if not p.exists() and fallback is not None:
        p = fallback
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def flags() -> dict:
    cfg = _json("monetization.json")
    return {k: bool(cfg.get(k, False)) for k in FLAGS}


def on(flag: str) -> bool:
    return flags().get(flag, False)


def featured_data() -> dict:
    return _json("featured.json", ROOT / "data" / "revenue" / "featured.json")


def affiliate_links() -> list[dict]:
    return [l for l in _json("affiliate-links.json").get("links", []) if str(l.get("url", "")).startswith("https://")]


def sponsors() -> list[dict]:
    return _json("sponsors.json").get("sponsors", [])


def esc(s) -> str:
    return _html.escape(str(s or ""), quote=True)


def ver(rel: str) -> str:
    import hashlib
    return hashlib.sha1((ROOT / rel).read_bytes()).hexdigest()[:8]


def css() -> str:
    return f'<link rel="stylesheet" href="/css/revenue.css?v={ver("css/revenue.css")}">'


# ---------------------------------------------------------------- hidden pages
def hidden_paths() -> set[str]:
    """Generated but not public (noindex, not in sitemap): pages whose flag is off."""
    f, out = flags(), set()
    if not f["advertise_page"]:
        out.update(P["advertise"])
    if not f["quote_requests"]:
        out.update(P["quote"])
    return out


def page_entries() -> list[tuple]:
    from . import pages
    return pages.entries()


# ---------------------------------------------------------------- blocks
def featured_block(path: str, lang: str) -> str:
    cat = _feat.category_for_path(path)
    if not cat or not on("featured_suppliers"):
        return ""
    rows = _feat.live_for(featured_data(), cat)
    if not rows:
        return ""
    fr = lang == "fr"
    L = (lambda a, b: a if fr else b)
    tiers = featured_data().get("tiers", {})
    cards = []
    for s in rows:
        logo = (f'<img class="rv-logo" src="{esc(s["logo"])}" alt="" width="120" height="40" loading="lazy">' if s.get("logo") else
                f'<span class="rv-logo rv-logo-txt" aria-hidden="true">{esc(s["name"][:2].upper())}</span>')
        tier = tiers.get(s.get("tier", "standard"), {}).get(lang, "")
        cards.append(
            f'<li class="rv-card{" rv-plus" if s.get("tier") == "plus" else ""}">{logo}<div class="rv-body">'
            f'<p class="rv-name"><strong>{esc(s["name"])}</strong> <span class="rv-tag">{L("Commandité", "Sponsored")}</span></p>'
            f'<p class="rv-blurb">{esc(s.get("blurb_fr" if fr else "blurb_en") or s.get("blurb_fr", ""))}</p>'
            f'<a class="rv-link" href="{esc(s["url"])}" rel="sponsored noopener" target="_blank">{L("Visiter le site", "Visit website")} ↗<span class="vh"> — {esc(s["name"])} ({esc(tier)})</span></a>'
            f"</div></li>")
    more = (f' <a href="{P["advertise"][0 if fr else 1]}">{L("Annoncer ici", "Advertise here")} →</a>' if on("advertise_page") else "")
    return (f'{css()}<section class="rv-featured" aria-labelledby="rv-feat-h-{lang}">'
            f'<div class="rv-head"><h2 id="rv-feat-h-{lang}">{L("En vedette", "Featured")}</h2>'
            f'<span class="rv-tag">{L("Commandité", "Sponsored")}</span></div>'
            f'<ul class="rv-grid">{"".join(cards)}</ul>'
            f'<p class="rv-note">{L("Espaces payés par les fournisseurs. Le reste de la page est gratuit, sans ordre de préférence, et les prix ne sont jamais modifiés.", "Spots paid for by suppliers. The rest of the page is free, in no order of preference, and prices are never changed.")}'
            f' <a href="{P["disc"][0 if fr else 1]}">{L("Divulgation", "Disclosure")}</a>.{more}</p></section>')


def affiliate_a(link: dict, lang: str) -> str:
    """Helper: one affiliate link, always rel="sponsored nofollow" and visibly marked."""
    fr = lang == "fr"
    label = link.get("label_fr" if fr else "label_en") or link.get("label_fr", "")
    merch = f' <span class="rv-merchant">{esc(link["merchant"])}</span>' if link.get("merchant") else ""
    return (f'<a class="rv-aff" href="{esc(link["url"])}" rel="sponsored nofollow noopener" target="_blank">{esc(label)} ↗</a>{merch}'
            f' <span class="rv-tag rv-tag-aff">{"lien affilié" if fr else "affiliate link"}</span>')


def disclosure_line(lang: str) -> str:
    fr = lang == "fr"
    return (f'<p class="rv-disc">{"Liens affiliés : si vous achetez par ces liens, CoupeFab peut recevoir une commission, sans coût pour vous. Ça ne change ni les prix affichés ni l’ordre des résultats." if fr else "Affiliate links: if you buy through them, CoupeFab may earn a commission at no cost to you. It never changes the prices shown or the order of results."}'
            f' <a href="{P["disc"][0 if fr else 1]}">{"Divulgation" if fr else "Disclosure"}</a>.</p>')


def affiliate_block(path: str, lang: str) -> str:
    if not on("affiliate_links"):
        return ""
    links = [l for l in affiliate_links() if any(path == pg for pg in l.get("pages", []))]
    if not links:
        return ""
    fr = lang == "fr"
    items = "".join(f"<li>{affiliate_a(l, lang)}</li>" for l in links)
    return (f'{css()}<section class="rv-affiliate" aria-labelledby="rv-aff-h-{lang}"><h2 id="rv-aff-h-{lang}">{"Où acheter" if fr else "Where to buy"}</h2>'
            f'<ul class="rv-aff-list">{items}</ul>{disclosure_line(lang)}</section>')


def quote_cta(path: str, lang: str) -> str:
    if not on("quote_requests") or path not in ("/fournisseurs/", "/en/suppliers/", "/pieces/", "/en/parts/", "/outillage/", "/en/tooling/"):
        return ""
    fr = lang == "fr"
    return (f'{css()}<aside class="rv-cta"><div><strong>{"Besoin d’une pièce coupée, pliée ou usinée?" if fr else "Need a part cut, bent or machined?"}</strong>'
            f'<span>{"Décrivez la job une fois; on la transmet à des ateliers du Québec qui font ce procédé dans votre région." if fr else "Describe the job once; we pass it to Quebec shops that do that process in your region."}</span></div>'
            f'<a class="btn" href="{P["quote"][0 if fr else 1]}">{"Demander une soumission" if fr else "Request a quote"}</a></aside>')


def disclosure_extra(lang: str) -> str:
    f = flags()
    if not (f["affiliate_links"] or f["featured_suppliers"] or f["digest_sponsor"]):
        return ""
    fr = lang == "fr"
    L = (lambda a, b: a if fr else b)
    parts = [f'{css()}<section class="rv-disc-page"><p class="pill pill-draft">{L("Brouillon — à réviser par Michaël", "Draft — to be reviewed by Michaël")}</p>']
    if f["affiliate_links"]:
        parts.append(L("<h2>Liens affiliés</h2><p>Certaines pages (pièces, outillage) contiennent des liens affiliés, marqués « lien affilié ». Si vous achetez par ces liens, CoupeFab peut recevoir une commission, sans coût supplémentaire pour vous. Les liens affiliés n’influencent jamais les prix du comparateur, l’ordre des résultats ni le contenu des guides. Ils portent l’attribut rel=\"sponsored nofollow\".</p>",
                       "<h2>Affiliate links</h2><p>Some pages (parts, tooling) contain affiliate links, marked “affiliate link”. If you buy through them, CoupeFab may earn a commission at no extra cost to you. Affiliate links never affect price-tool prices, the order of results or guide content. They carry rel=\"sponsored nofollow\".</p>"))
    if f["featured_suppliers"]:
        parts.append(L("<h2>Fournisseurs en vedette</h2><p>Le bloc « En vedette », marqué « Commandité », est payé par les fournisseurs qui y figurent, pour une période précise. Il est séparé du répertoire, qui reste gratuit pour tous et sans ordre de préférence. Un fournisseur en vedette n’obtient aucun traitement de faveur dans le comparateur de prix.</p>",
                       "<h2>Featured suppliers</h2><p>The “Featured” block, marked “Sponsored”, is paid for by the suppliers shown, for a set period. It is kept apart from the directory, which stays free for everyone and in no order of preference. A featured supplier gets no special treatment in the price tool.</p>"))
    if f["digest_sponsor"]:
        parts.append(L("<h2>Commandite de l’infolettre</h2><p>Chaque numéro de l’infolettre peut contenir un seul encadré « Commandité ». Le commanditaire ne choisit ni ne relit le reste du contenu.</p>",
                       "<h2>Newsletter sponsor</h2><p>Each newsletter issue may carry one “Sponsored” box. The sponsor neither chooses nor reviews the rest of the content.</p>"))
    parts.append("</section>")
    return "".join(parts)


def _after_hero(body: str, block: str) -> str:
    h = body.find("<h1")
    e = body.find("</section>", h) if h >= 0 else -1
    if e < 0:
        return block + body
    e += len("</section>")
    return body[:e] + block + body[e:]


def inject(path: str, lang: str, body: str) -> str:
    """Add revenue blocks to an existing page body. Returns body unchanged when every flag is off."""
    if not any(flags().values()):
        return body
    top = featured_block(path, lang) + quote_cta(path, lang)
    if top:
        body = _after_hero(body, top)
    aff = affiliate_block(path, lang)
    if aff:
        body = body + aff
    if path in P["disc"]:
        extra = disclosure_extra(lang)
        if extra:
            body = _after_hero(body, extra) if "<h1" in body else extra + body
    return body


# footer / home / page sentences that stop being true once a paid feature is on
_PAID_SWAPS = [
    ("Aucun lien d’affiliation ni publicité payante; la mention « Partenaire » de SMF Mécanique n’est pas rémunérée (voir la divulgation).",
     "Certains liens et espaces sont affiliés ou commandités, toujours identifiés (voir la divulgation); la mention « Partenaire » de SMF Mécanique n’est pas rémunérée."),
    ("No affiliate links or paid ads; the SMF Mécanique “Partner” label is unpaid (see the disclosure).",
     "Some links and spots are affiliate or sponsored, always labelled (see the disclosure); the SMF Mécanique “Partner” label is unpaid."),
    ("Divulgation (aucune affiliation, partenaire)", "Divulgation (affiliations, commandites, partenaire)"),
    ("Disclosure (no affiliates, partner)", "Disclosure (affiliates, sponsors, partner)"),
]
_AFF_SWAPS = [
    ("<li><b>0</b><span>lien d’affiliation, zéro chiffre inventé</span></li>", "<li><b>0</b><span>chiffre inventé, liens affiliés toujours identifiés</span></li>"),
    ("<li><b>0</b><span>affiliate links, zero invented numbers</span></li>", "<li><b>0</b><span>invented numbers, affiliate links always labelled</span></li>"),
    (" Aucun lien d’affiliation sur cette page.", " Les liens affiliés éventuels sont identifiés."),
    (" No affiliate links on this page.", " Any affiliate links are labelled."),
]


def postprocess(path: str, lang: str, page_html: str) -> str:
    """Whole-page tweaks (footer wording, footer links). Identity when every flag is off."""
    f = flags()
    if not any(f.values()):
        return page_html
    if f["affiliate_links"] or f["featured_suppliers"] or f["digest_sponsor"]:
        for a, b in _PAID_SWAPS:
            page_html = page_html.replace(a, b)
    if f["affiliate_links"] and affiliate_links():
        for a, b in _AFF_SWAPS:
            page_html = page_html.replace(a, b)
    fr = lang == "fr"
    extra = ""
    if f["quote_requests"]:
        extra += f'<li><a href="{P["quote"][0 if fr else 1]}">{"Demander une soumission" if fr else "Request a quote"}</a></li>'
    if f["advertise_page"]:
        extra += f'<li><a href="{P["advertise"][0 if fr else 1]}">{"Annoncer sur CoupeFab" if fr else "Advertise on CoupeFab"}</a></li>'
    if extra:
        sup = '<li><a href="/fournisseurs/">Fournisseurs</a></li>' if fr else '<li><a href="/en/suppliers/">Suppliers</a></li>'
        i = page_html.rfind(sup)  # the footer copy (the header nav uses a different markup)
        if i >= 0:
            page_html = page_html[: i + len(sup)] + extra + page_html[i + len(sup):]
    return page_html

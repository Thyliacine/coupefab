"""Render /occasions/ and /en/used-equipment/ from data/used/listings.json."""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

from . import parse, score

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "used"
MONTHS_FR = ["janvier", "février", "mars", "avril", "mai", "juin",
             "juillet", "août", "septembre", "octobre", "novembre", "décembre"]


def esc(s) -> str:
    return (str(s if s is not None else "")
            .replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def ver(rel: str) -> int:
    p = ROOT / rel
    return p.stat().st_mtime_ns // 1000 if p.exists() else 0


def nfr(x, d=0) -> str:
    s = f"{x:,.{d}f}".replace(",", " ")
    return s.replace(".", ",") if d else s


def money(amount, fr: bool, currency="CAD") -> str:
    if amount is None:
        return "Sur demande" if fr else "On request"
    cad = (currency or "CAD").upper().startswith("CA")
    if fr:
        return f"{nfr(amount, 0)} {'$' if cad else 'US$'}"
    return f"${amount:,.0f}" + (" CAD" if cad else " USD")


def date_fr(iso: str | None) -> str:
    if not iso:
        return ""
    try:
        d = dt.date.fromisoformat(str(iso)[:10])
    except ValueError:
        return str(iso)
    return f"{d.day} {MONTHS_FR[d.month - 1]} {d.year}"


def date_en(iso: str | None) -> str:
    if not iso:
        return ""
    try:
        d = dt.date.fromisoformat(str(iso)[:10])
    except ValueError:
        return str(iso)
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]
    return f"{months[d.month - 1]} {d.day}, {d.year}"


def load():
    path = DATA / "listings.json"
    if not path.exists():
        return {"listings": [], "fx": {}, "generated": None, "msrp_count": 0, "method": {}, "sources": []}
    return json.loads(path.read_text())


PUBLIC_KEYS = (
    "id", "title", "category", "make", "model", "year", "hours", "price", "currency",
    "price_cad", "price_type", "location", "city", "province", "distance_km",
    "seller", "source_id", "source_name", "url", "photo_url", "first_seen",
    "last_seen", "status", "badge", "badge_reason_fr", "badge_reason_en",
    "pct_off_msrp", "pct_vs_used_median", "n_comps", "msrp_cad", "msrp_source_url",
    "msrp_source_url_2", "msrp_kind", "msrp_date", "days_on_market", "price_dropped",
    "drop_pct", "condition_new", "size_class",
)


def public_row(it: dict) -> dict:
    return {k: it.get(k) for k in PUBLIC_KEYS}


def deal_rank(badge) -> int:
    return {"super": 0, "good": 1, "market": 2, "high": 3}.get(badge or "", 9)


def off_label(pct, fr) -> str:
    if pct is None:
        return ""
    n = nfr(abs(pct), 0) if fr else f"{abs(pct):.0f}"
    if fr:
        return f"{n} % sous le prix neuf" if pct >= 0 else f"{n} % au-dessus du prix neuf"
    return f"{n}% off new" if pct >= 0 else f"{n}% above new"


def card_html(it: dict, fr: bool) -> str:
    badge = it.get("badge")
    reason = it.get("badge_reason_fr") if fr else it.get("badge_reason_en")
    pill = ""
    if badge:
        label = (score.BADGE_FR if fr else score.BADGE_EN)[badge]
        pill = (f'<span class="oc-tier oc-t-{esc(badge)}" title="{esc(reason)}" '
                f'data-tip="{esc(reason)}">{esc(label)}</span>')
    dropped = ""
    if it.get("price_dropped") and it.get("drop_pct") is not None:
        n = nfr(it["drop_pct"], 0) if fr else f"{it['drop_pct']:.0f}"
        dropped = f'<span class="oc-drop">-{n} %</span>'
    days = it.get("days_on_market")
    if days is None:
        days_txt = ""
    elif days == 0:
        days_txt = "Repérée aujourd’hui" if fr else "Spotted today"
    elif days == 1:
        days_txt = "Repérée hier" if fr else "Spotted yesterday"
    else:
        days_txt = (f"En ligne depuis {days} jours" if fr else f"Listed {days} days ago")
    loc = it.get("location") or ""
    if it.get("distance_km") is not None:
        dk = nfr(it["distance_km"], 0) if fr else f"{it['distance_km']:.0f}"
        loc = f"{loc} · {dk} km"
    year = f" · {it['year']}" if it.get("year") else ""
    hours = ""
    if it.get("hours") is not None:
        hours = f" · {nfr(it['hours'], 0)} h" if fr else f" · {it['hours']:,} h"
    labs = parse.CATEGORIES.get(it.get("category") or "other", parse.CATEGORIES["other"])
    cat_lab = labs[0] if fr else labs[1]
    status_pill = ""
    if it.get("status") == "sold":
        status_pill = f'<span class="oc-tier oc-t-sold">{"Vendu" if fr else "Sold"}</span>'
    elif it.get("status") == "stale":
        status_pill = f'<span class="oc-tier oc-t-stale">{"Périmée" if fr else "Stale"}</span>'
    photo = it.get("photo_url") or ""
    if photo:
        img = (f'<img src="{esc(photo)}" alt="" loading="lazy" decoding="async" '
               f'referrerpolicy="no-referrer" onerror="this.removeAttribute(\'src\');this.classList.add(\'is-fallback\')">')
    else:
        img = '<span class="oc-ph" aria-hidden="true"></span>'
    msrp_line = ""
    if it.get("msrp_cad"):
        src = it.get("msrp_source_url") or ""
        src2 = it.get("msrp_source_url_2") or ""
        when = date_fr(it.get("msrp_date")) if fr else date_en(it.get("msrp_date"))
        estimated = (it.get("msrp_kind") or "official") == "estimated"
        if estimated:
            label = "Prix neuf estimé" if fr else "Estimated new price"
        else:
            label = "Prix neuf" if fr else "New price"
        def _cite(url, text):
            return f'<a href="{esc(url)}" rel="nofollow noopener" target="_blank">{esc(text)}</a>' if url else esc(text)
        cite = _cite(src, label)
        if src2:
            cite += " · " + _cite(src2, "source 2" if not fr else "source 2")
        extra = f" ({when})" if when else ""
        off = off_label(it.get("pct_off_msrp"), fr) if it.get("price_cad") else ""
        off_s = f" · {off}" if off else ""
        msrp_line = f'<p class="oc-msrp">{cite} {money(it["msrp_cad"], fr)}{extra}{off_s}</p>'
    if it.get("price_cad") or it.get("price"):
        price_lbl = money(it.get("price_cad") or it.get("price"), fr, it.get("currency") or "CAD")
    else:
        price_lbl = "Sur demande" if fr else "On request"
    typ_map = {
        "buy_now": ("Achat immédiat", "Buy now"),
        "auction": ("Enchère", "Auction"),
        "quote": ("Sur demande", "On request"),
        "asking": ("Prix affiché", "Asking"),
    }
    typ_lab = typ_map.get(it.get("price_type") or "", ("", ""))
    typ_s = f'<span class="oc-chip">{esc(typ_lab[0] if fr else typ_lab[1])}</span>' if typ_lab[0] else ""
    new_s = f'<span class="oc-chip">{"Neuf" if fr else "New"}</span>' if it.get("condition_new") else ""
    cta = "Voir l’annonce" if fr else "View listing"
    url = esc(it.get("url") or "#")
    dist = it.get("distance_km") if it.get("distance_km") is not None else ""
    price_d = it.get("price_cad") if it.get("price_cad") is not None else ""
    specs = []
    if it.get("year"):
        specs.append(f'<li><span class="vh">{"Année" if fr else "Year"} </span>{it["year"]}</li>')
    if it.get("hours") is not None:
        specs.append(f'<li>{esc(hours.strip(" ·"))}</li>')
    if loc:
        specs.append(f'<li class="oc-loc">{esc(loc)}</li>')
    spec_ul = f'<ul class="oc-specs">{"".join(specs)}</ul>' if specs else ""
    seller = esc(it.get("seller") or "")
    src_tag = f'<span class="oc-src">{seller}</span>' if seller else ""
    return (
        f'<article class="oc-card" data-id="{esc(it.get("id"))}" '
        f'data-cat="{esc(it.get("category") or "other")}" data-prov="{esc(it.get("province") or "")}" '
        f'data-dist="{dist}" data-price="{price_d}" data-year="{it.get("year") or ""}" '
        f'data-src="{esc(it.get("source_id") or "")}" data-badge="{esc(badge or "")}" '
        f'data-status="{esc(it.get("status") or "active")}" data-seen="{esc(it.get("last_seen") or "")}" '
        f'data-deal="{deal_rank(badge)}" data-dropped="{1 if it.get("price_dropped") else 0}">'
        f'<a class="oc-photo" href="{url}" rel="nofollow noopener" target="_blank" tabindex="-1" aria-hidden="true">{img}'
        f'<span class="oc-photo-tags">{pill}{status_pill}</span>{src_tag}</a>'
        f'<div class="oc-body"><header>'
        f'<p class="oc-k">{esc(cat_lab)}</p>'
        f'<h3><a href="{url}" rel="nofollow noopener" target="_blank">{esc(it.get("title"))}</a></h3>'
        f'</header>'
        f'<p class="oc-price"><b>{esc(price_lbl)}</b> {typ_s} {new_s} {dropped}</p>'
        f'{msrp_line}'
        f'{spec_ul}'
        f'<div class="oc-foot"><span class="oc-meta">{esc(days_txt)}</span>'
        f'<a class="oc-btn" href="{url}" rel="nofollow noopener" target="_blank">{esc(cta)} <span aria-hidden="true">↗</span></a></div>'
        f'</div></article>'
    )


def render(site="https://coupefab.vercel.app"):
    data = load()
    listings = data.get("listings") or []
    fx = data.get("fx") or {}
    gen = data.get("generated") or ""
    method = data.get("method") or {}
    sources = data.get("sources") or []

    active = [l for l in listings if l.get("status") == "active"]
    priced = [l for l in active if l.get("price_cad")]
    with_msrp = [l for l in active if l.get("msrp_cad")]
    supers = [l for l in active if l.get("badge") == "super"]
    src_ids = sorted({l.get("source_id") for l in active if l.get("source_id")})

    cats_present = []
    for cid, labs in parse.CATEGORIES.items():
        n = sum(1 for l in active if l.get("category") == cid)
        if n:
            cats_present.append((cid, labs[0], labs[1], n))

    def sort_key(l):
        pr = {"QC": 0, "ON": 1}.get(l.get("province") or "", 2)
        return (deal_rank(l.get("badge")), pr, l.get("price_cad") is None, l.get("price_cad") or 0)

    ordered = sorted(active, key=sort_key)
    rest = [l for l in listings if l.get("status") != "active"]

    dest = ROOT / "occasions" / "donnees.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps({
        "generated": gen, "fx": fx, "method": method,
        "listings": [public_row(l) for l in listings],
        "categories": {k: {"fr": v[0], "en": v[1]} for k, v in parse.CATEGORIES.items()},
        "badges": {"fr": score.BADGE_FR, "en": score.BADGE_EN},
    }, ensure_ascii=False, separators=(",", ":")))

    src_opts = sorted({(l.get("source_id"), l.get("source_name") or l.get("source_id"))
                       for l in active if l.get("source_id")})

    def page(fr: bool) -> str:
        def L(a, b):
            return a if fr else b

        tabs = [(None, L("Toutes", "All"), len(active))]
        tabs += [(c, (lf if fr else le), n) for c, lf, le, n in cats_present]
        tabs_html = []
        for i, (cid, lab, n) in enumerate(tabs):
            sel = "true" if i == 0 else "false"
            tb = 0 if i == 0 else -1
            tabs_html.append(
                f'<button type="button" role="tab" id="oc-tab-{esc(cid or "all")}" '
                f'aria-selected="{sel}" tabindex="{tb}" data-cat="{esc(cid or "")}">'
                f'{esc(lab)} <small>{n}</small></button>'
            )
        cards = "\n".join(card_html(l, fr) for l in ordered + rest)
        ca = {"QC", "ON", "BC", "AB", "SK", "MB", "NS", "NB", "PE", "NL", "YT", "NT", "NU"}
        deals = [l for l in ordered if l.get("badge") in ("super", "good") and l.get("price_cad")
                 and (l.get("province") or "") in ca][:5]
        deals_html = ""
        if deals:
            deals_html = (
                f'<section class="oc-deals" id="oc-deals">'
                f'<h2>{L("Meilleures aubaines en ce moment", "Best deals right now")}</h2>'
                f'<div class="oc-grid oc-grid-deals">{"".join(card_html(l, fr) for l in deals)}</div>'
                f'</section>'
            )
        src_html = "".join(
            f'<option value="{esc(sid)}">{esc(name)}</option>' for sid, name in src_opts if sid
        )
        stamp = date_fr(gen) if fr else date_en(gen)
        if fx.get("rate"):
            fx_txt = (f"1 USD = {nfr(fx['rate'], 4)} CAD" if fr
                      else f"1 USD = {fx['rate']:.4f} CAD")
            when = date_fr(fx.get("date")) if fr else date_en(fx.get("date"))
            if when:
                fx_txt += f" ({when})"
        else:
            fx_txt = ""
        lede = L(
            f"{len(active)} annonces publiques chez {len(src_ids)} sources, dont {len(priced)} avec un prix affiché"
            + (f" et {len(with_msrp)} comparées à un prix neuf documenté" if with_msrp else "")
            + ". Repérez une super aubaine et ouvrez l’annonce en un clic.",
            f"{len(active)} public listings from {len(src_ids)} sources, {len(priced)} with a published price"
            + (f" and {len(with_msrp)} matched to a documented new price" if with_msrp else "")
            + ". Spot a super deal and open the listing in one click.",
        )
        boot = "(function(){var a=document.getElementById('oc-app');if(a)a.classList.add('js');})();"
        return f"""<link rel="stylesheet" href="/css/occasions.css?v={ver('css/occasions.css')}">
<div class="oc" id="oc-app" data-lang="{L('fr','en')}">
<script>{boot}</script>
<section class="oc-hero">
  <div class="oc-hero-top">
    <div>
      <p class="oc-kicker">{L("Comparateur d’équipements d’occasion", "Used equipment deal tracker")} <span class="oc-beta">{L("bêta", "beta")}</span></p>
      <h1>{L("Occasions CNC et métaux au Québec", "Used CNC and metalworking equipment in Quebec")}</h1>
      <p class="oc-lede">{esc(lede)}</p>
    </div>
    <p class="oc-stamp" role="status"><span><b>{L("Mis à jour", "Updated")}</b> {esc(stamp or "—")}</span>
      <span>{L("Distance depuis Berthierville (QC)", "Distance from Berthierville, Quebec")}</span></p>
  </div>
</section>

<details class="oc-caveat">
  <summary><b>{L("CoupeFab n’est pas un courtier.", "CoupeFab is not a broker.")}</b> {L("Vérifiez toujours auprès du vendeur.", "Always confirm with the seller.")} <span class="oc-more">{L("Détails", "Details")}</span></summary>
  <p>{L("Les prix, la disponibilité et l’état changent sans préavis. Un prix « sur demande » n’est pas une offre. Les enchères excluent souvent la prime d’acheteur, le transport et les taxes (TPS/TVQ). Les prix en USD sont convertis au taux de la Banque du Canada lorsqu’il est disponible.",
     "Prices, availability and condition change without notice. A “price on request” is not an offer. Auction figures often exclude the buyer’s premium, freight and taxes (GST/QST). USD prices are converted at the Bank of Canada rate when available.")}
  {esc(fx_txt)}</p>
</details>

<button type="button" class="oc-filters-toggle" aria-expanded="false" aria-controls="oc-filters">{L("Filtres", "Filters")} <span class="oc-nf" data-nf></span></button>
<form class="oc-filters" id="oc-filters" role="search" aria-label="{L("Filtrer les annonces", "Filter listings")}" onsubmit="return false">
  <label class="oc-q"><span>{L("Rechercher", "Search")}</span>
    <input type="search" name="q" autocomplete="off" placeholder="{L("ex. Haas VF-2, plasma 5x10, plieuse", "e.g. Haas VF-2, 5x10 plasma, press brake")}"></label>
  <label><span>{L("Région", "Region")}</span>
    <select name="region">
      <option value="" selected>{L("Toutes", "All")}</option>
      <option value="ca">{L("Canada", "Canada")}</option>
      <option value="qc">{L("Québec seulement", "Quebec only")}</option>
      <option value="qc-on">{L("Québec et Ontario", "Quebec and Ontario")}</option>
      <option value="near150">{L("≤ 150 km de Berthierville", "Within 150 km of Berthierville")}</option>
      <option value="near300">{L("≤ 300 km de Berthierville", "Within 300 km of Berthierville")}</option>
    </select></label>
  <label><span>{L("Prix", "Price")}</span>
    <select name="price">
      <option value="">{L("Tous", "All")}</option>
      <option value="0-10000">{L("Moins de 10 000 $", "Under $10,000")}</option>
      <option value="10000-40000">10 000 – 40 000 $</option>
      <option value="40000-100000">40 000 – 100 000 $</option>
      <option value="100000-">{L("100 000 $ et plus", "$100,000 and up")}</option>
      <option value="quote">{L("Sur demande seulement", "On request only")}</option>
    </select></label>
  <label><span>{L("Année", "Year")}</span>
    <select name="year">
      <option value="">{L("Toutes", "All")}</option>
      <option value="2020-">2020 – 2026</option>
      <option value="2010-2019">2010 – 2019</option>
      <option value="2000-2009">2000 – 2009</option>
      <option value="-1999">{L("Avant 2000", "Before 2000")}</option>
    </select></label>
  <label><span>{L("Source", "Source")}</span>
    <select name="source"><option value="">{L("Toutes", "All")}</option>{src_html}</select></label>
  <label class="oc-check"><input type="checkbox" name="deals"> {L("Aubaines seulement", "Deals only")}</label>
  <button type="button" class="oc-reset" data-reset>{L("Réinitialiser", "Reset")}</button>
</form>

<nav class="oc-tabs" role="tablist" aria-label="{L("Catégories", "Categories")}">{"".join(tabs_html)}</nav>

{deals_html}

<div class="oc-results-head">
  <h2 class="oc-h2" id="oc-results-title">{L("Toutes les annonces", "All listings")}</h2>
  <p class="oc-count" id="oc-count" aria-live="polite"></p>
  <label class="oc-sort"><span>{L("Trier", "Sort")}</span>
    <select id="oc-sort">
      <option value="deal">{L("Meilleure aubaine", "Best deal")}</option>
      <option value="newest">{L("Plus récentes", "Newest")}</option>
      <option value="price-asc">{L("Prix croissant", "Price: low to high")}</option>
      <option value="price-desc">{L("Prix décroissant", "Price: high to low")}</option>
      <option value="near">{L("Plus proches", "Closest")}</option>
      <option value="year-desc">{L("Plus récentes (année)", "Newest year")}</option>
    </select>
  </label>
  <label class="oc-check"><input type="checkbox" name="showgone" form="oc-filters"> {L("Afficher vendues / périmées", "Show sold / stale")}</label>
</div>

<div class="oc-grid" id="oc-grid">{cards}</div>
<p class="oc-empty" id="oc-empty" hidden>{L("Aucune annonce ne correspond à ces filtres.", "No listings match these filters.")}</p>

{_method_html(fr, method, fx_txt, sources)}
{_checklist_html(fr)}
</div>
<script src="/js/occasions.js?v={ver('js/occasions.js')}" defer></script>"""

    meta = {
        "n_active": len(active), "n_priced": len(priced), "n_msrp": len(with_msrp),
        "n_sources": len(src_ids), "n_super": len(supers), "generated": gen,
    }
    return page(True), page(False), meta


def _src_li(s: dict) -> str:
    why = s.get("reason") or s.get("status")
    return (f'<li><a href="{esc(s.get("url"))}" rel="nofollow noopener" target="_blank">'
            f'{esc(s.get("name"))}</a> — {esc(why)}</li>')


def _method_html(fr: bool, method: dict, fx_txt: str, sources: list) -> str:
    added = [s for s in sources if s.get("status") in ("added", "quote-only")]
    blocked = [s for s in sources if s.get("status") == "blocked"]
    su = method.get("super_used_pct", 20)
    sm = method.get("super_msrp_pct", 50)
    tp = method.get("tier_pct", 10)
    gm = method.get("good_msrp_pct", 35)
    dep = int((method.get("depreciation") or 0.08) * 100)
    cap = method.get("dep_cap_years", 10)
    stale = method.get("stale_days", 14)
    added_ul = "".join(_src_li(s) for s in added) or ("<li>Aucune pour ce relevé.</li>" if fr else "<li>None in this survey.</li>")
    blocked_ul = "".join(_src_li(s) for s in blocked) or ("<li>Aucune bloquée pour ce relevé.</li>" if fr else "<li>None blocked in this survey.</li>")
    if fr:
        return f"""<details class="oc-details" id="oc-method">
  <summary>Comment nous notons les aubaines</summary>
  <p>Nous ne relions que des pages publiques. Pas d’aspiration derrière une connexion, pas de contournement de protection anti-robot. Si un prix n’est pas affiché sur la page, nous écrivons « sur demande » — même lorsqu’une API interne expose un montant.</p>
  <h3>Les étiquettes d’aubaine</h3>
  <ul class="oc-legend">
    <li><span class="oc-tier oc-t-super">Super aubaine</span> au moins {su} % sous la médiane usagée (au moins 2 comparables), ou au moins {sm} % sous un prix neuf documenté, ou les deux (≥ 45 % sous le neuf et ≥ 10 % sous la médiane).</li>
    <li><span class="oc-tier oc-t-good">Bonne affaire</span> au moins {tp} % sous la médiane, ou au moins {gm} % sous le neuf en l’absence de comparables.</li>
    <li><span class="oc-tier oc-t-market">Prix du marché</span> à ± {tp} % de la médiane, ou 20–35 % sous le neuf sans comparables.</li>
    <li><span class="oc-tier oc-t-high">Cher</span> au moins {tp} % au-dessus de la médiane, ou moins de 20 % sous le neuf sans comparables.</li>
  </ul>
  <p>Les comparables, dans l’ordre, dès qu’il y en a au moins deux autres avec un prix : (1) même marque et même modèle ; (2) même catégorie, même marque et même classe de taille ; (3) même catégorie et même classe de taille. Une table hobby n’est pas comparée à une table de production, ni une plieuse de 44 t à une de 200 t. Une machine neuve en inventaire n’entre pas dans la médiane usagée, et l’inverse. L’âge est ramené à l’année de l’annonce avec un facteur estimatif de {dep} % par an (plafond {cap} ans) — c’est une estimation CoupeFab, pas une expertise. Pointez ou touchez une étiquette pour voir le calcul (par ex. « 42 % sous le prix neuf, 18 % sous la médiane usagée »).</p>
  <p>Un prix neuf n’est affiché que s’il provient d’une page officielle du fabricant ou d’un concessionnaire autorisé (URL + date), ou, à défaut, d’une fourchette clairement étiquetée « Prix neuf estimé » appuyée par au moins deux sources de presse ou de concessionnaires. Nous n’inventons jamais ce chiffre. Un appareil usagé peut inclure des options que le prix de base n’inclut pas, ou l’inverse.</p>
  <p>Une baisse de prix est signalée lorsque le montant publié a diminué depuis notre premier relevé. Les jours en ligne sont comptés depuis ce premier relevé. Une annonce absente pendant {stale} jours est marquée périmée ; « vendu » ne l’est que si le vendeur l’indique.</p>
  <p>{esc(fx_txt)}</p>
  <h3>Sources lues</h3>
  <ul>{added_ul}</ul>
  <h3>Sources non lues</h3>
  <ul>{blocked_ul}</ul>
</details>"""
    return f"""<details class="oc-details" id="oc-method">
  <summary>How we score deals</summary>
  <p>We only link to public pages. No login walls, and no bypassing bot protection. If a price is not shown on the page, we write “on request” — even when an internal API exposes a number.</p>
  <h3>Badges</h3>
  <ul class="oc-legend">
    <li><span class="oc-tier oc-t-super">Super deal</span> at least {su}% below the used median (at least 2 comparables), or at least {sm}% off a documented new price, or both (≥ 45% off new and ≥ 10% below the median).</li>
    <li><span class="oc-tier oc-t-good">Good deal</span> at least {tp}% below the median, or at least {gm}% off new when there are no comparables.</li>
    <li><span class="oc-tier oc-t-market">Market price</span> within ±{tp}% of the median, or 20–35% off new with no comparables.</li>
    <li><span class="oc-tier oc-t-high">High</span> at least {tp}% above the median, or less than 20% off new with no comparables.</li>
  </ul>
  <p>Comparables, in order, once at least two other priced listings exist: (1) same make and model; (2) same category, make and size class; (3) same category and size class. A hobby table is not compared with a production table, nor a 44-ton brake with a 200-ton brake. New in-stock machines are not used as comparables for used listings, and the reverse. Age is brought to the listing’s year with an estimated {dep}% declining-balance factor per year (capped at {cap} years) — a CoupeFab estimate, not an appraisal. Hover or tap a badge to see the arithmetic (e.g. “42% off new, 18% below the used median”).</p>
  <p>A new-price figure is shown only from an official manufacturer or authorized-dealer page (URL + date), or, failing that, a clearly labelled “Estimated new price” backed by at least two dealer or press sources. We never invent that number. A used machine may include options the base price does not, or the reverse.</p>
  <p>A price-drop mark appears when the published figure has fallen since we first saw the listing. Days on market are counted from that first sighting. A listing missing for {stale} days is marked stale; “sold” is used only when the seller says so.</p>
  <p>{esc(fx_txt)}</p>
  <h3>Sources read</h3>
  <ul>{added_ul}</ul>
  <h3>Sources not read</h3>
  <ul>{blocked_ul}</ul>
</details>"""


def _checklist_html(fr: bool) -> str:
    if fr:
        items = [
            ("Enveloppe de l’atelier.", "Dimensions utiles contre portes, pont roulant et hauteur ; tension réelle (208 / 460 / 600 V) ; air comprimé et sécheur ; dépoussiéreur ou table à eau déjà en place."),
            ("Source et outils.", "Marque, modèle, intensité ou puissance, consommables, heures si elles existent, THC ou commande fonctionnels. Une « capacité » publicitaire n’est pas une qualité de production — demandez à voir couper ou usiner votre pièce typique."),
            ("Mécanique.", "Jeu des crémaillères ou vis, équerrage, état des rails, câbles, rouilles, fuites."),
            ("Contrôle et licences.", "Contrôleur, sauvegardes, logiciels CAM et leurs licences : ce qui est inclus, ce qui est à racheter."),
            ("Historique.", "Rétrofit (quand, par qui), disponibilité des pièces au Canada, documentation d’origine."),
            ("Essai.", "Voir la machine en marche. Mesurer une pièce étalon. Écouter les fins de course et les défauts."),
            ("Logistique et contrat.", "Vendu tel quel, démantèlement, transport, taxes (TPS/TVQ), délai. Un prix « sorti d’usine » sans grue ni déplacement n’est pas un prix rendu dans votre cour."),
        ]
        title, lead = "Liste de vérification (achat au Québec)", "Ce canevas d’atelier n’est pas une expertise. Vérifiez toujours sur place."
    else:
        items = [
            ("Shop envelope.", "Useful dimensions versus doors, crane and height; actual voltage (208 / 460 / 600 V); compressed air and dryer; dust collector or water table already in place."),
            ("Power source and tooling.", "Make, model, amperage or power, consumables, hours if given, working THC or control. An advertised “capacity” is not a production finish — ask to see your typical part cut or machined."),
            ("Mechanics.", "Backlash in racks or screws, squareness, rails, cables, rust, leaks."),
            ("Control and licences.", "Controller, backups, CAM software and licences: what is included, what must be bought again."),
            ("History.", "Retrofits (when, by whom), parts availability in Canada, original documentation."),
            ("Trial.", "See the machine run. Measure a test part. Listen for limit-switch and arc faults."),
            ("Logistics and contract.", "Sold as-is, dismantling, freight, taxes (GST/QST), availability. An “ex-works” price without a crane or a move is not a price in your yard."),
        ]
        title, lead = "Checklist (buying in Quebec)", "This is a shop-floor canvas, not an inspection. Always verify in person."
    lis = "".join(f"<li><strong>{esc(h)}</strong> {esc(b)}</li>" for h, b in items)
    return f"""<details class="oc-details" id="oc-checklist">
  <summary>{esc(title)}</summary>
  <p>{esc(lead)}</p>
  <ul class="oc-check-list">{lis}</ul>
</details>"""


def write_pages(site="https://coupefab.vercel.app"):
    """Write the two occasions pages using the shared sitekit layout, without rebuilding the rest of the site."""
    import sitekit
    fr, en, meta = render(site)
    pages = [
        ("/occasions/", "/en/used-equipment/", "fr",
         "Occasions CNC et métaux au Québec — comparateur d’aubaines — CoupeFab",
         "Annonces publiques de tables plasma, lasers, fraiseuses, tours et plieuses au Québec et au Canada, avec repérage des super aubaines et comparaison au prix neuf lorsqu’il est documenté.",
         fr),
        ("/en/used-equipment/", "/occasions/", "en",
         "Used CNC and metalworking equipment in Quebec — deal tracker — CoupeFab",
         "Public listings of plasma tables, lasers, mills, lathes and press brakes in Quebec and Canada, with Super deal badges and a comparison to documented new prices.",
         en),
    ]
    written = []
    for path, alt, lang, title, description, body in pages:
        rel = path.strip("/")
        dest = ROOT / rel / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(sitekit.layout(
            lang=lang, title=title, description=description, path=path, alt=alt,
            body=body, draft=False, article=False,
        ), encoding="utf-8")
        written.append(str(dest.relative_to(ROOT)))
    return written, meta

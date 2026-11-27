"""Render /pieces/ and /en/parts/ from data/parts/."""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "parts"
MONTHS_FR = ["janvier", "février", "mars", "avril", "mai", "juin",
             "juillet", "août", "septembre", "octobre", "novembre", "décembre"]


def esc(s) -> str:
    return (str(s if s is not None else "")
            .replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def ver(rel: str) -> int:
    p = ROOT / rel
    return p.stat().st_mtime_ns // 1000 if p.exists() else 0


def nfr(x, d=2) -> str:
    s = f"{x:,.{d}f}".replace(",", " ")
    return s.replace(".", ",")


def money(amount, fr: bool, currency="CAD") -> str:
    cad = (currency or "CAD").upper().startswith("CA")
    if fr:
        return f"{nfr(amount, 2)} {'$' if cad else 'US$'}"
    return f"${amount:,.2f}" + (" CAD" if cad else " USD")


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
    catalog = json.loads((DATA / "catalog.json").read_text(encoding="utf-8"))
    prices = json.loads((DATA / "prices.json").read_text(encoding="utf-8"))
    suppliers = json.loads((DATA / "suppliers.json").read_text(encoding="utf-8"))
    return catalog, prices, suppliers


def _opts(items, value_key, label_fn, all_label):
    html = [f'<option value="" selected>{esc(all_label)}</option>']
    for it in items:
        html.append(f'<option value="{esc(it[value_key])}">{esc(label_fn(it))}</option>')
    return "".join(html)


def _guide_html(g: dict, fr: bool) -> str:
    title = g["title_fr"] if fr else g["title_en"]
    what = g["what_fr"] if fr else g["what_en"]
    wear = g["wear_fr"] if fr else g["wear_en"]
    when = g["when_fr"] if fr else g["when_en"]
    srcs = "".join(
        f'<li><a href="{esc(s["url"])}" rel="noopener noreferrer">{esc(s["fr"] if fr else s["en"])}</a></li>'
        if s.get("url") else f'<li>{esc(s["fr"] if fr else s["en"])}</li>'
        for s in (g.get("sources") or [])
    )
    src_block = f'<p class="pc-src-h">{esc("Sources" if fr else "Sources")}</p><ul class="pc-src">{srcs}</ul>' if srcs else ""
    return f"""
<article class="pc-guide">
  <h3>{esc(title)}</h3>
  <p><b>{esc("À quoi ça sert" if fr else "What it is")}</b> — {esc(what)}</p>
  <p><b>{esc("Signes d’usure" if fr else "Wear signs")}</b> — {esc(wear)}</p>
  <p><b>{esc("Quand remplacer" if fr else "When to replace")}</b> — {esc(when)}</p>
  {src_block}
</article>"""


def render(site="https://coupefab.vercel.app"):
    catalog, prices, suppliers = load()
    items = prices.get("items") or []
    shops = suppliers.get("suppliers") or []
    fetched = prices.get("fetched") or catalog.get("updated")
    cats = catalog["categories"]
    machines = catalog["machines"]
    cat_by_id = {c["id"]: c for c in cats}
    mac_by_id = {m["id"]: m for m in machines}

    dest = ROOT / "pieces" / "donnees.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps({
        "fetched": fetched,
        "timezone": prices.get("timezone") or "America/Toronto",
        "items": items,
        "suppliers": shops,
        "categories": {c["id"]: {"fr": c["fr"], "en": c["en"], "machine": c.get("machine") or ""} for c in cats},
        "machines": {m["id"]: {"fr": m["fr"], "en": m["en"]} for m in machines},
    }, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    n_price = len(items)
    n_shop = len(shops)
    n_shop_qc = sum(1 for s in shops if s.get("province") == "QC")
    n_shop_priced = sum(1 for s in shops if s.get("public_prices") == "y")
    n_cat = len(cats)
    brands = sorted({i.get("brand") or "" for i in items if i.get("brand") and i.get("brand") != "—"})

    def page(fr: bool) -> str:
        def L(a, b):
            return a if fr else b

        stamp = date_fr(fetched) if fr else date_en(fetched)
        lede = L(
            f"{n_shop} fournisseurs (dont {n_shop_qc} au Québec) et {n_price} prix publics, relevés le {stamp}. "
            "Pièces d’usure pour plasma, laser fibre, usinage, presse plieuse, jet d’eau et mouvement — avec le numéro de pièce, la source et la date.",
            f"{n_shop} suppliers ({n_shop_qc} in Quebec) and {n_price} published prices, recorded on {stamp}. "
            "Wear parts for plasma, fiber laser, machining, press brakes, waterjet and motion — with the part number, the source and the date.",
        )
        cards = []
        for m in machines:
            n = sum(1 for i in items if i.get("machine") == m["id"])
            blurb = m["blurb_fr"] if fr else m["blurb_en"]
            label = m["fr"] if fr else m["en"]
            count = L(f"{n} prix publics", f"{n} published prices") if n else L("Prix sur demande chez les fournisseurs listés", "Prices on request from the listed suppliers")
            cards.append(
                f'<button type="button" class="pc-mcard" data-machine="{esc(m["id"])}">'
                f'<strong>{esc(label)}</strong><span class="pc-mblurb">{esc(blurb)}</span>'
                f'<span class="pc-mcount">{esc(count)}</span></button>'
            )

        market = catalog["market"]
        points = "".join(f"<li>{esc(p)}</li>" for p in (market["points_fr"] if fr else market["points_en"]))
        msrc = "".join(
            f'<li><a href="{esc(s["url"])}" rel="noopener noreferrer">{esc(s["fr"] if fr else s["en"])}</a></li>'
            if s.get("url") else f'<li>{esc(s["fr"] if fr else s["en"])}</li>'
            for s in market.get("sources") or []
        )
        market_html = f"""
<section class="pc-market" id="pc-market">
  <h2>{L("Y a-t-il un marché pour ces pièces ?", "Is there a market for these parts?")}</h2>
  <p class="pc-verdict">{esc(market["verdict_fr"] if fr else market["verdict_en"])}</p>
  <ul>{points}</ul>
  <p class="pc-src-h">{L("Sources", "Sources")}</p>
  <ul class="pc-src">{msrc}</ul>
</section>"""

        guides_html = "".join(_guide_html(g, fr) for g in catalog["guides"].values())
        xref = catalog["crossref"]
        xrows = []
        for r in xref["rows"]:
            xrows.append(
                "<tr>"
                f"<td>{esc(r['role_fr'] if fr else r['role_en'])}</td>"
                f"<td><code>{esc(r['oem'])}</code></td>"
                f"<td>{esc(r['use_fr'] if fr else r['use_en'])}</td>"
                f"<td>{('<code>' + esc(r['aftermarket']) + '</code>') if r.get('aftermarket') else '—'}</td>"
                f"<td>{esc(r['notes_fr'] if fr else r['notes_en'])}</td>"
                "</tr>"
            )
        xhead = "".join(f"<th>{esc(h)}</th>" for h in (xref["columns_fr"] if fr else xref["columns_en"]))
        sync = catalog["sync_note"]
        cross_html = f"""
<section class="pc-cross" id="pc-cross">
  <h2>{esc(xref['title_fr'] if fr else xref['title_en'])}</h2>
  <p class="pc-note">{esc(xref['caveat_fr'] if fr else xref['caveat_en'])}</p>
  <div class="pc-scroll">
    <table class="pc-table">
      <thead><tr>{xhead}</tr></thead>
      <tbody>{''.join(xrows)}</tbody>
    </table>
  </div>
  <h3>{esc(sync['title_fr'] if fr else sync['title_en'])}</h3>
  <p>{esc(sync['fr'] if fr else sync['en'])}</p>
</section>"""

        # supplier rows (also hydrated by JS for filtering; server-render for no-JS)
        def region_of(s):
            if s.get("province") == "QC":
                return "qc"
            if s.get("country") == "CA":
                return "ca"
            return "us"

        cat_lab = {
            "plasma": L("plasma", "plasma"),
            "laser": L("laser", "laser"),
            "usinage": L("usinage", "machining"),
            "plieuse": L("presse plieuse", "press brake"),
            "jet-eau": L("jet d’eau", "waterjet"),
            "routeur": L("routeur", "router"),
            "mouvement": L("mouvement", "motion"),
            "broche": L("broche", "spindle"),
            "entretien": L("entretien", "maintenance"),
            "filtres-gaz": L("gaz et filtres", "gas and filters"),
            "filtres-lubrifiants": L("filtres et lubrifiants", "filters and lubricants"),
            "soudage": L("soudage", "welding"),
        }
        def cats_label(raw):
            return ", ".join(cat_lab.get(c.strip(), c.strip()) for c in (raw or "").split(",") if c.strip())

        shop_rows = []
        for s in shops:
            region = region_of(s)
            cats_s = s.get("categories") or ""
            cats_show = cats_label(cats_s)
            priced = s.get("public_prices") == "y"
            contact = []
            if s.get("email"):
                contact.append(f'<a href="mailto:{esc(s["email"])}">{esc(s["email"])}</a>')
            if s.get("phone"):
                contact.append(esc(s["phone"]))
            city = s.get("city") or ""
            if s.get("province"):
                city = f"{city}, {s['province']}" if city else s["province"]
            price_lab = L("Oui", "Yes") if priced else L("Sur demande", "On request")
            ships = L("Oui", "Yes") if s.get("ships_to_qc") == "y" else L("À confirmer", "To confirm")
            shop_rows.append(
                f'<tr data-region="{region}" data-priced="{"1" if priced else "0"}" '
                f'data-cats="{esc(cats_s)}" data-brands="{esc(s.get("brands") or "")}" '
                f'data-text="{esc((s.get("name") or "") + " " + city + " " + (s.get("brands") or "") + " " + cats_s)}">'
                f'<td><a href="{esc(s.get("website") or "#")}" rel="noopener noreferrer">{esc(s.get("name"))}</a></td>'
                f'<td>{esc(city)}</td>'
                f'<td>{esc(cats_show)}</td>'
                f'<td>{esc(s.get("brands") or "")}</td>'
                f'<td>{price_lab}</td>'
                f'<td>{ships}</td>'
                f'<td>{ " · ".join(contact) }</td>'
                f'</tr>'
            )

        # price rows: server-render a compact first page? 1962 rows is heavy in HTML.
        # Occasions puts all cards in HTML. 1962 table rows might be ~1.5MB HTML x2 pages.
        # Better: JS-render prices from donnees.json, with a noscript note.
        # I'll still include a short "featured" set of core Duramax / laser / brake items in HTML
        # and let JS fill the full table. For no-JS, show the featured table + link to JSON.
        core_oems = {"220842", "220819", "220816", "220941", "220854", "220818", "220857",
                     "220777", "220930", "220797", "220990", "428927"}
        featured = [i for i in items if i.get("oem_part") in core_oems and i.get("origin") in ("oem", "compatible")]
        # keep one pack-of-5 or listed pack per source+oem+origin preferably
        featured = featured[:40]

        def price_row(i):
            cat = cat_by_id.get(i.get("category") or "", {})
            catlab = (cat.get("fr") if fr else cat.get("en")) or i.get("category") or ""
            mac = mac_by_id.get(i.get("machine") or "", {})
            maclab = (mac.get("fr") if fr else mac.get("en")) or i.get("machine") or ""
            origin = i.get("origin") or "unknown"
            olab = {"oem": L("Pièce d’origine", "Genuine"),
                    "compatible": L("Pièce compatible", "Compatible")}.get(origin, L("Non précisé", "Not stated"))
            pack = i.get("pack_qty")
            packlab = (L(f"paquet de {pack}", f"pack of {pack}") if pack else L("à confirmer", "check listing"))
            when = date_fr(i.get("fetched")) if fr else date_en(i.get("fetched"))
            oem = i.get("oem_part") or "—"
            return (
                f'<tr data-machine="{esc(i.get("machine") or "")}" data-cat="{esc(i.get("category") or "")}" '
                f'data-origin="{esc(origin)}" data-source="{esc(i.get("source") or "")}" '
                f'data-brand="{esc(i.get("brand") or "")}" data-region="{esc((i.get("province") or "").lower())}">'
                f'<td>{esc(i.get("name") or "")}</td>'
                f'<td><code>{esc(i.get("sku") or "—")}</code></td>'
                f'<td><code>{esc(oem)}</code></td>'
                f'<td>{esc(i.get("brand") or "")}</td>'
                f'<td>{esc(maclab)}</td>'
                f'<td>{esc(catlab)}</td>'
                f'<td>{esc(olab)}</td>'
                f'<td>{esc(packlab)}</td>'
                f'<td class="pc-num">{esc(money(i["price"], fr, i.get("currency") or "CAD"))}</td>'
                f'<td><a href="{esc(i.get("source_url") or "#")}" rel="noopener noreferrer">{esc(i.get("source_name") or "")}</a>'
                f'<div class="pc-when">{esc(when)}</div></td>'
                f'</tr>'
            )

        machine_opts = _opts(machines, "id", lambda m: m["fr"] if fr else m["en"], L("Tous", "All"))
        cat_opts = _opts(cats, "id", lambda c: c["fr"] if fr else c["en"], L("Tous", "All"))
        brand_opts = '<option value="" selected>' + esc(L("Toutes", "All")) + "</option>" + "".join(
            f'<option value="{esc(b)}">{esc(b)}</option>' for b in brands
        )
        source_ids = []
        seen_src = set()
        for i in items:
            sid = i.get("source")
            if sid and sid not in seen_src:
                seen_src.add(sid)
                source_ids.append((sid, i.get("source_name") or sid))
        source_opts = '<option value="" selected>' + esc(L("Toutes", "All")) + "</option>" + "".join(
            f'<option value="{esc(s)}">{esc(n)}</option>' for s, n in source_ids
        )

        method = catalog["method"]
        method_p = method["fr"] if fr else method["en"]
        method_srcs = "".join(
            f'<li><a href="{esc(s["url"])}" rel="noopener noreferrer">{esc(s["name"])}</a>'
            + (f' — {esc(s["note"])}' if s.get("note") else "")
            + "</li>"
            for s in method.get("sources") or []
        )

        boot = "(function(){var a=document.getElementById('pc-app');if(a)a.classList.add('js');})();"
        lang = "fr" if fr else "en"
        return f"""<link rel="stylesheet" href="/css/pieces.css?v={ver('css/pieces.css')}">
<div class="pc" id="pc-app" data-lang="{lang}" data-json="/pieces/donnees.json">
<script>{boot}</script>
<section class="pc-hero">
  <div class="pc-hero-top">
    <div>
      <p class="pc-kicker">{L("Pièces d’usure et consommables", "Wear parts and consumables")}</p>
      <h1>{L("Pièces pour machines CNC, plasma, laser et tôlerie", "Parts for CNC, plasma, laser and fabrication machines")}</h1>
      <p class="pc-lede">{esc(lede)}</p>
    </div>
    <p class="pc-stamp" role="status"><span><b>{L("Prix relevés le", "Prices recorded")}</b> {esc(stamp)}</span>
      <span>{L("Fuseau de l’Est (America/Toronto)", "Eastern Time (America/Toronto)")}</span>
      <span>{n_cat} {L("types de pièces", "part types")} · {n_shop} {L("fournisseurs", "suppliers")} · {n_price} {L("prix", "prices")}</span></p>
  </div>
</section>

<div class="pc-caveat">
  <p><b>{L("Des prix publics, pas une offre de vente.", "Published prices, not an offer to sell.")}</b>
  {L("CoupeFab n’est pas un distributeur. Un prix affiché est indicatif : taxes (TPS/TVQ), transport, courtage et disponibilité s’ajoutent souvent. Vérifiez le numéro de pièce dans le manuel de votre machine, et si la pièce est d’origine ou compatible. Aucun lien d’affiliation sur cette page.",
     "CoupeFab is not a distributor. A listed price is indicative: taxes (GST/QST), freight, brokerage and availability often apply. Check the part number in your machine manual, and whether the part is genuine or compatible. No affiliate links on this page.")}</p>
</div>

<div class="pc-machines" id="pc-machines">{''.join(cards)}</div>

<div class="pc-tabs" role="tablist" aria-label="{L("Sections de la page", "Page sections")}">
  <button type="button" role="tab" id="pc-tab-guides" aria-selected="true" aria-controls="pc-panel-guides">{L("Guides", "Guides")}</button>
  <button type="button" role="tab" id="pc-tab-shops" aria-selected="false" aria-controls="pc-panel-shops" tabindex="-1">{L("Fournisseurs", "Suppliers")} <small>{n_shop}</small></button>
  <button type="button" role="tab" id="pc-tab-prices" aria-selected="false" aria-controls="pc-panel-prices" tabindex="-1">{L("Prix", "Prices")} <small>{n_price}</small></button>
  <button type="button" role="tab" id="pc-tab-market" aria-selected="false" aria-controls="pc-panel-market" tabindex="-1">{L("Marché", "Market")}</button>
</div>

<section class="pc-panel is-active" id="pc-panel-guides" role="tabpanel" aria-labelledby="pc-tab-guides">
  <p class="pc-lead">{L("Chaque guide dit ce qu’est la pièce, comment voir qu’elle est usée, et quand la changer — avec les sources quand elles existent. Les mots techniques sont expliqués en français courant.",
                        "Each guide says what the part is, how to tell it is worn, and when to change it — with sources where they exist. Technical terms are explained in plain language.")}</p>
  <div class="pc-guides">{guides_html}</div>
  {cross_html}
</section>

<section class="pc-panel" id="pc-panel-shops" role="tabpanel" aria-labelledby="pc-tab-shops" hidden>
  <form class="pc-filters" id="pc-shop-filters" role="search" aria-label="{L("Filtrer les fournisseurs", "Filter suppliers")}" onsubmit="return false">
    <label class="pc-q"><span>{L("Rechercher", "Search")}</span>
      <input type="search" name="q" autocomplete="off" placeholder="{L("ex. Hypertherm, Lévis, plieuse", "e.g. Hypertherm, Lévis, press brake")}"></label>
    <label><span>{L("Région", "Region")}</span>
      <select name="region">
        <option value="" selected>{L("Toutes", "All")}</option>
        <option value="qc">{L("Québec", "Quebec")}</option>
        <option value="ca">{L("Reste du Canada", "Rest of Canada")}</option>
        <option value="us">{L("États-Unis / places de marché", "United States / marketplaces")}</option>
      </select></label>
    <label><span>{L("Prix publics", "Published prices")}</span>
      <select name="priced">
        <option value="" selected>{L("Tous", "All")}</option>
        <option value="1">{L("Avec un prix affiché", "With a listed price")}</option>
        <option value="0">{L("Prix sur demande", "Price on request")}</option>
      </select></label>
    <label><span>{L("Machine", "Machine")}</span>
      <select name="machine">{machine_opts}</select></label>
    <button type="reset" class="pc-reset">{L("Réinitialiser", "Reset")}</button>
  </form>
  <p class="pc-count" id="pc-shop-count" role="status"></p>
  <div class="pc-scroll">
    <table class="pc-table" id="pc-shop-table">
      <thead><tr>
        <th>{L("Fournisseur", "Supplier")}</th>
        <th>{L("Ville", "City")}</th>
        <th>{L("Types de pièces", "Part types")}</th>
        <th>{L("Marques", "Brands")}</th>
        <th>{L("Prix publics", "Published prices")}</th>
        <th>{L("Livre au Québec", "Ships to Quebec")}</th>
        <th>{L("Contact", "Contact")}</th>
      </tr></thead>
      <tbody>{''.join(shop_rows)}</tbody>
    </table>
  </div>
  <p class="pc-note">{n_shop_priced} {L("fournisseurs ont au moins quelques prix publics ; les autres cotent sur demande. Les courriels et téléphones viennent des pages publiques des entreprises.",
                                        "suppliers have at least some published prices; the others quote on request. Emails and phone numbers come from the companies’ public pages.")}</p>
</section>

<section class="pc-panel" id="pc-panel-prices" role="tabpanel" aria-labelledby="pc-tab-prices" hidden>
  <form class="pc-filters" id="pc-price-filters" role="search" aria-label="{L("Filtrer les prix", "Filter prices")}" onsubmit="return false">
    <label class="pc-q"><span>{L("Rechercher", "Search")}</span>
      <input type="search" name="q" autocomplete="off" placeholder="{L("ex. 220819, buse 65 A, Raytools", "e.g. 220819, 65 A nozzle, Raytools")}"></label>
    <label><span>{L("Machine", "Machine")}</span>
      <select name="machine">{machine_opts}</select></label>
    <label><span>{L("Type de pièce", "Part type")}</span>
      <select name="cat">{cat_opts}</select></label>
    <label><span>{L("Origine", "Origin")}</span>
      <select name="origin">
        <option value="" selected>{L("Toutes", "All")}</option>
        <option value="oem">{L("Pièce d’origine", "Genuine")}</option>
        <option value="compatible">{L("Pièce compatible", "Compatible")}</option>
      </select></label>
    <label><span>{L("Fournisseur", "Supplier")}</span>
      <select name="source">{source_opts}</select></label>
    <label><span>{L("Marque", "Brand")}</span>
      <select name="brand">{brand_opts}</select></label>
    <button type="reset" class="pc-reset">{L("Réinitialiser", "Reset")}</button>
  </form>
  <p class="pc-count" id="pc-price-count" role="status">{L("Chargement du tableau…", "Loading the table…")}</p>
  <div class="pc-scroll">
    <table class="pc-table" id="pc-price-table">
      <thead><tr>
        <th>{L("Pièce", "Part")}</th>
        <th>{L("N° vendeur", "Seller no.")}</th>
        <th>{L("N° d’origine", "OEM no.")}</th>
        <th>{L("Marque", "Brand")}</th>
        <th>{L("Machine", "Machine")}</th>
        <th>{L("Type", "Type")}</th>
        <th>{L("Origine", "Origin")}</th>
        <th>{L("Quantité", "Quantity")}</th>
        <th>{L("Prix", "Price")}</th>
        <th>{L("Source et date", "Source and date")}</th>
      </tr></thead>
      <tbody id="pc-price-body">{''.join(price_row(i) for i in featured)}</tbody>
    </table>
  </div>
  <noscript><p class="pc-note">{L("Sans JavaScript, seules quelques pièces courantes (torche Duramax) sont affichées. Ouvrez donnees.json pour la liste complète.",
                                  "Without JavaScript, only a few common Duramax-torch parts are shown. Open donnees.json for the full list.")}</p></noscript>
  <details class="pc-details">
    <summary>{L("Comment ces prix ont été relevés", "How these prices were recorded")}</summary>
    <p>{esc(method_p)}</p>
    <ul class="pc-src">{method_srcs}</ul>
  </details>
</section>

<section class="pc-panel" id="pc-panel-market" role="tabpanel" aria-labelledby="pc-tab-market" hidden>
  {market_html}
</section>
</div>
<script src="/js/pieces.js?v={ver('js/pieces.js')}" defer></script>
"""

        # The featured rows are a no-JS fallback; JS replaces the tbody with the full list.

    fr_body = page(True)
    en_body = page(False)
    meta = {
        "fetched": fetched,
        "suppliers": n_shop,
        "suppliers_qc": n_shop_qc,
        "prices": n_price,
        "categories": n_cat,
        "machines": len(machines),
    }
    return fr_body, en_body, meta

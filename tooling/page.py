"""Render /outillage/ (FR) and /en/tooling/ (EN) from data/tooling/prices.json.

Writes outillage/donnees.json (compact rows for js/outillage.js) and outillage/coupefab-prix-outillage.csv.
The table is rendered by JS (thousands of rows); a no-JS fallback shows the cheapest rows per category.
"""
from __future__ import annotations

import csv
import datetime as dt
import io
import json
from pathlib import Path

from tooling.classify import CATEGORIES, GROUPS

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "tooling" / "prices.json"
DATA_GZ = ROOT / "data" / "tooling" / "prices.json.gz"
OUT_DIR = ROOT / "outillage"
MONTHS_FR = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre",
             "octobre", "novembre", "décembre"]
MONTHS_EN = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
             "October", "November", "December"]
PROV_FR = {"QC": "Québec", "ON": "Ontario", "MB": "Manitoba", "BC": "Colombie-Britannique", "AB": "Alberta"}
PROV_EN = {"QC": "Quebec", "ON": "Ontario", "MB": "Manitoba", "BC": "British Columbia", "AB": "Alberta"}


def esc(s) -> str:
    return (str(s if s is not None else "").replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def ver(rel: str) -> int:
    p = ROOT / rel
    return p.stat().st_mtime_ns // 1000 if p.exists() else 0


def nfr(x, d=2):
    return f"{x:,.{d}f}".replace(",", "\u202f").replace(".", ",")


def money(x, fr):
    return f"{nfr(x)} $" if fr else f"${x:,.2f}"


def date_lab(iso, fr):
    try:
        d = dt.date.fromisoformat(str(iso)[:10])
    except (TypeError, ValueError):
        return str(iso or "")
    return f"{d.day} {MONTHS_FR[d.month - 1]} {d.year}" if fr else f"{MONTHS_EN[d.month - 1]} {d.day}, {d.year}"


def load():
    from tooling.fetch_tooling import read_snapshot
    return read_snapshot()


# compact row layout shared with js/outillage.js
COLS = ["cat", "name", "spec", "brand", "src", "price", "unit", "pack", "cur", "orig", "url", "date", "stock", "sku"]


def write_exports(d):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    src_idx = {s["id"]: i for i, s in enumerate(d["suppliers"])}
    rows = []
    for it in d["items"]:
        rows.append([it["cat"], it["name"], it["spec"], it["brand"], src_idx[it["source"]], it["price_cad"],
                     it["unit_cad"], it["pack"] or 0, it["currency"], it["price_orig"], it["url"], it["fetched"],
                     1 if it.get("in_stock", True) else 0, it.get("sku") or ""])
    blob = {"fetched": d["fetched"], "timezone": d["timezone"], "fx": d["fx"], "cols": COLS,
            "suppliers": d["suppliers"], "categories": [{"id": c[0], "group": c[1], "fr": c[2], "en": c[3]} for c in CATEGORIES],
            "rows": rows}
    (OUT_DIR / "donnees.json").write_text(json.dumps(blob, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["category", "item", "spec", "brand", "supplier", "supplier_region", "price_cad", "unit_price_cad",
                "pack_qty", "listed_currency", "listed_price", "fx_usdcad", "in_stock", "date", "url"])
    names = {s["id"]: s for s in d["suppliers"]}
    for it in d["items"]:
        s = names[it["source"]]
        w.writerow([it["cat"], it["name"], it["spec"], it["brand"], s["name"], s["province"] or s["country"],
                    f'{it["price_cad"]:.2f}', f'{it["unit_cad"]:.2f}', it["pack"] or "", it["currency"],
                    f'{it["price_orig"]:.2f}', (d["fx"]["rate"] if it["currency"] == "USD" else ""), "y" if it.get("in_stock", True) else "n",
                    it["fetched"], it["url"]])
    (OUT_DIR / "coupefab-prix-outillage.csv").write_text(buf.getvalue(), encoding="utf-8")


def render(site="https://coupefab.ca"):
    d = load()
    write_exports(d)
    items = d["items"]
    sups = d["suppliers"]
    by_src = {}
    for it in items:
        by_src.setdefault(it["source"], []).append(it)
    active = [s for s in sups if by_src.get(s["id"])]
    n_items, n_sup = len(items), len(active)
    n_qc = sum(1 for s in active if s["province"] == "QC")
    n_cat = sum(1 for c in CATEGORIES if any(i["cat"] == c[0] for i in items))
    fx = d["fx"]
    brands = sorted({i["brand"] for i in items if i["brand"]}, key=str.lower)

    def page(fr: bool) -> str:
        L = (lambda a, b: a if fr else b)
        stamp = date_lab(d["fetched"], fr)
        lede = L(f"{n_items:,} prix publics".replace(",", "\u202f") + f" chez {n_sup} fournisseurs ({n_qc} au Québec), relevés le {stamp}. "
                 "Consommables plasma et laser, fraises, forets, tarauds, plaquettes carbure, porte-outils, lames de scie, abrasifs, outillage de plieuse et instruments de mesure — chaque ligne donne la source, le prix en dollars canadiens et la date.",
                 f"{n_items:,} published prices from {n_sup} suppliers ({n_qc} in Quebec), recorded on {stamp}. "
                 "Plasma and laser consumables, end mills, drills, taps, carbide inserts, toolholders, saw blades, abrasives, press-brake tooling and measuring tools — every row gives the source, the price in Canadian dollars and the date.")
        # category cards
        cards = []
        for cid, grp, cfr, cen in CATEGORIES:
            rs = [i for i in items if i["cat"] == cid]
            if not rs:
                continue
            low = min(r["unit_cad"] for r in rs)
            nsrc = len({r["source"] for r in rs})
            cards.append(
                f'<button type="button" class="tl-card" data-cat="{cid}" aria-pressed="false">'
                f'<strong>{esc(cfr if fr else cen)}</strong>'
                f'<span class="tl-card-n">{L(f"{len(rs)} prix · {nsrc} fournisseur" + ("s" if nsrc > 1 else ""), f"{len(rs)} prices · {nsrc} supplier" + ("s" if nsrc > 1 else ""))}</span>'
                f'<span class="tl-card-low">{L("dès", "from")} {esc(money(low, fr))} {L("l’unité", "each")}</span></button>')
        cat_opts = f'<option value="" selected>{L("Tous", "All")}</option>' + "".join(
            f'<optgroup label="{esc(g[1] if fr else g[2])}">' + "".join(
                f'<option value="{c[0]}">{esc(c[2] if fr else c[3])}</option>' for c in CATEGORIES if c[1] == g[0]) + "</optgroup>"
            for g in GROUPS)
        src_opts = f'<option value="" selected>{L("Tous", "All")}</option>' + "".join(
            f'<option value="{esc(s["id"])}">{esc(s["name"])} ({esc(s["province"] or s["country"])})</option>' for s in active)
        brand_opts = f'<option value="" selected>{L("Tous", "All")}</option>' + "".join(
            f'<option value="{esc(b)}">{esc(b)}</option>' for b in brands)

        # no-JS fallback: 3 cheapest per category
        fb = []
        names = {s["id"]: s for s in sups}
        for cid, *_ in CATEGORIES:
            rs = sorted((i for i in items if i["cat"] == cid), key=lambda r: r["unit_cad"])[:3]
            for r in rs:
                fb.append(row_html(r, names[r["source"]], fr))

        # supplier table
        catlab = {c[0]: (c[2] if fr else c[3]) for c in CATEGORIES}
        sup_rows = []
        order = {"qc": 0, "ca": 1, "us": 2}
        for s in sorted(active, key=lambda s: (order[region(s)], -len(by_src[s["id"]]))):
            rs = by_src[s["id"]]
            cats = sorted({r["cat"] for r in rs}, key=lambda c: [x[0] for x in CATEGORIES].index(c))
            where = ", ".join(x for x in [s["city"], (PROV_FR if fr else PROV_EN).get(s["province"], s["province"])] if x) or s["country"]
            if s["country"] == "US":
                where = (s["city"] + ", " if s["city"] else "") + L("États-Unis (prix en USD convertis)", "United States (USD converted)")
            sup_rows.append(
                f'<tr data-region="{region(s)}"><td><a href="https://{esc(s["host"])}/" rel="noopener nofollow" target="_blank">{esc(s["name"])}</a></td>'
                f'<td>{esc(where)}</td><td class="tl-num">{len(rs)}</td>'
                f'<td>{esc(", ".join(catlab[c] for c in cats))}</td>'
                f'<td>{L("Boutique en ligne (flux public)", "Online store (public feed)")}</td></tr>')
        blocked = "".join(
            f'<li><b>{esc(b["name"])}</b>{(" — " + esc(b["host"])) if b["host"] else ""}{(" (" + esc(b["province"]) + ")") if b["province"] else ""} : {esc(b["why_fr"] if fr else b["why_en"])}</li>'
            for b in d.get("blocked", []))
        status_bad = [s for s in d.get("status", []) if not s["ok"]]
        stale = ""
        if status_bad:
            stale = "<p class=\"tl-note\">" + esc(L("Relevé incomplet pour : ", "Incomplete run for: ")) + esc(", ".join(s["id"] for s in status_bad)) + esc(L(" — lignes précédentes conservées.", " — previous rows kept.")) + "</p>"

        rate = f'{fx["rate"]:.4f}'
        rate_s = rate.replace(".", ",") if fr else rate
        lang = "fr" if fr else "en"
        boot = "(function(){var a=document.getElementById('tl-app');if(a)a.classList.add('js');})();"
        return f"""<link rel="stylesheet" href="/css/outillage.css?v={ver('css/outillage.css')}">
<div class="tl" id="tl-app" data-lang="{lang}" data-json="/outillage/donnees.json">
<script>{boot}</script>
<section class="tl-hero">
  <div class="tl-hero-top">
    <div>
      <p class="tl-kicker">{L("Outillage d’atelier", "Shop tooling")}</p>
      <h1>{L("Prix de l’outillage : plasma, laser, usinage, routeur, sciage et plieuse", "Tooling prices: plasma, laser, machining, router, sawing and press brake")}</h1>
      <p class="tl-lede">{esc(lede)}</p>
    </div>
    <p class="tl-stamp" role="status"><span><b>{L("Prix relevés le", "Prices recorded")}</b> {esc(stamp)}</span>
      <span>{L("Fuseau de l’Est (America/Toronto)", "Eastern Time (America/Toronto)")}</span>
      <span>{n_cat} {L("catégories", "categories")} · {n_sup} {L("fournisseurs", "suppliers")}</span></p>
  </div>
</section>

<div class="tl-caveat"><p><b>{L("Des prix publics, pas une offre de vente.", "Published prices, not an offer to sell.")}</b>
  {L(f"CoupeFab n’est pas un distributeur et n’a aucun lien d’affiliation. Les prix sont ceux affichés par chaque boutique, avant taxes (TPS/TVQ) et transport. Les prix en dollars américains sont convertis au taux de la Banque du Canada du {date_lab(fx.get('date'), True)} ({rate_s} $ CA pour 1 $ US), le même que sur la page des prix des tôles ; droits et courtage en sus.",
     f"CoupeFab is not a distributor and has no affiliate links. Prices are as listed by each store, before taxes (GST/QST) and freight. US-dollar prices are converted at the Bank of Canada rate of {date_lab(fx.get('date'), False)} (CA${rate_s} per US$1), the same rate as the sheet-price page; duties and brokerage extra.")}</p></div>

<h2 class="tl-h2">{L("Choisir une catégorie", "Pick a category")}</h2>
<div class="tl-cards" id="tl-cards">{''.join(cards)}</div>

<div class="tl-tabs" role="tablist" aria-label="{L("Sections de la page", "Page sections")}">
  <button type="button" role="tab" id="tl-tab-prices" aria-selected="true" aria-controls="tl-panel-prices">{L("Prix", "Prices")} <small>{n_items}</small></button>
  <button type="button" role="tab" id="tl-tab-shops" aria-selected="false" aria-controls="tl-panel-shops" tabindex="-1">{L("Fournisseurs", "Suppliers")} <small>{n_sup}</small></button>
  <button type="button" role="tab" id="tl-tab-method" aria-selected="false" aria-controls="tl-panel-method" tabindex="-1">{L("Méthode et sources", "Method and sources")}</button>
</div>

<section class="tl-panel is-active" id="tl-panel-prices" role="tabpanel" aria-labelledby="tl-tab-prices">
  <form class="tl-filters" id="tl-filters" role="search" aria-label="{L("Filtrer les prix", "Filter prices")}" onsubmit="return false">
    <label class="tl-q"><span>{L("Rechercher", "Search")}</span>
      <input type="search" name="q" autocomplete="off" placeholder="{L("ex. fraise 1/4, ER32, disque à lamelles, 220819", "e.g. 1/4 end mill, ER32, flap disc, 220819")}"></label>
    <label><span>{L("Catégorie", "Category")}</span><select name="cat">{cat_opts}</select></label>
    <label><span>{L("Région", "Region")}</span><select name="region">
      <option value="" selected>{L("Tous", "All")}</option>
      <option value="qc">{L("Québec", "Quebec")}</option>
      <option value="ca">{L("Reste du Canada", "Rest of Canada")}</option>
      <option value="us">{L("États-Unis (livre au Canada)", "United States (ships to Canada)")}</option></select></label>
    <label><span>{L("Fournisseur", "Supplier")}</span><select name="src">{src_opts}</select></label>
    <label><span>{L("Marque", "Brand")}</span><select name="brand">{brand_opts}</select></label>
    <label><span>{L("Disponibilité", "Availability")}</span><select name="stock">
      <option value="" selected>{L("Tous", "All")}</option>
      <option value="1">{L("En stock seulement", "In stock only")}</option></select></label>
    <button type="reset" class="tl-btn tl-reset">{L("Tout afficher", "Show all")}</button>
  </form>
  <p class="tl-count" id="tl-count" role="status" aria-live="polite">{L("Chargement du tableau…", "Loading the table…")}</p>
  <div class="tl-scroll">
    <table class="tl-table" id="tl-table">
      <caption class="tl-sr">{L("Prix de l’outillage, un article par ligne. Cliquez sur un en-tête pour trier.", "Tooling prices, one item per row. Click a header to sort.")}</caption>
      <thead><tr>
        <th scope="col"><button type="button" class="tl-sort" data-sort="name">{L("Article", "Item")}</button></th>
        <th scope="col">{L("Caractéristiques", "Spec")}</th>
        <th scope="col"><button type="button" class="tl-sort" data-sort="src">{L("Fournisseur", "Supplier")}</button></th>
        <th scope="col" class="tl-r"><button type="button" class="tl-sort" data-sort="price">{L("Prix (CAD)", "Price (CAD)")}</button></th>
        <th scope="col" class="tl-r"><button type="button" class="tl-sort" data-sort="unit" aria-sort="ascending">{L("Prix à l’unité", "Price per unit")}</button></th>
        <th scope="col">{L("Relevé le", "Recorded")}</th>
        <th scope="col">{L("Lien", "Link")}</th>
      </tr></thead>
      <tbody id="tl-body">{''.join(fb)}</tbody>
    </table>
  </div>
  <nav class="cf-pager" id="tl-pager" hidden></nav>
  <noscript><p class="tl-note">{L("Sans JavaScript, seuls les trois prix à l’unité les plus bas de chaque catégorie sont affichés. Le fichier CSV complet est plus bas.", "Without JavaScript, only the three lowest unit prices per category are shown. The full CSV file is below.")}</p></noscript>
  <p class="tl-note">{L("« Prix à l’unité » = prix affiché divisé par le nombre de pièces quand la boutique vend en paquet (ex. 5 buses). Sinon, c’est le prix affiché.", "“Price per unit” = listed price divided by the number of pieces when the store sells a pack (e.g. 5 nozzles). Otherwise it is the listed price.")}
  <a href="/outillage/coupefab-prix-outillage.csv" download>{L("Télécharger tous les prix (CSV)", "Download every price (CSV)")}</a></p>
</section>

<section class="tl-panel" id="tl-panel-shops" role="tabpanel" aria-labelledby="tl-tab-shops" hidden>
  <p class="tl-lead">{L("Québec d’abord, puis le reste du Canada, puis les boutiques américaines qui livrent au Canada. Pour l’acier en feuille, les pièces de rechange et tous les autres fournisseurs, voyez aussi", "Quebec first, then the rest of Canada, then US stores that ship to Canada. For sheet metal, spare parts and every other supplier, see also")}
    <a href="{L("/fournisseurs/", "/en/suppliers/")}">{L("le répertoire des fournisseurs", "the supplier directory")}</a> {L("et", "and")} <a href="{L("/pieces/", "/en/parts/")}">{L("les pièces et consommables", "parts and consumables")}</a>.</p>
  <div class="tl-scroll"><table class="tl-table">
    <thead><tr><th scope="col">{L("Fournisseur", "Supplier")}</th><th scope="col">{L("Où", "Where")}</th><th scope="col" class="tl-r">{L("Prix relevés", "Prices")}</th><th scope="col">{L("Catégories", "Categories")}</th><th scope="col">{L("Source", "Source")}</th></tr></thead>
    <tbody>{''.join(sup_rows)}</tbody></table></div>
  <h3 class="tl-h3">{L("Fournisseurs vérifiés, mais sans prix relevés", "Suppliers checked, but with no prices recorded")}</h3>
  <p class="tl-lead">{L("Nous ne contournons jamais un pare-feu anti-robots ni un captcha, et nous respectons le fichier robots.txt de chaque site. Ces boutiques restent de bonnes adresses ; leurs prix se consultent sur leur site ou par soumission.", "We never get around a bot firewall or a captcha, and we follow each site’s robots.txt. These stores are still good places to buy; check prices on their site or ask for a quote.")}</p>
  <ul class="tl-blocked">{blocked}</ul>
</section>

<section class="tl-panel" id="tl-panel-method" role="tabpanel" aria-labelledby="tl-tab-method" hidden>
  <div class="tl-prose">
  <p>{L("Chaque prix vient du flux public de la boutique (catalogue Shopify « products.json » ou API publique WooCommerce Store), lu une requête à la fois, avec un robot identifié « CoupeFabPriceBot ». Nous n’utilisons aucun compte, aucun prix de membre ni panier.", "Each price comes from the store’s public feed (Shopify “products.json” catalogue or the public WooCommerce Store API), read one request at a time by a bot identified as “CoupeFabPriceBot”. No account, member price or cart is used.")}</p>
  <p>{L("Les articles sont classés par mots-clés (anglais et français) dans le titre et le type de produit. Un article mal classé ? Écrivez-nous. Pour les très grands catalogues, nous gardons au plus 700 lignes par fournisseur et par catégorie (les articles en stock et les moins chers à l’unité d’abord).", "Items are sorted by keywords (English and French) in the title and product type. Spotted a misfiled item? Write to us. For very large catalogues we keep at most 700 rows per supplier and category (in-stock and lowest unit price first).")}</p>
  <p>{L(f"Taux de change : {rate_s} $ CA pour 1 $ US, Banque du Canada, {date_lab(fx.get('date'), True)}.", f"Exchange rate: CA${rate_s} per US$1, Bank of Canada, {date_lab(fx.get('date'), False)}.")} <a href="{esc(fx.get('url') or 'https://www.bankofcanada.ca/rates/exchange/daily-exchange-rates/')}" rel="noopener">{L("Source", "Source")}</a></p>
  <p>{L("Vous vendez de l’outillage au Québec ?", "Do you sell tooling in Quebec?")} <a href="{L("/fournisseurs/#ajouter", "/en/suppliers/#add")}">{L("Ajoutez gratuitement votre liste de prix", "Add your price list for free")}</a>.</p>
  {stale}
  </div>
</section>
</div>
<script src="/js/outillage.js?v={ver('js/outillage.js')}" defer></script>
"""

    return page(True), page(False), {"fetched": d["fetched"], "prices": n_items, "suppliers": n_sup,
                                     "suppliers_qc": n_qc, "categories": n_cat}


def region(s):
    return "qc" if s["province"] == "QC" else ("ca" if s["country"] == "CA" else "us")


def row_html(r, s, fr):
    L = (lambda a, b: a if fr else b)
    pack = f'<div class="tl-sub">{L("paquet de", "pack of")} {r["pack"]}</div>' if r.get("pack") else ""
    usd = f'<div class="tl-sub">{L("affiché", "listed")} {r["price_orig"]:.2f} US$</div>' if r["currency"] == "USD" else ""
    return (f'<tr><td>{esc(r["name"])}{("<div class=\"tl-sub\">" + esc(r["brand"]) + "</div>") if r["brand"] else ""}</td>'
            f'<td>{esc(r["spec"] or "—")}</td><td>{esc(s["name"])}<div class="tl-sub">{esc(s["province"] or s["country"])}</div></td>'
            f'<td class="tl-r tl-num">{esc(money(r["price_cad"], fr))}{usd}</td>'
            f'<td class="tl-r tl-num">{esc(money(r["unit_cad"], fr))}{pack}</td>'
            f'<td>{esc(date_lab(r["fetched"], fr))}</td>'
            f'<td><a href="{esc(r["url"])}" rel="noopener nofollow" target="_blank">{L("Voir", "View")}</a></td></tr>')

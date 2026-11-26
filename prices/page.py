"""Render the /prix/ and /en/sheet-prices/ pages from data/prices/latest.json.

Only numbers present in latest.json are shown. Derived values ($/lb, $/sq ft,
weights) are labelled as calculations on the page.
"""
import csv
import datetime as dt
import json
import statistics
from pathlib import Path

from . import normalize as N

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "prices"
MONTHS_FR = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre",
             "octobre", "novembre", "décembre"]
ELIGIBLE = {"oui", "cueillette", "a_confirmer"}  # can actually be bought by a Quebec shop

STEEL_FRACS = [0.1875, 0.25, 0.3125, 0.375, 0.5, 0.625, 0.75, 0.875, 1, 1.25, 1.5, 1.75, 2, 2.5, 3, 4]
AL_DEC = [0.016, 0.020, 0.025, 0.032, 0.040, 0.050, 0.063, 0.071, 0.080, 0.090, 0.100, 0.125, 0.160, 0.1875,
          0.250, 0.3125, 0.375, 0.5, 0.625, 0.75, 1, 1.25, 1.5, 2, 2.5, 3]


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;"))


def nfr(x, d=2):
    return f"{x:,.{d}f}".replace(",", " ").replace(".", ",")


def nen(x, d=2):
    return f"{x:,.{d}f}"


def canon_thickness(fam, grade, t):
    """Snap a thickness to a standard gauge/fraction. Returns (key, label_fr, label_en)."""
    if not t:
        return None, None, None
    cands = []
    if fam == "acier":
        tab = N.GAUGE_GALV if (grade or "").lower().startswith("galv") else N.GAUGE_STEEL
        cands += [(v, f"{g} ga") for g, v in tab.items() if v < 0.18]
        cands += [(v, N.fmt_frac(v) + " po") for v in STEEL_FRACS]
    elif fam == "inox":
        cands += [(v, f"{g} ga") for g, v in N.GAUGE_SS.items() if v < 0.18]
        cands += [(v, N.fmt_frac(v) + " po") for v in STEEL_FRACS]
    else:
        cands += [(v, (N.fmt_frac(v) + " po") if v >= 0.1875 and N.fmt_frac(v) else f"{v:.3f} po".replace("0.", ".")) for v in AL_DEC]
    v, lab = min(cands, key=lambda c: abs(c[0] - t))
    if abs(v - t) / t > 0.07:
        v, lab = t, f"{t:.4f}".rstrip("0") + " po"
    mm = v * 25.4
    lab_fr = f"{lab} ({nfr(v,4).rstrip('0').rstrip(',')} po · {nfr(mm,2)} mm)" if "ga" in lab else f"{lab} ({nfr(mm,2)} mm)"
    lab_en = lab_fr.replace(" po", " in").replace(",", ".")
    return f"{v:.4f}", lab_fr, lab_en.replace(" in (", " in (") if lab_en else lab_en


def subclass(r):
    f, g = r["family"], (r["grade"] or "")
    if f == "acier":
        if g.lower().startswith("galv"):
            return "galv"
        if g.startswith("Plaque dure"):
            return "ar"
        return "noir"
    if f == "inox":
        if g.startswith("316"):
            return "316"
        if g in ("303", "304", "304L", ""):
            return "304"
        return g
    return g or "?"


SUB_LABEL = {"ar": ("plaque dure AR", "AR hard plate"), "noir": ("noir (HR/CR/A36/44W)", "black (HR/CR/A36/44W)"),
             "galv": ("galvanisé", "galvanized"), "304": ("304/304L", "304/304L"), "316": ("316/316L", "316/316L")}


def load():
    latest = json.loads((DATA / "latest.json").read_text())
    rows = latest["rows"]
    sup = latest["suppliers"]
    # sanity band on computed $/lb for sheet & plate (bars are cut pieces: no band)
    band = {"acier": (0.35, 12), "inox": (1.5, 40), "aluminium": (1.5, 40), "cuivre": (3, 60), "laiton": (3, 60),
            "bronze": (3, 60), "bronze_alu": (3, 60)}
    for r in rows:
        lb = r.get("price_per_lb_cad")
        lo, hi = band.get(r["family"], (0, 1e9))
        r["outlier"] = bool(r["form"] in ("tole", "plaque") and lb and not (lo <= lb <= hi))
        ships = sup.get(r["supplier"], {}).get("ships_qc", "")
        avail = (r.get("availability") or "").lower()
        r["eligible"] = ships in ELIGIBLE and "rupture" not in avail and not r["outlier"]
        # spec key
        if r["form"] in ("tole", "plaque"):
            k, lf, le = canon_thickness(r["family"], r["grade"], r.get("thickness_in"))
            sc = subclass(r)
            fl = N.FAMILY_LABELS[r["family"]]
            sl = SUB_LABEL.get(sc, (sc, sc))
            if k:
                r["spec"] = f"{r['family']}|{sc}|{k}"
                r["spec_fr"] = f"{fl[0]} {sl[0]} — {lf}"
                r["spec_en"] = f"{fl[1]} {sl[1]} — {le}"
            r["metric"] = r.get("price_per_sqft_cad")
        else:
            sz = (r.get("size_label") or "").split(" — ")[0].strip()
            r["spec"] = f"{r['family']}|{r['grade'] or '?'}|{r['form']}|{sz}"
            fl = N.FAMILY_LABELS[r["family"]]
            fo = N.FORM_LABELS[r["form"]]
            r["spec_fr"] = f"{fl[0]} {r['grade'] or ''} — {fo[0].lower()} {sz}".replace("  ", " ")
            r["spec_en"] = f"{fl[1]} {r['grade'] or ''} — {fo[1].lower()} {sz}".replace("  ", " ")
            r["metric"] = r.get("price_per_ft_cad") or r.get("price_per_lb_cad")
    # best per spec
    by = {}
    for r in rows:
        if r.get("spec") and r["eligible"] and r.get("metric"):
            by.setdefault(r["spec"], []).append(r)
    for spec, rs in by.items():
        n = len({x["supplier"] for x in rs})
        if n < 2:
            continue  # a "best price" needs at least two suppliers to compare
        b = min(rs, key=lambda x: x["metric"])
        b["best"] = True
        b["n_suppliers"] = n
        b["runner_up"] = None
        others = sorted([x for x in rs if x["supplier"] != b["supplier"]], key=lambda x: x["metric"])
        if others:
            b["runner_up"] = {"supplier": others[0]["supplier"], "metric": others[0]["metric"]}
    index = []
    if (DATA / "index.csv").exists():
        with (DATA / "index.csv").open() as f:
            index = list(csv.DictReader(f))
    return latest, rows, index


def compact(latest, rows, index):
    keys = ["supplier", "family", "grade", "in_catalogue", "form", "description", "size_label", "thickness_in",
            "thickness_mm", "gauge", "width_in", "length_in", "length_ft", "price", "currency", "unit", "price_cad",
            "price_per_lb_cad", "price_per_kg_cad", "price_per_sqft_cad", "price_per_ft_cad", "weight_lb",
            "availability", "url", "fetched_at", "source_updated", "notes", "outlier", "eligible", "spec", "spec_fr",
            "spec_en", "best"]
    short = {k: i for i, k in enumerate(keys)}
    data = {
        "generated_at": latest["generated_at"], "fx": latest["fx"],
        "suppliers": {k: {kk: v.get(kk) for kk in ("name", "city", "region", "currency", "ships_qc", "shipping", "shipping_en", "site")}
                      for k, v in latest["suppliers"].items()},
        "status": latest["status"], "catalogue": latest["catalogue"],
        "families": {k: list(v) for k, v in N.FAMILY_LABELS.items()},
        "forms": {k: list(v) for k, v in N.FORM_LABELS.items()},
        "density": N.DENSITY, "keys": keys,
        "rows": [[r.get(k) for k in keys] for r in rows],
        "index": index,
    }
    return data


def date_fr(iso):
    d = dt.date.fromisoformat(iso[:10])
    return f"{d.day} {MONTHS_FR[d.month-1]} {d.year}"


def date_en(iso):
    d = dt.date.fromisoformat(iso[:10])
    return d.strftime("%B %-d, %Y")


def gauge_table_html(fr):
    head = ("<tr><th>Calibre</th><th>Acier (MSG)</th><th>Galvanisé</th><th>Inox</th><th>Aluminium (B&amp;S)</th></tr>"
            if fr else "<tr><th>Gauge</th><th>Steel (MSG)</th><th>Galvanized</th><th>Stainless</th><th>Aluminum (B&amp;S)</th></tr>")
    out = []
    for g in range(7, 27):
        cells = []
        for tab in (N.GAUGE_STEEL, N.GAUGE_GALV, N.GAUGE_SS, N.GAUGE_AL):
            v = tab.get(g)
            if v:
                cells.append(f"<td>{v:.4f} po<br><span class=\"mm\">{nfr(v*25.4)} mm</span></td>" if fr
                             else f"<td>{v:.4f} in<br><span class=\"mm\">{v*25.4:.2f} mm</span></td>")
            else:
                cells.append("<td>—</td>")
        out.append(f"<tr><th scope=\"row\">{g}</th>{''.join(cells)}</tr>")
    return f'<div class="table-wrap"><table class="gauge"><thead>{head}</thead><tbody>{"".join(out)}</tbody></table></div>'


def best_table_html(rows, sup, fr):
    """Server-rendered 'meilleur prix' for the flagship sheet/plate specs (SEO + no-JS)."""
    picks = []
    for r in rows:
        if r.get("best") and r["form"] in ("tole", "plaque") and r.get("n_suppliers", 1) >= 2:
            picks.append(r)
    order = {"acier": 0, "inox": 1, "aluminium": 2, "cuivre": 3, "laiton": 4, "bronze": 5, "bronze_alu": 6}
    picks.sort(key=lambda r: (order.get(r["family"], 9), subclass(r), r.get("thickness_in") or 0))
    body = []
    for r in picks[:40]:
        s = sup[r["supplier"]]
        ru = r.get("runner_up")
        if fr:
            gap = f"{nfr(ru['metric'])} $ chez {esc(sup[ru['supplier']]['name'])}" if ru else "—"
            body.append(f"<tr><td>{esc(r['spec_fr'])}</td><td><strong>{nfr(r['metric'])} $/pi²</strong></td>"
                        f"<td><a href=\"{esc(r['url'])}\" rel=\"nofollow noopener\">{esc(s['name'])}</a><br><span class=\"mm\">{esc(r['grade'])} · {esc(r['size_label'])} · {nfr(r['price_cad'])} $</span></td>"
                        f"<td>{gap}</td><td>{r['n_suppliers']}</td></tr>")
        else:
            gap = f"${nen(ru['metric'])} at {esc(sup[ru['supplier']]['name'])}" if ru else "—"
            body.append(f"<tr><td>{esc(r['spec_en'])}</td><td><strong>${nen(r['metric'])}/sq ft</strong></td>"
                        f"<td><a href=\"{esc(r['url'])}\" rel=\"nofollow noopener\">{esc(s['name'])}</a><br><span class=\"mm\">{esc(r['grade'])} · {esc(r['size_label'].replace(' po',' in'))} · ${nen(r['price_cad'])}</span></td>"
                        f"<td>{gap}</td><td>{r['n_suppliers']}</td></tr>")
    head = ("<tr><th>Spécification</th><th>Meilleur prix (CAD, calculé)</th><th>Fournisseur · feuille</th><th>Suivant</th><th>Fourn.</th></tr>"
            if fr else "<tr><th>Spec</th><th>Best price (CAD, computed)</th><th>Supplier · sheet</th><th>Next best</th><th>Suppl.</th></tr>")
    return f'<div class="table-wrap"><table class="best"><thead>{head}</thead><tbody>{"".join(body)}</tbody></table></div>'


def suppliers_html(latest, rows, fr):
    sup, st = latest["suppliers"], latest["status"]
    counts = {}
    for r in rows:
        counts[r["supplier"]] = counts.get(r["supplier"], 0) + 1
    ship_lbl = {"oui": ("Livre au Québec", "Ships to Quebec"), "cueillette": ("Cueillette au Québec", "Pickup in Quebec"),
                "indicatif": ("Indicatif (non vendu seul)", "Indicative (not sold alone)"),
                "a_confirmer": ("Expédition à confirmer", "Shipping to confirm"), "non": ("Repère hors Québec", "Benchmark outside Quebec")}
    li = []
    for sid, s in sup.items():
        n = counts.get(sid, 0)
        ok = st.get(sid, {}).get("ok", False)
        lab = ship_lbl.get(s["ships_qc"], ("", ""))[0 if fr else 1]
        note = s["shipping"] if fr else s.get("shipping_en", s["shipping"])
        state = (f"{n} lignes" if fr else f"{n} rows") + ("" if ok else (" · relevé en échec, données précédentes" if fr else " · fetch failed, previous data"))
        li.append(f"<li><strong><a href=\"{esc(s['site'])}\" rel=\"nofollow noopener\">{esc(s['name'])}</a></strong> — {esc(s['city'])} · "
                  f"<span class=\"tag\">{esc(lab)}</span> · {state}<br><span class=\"meta\">{esc(note)}</span></li>")
    st_lbl = {"sur_demande": ("Prix sur demande", "Quote only"), "bloque": ("Bloqué (non lu)", "Blocked (not read)"),
              "non_couvert": ("Pas encore couvert", "Not covered yet")}
    li2 = []
    for s in latest["suppliers_static"]:
        lab = st_lbl[s["status"]][0 if fr else 1]
        li2.append(f"<li><strong><a href=\"{esc(s['url'])}\" rel=\"nofollow noopener\">{esc(s['name'])}</a></strong> — {esc(s['city'])} · "
                   f"<span class=\"tag tag-muted\">{lab}</span><br><span class=\"meta\">{esc(s['note'] if fr else s['note_en'])}</span></li>")
    return "<ul class=\"suppliers\">" + "".join(li) + "</ul>", "<ul class=\"suppliers\">" + "".join(li2) + "</ul>"


def coverage_html(rows, fr):
    have = {}
    for r in rows:
        if r.get("in_catalogue"):
            have.setdefault((r["family"], r["grade"]), set()).add(r["form"])
    out = []
    for fam, grades in N.CATALOGUE.items():
        fl = N.FAMILY_LABELS[fam][0 if fr else 1]
        cells = []
        for g in grades:
            forms = have.get((fam, g))
            if fam == "acier" and g.startswith("A500"):
                forms = (forms or set()) | have.get((fam, "A500"), set())
            if forms:
                fls = ", ".join(sorted(N.FORM_LABELS[f][0 if fr else 1].split(" (")[0].lower() for f in forms))
                cells.append(f'<li class="has" data-family="{fam}" data-grade="{esc(g)}"><button type="button" class="grade-pick" data-family="{fam}" data-grade="{esc(g)}">{esc(g)}</button><span>{esc(fls)}</span></li>')
            else:
                cells.append(f'<li class="none"><b>{esc(g)}</b><span>{"sur demande" if fr else "quote only"}</span></li>')
        out.append(f"<div class=\"cov\"><h3>{fl}</h3><ul>{''.join(cells)}</ul></div>")
    return "<div class=\"coverage\">" + "".join(out) + "</div>"


def render(form_newsletter, site):
    latest, rows, index = load()
    data = compact(latest, rows, index)
    (ROOT / "prix").mkdir(exist_ok=True)
    (ROOT / "prix" / "donnees.json").write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")))
    # public CSV of the current snapshot
    import io
    buf = io.StringIO()
    w = csv.writer(buf)
    ck = ["supplier", "family", "grade", "form", "description", "size_label", "thickness_in", "thickness_mm", "gauge",
          "width_in", "length_in", "length_ft", "price", "currency", "unit", "price_cad", "price_per_lb_cad",
          "price_per_kg_cad", "price_per_sqft_cad", "price_per_ft_cad", "weight_lb", "availability", "url",
          "fetched_at", "source_updated", "notes"]
    w.writerow(ck)
    for r in rows:
        w.writerow([r.get(k) for k in ck])
    (ROOT / "prix" / "coupefab-prix-metaux.csv").write_text(buf.getvalue(), encoding="utf-8")

    gen = latest["generated_at"]
    fx = latest["fx"]
    n_rows = len(rows)
    n_real = len([s for s in latest["status"].values() if s.get("rows")])
    sup = latest["suppliers"]
    stamp_fr = f"{date_fr(gen)}, {gen[11:16]} (heure de Montréal)"
    stamp_en = f"{date_en(gen)}, {gen[11:16]} (Montreal time)"

    def page(fr):
        L = (lambda a, b: a if fr else b)
        sup_live, sup_static = suppliers_html(latest, rows, fr)
        schema = {
            "@context": "https://schema.org", "@type": "Dataset",
            "name": L("Prix publiés des tôles et métaux au Québec et au Canada — CoupeFab",
                      "Published sheet-metal and metal stock prices for Quebec and Canada — CoupeFab"),
            "description": L("Relevé quotidien des prix publiés en ligne (tôle, plaque, barre, tube, tuyau) chez des fournisseurs qui livrent au Québec ou au Canada, normalisés en CAD, $/lb, $/kg et $/pi², avec source et date pour chaque ligne.",
                             "Daily survey of prices published online (sheet, plate, bar, tube, pipe) by suppliers shipping to Quebec or Canada, normalized to CAD, $/lb, $/kg and $/sq ft, with a source and date on every row."),
            "url": site + L("/prix/", "/en/sheet-prices/"), "inLanguage": L("fr-CA", "en-CA"),
            "creator": {"@type": "Organization", "name": "CoupeFab", "url": site + "/"},
            "dateModified": gen, "temporalCoverage": f"{(index[0]['date'] if index else gen[:10])}/..",
            "spatialCoverage": {"@type": "Place", "name": "Québec, Canada"},
            "isAccessibleForFree": True,
            "keywords": ["prix acier", "prix tôle", "steel price Canada", "aluminium", "inox", "plasma CNC", "Québec"],
            "variableMeasured": ["prix CAD", "CAD/lb", "CAD/kg", "CAD/pi²", "CAD/pi linéaire"],
            "distribution": [
                {"@type": "DataDownload", "encodingFormat": "text/csv", "contentUrl": site + "/prix/coupefab-prix-metaux.csv"},
                {"@type": "DataDownload", "encodingFormat": "application/json", "contentUrl": site + "/prix/donnees.json"}],
        }
        fx_txt = L(f"1 USD = {nfr(fx['rate'],4)} CAD (Banque du Canada, {date_fr(fx['date'])})",
                   f"1 USD = {fx['rate']:.4f} CAD (Bank of Canada, {date_en(fx['date'])})")
        best = best_table_html(rows, sup, fr)
        H = []
        H.append(f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>')
        H.append(f'''<div class="wrap prix" id="prix-app" data-lang="{L("fr","en")}">
  <p class="kicker">{L("Prix des métaux · bêta", "Metal prices · beta")}</p>
  <h1 class="page-title">{L("Prix des tôles et des métaux au Québec", "Sheet-metal and metal prices in Quebec")}</h1>
  <p class="lede">{L("Les prix <strong>publiés en ligne</strong> par les fournisseurs qui vendent au Québec et au Canada, comparés au pied carré et à la livre, en dollars canadiens. Chaque chiffre a sa source et sa date. Aucun prix inventé : si un fournisseur ne publie rien, on écrit « sur demande ».",
                     "Prices <strong>published online</strong> by suppliers selling to Quebec and Canada, compared per square foot and per pound, in Canadian dollars. Every number has a source and a date. No invented prices: when a supplier publishes nothing, we say “quote only”.")}</p>
  <div class="stamp" role="status">
    <span><b>{L("Mis à jour", "Updated")}</b> {L(stamp_fr, stamp_en)}</span>
    <span><b>{n_rows}</b> {L("prix", "prices")} · <b>{n_real}</b> {L("fournisseurs avec prix publiés", "suppliers with published prices")}</span>
    <span>{fx_txt}</span>
  </div>
  <nav class="toc" aria-label="{L("Sur cette page", "On this page")}">
    <a href="#comparateur">{L("Comparateur", "Comparison")}</a>
    <a href="#meilleurs">{L("Meilleurs prix", "Best prices")}</a>
    <a href="#calculateur">{L("Calculateur", "Calculator")}</a>
    <a href="#tendance">{L("Tendance", "Trend")}</a>
    <a href="#catalogue">{L("Nuances suivies", "Tracked grades")}</a>
    <a href="#calibres">{L("Calibres → mm", "Gauge → mm")}</a>
    <a href="#fournisseurs">{L("Fournisseurs", "Suppliers")}</a>
    <a href="#methode">{L("Méthode", "Method")}</a>
    <a href="#alerte">{L("Alerte prix", "Price alert")}</a>
  </nav>

  <section id="comparateur" class="panel">
    <h2>{L("Comparateur", "Comparison table")}</h2>
    <form class="filters" id="filters" onsubmit="return false">
      <label>{L("Famille", "Family")}<select name="family"><option value="">{L("Toutes", "All")}</option></select></label>
      <label>{L("Nuance", "Grade")}<select name="grade"><option value="">{L("Toutes", "All")}</option></select></label>
      <label>{L("Forme", "Form")}<select name="form"><option value="">{L("Tôle et plaque", "Sheet and plate")}</option></select></label>
      <label>{L("Épaisseur / format", "Thickness / size")}<select name="spec"><option value="">{L("Toutes", "All")}</option></select></label>
      <label>{L("Fournisseur", "Supplier")}<select name="supplier"><option value="">{L("Tous", "All")}</option></select></label>
      <label class="search">{L("Recherche", "Search")}<input type="search" name="q" placeholder="{L("ex. 14 ga, 5052, 1/4", "e.g. 14 ga, 5052, 1/4")}"></label>
      <label class="check"><input type="checkbox" name="qc" checked> {L("Achetable au Québec seulement", "Buyable in Quebec only")}</label>
      <label class="check"><input type="checkbox" name="cat"> {L("Nuances du catalogue seulement", "Catalogue grades only")}</label>
    </form>
    <p class="count" id="count" aria-live="polite"></p>
    <div class="table-wrap"><table class="cmp" id="cmp">
      <thead><tr>
        <th data-k="spec" aria-sort="none"><button type="button">{L("Spécification", "Spec")}</button></th>
        <th data-k="supplier"><button type="button">{L("Fournisseur", "Supplier")}</button></th>
        <th data-k="size"><button type="button">{L("Format", "Size")}</button></th>
        <th data-k="price" class="num"><button type="button">{L("Prix affiché", "Listed price")}</button></th>
        <th data-k="cad" class="num"><button type="button">CAD</button></th>
        <th data-k="sqft" class="num"><button type="button">$/{L("pi²", "sq ft")}</button></th>
        <th data-k="lb" class="num"><button type="button">$/lb</button></th>
        <th data-k="kg" class="num"><button type="button">$/kg</button></th>
        <th data-k="ft" class="num"><button type="button">$/{L("pi", "ft")}</button></th>
        <th>{L("Source · date", "Source · date")}</th>
      </tr></thead>
      <tbody><tr><td colspan="10">{L("Chargement du tableau… (JavaScript requis pour filtrer; les meilleurs prix sont aussi listés plus bas)", "Loading table… (JavaScript needed to filter; best prices are also listed below)")}</td></tr></tbody>
    </table></div>
    <p class="meta">{L("<span class=\"best-dot\"></span> = meilleur prix de la spécification parmi les fournisseurs achetables au Québec, en stock, hors valeurs aberrantes. $/lb, $/kg et $/pi² sont <em>calculés</em> à partir du prix affiché et du poids théorique (densité × épaisseur × surface) ou du poids d’expédition publié. Transport, taxes, coupe et droits non compris.",
                        "<span class=\"best-dot\"></span> = best price for the spec among suppliers buyable in Quebec, in stock, outliers excluded. $/lb, $/kg and $/sq ft are <em>computed</em> from the listed price and the theoretical weight (density × thickness × area) or the published shipping weight. Freight, taxes, cutting and duties not included.")}
      <a href="/prix/coupefab-prix-metaux.csv" download>{L("Télécharger le CSV", "Download the CSV")}</a> · <a href="/prix/donnees.json">JSON</a></p>
  </section>

  <section id="meilleurs" class="panel">
    <h2>{L("Meilleurs prix — tôle et plaque", "Best prices — sheet and plate")}</h2>
    <p>{L("Spécifications offertes par au moins deux fournisseurs. Comparaison au pied carré, en CAD.", "Specs offered by at least two suppliers. Compared per square foot, in CAD.")}</p>
    {best}
  </section>

  <section id="calculateur" class="panel">
    <h2>{L("Calculateur : poids et coût d’une pièce", "Calculator: part weight and cost")}</h2>
    <form class="calc" id="calc" onsubmit="return false">
      <label>{L("Matériau", "Material")}<select name="family"></select></label>
      <label>{L("Épaisseur (spécification)", "Thickness (spec)")}<select name="spec"></select></label>
      <label>{L("Largeur", "Width")}<input name="w" type="number" min="0" step="any" value="300"></label>
      <label>{L("Longueur", "Length")}<input name="l" type="number" min="0" step="any" value="500"></label>
      <label>{L("Unités", "Units")}<select name="unit"><option value="mm">mm</option><option value="in">{L("po", "in")}</option></select></label>
      <label>{L("Quantité", "Quantity")}<input name="qty" type="number" min="1" step="1" value="1"></label>
      <label>{L("Saignée (kerf) + espacement, mm", "Kerf + spacing, mm")}<input name="kerf" type="number" min="0" step="0.1" value="3"></label>
      <label>{L("Perte d’imbrication (nesting), %", "Nesting waste, %")}<input name="waste" type="number" min="0" max="90" step="1" value="15"></label>
    </form>
    <div id="calc-out" class="calc-out" aria-live="polite"></div>
    <p class="meta">{L("Poids = densité × épaisseur × surface de la pièce. Coût = surface consommée (pièce + saignée, puis perte d’imbrication) × prix au pi² le plus bas de chaque fournisseur pour cette épaisseur. Plasma : prévoir 1,5 à 3 mm de saignée selon la buse et l’ampérage.",
                        "Weight = density × thickness × part area. Cost = consumed area (part + kerf, then nesting waste) × each supplier’s lowest $/sq ft for that thickness. Plasma: allow 1.5 to 3 mm of kerf depending on nozzle and amperage.")}</p>
  </section>

  <section id="tendance" class="panel">
    <h2>{L("Indice CoupeFab : médiane $/lb par famille", "CoupeFab index: median $/lb by family")}</h2>
    <div id="chart" class="chart" role="img" aria-label="{L("Graphique de tendance des prix médians", "Median price trend chart")}"></div>
    <p class="meta">{L("Médiane quotidienne des prix au livre (CAD, calculés) de toutes les lignes tôle et plaque, tous fournisseurs avec prix publiés, hors liste indicative. L’historique commence le " + date_fr(index[0]["date"]) + "; la courbe se remplit à chaque relevé quotidien." if index else "",
                        "Daily median per-pound price (CAD, computed) of all sheet and plate rows from suppliers with published prices, excluding the indicative list. History starts on " + date_en(index[0]["date"]) + "; the line fills in with every daily survey." if index else "")}</p>
  </section>

  <section id="catalogue" class="panel">
    <h2>{L("Nuances suivies", "Tracked grades")}</h2>
    <p>{L("La liste de matériaux d’un atelier d’usinage et de fabrication québécois. Cliquez une nuance pour filtrer le comparateur. « Sur demande » : aucun fournisseur relevé ne publie de prix pour cette nuance.",
          "The material list of a Quebec machine and fabrication shop. Click a grade to filter the table. “Quote only”: no surveyed supplier publishes a price for that grade.")}</p>
    {coverage_html(rows, fr)}
  </section>

  <section id="calibres" class="panel">
    <h2>{L("Tableau des calibres : pouces et millimètres", "Gauge chart: inches and millimetres")}</h2>
    <p>{L("Un même calibre n’a pas la même épaisseur selon le métal. Toujours confirmer l’épaisseur réelle avec le fournisseur avant de programmer la coupe.",
          "The same gauge number is a different thickness depending on the metal. Always confirm the real thickness with the supplier before programming the cut.")}</p>
    {gauge_table_html(fr)}
  </section>

  <section id="fournisseurs" class="panel">
    <h2>{L("Fournisseurs relevés", "Suppliers surveyed")}</h2>
    {sup_live}
    <h3>{L("Sans prix publics (sur demande), bloqués ou pas encore couverts", "No public prices (quote only), blocked, or not yet covered")}</h3>
    {sup_static}
    <p class="meta">{L("Vous êtes un fournisseur et vous publiez vos prix? Écrivez-nous depuis la page À propos pour être ajouté.", "Are you a supplier publishing prices? Write to us from the About page to be added.")}</p>
  </section>

  <section id="methode" class="panel prose">
    <h2>{L("Méthode", "Method")}</h2>
    <ol>
      <li>{L("Un robot identifié (<code>CoupeFabPrixBot</code>) lit chaque jour les pages publiques des fournisseurs, une requête à la fois, en respectant robots.txt et son délai. Aucune connexion, aucun panier, aucun contournement de protection anti-robot : un site qui refuse est noté « bloqué ».",
             "An identified bot (<code>CoupeFabPrixBot</code>) reads suppliers’ public pages daily, one request at a time, honouring robots.txt and its crawl delay. No login, no cart, no bot-protection bypass: a site that refuses is marked “blocked”.")}</li>
      <li>{L("On garde le prix tel qu’affiché (devise, unité, format) et l’URL. Les prix en USD sont convertis au taux quotidien de la Banque du Canada.", "We keep the price as listed (currency, unit, size) and its URL. USD prices are converted at the Bank of Canada daily rate.")}</li>
      <li>{L("Pour les tôles vendues au format, on retient le plus grand format offert en ligne (souvent 48 × 96 po); pour les barres et tubes, la plus grande longueur. $/pi², $/lb et $/kg sont calculés.", "For sheet sold by size we keep the largest size offered online (often 48 × 96 in); for bar and tube, the longest length. $/sq ft, $/lb and $/kg are computed.")}</li>
      <li>{L("Une ligne dont le $/lb s’écarte fortement de la médiane de sa famille est signalée « à vérifier » et exclue des meilleurs prix, sans être supprimée.", "A row whose $/lb is far from its family median is flagged “to check” and excluded from best prices, but not deleted.")}</li>
      <li>{L("Prix avant taxes, transport, coupe et droits. Les prix changent : confirmez toujours auprès du fournisseur.", "Prices before taxes, freight, cutting and duties. Prices change: always confirm with the supplier.")}</li>
      <li>{L("Historique daté conservé dans le dépôt public du site (un fichier par jour). Aucun lien d’affiliation sur cette page pour l’instant; s’il y en a un jour, il sera identifié et expliqué dans la <a href=\"/divulgation/\">divulgation</a>.", "Dated history kept in the site’s public repository (one file per day). No affiliate links on this page for now; if that changes they will be labelled and explained in the <a href=\"/en/affiliate-disclosure/\">disclosure</a>.")}</li>
    </ol>
  </section>

  <section id="alerte" class="panel cta">
    <h2>{L("Alerte prix", "Price alert")}</h2>
    <p>{L("Recevez la variation de la semaine (acier, alu, inox) et les meilleures offres repérées, dans l’infolettre CoupeFab.", "Get the week’s price moves (steel, aluminum, stainless) and the best deals spotted, in the CoupeFab newsletter.")}</p>
    {form_newsletter("fr" if fr else "en")}
  </section>
</div>
<script src="/js/prix.js" defer></script>''')
        return "\n".join(H)

    meta = {"rows": n_rows, "suppliers": n_real, "generated_at": gen}
    return page(True), page(False), meta

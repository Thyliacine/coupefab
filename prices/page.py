"""Render the /prix/ and /en/sheet-prices/ pages from data/prices/latest.json.

Only numbers present in latest.json are shown. Derived values ($/lb, $/sq ft,
weights) are labelled as calculations on the page.
"""
import csv
import datetime as dt
import json
import re
import statistics
from pathlib import Path

from . import normalize as N
from .store import read_latest

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "prices"
MONTHS_FR = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre",
             "octobre", "novembre", "décembre"]
ELIGIBLE = {"oui", "cueillette", "a_confirmer"}  # can actually be bought by a Quebec shop
TIER_PCT = 10  # ±10 % around the median: "bon prix" / "cher"
# Surplus / clearance sellers: shown, but never "Meilleur prix" and never part of the median
# (decision of 26 Nov 2026: Mercier 40 = new "red corner" plates, grade not stated, stock varies).
SURPLUS = {"mercier40", "recyborg"}

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
        if g.lower().startswith("galv") or "galvan" in (r.get("description") or "").lower():
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


def spec_dims(r):
    """Numeric dimensions behind a spec key, for the nearest-spec search."""
    parts = (r.get("spec") or "").split("|")
    if r["form"] in ("tole", "plaque"):
        try:
            return [float(parts[2])]
        except (IndexError, ValueError):
            return None
    if len(parts) < 4 or ":" not in parts[3]:
        return None
    body = parts[3].split(":", 1)[1].replace("mm", "")
    try:
        return [float(x) for x in re.split(r"[x/]", body) if re.fullmatch(r"[\d.]+", x)]
    except ValueError:
        return None


def load():
    latest = read_latest(DATA)
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
        r["surplus"] = r["supplier"] in SURPLUS
        r["eligible"] = ships in ELIGIBLE and "rupture" not in avail and not r["outlier"] and not r["surplus"]
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
            r["metric"], r["munit"] = r.get("price_per_sqft_cad"), "sqft"
        else:
            sz = (r.get("size_label") or "").split(" — ")[0].strip()
            fl = N.FAMILY_LABELS[r["family"]]
            fo = N.FORM_LABELS[r["form"]]
            # normalized section + comparable grade group, so the same bar from different
            # suppliers lands in one comparison (see normalize.section_key / grade_group)
            sk, slab = N.section_key(r["form"], r["description"])
            if not sk:
                sk, slab = N.section_key(r["form"], r["description"] + " " + sz)
            gk, gfr, gen = N.grade_group(r["family"], r["grade"], r["form"], r.get("description"))
            r["grade_group"] = gk
            if sk:
                r["spec"] = f"{r['family']}|{gk}|{r['form']}|{sk}"
                r["spec_fr"] = f"{fl[0]} {gfr} — {fo[0].lower()} {slab}"
                r["spec_en"] = f"{fl[1]}, {gen} — {fo[1].lower()} {slab.replace(' po', ' in').replace('paroi', 'wall')}"
            else:
                r["spec"] = f"{r['family']}|{r['grade'] or '?'}|{r['form']}|{sz}"
                r["spec_fr"] = f"{fl[0]} {r['grade'] or ''} — {fo[0].lower()} {sz}".replace("  ", " ")
                r["spec_en"] = f"{fl[1]} {r['grade'] or ''} — {fo[1].lower()} {sz}".replace("  ", " ")
            r["metric"], r["munit"] = (r["price_per_ft_cad"], "ft") if r.get("price_per_ft_cad") else (r.get("price_per_lb_cad"), "lb")
        r["pool"] = f"{r.get('spec')}|{r.get('munit')}"  # never compare $/ft with $/lb
    # price-quality signals: compare each row's unit price to the median across suppliers of the same spec
    pools = {}
    for r in rows:
        if r.get("spec") and r["eligible"] and r.get("metric"):
            pools.setdefault(r["pool"], {}).setdefault(r["supplier"], []).append(r)
    stats = {}
    for key, by_sup in pools.items():
        if len(by_sup) < 2:
            continue  # one supplier: nothing to compare against
        mins = sorted(min(x["metric"] for x in v) for v in by_sup.values())
        best = min((x for v in by_sup.values() for x in v), key=lambda x: x["metric"])
        best["best"] = True
        stats[key] = (statistics.median(mins), len(by_sup), mins[-1])
    for r in rows:
        st = stats.get(r.get("pool"))
        if not (st and r.get("metric")):
            r["tier"] = "check" if r["outlier"] else ("surplus" if r.get("surplus") else None)
            continue
        med, n, _ = st
        r["median"], r["n_suppliers"] = round(med, 4), n
        r["pct"] = round((r["metric"] / med - 1) * 100, 1)
        if r["outlier"]:
            r["tier"], r["pct"] = "check", None
        elif r.get("surplus"):
            r["tier"] = "surplus"
        elif not r["eligible"]:
            r["tier"] = "oos" if "rupture" in (r.get("availability") or "").lower() else "ref"
        elif r.get("best"):
            r["tier"] = "best"
        elif r["pct"] <= -TIER_PCT:
            r["tier"] = "good"
        elif r["pct"] >= TIER_PCT:
            r["tier"] = "high"
        else:
            r["tier"] = "avg"
    # how many distinct suppliers publish a price for each spec (any shipping status), and,
    # for a spec with a single supplier, the closest specs (same family/grade group/form/unit)
    # that do have several suppliers, so a lone price can still be put in context.
    src = {}
    for r in rows:
        if r.get("spec") and r.get("metric"):
            src.setdefault(r["pool"], set()).add(r["supplier"])
    for r in rows:
        r["n_src"] = len(src.get(r.get("pool"), ()))
    specs = {}
    for r in rows:
        if not (r.get("spec") and r.get("metric")):
            continue
        e = specs.setdefault(r["pool"], {"spec": r["spec"], "fr": r["spec_fr"], "en": r["spec_en"], "munit": r["munit"],
                                         "n": r["n_src"], "min": None, "fam": r["family"], "form": r["form"],
                                         "grp": r["spec"].split("|")[1], "dims": spec_dims(r)})
        if r["eligible"] and (e["min"] is None or r["metric"] < e["min"]):
            e["min"] = round(r["metric"], 3)
    near = {}
    multi = [e for e in specs.values() if e["n"] >= 2 and e["min"] is not None and e["dims"]]
    for pool, e in specs.items():
        if e["n"] != 1 or not e["dims"]:
            continue
        cands = [m for m in multi if m["fam"] == e["fam"] and m["grp"] == e["grp"] and m["form"] == e["form"]
                 and m["munit"] == e["munit"] and len(m["dims"]) == len(e["dims"])]
        cands.sort(key=lambda m: sum(abs(a - b) / max(a, b, 1e-6) for a, b in zip(m["dims"], e["dims"])))
        if cands:
            near[e["spec"]] = [[m["spec"], m["fr"], m["en"], m["min"], m["munit"], m["n"]] for m in cands[:3]
                               if sum(abs(a - b) / max(a, b, 1e-6) for a, b in zip(m["dims"], e["dims"])) < 1.2]
    latest["_near"] = {k: v for k, v in near.items() if v}
    index = []
    if (DATA / "index.csv").exists():
        with (DATA / "index.csv").open() as f:
            index = list(csv.DictReader(f))
    return latest, rows, index


# ---------------------------------------------------------------------------
# Quick-buy targets
# ---------------------------------------------------------------------------
# Contact / quote pages (checked by hand, 26 Nov 2026). Plain links, no affiliate parameters.
QUOTE_URL = {
    "unitedstainless": "https://unitedstainless.ca/contact-us",
    "mercier40": "https://mercier40.ca/contactez-nous",
    "millennium": "https://millenniumalloys.ca/contact/",
    "nationalsalvage": "https://shop.nationalsalvage.ca/pages/contact",
}
QUOTE_URL_STATIC = {
    "Metal Supermarkets": "https://www.metalsupermarkets.com/contact-us/",
    "Russel Metals": "https://www.russelmetals.com/en/contact/",
    "Acier Leroux (Leroux Steel)": "https://www.russelmetals.com/en/contact/",
    "Acier Picard": "https://groupepicard.ca/contactez-acier-picard/",
    "Marmen": "https://marmeninc.com/contact",
    "Acier Lachine": "https://www.acierlachine.com/demande-de-soumission/",
    "Multi-Plis": "https://www.multiplis.qc.ca/obtenir-un-prix/",
    "North York Iron": "https://northyorkiron.com/contact-nyi/",
    "GTA Steel": "https://gtasteel.com/contact-us/",
}
SHIP_LBL = {"oui": ("Livre au Québec", "Ships to Quebec"), "cueillette": ("Cueillette au Québec", "Pickup in Quebec"),
            "indicatif": ("Prix indicatif", "Indicative price"), "a_confirmer": ("Livraison à confirmer", "Shipping TBC"),
            "non": ("Repère hors Québec", "Benchmark, outside QC"), "repere": ("Repère hors Québec", "Benchmark, outside QC")}
TIER_LBL = {"best": ("Meilleur prix", "Best price"), "good": ("Bon prix", "Good price"), "avg": ("Dans la moyenne", "Average"),
            "high": ("Cher", "Expensive"), "ref": ("Repère", "Benchmark"), "oos": ("Rupture", "Out of stock"),
            "check": ("À vérifier", "To check"), "surplus": ("Surplus / indicatif", "Surplus / indicative")}

# Popular specs shown as "best deal" cards at the top of Comparer.
CARDS = [
    ("acier|noir|0.2500", None, ("Plaque A36 / HR", "A36 / HR plate"), ("1/4 po · 6,35 mm", "1/4 in · 6.35 mm")),
    ("acier|noir|0.1875", None, ("Plaque A36 / HR", "A36 / HR plate"), ("3/16 po · 4,76 mm", "3/16 in · 4.76 mm")),
    ("acier|noir|0.0598", None, ("Tôle d’acier doux", "Mild steel sheet"), ("16 ga · 1,52 mm", "16 ga · 1.52 mm")),
    ("acier|noir|0.0747", None, ("Tôle d’acier doux", "Mild steel sheet"), ("14 ga · 1,90 mm", "14 ga · 1.90 mm")),
    ("acier|noir|0.1196", None, ("Tôle d’acier doux", "Mild steel sheet"), ("11 ga · 3,04 mm", "11 ga · 3.04 mm")),
    ("aluminium|5052|0.0630", None, ("Aluminium 5052", "Aluminum 5052"), ("0,063 po · 1,60 mm", "0.063 in · 1.60 mm")),
    ("aluminium|5052|0.1250", None, ("Aluminium 5052", "Aluminum 5052"), ("0,125 po · 3,18 mm", "0.125 in · 3.18 mm")),
    ("aluminium|6061|0.2500", None, ("Plaque alu 6061", "6061 aluminum plate"), ("1/4 po · 6,35 mm", "1/4 in · 6.35 mm")),
    ("inox|304|0.0625", "2B", ("Inox 304 fini 2B", "304 stainless, 2B finish"), ("16 ga · 1,59 mm", "16 ga · 1.59 mm")),
]


def buy_action(r, sup):
    """(kind, url) for a row's main button. kind: buy | see | quote."""
    s = sup.get(r["supplier"], {})
    ships = s.get("ships_qc")
    if ships == "indicatif":
        return "quote", QUOTE_URL.get(r["supplier"]) or r["url"]
    if ships == "oui":
        return "buy", r.get("buy_url") or r["url"]
    return "see", r.get("buy_url") or r["url"]  # url may be None: no link beats a link that shows nothing


def compact(latest, rows, index):
    keys = ["supplier", "family", "grade", "in_catalogue", "form", "description", "size_label", "thickness_in",
            "thickness_mm", "gauge", "width_in", "length_in", "length_ft", "price", "currency", "unit", "price_cad",
            "price_per_lb_cad", "price_per_kg_cad", "price_per_sqft_cad", "price_per_ft_cad", "weight_lb",
            "availability", "url", "buy_url", "fetched_at", "source_updated", "notes", "outlier", "eligible", "spec",
            "spec_fr", "spec_en", "best", "metric", "munit", "median", "pct", "tier", "n_suppliers", "n_src"]
    sups = {}
    for k, v in latest["suppliers"].items():
        sups[k] = {kk: v.get(kk) for kk in ("name", "city", "region", "currency", "ships_qc", "shipping", "shipping_en", "site")}
        sups[k]["quote_url"] = QUOTE_URL.get(k)
    base = {
        "generated_at": latest["generated_at"], "fx": latest["fx"], "suppliers": sups,
        "status": latest["status"], "catalogue": latest["catalogue"],
        "families": {k: list(v) for k, v in N.FAMILY_LABELS.items()},
        "forms": {k: list(v) for k, v in N.FORM_LABELS.items()},
        "density": N.DENSITY, "keys": keys, "tier_pct": TIER_PCT, "index": index,
        "near": latest.get("_near", {}),
    }
    full = dict(base, part="all", rows=[[r.get(k) for k in keys] for r in rows])
    light = dict(base, part="sheet", rows=[[r.get(k) for k in keys] for r in rows if r["form"] in ("tole", "plaque")],
                 near={k: v for k, v in base["near"].items() if k.count("|") == 2})
    return full, light


def date_short_fr(iso):
    d = dt.date.fromisoformat(iso[:10])
    return f"{d.day} {MONTHS_FR[d.month-1][:4].rstrip('.')}{'.' if len(MONTHS_FR[d.month-1]) > 4 else ''}"


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
                cells.append(f'<li class="has" data-family="{fam}" data-grade="{esc(plain(g))}"><button type="button" class="grade-pick" data-family="{fam}" data-grade="{esc(plain(g))}">{esc(plain(g))}</button><span>{esc(fls)}</span></li>')
            else:
                cells.append(f'<li class="none"><b>{esc(g)}</b><span>{"sur demande" if fr else "quote only"}</span></li>')
        out.append(f"<div class=\"cov\"><h3>{fl}</h3><ul>{''.join(cells)}</ul></div>")
    return "<div class=\"coverage\">" + "".join(out) + "</div>"


def cards_html(rows, sup, fr):
    L = (lambda a, b: a if fr else b)
    money = (lambda x: f"{nfr(x)} $") if fr else (lambda x: f"${nen(x)}")
    pct = (lambda p: (f"{'+' if p > 0 else '−'}{nfr(abs(p), 0)} %") if fr else (f"{'+' if p > 0 else '−'}{abs(p):.0f}%"))
    out = []
    for spec, must, title, sub in CARDS:
        rs = [r for r in rows if r.get("spec") == spec and r["eligible"] and r.get("metric")
              and (not must or must.lower() in r["description"].lower())]
        by = {}
        for r in rs:
            if r["supplier"] not in by or r["metric"] < by[r["supplier"]]["metric"]:
                by[r["supplier"]] = r
        ranked = sorted(by.values(), key=lambda r: r["metric"])
        q = f"comparer?spec={spec}" + (f"&q={must}" if must else "")
        q_en = q.replace("comparer", "compare")
        if len(ranked) < 2:
            continue
        mins = [r["metric"] for r in ranked]
        med = statistics.median(mins)
        b, nxt, worst = ranked[0], ranked[1], ranked[-1]
        kind, url = buy_action(b, sup)
        sname = sup[b["supplier"]]["name"]
        btn = L("Acheter", "Buy") if kind == "buy" else L("Voir l’offre", "View offer")
        size = b["size_label"] if fr else b["size_label"].replace(" po", " in")
        lb = b.get("price_per_lb_cad")
        ship = SHIP_LBL.get(sup[b["supplier"]]["ships_qc"], ("", ""))[0 if fr else 1]
        usd = " · USD→CAD" if b["currency"] == "USD" else ""
        out.append(f'''<article class="px-card">
  <header><h3>{esc(title[0 if fr else 1])}</h3><p>{esc(sub[0 if fr else 1])}</p></header>
  <p class="px-card-price"><b>{money(b["metric"])}</b><span>/{L("pi²", "sq ft")}</span>{f'<small>≈ {money(lb)}/lb</small>' if lb else ""}</p>
  <p class="px-card-sup"><span class="px-tier px-t-best">{L("Meilleur prix", "Best price")}</span> <b>{esc(sname)}</b> <span class="px-muted">{esc(ship)}{usd}</span></p>
  <p class="px-card-meta">{L("Feuille", "Sheet")} {esc(size)} : <b>{money(b["price_cad"])}</b> · <span class="px-down">{pct((b["metric"] / med - 1) * 100)}</span> {L("vs médiane", "vs median")} ({money(med)}, {len(ranked)} {L("fourn.", "suppliers")})</p>
  {f'<a class="px-btn px-btn-buy" href="{esc(url)}" target="_blank" rel="noopener nofollow">{esc(btn)} <span aria-hidden="true">↗</span></a>' if url else ""}
  <ul class="px-card-alt">
    <li>{L("2ᵉ", "2nd")} : {esc(sup[nxt["supplier"]]["name"])} {money(nxt["metric"])} <span class="px-up">{pct((nxt["metric"] / b["metric"] - 1) * 100)}</span></li>
    {f'<li>{L("Plus cher", "Priciest")} : {esc(sup[worst["supplier"]]["name"])} {money(worst["metric"])} <span class="px-up">{pct((worst["metric"] / b["metric"] - 1) * 100)}</span></li>' if worst is not nxt else ""}
  </ul>
  <a class="px-card-more" href="#{L(q, q_en)}" data-goto="{esc(spec)}"{f' data-q="{must}"' if must else ""}>{L("Comparer les", "Compare all")} {sum(1 for r in rows if r.get("spec") == spec)} {L("prix", "prices")} →</a>
</article>''')
    return '<div class="px-cards">' + "".join(out) + "</div>"


def suppliers_html(latest, rows, fr):
    L = (lambda a, b: a if fr else b)
    sup, st = latest["suppliers"], latest["status"]
    counts = {}
    for r in rows:
        counts[r["supplier"]] = counts.get(r["supplier"], 0) + 1
    li = []
    for sid, s in sup.items():
        n = counts.get(sid, 0)
        ok = st.get(sid, {}).get("ok", False)
        lab = SHIP_LBL.get(s["ships_qc"], ("", ""))[0 if fr else 1]
        note = plain(s["shipping"] if fr else s.get("shipping_en", s["shipping"]))
        state = L(f"{n} lignes", f"{n} rows") + ("" if ok else L(" · relevé en échec, données précédentes", " · fetch failed, previous data"))
        q = QUOTE_URL.get(sid)
        li.append(f'<li><div><strong>{esc(s["name"])}</strong> <span class="px-muted">{esc(s["city"])} · {s["currency"]}</span><br>'
                  f'<span class="px-chip">{esc(lab)}</span> <span class="px-muted">{state}</span><p>{esc(note)}</p></div>'
                  f'<div class="px-sup-act"><a class="px-btn px-btn-ghost" href="{esc(s["site"])}" target="_blank" rel="noopener nofollow">{L("Site", "Website")} ↗</a>'
                  + (f'<a class="px-btn px-btn-ghost" href="{esc(q)}" target="_blank" rel="noopener nofollow">{L("Demander un prix", "Request a quote")} ↗</a>' if q else "")
                  + "</div></li>")
    st_lbl = {"sur_demande": ("Prix sur demande", "Quote only"), "bloque": ("Bloqué (non lu)", "Blocked (not read)"),
              "non_couvert": ("Pas encore couvert", "Not covered yet")}
    li2 = []
    for s in latest["suppliers_static"]:
        lab = st_lbl[s["status"]][0 if fr else 1]
        q = QUOTE_URL_STATIC.get(s["name"])
        act = (f'<a class="px-btn px-btn-quote" href="{esc(q)}" target="_blank" rel="noopener nofollow">{L("Demander un prix", "Request a quote")} ↗</a>' if q
               else f'<a class="px-btn px-btn-ghost" href="{esc(s["url"])}" target="_blank" rel="noopener nofollow">{L("Voir le site", "Visit site")} ↗</a>')
        li2.append(f'<li><div><strong>{esc(s["name"])}</strong> <span class="px-muted">{esc(s["city"])}</span><br><span class="px-chip px-chip-muted">{lab}</span>'
                   f'<p>{esc(plain(s["note"] if fr else s["note_en"]))}</p></div><div class="px-sup-act">{act}</div></li>')
    return '<ul class="px-suppliers">' + "".join(li) + "</ul>", '<ul class="px-suppliers">' + "".join(li2) + "</ul>"


TABS = [("comparer", "compare", "Comparer", "Compare"), ("calculateur", "calculator", "Calculateur", "Calculator"),
        ("tendances", "trends", "Tendances", "Trends"), ("alliages", "grades", "Alliages & épaisseurs", "Alloys & thicknesses"),
        ("methode", "method", "Méthode & sources", "Method & sources")]
# old single-page anchors still land on the right tab
TAB_ALIASES = {"comparateur": 0, "meilleurs": 0, "tendance": 2, "catalogue": 3, "calibres": 3, "nuances": 3, "fournisseurs": 4, "alerte": 4}


def plain(txt):
    """Display wording: the data keeps the shop term « nuance »; the site says « alliage » (owner request)."""
    return (txt or "").replace("nuance non précisée", "alliage non précisé").replace("Nuance non précisée", "Alliage non précisé")


def ver(rel):
    import hashlib
    return hashlib.sha1((ROOT / rel).read_bytes()).hexdigest()[:8]


def render(form_newsletter, site):
    latest, rows, index = load()
    full, light = compact(latest, rows, index)
    (ROOT / "prix").mkdir(exist_ok=True)
    (ROOT / "prix" / "donnees.json").write_text(plain(json.dumps(full, ensure_ascii=False, separators=(",", ":"))))
    (ROOT / "prix" / "donnees-toles.json").write_text(plain(json.dumps(light, ensure_ascii=False, separators=(",", ":"))))
    # public CSV of the current snapshot
    import io
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
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
    n_cmp = len({r["pool"] for r in rows if r.get("tier") in ("best", "good", "avg", "high")})
    sup = latest["suppliers"]
    stamp_fr = f"{date_fr(gen)}, {gen[11:16]} (heure de Montréal)"
    stamp_en = f"{date_en(gen)}, {gen[11:16]} (Montreal time)"
    tabmap = {t[0]: i for i, t in enumerate(TABS)}
    tabmap.update({t[1]: i for i, t in enumerate(TABS)})
    tabmap.update(TAB_ALIASES)

    def page(fr):
        L = (lambda a, b: a if fr else b)
        tid = [t[0 if fr else 1] for t in TABS]
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
            "license": "https://creativecommons.org/licenses/by/4.0/",
            "keywords": ["prix acier", "prix tôle", "steel price Canada", "aluminium", "inox", "plasma CNC", "Québec"],
            "variableMeasured": ["prix CAD", "CAD/lb", "CAD/kg", "CAD/pi²", "CAD/pi linéaire"],
            "distribution": [
                {"@type": "DataDownload", "encodingFormat": "text/csv", "contentUrl": site + "/prix/coupefab-prix-metaux.csv"},
                {"@type": "DataDownload", "encodingFormat": "application/json", "contentUrl": site + "/prix/donnees.json"}],
        }
        fx_txt = L(f"1 USD = {nfr(fx['rate'],4)} CAD (Banque du Canada, {date_fr(fx['date'])})",
                   f"1 USD = {fx['rate']:.4f} CAD (Bank of Canada, {date_en(fx['date'])})")
        tabs_html = "".join(
            f'<a role="tab" id="tab-{tid[i]}" href="#{tid[i]}" aria-controls="p-{tid[i]}" aria-selected="{"true" if i == 0 else "false"}"'
            f' tabindex="{0 if i == 0 else -1}" data-i="{i}">{esc(t[2] if fr else t[3])}</a>' for i, t in enumerate(TABS))
        boot = ("(function(){var a=document.getElementById('prix-app');a.classList.add('js');"
                f"var m={json.dumps(tabmap)},h=(location.hash.slice(1).split('?')[0]||'').toLowerCase(),i=m[h]||0;"
                "a.setAttribute('data-tab',i);var p=a.querySelectorAll('.px-panel');for(var k=0;k<p.length;k++)p[k].classList.toggle('is-active',k==i);"
                "var t=a.querySelectorAll('[role=tab]');for(k=0;k<t.length;k++){t[k].setAttribute('aria-selected',k==i);t[k].tabIndex=k==i?0:-1;}"
                "window.__pxData=fetch('/prix/donnees-toles.json').then(function(r){return r.json()});})();")
        legend = "".join(f'<li><span class="px-tier px-t-{k}">{TIER_LBL[k][0 if fr else 1]}</span> {d}</li>' for k, d in [
            ("best", L("le plus bas de la spécification (≥ 2 fournisseurs achetables au Québec)", "lowest for the spec (≥ 2 suppliers buyable in Quebec)")),
            ("good", L(f"au moins {TIER_PCT} % sous la médiane", f"at least {TIER_PCT}% below the median")),
            ("avg", L(f"à ± {TIER_PCT} % de la médiane", f"within ±{TIER_PCT}% of the median")),
            ("high", L(f"au moins {TIER_PCT} % au-dessus de la médiane", f"at least {TIER_PCT}% above the median")),
            ("ref", L("repère (non achetable au Québec ou indicatif) : écart affiché, jamais « meilleur »", "benchmark (not buyable in Quebec, or indicative): gap shown, never “best”")),
            ("check", L("valeur aberrante, exclue des comparaisons", "outlier, excluded from comparisons"))])
        H = []
        H.append(f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>')
        H.append(f'''<link rel="stylesheet" href="/css/prix.css?v={ver("css/prix.css")}">
<div class="px" id="prix-app" data-lang="{L("fr","en")}">
<script>{boot}</script>
<section class="px-hero">
  <div class="px-hero-top">
    <div>
      <p class="px-kicker">{L("Comparateur de prix des métaux", "Metal price comparison")} <span class="px-beta">{L("bêta", "beta")}</span></p>
      <h1>{L("Prix des tôles et des métaux au Québec", "Sheet-metal and metal prices in Quebec")}</h1>
      <p class="px-lede">{L(f"{nfr(n_rows, 0)} prix publiés chez {n_real} fournisseurs, en dollars canadiens, au pi² et à la livre. Comparez, repérez la meilleure offre et achetez directement chez le fournisseur.",
                              f"{n_rows:,} published prices from {n_real} suppliers, in Canadian dollars, per sq ft and per pound. Compare, spot the best deal and buy straight from the supplier.")}</p>
    </div>
    <p class="px-stamp" role="status"><span><b>{L("Mis à jour", "Updated")}</b> {L(stamp_fr, stamp_en)}</span><span>{fx_txt}</span></p>
  </div>
</section>
  <form class="px-search" id="px-search" role="search" aria-label="{L("Recherche rapide de prix", "Quick price search")}" onsubmit="return false">
    <label class="px-q"><span>{L("Rechercher", "Search")}</span><input type="search" name="q" autocomplete="off" placeholder="{L("ex. 14 ga, 5052 0.063, 1/4 A36, 304 2B", "e.g. 14 ga, 5052 0.063, 1/4 A36, 304 2B")}"></label>
    <button type="button" class="px-ftog" aria-expanded="false" aria-controls="px-search">{L("Filtres", "Filters")} <span data-nf></span></button>
    <label><span>{L("Famille", "Family")}</span><select name="family"><option value="">{L("Toutes", "All")}</option></select></label>
    <label><span>{L("Alliage / grade", "Alloy / grade")}</span><select name="grade"><option value="">{L("Toutes", "All")}</option></select></label>
    <label><span>{L("Forme", "Form")}</span><select name="form"><option value="">{L("Toutes", "All")}</option></select></label>
    <label><span>{L("Épaisseur / dim.", "Thickness / size")}</span><select name="spec"><option value="">{L("Toutes", "All")}</option></select></label>
    <label><span>{L("Format", "Size")}</span><select name="size"><option value="">{L("Tous", "All")}</option></select></label>
    <button type="button" class="px-reset" data-reset>{L("Réinitialiser", "Reset")}</button>
  </form>

<nav class="px-tabs" role="tablist" aria-label="{L("Sections du comparateur", "Price tool sections")}">{tabs_html}</nav>

<section class="px-panel is-active" id="p-{tid[0]}" role="tabpanel" aria-labelledby="tab-{tid[0]}" tabindex="-1">
  <details class="px-caveat">
    <summary><b>{L("Tous les prix en CAD, avant taxes, transport et coupe.", "All prices in CAD, before taxes, freight and cutting.")}</b> <span class="px-more">{L("Détails", "Details")}</span></summary>
    <p>{L(f"Les prix en USD sont convertis au taux de la Banque du Canada ({fx_txt.split(' (')[0]}). Pour un fournisseur américain, ajoutez le transport transfrontalier, le courtage et les droits ou surtaxes en vigueur (l’acier et l’aluminium importés des États-Unis peuvent être visés par des surtaxes canadiennes) : vérifiez avant de commander.",
       f"USD prices are converted at the Bank of Canada rate ({fx_txt.split(' (')[0]}). From a US supplier, add cross-border freight, brokerage and any duties or surtaxes in force (steel and aluminum imported from the US may be subject to Canadian surtaxes): check before you order.")}</p>
  </details>
  <div class="px-deals">
  <h2 class="px-h2">{L("Meilleures offres du jour", "Today’s best deals")}</h2>
  {cards_html(rows, sup, fr)}
  </div>
  <div class="px-results-head">
    <h2 class="px-h2" id="px-results-title">{L("Tous les prix", "All prices")}</h2>
    <p class="px-count" id="px-count" aria-live="polite"></p>
    <p class="cf-showing" id="px-showing"></p>
    <div class="px-tools">
      <label class="px-check"><input type="checkbox" name="qc" form="px-search" checked> {L("Achetable au Québec", "Buyable in Quebec")}</label>
      <label class="px-check"><input type="checkbox" name="cmp" form="px-search"> {L("Comparables seulement", "Comparable only")}</label>
      <label class="px-check"><input type="checkbox" name="cat" form="px-search"> {L("Matériaux courants d’atelier", "Common shop materials")}</label>
      <label class="px-sort"><span>{L("Trier", "Sort")}</span><select id="px-sort">
        <option value="spec">{L("Produit, puis prix", "Product, then price")}</option>
        <option value="metric">{L("Prix unitaire ↑", "Unit price ↑")}</option>
        <option value="pct">{L("Écart vs médiane ↑", "Gap vs median ↑")}</option>
        <option value="price">{L("Prix affiché ↑", "Listed price ↑")}</option>
        <option value="lb">$/lb ↑</option>
        <option value="supplier">{L("Fournisseur", "Supplier")}</option>
      </select></label>
    </div>
  </div>
  <dl class="px-howto" aria-label="{L("Comment lire le tableau", "How to read the table")}">
    <div><dt>{L("Prix affiché", "Listed price")}</dt><dd>{L("Le prix du fournisseur pour le format indiqué, en $ CA.", "The supplier’s price for the size shown, in CAD.")}</dd></div>
    <div><dt>{L("Prix unitaire", "Unit price")}</dt><dd>{L("Ramené au pi², au pied ou à la livre pour comparer des formats différents.", "Brought to $/sq ft, $/ft or $/lb so different sizes compare fairly.")}</dd></div>
    <div><dt>{L("Écart vs médiane", "vs median price")}</dt><dd>{L(f"Comparaison avec le prix médian des fournisseurs pour le même produit : vert = moins cher, rouge = plus cher (± {TIER_PCT} %).", f"Compared with the median supplier price for the same product: green = cheaper, red = pricier (±{TIER_PCT}%).")}</dd></div>
  </dl>
  <details class="px-legend"><summary>{L("Que veulent dire les étiquettes « Meilleur prix », « Bon prix »…?", "What do the “Best price”, “Good price”… labels mean?")}</summary>
    <ul>{legend}</ul>
    <p>{L("La médiane est calculée sur le meilleur prix unitaire de chaque fournisseur achetable au Québec pour la même spécification (même famille, sous-classe et épaisseur; $/pi² pour la tôle et la plaque, $/pi ou $/lb pour les barres et tubes). Sans au moins deux fournisseurs, aucune étiquette : on n’invente pas de comparaison.",
          "The median is taken over each Quebec-buyable supplier’s best unit price for the same spec (same family, sub-class and thickness; $/sq ft for sheet and plate, $/ft or $/lb for bar and tube). With fewer than two suppliers there is no label: we don’t invent a comparison.")}</p>
  </details>
  <div class="px-table-wrap" id="px-table-wrap">
    <table class="px-table" id="px-table">
      <caption class="px-sr">{L("Prix publiés, triables", "Published prices, sortable")}</caption>
      <thead><tr>
        <th scope="col" data-k="spec" aria-sort="ascending"><button type="button">{L("Produit", "Product")}</button></th>
        <th scope="col" data-k="supplier"><button type="button">{L("Fournisseur", "Supplier")}</button></th>
        <th scope="col" data-k="size">{L("Format", "Size")}</th>
        <th scope="col" data-k="price" class="num"><button type="button">{L("Prix affiché", "Listed price")}</button></th>
        <th scope="col" data-k="metric" class="num"><button type="button">{L("Prix unitaire", "Unit price")}</button></th>
        <th scope="col" data-k="pct"><button type="button">{L("Écart vs médiane", "vs median price")}</button></th>
        <th scope="col"><span class="px-sr">{L("Acheter", "Buy")}</span></th>
      </tr></thead>
      <tbody><tr><td colspan="7" class="px-loading">{L("Chargement des prix…", "Loading prices…")}</td></tr></tbody>
    </table>
  </div>
  <nav class="cf-pager" id="px-pager" hidden></nav>
  <noscript><p>{L("Le tableau filtrable demande JavaScript. Toutes les données sont dans le", "The filterable table needs JavaScript. All data is in the")} <a href="/prix/coupefab-prix-metaux.csv">CSV</a>.</p></noscript>
  <p class="px-foot">{L("Chaque ligne garde sa source et sa date de relevé. $/pi², $/pi et $/lb sont calculés à partir du prix affiché et du poids théorique ou publié.", "Every row keeps its source and survey date. $/sq ft, $/ft and $/lb are computed from the listed price and the theoretical or published weight.")}
    <a href="/prix/coupefab-prix-metaux.csv" download>CSV</a> · <a href="/prix/donnees.json">JSON</a> · <a href="https://creativecommons.org/licenses/by/4.0/deed.{L("fr","en")}" rel="license noopener">CC BY 4.0</a></p>
</section>

<section class="px-panel" id="p-{tid[1]}" role="tabpanel" aria-labelledby="tab-{tid[1]}" tabindex="-1">
  <h2 class="px-h2">{L("Calculateur : poids et coût d’une pièce", "Calculator: part weight and cost")}</h2>
  <form class="px-calc" id="px-calc" onsubmit="return false">
    <label><span>{L("Matériau", "Material")}</span><select name="family"></select></label>
    <label class="px-wide"><span>{L("Épaisseur", "Thickness")}</span><select name="spec"></select></label>
    <label><span>{L("Largeur", "Width")}</span><input name="w" type="number" min="0" step="any" value="300" inputmode="decimal"></label>
    <label><span>{L("Longueur", "Length")}</span><input name="l" type="number" min="0" step="any" value="500" inputmode="decimal"></label>
    <label><span>{L("Unités", "Units")}</span><select name="unit"><option value="mm">mm</option><option value="in">{L("po", "in")}</option></select></label>
    <label><span>{L("Quantité", "Quantity")}</span><input name="qty" type="number" min="1" step="1" value="1" inputmode="numeric"></label>
    <label><span>{L("Saignée + espacement (mm)", "Kerf + spacing (mm)")}</span><input name="kerf" type="number" min="0" step="0.1" value="3" inputmode="decimal"></label>
    <label><span>{L("Perte d’imbrication (%)", "Nesting waste (%)")}</span><input name="waste" type="number" min="0" max="90" step="1" value="15" inputmode="numeric"></label>
  </form>
  <div id="px-calc-out" class="px-calc-out" aria-live="polite"></div>
  <p class="px-foot">{L("Poids = densité × épaisseur × surface. Coût = surface consommée (pièce + saignée, puis perte d’imbrication) × prix au pi² le plus bas de chaque fournisseur. Plasma : 1,5 à 3 mm de saignée selon la buse et l’ampérage. Avant taxes, transport et coupe.",
                         "Weight = density × thickness × area. Cost = consumed area (part + kerf, then nesting waste) × each supplier’s lowest $/sq ft. Plasma: 1.5 to 3 mm of kerf depending on nozzle and amperage. Before taxes, freight and cutting.")}</p>
</section>

<section class="px-panel" id="p-{tid[2]}" role="tabpanel" aria-labelledby="tab-{tid[2]}" tabindex="-1">
  <h2 class="px-h2">{L("Indice CoupeFab : médiane $/lb par famille", "CoupeFab index: median $/lb by family")}</h2>
  <div id="px-chart" class="px-chart" role="img" aria-label="{L("Graphique de tendance des prix médians", "Median price trend chart")}"></div>
  <div id="px-spread"></div>
  <p class="px-foot">{L("Médiane quotidienne des prix à la livre (CAD, calculés) de toutes les lignes tôle et plaque des fournisseurs à prix publiés, hors liste indicative. Historique depuis le " + date_fr(index[0]["date"]) + "; la courbe se remplit à chaque relevé." if index else "",
                         "Daily median per-pound price (CAD, computed) of all sheet and plate rows from suppliers with published prices, excluding the indicative list. History since " + date_en(index[0]["date"]) + "; the line fills in with every survey." if index else "")}</p>
</section>

<section class="px-panel" id="p-{tid[3]}" role="tabpanel" aria-labelledby="tab-{tid[3]}" tabindex="-1">
  <h2 class="px-h2">{L("Alliages suivis", "Tracked alloys and grades")}</h2>
  <p>{L("La liste de matériaux d’un atelier d’usinage et de fabrication québécois. Cliquez un alliage pour voir ses prix. « Sur demande » : aucun fournisseur relevé ne publie de prix.",
        "The material list of a Quebec machine and fabrication shop. Click a grade to see its prices. “Quote only”: no surveyed supplier publishes a price.")}</p>
  {coverage_html(rows, fr)}
  <h2 class="px-h2">{L("Calibres : pouces et millimètres", "Gauges: inches and millimetres")}</h2>
  <p>{L("Un même calibre n’a pas la même épaisseur selon le métal. Confirmez l’épaisseur réelle avant de programmer la coupe.",
        "The same gauge is a different thickness depending on the metal. Confirm the real thickness before programming the cut.")}</p>
  {gauge_table_html(fr)}
</section>

<section class="px-panel" id="p-{tid[4]}" role="tabpanel" aria-labelledby="tab-{tid[4]}" tabindex="-1">
  <h2 class="px-h2">{L("Fournisseurs relevés", "Suppliers surveyed")}</h2>
  {sup_live}
  <h2 class="px-h2">{L("Prix sur demande, bloqués ou pas encore couverts", "Quote only, blocked or not yet covered")}</h2>
  <p>{L("Ces fournisseurs ne publient pas de prix lisibles. Demandez une soumission directement : les liens mènent à leur page de contact ou de soumission.",
        "These suppliers don’t publish readable prices. Ask them directly: links go to their contact or quote page.")}</p>
  {sup_static}
  <p class="px-foot"><a href="{L("/fournisseurs/", "/en/suppliers/")}">{L("Voir le répertoire complet des fournisseurs (Québec et Canada) →", "See the full supplier directory (Quebec and Canada) →")}</a></p>
  <h2 class="px-h2">{L("Méthode", "Method")}</h2>
  <ol class="px-method">
    <li>{L("Un robot identifié (<code>CoupeFabPrixBot</code>) lit les pages publiques des fournisseurs, une requête à la fois, en respectant robots.txt et son délai. Aucune connexion, aucun panier, aucun contournement anti-robot : un site qui refuse est noté « bloqué ».",
           "An identified bot (<code>CoupeFabPrixBot</code>) reads suppliers’ public pages, one request at a time, honouring robots.txt and its crawl delay. No login, no cart, no bot-protection bypass: a site that refuses is marked “blocked”.")}</li>
    <li>{L("Fréquence : tôle et plaque chaque jour; barres, tubes et tuyaux chaque semaine. Chaque ligne affiche sa propre date.", "Frequency: sheet and plate daily; bar, tube and pipe weekly. Each row shows its own date.")}</li>
    <li>{L("On garde le prix tel qu’affiché (devise, unité, format) et l’URL. USD → CAD au taux quotidien de la Banque du Canada.", "We keep the price as listed (currency, unit, size) and its URL. USD → CAD at the Bank of Canada daily rate.")}</li>
    <li>{L("Tôle vendue au format : on retient le plus grand format offert en ligne (souvent 48 × 96 po); barres et tubes : la plus grande longueur. $/pi², $/lb et $/kg sont calculés.", "Sheet sold by size: we keep the largest size offered online (often 48 × 96 in); bar and tube: the longest length. $/sq ft, $/lb and $/kg are computed.")}</li>
    <li>{L(f"Étiquettes de prix : écart du prix unitaire à la médiane des fournisseurs de la même spécification (± {TIER_PCT} %). Les repères (hors Québec, indicatifs) et les ruptures ne peuvent pas être « meilleur prix ». Une valeur aberrante est signalée « à vérifier », sans être supprimée.",
           f"Price labels: gap between the unit price and the median of suppliers for the same spec (±{TIER_PCT}%). Benchmarks (outside Quebec, indicative) and out-of-stock rows can’t be “best price”. An outlier is flagged “to check”, never deleted.")}</li>
    <li>{L("Boutons « Acheter » et « Voir chez » : lien direct vers la fiche du produit chez le fournisseur (ou sa ligne sur la page catégorie quand le fournisseur n’a pas de fiche par produit). Liens ordinaires, sans paramètre d’affiliation; voir la <a href=\"/divulgation/\">divulgation</a>.",
           "“Buy” and “View at” buttons: direct link to the product page at the supplier (or its row on the category page when the supplier has no per-product page). Plain links, no affiliate parameters; see the <a href=\"/en/affiliate-disclosure/\">disclosure</a>.")}</li>
    <li>{L("Licence : les données compilées (tableau, CSV, JSON, historique) sont publiées sous <a href=\"https://creativecommons.org/licenses/by/4.0/deed.fr\" rel=\"license\">CC BY 4.0</a>; réutilisation libre en citant CoupeFab. Les prix restent ceux des fournisseurs cités.",
           "Licence: the compiled data (table, CSV, JSON, history) is published under <a href=\"https://creativecommons.org/licenses/by/4.0/\" rel=\"license\">CC BY 4.0</a>; reuse freely with credit to CoupeFab. Prices remain those of the cited suppliers.")}</li>
    <li>{L("Historique daté dans le dépôt public du site (journal mensuel des changements). Vous êtes fournisseur? <a href=\"/fournisseurs/#ajouter\">Ajoutez vos prix</a> : après vérification, ils entrent au comparateur avec la mention « Prix vérifiés ».",
           "Dated history in the site’s public repository (monthly change log). Are you a supplier? <a href=\"/en/suppliers/#ajouter\">Add your prices</a>: once reviewed, they join the price tool with a “Verified prices” badge.")}</li>
  </ol>
  <p class="px-foot"><a href="/prix/coupefab-prix-metaux.csv" download>{L("Télécharger le CSV", "Download the CSV")}</a> · <a href="/prix/donnees.json">JSON</a> · {n_cmp} {L("spécifications comparables aujourd’hui", "comparable specs today")}</p>
</section>

<aside class="px-alert" id="alerte">
  <div><h2>{L("Alerte prix", "Price alert")}</h2>
  <p>{L("La variation de la semaine (acier, alu, inox) et les meilleures offres repérées, dans l’infolettre CoupeFab.", "The week’s price moves (steel, aluminum, stainless) and the best deals spotted, in the CoupeFab newsletter.")}</p></div>
  {form_newsletter("fr" if fr else "en")}
</aside>
</div>
<script src="/js/prix.js?v={ver("js/prix.js")}" defer></script>''')
        return "\n".join(H)

    meta = {"rows": n_rows, "suppliers": n_real, "generated_at": gen}
    return page(True), page(False), meta

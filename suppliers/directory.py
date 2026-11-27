"""Build data/suppliers/directory.json: the public supplier directory.

Inputs
  * data/prices/latest.json                  suppliers read by the price tool (with or without prices)
  * a private contacts CSV (not in the repo)  default: /workspace/coupefab-supplier-contacts.csv

Only public business facts leave this script: company name, cities, province/state, website root,
inferred categories, languages and whether prices are published. No people, emails or phone numbers.

    python -m suppliers.directory [path/to/contacts.csv]
"""
import csv
import json
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "suppliers" / "directory.json"
DEFAULT_CSV = Path("/workspace/coupefab-supplier-contacts.csv")

CATS = {  # id: (fr, en, regex on name + notes)
    "steel": ("Acier", "Steel", r"steel|acier|\biron\b|\bfer\b|metal|métal|métaux|plate|tôle"),
    "alu": ("Aluminium", "Aluminum", r"alumin"),
    "inox": ("Inox", "Stainless", r"stainless|inox"),
    "alloys": ("Alliages spéciaux", "Specialty alloys", r"alloy|alliage|nickel|titan|tool steel|acier à outils|bronze|brass|laiton|copper|cuivre"),
    "tube": ("Tubes et tuyaux", "Tube and pipe", r"\btube|tubing|\bpipe|tuyau|piling"),
    "cut": ("Découpe sur mesure", "Cut to size", r"laser|plasma|waterjet|jet d.eau|cut to size|coupe sur mesure|découpe|cutting|sendcutsend|oshcut|osh cut|profiles|burning"),
    "retail": ("Quincaillerie / grande surface", "Hardware / big box", r"home depot|rona|canadian tire|canac|\bbmr\b|lowe|home hardware|princess auto|patrick morin|réno-dépôt|lordco|matériaux"),
    "surplus": ("Surplus / récupération", "Surplus / salvage", r"surplus|salvage|recyborg|ressourcerie|usagé|scrap|récup"),
    "online": ("Boutique en ligne", "Online store", r"online store|boutique en ligne|e-?commerce|onlinemetals|metals depot|speedy|mcmaster|online metals"),
    "tooling": ("Outillage et consommables", "Tooling and consumables", r"(?!x)x"),
}
PROV = {"QC": ("Québec", "Quebec"), "ON": ("Ontario", "Ontario"), "BC": ("Colombie-Britannique", "British Columbia"),
        "AB": ("Alberta", "Alberta"), "MB": ("Manitoba", "Manitoba"), "SK": ("Saskatchewan", "Saskatchewan"),
        "NB": ("Nouveau-Brunswick", "New Brunswick"), "NS": ("Nouvelle-Écosse", "Nova Scotia"),
        "PE": ("Île-du-Prince-Édouard", "Prince Edward Island"), "NL": ("Terre-Neuve-et-Labrador", "Newfoundland and Labrador"),
        "YT": ("Yukon", "Yukon"), "NT": ("Territoires du Nord-Ouest", "Northwest Territories"), "NU": ("Nunavut", "Nunavut"),
        "US": ("États-Unis", "United States"), "CA": ("Partout au Canada", "Canada-wide")}


ALIAS = {"acierleroux": "russelmetals", "acierpicard": "picard", "aqmaciermajeau": "picard", "ronalowesbmr": "rona",
         "millenniumalloys": "millenniumspecialtyalloys"}
SKIP = {"amazonca"}  # a marketplace, not a metal supplier
PROV_FIX = {"potvinbouchard": ["QC"]}


def key(name):
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"\(.*?\)", " ", s)
    s = re.sub(r"[’'`]", "", s)
    s = re.sub(r"\b(inc|ltd|limited|ltee|corp|co|the|les|groupe)\b\.?", " ", s)
    return re.sub(r"[^a-z0-9]+", "", s)


def site_root(*urls):
    for u in urls:
        if u and u.startswith("http"):
            p = urlparse(u)
            host = p.netloc.lower()
            if host and not any(b in host for b in ("facebook.", "google.", "yelp.", "411.", "canpages", "aciertransbec", "yellowpages", "pagesjaunes")):
                return f"{p.scheme}://{host}"
    return ""


def prov_code(s):
    s = (s or "").upper()
    if "USA" in s or s.startswith("US"):
        return "US"
    if "NATIONAL" in s:
        return "CA"
    return s[:2] if s[:2] in PROV else ""


def langs(s):
    s = (s or "").lower()
    out = []
    if "french" in s or "fr" in s.split():
        out.append("fr")
    if "english" in s:
        out.append("en")
    return out


TOOLING = ROOT / "data" / "tooling" / "prices.json"


def add_tooling(out):
    """Merge the tooling-page suppliers (data/tooling/prices.json) into the directory list. Idempotent."""
    if not TOOLING.exists():
        return out
    d = json.loads(TOOLING.read_text(encoding="utf-8"))
    rows = {}
    for it in d.get("items", []):
        rows[it["source"]] = rows.get(it["source"], 0) + 1
    host = lambda u: urlparse(u if "//" in (u or "") else "https://" + (u or "")).netloc.lower().removeprefix("www.")
    by_host = {host(s["site"]): s for s in out if s.get("site")}
    by_key = {s["id"]: s for s in out}
    entries = [(s, rows.get(s["id"], 0)) for s in d.get("suppliers", [])]
    entries += [({"id": "", "name": b["name"], "host": b["host"], "city": "", "province": b.get("province") or "",
                  "country": "US" if not b.get("province") else "CA"}, 0)
                for b in d.get("blocked", []) if b.get("host") and "," not in b["name"]]
    for s, n in entries:
        k = key(s["name"])
        cur = by_host.get(host(s["host"])) or by_key.get(k)
        if not cur:
            prov = s["province"] or ("US" if s["country"] == "US" else "CA")
            cur = {"id": k, "name": s["name"], "cities": [s["city"]] if s.get("city") and s["country"] == "CA" else [],
                   "n_branches": 1 if s.get("city") and s["country"] == "CA" else 0, "provs": [prov],
                   "site": f"https://{s['host']}", "cats": [], "langs": ["fr"] if s["province"] == "QC" else ["en"],
                   "public_prices": False, "tracked": False, "rows": 0, "verified": False}
            out.append(cur); by_key[k] = cur; by_host[host(cur["site"])] = cur
        if "tooling" not in cur["cats"]:
            cur["cats"] = [c for c in cur["cats"] if c != "online"] + ["tooling"] + (["online"] if "online" in cur["cats"] or s.get("platform") else [])
        cur["tooling_rows"] = n
        if n:
            cur["public_prices"] = True
    return out


def build(csv_path=DEFAULT_CSV):
    latest = json.loads((ROOT / "data" / "prices" / "latest.json").read_text())
    tracked = {}
    for sid, s in latest["suppliers"].items():
        rows = latest["status"].get(sid, {}).get("rows") or 0
        tracked[key(s["name"])] = {"name": s["name"].replace("’", "'"), "site": s["site"], "city": s["city"], "prices": rows > 0,
                                   "rows": rows, "sid": sid, "ships_qc": s.get("ships_qc")}
    for s in latest["suppliers_static"]:
        tracked.setdefault(key(s["name"]), {"name": s["name"], "site": site_root(s.get("url")), "city": s.get("city", ""),
                                            "prices": False, "rows": 0, "status": s["status"]})
    groups = {}
    if Path(csv_path).exists():
        for r in csv.DictReader(open(csv_path, encoding="utf-8")):
            name = (r.get("company") or "").strip()
            if not name:
                continue
            g = groups.setdefault(key(name), {"name": name, "cities": [], "provs": [], "site": "", "text": "", "langs": set(), "public": False})
            city = (r.get("branch_or_city") or "").strip()
            if re.search(r"online|en ligne", city, re.I):
                g["text"] += " online store"
                city = ""
            city = re.sub(r"\s*\((unlisted city|inferred|various|multiple)[^)]*\)", "", city).strip()
            city = re.sub(r"\s*\((centre principal|corporate[^)]*|stores?[^)]*)\)", "", city).strip()
            if re.search(r"unlisted|various|multiple|national|^n/?a$|^canada$|^quebec$", city, re.I):
                city = ""
            if city and city not in g["cities"] and len(city) < 40:
                g["cities"].append(city)
            pc = prov_code(r.get("province_state"))
            if pc and pc not in g["provs"]:
                g["provs"].append(pc)
            g["site"] = g["site"] or site_root(r.get("contact_page_url"), r.get("source_url"), r.get("quote_or_rfq_url"))
            g["text"] += " " + " ".join(r.get(k) or "" for k in ("company", "division_or_brand", "notes", "price_list_or_online_account"))
            g["langs"] |= set(langs(r.get("languages")))
            if "has_public_prices=Y" in (r.get("price_list_or_online_account") or ""):
                g["public"] = True
    # merge tracked suppliers (same key, alias, same website host, or prefix match)
    host = lambda u: urlparse(u or "").netloc.lower().removeprefix("www.")
    by_host = {host(g["site"]): g for g in groups.values() if g["site"]}
    for k, t in tracked.items():
        if k in SKIP:
            continue
        g = (groups.get(ALIAS.get(k, k)) or by_host.get(host(t["site"]))
             or next((v for kk, v in groups.items() if kk.startswith(k) or k.startswith(kk) and len(kk) > 5), None))
        if not g:
            g = groups.setdefault(k, {"name": t["name"], "cities": [], "provs": [], "site": "", "text": "", "langs": set(), "public": False})
            m = re.search(r"\((QC|ON|AB|BC|NS|NB|MB|SK|N\.-É\.)", t.get("city") or "")
            if m:
                g["provs"].append({"N.-É.": "NS"}.get(m.group(1), m.group(1)))
            elif "É.-U." in (t.get("city") or ""):
                g["provs"].append("US")
            city = re.sub(r"\s*\(.*", "", t.get("city") or "").strip()
            if city:
                g["cities"].append(city)
        g["site"] = g["site"] or t["site"]
        g["tracked"] = True
        g["rows"] = t["rows"]
        g["public"] = g["public"] or t["prices"]
        g["text"] += " " + t["name"]
    out = []
    for k, g in groups.items():
        text = (g["name"] + " " + g["text"]).lower()
        cats = [c for c, (_, _, rx) in CATS.items() if re.search(rx, text)]
        if any(c in cats for c in ("alu", "inox", "alloys", "tube")) and not re.search(r"steel|acier|\bfer\b|iron", g["name"].lower()):
            cats = [c for c in cats if c != "steel"] or cats
        if not cats:
            cats = ["steel"]
        out.append({
            "id": k, "name": g["name"], "cities": g["cities"][:6], "n_branches": len(g["cities"]),
            "provs": g["provs"] or PROV_FIX.get(k, []), "site": g["site"], "cats": cats,
            "langs": sorted(g["langs"]), "public_prices": bool(g["public"]),
            "tracked": bool(g.get("tracked")), "rows": g.get("rows", 0), "verified": False,
        })
    out = add_tooling(out)
    out.sort(key=lambda x: (0 if "QC" in x["provs"] else 1, key(x["name"])))
    return {"generated": latest["generated_at"][:10], "cats": {c: [v[0], v[1]] for c, v in CATS.items()},
            "provs": {p: list(v) for p, v in PROV.items()}, "suppliers": out}


if __name__ == "__main__":
    d = build(Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_CSV)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(d, ensure_ascii=False, indent=0, separators=(",", ":")) + "\n", encoding="utf-8")
    n = len(d["suppliers"])
    print(f"wrote {OUT.relative_to(ROOT)}: {n} suppliers, {sum(s['public_prices'] for s in d['suppliers'])} with public prices, "
          f"{sum('QC' in s['provs'] for s in d['suppliers'])} in Quebec")

#!/usr/bin/env python3
"""Build data/machines.json (machine cards for the site search) from a MachineToolIndex crawl.

Re-runnable: python3 scripts/build_machines.py [--pages DIR] [--cats FILE]
  --pages  folder of saved MTI model pages (<slug>.html), default /workspace/cf-coolant/mti/pages
  --cats   slug -> category map written by the crawler, default /workspace/cf-coolant/mti/cats.json

What is kept: FACTS ONLY (brand, model, type, travels, spindle, power, tools, table, weight,
coolant, control, turning capacities) read from each page's schema.org Product data, converted
into CoupeFab's own schema and units. No descriptions, prose, images, prices or page structure
are copied. Every record keeps the MTI page URL and the maker's page URL for attribution.

The coolant DB (data/coolant-machines.json) is merged in: machines it lists that MTI does not
are added (coolant facts only, with their own cited source), and every card that matches a
coolant row carries its exact calculator label so "Calculer le liquide de coupe" is prefilled.
build.py turns data/machines.json into the lazy-loaded public index (sitekit/machines.py).
"""
from __future__ import annotations

import argparse
import html as htmlmod
import json
import os
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "machines.json"
COOLANT = ROOT / "data" / "coolant-machines.json"
MTI = "https://machinetoolindex.com/machines/"
GAL = 3.785411784

BRAND_MAP = {"haas automation": "Haas", "doosan": "DN Solutions (Doosan)", "doosan machine tools": "DN Solutions (Doosan)",
             "dn solutions": "DN Solutions (Doosan)", "yamazaki mazak": "Mazak", "dmg": "DMG MORI", "dmg mori": "DMG MORI"}
CATSLUG = {"vertical-machining-centers": "vmc", "horizontal-machining-centers": "hmc", "5-axis-machining-centers": "5ax",
           "cnc-lathes": "lathe", "mill-turn-machines": "millturn", "swiss-type-lathes": "swiss",
           "cnc-grinding-machines": "grinder", "cnc-boring-machines": "boring", "cnc-routers": "router",
           "cnc-laser-cutting": "laser", "cnc-plasma-cutting": "plasma", "cnc-waterjet": "waterjet",
           "cnc-press-brakes": "brake", "cnc-punch-presses": "punch", "wire-edm": "wedm", "sinker-edm": "sedm",
           "multi-spindle-automatics": "multispindle", "cnc-gear-cutting": "gear", "metal-additive-manufacturing": "am"}
CATWORD = [("swiss", "swiss"), ("mill-turn", "millturn"), ("multi-tasking", "millturn"), ("5-axis", "5ax"),
           ("horizontal machining", "hmc"), ("vertical machining", "vmc"), ("vertical turning", "vtl"), ("lathe", "lathe"),
           ("turning", "lathe"), ("grind", "grinder"), ("boring", "boring"), ("router", "router"), ("laser", "laser"),
           ("plasma", "plasma"), ("waterjet", "waterjet"), ("press brake", "brake"), ("punch", "punch"), ("wire edm", "wedm"),
           ("sinker", "sedm"), ("edm", "wedm")]
SKIP_HOSTS = ("machinetoolindex.com", "youtube", "google", "facebook", "linkedin", "twitter", "x.com", "instagram",
              "reddit", "cnczone", "practicalmachinist", "ahrefs", "cloudflare", "schema.org", "wikipedia")

sq = lambda t: re.sub(r"[^a-z0-9]", "", (t or "").lower())


def num(s):
    try:
        return float(s.replace(",", "").replace("\u202f", "").replace(" ", ""))
    except ValueError:
        return None


NUM = r"(\d[\d,]*(?:\.\d+)?)"


def to_mm(v):
    if v is None:
        return None
    v = str(v)
    m = re.search(NUM + r"\s*mm\b", v)
    if m:
        return num(m.group(1))
    m = re.search(NUM + r"\s*m\b(?!/)", v)
    if m and num(m.group(1)) is not None and num(m.group(1)) < 60:
        return num(m.group(1)) * 1000
    m = re.search(NUM + r"\s*(?:in\b|inch|\")", v)
    if m:
        return round(num(m.group(1)) * 25.4)
    return None


def pair_mm(v):
    v = str(v or "")
    m = re.search(NUM + r"\s*(?:mm\s*)?[x×]\s*" + NUM + r"\s*mm", v)
    if m:
        return [num(m.group(1)), num(m.group(2))]
    m = re.search(NUM + r"\s*(?:in\s*)?[x×]\s*" + NUM + r"\s*in\b", v)
    if m:
        return [round(num(m.group(1)) * 25.4), round(num(m.group(2)) * 25.4)]
    return None


def to_rpm(v):
    v = str(v or "")
    if not re.search(r"(?i)rpm|min-1|min⁻¹", v) and not re.fullmatch(r"\s*" + NUM + r"\s*", v):
        return None
    vals = [num(x) for x in re.findall(NUM, v.split("(")[0])]
    vals = [x for x in vals if x]
    return int(max(vals)) if vals else None


def to_kw(v):
    v = str(v or "")
    m = re.search(NUM + r"\s*kW", v, re.I)
    if m:
        return num(m.group(1))
    m = re.search(NUM + r"\s*hp", v, re.I)
    if m:
        return round(num(m.group(1)) * 0.7457, 1)
    return None


def to_kg(v):
    v = str(v or "")
    m = re.search(NUM + r"\s*kg", v, re.I)
    if m:
        return num(m.group(1))
    m = re.search(NUM + r"\s*t(?:on|onnes?)?\b", v)
    if m and num(m.group(1)) < 500:
        return num(m.group(1)) * 1000
    m = re.search(NUM + r"\s*lbs?\b", v, re.I)
    if m:
        return round(num(m.group(1)) * 0.45359237)
    return None


def to_l(v):
    v = str(v or "").replace(",", "")
    m = re.search(r"([\d.]+)\s*(?:L|l|liters?|litres?)\b", v)
    if m:
        return num(m.group(1))
    m = re.search(r"([\d.]+)\s*(?:US\s*)?gal", v)
    if m:
        return round(num(m.group(1)) * GAL)
    return None


def first_int(v):
    m = re.search(r"\d+", str(v or ""))
    return int(m.group()) if m else None


def short(v, n=48):
    v = re.sub(r"\s+", " ", htmlmod.unescape(str(v or ""))).strip()
    return v if 0 < len(v) <= n else (v[:n].rsplit(" ", 1)[0] + "…" if v else None)


def pick(pr, *keys):
    for k in keys:
        if pr.get(k) not in (None, ""):
            return pr[k]
    return None


def product(h):
    prod, props = None, {}
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try:
            d = json.loads(m.group(1))
        except Exception:
            continue
        for o in (d if isinstance(d, list) else [d]):
            if isinstance(o, dict) and o.get("@type") == "Product":
                prod = o
                for p in o.get("additionalProperty") or []:
                    props[p.get("name", "")] = p.get("value", "")
    return prod, props


def maker_url(prod, h, brand):
    cands = []
    off = prod.get("offers")
    if isinstance(off, dict) and off.get("url"):
        cands.append(off["url"])
    cands += re.findall(r'href="(https?://[^"]+)"', h)
    tok = sq(brand.split()[0])[:5]
    ok = [u for u in dict.fromkeys(cands) if not any(s in urlparse(u).netloc for s in SKIP_HOSTS)]
    for u in ok:
        if tok and tok in sq(urlparse(u).netloc):
            return u
    return None


def sane(v, lo, hi):
    return v if v is not None and lo <= v <= hi else None


def parse_page(path, cats):
    slug = path.stem
    h = path.read_text(errors="ignore")
    prod, pr = product(h)
    if not prod or not prod.get("name"):
        return None
    b = prod.get("brand")
    braw = (b.get("name") if isinstance(b, dict) else b) or prod["name"].split()[0]
    braw = htmlmod.unescape(braw).strip()
    brand = BRAND_MAP.get(braw.lower(), braw)
    name = htmlmod.unescape(prod["name"]).strip()
    model = name
    for pre in sorted({braw, brand, braw.split()[0], brand.split()[0], re.sub(r"\s*\(.*\)", "", brand)}, key=len, reverse=True):
        if model.lower().startswith(pre.lower() + " "):
            model = model[len(pre):].strip()
            break
    cat = (prod.get("category") or "").lower()
    typ = CATSLUG.get(cats.get(slug, "")) or next((t for k, t in CATWORD if k in cat), "other")
    s = {}
    x, y, z = (sane(to_mm(pick(pr, f"{a}-Axis Travel", f"{a} Axis Travel")), 1, 60000) for a in "XYZ")
    if x or y or z:
        s["xyz"] = [x, y, z]
    s["rpm"] = sane(to_rpm(pick(pr, "Max Spindle Speed", "Main Spindle Speed", "Spindle Speed", "Max Spindle Speed Main")), 10, 200000)
    s["taper"] = short(pick(pr, "Spindle Taper", "Spindle Nose"), 32)
    s["kw"] = sane(to_kw(pick(pr, "Spindle Motor Power", "Main Spindle Power", "Spindle Power", "Spindle Power Intermittent")), 0.1, 2000)
    s["tools"] = sane(first_int(pick(pr, "Tool Capacity", "Atc Capacity", "ATC Capacity")), 1, 2000)
    s["turret"] = sane(first_int(pick(pr, "Turret Stations")), 1, 200)
    s["table"] = pair_mm(pick(pr, "Table Size", "Pallet Size"))
    s["kg"] = sane(to_kg(pick(pr, "Machine Weight")), 20, 1000000)
    s["coolant_l"] = sane(to_l(pick(pr, "Coolant Capacity", "Coolant Tank Capacity")), 3, 100000)
    s["control"] = short(pick(pr, "CNC Control", "Control", "CNC Controller"), 48)
    s["swing"] = sane(to_mm(pick(pr, "Max Swing", "Swing Over Bed")), 10, 20000)
    s["turn_d"] = sane(to_mm(pick(pr, "Max Turning Diameter", "Max Machining Diameter")), 5, 20000)
    s["turn_l"] = sane(to_mm(pick(pr, "Max Turning Length", "Max Machining Length")), 5, 40000)
    s["bar"] = sane(to_mm(pick(pr, "Bar Capacity", "Max Bar Capacity")), 1, 1000)
    s["chuck"] = sane(to_mm(pick(pr, "Chuck Size")), 20, 3000)
    s = {k: v for k, v in s.items() if v not in (None, [], [None, None, None])}
    return {"id": slug, "brand": brand, "model": model, "type": typ, "specs": s,
            "mti": MTI + slug, "maker": maker_url(prod, h, brand)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", default="/workspace/cf-coolant/mti/pages")
    ap.add_argument("--cats", default="/workspace/cf-coolant/mti/cats.json")
    a = ap.parse_args()
    cats = json.load(open(a.cats)) if os.path.exists(a.cats) else {}
    out, seen = [], set()
    for p in sorted(Path(a.pages).glob("*.html")):
        if p.stat().st_size < 1000:
            continue
        r = parse_page(p, cats)
        if r and r["model"] and (sq(r["brand"]) + "|" + sq(r["model"])) not in seen:
            seen.add(sq(r["brand"]) + "|" + sq(r["model"]))
            out.append(r)
    mti_n = len(out)

    # coolant DB merge: label for the calculator, and coolant-only machines as cards
    cool = json.load(open(COOLANT))["machines"]
    bykey = {sq(r["brand"]) + "|" + sq(r["model"]): r for r in out}
    byslug = {r["id"]: r for r in out}
    bbrand = {sq(r["brand"]): r["brand"] for r in out}
    linked = added = 0
    for c in cool:
        label = c["brand"] + " " + c["model"]
        src = c.get("source") or ""
        hit = byslug.get(src[len(MTI):]) if src.startswith(MTI) else None
        hit = hit or bykey.get(sq(c["brand"]) + "|" + sq(re.sub(r"\(.*?\)", "", c["model"])))
        if not hit:  # "LB45 (LB45-II / LB45III)" -> try each listed variant against MTI models without a link
            for v in re.split(r"[()/]", c["model"]):
                h2 = bykey.get(sq(c["brand"]) + "|" + sq(v))
                if sq(v) and h2 and not h2.get("coolant"):
                    hit = h2
                    break
        if hit and c.get("shop"):
            hit["alias"] = c["shop"]
        if hit:
            hit["coolant"] = label
            if c.get("liters"):
                hit["specs"]["coolant_l"] = c["liters"]
                if not src.startswith(MTI):
                    hit["coolant_src"] = src
            linked += 1
            continue
        mid = "cf-" + re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")
        if mid in byslug:
            continue
        rec = {"id": mid, "brand": bbrand.get(sq(c["brand"]), c["brand"]), "model": c["model"], "type": c["type"],
               "specs": {"coolant_l": c["liters"]} if c.get("liters") else {}, "mti": None,
               "maker": c.get("official"), "coolant": label, "coolant_src": src or None, "alias": c.get("shop")}
        out.append({k: v for k, v in rec.items() if v is not None})
        byslug[mid] = rec
        added += 1

    out.sort(key=lambda r: (r["brand"].lower(), [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", r["model"].lower())]))
    data = {"version": __import__("datetime").date.today().isoformat(),
            "schema": "CoupeFab machine facts v1. Units: mm, kg, kW, rpm, liters. xyz=[X,Y,Z] travels, table=[L,W], "
                      "turn_d/turn_l=max turning diameter/length, bar=bar capacity, chuck=chuck size.",
            "sources": "Facts compiled from MachineToolIndex (machinetoolindex.com, specs compiled from manufacturer sources) "
                       "and the sources cited in coolant-machines.json; each record links its MTI page and the maker's page.",
            "count": len(out), "count_mti": mti_n, "machines": out}
    OUT.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"machines.json: {len(out)} machines ({mti_n} from MTI, {added} coolant-only, {linked} linked to the coolant calculator)")


if __name__ == "__main__":
    main()

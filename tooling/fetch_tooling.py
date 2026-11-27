#!/usr/bin/env python3
"""Fetch public tooling prices (plasma consumables, end mills, drills, taps, inserts, router bits, saw blades,
abrasives, laser consumables, press-brake tooling, collets/holders, measuring tools).

    python -m tooling.fetch_tooling            # all sources -> data/tooling/prices.json
    python -m tooling.fetch_tooling --only airtek glcs
    python -m tooling.fetch_tooling --cache /tmp/raw   # keep/reuse raw feed pages (development)

Polite: one request at a time per host, ~1 s apart, identified User-Agent, robots.txt checked per run.
A source that fails keeps its rows from the previous snapshot (marked stale) so the page never empties.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import json
import re
import sys
import time
import urllib.robotparser as robotparser
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

from tooling import classify as C
from tooling.sources import SOURCES, BLOCKED

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "tooling" / "prices.json"
TZ = ZoneInfo("America/Toronto")
UA = "CoupeFabPriceBot/1.0 (+https://coupefab.vercel.app/a-propos/; prix publics, une requete a la fois)"
S = requests.Session()
S.headers.update({"User-Agent": UA, "Accept": "application/json"})
DELAY = 1.0


def today():
    return dt.datetime.now(TZ).date().isoformat()


def fx_rate():
    """Same USD/CAD figure the sheet-price page uses (data/prices/latest.json, Bank of Canada Valet)."""
    p = ROOT / "data" / "prices" / "latest.json"
    try:
        fx = json.loads(p.read_text())["fx"]
        return {"rate": float(fx["rate"]), "date": fx.get("date"), "source": fx.get("source"), "url": fx.get("url")}
    except Exception:
        r = S.get("https://www.bankofcanada.ca/valet/observations/FXUSDCAD/json?recent=1", timeout=30)
        o = r.json()["observations"][-1]
        return {"rate": float(o["FXUSDCAD"]["v"]), "date": o["d"], "source": "Banque du Canada (Valet FXUSDCAD)",
                "url": "https://www.bankofcanada.ca/rates/exchange/daily-exchange-rates/"}


class Fetcher:
    def __init__(self, cache: Path | None):
        self.cache = cache
        self.robots = {}
        self.last = {}

    def allowed(self, host, path):
        if host not in self.robots:
            rp = robotparser.RobotFileParser()
            try:
                r = S.get(f"https://{host}/robots.txt", timeout=20)
                rp.parse(r.text.splitlines() if r.status_code == 200 else [])
            except requests.RequestException:
                rp.parse([])
            self.robots[host] = rp
        return self.robots[host].can_fetch(UA, f"https://{host}{path}")

    def get_json(self, host, path):
        key = hashlib.sha1(f"{host}{path}".encode()).hexdigest()[:16]
        if self.cache:
            f = self.cache / f"{host}-{key}.json"
            if f.exists():
                return json.loads(f.read_text())
        if not self.allowed(host, path.split("?")[0]):
            raise PermissionError(f"robots.txt disallows {host}{path}")
        wait = DELAY - (time.time() - self.last.get(host, 0))
        if wait > 0:
            time.sleep(wait)
        for attempt in range(3):
            r = S.get(f"https://{host}{path}", timeout=45)
            self.last[host] = time.time()
            if r.status_code == 429 or r.status_code >= 500:
                time.sleep(5 * (attempt + 1)); continue
            break
        if r.status_code != 200:
            raise RuntimeError(f"HTTP {r.status_code} {host}{path}")
        data = r.json()
        if self.cache:
            (self.cache / f"{host}-{key}.json").write_text(json.dumps(data))
        return data


def clean(s):
    s = html.unescape(re.sub(r"<[^>]+>", " ", str(s or "")))
    return re.sub(r"\s+", " ", s).strip()


def shopify_items(F, src):
    host = src["host"]
    for page in range(1, src.get("max_pages", 10) + 1):
        data = F.get_json(host, f"/products.json?limit=250&page={page}")
        prods = data.get("products") or []
        if not prods:
            break
        for p in prods:
            opts = [o.get("name", "") for o in p.get("options") or []]
            for v in p.get("variants") or []:
                vt = v.get("title") or ""
                if vt.lower() == "default title":
                    vt = ""
                try:
                    price = float(v.get("price") or 0)
                except ValueError:
                    continue
                yield {
                    "title": clean(p.get("title")), "variant": clean(vt), "vendor": clean(p.get("vendor")),
                    "ptype": clean(p.get("product_type")), "tags": [clean(t) for t in (p.get("tags") or [])][:30],
                    "sku": clean(v.get("sku")), "price": price, "available": bool(v.get("available", True)),
                    "url": f"https://{host}{src.get('lang_path','')}/products/{p.get('handle')}" + (f"?variant={v['id']}" if vt else ""),
                    "opts": opts,
                }
        if len(prods) < 250:
            break


def woo_price(prices):
    unit = int(prices.get("currency_minor_unit", 2))
    raw = prices.get("price") or "0"
    try:
        return int(raw) / (10 ** unit)
    except ValueError:
        return 0.0


def woo_items(F, src):
    host = src["host"]
    plans = src.get("categories") or {None: src.get("max_pages", 5)}
    seen = set()
    for cat, pages in plans.items():
        for page in range(1, pages + 1):
            q = f"/wp-json/wc/store/v1/products?per_page=100&page={page}" + (f"&category={cat}" if cat else "")
            try:
                prods = F.get_json(host, q)
            except RuntimeError as e:  # page past the end answers 400
                if "HTTP 400" in str(e):
                    break
                raise
            if not prods:
                break
            for p in prods:
                if p["id"] in seen:
                    continue
                seen.add(p["id"])
                cats = [clean(c.get("name")) for c in p.get("categories") or []]
                base = {"title": clean(p.get("name")), "vendor": clean((p.get("brands") or [{}])[0].get("name", "")) if p.get("brands") else "",
                        "ptype": " / ".join(cats), "tags": [clean(t.get("name")) for t in p.get("tags") or []][:30],
                        "available": bool(p.get("is_in_stock", True)), "opts": []}
                vars_ = p.get("variations") or []
                if src.get("variations") and vars_:
                    for v in vars_[:60]:
                        try:
                            vp = F.get_json(host, f"/wp-json/wc/store/v1/products/{v['id']}")
                        except Exception:
                            continue
                        vt = ", ".join(a.get("value", "") for a in v.get("attributes") or [])
                        price = woo_price(vp.get("prices") or {})
                        yield dict(base, variant=clean(vt), sku=clean(vp.get("sku")), price=price,
                                   url=vp.get("permalink") or p.get("permalink"))
                else:
                    yield dict(base, variant="", sku=clean(p.get("sku")), price=woo_price(p.get("prices") or {}),
                               url=p.get("permalink"))
            if len(prods) < 100:
                break


# Plasma and laser consumables already recorded for /pieces/ (same public sources, same date stamp).
PARTS_SOURCES = {"gm-welding": ("GM Welding Supplies", "gmweldingsupplies.ca", "Mississauga", "ON"),
                 "torchandtip": ("Torch and Tip", "torchandtip.com", "Bragg Creek", "AB"),
                 "canada-welding-supply": ("Canada Welding Supply", "canadaweldingsupply.ca", "Mississauga", "ON"),
                 "mapleweld": ("MapleWeld", "mapleweld.ca", "Toronto", "ON")}


PARTS_CATS = {"plasma-electrode", "plasma-nozzle", "plasma-swirl", "plasma-shield", "plasma-cap", "plasma-cartridge",
              "laser-nozzle", "laser-window", "laser-ceramic"}


def from_parts_snapshot():
    p = ROOT / "data" / "parts" / "prices.json"
    if not p.exists():
        return [], []
    parts = json.loads(p.read_text(encoding="utf-8")).get("items") or []
    sups, rows = [], []
    used = set()
    for it in parts:
        if it.get("source") not in PARTS_SOURCES or it.get("category") not in PARTS_CATS:
            continue
        if not it.get("price") or (it.get("currency") or "CAD") != "CAD":
            continue
        pq = it.get("pack_qty") or None
        price = round(float(it["price"]), 2)
        used.add(it["source"])
        spec = " · ".join(x for x in [("N° " + it["oem_part"]) if it.get("oem_part") else "",
                                      {"oem": "pièce d’origine / genuine", "compatible": "compatible"}.get(it.get("origin"), "")] if x)
        rows.append({"cat": it["category"].split("-")[0], "name": C.clean_name(it.get("name") or "")[:160], "spec": spec,
                     "sku": (it.get("sku") or "")[:40], "brand": it.get("brand") if it.get("brand") not in (None, "", "—") else "",
                     "pack": pq, "price_cad": price, "unit_cad": round(price / pq, 2) if pq else price,
                     "price_orig": price, "currency": "CAD", "source": it["source"], "url": it.get("source_url"),
                     "fetched": it.get("fetched"), "in_stock": True})
    for sid in sorted(used):
        n, host, city, prov = PARTS_SOURCES[sid]
        sups.append({"id": sid, "name": n, "host": host, "city": city, "province": prov, "country": "CA",
                     "currency": "CAD", "platform": "pieces"})
    return sups, C.dedupe(rows)


def write(out):
    """Metadata on top, one row per line: diff-friendly and far below the 8 MB connector limit."""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    meta = {k: v for k, v in out.items() if k != "items"}
    head = json.dumps(meta, ensure_ascii=False, separators=(",", ":"))[:-1]
    lines = ",\n".join(json.dumps(i, ensure_ascii=False, separators=(",", ":")) for i in out["items"])
    OUT.write_text(head + ',"items":[\n' + lines + "\n]}\n", encoding="utf-8")


def run(only=None, cache=None):
    F = Fetcher(Path(cache) if cache else None)
    if F.cache:
        F.cache.mkdir(parents=True, exist_ok=True)
    fx = fx_rate()
    date = today()
    prev = {}
    if OUT.exists():
        try:
            old = json.loads(OUT.read_text())
            for it in old.get("items", []):
                prev.setdefault(it["source"], []).append(it)
        except Exception:
            pass
    items, status = [], []
    for src in SOURCES:
        if only and src["id"] not in only:
            items += prev.get(src["id"], [])
            continue
        gen = shopify_items if src["platform"] == "shopify" else woo_items
        rows, err = [], None
        try:
            for raw in gen(F, src):
                row = C.to_row(raw, src, fx, date)
                if row:
                    rows.append(row)
        except Exception as e:  # keep yesterday's rows for this source
            err = f"{type(e).__name__}: {e}"[:200]
        if err and not rows:
            kept = prev.get(src["id"], [])
            for k in kept:
                k["stale"] = True
            rows = kept
        rows = C.dedupe(rows)
        rows = C.cap(rows)
        items += rows
        status.append({"id": src["id"], "ok": err is None, "error": err, "rows": len(rows)})
        print(f"{src['id']:22s} {len(rows):6d} rows {'' if not err else 'ERROR ' + err}", file=sys.stderr)
    suppliers = [{k: s[k] for k in ("id", "name", "host", "city", "province", "country", "currency", "platform")}
                 for s in SOURCES]
    extra_sup, extra_rows = from_parts_snapshot()
    suppliers += extra_sup
    items += extra_rows
    status.append({"id": "pieces-snapshot", "ok": True, "error": None, "rows": len(extra_rows)})
    out = {"fetched": date, "timezone": "America/Toronto", "currency": "CAD", "fx": fx,
           "count": len(items), "status": status, "suppliers": suppliers, "blocked": BLOCKED, "items": items}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    write(out)
    print(f"total {len(items)} rows -> {OUT.relative_to(ROOT)}", file=sys.stderr)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--cache")
    a = ap.parse_args()
    run(a.only, a.cache)

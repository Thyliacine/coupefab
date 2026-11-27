"""Curated supplier-directory layer maintained by the daily discovery & cleanup routine.

Files (all in data/suppliers/, committed):
  additions.json   new businesses found by the routine (public facts only, with source URL and date)
  checks.json      rotating health check: last_checked date, status (ok / flag / robots / no-site),
                   note, and optional "site" override when a business moved domain ("" = no own site)
  removals.csv     removal log (id, name, date, evidence URL, evidence) — removed ids are dropped
  search-log.csv   discovery search log so daily runs vary regions and categories

apply(suppliers, meta) is called after directory.json + tooling are merged (suppliers/stats.py).
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "data" / "suppliers"
ADDITIONS = DIR / "additions.json"
CHECKS = DIR / "checks.json"
REMOVALS = DIR / "removals.csv"

# Service categories added for shops (not only metal distributors).
EXTRA_CATS = {
    "machining": ["Usinage", "Machining"],
    "sheetmetal": ["Tôlerie et pliage", "Sheet metal and bending"],
    "welding": ["Soudure et fabrication", "Welding and fabrication"],
}


def _load(path, default):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def additions() -> list[dict]:
    return _load(ADDITIONS, [])


def removed_ids() -> set[str]:
    if not REMOVALS.exists():
        return set()
    with REMOVALS.open(encoding="utf-8", newline="") as f:
        return {r["id"] for r in csv.DictReader(f) if r.get("id")}


def phones() -> dict[str, str]:
    return {a["id"]: a["phone"] for a in additions() if a.get("phone")}


def apply(sup: list[dict], meta: dict | None = None) -> list[dict]:
    if meta is not None:
        for k, v in EXTRA_CATS.items():
            meta.setdefault("cats", {}).setdefault(k, v)
    gone = removed_ids()
    checks = _load(CHECKS, {})
    out = []
    for s in sup:
        if s.get("id") in gone:
            continue
        c = checks.get(s.get("id") or "")
        if c and "site" in c:
            s = dict(s, site=c["site"])
        out.append(s)
    have = {s.get("id") for s in out}
    for a in additions():
        if a["id"] in have or a["id"] in gone:
            continue
        out.append({"id": a["id"], "name": a["name"], "cities": a.get("cities") or [],
                    "n_branches": len(a.get("cities") or []), "provs": a["provs"], "site": a.get("site", ""),
                    "cats": a["cats"], "langs": a.get("langs") or [], "public_prices": False,
                    "tracked": False, "rows": 0, "verified": False})
    return out

"""Social-proof counts: suppliers with prices, and prices tracked (sheet + tooling)."""
from __future__ import annotations

import json
from pathlib import Path

from .directory import add_tooling
from . import curated

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "data" / "suppliers" / "directory.json"
TOOLING = ROOT / "data" / "tooling" / "prices.json"


def fmt(n: int, lang: str) -> str:
    if lang == "fr":
        return f"{n:,}".replace(",", "\u202f")
    return f"{n:,}"


def proof() -> dict:
    d = json.loads(DIR.read_text(encoding="utf-8"))
    sup = curated.apply(add_tooling(list(d["suppliers"])), d)
    tp = json.loads(TOOLING.read_text(encoding="utf-8")) if TOOLING.exists() else {}
    tooling_n = int(tp.get("count") or 0)
    with_p = {s["id"] for s in sup if s.get("public_prices") or s.get("rows") or s.get("tooling_rows")}
    for s in tp.get("suppliers") or []:
        if isinstance(s, dict):
            with_p.add(s.get("id") or s.get("host") or s.get("name"))
    sheet = sum(int(s.get("rows") or 0) for s in sup)
    return {
        "n_dir": len(sup),
        "n_qc": sum("QC" in (s.get("provs") or []) for s in sup),
        "n_with_prices": len(with_p),
        "n_prices": sheet + tooling_n,
        "n_sheet": sheet,
        "n_tooling": tooling_n,
        "suppliers": sup,
        "meta": d,
    }

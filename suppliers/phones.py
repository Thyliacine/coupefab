"""Optional public phone numbers from the private contacts CSV (build-time only, not committed)."""
from __future__ import annotations

import csv
from pathlib import Path

from .directory import DEFAULT_CSV, key


def _clean(num: str) -> str:
    s = " ".join((num or "").split())
    return s[:40]


def load(csv_path: Path | None = None) -> dict[str, str]:
    from .curated import phones as curated_phones
    path = csv_path or DEFAULT_CSV
    out: dict[str, str] = dict(curated_phones())
    if not path.exists():
        return out
    with path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            num = _clean(row.get("phone") or "") or _clean(row.get("toll_free") or "")
            if not num:
                continue
            for field in ("company", "division_or_brand"):
                k = key(row.get(field) or "")
                if k and k not in out:
                    out[k] = num
    return out

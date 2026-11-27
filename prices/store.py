"""Storage of the price snapshot, split so every file stays well under 8 MB.

    data/prices/latest.json               metadata (FX, suppliers, status, catalogue) + "rows_files"
    data/prices/latest-rows/part-NN.jsonl one normalized price row per line (≤ ~4 MB per part)

Why: the full snapshot (9,700+ rows, ~9 MB) no longer fits the GitHub connector's 8 MB
per-file limit. Text shards stay diff-friendly. read_latest() still accepts the old
single-file layout (rows inline), so older checkouts keep building.
"""
from __future__ import annotations

import json
from pathlib import Path

PART_DIR = "latest-rows"
PART_BYTES = 4_000_000


def read_latest(data_dir: Path) -> dict:
    data_dir = Path(data_dir)
    latest = json.loads((data_dir / "latest.json").read_text())
    if "rows" not in latest:
        rows = []
        for rel in latest.get("rows_files", []):
            with open(data_dir / rel, encoding="utf-8") as fh:
                rows += [json.loads(line) for line in fh if line.strip()]
        if len(rows) != latest.get("n_rows", len(rows)):
            raise ValueError(f"price snapshot incomplete: {len(rows)} rows, expected {latest.get('n_rows')}")
        latest["rows"] = rows
    return latest


def write_latest(data_dir: Path, d: dict) -> list[str]:
    """Write metadata + row shards; remove shards left over from a larger snapshot."""
    data_dir = Path(data_dir)
    part_dir = data_dir / PART_DIR
    part_dir.mkdir(parents=True, exist_ok=True)
    parts, buf, size = [], [], 0
    for r in d.get("rows", []):
        line = json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n"
        n = len(line.encode())
        if buf and size + n > PART_BYTES:
            parts.append(buf); buf, size = [], 0
        buf.append(line); size += n
    if buf or not parts:
        parts.append(buf)
    names = []
    for i, lines in enumerate(parts, 1):
        rel = f"{PART_DIR}/part-{i:02d}.jsonl"
        (data_dir / rel).write_text("".join(lines), encoding="utf-8")
        names.append(rel)
    for old in part_dir.glob("part-*.jsonl"):
        if f"{PART_DIR}/{old.name}" not in names:
            old.unlink()
    meta = {k: v for k, v in d.items() if k != "rows"}
    meta["n_rows"] = len(d.get("rows", []))
    meta["rows_files"] = names
    (data_dir / "latest.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return names

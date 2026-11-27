"""Machine cards for the site search: data/machines.json -> lazy-loaded public files.

  /js/machines/index.json      compact search index (id, brand, model, type, alias), fetched on the first search
  /js/machines/b/<brand>.json  card details for one brand, fetched when a card opens

Built by build.py; the data comes from scripts/build_machines.py.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "machines.json"
OUT = ROOT / "js" / "machines"


def _slug(t):
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-") or "x"


def write_assets():
    if not SRC.exists():
        return 0
    d = json.loads(SRC.read_text(encoding="utf-8"))
    brands, shards, rows, det = [], [], [], {}
    for m in d["machines"]:
        if m["brand"] not in brands:
            brands.append(m["brand"])
            shards.append(_slug(m["brand"]))
        bi = brands.index(m["brand"])
        row = [m["id"], bi, m["model"], m["type"]]
        if m.get("alias"):
            row.append(m["alias"])
        rows.append(row)
        det.setdefault(shards[bi], {})[m["id"]] = {k: v for k, v in {
            "s": m.get("specs") or {}, "mti": m.get("mti"), "mk": m.get("maker"),
            "c": m.get("coolant"), "cs": m.get("coolant_src")}.items() if v}
    (OUT / "b").mkdir(parents=True, exist_ok=True)
    for f in (OUT / "b").glob("*.json"):
        f.unlink()
    js = lambda o: json.dumps(o, ensure_ascii=False, separators=(",", ":"))
    (OUT / "index.json").write_text(js({"v": d.get("version"), "n": len(rows), "b": brands, "s": shards, "r": rows}), encoding="utf-8")
    for s, o in det.items():
        (OUT / "b" / f"{s}.json").write_text(js(o), encoding="utf-8")
    return len(rows)

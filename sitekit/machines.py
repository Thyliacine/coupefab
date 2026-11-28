"""Machine cards for the site search: data/machines.json -> lazy-loaded public files.

  /js/machines/index.json      compact search index (id, brand, model, type, alias), fetched on the first search
  /js/machines/b/<brand>.json  card details for one brand, fetched when a card opens

Built by build.py; the data comes from scripts/build_machines.py.

Duplicate cards (same machine under two brand spellings, or a coolant-only
stub next to a fuller MachineToolIndex record) are merged here, so the
source JSON stays untouched and a rebuild stays deterministic.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "machines.json"
OUT = ROOT / "js" / "machines"

# Corporate / legal endings stripped when comparing brands (and when picking a display name).
_LEGAL = re.compile(
    r"\s+(werkzeugmaschinen|machine\s+tools?|machinery|corporation|company|"
    r"incorporated|limited|llc|plc|inc|ltd|gmbh|co|ag|sa|kg|spa)\s*$",
    re.I,
)
# Trailing marketing words that are not part of the model identifier.
_MODEL_TAIL = re.compile(
    r"[\s\-]*(super\s*speed\s*vmc|super\s*speed|high[-\s]?capacity\s*vmc|"
    r"vertical\s*machining\s*center|horizontal\s*machining\s*center|"
    r"machining\s*center|turning\s*center|cnc\s*lathe|\bseries\b)\s*$",
    re.I,
)
# Applied only when a model exists under both names. Mori Seiki cards are
# not renamed to DMG MORI unless that exact model also appears under DMG MORI.
_BRAND_ALIASES = {"moriseiki": "dmgmori", "dmg": "dmgmori"}
# Prefer this type when two listings of the same machine use different categories.
_TYPE_RANK = {"5ax": 5, "millturn": 4, "swiss": 3, "vtl": 2, "hmc": 1, "vmc": 1, "lathe": 1}


def _slug(t):
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-") or "x"


def _squash(t):
    return re.sub(r"[^a-z0-9]", "", (t or "").lower())


def _brand_stem(brand):
    t = (brand or "").lower().replace("&", " and ")
    t = re.sub(r"[.,'/()+-]+", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    while True:
        n = _LEGAL.sub("", t).strip()
        if n == t:
            return t
        t = n


def _brand_key(brand, alias=True):
    key = _squash(_brand_stem(brand))
    if alias:
        key = _BRAND_ALIASES.get(key, key)
    return key


def _model_key(model):
    t = (model or "").strip()
    while True:
        n = _MODEL_TAIL.sub("", t).strip()
        if n == t or not n:
            break
        t = n
    return _squash(t)


def _values_agree(a, b):
    """True if two spec values are the same machine fact (gaps and wording variants allowed)."""
    if a is None or b is None or a == "" or b == "":
        return True
    if a == b:
        return True
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(float(a) - float(b)) < 1e-6
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            return False
        return all(_values_agree(x, y) for x, y in zip(a, b))
    if isinstance(a, str) and isinstance(b, str):
        sa, sb = _squash(a), _squash(b)
        return sa == sb or sa in sb or sb in sa
    return False


def _specs_conflict(a, b):
    sa, sb = a.get("specs") or {}, b.get("specs") or {}
    for k in sa:
        if k in sb and not _values_agree(sa[k], sb[k]):
            return True
    return False


def _richness(m):
    s = m.get("specs") or {}
    return len(s) + sum(1 for k in ("mti", "maker", "coolant", "coolant_src", "alias") if m.get(k))


def _preferred_id(recs):
    def score(m):
        ident = m["id"]
        return (
            0 if ident.startswith("cf-") else 1,
            0 if re.search(r"-(lathe|series|boring)$", ident) else 1,
            _richness(m),
            -len(ident),
        )
    return sorted(recs, key=score, reverse=True)[0]["id"]


def _preferred_brand(names):
    """Short official name: 'Matsuura' not 'Matsuura Machinery'; most common casing among clean names."""
    names = [n for n in names if n]
    if not names:
        return ""
    counts = {}
    for n in names:
        counts[n] = counts.get(n, 0) + 1
    clean = [n for n in counts if _squash(n) == _brand_key(n, alias=False)]
    pool = clean or list(counts)
    pool.sort(key=lambda n: (-counts[n], len(n), n))
    return pool[0]


def _preferred_model(recs):
    def score(m):
        raw = m["model"]
        stripped = _MODEL_TAIL.sub("", raw).strip() or raw
        # Prefer the official short form (already without a marketing tail).
        return (0 if stripped == raw else 1, len(stripped), len(raw), raw)
    return sorted(recs, key=score)[0]["model"]


def _preferred_type(recs):
    # Ignore coolant-only stubs when they disagree with a fuller record (e.g. ST-10Y).
    substantial = [r for r in recs if _richness(r) > 3] or list(recs)
    return max(substantial, key=lambda m: (_TYPE_RANK.get(m.get("type"), 0), _richness(m)))["type"]


def _merge_group(recs):
    """Combine recs that are the same machine. Recs is already conflict-checked."""
    recs = list(recs)
    kept_id = _preferred_id(recs)
    base = next(r for r in recs if r["id"] == kept_id)
    out = dict(base)
    specs = dict(base.get("specs") or {})
    aliases, mtis, makers, coolants, csrcs, brands, models = [], [], [], [], [], [], []
    for r in recs:
        brands.append(r["brand"])
        models.append(r["model"])
        for k, v in (r.get("specs") or {}).items():
            if k not in specs or specs[k] in (None, ""):
                specs[k] = v
            elif isinstance(specs[k], str) and isinstance(v, str) and v != specs[k] and len(v) > len(specs[k]) and _squash(specs[k]) in _squash(v):
                specs[k] = v
        if r.get("alias"):
            aliases.append(r["alias"])
        if r.get("mti"):
            mtis.append(r["mti"])
        if r.get("maker"):
            makers.append(r["maker"])
        if r.get("coolant"):
            coolants.append((0 if r["id"].startswith("cf-") else 1, len(r["coolant"]), r["coolant"]))
        if r.get("coolant_src"):
            csrcs.append(r["coolant_src"])
        if r["brand"] != out.get("brand"):
            aliases.append(r["brand"])
        if r["model"] != out.get("model") and r["model"] not in aliases:
            aliases.append(r["model"])
    out["id"] = kept_id
    out["brand"] = _preferred_brand(brands)
    out["model"] = _preferred_model(recs)
    out["type"] = _preferred_type(recs)
    out["specs"] = specs
    # Prefer the coolant-stub label (matches the calculator) when both exist.
    if coolants:
        coolants.sort()
        out["coolant"] = coolants[0][2]
    if csrcs:
        out["coolant_src"] = csrcs[0]
        if len(set(csrcs)) > 1:
            out["coolant_src"] = csrcs[0]
    if mtis:
        seen = []
        for u in mtis:
            if u not in seen:
                seen.append(u)
        out["mti"] = seen[0]
        if len(seen) > 1:
            out["mti2"] = seen[1]
    if makers:
        out["maker"] = next((u for u in makers if u), makers[0])
    # unique alias tokens, keep a single search string
    seen_a, parts = set(), []
    for a in aliases:
        k = _squash(a)
        if a and k and k not in seen_a and k != _squash(out["model"]) and k != _squash(out["brand"]):
            seen_a.add(k)
            parts.append(a)
    if parts:
        out["alias"] = ", ".join(parts)
    elif "alias" in out and not out["alias"]:
        del out["alias"]
    dropped = [r["id"] for r in recs if r["id"] != kept_id]
    return out, dropped


def dedupe_machines(machines):
    """Merge cards that share a normalized brand + model. Skip a pair when numeric specs disagree.

    Brand aliases (Machinery, Machine Tools, Inc, Ltd, GmbH, …) and light model
    tails (Super Speed VMC, Turning Center, Series, …) are normalized first.
    Mori Seiki / DMG MORI only collapse when the same model is present under both.
    Returns (deduped list, merge log).
    """
    groups = {}
    order = []
    for m in machines:
        key = (_brand_key(m["brand"]), _model_key(m["model"]))
        if key not in groups:
            order.append(key)
            groups[key] = []
        groups[key].append(m)

    # Canonical display brand per stem, except Mori Seiki stays Mori Seiki
    # unless a model also exists under DMG MORI (handled by the alias key).
    names_by_stem = {}
    for m in machines:
        stem = _brand_key(m["brand"], alias=False)
        names_by_stem.setdefault(stem, []).append(m["brand"])
    canon = {stem: _preferred_brand(names) for stem, names in names_by_stem.items()}

    out, merges = [], []
    for key in order:
        recs = groups[key]
        if len(recs) == 1:
            m = dict(recs[0])
            stem = _brand_key(m["brand"], alias=False)
            # Do not mass-rename Mori Seiki -> DMG MORI
            if stem not in _BRAND_ALIASES and m["brand"] != canon[stem]:
                old = m["brand"]
                m["brand"] = canon[stem]
                extra = (m.get("alias") + ", " if m.get("alias") else "") + old
                m["alias"] = extra
            out.append(m)
            continue
        # Split the group if any pair has conflicting numeric specs
        accepted, skipped = [recs[0]], []
        for r in recs[1:]:
            if any(_specs_conflict(r, a) for a in accepted):
                skipped.append(r)
            else:
                accepted.append(r)
        if len(accepted) > 1:
            merged, dropped = _merge_group(accepted)
            out.append(merged)
            merges.append({
                "kept": merged["id"],
                "brand": merged["brand"],
                "model": merged["model"],
                "from": dropped,
                "labels": [f"{r['brand']} {r['model']}" for r in accepted],
            })
        else:
            out.append(dict(accepted[0]))
        for r in skipped:
            out.append(dict(r))
    return out, merges


def write_assets():
    parts = sorted((ROOT / "data" / "machines").glob("part-*.json"))
    if SRC.exists():
        d = json.loads(SRC.read_text(encoding="utf-8"))
    elif parts:
        # data/machines.json is split in parts (the GitHub connector caps one push near 1 MB per call)
        d = None
        for pf in parts:
            x = json.loads(pf.read_text(encoding="utf-8"))
            if d is None:
                d = x
            else:
                d["machines"] += x["machines"]
    else:
        return 0
    before = len(d["machines"])
    d["machines"], merges = dedupe_machines(d["machines"])
    if merges:
        print(f"machine cards: merged {len(merges)} duplicate group(s) "
              f"({before} → {len(d['machines'])})")
        for m in merges:
            print(f"  {m['brand']} {m['model']}: kept {m['kept']}  (from {', '.join(m['from'])})")
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
            "s": m.get("specs") or {}, "mti": m.get("mti"), "mti2": m.get("mti2"),
            "mk": m.get("maker"),
            "c": m.get("coolant"), "cs": m.get("coolant_src")}.items() if v}
    (OUT / "b").mkdir(parents=True, exist_ok=True)
    for f in (OUT / "b").glob("*.json"):
        f.unlink()
    js = lambda o: json.dumps(o, ensure_ascii=False, separators=(",", ":"))
    (OUT / "index.json").write_text(js({"v": d.get("version"), "n": len(rows), "b": brands, "s": shards, "r": rows}), encoding="utf-8")
    for s, o in det.items():
        (OUT / "b" / f"{s}.json").write_text(js(o), encoding="utf-8")
    return len(rows)

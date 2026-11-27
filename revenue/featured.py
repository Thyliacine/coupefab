"""Featured (sponsored) supplier spots — status comes from payment, never from a manual picker.

Data model, one entry per supplier in data/revenue/featured.json:

    {
      "id": "acier-exemple",            # supplier id (data/suppliers/directory.json) or a new slug
      "name": "Acier Exemple inc.",
      "tier": "standard" | "plus",
      "logo": "/assets/sponsors/acier-exemple.svg" or "https://…",
      "blurb_fr": "…", "blurb_en": "…",  # one or two plain sentences
      "url": "https://…",                # rendered with rel="sponsored noopener"
      "categories": ["suppliers", "prices", "parts", "tooling"],
      "start": "2027-02-01", "end": "2027-02-28",   # inclusive, set from the paid period
      "subscription": {"provider": "stripe", "id": "sub_…", "status": "active", "updated": "…"}
    }

A supplier shows only when: flag featured_suppliers is on, today is within start..end, and
subscription.status is "active" or "trialing". apply_subscription_event() is the single
place that turns a spot on or off; api/stripe-webhook.js forwards payment events to it
(through FEATURED_WEBHOOK_URL / the daily refresh), so nobody edits featured status by hand.
"""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from zoneinfo import ZoneInfo

TZ = ZoneInfo("America/Toronto")
CATEGORIES = {
    "suppliers": ("/fournisseurs/", "/en/suppliers/"),
    "prices": ("/prix/", "/en/sheet-prices/"),
    "parts": ("/pieces/", "/en/parts/"),
    "tooling": ("/outillage/", "/en/tooling/"),
}
LIVE_STATUSES = {"active", "trialing"}


def today() -> str:
    return dt.datetime.now(TZ).date().isoformat()


def load(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def is_live(s: dict, on: str | None = None) -> bool:
    on = on or today()
    sub = s.get("subscription") or {}
    return (sub.get("status") in LIVE_STATUSES and bool(s.get("url"))
            and (s.get("start") or "0000") <= on <= (s.get("end") or "9999"))


def category_for_path(path: str) -> str | None:
    for cat, (fr, en) in CATEGORIES.items():
        if path in (fr, en):
            return cat
    return None


def live_for(data: dict, category: str, on: str | None = None) -> list[dict]:
    rows = [s for s in data.get("suppliers", []) if category in s.get("categories", []) and is_live(s, on)]
    # Plus tier first, then by start date (oldest sponsor first); never by price paid inside a tier
    return sorted(rows, key=lambda s: (s.get("tier") != "plus", s.get("start") or "", s.get("name", "").lower()))


def apply_subscription_event(path: Path, event: dict) -> dict:
    """Payment hook. `event` is the normalized payload sent by api/stripe-webhook.js:

        {"supplier_id": "…", "status": "active|trialing|past_due|canceled|unpaid|incomplete_expired",
         "period_start": "YYYY-MM-DD", "period_end": "YYYY-MM-DD", "subscription_id": "sub_…",
         "tier": "standard|plus", "categories": [...]?, "profile": {name, logo, blurb_fr, blurb_en, url}?}

    Creates or updates the supplier entry; status other than active/trialing turns it off
    (the entry is kept for history). Returns the updated entry."""
    path = Path(path)
    data = load(path)
    sid = str(event["supplier_id"]).strip()
    cur = next((s for s in data["suppliers"] if s["id"] == sid), None)
    if cur is None:
        cur = {"id": sid, "name": sid, "tier": "standard", "categories": ["suppliers"], "url": ""}
        data["suppliers"].append(cur)
    prof = event.get("profile") or {}
    for k in ("name", "logo", "blurb_fr", "blurb_en", "url"):
        if prof.get(k):
            cur[k] = prof[k]
    if event.get("tier") in data.get("tiers", {}):
        cur["tier"] = event["tier"]
    if event.get("categories"):
        cur["categories"] = [c for c in event["categories"] if c in CATEGORIES]
    if event.get("period_start"):
        cur["start"] = event["period_start"]
    if event.get("period_end"):
        cur["end"] = event["period_end"]
    cur["subscription"] = {"provider": "stripe", "id": event.get("subscription_id", ""),
                           "status": event.get("status", "unknown"),
                           "updated": dt.datetime.now(TZ).isoformat(timespec="seconds")}
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return cur


if __name__ == "__main__":  # python3 -m revenue.featured event.json  (apply one forwarded event by hand)
    import sys
    root = Path(__file__).resolve().parent.parent
    ev = json.loads(Path(sys.argv[1]).read_text())
    print(json.dumps(apply_subscription_event(root / "data" / "revenue" / "featured.json", ev), ensure_ascii=False, indent=1))

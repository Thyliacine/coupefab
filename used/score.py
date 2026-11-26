"""Deal badges and comparable used medians. Thresholds are documented on the page.

Rules (applied only to listings with a published asking or buy-now price):

Used median (needs at least 2 comparables):
  Super aubaine  — at least 20 % below the year-adjusted used median
  Bonne affaire  — at least 10 % below the median
  Prix du marché — within ±10 % of the median
  Cher           — at least 10 % above the median

MSRP only (official new price known, but fewer than 2 used comparables):
  Super aubaine  — at least 50 % off the published new price
  Bonne affaire  — at least 35 % off
  Prix du marché — 20–35 % off (a typical used discount, not a steal)
  Cher           — less than 20 % off new (used priced close to new)

Combined: Super aubaine also if ≥ 45 % off new AND ≥ 10 % below the used median.

Year adjustment (comparables only, never shown as an “appraised value”):
  A comparable’s price is brought to the subject year with a declining-balance
  factor of 8 % per year of age difference, capped at 10 years. Documented as a
  CoupeFab estimate. Listings with no year are compared unadjusted.

Comparables, in order, stopping at the first set with ≥ 2 members
other than the subject itself:
  1. same make + same normalized model
  2. same category + same make + same size class (when known)
  3. otherwise no used-median badge (MSRP-only rules may still apply)

Auction listings (price_type = auction) are scored, but the badge tooltip
mentions that hammer prices exclude buyer’s premium and fees.
"""
from __future__ import annotations

import datetime as dt
import re
import statistics
from typing import Any

TIER_PCT = 10          # ± % around the used median
SUPER_USED_PCT = 20    # % below median for Super aubaine
SUPER_MSRP_PCT = 50
GOOD_MSRP_PCT = 35
MARKET_MSRP_PCT = 20
SUPER_COMBO_MSRP = 45
DEPRECIATION = 0.08
DEP_CAP_YEARS = 10
STALE_DAYS = 14

BADGE_FR = {"super": "Super aubaine", "good": "Bonne affaire", "market": "Prix du marché", "high": "Cher"}
BADGE_EN = {"super": "Super deal", "good": "Good deal", "market": "Market price", "high": "High"}


def _norm_model(s: str | None) -> str:
    if not s:
        return ""
    return re.sub(r"[^a-z0-9]", "", s.lower())


def _norm_make(s: str | None) -> str:
    if not s:
        return ""
    return re.sub(r"[^a-z0-9]", "", s.lower())


def adjust_to_year(price: float, year_from: int | None, year_to: int | None) -> float:
    if not price or not year_from or not year_to or year_from == year_to:
        return price
    dy = max(-DEP_CAP_YEARS, min(DEP_CAP_YEARS, year_from - year_to))
    # older comparable (year_from < year_to): price is adjusted UP toward the newer year
    # newer comparable: price is adjusted DOWN
    return price / ((1 - DEPRECIATION) ** dy)


def comparables(subject: dict, pool: list[dict]) -> list[dict]:
    """Return the tightest comparable set with at least 2 other priced, active listings."""
    if not subject.get("price_cad"):
        return []
    sid = subject.get("id")
    mk, md = _norm_make(subject.get("make")), _norm_model(subject.get("model"))
    cat, klass = subject.get("category"), subject.get("size_class")

    def ok(l: dict) -> bool:
        if l.get("id") == sid:
            return False
        if l.get("status") not in (None, "active"):
            return False
        if not l.get("price_cad"):
            return False
        if l.get("price_type") == "auction":
            return False  # hammer / buy-now mix would skew the median
        return True

    others = [l for l in pool if ok(l)]
    if mk and md:
        s = [l for l in others if _norm_make(l.get("make")) == mk and _norm_model(l.get("model")) == md]
        if len(s) >= 2:
            return s
    if mk and cat:
        s = [l for l in others if _norm_make(l.get("make")) == mk and l.get("category") == cat]
        if klass:
            s = [l for l in s if l.get("size_class") == klass]
        if len(s) >= 2:
            return s
    if cat and klass:
        s = [l for l in others if l.get("category") == cat and l.get("size_class") == klass]
        if len(s) >= 2:
            return s
    return []


def pct_off(price: float, ref: float) -> float | None:
    if not price or not ref:
        return None
    return round((ref - price) / ref * 100.0, 1)


def _fmt_pct(p: float | None, fr: bool, kind: str) -> str:
    if p is None:
        return ""
    if fr:
        n = f"{abs(p):.0f}".replace(".", ",")
        if kind == "msrp":
            return f"{n} % sous le prix neuf" if p >= 0 else f"{n} % au-dessus du prix neuf"
        return f"{n} % sous la médiane usagée" if p >= 0 else f"{n} % au-dessus de la médiane usagée"
    n = f"{abs(p):.0f}"
    if kind == "msrp":
        return f"{n}% off new" if p >= 0 else f"{n}% above new"
    return f"{n}% below the used median" if p >= 0 else f"{n}% above the used median"


def _badge_from_rules(pct_used: float | None, n_comps: int, pct_msrp: float | None) -> str | None:
    used_ok = pct_used is not None and n_comps >= 2
    if used_ok and pct_msrp is not None and pct_msrp >= SUPER_COMBO_MSRP and pct_used >= TIER_PCT:
        return "super"
    if used_ok:
        if pct_used >= SUPER_USED_PCT:
            return "super"
        if pct_used >= TIER_PCT:
            return "good"
        if pct_used <= -TIER_PCT:
            return "high"
        return "market"
    if pct_msrp is not None:
        if pct_msrp >= SUPER_MSRP_PCT:
            return "super"
        if pct_msrp >= GOOD_MSRP_PCT:
            return "good"
        if pct_msrp >= MARKET_MSRP_PCT:
            return "market"
        return "high"
    return None


def score_one(item: dict, pool: list[dict], today: dt.date) -> dict:
    price = item.get("price_cad")
    comps = comparables(item, pool) if price else []
    median = None
    if comps:
        adjusted = [adjust_to_year(c["price_cad"], c.get("year"), item.get("year")) for c in comps]
        median = statistics.median(adjusted)
    pct_used = pct_off(price, median) if (price and median) else None
    pct_msrp = pct_off(price, item.get("msrp_cad")) if (price and item.get("msrp_cad")) else None
    n_comps = len(comps)
    badge = _badge_from_rules(pct_used, n_comps, pct_msrp) if price else None

    # reasons
    bits_fr, bits_en = [], []
    if pct_msrp is not None:
        bits_fr.append(_fmt_pct(pct_msrp, True, "msrp"))
        bits_en.append(_fmt_pct(pct_msrp, False, "msrp"))
    if pct_used is not None:
        bits_fr.append(_fmt_pct(pct_used, True, "used") + f" ({n_comps} comparables)")
        bits_en.append(_fmt_pct(pct_used, False, "used") + f" ({n_comps} comparables)")
    if item.get("price_type") == "auction":
        bits_fr.append("enchère : frais et prime d’acheteur en sus")
        bits_en.append("auction: buyer’s premium and fees extra")
    if not price:
        bits_fr.append("prix sur demande : pas de pastille")
        bits_en.append("price on request: no badge")

    first = item.get("first_seen") or item.get("last_seen")
    try:
        first_d = dt.date.fromisoformat(str(first)[:10]) if first else today
    except ValueError:
        first_d = today
    days = max(0, (today - first_d).days)

    hist = item.get("price_history") or []
    drop_pct = None
    dropped = False
    if price and hist:
        earlier = [h for h in hist if h.get("price_cad") and str(h.get("date"))[:10] < str(today)]
        if earlier:
            prev = earlier[-1]["price_cad"]
            if prev and price < prev - 1:
                dropped = True
                drop_pct = round((prev - price) / prev * 100.0, 1)

    item["used_median_cad"] = round(median, 2) if median else None
    item["pct_vs_used_median"] = pct_used
    item["pct_off_msrp"] = pct_msrp
    item["n_comps"] = n_comps
    item["badge"] = badge
    item["badge_reason_fr"] = ", ".join(bits_fr).capitalize() if bits_fr else ""
    item["badge_reason_en"] = ", ".join(bits_en).capitalize() if bits_en else ""
    item["days_on_market"] = days
    item["price_dropped"] = dropped
    item["drop_pct"] = drop_pct
    return item


def score_all(listings: list[dict], today: dt.date | None = None) -> list[dict]:
    today = today or dt.datetime.now().date()
    for it in listings:
        score_one(it, listings, today)
    return listings

"""Voluntary donation Payment Link (config/donate.json), behind the monetization switch.

The current Payment Link is Stripe test mode. Do not show it on the public site
until a live CoupeFab link is in config/donate.json (livemode true, no /test_/)
and config/monetization.json has "donations": true.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CFG = ROOT / "config" / "donate.json"


def _cfg() -> dict:
    try:
        return json.loads(CFG.read_text(encoding="utf-8"))
    except OSError:
        return {}


def enabled() -> bool:
    cfg = _cfg()
    url = str(cfg.get("url") or "")
    if not url.startswith("https://"):
        return False
    if cfg.get("livemode") is False or "/test_" in url or url.startswith("https://donate.stripe.com/test_"):
        return False
    try:
        import revenue
        return bool(revenue.on("donations"))
    except Exception:
        return False


def url() -> str:
    if not enabled():
        return ""
    return str(_cfg().get("url") or "")


def button(lang: str, cls: str = "btn-support") -> str:
    href = url()
    if not href:
        return ""
    fr = lang == "fr"
    label = "Soutenir CoupeFab" if fr else "Support CoupeFab"
    title = "Don volontaire, montant au choix (5, 10 ou 25 $ CA, ou un autre montant)." if fr else "Voluntary donation, choose an amount (CAD 5, 10 or 25, or another amount)."
    return (f'<a class="{cls}" href="{href}" target="_blank" rel="noopener noreferrer" title="{title}">'
            f"{label}</a>")

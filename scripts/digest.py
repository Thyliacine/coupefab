#!/usr/bin/env python3
"""CoupeFab price digest (newsletter) generator — email-safe HTML + plain text, FR and EN.

    python3 scripts/digest.py                 # writes digest-preview/digest-YYYY-MM-DD.{fr,en}.{html,txt}
    COUPEFAB_REVENUE_DIR=config/demo python3 scripts/digest.py   # with the demo sponsor

It only builds files; it sends nothing. digest-preview/ has no index.html, so it is never deployed.
A sponsor block («Commandité / Sponsored»: name, logo, two lines, link) is added only when the
digest_sponsor flag is on AND a sponsor in config/sponsors.json has paid=true and today in start..end.
"""
from __future__ import annotations

import datetime as dt
import html
import sys
from collections import defaultdict
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import revenue  # noqa: E402
from prices import store  # noqa: E402

SITE = "https://coupefab.vercel.app"
OUT = ROOT / "digest-preview"
TZ = ZoneInfo("America/Toronto")
FAM = {"acier": ("Acier", "Steel"), "inox": ("Inox", "Stainless"), "aluminium": ("Aluminium", "Aluminum"),
       "galvanise": ("Galvanisé", "Galvanized"), "cuivre": ("Cuivre", "Copper"), "laiton": ("Laiton", "Brass")}
e = html.escape
FLOOR = {"acier": 0.3, "galvanise": 0.4, "inox": 1.5, "aluminium": 1.5, "cuivre": 4.0, "laiton": 3.0, "bronze": 4.0}


def active_sponsor(today: str) -> dict | None:
    if not revenue.on("digest_sponsor"):
        return None
    ok = [s for s in revenue.sponsors() if s.get("paid") and str(s.get("url", "")).startswith("https://")
          and s.get("start", "0000") <= today <= s.get("end", "9999")]
    return sorted(ok, key=lambda s: s.get("start", ""))[0] if ok else None


def summary(d: dict) -> list[dict]:
    """Cheapest sheet price per lb by family, plus how many suppliers carry it."""
    by, sup = defaultdict(list), defaultdict(set)
    for r in d.get("rows", []):
        if r.get("form") != "tole" or not r.get("price_per_lb_cad"):
            continue
        by[r.get("family")].append(r)
        sup[r.get("family")].add(r.get("supplier"))
    best = {}
    for f, rs in by.items():
        floor = FLOOR.get(f, 0.3)   # drop obvious unit/scrape errors (e.g. stainless under $1.50/lb)
        ok = [r for r in rs if r["price_per_lb_cad"] >= floor] or rs
        best[f] = min(ok, key=lambda r: r["price_per_lb_cad"])
    return [dict(family=f, n=len(sup[f]), row=best[f]) for f in sorted(best, key=lambda k: (k not in FAM, k))]


def sponsor_html(s: dict, fr: bool) -> str:
    l1, l2 = s.get("line1_fr" if fr else "line1_en", ""), s.get("line2_fr" if fr else "line2_en", "")
    logo = (f'<img src="{e(s["logo"] if s["logo"].startswith("http") else SITE + s["logo"])}" alt="{e(s["name"])}" width="120" height="40" style="display:block;border:0;margin:0 0 8px">'
            if s.get("logo") else "")
    return (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:24px 0;border:1px solid #e1ded5;border-left:4px solid #c2410c;border-radius:8px;background:#fdeee6">'
            f'<tr><td style="padding:14px 16px;font:15px/1.5 Arial,sans-serif;color:#15191c">'
            f'<div style="font:600 11px Arial,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:#9a3412;margin:0 0 6px">{"Commandité" if fr else "Sponsored"}</div>'
            f'{logo}<strong>{e(s["name"])}</strong><br>{e(l1)}{"<br>" + e(l2) if l2 else ""}<br>'
            f'<a href="{e(s["url"])}" rel="sponsored" style="color:#c2410c;font-weight:600">{"En savoir plus" if fr else "Learn more"} →</a>'
            f'</td></tr></table>')


def sponsor_text(s: dict, fr: bool) -> str:
    l1, l2 = s.get("line1_fr" if fr else "line1_en", ""), s.get("line2_fr" if fr else "line2_en", "")
    return "\n".join(x for x in [f"--- {'COMMANDITÉ' if fr else 'SPONSORED'} ---", s["name"], l1, l2, s["url"], "---"] if x)


def build(lang: str, d: dict, sponsor: dict | None) -> tuple[str, str]:
    fr = lang == "fr"
    prix = SITE + ("/prix/" if fr else "/en/sheet-prices/")
    date = d.get("date", "")
    rows = summary(d)
    title = f"CoupeFab — {'prix de la tôle au' if fr else 'sheet prices as of'} {date}"
    trs, txt = [], []
    for x in rows:
        r = x["row"]
        name = FAM.get(x["family"], (x["family"].title(),) * 2)[0 if fr else 1]
        trs.append(f'<tr><td style="padding:6px 8px;border-bottom:1px solid #e1ded5">{e(name)}</td>'
                   f'<td style="padding:6px 8px;border-bottom:1px solid #e1ded5;text-align:right"><strong>{r["price_per_lb_cad"]:.2f} $/lb</strong></td>'
                   f'<td style="padding:6px 8px;border-bottom:1px solid #e1ded5;color:#586064">{e(r.get("grade") or "")} {e(r.get("description") or "")[:60]}</td>'
                   f'<td style="padding:6px 8px;border-bottom:1px solid #e1ded5;text-align:right;color:#586064">{x["n"]}</td></tr>')
        txt.append(f"- {name}: {r['price_per_lb_cad']:.2f} $/lb ({', '.join(y for y in [r.get('grade') or '', str(x['n']) + (' fournisseur(s)' if fr else ' supplier(s)')] if y)})")
    intro = (f"Les prix les plus bas par livre pour la tôle, relevés chez {len(d.get('suppliers', {}))} fournisseurs. Les prix changent : vérifiez toujours chez le fournisseur."
             if fr else f"The lowest sheet prices per pound, collected from {len(d.get('suppliers', {}))} suppliers. Prices change: always check with the supplier.")
    sp_h = sponsor_html(sponsor, fr) if sponsor else ""
    head = ("<tr><th align=left style='padding:6px 8px'>Métal</th><th align=right style='padding:6px 8px'>Le plus bas</th><th align=left style='padding:6px 8px'>Produit</th><th align=right style='padding:6px 8px'>Fourn.</th></tr>"
            if fr else "<tr><th align=left style='padding:6px 8px'>Metal</th><th align=right style='padding:6px 8px'>Lowest</th><th align=left style='padding:6px 8px'>Product</th><th align=right style='padding:6px 8px'>Suppl.</th></tr>")
    unsub = ("Vous recevez ce courriel parce que vous êtes abonné à l’infolettre CoupeFab. Pour vous désabonner, répondez « désabonner ». Responsable : Michaël Brassard, info@coupefab.ca."
             if fr else "You get this email because you subscribed to the CoupeFab newsletter. To unsubscribe, reply “unsubscribe”. Contact: Michaël Brassard, info@coupefab.ca.")
    page = f"""<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>{e(title)}</title></head>
<body style="margin:0;background:#f6f5f1"><table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td align="center" style="padding:24px 12px">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="max-width:600px;background:#fff;border:1px solid #e1ded5;border-radius:10px">
<tr><td style="padding:22px 24px;font:16px/1.6 Arial,sans-serif;color:#15191c">
<div style="font:700 20px Arial,sans-serif">CoupeFab</div>
<h1 style="font:700 22px/1.3 Arial,sans-serif;margin:14px 0 8px">{e(title)}</h1>
<p style="margin:0 0 14px;color:#586064">{e(intro)}</p>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="font:14px Arial,sans-serif;border-collapse:collapse">{head}{"".join(trs)}</table>
<p style="margin:16px 0"><a href="{prix}" style="background:#c2410c;color:#fff;text-decoration:none;font-weight:600;padding:10px 16px;border-radius:8px;display:inline-block">{"Comparer tous les prix" if fr else "Compare all prices"} →</a></p>
{sp_h}
<p style="font-size:12px;color:#7d8488;margin:18px 0 0">{e(unsub)}</p>
</td></tr></table></td></tr></table></body></html>
"""
    text = "\n".join([title, "", intro, "", *txt, "", f"{'Comparer tous les prix' if fr else 'Compare all prices'}: {prix}", "",
                      *( [sponsor_text(sponsor, fr), ""] if sponsor else []), unsub]) + "\n"
    return page, text


def main() -> None:
    d = store.read_latest(ROOT / "data" / "prices")
    today = dt.datetime.now(TZ).date().isoformat()
    sp = active_sponsor(today)
    OUT.mkdir(exist_ok=True)
    for lang in ("fr", "en"):
        h, t = build(lang, d, sp)
        (OUT / f"digest-{d.get('date', today)}.{lang}.html").write_text(h, encoding="utf-8")
        (OUT / f"digest-{d.get('date', today)}.{lang}.txt").write_text(t, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}/digest-{d.get('date', today)}.{{fr,en}}.{{html,txt}}; sponsor: {sp['name'] if sp else 'none'}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""CoupeFab admin — a small LOCAL page to edit the revenue settings. Never deployed.

    python3 scripts/admin.py            # then open http://127.0.0.1:8765/
    python3 scripts/admin.py --port 9000

What it edits (plain JSON files in the repo; rebuild + commit + push afterwards):
  - Switches ........ config/monetization.json
  - Partner ......... content/shops.json  ("partner": true — unpaid « Partenaire » label)
  - Digest sponsors . config/sponsors.json
  - Affiliate links . config/affiliate-links.json (url only after you joined a program yourself)
What it only SHOWS: featured suppliers (data/revenue/featured.json). Featured = an active paid
subscription; the payment hook (api/stripe-webhook.js -> revenue.featured) turns it on and off.
Binds to 127.0.0.1 only. No login, no network calls.
"""
from __future__ import annotations

import argparse
import html
import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from revenue import FLAGS  # noqa: E402
from revenue import featured as feat  # noqa: E402

F_FLAGS = ROOT / "config" / "monetization.json"
F_SHOPS = ROOT / "content" / "shops.json"
F_SPONS = ROOT / "config" / "sponsors.json"
F_AFF = ROOT / "config" / "affiliate-links.json"
F_FEAT = ROOT / "data" / "revenue" / "featured.json"
e = lambda s: html.escape(str(s if s is not None else ""), quote=True)  # noqa: E731
LABELS = {
    "featured_suppliers": ("Fournisseurs en vedette", "Bloc « En vedette » (payé) en haut des fournisseurs, prix, pièces, outillage"),
    "affiliate_links": ("Liens affiliés", "Encadré « Où acheter » + texte de divulgation (seulement les liens avec une URL)"),
    "digest_sponsor": ("Commandite de l’infolettre", "Encadré « Commandité » dans scripts/digest.py"),
    "quote_requests": ("Demandes de soumission", "Page /soumission/ publiée, liens dans le pied de page et sur fournisseurs/pièces/outillage"),
    "advertise_page": ("Page « Annoncer »", "Page /annoncer/ publiée (tarifs encore « à déterminer »)"),
}
SP_FIELDS = ["id", "name", "logo", "url", "line1_fr", "line2_fr", "line1_en", "line2_en", "start", "end"]
AFF_FIELDS = ["key", "merchant", "label_fr", "label_en", "url"]


def load(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def save(p: Path, d: dict, indent=2) -> None:
    txt = json.dumps(d, ensure_ascii=False, indent=indent)
    p.write_text(txt if p == F_SHOPS else txt + "\n", encoding="utf-8")


def page(msg: str = "") -> str:
    fl, shops, sp, aff, ft = load(F_FLAGS), load(F_SHOPS), load(F_SPONS), load(F_AFF), load(F_FEAT)
    flag_rows = "".join(
        f'<label class="row"><input type="checkbox" name="flag" value="{k}"{" checked" if fl.get(k) else ""}> <b>{e(LABELS[k][0])}</b> <small>{e(LABELS[k][1])}</small></label>'
        for k in FLAGS)
    shop_rows = "".join(
        f'<label class="row"><input type="checkbox" name="partner" value="{e(k)}"{" checked" if v.get("partner") else ""}> {e(v["name"])} <small>{e(v.get("city", ""))}</small></label>'
        for k, v in sorted(shops["shops"].items(), key=lambda kv: kv[1]["name"].lower()))
    def sp_row(i, s):
        cells = "".join(f'<td><input name="sp{i}_{f}" value="{e(s.get(f, ""))}" {"type=date" if f in ("start", "end") else ""}></td>' for f in SP_FIELDS)
        return f'<tr>{cells}<td><input type="checkbox" name="sp{i}_paid"{" checked" if s.get("paid") else ""}></td><td><input type="checkbox" name="sp{i}_del"></td></tr>'
    sps = sp.get("sponsors", [])
    sp_rows = "".join(sp_row(i, s) for i, s in enumerate(sps)) + sp_row(len(sps), {})
    aff_rows = "".join(
        "<tr>" + "".join(f'<td><input name="af{i}_{f}" value="{e(l.get(f, ""))}"{" readonly" if f == "key" else ""}></td>' for f in AFF_FIELDS)
        + f'<td><small>{e(", ".join(l.get("pages", [])))}</small></td></tr>'
        for i, l in enumerate(aff.get("links", [])))
    today = feat.today()
    ft_rows = "".join(
        f'<tr><td>{e(s.get("name"))}</td><td>{e(s.get("tier"))}</td><td>{e((s.get("subscription") or {}).get("status", "—"))}</td>'
        f'<td>{e(s.get("start"))} → {e(s.get("end"))}</td><td>{e(", ".join(s.get("categories", [])))}</td>'
        f'<td>{"✅ affiché" if feat.is_live(s, today) and fl.get("featured_suppliers") else ("payé, interrupteur off" if feat.is_live(s, today) else "—")}</td></tr>'
        for s in ft.get("suppliers", [])) or '<tr><td colspan="6"><i>Aucun abonnement payé pour l’instant.</i></td></tr>'
    note = f'<p class="msg">{e(msg)}</p>' if msg else ""
    return f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>CoupeFab — admin local</title>
<style>body{{font:15px/1.5 system-ui,sans-serif;max-width:76rem;margin:0 auto;padding:1.5rem;background:#f6f5f1;color:#15191c}}
section{{background:#fff;border:1px solid #e1ded5;border-radius:10px;padding:1rem 1.2rem;margin:1rem 0}}h1{{margin:.2rem 0}}h2{{margin:.2rem 0 .6rem;font-size:1.1rem}}
.row{{display:block;padding:.3rem .4rem;border-radius:6px}}.row:hover{{background:#fdeee6}}.row input:checked+b{{color:#c2410c}}small{{color:#586064}}
table{{border-collapse:collapse;width:100%}}td,th{{border-bottom:1px solid #e1ded5;padding:.3rem;text-align:left;font-size:.88rem;vertical-align:top}}td input{{width:100%;font:inherit;padding:.25rem}}
button{{background:#c2410c;color:#fff;border:0;border-radius:8px;padding:.55rem 1rem;font-weight:600;cursor:pointer}}button:hover{{background:#9a3412}}
.msg{{background:#e7f4ec;color:#1f6b3d;padding:.6rem .8rem;border-radius:8px;font-weight:600}}.ro{{background:#f3ecd6}}</style></head><body>
<h1>CoupeFab — admin local</h1><p><small>Modifie des fichiers JSON du dépôt. Ensuite : <code>python3 build.py</code>, vérifier, commit, push, déployer.</small></p>{note}
<form method="post" action="/save">
<section><h2>Interrupteurs</h2>{flag_rows}</section>
<section><h2>Partenaire (non rémunéré)</h2><p><small>Ajoute la pastille « Partenaire » dans les listes d’ateliers des guides. À divulguer (page Divulgation).</small></p>{shop_rows}</section>
<section><h2>Commanditaires de l’infolettre</h2><p><small>Un seul est utilisé par numéro (le premier payé dont la période inclut la date d’envoi). URL en https://, 90 caractères max par ligne.</small></p>
<table><tr>{"".join(f"<th>{f}</th>" for f in SP_FIELDS)}<th>payé</th><th>suppr.</th></tr>{sp_rows}</table></section>
<section><h2>Liens affiliés</h2><p><small>Laisser l’URL vide tant que vous n’êtes pas inscrit vous-même au programme. Une URL vide n’est jamais affichée.</small></p>
<table><tr>{"".join(f"<th>{f}</th>" for f in AFF_FIELDS)}<th>pages</th></tr>{aff_rows}</table></section>
<p><button type="submit">Enregistrer</button></p></form>
<section class="ro"><h2>Fournisseurs en vedette (lecture seule)</h2><p><small>En vedette = abonnement payé actif. Géré uniquement par le crochet de paiement (api/stripe-webhook.js → revenue.featured). Pas de sélection manuelle.</small></p>
<table><tr><th>Nom</th><th>Niveau</th><th>Abonnement</th><th>Période</th><th>Pages</th><th>État</th></tr>{ft_rows}</table></section>
</body></html>"""


def apply(form: dict[str, list[str]]) -> str:
    g = lambda k: (form.get(k) or [""])[0].strip()  # noqa: E731
    fl = load(F_FLAGS)
    chosen = set(form.get("flag", []))
    for k in FLAGS:
        fl[k] = k in chosen
    save(F_FLAGS, fl)
    shops = load(F_SHOPS)
    partners = set(form.get("partner", []))
    for k, v in list(shops["shops"].items()):
        v.pop("partner", None)
        if k in partners:  # keep the usual key order: name, city, url, partner, fr, en
            items = list(v.items())
            at = next((i + 1 for i, (kk, _) in enumerate(items) if kk == "url"), len(items))
            shops["shops"][k] = dict(items[:at] + [("partner", True)] + items[at:])
    save(F_SHOPS, shops, indent=1)
    sp = load(F_SPONS)
    out, errs = [], []
    idx = sorted({int(k[2:].split("_")[0]) for k in form if k.startswith("sp") and k[2:].split("_")[0].isdigit()})
    for i in idx[:200]:
        row = {f: g(f"sp{i}_{f}") for f in SP_FIELDS}
        row["paid"] = f"sp{i}_paid" in form
        if f"sp{i}_del" in form or not (row["id"] or row["name"] or row["url"]):
            continue
        if not row["url"].startswith("https://") or not row["id"] or not row["name"] or not row["line1_fr"] or not row["line1_en"]:
            errs.append(f"commanditaire « {row['name'] or row['id']} » ignoré : id, nom, URL https et ligne 1 FR/EN requis")
            continue
        out.append({k: v for k, v in row.items() if v != ""})
    sp["sponsors"] = out
    save(F_SPONS, sp)
    aff = load(F_AFF)
    for i, l in enumerate(aff.get("links", [])):
        for f in AFF_FIELDS[1:]:
            if f"af{i}_{f}" in form:
                l[f] = g(f"af{i}_{f}")
        if l["url"] and not l["url"].startswith("https://"):
            errs.append(f"lien {l['key']} : URL ignorée (https:// requis)")
            l["url"] = ""
    save(F_AFF, aff)
    return "Enregistré. Relancez python3 build.py." + ((" Attention : " + "; ".join(errs)) if errs else "")


class H(BaseHTTPRequestHandler):
    def _send(self, body: str, code=200):
        b = body.encode("utf-8")
        self.send_response(code)
        self.send_header("content-type", "text/html; charset=utf-8")
        self.send_header("content-length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        self._send(page() if self.path in ("/", "/index.html") else "not found", 200 if self.path in ("/", "/index.html") else 404)

    def do_POST(self):
        if self.path != "/save" or self.headers.get("Origin", "http://127.0.0.1").split(":")[1] not in ("//127.0.0.1", "//localhost"):
            return self._send("forbidden", 403)
        n = min(int(self.headers.get("content-length") or 0), 500_000)
        form = parse_qs(self.rfile.read(n).decode("utf-8"), keep_blank_values=True)
        self._send(page(apply(form)))

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8765)
    a = ap.parse_args()
    print(f"CoupeFab admin: http://127.0.0.1:{a.port}/  (Ctrl+C to stop)")
    HTTPServer(("127.0.0.1", a.port), H).serve_forever()

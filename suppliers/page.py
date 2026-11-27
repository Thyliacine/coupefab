"""Supplier directory pages: /fournisseurs/ (FR) and /en/suppliers/ (EN).

Rendered from data/suppliers/directory.json (built by `python -m suppliers.directory`).
Static cards for SEO; js/fournisseurs.js filters them in place and posts the
"Ajoutez vos prix / Add your prices" form to /api/supplier-submit (manual review, never auto-published).
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "suppliers" / "directory.json"
PATH_FR, PATH_EN = "/fournisseurs/", "/en/suppliers/"


def esc(s):
    return str(s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def ver(rel):
    return hashlib.sha1((ROOT / rel).read_bytes()).hexdigest()[:8]


def nfr(n):
    return f"{n:,}".replace(",", "\u202f")


def _card(s, d, fr):
    L = (lambda a, b: a if fr else b)
    cats = "".join(f'<li>{esc(d["cats"][c][0 if fr else 1])}</li>' for c in s["cats"])
    provs = ", ".join(esc(d["provs"].get(p, [p, p])[0 if fr else 1]) for p in s["provs"]) or L("Région non précisée", "Region not listed")
    cities = " · ".join(esc(c) for c in s["cities"][:4]) + (f' {L("et", "and")} {len(s["cities"]) - 4} {L("autres", "more")}' if len(s["cities"]) > 4 else "")
    badges = []
    if s.get("verified"):
        badges.append(f'<span class="sp-b sp-b-ver">{L("Prix vérifiés", "Verified prices")}</span>')
    if s["public_prices"]:
        badges.append(f'<span class="sp-b sp-b-pub">{L("Prix publics", "Public prices")}</span>')
    else:
        badges.append(f'<span class="sp-b sp-b-quote">{L("Prix sur demande", "Quote only")}</span>')
    tracked = ""
    if s.get("rows"):
        rows_fr, rows_en = nfr(s["rows"]), f'{s["rows"]:,}'
        tracked = (f'<a class="sp-tracked" href="{L("/prix/", "/en/sheet-prices/")}">'
                   f'{L(rows_fr + " prix dans le comparateur", rows_en + " prices in the price tool")} →</a>')
    if s.get("tooling_rows"):
        n_t = s["tooling_rows"]
        tracked += (f'<a class="sp-tracked" href="{L("/outillage/", "/en/tooling/")}">'
                    f'{L(nfr(n_t) + " prix d’outillage", f"{n_t:,} tooling prices")} →</a>')
    host = s["site"].split("//", 1)[-1] if s["site"] else ""
    site = (f'<a class="sp-site" href="{esc(s["site"])}" target="_blank" rel="noopener nofollow">{esc(host)} <span aria-hidden="true">↗</span></a>'
            if s["site"] else "")
    return (f'<li class="sp-card" data-prov="{" ".join(s["provs"])}" data-cats="{" ".join(s["cats"])}" '
            f'data-pub="{1 if s["public_prices"] else 0}" data-lang="{" ".join(s["langs"])}" '
            f'data-name="{esc(s["name"].lower())} {esc(" ".join(s["cities"]).lower())}">'
            f'<div class="sp-top"><h3>{esc(s["name"])}</h3><div class="sp-badges">{"".join(badges)}</div></div>'
            f'<p class="sp-loc">{cities}{" — " if cities else ""}<b>{provs}</b></p>'
            f'<ul class="sp-cats">{cats}</ul>'
            f'<div class="sp-foot">{site}{tracked}</div></li>')


def render(form_newsletter=None):
    d = json.loads(DATA.read_text())
    from suppliers.directory import add_tooling, CATS
    d["suppliers"] = add_tooling(d["suppliers"])
    d["suppliers"].sort(key=lambda x: (0 if "QC" in x["provs"] else 1, x["name"].lower()))
    d["cats"].setdefault("tooling", [CATS["tooling"][0], CATS["tooling"][1]])
    sup = d["suppliers"]

    def page(fr):
        L = (lambda a, b: a if fr else b)
        n, n_qc = len(sup), sum("QC" in s["provs"] for s in sup)
        n_pub = sum(s["public_prices"] for s in sup)
        prov_used = [p for p in d["provs"] if any(p in s["provs"] for s in sup)]
        prov_opts = "".join(f'<option value="{p}">{esc(d["provs"][p][0 if fr else 1])}</option>' for p in prov_used)
        cat_opts = "".join(f'<option value="{c}">{esc(v[0 if fr else 1])}</option>' for c, v in d["cats"].items())
        cards = "".join(_card(s, d, fr) for s in sup)
        return f'''<link rel="stylesheet" href="/css/fournisseurs.css?v={ver("css/fournisseurs.css")}">
<div class="sp" id="sp-app" data-lang="{L("fr", "en")}">
<section class="sp-hero">
  <p class="sp-kicker">{L("Répertoire", "Directory")}</p>
  <h1>{L("Fournisseurs de métal au Québec et au Canada", "Metal suppliers in Quebec and across Canada")}</h1>
  <p class="sp-lede">{L(f"{n} fournisseurs, dont {n_qc} au Québec : centres de service, aluminium, inox, tubes, découpe sur mesure, surplus et outillage d’atelier. {n_pub} publient leurs prix en ligne; les autres répondent sur demande.",
                       f"{n} suppliers, {n_qc} of them in Quebec: service centres, aluminum, stainless, tube, cut-to-size, surplus and shop tooling. {n_pub} publish prices online; the rest quote on request.")}</p>
  <div class="sp-hero-cta"><a class="btn" href="#ajouter">{L("Ajoutez vos prix", "Add your prices")}</a><a class="btn-ghost" href="{L("/prix/", "/en/sheet-prices/")}">{L("Comparer les prix publiés", "Compare published prices")}</a></div>
</section>

<form class="sp-filters" id="sp-filters" role="search" aria-label="{L("Filtrer les fournisseurs", "Filter suppliers")}" onsubmit="return false">
  <label class="sp-q"><span>{L("Rechercher", "Search")}</span><input type="search" name="q" autocomplete="off" placeholder="{L("Nom ou ville (ex. Joliette, Picard)", "Name or city (e.g. Laval, Russel)")}"></label>
  <label><span>{L("Province", "Province")}</span><select name="prov"><option value="" selected>{L("Tous", "All")}</option>{prov_opts}</select></label>
  <label><span>{L("Catégorie", "Category")}</span><select name="cat"><option value="" selected>{L("Tous", "All")}</option>{cat_opts}</select></label>
  <label><span>{L("Prix", "Prices")}</span><select name="pub"><option value="" selected>{L("Tous", "All")}</option><option value="1">{L("Prix publics", "Public prices")}</option><option value="0">{L("Sur demande", "Quote only")}</option></select></label>
  <label><span>{L("Langue de service", "Service language")}</span><select name="lang"><option value="" selected>{L("Tous", "All")}</option><option value="fr">{L("Français", "French")}</option><option value="en">{L("Anglais", "English")}</option></select></label>
  <button type="button" class="sp-reset" data-reset>{L("Réinitialiser", "Reset")}</button>
</form>
<h2 class="vh">{L("Liste des fournisseurs", "Supplier list")}</h2>
<p class="sp-count" id="sp-count" aria-live="polite">{L(f"{n} fournisseurs", f"{n} suppliers")}</p>
<ul class="sp-grid" id="sp-grid">{cards}</ul>
<p class="sp-empty" id="sp-empty" hidden>{L("Aucun fournisseur pour ces filtres.", "No supplier matches these filters.")}</p>
<p class="sp-note">{L("Informations publiques tirées des sites des fournisseurs (nom, villes, site web). Catégories déduites par CoupeFab : vérifiez auprès du fournisseur. Une erreur ou un oubli? Utilisez le formulaire ci-dessous.",
                      "Public information from suppliers’ own websites (name, cities, website). Categories are inferred by CoupeFab: confirm with the supplier. Spotted an error or a gap? Use the form below.")}</p>

<section class="sp-submit" id="ajouter" aria-labelledby="sp-submit-h">
  <div class="sp-submit-intro">
    <p class="sp-kicker">{L("Pour les fournisseurs", "For suppliers")}</p>
    <h2 id="sp-submit-h">{L("Ajoutez vos prix", "Add your prices")}</h2>
    <p>{L("Envoyez votre liste de prix (PDF, CSV ou Excel) ou le lien vers vos prix en ligne. Après vérification manuelle par CoupeFab, vos prix entrent dans le comparateur avec la mention « Prix vérifiés » et un lien vers votre site.",
          "Send your price list (PDF, CSV or Excel) or a link to your online prices. Once CoupeFab has reviewed it by hand, your prices join the price tool with a “Verified prices” badge and a link to your website.")}</p>
    <p class="sp-brochure"><a class="btn-ghost" href="{L("/fournisseurs/envoyer-brochure/", "/en/suppliers/send-brochure/")}">{L("Envoyer une brochure ou une liste de prix (10 Mo)", "Send a brochure or price list (10 MB)")} →</a></p>
    <ul class="sp-perks">
      <li>{L("Badge « Prix vérifiés » sur votre fiche et dans le comparateur", "“Verified prices” badge on your listing and in the price tool")}</li>
      <li>{L("Lien direct vers votre site (sans paramètre d’affiliation)", "Direct link to your website (no affiliate parameters)")}</li>
      <li>{L("Rien n’est publié sans vérification; vous pouvez retirer vos prix en tout temps", "Nothing goes live unreviewed; you can withdraw your prices at any time")}</li>
    </ul>
  </div>
  <form class="sp-form" id="sp-form" novalidate>
    <label>{L("Nom de l’entreprise", "Company name")} <input type="text" name="company" required maxlength="200" autocomplete="organization"></label>
    <label>{L("Courriel de contact", "Contact email")} <input type="email" name="email" required maxlength="200" autocomplete="email"></label>
    <label>{L("Site web", "Website")} <input type="url" name="site" maxlength="300" placeholder="https://" inputmode="url"></label>
    <label>{L("Lien vers vos prix (facultatif)", "Link to your prices (optional)")} <input type="url" name="price_url" maxlength="500" placeholder="https://" inputmode="url"></label>
    <label class="sp-file">{L("Liste de prix : PDF, CSV ou Excel, 2 Mo max (facultatif)", "Price list: PDF, CSV or Excel, 2 MB max (optional)")} <input type="file" name="file" accept=".pdf,.csv,.xls,.xlsx,application/pdf,text/csv"></label>
    <label>{L("Message (facultatif)", "Message (optional)")} <textarea name="message" maxlength="2000" rows="3"></textarea></label>
    <label class="sp-hp" aria-hidden="true">Website <input type="text" name="website" tabindex="-1" autocomplete="off"></label>
    <label class="consent"><input type="checkbox" name="consent" required> <span>{L("Je représente cette entreprise et j’autorise CoupeFab à publier ces prix, avec la source et la date, après vérification. CoupeFab peut m’écrire au sujet de cette soumission.",
                                                                                         "I represent this company and allow CoupeFab to publish these prices, with source and date, after review. CoupeFab may email me about this submission.")}</span></label>
    <button class="btn" type="submit">{L("Envoyer pour vérification", "Send for review")}</button>
    <p class="sp-status" role="status" aria-live="polite"></p>
  </form>
</section>
</div>
<script src="/js/fournisseurs.js?v={ver("js/fournisseurs.js")}" defer></script>'''

    return page(True), page(False)


def page_entries():
    fr, en = render()
    return [
        (PATH_FR, PATH_EN, "fr", "Fournisseurs de métal au Québec et au Canada — répertoire — CoupeFab",
         "Répertoire des fournisseurs d’acier, d’aluminium, d’inox et de tubes au Québec et au Canada : villes, catégories, prix publics ou sur demande. Ajoutez vos prix.",
         fr, False, False),
        (PATH_EN, PATH_FR, "en", "Metal suppliers in Quebec and Canada — directory — CoupeFab",
         "Directory of steel, aluminum, stainless and tube suppliers in Quebec and across Canada: cities, categories, public or quote-only prices. Add your prices.",
         en, False, False),
    ]

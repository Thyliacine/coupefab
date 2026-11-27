"""Supplier directory and 'Add your prices' landing pages (FR + EN)."""
import hashlib
import json
from pathlib import Path

from .directory import CATS, add_tooling, key
from .phones import load as load_phones
from .stats import fmt, proof

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "suppliers" / "directory.json"
PATH_FR, PATH_EN = "/fournisseurs/", "/en/suppliers/"
ADD_FR, ADD_EN = "/ajouter-vos-prix/", "/en/add-your-prices/"

# Material categories vs services (cut-to-size, retail, online, tooling…).
CAT_KEYS = ("steel", "alu", "inox", "alloys", "tube")
SVC_KEYS = ("cut", "machining", "sheetmetal", "welding", "retail", "surplus", "online", "tooling")


def esc(s):
    return str(s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def ver(rel):
    return hashlib.sha1((ROOT / rel).read_bytes()).hexdigest()[:8]


def qc_flag():
    return (
        '<span class="sp-qc" title="Québec">'
        '<svg viewBox="0 0 32 20" aria-hidden="true" focusable="false">'
        '<rect width="32" height="20" fill="#003da5"/>'
        '<path fill="#fff" d="M14 0h4v20h-4zM0 8h32v4H0z"/>'
        '<g fill="#fff">'
        '<path d="M6.4 3.1l.5 1.4h1.5l-1.2.9.5 1.4-1.3-.9-1.3.9.5-1.4-1.2-.9h1.5z"/>'
        '<path d="M23.4 3.1l.5 1.4h1.5l-1.2.9.5 1.4-1.3-.9-1.3.9.5-1.4-1.2-.9h1.5z"/>'
        '<path d="M6.4 12.2l.5 1.4h1.5l-1.2.9.5 1.4-1.3-.9-1.3.9.5-1.4-1.2-.9h1.5z"/>'
        '<path d="M23.4 12.2l.5 1.4h1.5l-1.2.9.5 1.4-1.3-.9-1.3.9.5-1.4-1.2-.9h1.5z"/>'
        '</g></svg></span>'
    )


def submit_form(fr: bool, compact: bool = False) -> str:
    L = (lambda a, b: a if fr else b)
    return f'''<form class="sp-form" id="sp-form" novalidate>
    <label>{L("Nom de l’entreprise", "Company name")} <input type="text" name="company" required maxlength="200" autocomplete="organization"></label>
    <label>{L("Courriel de contact", "Contact email")} <input type="email" name="email" required maxlength="200" autocomplete="email"></label>
    <label>{L("Site web (facultatif)", "Website (optional)")} <input type="url" name="site" maxlength="300" placeholder="https://" inputmode="url"></label>
    <label>{L("Lien vers vos prix (facultatif)", "Link to your prices (optional)")} <input type="url" name="price_url" maxlength="500" placeholder="https://" inputmode="url"></label>
    <label class="sp-file">{L("Liste de prix : PDF, CSV ou Excel, 2 Mo max (facultatif)", "Price list: PDF, CSV or Excel, 2 MB max (optional)")} <input type="file" name="file" accept=".pdf,.csv,.xls,.xlsx,application/pdf,text/csv"></label>
    <label>{L("Message (facultatif)", "Message (optional)")} <textarea name="message" maxlength="2000" rows="{2 if compact else 3}"></textarea></label>
    <label class="sp-hp" aria-hidden="true">Website <input type="text" name="website" tabindex="-1" autocomplete="off"></label>
    <label class="consent"><input type="checkbox" name="consent" required> <span>{L("Je représente cette entreprise et j’autorise CoupeFab à publier ces prix, avec la source et la date, après vérification. CoupeFab peut m’écrire au sujet de cette soumission.",
                                                                                         "I represent this company and allow CoupeFab to publish these prices, with source and date, after review. CoupeFab may email me about this submission.")}</span></label>
    <button class="btn" type="submit">{L("Envoyer pour vérification", "Send for review")}</button>
    <p class="sp-status" role="status" aria-live="polite"></p>
  </form>
  <script src="/js/ajouter-prix.js?v={ver("js/ajouter-prix.js")}" defer></script>'''


def _card(s, d, fr, phones):
    L = (lambda a, b: a if fr else b)
    cats = [c for c in s["cats"] if c in CAT_KEYS or c not in SVC_KEYS]
    svcs = [c for c in s["cats"] if c in SVC_KEYS]
    cat_lis = "".join(f'<li>{esc(d["cats"].get(c, [c, c])[0 if fr else 1])}</li>' for c in cats)
    svc_lis = "".join(f'<li>{esc(d["cats"].get(c, [c, c])[0 if fr else 1])}</li>' for c in svcs)
    provs = ", ".join(esc(d["provs"].get(p, [p, p])[0 if fr else 1]) for p in s["provs"]) or L("Région non précisée", "Region not listed")
    cities = " · ".join(esc(c) for c in s["cities"][:3]) + (
        f' {L("et", "and")} {len(s["cities"]) - 3} {L("autres", "more")}' if len(s["cities"]) > 3 else "")
    loc = " — ".join(x for x in (cities, f"<b>{provs}</b>") if x)
    has_prices = bool(s.get("public_prices") or s.get("rows") or s.get("tooling_rows"))
    badge = (f'<span class="sp-b sp-b-pub">{L("Prix disponibles", "Prices available")}</span>'
             if has_prices else "")
    if s.get("verified"):
        badge = f'<span class="sp-b sp-b-ver">{L("Prix vérifiés", "Verified prices")}</span>' + badge
    host = s["site"].split("//", 1)[-1].removeprefix("www.") if s.get("site") else ""
    site = (f'<a class="sp-site" href="{esc(s["site"])}" target="_blank" rel="noopener nofollow">{esc(host)}</a>'
            if s.get("site") else "")
    phone = phones.get(s.get("id") or "") or phones.get(key(s["name"]))
    tel = f'<a class="sp-tel" href="tel:{esc(phone)}">{esc(phone)}</a>' if phone else ""
    flag = qc_flag() if "QC" in (s.get("provs") or []) else ""
    city0 = (s["cities"][0] if s.get("cities") else "")
    return (
        f'<li class="sp-card" data-prov="{" ".join(s["provs"])}" data-cats="{" ".join(cats)}" '
        f'data-svc="{" ".join(svcs)}" data-pub="{1 if has_prices else 0}" '
        f'data-lang="{" ".join(s.get("langs") or [])}" data-city="{esc(city0.lower())}" '
        f'data-name="{esc(s["name"].lower())} {esc(" ".join(s.get("cities") or []).lower())} {esc(host.lower())}">'
        f'<div class="sp-top"><h3>{esc(s["name"])}{flag}</h3>{badge}</div>'
        f'<p class="sp-loc">{loc}</p>'
        f'{("<ul class=\"sp-cats\">" + cat_lis + "</ul>") if cat_lis else ""}'
        f'{("<ul class=\"sp-cats sp-svcs\">" + svc_lis + "</ul>") if svc_lis else ""}'
        f'<div class="sp-foot">{site}{tel}</div></li>'
    )


def directory_body(fr: bool) -> str:
    L = (lambda a, b: a if fr else b)
    p = proof()
    d, sup = p["meta"], p["suppliers"]
    d["cats"].setdefault("tooling", [CATS["tooling"][0], CATS["tooling"][1]] if "tooling" in CATS else ["Outillage", "Tooling"])
    sup.sort(key=lambda x: (0 if "QC" in x["provs"] else 1, x["name"].lower()))
    phones = load_phones()
    n, n_qc, n_pub, n_prices = p["n_dir"], p["n_qc"], p["n_with_prices"], p["n_prices"]
    prov_used = [pr for pr in d["provs"] if any(pr in s["provs"] for s in sup)]
    prov_opts = "".join(f'<option value="{pr}">{esc(d["provs"][pr][0 if fr else 1])}</option>' for pr in prov_used)
    cat_opts = "".join(f'<option value="{c}">{esc(d["cats"][c][0 if fr else 1])}</option>'
                       for c in CAT_KEYS if c in d["cats"])
    svc_opts = "".join(f'<option value="{c}">{esc(d["cats"][c][0 if fr else 1])}</option>'
                       for c in SVC_KEYS if c in d["cats"] or c == "tooling")
    cards = "".join(_card(s, d, fr, phones) for s in sup)
    return f'''<link rel="stylesheet" href="/css/fournisseurs.css?v={ver("css/fournisseurs.css")}">
<div class="sp" id="sp-app" data-lang="{L("fr", "en")}">
<section class="sp-hero">
  <p class="sp-kicker">{L("Répertoire", "Directory")}</p>
  <h1>{L("Fournisseurs de métal au Québec et au Canada", "Metal suppliers in Quebec and across Canada")}</h1>
  <p class="sp-lede">{L(f"{fmt(n, 'fr')} fournisseurs, dont {fmt(n_qc, 'fr')} au Québec. {fmt(n_pub, 'fr')} y publient déjà des prix — {fmt(n_prices, 'fr')} prix suivis dans les comparateurs.",
                       f"{fmt(n, 'en')} suppliers, {fmt(n_qc, 'en')} of them in Quebec. {fmt(n_pub, 'en')} already publish prices — {fmt(n_prices, 'en')} prices tracked in the tools.")}</p>
  <div class="sp-hero-cta"><a class="btn" href="{L(ADD_FR, ADD_EN)}">{L("Ajoutez vos prix", "Add your prices")}</a><a class="btn-ghost" href="{L("/prix/", "/en/sheet-prices/")}">{L("Comparer les prix publiés", "Compare published prices")}</a></div>
</section>

<form class="sp-filters" id="sp-filters" role="search" aria-label="{L("Filtrer les fournisseurs", "Filter suppliers")}" onsubmit="return false">
  <label class="sp-q"><span>{L("Rechercher", "Search")}</span><input type="search" name="q" autocomplete="off" placeholder="{L("Nom, ville ou site", "Name, city or site")}"></label>
  <label><span>{L("Région", "Region")}</span><select name="region"><option value="" selected>{L("Toutes", "All")}</option>{prov_opts}</select></label>
  <label><span>{L("Catégorie", "Category")}</span><select name="cat"><option value="" selected>{L("Toutes", "All")}</option>{cat_opts}</select></label>
  <label><span>{L("Service", "Service")}</span><select name="svc"><option value="" selected>{L("Tous", "All")}</option>{svc_opts}</select></label>
  <label><span>{L("Trier", "Sort")}</span><select name="sort">
    <option value="qc" selected>{L("Québec d’abord", "Quebec first")}</option>
    <option value="name">{L("Nom (A–Z)", "Name (A–Z)")}</option>
    <option value="prices">{L("Prix disponibles d’abord", "Prices available first")}</option>
    <option value="city">{L("Ville", "City")}</option>
  </select></label>
  <button type="button" class="sp-reset" data-reset>{L("Réinitialiser", "Reset")}</button>
</form>
<h2 class="vh">{L("Liste des fournisseurs", "Supplier list")}</h2>
<p class="sp-count" id="sp-count" aria-live="polite">{L(f"{fmt(n, 'fr')} fournisseurs", f"{fmt(n, 'en')} suppliers")}</p>
<ul class="sp-grid" id="sp-grid">{cards}</ul>
<nav class="cf-pager" id="sp-pager" hidden></nav>
<p class="sp-empty" id="sp-empty" hidden>{L("Aucun fournisseur pour ces filtres.", "No supplier matches these filters.")}</p>
<p class="sp-note">{L("Informations publiques tirées des sites des fournisseurs (nom, villes, site web, téléphone s’il est affiché). Catégories déduites par CoupeFab : vérifiez auprès du fournisseur.",
                      "Public information from suppliers’ own websites (name, cities, website, and phone when listed). Categories are inferred by CoupeFab: confirm with the supplier.")}</p>
<p class="sp-repeat"><a class="btn-ghost" href="{L(ADD_FR, ADD_EN)}">{L("Vous vendez du métal ou de l’outillage? Ajoutez vos prix.", "Do you sell metal or tooling? Add your prices.")}</a> <a class="btn-ghost" href="{L("/fournisseurs/envoyer-brochure/", "/en/suppliers/send-brochure/")}">{L("Envoyer une brochure (10 Mo)", "Send a brochure (10 MB)")}</a></p>
</div>
<script src="/js/fournisseurs.js?v={ver("js/fournisseurs.js")}" defer></script>'''


def landing_body(fr: bool) -> str:
    L = (lambda a, b: a if fr else b)
    p = proof()
    n_pub, n_prices = p["n_with_prices"], p["n_prices"]
    return f'''<link rel="stylesheet" href="/css/fournisseurs.css?v={ver("css/fournisseurs.css")}">
<link rel="stylesheet" href="/css/ux.css?v={ver("css/ux.css")}">
<div class="sp ap" id="ap-app" data-lang="{L("fr", "en")}">
<section class="sp-hero ap-hero">
  <p class="sp-kicker">{L("Pour les fournisseurs", "For suppliers")}</p>
  <h1>{L("Ajoutez vos prix à CoupeFab", "Add your prices to CoupeFab")}</h1>
  <p class="sp-lede">{L("Plus il y a de fournisseurs qui publient leurs prix, plus l’outil est utile pour les ateliers qui achètent. L’envoi est gratuit, sans engagement, et rien n’est mis en ligne avant une vérification manuelle.",
                       "The more suppliers post their prices, the more useful the tool is for shops that buy. Submitting is free, with no commitment, and nothing goes live before a manual review.")}</p>
  <ul class="ap-proof" aria-label="{L("Données actuelles", "Current figures")}">
    <li><b>{fmt(n_pub, "fr" if fr else "en")}</b><span>{L("fournisseurs avec des prix", "suppliers with prices")}</span></li>
    <li><b>{fmt(n_prices, "fr" if fr else "en")}</b><span>{L("prix suivis (tôles et outillage)", "prices tracked (sheet and tooling)")}</span></li>
  </ul>
</section>
<div class="ap-grid">
  <div class="ap-copy">
    <ul class="sp-perks">
      <li>{L("Badge « Prix disponibles » sur votre fiche et dans les comparateurs", "“Prices available” badge on your listing and in the price tools")}</li>
      <li>{L("Lien direct vers votre site, sans paramètre d’affiliation", "A direct link to your website, with no affiliate parameters")}</li>
      <li>{L("Vous pouvez retirer vos prix en tout temps; nous vous écrivons avant publication", "You can withdraw your prices at any time; we’ll email you before publication")}</li>
    </ul>
    <p class="sp-note">{L("Envoyez un lien vers vos prix en ligne, un fichier (PDF, CSV ou Excel), ou les deux. Après vérification, ils entrent dans les comparateurs de tôles et d’outillage.",
                          "Send a link to your online prices, a file (PDF, CSV or Excel), or both. After review, they join the sheet and tooling price tools.")}</p>
    <p class="sp-brochure"><a class="btn-ghost" href="{L("/fournisseurs/envoyer-brochure/", "/en/suppliers/send-brochure/")}">{L("Envoyer une brochure ou une liste de prix (10 Mo)", "Send a brochure or price list (10 MB)")} →</a></p>
  </div>
  {submit_form(fr)}
</div>
<p class="sp-repeat"><a href="{L(PATH_FR, PATH_EN)}">{L("Retour au répertoire des fournisseurs", "Back to the supplier directory")} →</a></p>
</div>'''


def render():
    return directory_body(True), directory_body(False)


def page_entries():
    fr, en = render()
    add_fr, add_en = landing_body(True), landing_body(False)
    return [
        (PATH_FR, PATH_EN, "fr", "Fournisseurs de métal au Québec et au Canada — répertoire — CoupeFab",
         "Répertoire des fournisseurs d’acier, d’aluminium, d’inox et de tubes au Québec et au Canada : villes, catégories, prix disponibles. Ajoutez vos prix.",
         fr, False, False),
        (PATH_EN, PATH_FR, "en", "Metal suppliers in Quebec and Canada — directory — CoupeFab",
         "Directory of steel, aluminum, stainless and tube suppliers in Quebec and across Canada: cities, categories, prices available. Add your prices.",
         en, False, False),
        (ADD_FR, ADD_EN, "fr", "Ajoutez vos prix — fournisseurs — CoupeFab",
         "Publiez gratuitement vos prix de métaux ou d’outillage sur CoupeFab. Plus il y a de listes, plus c’est utile pour les acheteurs. Vérification manuelle, sans affiliation.",
         add_fr, False, False),
        (ADD_EN, ADD_FR, "en", "Add your prices — suppliers — CoupeFab",
         "Publish your metal or tooling prices on CoupeFab for free. The more lists we have, the more useful it is for buyers. Manual review, no affiliates.",
         add_en, False, False),
    ]

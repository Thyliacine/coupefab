"""Brochure / price-list upload page for suppliers.

/fournisseurs/envoyer-brochure/ (FR) and /en/suppliers/send-brochure/ (EN).
js/brochure.js asks /api/supplier-submit (action "brochure-token") for a one-file private
Vercel Blob upload token, PUTs the file (PDF, JPG, PNG, XLSX, CSV, DOCX, 10 MB max) straight
to the private store, then confirms (action "brochure"): the file lands in the admin Inbox as
type "brochure", downloadable by the admin only. Class names use the "bro-" prefix
(never "ad-": ad blockers hide those).
"""
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PATH_FR, PATH_EN = "/fournisseurs/envoyer-brochure/", "/en/suppliers/send-brochure/"
ACCEPT = (".pdf,.jpg,.jpeg,.png,.xlsx,.csv,.docx,application/pdf,image/jpeg,image/png,text/csv,"
          "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,"
          "application/vnd.openxmlformats-officedocument.wordprocessingml.document")


def ver(rel):
    return hashlib.sha1((ROOT / rel).read_bytes()).hexdigest()[:8]


def body(fr):
    L = (lambda a, b: a if fr else b)
    dir_url = L("/fournisseurs/", "/en/suppliers/")
    return f'''<link rel="stylesheet" href="/css/brochure.css?v={ver("css/brochure.css")}">
<div class="bro" id="bro-app" data-lang="{L("fr", "en")}">
<nav class="bro-crumbs" aria-label="{L("Fil d’Ariane", "Breadcrumb")}"><a href="{dir_url}">{L("Fournisseurs", "Suppliers")}</a> <span aria-hidden="true">›</span> {L("Envoyer une brochure", "Send a brochure")}</nav>
<section class="bro-wrap" aria-labelledby="bro-h">
  <div class="bro-intro">
    <p class="bro-kicker">{L("Pour les fournisseurs", "For suppliers")}</p>
    <h1 id="bro-h">{L("Envoyez-nous votre brochure ou votre liste de prix", "Send us your brochure or price list")}</h1>
    <p class="bro-lede">{L("Un fichier suffit : catalogue, brochure, liste de prix ou fiche de produits. Nous l’utilisons pour compléter votre fiche dans le répertoire et, après vérification, ajouter vos prix au comparateur. L’inscription est gratuite.",
                          "One file is enough: catalogue, brochure, price list or product sheet. We use it to complete your directory listing and, once reviewed, add your prices to the price tool. Listing is free.")}</p>
    <ul class="bro-perks">
      <li>{L("Fiche gratuite dans le répertoire des fournisseurs du Québec et du Canada", "Free listing in the Quebec and Canada supplier directory")}</li>
      <li>{L("Les acheteurs du Québec comparent les prix et vous trouvent plus vite", "Quebec buyers compare prices and find you faster")}</li>
      <li>{L("Badge « Prix vérifiés » et lien direct vers votre site", "“Verified prices” badge and a direct link to your website")}</li>
      <li>{L("Rien n’est publié sans vérification; le fichier reste privé (seul CoupeFab y a accès)", "Nothing goes live unreviewed; the file stays private (only CoupeFab can open it)")}</li>
    </ul>
    <p class="bro-alt">{L("Vos prix sont déjà en ligne?", "Prices already online?")} <a href="{dir_url}#ajouter">{L("Ajoutez simplement le lien", "Just add the link")} →</a></p>
  </div>
  <form class="bro-form" id="bro-form" novalidate>
    <div class="bro-row">
      <label>{L("Entreprise", "Company")} <input type="text" name="company" required maxlength="200" autocomplete="organization"></label>
      <label>{L("Personne-ressource", "Contact name")} <input type="text" name="contact" required maxlength="200" autocomplete="name"></label>
    </div>
    <div class="bro-row">
      <label>{L("Courriel", "Email")} <input type="email" name="email" required maxlength="200" autocomplete="email"></label>
      <label>{L("Téléphone (facultatif)", "Phone (optional)")} <input type="tel" name="phone" maxlength="60" autocomplete="tel" inputmode="tel"></label>
    </div>
    <label class="bro-file">{L("Fichier : PDF, JPG, PNG, XLSX, CSV ou DOCX, 10 Mo max", "File: PDF, JPG, PNG, XLSX, CSV or DOCX, 10 MB max")}
      <input type="file" name="file" required accept="{ACCEPT}">
      <span class="bro-file-info" aria-live="polite"></span></label>
    <label>{L("Message (facultatif)", "Message (optional)")} <textarea name="message" maxlength="3000" rows="4" placeholder="{L("Ex. : régions desservies, quantités minimales, date de la liste", "E.g. regions served, minimum quantities, price-list date")}"></textarea></label>
    <label class="bro-hp" aria-hidden="true">Website <input type="text" name="website" tabindex="-1" autocomplete="off"></label>
    <label class="bro-consent"><input type="checkbox" name="consent" required> <span>{L("Je représente cette entreprise et j’autorise CoupeFab à utiliser ce document pour sa fiche et le comparateur de prix, après vérification. CoupeFab peut m’écrire au sujet de cet envoi.",
                                                                                         "I represent this company and allow CoupeFab to use this document for its listing and the price tool, after review. CoupeFab may email me about this upload.")}</span></label>
    <progress class="bro-progress" max="100" value="0" hidden></progress>
    <button class="btn" type="submit">{L("Envoyer le fichier", "Send the file")}</button>
    <p class="bro-status" role="status" aria-live="polite"></p>
    <p class="bro-fine">{L("Problème d’envoi? Écrivez à", "Trouble uploading? Email")} <a href="mailto:info@coupefab.ca">info@coupefab.ca</a>.</p>
  </form>
</section>
</div>
<script src="/js/brochure.js?v={ver("js/brochure.js")}" defer></script>'''


def page_entries():
    return [
        (PATH_FR, PATH_EN, "fr", "Envoyer une brochure ou une liste de prix — fournisseurs — CoupeFab",
         "Fournisseurs de métal : envoyez votre brochure, catalogue ou liste de prix (PDF, Excel, CSV, image). Fiche gratuite; les acheteurs du Québec comparent les prix sur CoupeFab.",
         body(True), False, False),
        (PATH_EN, PATH_FR, "en", "Send a brochure or price list — suppliers — CoupeFab",
         "Metal suppliers: send your brochure, catalogue or price list (PDF, Excel, CSV, image). Free listing; Quebec buyers compare prices on CoupeFab.",
         body(False), False, False),
    ]

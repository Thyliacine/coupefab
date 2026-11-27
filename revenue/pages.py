"""/annoncer/ (/en/advertise/) and /soumission/ (/en/quote/) page bodies."""
from __future__ import annotations

from . import P, css, esc, flags, hidden_paths, ver
from .routing import PROCESSES, REGIONS


def _preview(path: str, fr: bool) -> str:
    if path not in hidden_paths():
        return ""
    return (f'<p class="rv-preview" role="note"><strong>{"Aperçu interne" if fr else "Internal preview"}</strong> — '
            f'{"page non publiée (interrupteur désactivé dans config/monetization.json). Elle n’est ni indexée ni liée." if fr else "not published (switch off in config/monetization.json). Not indexed, not linked."}</p>')


def advertise(lang: str) -> str:
    fr = lang == "fr"
    L = (lambda a, b: a if fr else b)
    path = P["advertise"][0 if fr else 1]
    budgets = [
        ("", L("Je prefere ne pas le dire", "I would rather not say")),
        ("lt100", L("Moins de 100 $ CA", "Under CAD 100")),
        ("100-500", L("100 a 500 $ CA", "CAD 100-500")),
        ("500-1000", L("500 a 1 000 $ CA", "CAD 500-1,000")),
        ("1000+", L("Plus de 1 000 $ CA", "Over CAD 1,000")),
        ("discuss", L("A discuter", "Let us discuss")),
    ]
    # Fix accents after we know the file writes cleanly
    budgets = [
        ("", L("Je préfère ne pas le dire", "I'd rather not say")),
        ("lt100", L("Moins de 100 $ CA", "Under CAD 100")),
        ("100-500", L("100 à 500 $ CA", "CAD 100–500")),
        ("500-1000", L("500 à 1 000 $ CA", "CAD 500–1,000")),
        ("1000+", L("Plus de 1 000 $ CA", "Over CAD 1,000")),
        ("discuss", L("À discuter", "Let's discuss")),
    ]
    opts = "".join('<option value="%s">%s</option>' % (esc(k), esc(lab)) for k, lab in budgets)
    ph = L("Ex. une gamme de toles, un service d'usinage, une machine d'occasion…",
           "e.g. a sheet range, a machining service, a used machine…")
    lede_fr = ("Vous voulez faire connaître votre entreprise aux ateliers qui utilisent CoupeFab? "
               "Décrivez ce que vous souhaitez promouvoir. Nous vous répondons pour en discuter. "
               "Cette page n'affiche aucun tarif : les emplacements seront proposés lorsqu'une demande arrive.")
    lede_en = ("Want to introduce your company to the shops that use CoupeFab? Tell us what you'd like to promote. "
               "We'll write back to talk it over. This page shows no rates: placements are offered when a request comes in.")
    note = L("La fiche dans le répertoire et l'envoi de vos prix restent gratuits. Voir aussi la",
             "A directory listing and sending us your prices stay free. See also the")
    return (
        css()
        + '<link rel="stylesheet" href="/css/ux.css?v=%s">' % ver("css/ux.css")
        + '<div class="rv-page cf-request-page" id="cf-request">'
        + '<section class="rv-hero">'
        + _preview(path, fr)
        + '<p class="kicker">' + L("Annoncer", "Advertise") + "</p>"
        + "<h1>" + L("Annoncer sur CoupeFab", "Advertise on CoupeFab") + "</h1>"
        + '<p class="lede">' + L(lede_fr, lede_en) + "</p>"
        + "</section>"
        + '<form class="rv-form sp-form" id="cf-request-form" data-lang="' + lang + '" novalidate>'
        + "<label>" + L("Entreprise", "Company") + ' <input type="text" name="company" required maxlength="200" autocomplete="organization"></label>'
        + "<label>" + L("Personne-ressource", "Contact name") + ' <input type="text" name="contact" required maxlength="200" autocomplete="name"></label>'
        + "<label>" + L("Courriel", "Email") + ' <input type="email" name="email" required maxlength="200" autocomplete="email"></label>'
        + '<label class="rv-wide">' + L("Ce que vous souhaitez promouvoir", "What you want to promote")
        + ' <textarea name="promote" rows="3" maxlength="2000" required placeholder="' + esc(ph) + '"></textarea></label>'
        + "<label>" + L("Ordre de grandeur du budget (facultatif)", "Budget range (optional)")
        + ' <select name="budget">' + opts + "</select></label>"
        + '<label class="rv-wide">' + L("Message (facultatif)", "Message (optional)")
        + ' <textarea name="message" rows="3" maxlength="4000"></textarea></label>'
        + '<label class="rv-hp sp-hp" aria-hidden="true">Website <input type="text" name="website" tabindex="-1" autocomplete="off"></label>'
        + '<button class="btn btn-lg" type="submit">' + L("Envoyer la demande", "Send the request") + "</button>"
        + '<p class="rv-status cf-request-status" role="status" aria-live="polite"></p>'
        + "</form>"
        + '<p class="rv-note">' + note + ' <a href="' + P["disc"][0 if fr else 1] + '">'
        + L("page de divulgation", "disclosure page") + "</a>.</p>"
        + "</div>"
        + '<script src="/js/placement-request.js?v=' + ver("js/placement-request.js") + '" defer></script>'
    )


def quote(lang: str) -> str:
    fr = lang == "fr"
    L = (lambda a, b: a if fr else b)
    path = P["quote"][0 if fr else 1]
    proc = "".join(f'<option value="{k}">{esc(v[0] if fr else v[1])}</option>' for k, v in PROCESSES.items())
    reg = "".join(f'<option value="{k}">{esc(v[0] if fr else v[1])}</option>' for k, v in REGIONS.items())
    mats = [("acier", "Acier", "Steel"), ("inox", "Inox", "Stainless"), ("aluminium", "Aluminium", "Aluminum"),
            ("cuivre-laiton", "Cuivre, laiton, bronze", "Copper, brass, bronze"), ("plastique-bois", "Plastique, bois ou composite", "Plastic, wood or composite"),
            ("autre", "Autre / je ne sais pas", "Other / not sure")]
    mat = "".join(f'<option value="{k}">{esc(a if fr else b)}</option>' for k, a, b in mats)
    return f'''{css()}<div class="rv-page" id="rv-quote-app" data-lang="{lang}">
<section class="rv-hero">
  {_preview(path, fr)}
  <p class="kicker">{L("Découpe, pliage, usinage", "Cutting, bending, machining")}</p>
  <h1>{L("Demander une soumission", "Request a quote")}</h1>
  <p class="lede">{L("Décrivez votre pièce une seule fois. CoupeFab la lit et la transmet à des ateliers du Québec qui font ce procédé dans votre région. Gratuit pour vous, sans engagement.",
                     "Describe your part once. CoupeFab reads it and passes it to Quebec shops that do that process in your region. Free for you, no commitment.")}</p>
</section>
<form class="rv-form" id="rv-quote" novalidate>
  <fieldset><legend>{L("La job", "The job")}</legend>
    <label>{L("Procédé", "Process")} <select name="process" required><option value="">{L("Choisir…", "Choose…")}</option>{proc}</select></label>
    <label>{L("Matériau", "Material")} <select name="material" required><option value="">{L("Choisir…", "Choose…")}</option>{mat}</select></label>
    <label>{L("Épaisseur", "Thickness")} <input type="text" name="thickness" maxlength="60" placeholder="{L("ex. 1/4 po, 14 ga, 6 mm", "e.g. 1/4 in, 14 ga, 6 mm")}"></label>
    <label>{L("Quantité", "Quantity")} <input type="number" name="qty" min="1" max="1000000" step="1" inputmode="numeric" required></label>
    <label class="rv-wide">{L("Lien vers vos dessins (DXF, STEP, PDF) — Google Drive, Dropbox, WeTransfer…", "Link to your drawings (DXF, STEP, PDF) — Google Drive, Dropbox, WeTransfer…")} <input type="url" name="file_url" maxlength="500" placeholder="https://" inputmode="url"></label>
    <label class="rv-wide">{L("Ou décrivez la pièce (dimensions, finition, tolérances)", "Or describe the part (dimensions, finish, tolerances)")} <textarea name="description" rows="4" maxlength="3000"></textarea></label>
    <label>{L("Région de livraison ou de cueillette", "Delivery or pickup region")} <select name="region" required><option value="">{L("Choisir…", "Choose…")}</option>{reg}</select></label>
    <label>{L("Date souhaitée", "Needed by")} <input type="date" name="deadline"></label>
  </fieldset>
  <fieldset><legend>{L("Vos coordonnées", "Your contact details")}</legend>
    <label>{L("Nom", "Name")} <input type="text" name="name" required maxlength="120" autocomplete="name"></label>
    <label>{L("Entreprise (facultatif)", "Company (optional)")} <input type="text" name="company" maxlength="200" autocomplete="organization"></label>
    <label>{L("Courriel", "Email")} <input type="email" name="email" required maxlength="200" autocomplete="email"></label>
    <label>{L("Téléphone (facultatif)", "Phone (optional)")} <input type="tel" name="phone" maxlength="40" autocomplete="tel"></label>
  </fieldset>
  <label class="rv-hp" aria-hidden="true">Website <input type="text" name="website" tabindex="-1" autocomplete="off"></label>
  <input type="hidden" name="t0" value="">
  <label class="consent"><input type="checkbox" name="consent" required> <span>{L("J’accepte que CoupeFab conserve ces renseignements et les transmette à quelques ateliers choisis selon le procédé et la région, seulement pour préparer une soumission. Conservation : 12 mois au plus. Responsable : Michaël Brassard, info@coupefab.ca. Voir la",
     "I agree that CoupeFab keeps this information and shares it with a few shops picked by process and region, only to prepare a quote. Kept 12 months at most. Privacy officer: Michaël Brassard, info@coupefab.ca. See the")} <a href="{L("/confidentialite/", "/en/privacy/")}">{L("politique de confidentialité (Loi 25)", "privacy policy (Law 25)")}</a>.</span></label>
  <button class="btn btn-lg" type="submit">{L("Envoyer la demande", "Send the request")}</button>
  <p class="rv-status" role="status" aria-live="polite"></p>
</form>
<p class="rv-note">{L("Ajoutez un lien ou une description : au moins l’un des deux. Les fichiers restent chez vous (lien de partage); CoupeFab ne publie jamais une demande.", "Add a link or a description: at least one of the two. Files stay with you (share link); CoupeFab never publishes a request.")}</p>
</div>
<script src="/js/soumission.js?v={ver("js/soumission.js")}" defer></script>'''


def entries() -> list[tuple]:
    a_fr, a_en = P["advertise"]
    q_fr, q_en = P["quote"]
    return [
        (a_fr, a_en, "fr", "Annoncer sur CoupeFab — demande d’annonce — CoupeFab",
         "Demande pour annoncer sur CoupeFab. Aucun tarif affiché; nous vous répondons pour en discuter.", advertise("fr"), False, False),
        (a_en, a_fr, "en", "Advertise on CoupeFab — ad request — CoupeFab",
         "Request to advertise on CoupeFab. No rates listed; we will write back to talk it over.", advertise("en"), False, False),
        (q_fr, q_en, "fr", "Demander une soumission : découpe, pliage, usinage au Québec — CoupeFab",
         "Décrivez votre pièce une fois; CoupeFab la transmet à des ateliers du Québec qui font ce procédé dans votre région.", quote("fr"), False, False),
        (q_en, q_fr, "en", "Request a quote: cutting, bending, machining in Quebec — CoupeFab",
         "Describe your part once; CoupeFab passes it to Quebec shops that do that process in your region.", quote("en"), False, False),
    ]

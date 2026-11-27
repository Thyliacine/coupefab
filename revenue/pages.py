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
    tbd = f'<span class="rv-tbd">{L("Tarif à déterminer (TBD) — à approuver par Michaël", "Price to be determined (TBD) — pending Michaël’s approval")}</span>'
    opts = [
        (L("Fournisseur en vedette", "Featured supplier"),
         L("Votre logo, deux phrases et un lien en haut du répertoire des fournisseurs et des pages de prix, pièces ou outillage de votre choix. Toujours marqué « Commandité ». Actif tant que l’abonnement est payé; il s’arrête de lui-même à la fin de la période.",
           "Your logo, two sentences and a link at the top of the supplier directory and of the price, parts or tooling pages you pick. Always labelled “Sponsored”. Live while the subscription is paid; it stops on its own at the end of the period."),
         [L("Répertoire gratuit inchangé : votre fiche normale reste listée comme les autres", "The free directory doesn’t change: your normal listing stays listed like everyone else’s"),
          L("Aucun effet sur les prix ni sur l’ordre du comparateur", "No effect on prices or on the price-tool ranking"),
          L("Au mois, sans engagement (proposé)", "Monthly, no commitment (proposed)")]),
        (L("Commandite de l’infolettre des prix", "Price-digest sponsorship"),
         L("Un seul commanditaire par numéro : nom, logo, deux lignes de texte et un lien, marqués « Commandité », dans l’infolettre envoyée aux ateliers abonnés.",
           "One sponsor per issue: name, logo, two lines of copy and a link, labelled “Sponsored”, in the newsletter sent to subscribed shops."),
         [L("Réservé aux fournisseurs de métal, d’outillage et aux marchands de machines", "For metal and tooling suppliers and machine dealers"),
          L("Le commanditaire ne voit ni ne modifie le reste du contenu", "The sponsor neither sees nor edits the rest of the content")]),
        (L("Demandes de soumission (plus tard)", "Quote requests (later)"),
         L("Les ateliers recevront des demandes de soumission (procédé, matériau, quantité, région) envoyées par les visiteurs, avec leur consentement. Frais par demande reçue, seulement si la demande correspond à votre procédé et à votre région.",
           "Shops will receive quote requests (process, material, quantity, region) sent by visitors, with their consent. A fee per request received, only when it matches your process and region."),
         [L("Pas encore offert : on attend d’avoir assez de trafic", "Not offered yet: we’re waiting for enough traffic")]),
    ]
    cards = "".join(
        f'<li class="rv-opt"><h2>{esc(t)}</h2><p>{esc(d)}</p><ul>{"".join(f"<li>{esc(x)}</li>" for x in pts)}</ul><p class="rv-price">{tbd}</p></li>'
        for t, d, pts in opts)
    return f'''{css()}<div class="rv-page">
<section class="rv-hero">
  {_preview(path, fr)}
  <p class="kicker">{L("Pour les fournisseurs et marchands", "For suppliers and dealers")}</p>
  <h1>{L("Annoncer sur CoupeFab", "Advertise on CoupeFab")}</h1>
  <p class="lede">{L("La fiche dans le répertoire et l’envoi de vos prix restent gratuits pour tous. Pour plus de visibilité, voici les options payantes. Elles sont toujours clairement identifiées comme commanditées.",
                     "A directory listing and sending us your prices stay free for everyone. For more visibility, here are the paid options. They are always clearly labelled as sponsored.")}</p>
</section>
<ul class="rv-opts">{cards}</ul>
<section class="rv-rules">
  <h2>{L("Nos règles", "Our rules")}</h2>
  <ul>
    <li>{L("Tout espace payé porte la mention « Commandité » et un lien rel=\"sponsored\".", "Every paid spot says “Sponsored” and its link carries rel=\"sponsored\".")}</li>
    <li>{L("Payer ne change jamais un prix, un classement ou le contenu d’un guide.", "Paying never changes a price, a ranking or a guide’s content.")}</li>
    <li>{L("On peut refuser une annonce qui ne sert pas les ateliers.", "We may turn down an ad that doesn’t help shops.")}</li>
  </ul>
  <p>{L("Intéressé? Écrivez à", "Interested? Write to")} <a href="mailto:info@coupefab.ca?subject={L("Annoncer%20sur%20CoupeFab", "Advertise%20on%20CoupeFab")}">info@coupefab.ca</a>. {L("Voir aussi la", "See also the")} <a href="{P["disc"][0 if fr else 1]}">{L("page de divulgation", "disclosure page")}</a>.</p>
</section>
</div>'''


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
        (a_fr, a_en, "fr", "Annoncer sur CoupeFab — fournisseurs en vedette, commandite — CoupeFab",
         "Options payantes pour les fournisseurs : fiche en vedette, commandite de l’infolettre. Toujours identifiées comme commanditées.", advertise("fr"), False, False),
        (a_en, a_fr, "en", "Advertise on CoupeFab — featured suppliers, sponsorship — CoupeFab",
         "Paid options for suppliers: featured listing, newsletter sponsorship. Always labelled as sponsored.", advertise("en"), False, False),
        (q_fr, q_en, "fr", "Demander une soumission : découpe, pliage, usinage au Québec — CoupeFab",
         "Décrivez votre pièce une fois; CoupeFab la transmet à des ateliers du Québec qui font ce procédé dans votre région.", quote("fr"), False, False),
        (q_en, q_fr, "en", "Request a quote: cutting, bending, machining in Quebec — CoupeFab",
         "Describe your part once; CoupeFab passes it to Quebec shops that do that process in your region.", quote("en"), False, False),
    ]

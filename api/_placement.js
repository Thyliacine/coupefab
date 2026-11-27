/**
 * Placement request form → admin inbox (type "placement"). No prices are quoted.
 * Routed through api/supplier-submit.js (body.action === "placement") so this
 * is not a separate Vercel Function (Hobby limit is 12).
 */
const { saveForm } = require("./_inbox");
const sec = require("./_security");

function json(res, status, body) {
  res.statusCode = status;
  res.setHeader("content-type", "application/json; charset=utf-8");
  res.setHeader("cache-control", "no-store");
  res.end(JSON.stringify(body));
}

async function handle(b, req, res) {
  if (b && b.website) return json(res, 200, { ok: true });
  const company = sec.oneLine(b && b.company, 200);
  const contact = sec.oneLine(b && b.contact, 200);
  const email = sec.oneLine(b && b.email, 254).toLowerCase();
  const promote = sec.clean(b && b.promote, 2000);
  const budget = sec.oneLine(b && b.budget, 80);
  const message = sec.clean(b && b.message, 4000);
  const lang = b && b.lang === "en" ? "en" : "fr";
  if (!company || !contact || !sec.validEmail(email) || !promote) {
    return json(res, 400, { ok: false, error: "Champs requis manquants." });
  }
  if (sec.limited(req, "placement", 5, 3600_000, 100)) {
    res.setHeader("retry-after", "3600");
    return json(res, 429, { ok: false, error: lang === "en" ? "Too many requests. Try again in an hour." : "Trop de demandes. Réessayez dans une heure." });
  }
  const text = [
    "Demande de visibilité sur CoupeFab",
    "Entreprise : " + company,
    "Contact : " + contact,
    "Courriel : " + email,
    "À promouvoir : " + promote,
    budget ? ("Budget (ordre de grandeur, facultatif) : " + budget) : "Budget : non précisé",
    message ? ("Message : " + message) : "",
  ].filter(Boolean).join("\n");
  try {
    const saved = await saveForm({
      type: "placement",
      subject: "Visibilité : " + company,
      from: email,
      fromName: contact,
      to: "info@coupefab.ca",
      text,
      fields: { company, contact, email, promote, budget, message, lang },
    });
    return json(res, 200, { ok: true, id: saved && saved.id, persisted: true });
  } catch (e) {
    console.error("placement-request: storage failed");
    return json(res, 503, { ok: false, error: "Le formulaire n’est pas encore relié à notre boîte de réception. Réessayez bientôt." });
  }
}

module.exports = { handle };

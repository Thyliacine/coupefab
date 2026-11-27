/**
 * Placement request form → admin inbox (type "placement"). No prices are quoted.
 * Routed through api/supplier-submit.js (body.action === "placement") so this
 * is not a separate Vercel Function (Hobby limit is 12).
 */
const { saveForm } = require("./_inbox");

function json(res, status, body) {
  res.statusCode = status;
  res.setHeader("content-type", "application/json; charset=utf-8");
  res.setHeader("cache-control", "no-store");
  res.end(JSON.stringify(body));
}

async function handle(b, req, res) {
  if (b && b.website) return json(res, 200, { ok: true });
  const company = String((b && b.company) || "").trim().slice(0, 200);
  const contact = String((b && b.contact) || "").trim().slice(0, 200);
  const email = String((b && b.email) || "").trim().toLowerCase().slice(0, 200);
  const promote = String((b && b.promote) || "").trim().slice(0, 2000);
  const budget = String((b && b.budget) || "").trim().slice(0, 80);
  const message = String((b && b.message) || "").trim().slice(0, 4000);
  const lang = b && b.lang === "en" ? "en" : "fr";
  if (!company || !contact || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || !promote) {
    return json(res, 400, { ok: false, error: "Champs requis manquants." });
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
    console.error("placement-request", e);
    return json(res, 503, { ok: false, error: "Le formulaire n’est pas encore relié à notre boîte de réception. Réessayez bientôt." });
  }
}

module.exports = { handle };

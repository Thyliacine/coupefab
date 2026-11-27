/**
 * CoupeFab newsletter, contact and unsubscribe intake.
 * Each signup / message / unsubscribe request is written to the private CoupeFab admin
 * Inbox (Vercel Blob, private store). Optional: NEWSLETTER_WEBHOOK_URL also receives the JSON.
 * Nothing is written to /tmp or to the logs (no personal information in logs).
 *
 * Hardening: same-site Origin check (no CORS), body cap, strict email check, length caps,
 * control-character stripping, honeypot "website", per-IP + per-instance rate limits,
 * generic error messages. CASL: newsletter consent must be explicitly true.
 * Unsubscribe (type "unsubscribe"): always answers the same thing, whether or not the
 * address is on the list, so the form cannot be used to test who is subscribed.
 */
const sec = require("./_security");

function json(res, status, body) {
  res.statusCode = status;
  res.setHeader("content-type", "application/json; charset=utf-8");
  res.setHeader("cache-control", "no-store");
  res.end(JSON.stringify(body));
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    let raw = "";
    req.on("data", (c) => {
      raw += c;
      if (raw.length > 20_000) { reject(new Error("too large")); req.destroy(); }
    });
    req.on("end", () => {
      try {
        const v = raw ? JSON.parse(raw) : {};
        resolve(v && typeof v === "object" && !Array.isArray(v) ? v : {});
      } catch { reject(new Error("invalid json")); }
    });
    req.on("error", reject);
  });
}

async function forwardWebhook(entry) {
  const url = process.env.NEWSLETTER_WEBHOOK_URL;
  if (!url || !/^https:\/\//i.test(url)) return false;
  const res = await fetch(url, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(entry),
  });
  if (!res.ok) throw new Error("webhook " + res.status);
  return true;
}

const SUBJECTS = {
  contact: "Message depuis le site",
  newsletter: "Inscription à l’infolettre",
  unsubscribe: "Désabonnement de l’infolettre",
};

async function forwardInbox(entry) {
  const { saveForm } = require("./_inbox");
  await saveForm({
    type: entry.type === "contact" ? "contact" : "newsletter",
    subject: SUBJECTS[entry.type],
    from: entry.email,
    fromName: entry.name || "",
    to: "info@coupefab.ca",
    text: entry.message || (entry.type === "unsubscribe"
      ? "Retirer cette adresse de la liste d’envoi (demande de désabonnement)."
      : entry.type === "newsletter" ? "Inscription à l’infolettre" : ""),
    fields: entry,
  });
  return true;
}

module.exports = async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("allow", "POST");
    return json(res, 405, { ok: false, error: "method not allowed" });
  }
  if (!sec.originOk(req)) return json(res, 403, { ok: false, error: "forbidden" });

  let body;
  try { body = await readBody(req); } catch { return json(res, 400, { ok: false, error: "invalid body" }); }

  if (body.website) return json(res, 200, { ok: true });

  const type = ["contact", "unsubscribe"].includes(body.type) ? body.type : "newsletter";
  const lang = body.lang === "en" ? "en" : "fr";
  const email = sec.oneLine(body.email, 254).toLowerCase();
  const name = type === "unsubscribe" ? "" : sec.oneLine(body.name, 120);
  const message = type === "contact" ? sec.clean(body.message, 4000) : "";
  const consent = type === "newsletter" ? body.consent === true : false;

  if (!sec.validEmail(email)) return json(res, 400, { ok: false, error: "invalid email" });
  if (type === "newsletter" && !consent) return json(res, 400, { ok: false, error: "consent required" });
  if (type === "contact" && !message) return json(res, 400, { ok: false, error: "message required" });

  if (sec.limited(req, "subscribe", 6, 3600_000, 200)) {
    res.setHeader("retry-after", "3600");
    return json(res, 429, { ok: false, error: lang === "en" ? "Too many requests. Please try again later." : "Trop de demandes. Réessayez plus tard." });
  }

  const entry = { type, email, name, message, lang, consent, submittedAt: new Date().toISOString() };
  if (type === "newsletter") entry.consent_text = "infolettre-casl-v1";

  let stored = false;
  let failures = 0;
  for (const fn of [forwardWebhook, forwardInbox]) {
    try { stored = (await fn(entry)) || stored; } catch { failures += 1; }
  }
  if (failures) console.error("subscribe: " + failures + " storage target(s) failed");

  if (!stored) {
    return json(res, 503, { ok: false, error: lang === "en"
      ? "The form isn’t connected to our inbox yet. Please try again soon."
      : "Le formulaire n’est pas encore relié à notre boîte de réception. Réessayez bientôt." });
  }
  return json(res, 200, { ok: true, persisted: true });
};

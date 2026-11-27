const auth = require("../_auth");
const inbox = require("../_inbox");
const sec = require("../_security");

function fromAddr() {
  return process.env.RESEND_FROM || "CoupeFab <info@coupefab.ca>";
}

module.exports = async (req, res) => {
  if (req.method !== "POST") return auth.json(res, 405, { ok: false, error: "POST only" });
  if (!auth.requireAdmin(req, res)) return;
  if (!process.env.RESEND_API_KEY) {
    return auth.json(res, 503, {
      ok: false,
      error: "L’envoi n’est pas encore configuré. Créez un compte Resend gratuit, ajoutez la clé RESEND_API_KEY, puis les enregistrements DNS (voir le rapport).",
    });
  }
  let body = {};
  try { body = JSON.parse(await auth.readBody(req, 200_000)) || {}; } catch { return auth.json(res, 400, { ok: false, error: "JSON invalide." }); }
  const id = String(body.id || "");
  const text = String(body.text || "").trim().slice(0, 50_000);
  if (!text) return auth.json(res, 400, { ok: false, error: "Le message est vide." });
  const msg = await inbox.getMessage(id);
  if (!msg) return auth.json(res, 404, { ok: false, error: "Introuvable." });
  const to = String(body.to || msg.from || "").trim();
  if (!sec.validEmail(to)) return auth.json(res, 400, { ok: false, error: "Destinataire invalide." });
  const subject = sec.oneLine(body.subject || (msg.subject && !/^re:/i.test(msg.subject) ? "Re: " + msg.subject : (msg.subject || "CoupeFab")), 200);
  const payload = {
    from: fromAddr(),
    to: [to],
    subject,
    text,
  };
  if (msg.messageId) {
    const hdr = (v) => sec.oneLine(v, 2000).replace(/[^\x21-\x7e ]/g, "");
    payload.headers = { "In-Reply-To": hdr(msg.messageId), References: hdr(msg.references || msg.messageId) };
  }
  const r = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { authorization: "Bearer " + process.env.RESEND_API_KEY, "content-type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await r.json().catch(() => ({}));
  if (!r.ok) {
    console.error("resend send failed", r.status);
    return auth.json(res, 502, { ok: false, error: (data.error && data.error.message) || "Échec de l’envoi Resend." });
  }
  const reply = {
    at: new Date().toISOString(),
    to,
    subject,
    text,
    provider: "resend",
    providerId: data.id || "",
  };
  const updated = await inbox.addReply(id, reply);
  return auth.json(res, 200, { ok: true, reply, message: updated });
};

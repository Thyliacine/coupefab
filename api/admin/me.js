const auth = require("../_auth");
const blob = require("../_blob");
module.exports = async (req, res) => {
  if (req.method !== "GET") return auth.json(res, 405, { ok: false, error: "GET only" });
  if (!auth.requireAdmin(req, res, { csrf: false })) return;
  return auth.json(res, 200, {
    ok: true,
    blob: blob.configured(),
    outbound: Boolean(process.env.RESEND_API_KEY),
    inbound: Boolean(process.env.RESEND_WEBHOOK_SECRET),
    from: process.env.RESEND_FROM || "CoupeFab <info@coupefab.ca>",
  });
};

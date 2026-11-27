const auth = require("../_auth");
const blob = require("../_blob");
const inbox = require("../_inbox");

module.exports = async (req, res) => {
  if (req.method !== "GET") return auth.json(res, 405, { ok: false, error: "GET only" });
  if (!auth.requireAdmin(req, res, { csrf: false })) return;
  const u = new URL(req.url, "https://coupefab.ca");
  const id = u.searchParams.get("id") || "";
  const name = u.searchParams.get("name") || "";
  const msg = await inbox.getMessage(id);
  if (!msg) return auth.json(res, 404, { ok: false, error: "Introuvable." });
  const att = (msg.attachments || []).find((a) => a.name === name);
  if (!att) return auth.json(res, 404, { ok: false, error: "Pièce jointe introuvable." });
  try {
    const { body, contentType } = await blob.getBuffer(att.url || att.pathname);
    res.statusCode = 200;
    // Always a download, never rendered inline on coupefab.ca (a hostile HTML/SVG
    // attachment must not run in the admin's origin).
    const safe = String(att.name || "fichier").replace(/[^\w.\- ]+/g, "_").slice(0, 120) || "fichier";
    const ct = String(att.contentType || contentType || "application/octet-stream");
    res.setHeader("content-type", /^(application\/pdf|image\/(png|jpeg|gif|webp)|text\/csv|application\/vnd\.[\w.+-]+|application\/(zip|msword|vnd\.ms-excel))$/i.test(ct) ? ct : "application/octet-stream");
    res.setHeader("content-disposition", "attachment; filename=\"" + safe + "\"");
    res.setHeader("x-content-type-options", "nosniff");
    res.setHeader("content-security-policy", "default-src 'none'; sandbox");
    res.setHeader("cache-control", "private, no-store");
    res.setHeader("x-robots-tag", "noindex");
    res.end(body);
  } catch (e) {
    console.error("attachment failed", e && e.message);
    return auth.json(res, 404, { ok: false, error: "Fichier introuvable." });
  }
};

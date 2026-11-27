/**
 * CoupeFab — "Ajoutez vos prix / Add your prices" intake for suppliers.
 * Submissions go to MANUAL REVIEW only: nothing here publishes anything.
 *
 * Durable storage, same mechanisms as api/subscribe.js (set at least one in Vercel → Settings → Environment Variables):
 * Durable storage: written to the CoupeFab admin Inbox (Vercel Blob), file included as an attachment.
 * Optional: SUPPLIER_WEBHOOK_URL (or NEWSLETTER_WEBHOOK_URL) also POSTs JSON.
 * Without Blob storage the function answers 503 so the supplier is told to retry instead of being silently dropped.
 * Honeypot field "website" drops bots. Body capped at ~3.2 MB (2 MB file + base64 overhead; Vercel limit is 4.5 MB).
 */
const fs = require("fs");
const path = require("path");

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const URL_RE = /^https?:\/\/[^\s]+$/i;
const MAX_BODY = 3_200_000;
const MAX_FILE = 2 * 1024 * 1024;
const OK_TYPES = /\.(pdf|csv|xls|xlsx)$/i;
const TMP_FILE = path.join("/tmp", "coupefab-supplier-submissions.json");

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
      if (raw.length > MAX_BODY) { reject(new Error("too large")); req.destroy(); }
    });
    req.on("end", () => { try { resolve(raw ? JSON.parse(raw) : {}); } catch { reject(new Error("invalid json")); } });
    req.on("error", reject);
  });
}

const msg = (lang, fr, en) => (lang === "en" ? en : fr);

async function toWebhook(entry) {
  const url = process.env.SUPPLIER_WEBHOOK_URL || process.env.NEWSLETTER_WEBHOOK_URL;
  if (!url) return false;
  const r = await fetch(url, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ type: "supplier_prices", ...entry }) });
  if (!r.ok) throw new Error("webhook " + r.status);
  return true;
}

async function toInbox(entry) {
  const { saveForm } = require("./_inbox");
  const files = entry.file && entry.file.data ? [{ name: entry.file.name, data: entry.file.data, type: entry.file.type }] : [];
  const fields = { ...entry };
  if (fields.file) fields.file = { name: entry.file.name, size: entry.file.size, type: entry.file.type };
  await saveForm({
    type: "supplier",
    subject: "Prix fournisseur à vérifier : " + (entry.company || ""),
    from: entry.email,
    fromName: entry.company || "",
    to: "info@coupefab.ca",
    text: [entry.company, entry.site, entry.price_url, entry.message].filter(Boolean).join("\n"),
    fields,
    files,
  });
  return true;
}

module.exports = async function handler(req, res) {
  if (req.method !== "POST") return json(res, 405, { ok: false, error: "method not allowed" });
  let b;
  try { b = await readBody(req); } catch (e) { return json(res, 413, { ok: false, error: "Fichier trop lourd / file too large (2 MB max)" }); }
  if (b.action === "brochure-token" || b.action === "brochure") return require("./_brochure").handle(b, req, res);
  if (b.action === "placement") return require("./_placement").handle(b, req, res);
  const lang = b.lang === "en" ? "en" : "fr";
  if (b.website) return json(res, 200, { ok: true });

  const company = String(b.company || "").trim().slice(0, 200);
  const email = String(b.email || "").trim().toLowerCase().slice(0, 200);
  const site = String(b.site || "").trim().slice(0, 300);
  const price_url = String(b.price_url || "").trim().slice(0, 500);
  const message = String(b.message || "").trim().slice(0, 2000);
  if (!company || !EMAIL_RE.test(email)) return json(res, 400, { ok: false, error: msg(lang, "Nom de l’entreprise et courriel valide requis.", "Company name and a valid email are required.") });
  if (b.consent !== true) return json(res, 400, { ok: false, error: msg(lang, "Autorisation requise.", "Authorization required.") });
  if ((site && !URL_RE.test(site)) || (price_url && !URL_RE.test(price_url))) return json(res, 400, { ok: false, error: msg(lang, "Les liens doivent commencer par https://", "Links must start with https://") });

  let file = null;
  if (b.file && b.file.data) {
    const name = String(b.file.name || "liste-de-prix").replace(/[^\w.\- ]+/g, "_").slice(0, 120);
    const size = Math.floor((String(b.file.data).length * 3) / 4);
    if (!OK_TYPES.test(name)) return json(res, 400, { ok: false, error: msg(lang, "Formats acceptés : PDF, CSV, XLS, XLSX.", "Accepted formats: PDF, CSV, XLS, XLSX.") });
    if (size > MAX_FILE) return json(res, 413, { ok: false, error: msg(lang, "Fichier trop lourd (2 Mo max).", "File too large (2 MB max).") });
    file = { name, type: String(b.file.type || "application/octet-stream").slice(0, 100), size, data: String(b.file.data) };
  }
  if (!price_url && !file) return json(res, 400, { ok: false, error: msg(lang, "Ajoutez un lien vers vos prix ou un fichier.", "Add a link to your prices or a file.") });

  const entry = { company, email, site, price_url, message, lang, consent: true, status: "pending_review", file, submittedAt: new Date().toISOString() };
  try {
    let list = [];
    try { list = JSON.parse(fs.readFileSync(TMP_FILE, "utf8")); } catch { list = []; }
    list.push({ ...entry, file: file ? { name: file.name, size: file.size } : null });
    fs.writeFileSync(TMP_FILE, JSON.stringify(list));
  } catch (e) { console.error("tmp log failed", e); }

  let stored = false;
  const errors = [];
  for (const fn of [toWebhook, toInbox]) {
    try { stored = (await fn(entry)) || stored; } catch (e) { errors.push(String(e)); }
  }
  if (errors.length) console.error("supplier-submit forward errors", errors);
  if (!stored) {
    return json(res, 503, { ok: false, error: msg(lang, "Le formulaire n’est pas encore relié à notre boîte de réception. Réessayez bientôt ou écrivez-nous depuis la page À propos.",
      "The form isn’t connected to our inbox yet. Please try again soon, or write to us from the About page.") });
  }
  return json(res, 200, { ok: true, status: "pending_review" });
};

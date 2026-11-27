/**
 * CoupeFab — "Ajoutez vos prix / Add your prices" intake for suppliers.
 * Submissions go to MANUAL REVIEW only: nothing here publishes anything.
 *
 * Durable storage, same mechanisms as api/subscribe.js (set at least one in Vercel → Settings → Environment Variables):
 *   SUPPLIER_WEBHOOK_URL (or NEWSLETTER_WEBHOOK_URL)  JSON POST incl. the file as base64 (e.g. Google Apps Script → Sheet + Drive)
 *   SUPPLIER_INBOX (or NEWSLETTER_INBOX)              FormSubmit relay to an inbox, file sent as an attachment
 * Without either, the function answers 503 so the supplier is told to retry instead of being silently dropped.
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
  const inbox = process.env.SUPPLIER_INBOX || process.env.NEWSLETTER_INBOX;
  if (!inbox) return false;
  const fd = new FormData();
  fd.append("_subject", `CoupeFab — prix fournisseur à vérifier : ${entry.company}`);
  fd.append("_template", "table");
  fd.append("_captcha", "false");
  for (const k of ["company", "email", "site", "price_url", "message", "lang", "submittedAt"]) fd.append(k, entry[k] || "");
  fd.append("review", "MANUAL REVIEW REQUIRED — do not publish before checking prices, source and date.");
  if (entry.file) fd.append("attachment", new Blob([Buffer.from(entry.file.data, "base64")], { type: entry.file.type }), entry.file.name);
  const r = await fetch("https://formsubmit.co/ajax/" + encodeURIComponent(inbox), { method: "POST", headers: { accept: "application/json" }, body: fd });
  if (!r.ok) throw new Error("formsubmit " + r.status);
  return true;
}

module.exports = async function handler(req, res) {
  if (req.method !== "POST") return json(res, 405, { ok: false, error: "method not allowed" });
  let b;
  try { b = await readBody(req); } catch (e) { return json(res, 413, { ok: false, error: "Fichier trop lourd / file too large (2 MB max)" }); }
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

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
const sec = require("./_security");

const URL_RE = /^https?:\/\/[^\s<>"']+$/i;
const MAX_BODY = 3_200_000;
const MAX_FILE = 2 * 1024 * 1024;
const OK_TYPES = /\.(pdf|csv|xls|xlsx)$/i;
// Content type is decided here from the extension, never taken from the browser.
const MIME = {
  pdf: "application/pdf",
  csv: "text/csv",
  xls: "application/vnd.ms-excel",
  xlsx: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
};
function sniff(ext, buf) {
  if (ext === "pdf") return buf.subarray(0, 4).toString("latin1") === "%PDF";
  if (ext === "xlsx") return buf[0] === 0x50 && buf[1] === 0x4b && buf[2] === 0x03 && buf[3] === 0x04;
  if (ext === "xls") return buf.subarray(0, 8).equals(Buffer.from([0xd0, 0xcf, 0x11, 0xe0, 0xa1, 0xb1, 0x1a, 0xe1]));
  if (ext === "csv") return !buf.subarray(0, 8192).includes(0);
  return false;
}

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
    req.on("end", () => {
      try { const v = raw ? JSON.parse(raw) : {}; resolve(v && typeof v === "object" && !Array.isArray(v) ? v : {}); } catch { reject(new Error("invalid json")); }
    });
    req.on("error", reject);
  });
}

const msg = (lang, fr, en) => (lang === "en" ? en : fr);

async function toWebhook(entry) {
  const url = process.env.SUPPLIER_WEBHOOK_URL || process.env.NEWSLETTER_WEBHOOK_URL;
  if (!url || !/^https:\/\//i.test(url)) return false;
  const { file, ...rest } = entry;  // never forward the file bytes to a third party
  const meta = file ? { name: file.name, size: file.size, type: file.type } : null;
  const r = await fetch(url, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ type: "supplier_prices", ...rest, file: meta }) });
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
  if (req.method !== "POST") { res.setHeader("allow", "POST"); return json(res, 405, { ok: false, error: "method not allowed" }); }
  if (!sec.originOk(req)) return json(res, 403, { ok: false, error: "forbidden" });
  let b;
  try { b = await readBody(req); } catch (e) { return json(res, 413, { ok: false, error: "Fichier trop lourd / file too large (2 MB max)" }); }
  if (b.action === "brochure-token" || b.action === "brochure") return require("./_brochure").handle(b, req, res);
  if (b.action === "placement") return require("./_placement").handle(b, req, res);
  const lang = b.lang === "en" ? "en" : "fr";
  if (b.website) return json(res, 200, { ok: true });

  const company = sec.oneLine(b.company, 200);
  const email = sec.oneLine(b.email, 254).toLowerCase();
  const site = sec.oneLine(b.site, 300);
  const price_url = sec.oneLine(b.price_url, 500);
  const message = sec.clean(b.message, 2000);
  if (!company || !sec.validEmail(email)) return json(res, 400, { ok: false, error: msg(lang, "Nom de l’entreprise et courriel valide requis.", "Company name and a valid email are required.") });
  if (b.consent !== true) return json(res, 400, { ok: false, error: msg(lang, "Autorisation requise.", "Authorization required.") });
  if ((site && !URL_RE.test(site)) || (price_url && !URL_RE.test(price_url))) return json(res, 400, { ok: false, error: msg(lang, "Les liens doivent commencer par https://", "Links must start with https://") });

  let file = null;
  if (b.file && b.file.data) {
    const name = String(b.file.name || "liste-de-prix").replace(/[^\w.\- ]+/g, "_").slice(0, 120);
    const size = Math.floor((String(b.file.data).length * 3) / 4);
    if (!OK_TYPES.test(name)) return json(res, 400, { ok: false, error: msg(lang, "Formats acceptés : PDF, CSV, XLS, XLSX.", "Accepted formats: PDF, CSV, XLS, XLSX.") });
    if (size > MAX_FILE) return json(res, 413, { ok: false, error: msg(lang, "Fichier trop lourd (2 Mo max).", "File too large (2 MB max).") });
    const ext = name.split(".").pop().toLowerCase();
    const data = String(b.file.data);
    if (!/^[A-Za-z0-9+/=\s]*$/.test(data) || !sniff(ext, Buffer.from(data.slice(0, 12000), "base64"))) {
      return json(res, 400, { ok: false, error: msg(lang, "Le contenu du fichier ne correspond pas à son extension.", "The file content doesn’t match its extension.") });
    }
    file = { name, type: MIME[ext], size, data };
  }
  if (!price_url && !file) return json(res, 400, { ok: false, error: msg(lang, "Ajoutez un lien vers vos prix ou un fichier.", "Add a link to your prices or a file.") });

  if (sec.limited(req, "supplier", 6, 3600_000, 120)) {
    res.setHeader("retry-after", "3600");
    return json(res, 429, { ok: false, error: msg(lang, "Trop d’envois. Réessayez dans une heure.", "Too many submissions. Try again in an hour.") });
  }

  const entry = { company, email, site, price_url, message, lang, consent: true, status: "pending_review", file, submittedAt: new Date().toISOString() };

  let stored = false;
  let failures = 0;
  for (const fn of [toWebhook, toInbox]) {
    try { stored = (await fn(entry)) || stored; } catch { failures += 1; }
  }
  if (failures) console.error("supplier-submit: " + failures + " storage target(s) failed");
  if (!stored) {
    return json(res, 503, { ok: false, error: msg(lang, "Le formulaire n’est pas encore relié à notre boîte de réception. Réessayez bientôt ou écrivez-nous depuis la page À propos.",
      "The form isn’t connected to our inbox yet. Please try again soon, or write to us from the About page.") });
  }
  return json(res, 200, { ok: true, status: "pending_review" });
};

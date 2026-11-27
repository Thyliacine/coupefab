/**
 * CoupeFab — "Demander une soumission / Request a quote" intake.
 * Stores/forwards each request for MANUAL handling; nothing is sent to shops automatically.
 *
 * Durable storage: each request is written to the CoupeFab admin Inbox (Vercel Blob).
 * Optional: QUOTE_WEBHOOK_URL (or NEWSLETTER_WEBHOOK_URL) also POSTs JSON to a sheet.
 * Without Blob storage the function answers 503 so the visitor is told to retry instead of being silently dropped.
 * Spam: honeypot "website", minimum fill time (t0), and a best-effort per-IP rate limit
 * (QUOTE_RATE_MAX requests per QUOTE_RATE_WINDOW_S seconds, default 5 per 3600; per warm instance).
 * Loi 25: consent must be explicitly true; the consent text version is stored with the request.
 */
const sec = require("./_security");
const URL_RE = /^https?:\/\/[^\s<>"']+$/i;
const PROCESSES = ["plasma", "laser", "waterjet", "bending", "machining", "router", "welding", "other"];
const MATERIALS = ["acier", "inox", "aluminium", "cuivre-laiton", "plastique-bois", "autre"];
const REGIONS = ["montreal", "monteregie", "laurentides-lanaudiere", "mauricie-centre", "quebec-chaudiere", "saguenay", "autre-qc", "hors-qc"];
const CONSENT_VERSION = "2026-11-26-loi25-v1";
const hits = new Map();
let ROUTING = { table: {} };
try { ROUTING = require("./_lead-routing.js"); } catch { /* table optional */ }

function json(res, status, body) {
  res.statusCode = status;
  res.setHeader("content-type", "application/json; charset=utf-8");
  res.setHeader("cache-control", "no-store");
  res.end(JSON.stringify(body));
}
function readBody(req) {
  return new Promise((resolve, reject) => {
    let raw = "";
    req.on("data", (c) => { raw += c; if (raw.length > 20_000) { reject(new Error("too large")); req.destroy(); } });
    req.on("end", () => { try { resolve(raw ? JSON.parse(raw) : {}); } catch { reject(new Error("invalid json")); } });
    req.on("error", reject);
  });
}
const msg = (lang, fr, en) => (lang === "en" ? en : fr);
const s = (v, n) => sec.oneLine(v, n);

function rateLimited(ip) {
  const max = +process.env.QUOTE_RATE_MAX || 5, win = (+process.env.QUOTE_RATE_WINDOW_S || 3600) * 1000, now = Date.now();
  const list = (hits.get(ip) || []).filter((t) => now - t < win);
  list.push(now); hits.set(ip, list);
  return list.length > max;
}

async function toWebhook(entry) {
  const url = process.env.QUOTE_WEBHOOK_URL || process.env.NEWSLETTER_WEBHOOK_URL;
  if (!url || !/^https:\/\//i.test(url)) return false;
  const r = await fetch(url, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ type: "quote_request", ...entry }) });
  if (!r.ok) throw new Error("webhook " + r.status);
  return true;
}
async function toInbox(entry) {
  const { saveForm } = require("./_inbox");
  const lines = [
    (entry.process || "") + " / " + (entry.material || "") + " / " + (entry.region || ""),
    entry.description || "",
    entry.company ? ("Entreprise : " + entry.company) : "",
    entry.phone ? ("Téléphone : " + entry.phone) : "",
    entry.file_url ? ("Fichier : " + entry.file_url) : "",
  ].filter(Boolean);
  await saveForm({
    type: "quote",
    subject: "Demande de soumission : " + (entry.process || "") + " / " + (entry.region || ""),
    from: entry.email,
    fromName: entry.name || entry.company || "",
    to: "info@coupefab.ca",
    text: lines.join("\n"),
    fields: entry,
  });
  return true;
}

module.exports = async function handler(req, res) {
  if (req.method !== "POST") { res.setHeader("allow", "POST"); return json(res, 405, { ok: false, error: "method not allowed" }); }
  if (!sec.originOk(req)) return json(res, 403, { ok: false, error: "forbidden" });
  let b;
  try { b = await readBody(req); } catch { return json(res, 413, { ok: false, error: "Demande trop longue / request too large" }); }
  const lang = b.lang === "en" ? "en" : "fr";
  if (b.website) return json(res, 200, { ok: true });                       // honeypot
  const t0 = +b.t0 || 0;
  if (t0 && Date.now() - t0 < 3000) return json(res, 200, { ok: true });   // filled in < 3 s: a bot
  if (rateLimited(sec.clientIp(req)) || sec.limited(req, "quote", 1000, 3600_000, 150)) return json(res, 429, { ok: false, error: msg(lang, "Trop de demandes. Réessayez dans une heure.", "Too many requests. Please try again in an hour.") });

  const e = {
    process: s(b.process, 30), material: s(b.material, 30), thickness: s(b.thickness, 60), qty: Math.max(0, Math.floor(+b.qty || 0)),
    file_url: s(b.file_url, 500), description: sec.clean(b.description, 3000), region: s(b.region, 40), deadline: s(b.deadline, 10),
    name: s(b.name, 120), company: s(b.company, 200), email: s(b.email, 254).toLowerCase(), phone: s(b.phone, 40), lang,
  };
  if (!PROCESSES.includes(e.process) || !MATERIALS.includes(e.material) || !REGIONS.includes(e.region) || !e.qty)
    return json(res, 400, { ok: false, error: msg(lang, "Choisissez le procédé, le matériau, la région et la quantité.", "Pick the process, material, region and quantity.") });
  if (!e.name || !sec.validEmail(e.email)) return json(res, 400, { ok: false, error: msg(lang, "Nom et courriel valide requis.", "Name and a valid email are required.") });
  if (!e.file_url && !e.description) return json(res, 400, { ok: false, error: msg(lang, "Ajoutez un lien vers vos dessins ou une description.", "Add a link to your drawings or a description.") });
  if (e.file_url && !URL_RE.test(e.file_url)) return json(res, 400, { ok: false, error: msg(lang, "Le lien doit commencer par https://", "The link must start with https://") });
  if (e.deadline && !/^\d{4}-\d{2}-\d{2}$/.test(e.deadline)) e.deadline = "";
  if (b.consent !== true) return json(res, 400, { ok: false, error: msg(lang, "Le consentement est requis pour transmettre la demande.", "Consent is required to pass on the request.") });

  const matched_shops = ((ROUTING.table[e.region] || {})[e.process] || []).slice(0, 8); // for manual follow-up only
  const entry = { ...e, matched_shops, consent: true, consent_version: CONSENT_VERSION, status: "new", submittedAt: new Date().toISOString() };
  let stored = false;
  let failures = 0;
  for (const fn of [toWebhook, toInbox]) { try { stored = (await fn(entry)) || stored; } catch { failures += 1; } }
  if (failures) console.error("quote-request: " + failures + " storage target(s) failed");
  if (!stored) return json(res, 503, { ok: false, error: msg(lang, "Le formulaire n’est pas encore relié à notre boîte de réception. Réessayez bientôt ou écrivez à info@coupefab.ca.", "The form isn’t connected to our inbox yet. Please try again soon or write to info@coupefab.ca.") });
  return json(res, 200, { ok: true, status: "new" });
};

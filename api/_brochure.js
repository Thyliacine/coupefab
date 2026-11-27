/**
 * CoupeFab — supplier brochure / price-list upload (/fournisseurs/envoyer-brochure/).
 * Routed through api/supplier-submit.js (body.action) so no extra Vercel Function is created
 * (Hobby plan: 12 functions per deployment max).
 *
 * Flow (files up to 10 MB, above the 4.5 MB function body limit):
 *   1. action "brochure-token": validate fields + file name/size/type, honeypot, rate limit,
 *      return a short-lived Vercel Blob client token locked to one private pathname.
 *   2. browser PUTs the file straight to the private Blob store (inbox/uploads/<id>/<name>).
 *   3. action "brochure": check the signed upload id, look the blob up, re-check size and magic
 *      bytes, then save an Inbox message of type "brochure" (file = attachment; admin-only download).
 * Fallback: action "brochure" with file.data (base64, <= 2 MB) when the direct PUT is blocked.
 */
const crypto = require("crypto");
const blob = require("./_blob");
const inbox = require("./_inbox");
const sec = require("./_security");

const MAX_FILE = 10 * 1024 * 1024;
const MAX_INLINE = 2 * 1024 * 1024;
const TOKEN_TTL_MS = 15 * 60 * 1000;
const PER_IP_PER_HOUR = 6;
const GLOBAL_PER_HOUR = 60;
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const TYPES = {
  pdf: "application/pdf",
  jpg: "image/jpeg",
  jpeg: "image/jpeg",
  png: "image/png",
  xlsx: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  csv: "text/csv",
  docx: "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
};

const msg = (lang, fr, en) => (lang === "en" ? en : fr);

function json(res, status, body) {
  res.statusCode = status;
  res.setHeader("content-type", "application/json; charset=utf-8");
  res.setHeader("cache-control", "no-store");
  res.end(JSON.stringify(body));
}

function secret() {
  return process.env.ADMIN_SESSION_SECRET || process.env.BLOB_READ_WRITE_TOKEN || "";
}

function sign(s) {
  return crypto.createHmac("sha256", secret()).update("brochure|" + s).digest("hex");
}

function safeEq(a, b) {
  const x = Buffer.from(String(a)); const y = Buffer.from(String(b));
  return x.length === y.length && crypto.timingSafeEqual(x, y);
}

function safeName(name) {
  const n = String(name || "").normalize("NFKD").replace(/[\u0300-\u036f]/g, "")
    .replace(/[^\w.\- ]+/g, "_").replace(/\s+/g, "-").replace(/^[.\-_]+/, "").slice(-100);
  return n || "fichier";
}

function extOf(name) {
  const m = /\.([a-z0-9]+)$/i.exec(String(name || ""));
  return m ? m[1].toLowerCase() : "";
}

function sniff(ext, buf) {
  const b = buf.subarray(0, 8);
  if (ext === "pdf") return b.subarray(0, 4).toString("latin1") === "%PDF";
  if (ext === "jpg" || ext === "jpeg") return b[0] === 0xff && b[1] === 0xd8 && b[2] === 0xff;
  if (ext === "png") return b[0] === 0x89 && b.subarray(1, 4).toString("latin1") === "PNG";
  if (ext === "xlsx" || ext === "docx") return b[0] === 0x50 && b[1] === 0x4b && b[2] === 0x03 && b[3] === 0x04;
  if (ext === "csv") return !buf.subarray(0, 8192).includes(0);
  return false;
}

const clientIp = sec.clientIp;

function fields(b) {
  const t = (v, n) => String(v == null ? "" : v).replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f]/g, "").trim().slice(0, n);
  return {
    company: t(b.company, 200),
    contact: t(b.contact, 200),
    email: t(b.email, 254).replace(/\s+/g, "").toLowerCase(),
    phone: t(b.phone, 60),
    message: t(b.message, 3000),
    lang: b.lang === "en" ? "en" : "fr",
    page: t(b.page, 200),
  };
}

function check(f, b) {
  const L = (fr, en) => msg(f.lang, fr, en);
  if (!f.company || !f.contact) return L("Entreprise et nom de la personne-ressource requis.", "Company and contact name are required.");
  if (!sec.validEmail(f.email)) return L("Courriel invalide.", "Invalid email.");
  if (f.phone && !/^[0-9+().\-\s x#poste ext]{7,60}$/i.test(f.phone)) return L("Numéro de téléphone invalide.", "Invalid phone number.");
  if (b.consent !== true) return L("Autorisation requise.", "Authorization required.");
  return "";
}

function checkFile(lang, name, size) {
  const ext = extOf(name);
  if (!TYPES[ext]) return { error: msg(lang, "Formats acceptés : PDF, JPG, PNG, XLSX, CSV, DOCX.", "Accepted formats: PDF, JPG, PNG, XLSX, CSV, DOCX.") };
  const n = Number(size);
  if (!Number.isFinite(n) || n <= 0) return { error: msg(lang, "Fichier vide.", "Empty file.") };
  if (n > MAX_FILE) return { error: msg(lang, "Fichier trop lourd (10 Mo max).", "File too large (10 MB max).") };
  return { ext, contentType: TYPES[ext] };
}

let memHits = [];
async function rateLimited(req) {
  const now = Date.now();
  const ip = clientIp(req);
  const ipHash = crypto.createHash("sha256").update(ip + "|" + secret().slice(0, 12)).digest("hex").slice(0, 16);
  memHits = memHits.filter((h) => now - h.t < 3600_000);
  if (memHits.filter((h) => h.ip === ipHash).length >= PER_IP_PER_HOUR) return true;
  const hour = new Date(now).toISOString().slice(0, 13).replace(/[-T]/g, "");
  const prefix = "inbox/ratelimit/brochure/" + hour + "/";
  try {
    const all = await blob.list(prefix, { limit: 1000 });
    if (all.length >= GLOBAL_PER_HOUR) return true;
    if (all.filter((x) => (x.pathname || "").startsWith(prefix + ipHash)).length >= PER_IP_PER_HOUR) return true;
    await blob.put(prefix + ipHash + "-" + crypto.randomBytes(4).toString("hex") + ".txt", "1", { contentType: "text/plain", allowOverwrite: false });
  } catch (e) {
    console.error("brochure ratelimit store", e.message);
  }
  memHits.push({ ip: ipHash, t: now });
  return false;
}

function clientToken({ pathname, contentType, validUntil }) {
  const rw = process.env.BLOB_READ_WRITE_TOKEN || "";
  const storeId = rw.split("_")[3] || "";
  if (!storeId) throw new Error("bad blob token");
  const payload = Buffer.from(JSON.stringify({
    pathname,
    allowedContentTypes: [contentType],
    maximumSizeInBytes: MAX_FILE,
    addRandomSuffix: false,
    allowOverwrite: false,
    validUntil,
  })).toString("base64");
  const key = crypto.createHmac("sha256", rw).update(payload).digest("hex");
  return { storeId, token: "vercel_blob_client_" + storeId + "_" + Buffer.from(key + "." + payload).toString("base64") };
}

async function issueToken(b, req, res) {
  const f = fields(b);
  if (b.website) return json(res, 200, { ok: true, skip: true });
  if (!blob.configured()) return json(res, 503, { ok: false, error: msg(f.lang, "Envoi indisponible pour le moment. Écrivez à info@coupefab.ca.", "Uploads are unavailable right now. Email info@coupefab.ca.") });
  const err = check(f, b);
  if (err) return json(res, 400, { ok: false, error: err });
  const file = b.file || {};
  const ft = checkFile(f.lang, file.name, file.size);
  if (ft.error) return json(res, 400, { ok: false, error: ft.error });
  if (await rateLimited(req)) return json(res, 429, { ok: false, error: msg(f.lang, "Trop d’envois. Réessayez dans une heure ou écrivez à info@coupefab.ca.", "Too many uploads. Try again in an hour or email info@coupefab.ca.") });
  const id = inbox.nid("bro_");
  const pathname = "inbox/uploads/" + id + "/" + safeName(file.name);
  const exp = Date.now() + TOKEN_TTL_MS;
  const { token, storeId } = clientToken({ pathname, contentType: ft.contentType, validUntil: exp });
  const sig = sign(id + "|" + pathname + "|" + exp);
  return json(res, 200, { ok: true, id, pathname, exp, sig, token, storeId, contentType: ft.contentType, maxBytes: MAX_FILE });
}

async function save(f, att, req) {
  const lines = [
    "Entreprise : " + f.company,
    "Contact : " + f.contact,
    "Courriel : " + f.email,
    f.phone ? "Téléphone : " + f.phone : "",
    "Fichier : " + att.name + " (" + Math.round(att.size / 1024) + " Ko)",
    f.message ? "\n" + f.message : "",
  ].filter(Boolean);
  const m = {
    id: inbox.nid("msg_"),
    type: "brochure",
    status: "new",
    createdAt: new Date().toISOString(),
    from: f.email,
    fromName: f.contact + " — " + f.company,
    to: "info@coupefab.ca",
    subject: "Brochure / liste de prix : " + f.company,
    text: lines.join("\n"),
    html: "",
    fields: { company: f.company, contact: f.contact, email: f.email, phone: f.phone, message: f.message, lang: f.lang, page: f.page, file: { name: att.name, size: att.size, type: att.contentType } },
    attachments: [att],
    replies: [],
    source: "form",
  };
  await inbox.saveMessage(m);
  return m;
}

async function complete(b, req, res) {
  const f = fields(b);
  if (b.website) return json(res, 200, { ok: true });
  if (!blob.configured()) return json(res, 503, { ok: false, error: msg(f.lang, "Envoi indisponible pour le moment. Écrivez à info@coupefab.ca.", "Uploads are unavailable right now. Email info@coupefab.ca.") });
  const err = check(f, b);
  if (err) return json(res, 400, { ok: false, error: err });

  // Fallback: small file sent inline (direct Blob PUT blocked by a proxy/extension).
  if (b.file && b.file.data) {
    const data = Buffer.from(String(b.file.data), "base64");
    const ft = checkFile(f.lang, b.file.name, data.length);
    if (ft.error) return json(res, 400, { ok: false, error: ft.error });
    if (data.length > MAX_INLINE) return json(res, 413, { ok: false, error: msg(f.lang, "Fichier trop lourd pour l’envoi de secours (2 Mo). Écrivez à info@coupefab.ca.", "File too large for the fallback upload (2 MB). Email info@coupefab.ca.") });
    if (!sniff(ft.ext, data)) return json(res, 400, { ok: false, error: msg(f.lang, "Le contenu du fichier ne correspond pas à son extension.", "The file content doesn’t match its extension.") });
    if (await rateLimited(req)) return json(res, 429, { ok: false, error: msg(f.lang, "Trop d’envois. Réessayez dans une heure.", "Too many uploads. Try again in an hour.") });
    const id = inbox.nid("bro_");
    const att = await inbox.addAttachment(id, { name: safeName(b.file.name), data, contentType: ft.contentType });
    const m = await save(f, att, req);
    return json(res, 200, { ok: true, id: m.id });
  }

  const id = String(b.id || ""), pathname = String(b.pathname || ""), exp = Number(b.exp || 0);
  if (!/^bro_[a-z0-9]+$/.test(id) || !pathname.startsWith("inbox/uploads/" + id + "/") || !b.sig
      || !safeEq(sign(id + "|" + pathname + "|" + exp), b.sig) || Date.now() > exp + 30 * 60 * 1000) {
    return json(res, 400, { ok: false, error: msg(f.lang, "Envoi expiré. Réessayez.", "Upload expired. Please try again.") });
  }
  const hit = (await blob.list("inbox/uploads/" + id + "/", { limit: 5 })).find((x) => x.pathname === pathname);
  if (!hit) return json(res, 400, { ok: false, error: msg(f.lang, "Fichier introuvable. Réessayez.", "File not found. Please try again.") });
  const name = pathname.split("/").pop();
  const ft = checkFile(f.lang, name, hit.size);
  let ok = !ft.error;
  if (ok) {
    try {
      const { body } = await blob.getBuffer(hit.url || pathname);
      ok = body.length <= MAX_FILE && sniff(ft.ext, body);
    } catch (e) { console.error("brochure read", e.message); ok = false; }
  }
  if (!ok) {
    try { await blob.del(hit.url || pathname); } catch (e) { /* ignore */ }
    return json(res, 400, { ok: false, error: ft.error || msg(f.lang, "Le contenu du fichier ne correspond pas à son extension.", "The file content doesn’t match its extension.") });
  }
  const att = { name, pathname, size: hit.size, contentType: ft.contentType, url: hit.url || "" };
  const m = await save(f, att, req);
  return json(res, 200, { ok: true, id: m.id });
}

async function handle(b, req, res) {
  try {
    if (b.action === "brochure-token") return await issueToken(b, req, res);
    return await complete(b, req, res);
  } catch (e) {
    console.error("brochure failed", e && e.message);
    return json(res, 500, { ok: false, error: msg(b.lang, "Erreur d’envoi. Réessayez ou écrivez à info@coupefab.ca.", "Upload error. Try again or email info@coupefab.ca.") });
  }
}

module.exports = { handle, sniff, safeName, checkFile, clientToken, TYPES, MAX_FILE };

/**
 * Shared hardening helpers for the public form functions (not a Vercel Function:
 * files starting with "_" are bundled, never routed).
 *
 * - clientIp: Vercel sets x-real-ip / x-vercel-forwarded-for itself; the left-most
 *   x-forwarded-for value is only a last resort because a client can prepend to it.
 * - originOk: refuses cross-site browser posts (Origin/Referer must be coupefab.ca or a
 *   coupefab Vercel preview). Requests with neither header (curl, old browsers) pass,
 *   so the honeypot + rate limits still apply to them.
 * - limit: best-effort sliding-window limiter, per IP and per warm instance (global cap).
 * - clean: strips control characters (header/CSV injection) and trims to a max length.
 */
const crypto = require("crypto");

const EMAIL_RE = /^[^\s@<>()[\]\\,;:"]{1,64}@[\p{L}\p{N}](?:[\p{L}\p{N}-]{0,62}[\p{L}\p{N}])?(?:\.[\p{L}\p{N}](?:[\p{L}\p{N}-]{0,62}[\p{L}\p{N}])?)+$/u;

function validEmail(e) {
  const s = String(e || "");
  return s.length <= 254 && EMAIL_RE.test(s);
}

function clientIp(req) {
  const h = (req && req.headers) || {};
  const v = h["x-real-ip"] || String(h["x-vercel-forwarded-for"] || "").split(",")[0]
    || String(h["x-forwarded-for"] || "").split(",")[0] || (req.socket && req.socket.remoteAddress) || "0";
  return String(v).trim().slice(0, 64);
}

const HOST_RE = /^(coupefab\.ca|www\.coupefab\.ca|coupefab\.com|www\.coupefab\.com|coupefab\.vercel\.app|coupefab-[a-z0-9-]+\.vercel\.app)$/i;

function hostOk(u) {
  try {
    const x = new URL(u);
    return x.protocol === "https:" && HOST_RE.test(x.hostname);
  } catch { return false; }
}

function originOk(req) {
  const h = (req && req.headers) || {};
  if (h.origin && h.origin !== "null") return hostOk(h.origin);
  if (h.origin === "null") return false;
  if (h.referer) return hostOk(h.referer);
  return true;
}

const buckets = new Map();
function limit(key, max, windowMs, globalMax) {
  const now = Date.now();
  if (buckets.size > 5000) {
    for (const [k, v] of buckets) if (!v.length || now - v[v.length - 1] > windowMs) buckets.delete(k);
  }
  const g = "*" + key.split("|")[0];
  const list = (buckets.get(key) || []).filter((t) => now - t < windowMs);
  const glist = (buckets.get(g) || []).filter((t) => now - t < windowMs);
  list.push(now); glist.push(now);
  buckets.set(key, list); buckets.set(g, glist);
  return list.length > max || (globalMax ? glist.length > globalMax : false);
}

function limited(req, scope, max = 8, windowMs = 3600_000, globalMax = 300) {
  const ip = crypto.createHash("sha256").update(clientIp(req)).digest("hex").slice(0, 16);
  return limit(scope + "|" + ip, max, windowMs, globalMax);
}

function clean(v, n) {
  return String(v == null ? "" : v)
    .replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f\u2028\u2029]/g, "")
    .trim().slice(0, n);
}

function oneLine(v, n) {
  return clean(v, n).replace(/[\r\n\t]+/g, " ");
}

module.exports = { validEmail, clientIp, originOk, hostOk, limited, clean, oneLine };

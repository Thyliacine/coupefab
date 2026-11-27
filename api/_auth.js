/**
 * Admin session cookie + rate-limited login.
 * Cookie: cf_admin = v1.<expMs>.<hexhmac>  (HMAC-SHA256 of "v1.<expMs>")
 */
const crypto = require("crypto");
const COOKIE = "cf_admin";
const MAX_AGE_S = 12 * 60 * 60;
const LOGIN_WINDOW_MS = 15 * 60 * 1000;
const LOGIN_MAX = 5;
const hits = new Map();

function password() { return process.env.ADMIN_PASSWORD || ""; }
function secret() { return process.env.ADMIN_SESSION_SECRET || process.env.ADMIN_PASSWORD || ""; }
function configured() { return Boolean(password() && secret()); }

function json(res, status, body) {
  res.statusCode = status;
  res.setHeader("content-type", "application/json; charset=utf-8");
  res.setHeader("cache-control", "no-store");
  res.setHeader("x-robots-tag", "noindex, nofollow");
  res.end(JSON.stringify(body));
}

function clientIp(req) {
  const xf = String(req.headers["x-forwarded-for"] || "").split(",")[0].trim();
  return xf || req.headers["x-real-ip"] || req.socket?.remoteAddress || "0.0.0.0";
}

function rateLimited(ip) {
  const now = Date.now();
  const list = (hits.get(ip) || []).filter((t) => now - t < LOGIN_WINDOW_MS);
  list.push(now);
  hits.set(ip, list);
  return list.length > LOGIN_MAX;
}

function safeEqual(a, b) {
  const ba = Buffer.from(String(a));
  const bb = Buffer.from(String(b));
  if (ba.length !== bb.length) {
    crypto.timingSafeEqual(ba.length ? ba : Buffer.from("x"), ba.length ? ba : Buffer.from("x"));
    return false;
  }
  return crypto.timingSafeEqual(ba, bb);
}

function sign(payload) {
  return crypto.createHmac("sha256", secret()).update(payload).digest("hex");
}

function makeCookie() {
  const exp = Date.now() + MAX_AGE_S * 1000;
  const payload = "v1." + exp;
  return payload + "." + sign(payload);
}

function parseCookie(header) {
  const m = String(header || "").match(new RegExp("(?:^|;\\s*)" + COOKIE + "=([^;]+)"));
  return m ? decodeURIComponent(m[1]) : "";
}

function validSession(req) {
  if (!secret()) return false;
  const raw = parseCookie(req.headers.cookie);
  const parts = raw.split(".");
  if (parts.length !== 3 || parts[0] !== "v1") return false;
  const payload = parts[0] + "." + parts[1];
  if (!safeEqual(sign(payload), parts[2])) return false;
  const exp = Number(parts[1]);
  return Number.isFinite(exp) && Date.now() < exp;
}

function setSessionCookie(res, value, maxAge) {
  const attrs = [
    COOKIE + "=" + encodeURIComponent(value),
    "Path=/",
    "HttpOnly",
    "Secure",
    "SameSite=Lax",
    "Max-Age=" + String(maxAge),
  ];
  res.setHeader("set-cookie", attrs.join("; "));
}

function allowedOrigin(req) {
  const origin = String(req.headers.origin || "");
  if (!origin) {
    const ref = String(req.headers.referer || "");
    if (/^https:\/\/(coupefab\.ca|www\.coupefab\.ca|coupefab\.vercel\.app)(\/|$)/i.test(ref)) return true;
    if (/^https:\/\/coupefab-[a-z0-9-]+\.vercel\.app(\/|$)/i.test(ref)) return true;
    return !req.headers.referer; // same-origin form posts may omit both
  }
  try {
    const u = new URL(origin);
    if (u.protocol !== "https:") return false;
    return u.hostname === "coupefab.ca" || u.hostname === "www.coupefab.ca"
      || u.hostname === "coupefab.vercel.app"
      || /^coupefab-[a-z0-9-]+\.vercel\.app$/.test(u.hostname);
  } catch { return false; }
}

function requireAdmin(req, res, { csrf = true } = {}) {
  if (!configured()) {
    json(res, 503, { ok: false, error: "Admin password is not set." });
    return false;
  }
  if (!validSession(req)) {
    json(res, 401, { ok: false, error: "Connectez-vous." });
    return false;
  }
  if (csrf && req.method !== "GET" && req.method !== "HEAD" && !allowedOrigin(req)) {
    json(res, 403, { ok: false, error: "Origine refusée." });
    return false;
  }
  return true;
}

function readBody(req, limit = 1_000_000) {
  return new Promise((resolve, reject) => {
    let raw = "";
    req.on("data", (c) => {
      raw += c;
      if (raw.length > limit) { reject(new Error("too large")); req.destroy(); }
    });
    req.on("end", () => resolve(raw));
    req.on("error", reject);
  });
}

async function handleLogin(req, res) {
  if (req.method !== "POST") return json(res, 405, { ok: false, error: "POST only" });
  if (!configured()) return json(res, 503, { ok: false, error: "Admin password is not set." });
  if (!allowedOrigin(req) && req.headers.origin) return json(res, 403, { ok: false, error: "Origine refusée." });
  const ip = clientIp(req);
  if (rateLimited(ip)) {
    res.setHeader("retry-after", "900");
    return json(res, 429, { ok: false, error: "Trop d’essais. Réessayez dans 15 minutes." });
  }
  let body = {};
  try { body = JSON.parse(await readBody(req, 4000)) || {}; } catch { return json(res, 400, { ok: false, error: "JSON invalide." }); }
  if (!safeEqual(String(body.password || ""), password())) {
    return json(res, 401, { ok: false, error: "Mot de passe incorrect." });
  }
  setSessionCookie(res, makeCookie(), MAX_AGE_S);
  return json(res, 200, { ok: true });
}

function handleLogout(req, res) {
  setSessionCookie(res, "deleted", 0);
  return json(res, 200, { ok: true });
}

module.exports = {
  COOKIE, json, configured, validSession, requireAdmin, handleLogin, handleLogout,
  allowedOrigin, readBody, clientIp, safeEqual,
};

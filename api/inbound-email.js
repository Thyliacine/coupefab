/**
 * Resend inbound webhook (event email.received).
 * Verifies the Svix signature (svix-id, svix-timestamp, svix-signature)
 * with RESEND_WEBHOOK_SECRET (whsec_… from the Resend webhook page).
 * Stores the message in the CoupeFab admin Inbox. Never forwards to Gmail.
 */
const crypto = require("crypto");
const inbox = require("./_inbox");

function json(res, status, body) {
  res.statusCode = status;
  res.setHeader("content-type", "application/json; charset=utf-8");
  res.setHeader("cache-control", "no-store");
  res.end(JSON.stringify(body));
}

function readRaw(req, limit = 2_000_000) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    let n = 0;
    req.on("data", (c) => {
      n += c.length;
      if (n > limit) { reject(new Error("too large")); req.destroy(); return; }
      chunks.push(c);
    });
    req.on("end", () => resolve(Buffer.concat(chunks).toString("utf8")));
    req.on("error", reject);
  });
}

function header(req, name) {
  return String(req.headers[name] || req.headers[name.toLowerCase()] || "");
}

function verifySvix(raw, req, secret) {
  if (!secret) return false;
  const id = header(req, "svix-id") || header(req, "webhook-id");
  const ts = header(req, "svix-timestamp") || header(req, "webhook-timestamp");
  const sig = header(req, "svix-signature") || header(req, "webhook-signature");
  if (!id || !ts || !sig) return false;
  const tsNum = Number(ts);
  if (!Number.isFinite(tsNum) || Math.abs(Date.now() / 1000 - tsNum) > 5 * 60) return false;
  const key = secret.startsWith("whsec_") ? Buffer.from(secret.slice(6), "base64") : Buffer.from(secret, "base64");
  const toSign = id + "." + ts + "." + raw;
  const expected = crypto.createHmac("sha256", key).update(toSign).digest("base64");
  const candidates = sig.split(/\s+/).map((p) => {
    const i = p.indexOf(",");
    return i >= 0 ? p.slice(i + 1) : p;
  }).filter(Boolean);
  const expBuf = Buffer.from(expected);
  for (const c of candidates) {
    const cb = Buffer.from(c);
    if (cb.length === expBuf.length && crypto.timingSafeEqual(cb, expBuf)) return true;
  }
  return false;
}

function firstAddr(v) {
  if (!v) return "";
  if (Array.isArray(v)) return firstAddr(v[0]);
  if (typeof v === "string") {
    const m = v.match(/<([^>]+)>/);
    return (m ? m[1] : v).trim();
  }
  if (typeof v === "object") return v.email || v.address || v.value || "";
  return String(v);
}

function nameOf(v) {
  if (!v) return "";
  if (Array.isArray(v)) return nameOf(v[0]);
  if (typeof v === "string") {
    const m = v.match(/^(.*?)\s*<[^>]+>/);
    return m ? m[1].replace(/^["']|["']$/g, "").trim() : "";
  }
  if (typeof v === "object") return v.name || "";
  return "";
}

async function fetchReceiving(emailId) {
  const key = process.env.RESEND_API_KEY;
  if (!key || !emailId) return null;
  const r = await fetch("https://api.resend.com/emails/receiving/" + encodeURIComponent(emailId), {
    headers: { authorization: "Bearer " + key, accept: "application/json" },
  });
  if (!r.ok) {
    console.error("resend receiving get", r.status, await r.text().catch(() => ""));
    return null;
  }
  return r.json();
}

async function downloadAttachment(att) {
  const url = att.download_url || att.url;
  if (!url) return null;
  const headers = {};
  if (process.env.RESEND_API_KEY) headers.authorization = "Bearer " + process.env.RESEND_API_KEY;
  const r = await fetch(url, { headers });
  if (!r.ok) return null;
  const buf = Buffer.from(await r.arrayBuffer());
  return { name: att.filename || att.name || "piece-jointe", data: buf, contentType: att.content_type || att.contentType || r.headers.get("content-type") || "application/octet-stream" };
}

module.exports = async (req, res) => {
  if (req.method === "GET") return json(res, 200, { ok: true, service: "coupefab-inbound-email" });
  if (req.method !== "POST") return json(res, 405, { ok: false, error: "POST only" });
  const secret = process.env.RESEND_WEBHOOK_SECRET;
  if (!secret) return json(res, 503, { ok: false, error: "RESEND_WEBHOOK_SECRET is not set." });
  let raw;
  try { raw = await readRaw(req); } catch { return json(res, 413, { ok: false, error: "too large" }); }
  if (!verifySvix(raw, req, secret)) return json(res, 401, { ok: false, error: "invalid signature" });
  let event;
  try { event = JSON.parse(raw); } catch { return json(res, 400, { ok: false, error: "invalid json" }); }
  const type = event.type || event.event || "";
  if (type && type !== "email.received") return json(res, 200, { ok: true, ignored: type });
  const data = event.data || event;
  const emailId = data.email_id || data.id || "";
  let full = null;
  try { full = await fetchReceiving(emailId); } catch (e) { console.error("fetch receiving", e); }
  const src = full || data;
  const from = firstAddr(src.from);
  const toList = [].concat(src.to || []);
  const to = toList.map(firstAddr).filter(Boolean).join(", ") || "info@coupefab.ca";
  const id = inbox.nid("msg_");
  const attachments = [];
  for (const att of src.attachments || []) {
    try {
      const file = await downloadAttachment(att);
      if (file) attachments.push(await inbox.addAttachment(id, file));
    } catch (e) { console.error("inbound att", e); }
  }
  const msg = {
    id,
    type: "email",
    status: "new",
    createdAt: src.created_at || event.created_at || new Date().toISOString(),
    from,
    fromName: nameOf(src.from),
    to,
    cc: [].concat(src.cc || []).map(firstAddr).filter(Boolean).join(", "),
    subject: src.subject || data.subject || "(sans objet)",
    text: src.text || "",
    html: src.html || "",
    messageId: src.message_id || (src.headers && (src.headers["message-id"] || src.headers["Message-ID"])) || "",
    references: src.headers && (src.headers.references || src.headers.References) || "",
    resendEmailId: emailId,
    attachments,
    replies: [],
    source: "resend-inbound",
    fields: { to, from },
  };
  try {
    await inbox.saveMessage(msg);
  } catch (e) {
    console.error("inbound store", e);
    return json(res, 500, { ok: false, error: "store failed" });
  }
  return json(res, 200, { ok: true, id: msg.id });
};

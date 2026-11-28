/**
 * Inbox messages stored as one JSON blob each: inbox/messages/{id}.json
 * Attachments: inbox/attachments/{id}/{safeName}
 */
const crypto = require("crypto");
const blob = require("./_blob");

const TYPES = ["quote", "newsletter", "contact", "supplier", "email", "placement", "brochure"];
const STATUSES = ["new", "read", "archived"];

function nid(prefix) {
  return prefix + Date.now().toString(36) + crypto.randomBytes(4).toString("hex");
}

function safeName(name) {
  return String(name || "fichier").replace(/[^\w.\- ]+/g, "_").replace(/\s+/g, " ").trim().slice(0, 120) || "fichier";
}

function summaryOf(msg) {
  return {
    id: msg.id,
    type: msg.type,
    status: msg.status,
    createdAt: msg.createdAt,
    from: msg.from || "",
    fromName: msg.fromName || "",
    to: msg.to || "",
    subject: msg.subject || "",
    preview: String(msg.text || msg.html || "").replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim().slice(0, 180),
    attachments: (msg.attachments || []).map((a) => ({ name: a.name, size: a.size, contentType: a.contentType, pathname: a.pathname })),
    replies: (msg.replies || []).length,
  };
}

function pathFor(id) {
  return "inbox/messages/" + id + ".json";
}

async function saveMessage(msg) {
  if (!msg.id) msg.id = nid("msg_");
  if (!msg.createdAt) msg.createdAt = new Date().toISOString();
  if (!STATUSES.includes(msg.status)) msg.status = "new";
  if (!Array.isArray(msg.attachments)) msg.attachments = [];
  if (!Array.isArray(msg.replies)) msg.replies = [];
  const put = await blob.putJSON(pathFor(msg.id), msg);
  if (put && put.url) msg.blobUrl = put.url;
  if (put && put.url) await blob.putJSON(pathFor(msg.id), msg);
  return msg;
}

async function addAttachment(id, { name, data, contentType }) {
  const fn = safeName(name);
  const pathname = "inbox/attachments/" + id + "/" + fn;
  const buf = Buffer.isBuffer(data) ? data : Buffer.from(data);
  const put = await blob.put(pathname, buf, { contentType: contentType || "application/octet-stream", allowOverwrite: true });
  return { name: fn, pathname, size: buf.length, contentType: contentType || "application/octet-stream", url: put.url || "" };
}

async function getMessage(id) {
  if (!/^[A-Za-z0-9_-]+$/.test(id)) return null;
  const exact = pathFor(id);
  const files = await blob.list("inbox/messages/" + id);
  const hit = files.find((b) => b.pathname === exact)
    || files.find((b) => (b.pathname || "").endsWith("/" + id + ".json"))
    || files.find((b) => (b.pathname || "").includes("/" + id) && /\.json$/.test(b.pathname || ""));
  if (hit) {
    const { body } = await blob.getBuffer(hit.pathname || exact || hit.url);
    return JSON.parse(body.toString("utf8"));
  }
  try {
    return await blob.getJSON(exact);
  } catch (e) {
    if (e.status === 404) return null;
    throw e;
  }
}

async function listMessages() {
  const files = await blob.list("inbox/messages/");
  const msgs = [];
  for (const f of files) {
    if (!/\.json$/.test(f.pathname || f.url || "")) continue;
    try {
      const { body } = await blob.getBuffer(f.pathname || f.url);
      msgs.push(JSON.parse(body.toString("utf8")));
    } catch (e) {
      console.error("inbox list skip", e.message);
    }
  }
  msgs.sort((a, b) => String(b.createdAt || "").localeCompare(String(a.createdAt || "")));
  return msgs;
}

async function updateStatus(id, status) {
  if (!STATUSES.includes(status)) throw new Error("invalid status");
  const msg = await getMessage(id);
  if (!msg) return null;
  msg.status = status;
  msg.updatedAt = new Date().toISOString();
  await saveMessage(msg);
  return msg;
}

async function addReply(id, reply) {
  const msg = await getMessage(id);
  if (!msg) return null;
  msg.replies = msg.replies || [];
  msg.replies.push(reply);
  msg.updatedAt = new Date().toISOString();
  if (msg.status === "new") msg.status = "read";
  await saveMessage(msg);
  return msg;
}

function matchQuery(msg, q, type, status) {
  if (type && msg.type !== type) return false;
  if (status && msg.status !== status) return false;
  if (!q) return true;
  const hay = [
    msg.from, msg.fromName, msg.to, msg.subject, msg.text, msg.html,
    msg.id, JSON.stringify(msg.fields || {}),
  ].join("\n").toLowerCase();
  return hay.includes(q);
}

async function saveForm({ type, subject, from, fromName, to, text, fields, files }) {
  const id = nid("msg_");
  const attachments = [];
  for (const f of files || []) {
    if (!f || !f.data) continue;
    const data = typeof f.data === "string" ? Buffer.from(f.data, "base64") : f.data;
    attachments.push(await addAttachment(id, { name: f.name, data, contentType: f.type || f.contentType }));
  }
  const msg = {
    id,
    type,
    status: "new",
    createdAt: new Date().toISOString(),
    from: from || "",
    fromName: fromName || "",
    to: to || "info@coupefab.ca",
    subject: subject || "",
    text: text || "",
    html: "",
    fields: fields || {},
    attachments,
    replies: [],
    source: "form",
  };
  await saveMessage(msg);
  return msg;
}

function csvEscape(v) {
  let s = String(v == null ? "" : v);
  // Spreadsheet formula injection: a cell starting with = + - @ (or tab/CR) is
  // executed by Excel/Sheets; prefix it so it is shown as text.
  if (/^[=+\-@\t\r]/.test(s)) s = "'" + s;
  if (/[",\n\r]/.test(s)) return '"' + s.replace(/"/g, '""') + '"';
  return s;
}

function toCSV(msgs) {
  const cols = ["id", "type", "status", "createdAt", "from", "fromName", "to", "subject", "preview", "attachments"];
  const lines = [cols.join(",")];
  for (const m of msgs) {
    const s = summaryOf(m);
    lines.push([
      s.id, s.type, s.status, s.createdAt, s.from, s.fromName, s.to, s.subject, s.preview,
      (s.attachments || []).map((a) => a.name).join("; "),
    ].map(csvEscape).join(","));
  }
  return lines.join("\r\n") + "\r\n";
}

module.exports = {
  TYPES, STATUSES, nid, summaryOf, saveMessage, addAttachment, getMessage,
  listMessages, updateStatus, addReply, matchQuery, saveForm, toCSV, pathFor,
};

/**
 * Minimal Vercel Blob REST client (no npm). Uses BLOB_READ_WRITE_TOKEN.
 * Store "coupefab-inbox" is private and connected to this project.
 */
const API = (process.env.VERCEL_BLOB_API_URL || "https://vercel.com/api/blob").replace(/\/$/, "");
const VERSION = process.env.VERCEL_BLOB_API_VERSION_OVERRIDE || "13";

function token() {
  const t = process.env.BLOB_READ_WRITE_TOKEN;
  if (!t) throw new Error("BLOB_READ_WRITE_TOKEN missing");
  return t;
}

function configured() {
  return Boolean(process.env.BLOB_READ_WRITE_TOKEN);
}

function headers(extra) {
  return {
    authorization: "Bearer " + token(),
    "x-api-version": VERSION,
    ...(process.env.BLOB_STORE_ID ? { "x-vercel-blob-store-id": process.env.BLOB_STORE_ID } : {}),
    ...extra,
  };
}

async function request(pathnameQs, init) {
  const res = await fetch(API + pathnameQs, { ...init, headers: { ...headers(init.headers), ...(init.headers || {}) } });
  if (!res.ok) {
    let detail = res.statusText;
    try { const j = await res.json(); detail = (j.error && (j.error.message || j.error.code)) || JSON.stringify(j); } catch { try { detail = await res.text(); } catch { /* ignore */ } }
    const err = new Error("blob " + res.status + " " + detail);
    err.status = res.status;
    throw err;
  }
  const ct = res.headers.get("content-type") || "";
  if (ct.includes("application/json")) return res.json();
  return res;
}

async function put(pathname, body, { contentType = "application/octet-stream", allowOverwrite = true, cacheControlMaxAge = 60 } = {}) {
  const qs = "/?pathname=" + encodeURIComponent(pathname);
  const buf = Buffer.isBuffer(body) || body instanceof Uint8Array ? body : Buffer.from(typeof body === "string" ? body : String(body));
  return request(qs, {
    method: "PUT",
    headers: {
      "x-content-type": contentType,
      "x-add-random-suffix": "0",
      "x-allow-overwrite": allowOverwrite ? "1" : "0",
      "x-cache-control-max-age": String(cacheControlMaxAge),
    },
    body: buf,
  });
}

async function putJSON(pathname, obj) {
  return put(pathname, JSON.stringify(obj), { contentType: "application/json; charset=utf-8", allowOverwrite: true, cacheControlMaxAge: 60 });
}

async function list(prefix, { limit = 1000, cursor } = {}) {
  const out = [];
  let cur = cursor || "";
  do {
    let qs = "/?prefix=" + encodeURIComponent(prefix) + "&limit=" + Math.min(limit, 1000);
    if (cur) qs += "&cursor=" + encodeURIComponent(cur);
    const page = await request(qs, { method: "GET" });
    out.push(...(page.blobs || []));
    cur = page.hasMore ? (page.cursor || "") : "";
    if (out.length >= limit) break;
  } while (cur);
  return out;
}

async function getBuffer(pathnameOrUrl) {
  // Prefer the private blob URL when we have it; fall back to the API.
  if (/^https?:\/\//i.test(pathnameOrUrl)) {
    const res = await fetch(pathnameOrUrl, { headers: headers() });
    if (!res.ok) {
      const err = new Error("blob get " + res.status);
      err.status = res.status;
      throw err;
    }
    const buf = Buffer.from(await res.arrayBuffer());
    return { body: buf, contentType: res.headers.get("content-type") || "application/octet-stream" };
  }
  const res = await request("/get?pathname=" + encodeURIComponent(pathnameOrUrl), { method: "GET" });
  // request() may have parsed JSON; if so wrap it
  if (res && res.body && typeof res.arrayBuffer === "function") {
    return { body: Buffer.from(await res.arrayBuffer()), contentType: res.headers.get("content-type") || "application/octet-stream" };
  }
  return { body: Buffer.from(JSON.stringify(res)), contentType: "application/json" };
}

async function getJSON(pathname) {
  const { body } = await getBuffer(pathname);
  return JSON.parse(body.toString("utf8"));
}

async function del(pathnameOrUrl) {
  return request("/delete", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ urls: [pathnameOrUrl] }),
  });
}

module.exports = { configured, put, putJSON, list, getBuffer, getJSON, del };

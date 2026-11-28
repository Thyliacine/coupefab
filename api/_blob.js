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
  const qs = "/?pathname=" + encodeURIComponent(pathname) + "&access=private";
  const buf = Buffer.isBuffer(body) || body instanceof Uint8Array ? body : Buffer.from(typeof body === "string" ? body : String(body));
  return request(qs, {
    method: "PUT",
    headers: {
      "x-vercel-blob-access": "private",
      "x-content-type": contentType,
      "x-add-random-suffix": "false",
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

function assertBlobHost(url) {
  let u;
  try { u = new URL(url); } catch {
    const err = new Error("blob get refused: not a Vercel Blob URL");
    err.status = 400;
    throw err;
  }
  if (u.protocol !== "https:" || !/\.blob\.vercel-storage\.com$/i.test(u.hostname)) {
    const err = new Error("blob get refused: not a Vercel Blob URL");
    err.status = 400;
    throw err;
  }
  return u;
}

function pathnameOf(pathnameOrUrl) {
  if (!/^https?:\/\//i.test(pathnameOrUrl)) return String(pathnameOrUrl || "").replace(/^\//, "");
  const u = assertBlobHost(pathnameOrUrl);
  return decodeURIComponent(u.pathname.replace(/^\//, ""));
}

function storeIdFromToken() {
  // vercel_blob_rw_<storeId>_<secret> — never log the token.
  const parts = String(token()).split("_");
  const id = parts[3] || "";
  return id.replace(/^store_/, "");
}

function storeId() {
  const env = String(process.env.BLOB_STORE_ID || "").trim().replace(/^store_/, "");
  return env || storeIdFromToken();
}

function candidateUrls(pathnameOrUrl) {
  const urls = [];
  const seen = new Set();
  const add = (u) => { if (u && !seen.has(u)) { seen.add(u); urls.push(u); } };
  if (/^https?:\/\//i.test(pathnameOrUrl)) {
    const u = assertBlobHost(pathnameOrUrl);
    add(u.origin + u.pathname);
    // Listed URLs may omit the .private. infix; the SDK reads from {id}.private.blob...
    if (!/\.(private|public)\.blob\.vercel-storage\.com$/i.test(u.hostname)) {
      const id = u.hostname.replace(/\.blob\.vercel-storage\.com$/i, "");
      add("https://" + id + ".private.blob.vercel-storage.com" + u.pathname);
    }
  } else {
    const pathname = pathnameOf(pathnameOrUrl);
    const id = storeId();
    if (!pathname || !id) {
      const err = new Error("blob get refused: missing pathname or store id");
      err.status = 400;
      throw err;
    }
    add("https://" + id + ".private.blob.vercel-storage.com/" + pathname);
  }
  return urls;
}

async function sleep(ms) { return new Promise((r) => setTimeout(r, ms)); }

async function getBuffer(pathnameOrUrl) {
  // Download from the Blob storage host with Authorization only (same as the
  // official SDK). There is no vercel.com/api/blob/get?pathname= endpoint.
  const urls = candidateUrls(pathnameOrUrl);
  const authOnly = { authorization: "Bearer " + token() };
  let last;
  for (const url of urls) {
    for (let i = 0; i < 4; i++) {
      const res = await fetch(url, { method: "GET", headers: authOnly });
      if (res.ok) {
        return { body: Buffer.from(await res.arrayBuffer()), contentType: res.headers.get("content-type") || "application/octet-stream" };
      }
      const mitigated = res.headers.get("x-vercel-mitigated") || "";
      last = new Error("blob get " + res.status + (mitigated ? " " + mitigated : ""));
      last.status = res.status;
      if (res.status === 429 && i < 3) {
        await sleep(500 * Math.pow(2, i));
        continue;
      }
      break;
    }
  }
  throw last;
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

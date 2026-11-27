/**
 * CoupeFab — payment hook for featured supplier spots (future Stripe Checkout / Billing).
 * DORMANT: answers 503 until both env vars below are set. No Stripe product or price exists yet.
 *
 *   STRIPE_WEBHOOK_SECRET   whsec_… from the Stripe dashboard webhook endpoint (signature check)
 *   FEATURED_WEBHOOK_URL    where to store the normalized event (e.g. Apps Script → Sheet). The daily
 *                           refresh (or `python3 -m revenue.featured event.json`) applies it to
 *                           data/revenue/featured.json via revenue.featured.apply_subscription_event.
 *
 * Featured = paid: a spot turns ON for checkout.session.completed / customer.subscription.created|updated
 * with status active|trialing, and OFF for customer.subscription.deleted or any other status.
 * The Checkout Session / Subscription must carry metadata: supplier_id (required), tier, categories (comma list).
 */
const crypto = require("crypto");

function json(res, status, body) {
  res.statusCode = status;
  res.setHeader("content-type", "application/json; charset=utf-8");
  res.setHeader("cache-control", "no-store");
  res.end(JSON.stringify(body));
}
function rawBody(req) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    req.on("data", (c) => chunks.push(c));
    req.on("end", () => resolve(Buffer.concat(chunks)));
    req.on("error", reject);
  });
}
function verify(raw, header, secret, toleranceS = 300) {
  const parts = Object.fromEntries(String(header || "").split(",").map((kv) => kv.split("=")).filter((x) => x.length === 2).map(([k, v]) => [k.trim(), v.trim()]));
  const t = +parts.t, v1 = String(header || "").split(",").filter((x) => x.trim().startsWith("v1=")).map((x) => x.trim().slice(3));
  if (!t || !v1.length || Math.abs(Date.now() / 1000 - t) > toleranceS) return false;
  const expected = crypto.createHmac("sha256", secret).update(`${t}.${raw.toString("utf8")}`).digest("hex");
  return v1.some((sig) => sig.length === expected.length && crypto.timingSafeEqual(Buffer.from(sig), Buffer.from(expected)));
}
const day = (unix) => (unix ? new Date(unix * 1000).toLocaleDateString("en-CA", { timeZone: "America/Toronto" }) : "");

function normalize(evt) {
  const o = (evt.data && evt.data.object) || {};
  const md = o.metadata || {};
  if (!md.supplier_id) return null;
  let status = o.status || "";
  if (evt.type === "checkout.session.completed") status = o.payment_status === "paid" || o.status === "complete" ? "active" : "incomplete";
  if (evt.type === "customer.subscription.deleted") status = "canceled";
  return {
    supplier_id: String(md.supplier_id), status, tier: md.tier || "standard",
    categories: md.categories ? String(md.categories).split(",").map((c) => c.trim()).filter(Boolean) : undefined,
    period_start: day(o.current_period_start || o.created), period_end: day(o.current_period_end || o.cancel_at || 0),
    subscription_id: typeof o.subscription === "string" ? o.subscription : o.id, stripe_event: evt.id, event_type: evt.type,
  };
}

module.exports = async function handler(req, res) {
  if (req.method !== "POST") return json(res, 405, { ok: false });
  const secret = process.env.STRIPE_WEBHOOK_SECRET, store = process.env.FEATURED_WEBHOOK_URL;
  if (!secret || !store) return json(res, 503, { ok: false, error: "payments not configured" });
  const raw = await rawBody(req);
  if (!verify(raw, req.headers["stripe-signature"], secret)) return json(res, 400, { ok: false, error: "bad signature" });
  let evt;
  try { evt = JSON.parse(raw.toString("utf8")); } catch { return json(res, 400, { ok: false }); }
  const handled = ["checkout.session.completed", "customer.subscription.created", "customer.subscription.updated", "customer.subscription.deleted"];
  if (!handled.includes(evt.type)) return json(res, 200, { ok: true, ignored: evt.type });
  const ev = normalize(evt);
  if (!ev) return json(res, 200, { ok: true, ignored: "no supplier_id metadata" });
  const r = await fetch(store, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ type: "featured_subscription", ...ev }) });
  if (!r.ok) return json(res, 502, { ok: false, error: "store " + r.status });  // Stripe retries
  return json(res, 200, { ok: true });
};
module.exports.config = { api: { bodyParser: false } };

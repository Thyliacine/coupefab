/**
 * 12-month retention for newsletter personal data (Loi 25 / privacy policy).
 * Not a Vercel Function: files starting with "_" are bundled, never routed.
 *
 * Only newsletter signup and unsubscribe records are considered. An address is
 * eligible when its most recent newsletter event is an unsubscribe at least
 * 12 months old. A later signup (a re-subscription) is treated as active and
 * is never deleted. Other inbox types (contact, quote, supplier, email…) are
 * left untouched.
 *
 * plan() and apply() return counts only — never email addresses or message bodies.
 */
const inbox = require("./_inbox");
const blob = require("./_blob");

const MONTHS = 12;

function monthsAgo(from, n) {
  const d = new Date(from.getTime());
  d.setUTCMonth(d.getUTCMonth() - n);
  return d;
}

function isUnsubscribe(msg) {
  if (!msg || msg.type !== "newsletter") return false;
  const fields = msg.fields || {};
  if (fields.type === "unsubscribe") return true;
  return /^d[ée]sabonnement|^unsubscribe\b/i.test(String(msg.subject || ""));
}

function isSignup(msg) {
  return msg && msg.type === "newsletter" && !isUnsubscribe(msg);
}

function emailOf(msg) {
  return String((msg.fields && msg.fields.email) || msg.from || "").trim().toLowerCase();
}

function when(msg) {
  const t = Date.parse(msg.createdAt || "");
  return Number.isFinite(t) ? t : 0;
}

function planFrom(messages, now) {
  const cutoff = monthsAgo(now, MONTHS).getTime();
  const byEmail = new Map();
  for (const msg of messages) {
    if (msg.type !== "newsletter") continue;
    const email = emailOf(msg);
    if (!email || !email.includes("@")) continue;
    const list = byEmail.get(email) || [];
    list.push(msg);
    byEmail.set(email, list);
  }

  const deleteIds = [];
  let emailsEligible = 0, emailsActive = 0, emailsTooRecent = 0, emailsNoUnsub = 0;
  let attachmentsToDelete = 0;

  for (const [, list] of byEmail) {
    list.sort((a, b) => when(a) - when(b));
    const last = list[list.length - 1];
    if (isSignup(last)) { emailsActive += 1; continue; }
    if (!isUnsubscribe(last)) { emailsNoUnsub += 1; continue; }
    if (when(last) > cutoff) { emailsTooRecent += 1; continue; }
    emailsEligible += 1;
    for (const msg of list) {
      deleteIds.push(msg.id);
      attachmentsToDelete += (msg.attachments || []).length;
    }
  }

  return {
    now: now.toISOString(),
    cutoff: new Date(cutoff).toISOString(),
    counts: {
      newsletterEmails: byEmail.size,
      emailsEligible,
      emailsSkippedActive: emailsActive,
      emailsSkippedTooRecent: emailsTooRecent,
      emailsSkippedNoUnsubscribe: emailsNoUnsub,
      messagesToDelete: deleteIds.length,
      attachmentsToDelete,
    },
    deleteIds,
  };
}

async function plan(now = new Date()) {
  const { deleteIds, ...rest } = planFrom(await inbox.listMessages(), now);
  return rest;
}

async function deleteOne(id) {
  const msg = await inbox.getMessage(id);
  let attachments = 0, attachmentErrors = 0;
  const seen = new Set();
  const targets = [];
  if (msg) {
    for (const att of msg.attachments || []) {
      const t = att.url || att.pathname;
      if (t) { targets.push(t); seen.add(t); }
    }
  }
  try {
    for (const f of await blob.list("inbox/attachments/" + id + "/", { limit: 200 })) {
      const t = f.url || f.pathname;
      if (t && !seen.has(t)) { targets.push(t); seen.add(t); }
    }
  } catch { /* list may 404 when there are no attachments */ }
  for (const t of targets) {
    try { await blob.del(t); attachments += 1; } catch { attachmentErrors += 1; }
  }
  const msgTarget = (msg && msg.blobUrl) || inbox.pathFor(id);
  await blob.del(msgTarget);
  return { attachments, attachmentErrors };
}

async function apply(now = new Date()) {
  const messages = await inbox.listMessages();
  const planned = planFrom(messages, now);
  let messagesDeleted = 0, messageErrors = 0, attachmentsDeleted = 0, attachmentErrors = 0;
  for (const id of planned.deleteIds) {
    try {
      const r = await deleteOne(id);
      messagesDeleted += 1;
      attachmentsDeleted += r.attachments;
      attachmentErrors += r.attachmentErrors;
    } catch {
      messageErrors += 1;
    }
  }
  return {
    now: planned.now,
    cutoff: planned.cutoff,
    counts: {
      ...planned.counts,
      messagesDeleted,
      messageErrors,
      attachmentsDeleted,
      attachmentErrors,
    },
  };
}

module.exports = { plan, apply, planFrom, isUnsubscribe, isSignup, monthsAgo, MONTHS };

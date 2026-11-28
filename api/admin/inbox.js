const auth = require("../_auth");
const inbox = require("../_inbox");

module.exports = async (req, res) => {
  if (!auth.requireAdmin(req, res, { csrf: req.method !== "GET" })) return;
  try {
    if (req.method === "GET") {
      const u = new URL(req.url, "https://coupefab.ca");
      if (u.searchParams.get("action") === "retention") {
        const retention = require("../_retention");
        return auth.json(res, 200, { ok: true, dryRun: true, ...(await retention.plan()) });
      }
      const id = u.searchParams.get("id");
      if (id) {
        const msg = await inbox.getMessage(id);
        if (!msg) return auth.json(res, 404, { ok: false, error: "Introuvable." });
        return auth.json(res, 200, { ok: true, message: msg });
      }
      const q = (u.searchParams.get("q") || "").trim().toLowerCase();
      const type = u.searchParams.get("type") || "";
      const status = u.searchParams.get("status") || "";
      const format = u.searchParams.get("format") || "";
      const msgs = (await inbox.listMessages()).filter((m) => inbox.matchQuery(m, q, type, status));
      if (format === "csv") {
        const csv = inbox.toCSV(msgs);
        res.statusCode = 200;
        res.setHeader("content-type", "text/csv; charset=utf-8");
        res.setHeader("content-disposition", "attachment; filename=\"coupefab-inbox.csv\"");
        res.setHeader("cache-control", "no-store");
        res.setHeader("x-robots-tag", "noindex");
        res.end(csv);
        return;
      }
      const summaries = msgs.map(inbox.summaryOf);
      const counts = { all: 0, new: 0, read: 0, archived: 0 };
      for (const m of await inbox.listMessages()) {
        counts.all += 1;
        if (counts[m.status] != null) counts[m.status] += 1;
      }
      return auth.json(res, 200, { ok: true, count: summaries.length, counts, messages: summaries });
    }
    if (req.method === "POST") {
      let body = {};
      try { body = JSON.parse(await auth.readBody(req, 20_000) || "{}") || {}; } catch { return auth.json(res, 400, { ok: false, error: "JSON invalide." }); }
      if (body.action !== "retention") return auth.json(res, 400, { ok: false, error: "Action inconnue." });
      const retention = require("../_retention");
      if (body.delete === true) return auth.json(res, 200, { ok: true, dryRun: false, ...(await retention.apply()) });
      return auth.json(res, 200, { ok: true, dryRun: true, ...(await retention.plan()) });
    }
    if (req.method === "PATCH") {
      const raw = await auth.readBody(req, 20_000);
      let body = {};
      try { body = JSON.parse(raw) || {}; } catch { return auth.json(res, 400, { ok: false, error: "JSON invalide." }); }
      if (!body.id || !body.status) return auth.json(res, 400, { ok: false, error: "id et status requis." });
      const msg = await inbox.updateStatus(body.id, body.status);
      if (!msg) return auth.json(res, 404, { ok: false, error: "Introuvable." });
      return auth.json(res, 200, { ok: true, message: msg });
    }
    return auth.json(res, 405, { ok: false, error: "Méthode refusée." });
  } catch (e) {
    console.error("admin inbox failed", e && e.message);
    return auth.json(res, 500, { ok: false, error: "Erreur de stockage." });
  }
};

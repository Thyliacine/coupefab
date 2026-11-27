const fs = require("fs");
const path = require("path");
const auth = require("../_auth");
const blob = require("../_blob");

const PATH = "admin/settings.json";
const FLAG_KEYS = ["featured_suppliers", "affiliate_links", "digest_sponsor", "quote_requests", "advertise_page"];

function seed() {
  const candidates = [
    path.join(process.cwd(), "admin/settings-seed.json"),
    path.join(process.cwd(), "public/admin/settings-seed.json"),
    path.join(__dirname, "../../admin/settings-seed.json"),
  ];
  for (const p of candidates) {
    try { return JSON.parse(fs.readFileSync(p, "utf8")); } catch { /* next */ }
  }
  return { flags: {}, sponsors: [], affiliates: [], partners: [], featured: [] };
}

async function load() {
  try { return await blob.getJSON(PATH); } catch { return seed(); }
}

module.exports = async (req, res) => {
  if (!auth.requireAdmin(req, res, { csrf: req.method !== "GET" })) return;
  try {
    if (req.method === "GET") {
      const data = await load();
      data.fromSeed = !data.savedAt;
      data.liveSiteNote = "Le site public lit encore les fichiers du dépôt (config/*.json, content/shops.json). Enregistrer ici conserve une copie dans le stockage de l’admin ; un rebuild est requis pour publier les interrupteurs, commanditaires, affiliés ou partenaires.";
      return auth.json(res, 200, { ok: true, settings: data });
    }
    if (req.method === "PUT") {
      const body = JSON.parse(await auth.readBody(req, 400_000) || "{}");
      const cur = await load();
      const flags = {};
      for (const k of FLAG_KEYS) flags[k] = Boolean((body.flags || {})[k]);
      const next = {
        flags,
        sponsors: Array.isArray(body.sponsors) ? body.sponsors : (cur.sponsors || []),
        affiliates: Array.isArray(body.affiliates) ? body.affiliates : (cur.affiliates || []),
        partners: Array.isArray(body.partners) ? body.partners : (cur.partners || []),
        featured: cur.featured || [],
        savedAt: new Date().toISOString(),
      };
      await blob.putJSON(PATH, next);
      return auth.json(res, 200, { ok: true, settings: next });
    }
    return auth.json(res, 405, { ok: false, error: "Méthode refusée." });
  } catch (e) {
    console.error("settings failed", e && e.message);
    return auth.json(res, 500, { ok: false, error: "Impossible d’enregistrer les réglages." });
  }
};

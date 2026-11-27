const auth = require("../_auth");
module.exports = async (req, res) => {
  if (req.method !== "POST") return auth.json(res, 405, { ok: false, error: "POST only" });
  return auth.handleLogout(req, res);
};

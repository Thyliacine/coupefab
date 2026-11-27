const auth = require("../_auth");
module.exports = async (req, res) => auth.handleLogin(req, res);

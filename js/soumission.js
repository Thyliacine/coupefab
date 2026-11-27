/* CoupeFab — quote request form (/soumission/, /en/quote/) -> /api/quote-request. Vanilla JS. */
(function () {
  "use strict";
  var app = document.getElementById("rv-quote-app");
  var f = document.getElementById("rv-quote");
  if (!app || !f) return;
  var FR = app.getAttribute("data-lang") !== "en";
  var T = function (a, b) { return FR ? a : b; };
  var st = f.querySelector(".rv-status");
  f.t0.value = String(Date.now());
  function say(msg, ok) { st.textContent = msg; st.className = "rv-status " + (ok ? "is-ok" : "is-err"); if (window.cfFlash) window.cfFlash(st); }
  f.addEventListener("submit", function (e) {
    e.preventDefault();
    if (!f.checkValidity()) { f.reportValidity(); return; }
    if (!f.file_url.value.trim() && !f.description.value.trim()) { say(T("Ajoutez un lien vers vos dessins ou une description.", "Add a link to your drawings or a description."), false); f.description.focus(); return; }
    var data = {};
    ["process", "material", "thickness", "qty", "file_url", "description", "region", "deadline", "name", "company", "email", "phone", "website", "t0"].forEach(function (k) { data[k] = f[k].value.trim(); });
    data.consent = f.consent.checked; data.lang = FR ? "fr" : "en";
    var btn = f.querySelector("button[type=submit]"); btn.disabled = true;
    say(T("Envoi…", "Sending…"), true);
    fetch("/api/quote-request", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(data) })
      .then(function (r) { return r.json().catch(function () { return { ok: false }; }).then(function (j) { return { s: r.status, j: j }; }); })
      .then(function (x) {
        if (x.j.ok) { say(T("Merci! Votre demande est reçue. On vous écrit d’ici deux jours ouvrables.", "Thanks! Your request is in. We’ll write back within two business days."), true); f.reset(); f.t0.value = String(Date.now()); }
        else say(x.j.error || T("Envoi impossible pour le moment. Réessayez plus tard.", "Couldn’t send right now. Please try again later."), false);
      })
      .catch(function () { say(T("Pas de connexion. Réessayez.", "No connection. Please try again."), false); })
      .then(function () { btn.disabled = false; });
  });
})();

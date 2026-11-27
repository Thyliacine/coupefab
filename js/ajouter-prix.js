/* CoupeFab — low-friction "Add your prices" form → /api/supplier-submit. */
(function () {
  "use strict";
  var sf = document.getElementById("sp-form");
  if (!sf) return;
  var root = document.getElementById("ap-app") || document.getElementById("sp-app");
  var FR = !root || root.getAttribute("data-lang") !== "en";
  var T = function (fr, en) { return FR ? fr : en; };
  var status = sf.querySelector(".sp-status");
  var MAX = 2 * 1024 * 1024;
  function readFile(f) {
    return new Promise(function (res, rej) {
      if (!f) return res(null);
      if (f.size > MAX) return rej(new Error(T("Fichier trop lourd (2 Mo max). Envoyez plutôt un lien.", "File too large (2 MB max). Send a link instead.")));
      var r = new FileReader();
      r.onload = function () { res({ name: f.name, type: f.type || "application/octet-stream", size: f.size, data: String(r.result).split(",")[1] || "" }); };
      r.onerror = function () { rej(new Error(T("Lecture du fichier impossible.", "Could not read the file."))); };
      r.readAsDataURL(f);
    });
  }
  sf.addEventListener("submit", function (e) {
    e.preventDefault();
    status.className = "sp-status";
    var email = sf.email.value.trim(), company = sf.company.value.trim();
    var link = sf.price_url.value.trim(), hasFile = !!(sf.file.files && sf.file.files[0]);
    var msg = sf.message.value.trim();
    if (!company || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      status.textContent = T("Indiquez le nom de l’entreprise et un courriel valide.", "Enter the company name and a valid email.");
      status.classList.add("is-err"); return;
    }
    if (!link && !hasFile && !msg) {
      status.textContent = T("Ajoutez un lien, un fichier, ou un court message.", "Add a link, a file, or a short message.");
      status.classList.add("is-err"); return;
    }
    if (!sf.consent.checked) {
      status.textContent = T("Cochez la case d’autorisation pour continuer.", "Tick the authorization box to continue.");
      status.classList.add("is-err"); return;
    }
    var btn = sf.querySelector("button[type=submit]");
    btn.disabled = true; status.textContent = T("Envoi…", "Sending…");
    readFile(sf.file.files && sf.file.files[0]).then(function (file) {
      return fetch("/api/supplier-submit", {
        method: "POST", headers: { "content-type": "application/json" },
        body: JSON.stringify({
          company: company, email: email, site: sf.site.value.trim(), price_url: link,
          message: msg, website: sf.website.value, consent: true, lang: FR ? "fr" : "en", file: file
        })
      });
    }).then(function (r) { return r.json().then(function (j) { if (!r.ok || !j.ok) throw new Error(j.error || "HTTP " + r.status); return j; }); })
      .then(function () {
        sf.reset();
        status.textContent = T("Merci! Votre soumission est arrivée dans notre boîte. Nous vous écrirons avant toute publication.", "Thanks! Your submission landed in our inbox. We’ll email you before anything is published.");
        status.classList.add("is-ok");
      })
      .catch(function (err) {
        status.textContent = (err && err.message && err.message.length < 140 ? err.message : T("Envoi impossible pour le moment. Réessayez plus tard.", "Could not send right now. Please try again later."));
        status.classList.add("is-err");
      })
      .then(function () { btn.disabled = false; });
  });
})();

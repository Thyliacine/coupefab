/* CoupeFab — supplier directory: in-place filters + "Add your prices" form (vanilla JS). */
(function () {
  "use strict";
  var app = document.getElementById("sp-app");
  if (!app) return;
  var FR = app.getAttribute("data-lang") !== "en";
  var T = function (fr, en) { return FR ? fr : en; };
  var form = document.getElementById("sp-filters");
  var cards = [].slice.call(app.querySelectorAll(".sp-card"));
  var count = document.getElementById("sp-count"), empty = document.getElementById("sp-empty");
  function norm(s) { return String(s || "").toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, ""); }
  cards.forEach(function (c) { c._n = norm(c.getAttribute("data-name")); });
  function apply() {
    var q = norm(form.q.value.trim()), prov = form.prov.value, cat = form.cat.value, pub = form.pub.value, lang = form.lang.value, n = 0;
    cards.forEach(function (c) {
      var ok = (!q || c._n.indexOf(q) >= 0) &&
        (!prov || (" " + c.getAttribute("data-prov") + " ").indexOf(" " + prov + " ") >= 0) &&
        (!cat || (" " + c.getAttribute("data-cats") + " ").indexOf(" " + cat + " ") >= 0) &&
        (!pub || c.getAttribute("data-pub") === pub) &&
        (!lang || (" " + c.getAttribute("data-lang") + " ").indexOf(" " + lang + " ") >= 0);
      c.hidden = !ok; if (ok) n++;
    });
    count.textContent = n + T(n > 1 ? " fournisseurs" : " fournisseur", n === 1 ? " supplier" : " suppliers");
    empty.hidden = n > 0;
  }
  form.addEventListener("input", apply);
  form.addEventListener("change", apply);
  form.querySelector("[data-reset]").addEventListener("click", function () { form.reset(); apply(); });

  /* ---------- submission ---------- */
  var sf = document.getElementById("sp-form");
  if (!sf) return;
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
    if (!company || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { status.textContent = T("Indiquez le nom de l’entreprise et un courriel valide.", "Enter the company name and a valid email."); status.classList.add("is-err"); return; }
    if (!sf.price_url.value.trim() && !(sf.file.files && sf.file.files[0])) { status.textContent = T("Ajoutez un lien vers vos prix ou un fichier.", "Add a link to your prices or a file."); status.classList.add("is-err"); return; }
    if (!sf.consent.checked) { status.textContent = T("Cochez la case d’autorisation pour continuer.", "Tick the authorization box to continue."); status.classList.add("is-err"); return; }
    var btn = sf.querySelector("button[type=submit]");
    btn.disabled = true; status.textContent = T("Envoi…", "Sending…");
    readFile(sf.file.files && sf.file.files[0]).then(function (file) {
      return fetch("/api/supplier-submit", {
        method: "POST", headers: { "content-type": "application/json" },
        body: JSON.stringify({ company: company, email: email, site: sf.site.value.trim(), price_url: sf.price_url.value.trim(),
          message: sf.message.value.trim(), website: sf.website.value, consent: true, lang: FR ? "fr" : "en", file: file })
      });
    }).then(function (r) { return r.json().then(function (j) { if (!r.ok || !j.ok) throw new Error(j.error || "HTTP " + r.status); return j; }); })
      .then(function () {
        sf.reset();
        status.textContent = T("Merci! Votre soumission est en attente de vérification. Nous vous écrirons avant toute publication.", "Thanks! Your submission is waiting for review. We’ll email you before anything is published.");
        status.classList.add("is-ok");
      })
      .catch(function (err) { status.textContent = (err && err.message && err.message.length < 140 ? err.message : T("Envoi impossible pour le moment. Réessayez plus tard.", "Could not send right now. Please try again later.")); status.classList.add("is-err"); })
      .then(function () { btn.disabled = false; });
  });
})();

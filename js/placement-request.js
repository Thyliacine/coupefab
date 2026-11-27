/* CoupeFab — placement request form → /api/supplier-submit (action "placement"; no extra Vercel function). */
(function () {
  "use strict";
  var form = document.getElementById("cf-request-form");
  if (!form) return;
  var FR = (form.getAttribute("data-lang") || "fr") !== "en";
  var T = function (fr, en) { return FR ? fr : en; };
  var status = form.querySelector(".cf-request-status, .sp-status, .rv-status, [role=status]");
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (status) { status.className = status.className.replace(/\bis-ok\b|\bis-err\b/g, "").trim(); }
    var company = form.company.value.trim();
    var contact = form.contact.value.trim();
    var email = form.email.value.trim();
    var promote = form.promote.value.trim();
    var budget = form.budget.value;
    var message = form.message.value.trim();
    if (!company || !contact || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || !promote) {
      if (status) {
        status.textContent = T("Indiquez l’entreprise, le contact, un courriel valide et ce que vous souhaitez promouvoir.", "Enter the company, a contact name, a valid email and what you want to promote.");
        status.classList.add("is-err");
      }
      return;
    }
    if (form.website && form.website.value) { if (status) { status.textContent = T("Merci!", "Thanks!"); status.classList.add("is-ok"); } return; }
    var btn = form.querySelector("button[type=submit]");
    btn.disabled = true;
    if (status) status.textContent = T("Envoi…", "Sending…");
    fetch("/api/supplier-submit", {
      method: "POST", headers: { "content-type": "application/json" },
      body: JSON.stringify({
        action: "placement",
        company: company, contact: contact, email: email, promote: promote,
        budget: budget, message: message, lang: FR ? "fr" : "en",
        website: form.website ? form.website.value : ""
      })
    }).then(function (r) { return r.json().then(function (j) { if (!r.ok || !j.ok) throw new Error(j.error || "HTTP " + r.status); return j; }); })
      .then(function () {
        form.reset();
        if (status) {
          status.textContent = T("Merci! Votre demande est arrivée. Nous vous écrirons pour en discuter. Aucun tarif n’est affiché pour le moment.", "Thanks! Your request has arrived. We’ll email you to talk it over. No rates are listed for now.");
          status.classList.add("is-ok");
        }
      })
      .catch(function () {
        if (status) {
          status.textContent = T("Envoi impossible pour le moment. Réessayez plus tard ou écrivez à info@coupefab.ca.", "Could not send right now. Please try again later or write to info@coupefab.ca.");
          status.classList.add("is-err");
        }
      })
      .then(function () { btn.disabled = false; });
  });
})();

/* CoupeFab — brochure / price-list upload. Direct private Blob upload (10 MB), inline fallback (2 MB). */
(function () {
  "use strict";
  var app = document.getElementById("bro-app");
  var form = document.getElementById("bro-form");
  if (!app || !form) return;
  var en = app.getAttribute("data-lang") === "en";
  var T = function (fr, e) { return en ? e : fr; };
  var MAX = 10 * 1024 * 1024, INLINE_MAX = 2 * 1024 * 1024;
  var EXT = { pdf: "application/pdf", jpg: "image/jpeg", jpeg: "image/jpeg", png: "image/png", csv: "text/csv",
    xlsx: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    docx: "application/vnd.openxmlformats-officedocument.wordprocessingml.document" };
  var status = form.querySelector(".bro-status");
  var info = form.querySelector(".bro-file-info");
  var bar = form.querySelector(".bro-progress");
  var btn = form.querySelector("button[type=submit]");

  function ext(n) { var m = /\.([a-z0-9]+)$/i.exec(n || ""); return m ? m[1].toLowerCase() : ""; }
  function mb(n) { return (n / 1048576).toFixed(n < 1048576 ? 2 : 1).replace(".", en ? "." : ",") + (en ? " MB" : " Mo"); }
  function say(t, cls) { status.textContent = t; status.className = "bro-status" + (cls ? " " + cls : ""); }
  function fileProblem(f) {
    if (!f) return T("Choisissez un fichier.", "Choose a file.");
    if (!EXT[ext(f.name)]) return T("Formats acceptés : PDF, JPG, PNG, XLSX, CSV, DOCX.", "Accepted formats: PDF, JPG, PNG, XLSX, CSV, DOCX.");
    if (!f.size) return T("Ce fichier est vide.", "This file is empty.");
    if (f.size > MAX) return T("Fichier trop lourd (" + mb(f.size) + "). Maximum 10 Mo.", "File too large (" + mb(f.size) + "). 10 MB max.");
    return "";
  }

  form.file.addEventListener("change", function () {
    var f = form.file.files && form.file.files[0];
    var p = fileProblem(f);
    info.textContent = f ? (f.name + " — " + mb(f.size) + (p ? " · " + p : "")) : "";
    info.style.color = p ? "#a3261b" : "";
  });

  function post(body) {
    return fetch("/api/supplier-submit", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(body) })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { if (!r.ok || !j.ok) throw new Error(j.error || "HTTP " + r.status); return j; }); });
  }

  function putBlob(t, file) {
    return new Promise(function (resolve, reject) {
      var x = new XMLHttpRequest();
      x.open("PUT", "https://vercel.com/api/blob/?pathname=" + encodeURIComponent(t.pathname));
      x.setRequestHeader("authorization", "Bearer " + t.token);
      x.setRequestHeader("x-api-version", "13");
      x.setRequestHeader("x-vercel-blob-store-id", t.storeId);
      x.setRequestHeader("x-vercel-blob-access", "private");
      x.setRequestHeader("x-content-type", t.contentType);
      x.upload.onprogress = function (e) { if (e.lengthComputable) bar.value = Math.round((e.loaded / e.total) * 100); };
      x.onload = function () { if (x.status >= 200 && x.status < 300) resolve(); else reject(new Error("blob " + x.status + " " + (x.responseText || "").slice(0, 200))); };
      x.onerror = function () { reject(new Error("network")); };
      x.send(file);
    });
  }

  function readB64(file) {
    return new Promise(function (resolve, reject) {
      var r = new FileReader();
      r.onload = function () { resolve(String(r.result).split(",")[1] || ""); };
      r.onerror = reject;
      r.readAsDataURL(file);
    });
  }

  form.addEventListener("submit", function (ev) {
    ev.preventDefault();
    var f = form.file.files && form.file.files[0];
    var base = {
      lang: en ? "en" : "fr", page: location.pathname,
      company: form.company.value.trim(), contact: form.contact.value.trim(), email: form.email.value.trim(),
      phone: form.phone.value.trim(), message: form.message.value.trim(), website: form.website.value, consent: form.consent.checked
    };
    if (!base.company || !base.contact) return say(T("Indiquez l’entreprise et le nom de la personne-ressource.", "Enter the company and contact name."), "is-err");
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(base.email)) return say(T("Courriel invalide.", "Invalid email."), "is-err");
    var p = fileProblem(f); if (p) return say(p, "is-err");
    if (!base.consent) return say(T("Cochez la case d’autorisation pour continuer.", "Tick the authorization box to continue."), "is-err");

    btn.disabled = true; bar.hidden = false; bar.value = 0;
    say(T("Préparation de l’envoi…", "Preparing upload…"));
    var meta = { name: f.name, size: f.size, type: EXT[ext(f.name)] };
    post(Object.assign({ action: "brochure-token", file: meta }, base))
      .then(function (t) {
        if (t.skip) return { ok: true };
        say(T("Envoi du fichier…", "Uploading file…"));
        return putBlob(t, f).then(function () {
          say(T("Vérification…", "Checking…"));
          return post(Object.assign({ action: "brochure", id: t.id, pathname: t.pathname, exp: t.exp, sig: t.sig }, base));
        }, function (err) {
          if (f.size > INLINE_MAX) throw new Error(T("L’envoi direct a échoué (pare-feu ou bloqueur?). Réessayez ou écrivez à info@coupefab.ca.", "Direct upload failed (firewall or blocker?). Try again or email info@coupefab.ca."));
          return readB64(f).then(function (data) { return post(Object.assign({ action: "brochure", file: { name: f.name, data: data } }, base)); });
        });
      })
      .then(function () {
        bar.value = 100;
        form.reset(); info.textContent = "";
        say(T("Merci! Votre fichier est bien reçu. Nous l’examinons et vous écrivons sous peu.", "Thank you! Your file was received. We’ll review it and get back to you shortly."), "is-ok");
      })
      .catch(function (e) { say(e.message || T("Erreur d’envoi.", "Upload error."), "is-err"); })
      .then(function () { btn.disabled = false; setTimeout(function () { bar.hidden = true; }, 1200); });
  });
})();

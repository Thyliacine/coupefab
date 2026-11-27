(function () {
  const $ = (id) => document.getElementById(id);
  const loginBox = $("login"), app = $("app");
  let currentId = null, settingsCache = null, outbound = false;

  function showErr(el, msg) { el.hidden = !msg; el.textContent = msg || ""; }

  // Visible fallback: never leave a blank page. Inline styles + neutral id so
  // ad-blocker cosmetic lists (which hide many "ad-*" classes) cannot hide it.
  function fatal(msg, detail) {
    let box = document.getElementById("cfa-fatal");
    if (!box) {
      box = document.createElement("div");
      box.id = "cfa-fatal";
      box.setAttribute("role", "alert");
      box.style.cssText = "position:fixed;left:50%;top:1rem;transform:translateX(-50%);z-index:2147483647;max-width:40rem;width:calc(100% - 2rem);box-sizing:border-box;padding:1rem 1.2rem;background:#fff4f2;color:#7a1c12;border:2px solid #a3261b;border-radius:10px;font:15px/1.45 system-ui,'Segoe UI',sans-serif;box-shadow:0 8px 28px rgba(0,0,0,.15);display:block;visibility:visible;opacity:1";
      document.body.appendChild(box);
    }
    box.innerHTML = "";
    const p = document.createElement("p"); p.style.cssText = "margin:0 0 .5rem;font-weight:650"; p.textContent = msg; box.appendChild(p);
    if (detail) { const d = document.createElement("p"); d.style.cssText = "margin:0 0 .6rem;font:12px/1.4 ui-monospace,monospace;color:#5a1a12;word-break:break-word"; d.textContent = String(detail).slice(0, 400); box.appendChild(d); }
    const r = document.createElement("button"); r.type = "button"; r.textContent = "Recharger la page";
    r.style.cssText = "min-height:40px;padding:0 1rem;border:0;border-radius:8px;background:#c2410c;color:#fff;font:inherit;font-weight:650;cursor:pointer";
    r.addEventListener("click", () => location.reload());
    box.appendChild(r);
  }
  window.addEventListener("error", (e) => fatal("Erreur dans la page admin.", e && (e.message || e.error)));
  window.addEventListener("unhandledrejection", (e) => fatal("Erreur dans la page admin.", e && e.reason && (e.reason.message || e.reason)));

  // An extension (ad blocker) can hide the panel with CSS; detect it and say so.
  function checkVisible(el, what) {
    setTimeout(() => {
      if (!el || el.hidden) return;
      const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
      if (r.height < 20 || cs.display === "none" || cs.visibility === "hidden" || Number(cs.opacity) === 0) {
        fatal(what + " par une extension du navigateur (bloqueur de pub ?). Désactivez-la pour coupefab.ca, puis rechargez.");
      }
    }, 300);
  }

  async function api(url, opts) {
    const r = await fetch(url, { credentials: "same-origin", headers: { accept: "application/json", ...(opts && opts.body ? { "content-type": "application/json" } : {}) }, ...opts });
    const data = await r.json().catch(() => ({}));
    if (r.status === 401) throw Object.assign(new Error("auth"), { auth: true, data });
    if (!r.ok) throw Object.assign(new Error((data && data.error) || r.statusText), { status: r.status, data });
    return data;
  }

  function showLogin() {
    loginBox.hidden = false; app.hidden = true;
    checkVisible(loginBox, "Le formulaire de connexion est masqué");
  }

  async function checkSession() {
    let me;
    try {
      me = await api("/api/admin/me");
    } catch (e) {
      showLogin();
      if (!e.auth) showErr($("login-err"), (e.data && e.data.error) || "Le serveur admin ne répond pas. Réessayez dans un instant.");
      return false;
    }
    outbound = !!me.outbound;
    loginBox.hidden = true; app.hidden = false;
    checkVisible(app, "La boîte de réception est masquée");
    try {
      await loadInbox();
    } catch (e) {
      if (e.auth) { showLogin(); return false; }
      $("counts").textContent = "";
      $("list").innerHTML = "";
      const li = document.createElement("li"); li.className = "cfa-err";
      li.textContent = "Impossible de charger la boîte : " + ((e.data && e.data.error) || e.message || "erreur inconnue") + ". Rechargez la page.";
      $("list").appendChild(li);
    }
    return true;
  }

  $("login-form").addEventListener("submit", async (ev) => {
    ev.preventDefault();
    showErr($("login-err"), "");
    try {
      await api("/api/admin/login", { method: "POST", body: JSON.stringify({ password: $("password").value }) });
      $("password").value = "";
      await checkSession();
    } catch (e) {
      showErr($("login-err"), (e.data && e.data.error) || "Connexion impossible.");
    }
  });

  $("logout").addEventListener("click", async () => {
    try { await api("/api/admin/logout", { method: "POST", body: "{}" }); } catch (_) {}
    currentId = null; loginBox.hidden = false; app.hidden = true;
  });

  document.querySelectorAll(".cfa-tabs button").forEach((btn) => {
    btn.addEventListener("click", async () => {
      document.querySelectorAll(".cfa-tabs button").forEach((b) => b.setAttribute("aria-selected", b === btn ? "true" : "false"));
      $("tab-inbox").hidden = btn.dataset.tab !== "inbox";
      $("tab-settings").hidden = btn.dataset.tab !== "settings";
      if (btn.dataset.tab === "settings") await loadSettings();
    });
  });

  const typeLabel = { email: "Courriel", quote: "Soumission", newsletter: "Infolettre", contact: "Message", supplier: "Fournisseur", placement: "Annonce", brochure: "Brochure" };
  const statusLabel = { new: "Nouveau", read: "Lu", archived: "Archivé" };

  function inboxQuery() {
    const u = new URL("/api/admin/inbox", location.origin);
    const q = $("q").value.trim(), t = $("filter-type").value, s = $("filter-status").value;
    if (q) u.searchParams.set("q", q);
    if (t) u.searchParams.set("type", t);
    if (s) u.searchParams.set("status", s);
    return u;
  }

  async function loadInbox() {
    const data = await api(inboxQuery().toString());
    $("csv").href = inboxQuery().toString() + (inboxQuery().search ? "&" : "?") + "format=csv";
    const c = data.counts || {};
    $("counts").textContent = (c.new || 0) + " nouveau(x) · " + (c.read || 0) + " lu(s) · " + (c.archived || 0) + " archivé(s) · " + (data.count || 0) + " affiché(s)";
    const ul = $("list");
    ul.innerHTML = "";
    if (!data.messages || !data.messages.length) {
      ul.innerHTML = '<li class="cfa-empty">Aucun message.</li>';
      return;
    }
    for (const m of data.messages) {
      const li = document.createElement("li");
      const b = document.createElement("button");
      b.type = "button";
      if (m.id === currentId) b.className = "is-on";
      b.innerHTML = '<div class="cfa-from"><span></span><span class="cfa-pill ' + (m.status === "new" ? "cfa-pill-new" : "") + '"></span></div><div class="cfa-sub"></div>';
      b.querySelector(".cfa-from span").textContent = m.fromName || m.from || "(sans nom)";
      b.querySelector(".cfa-pill").textContent = (typeLabel[m.type] || m.type) + " · " + (statusLabel[m.status] || m.status);
      b.querySelector(".cfa-sub").textContent = (m.subject || m.preview || "") + (m.createdAt ? " — " + m.createdAt.replace("T", " ").slice(0, 16) : "");
      b.addEventListener("click", () => openMessage(m.id).catch((e) => {
        if (e.auth) return showLogin();
        const d = $("detail"); d.innerHTML = "";
        const p = document.createElement("p"); p.className = "cfa-err";
        p.textContent = "Impossible d’ouvrir ce message : " + ((e.data && e.data.error) || e.message || "erreur inconnue");
        d.appendChild(p);
      }));
      li.appendChild(b); ul.appendChild(li);
    }
  }

  ["q", "filter-type", "filter-status"].forEach((id) => {
    $(id).addEventListener("input", () => { clearTimeout($(id)._t); $(id)._t = setTimeout(loadInbox, 200); });
    $(id).addEventListener("change", loadInbox);
  });

  async function openMessage(id) {
    currentId = id;
    document.querySelectorAll(".cfa-list button").forEach((b, i) => {});
    const data = await api("/api/admin/inbox?id=" + encodeURIComponent(id));
    const m = data.message;
    if (m.status === "new") {
      try { await api("/api/admin/inbox", { method: "PATCH", body: JSON.stringify({ id, status: "read" }) }); m.status = "read"; } catch (_) {}
    }
    renderDetail(m);
    await loadInbox();
  }

  function fieldRows(fields) {
    if (!fields || typeof fields !== "object") return "";
    const skip = new Set(["consent", "file"]);
    let html = '<dl class="cfa-fields">';
    for (const [k, v] of Object.entries(fields)) {
      if (skip.has(k) || v == null || v === "") continue;
      const val = Array.isArray(v) ? v.join(", ") : (typeof v === "object" ? JSON.stringify(v) : String(v));
      html += "<div><dt></dt><dd></dd></div>";
    }
    html += "</dl>";
    const wrap = document.createElement("div"); wrap.innerHTML = html;
    const rows = wrap.querySelectorAll("div");
    let i = 0;
    for (const [k, v] of Object.entries(fields)) {
      if (skip.has(k) || v == null || v === "") continue;
      const val = Array.isArray(v) ? v.join(", ") : (typeof v === "object" ? JSON.stringify(v) : String(v));
      rows[i].querySelector("dt").textContent = k;
      rows[i].querySelector("dd").textContent = val;
      i += 1;
    }
    return wrap.innerHTML;
  }

  function renderDetail(m) {
    const el = $("detail");
    el.innerHTML = "";
    const h = document.createElement("h2");
    h.textContent = m.subject || "(sans objet)";
    const meta = document.createElement("p");
    meta.className = "cfa-meta";
    meta.textContent = (typeLabel[m.type] || m.type) + " · " + (m.fromName ? m.fromName + " <" + m.from + ">" : m.from) + (m.to ? " → " + m.to : "") + (m.createdAt ? " · " + m.createdAt.replace("T", " ").slice(0, 19) : "");
    el.appendChild(h); el.appendChild(meta);
    const actions = document.createElement("div");
    actions.className = "cfa-actions";
    for (const st of ["new", "read", "archived"]) {
      const b = document.createElement("button");
      b.type = "button"; b.className = "cfa-btn" + (m.status === st ? "" : " cfa-btn-ghost");
      b.textContent = "Marquer " + statusLabel[st].toLowerCase();
      b.addEventListener("click", async () => {
        await api("/api/admin/inbox", { method: "PATCH", body: JSON.stringify({ id: m.id, status: st }) });
        const fresh = await api("/api/admin/inbox?id=" + encodeURIComponent(m.id));
        renderDetail(fresh.message); await loadInbox();
      });
      actions.appendChild(b);
    }
    el.appendChild(actions);
    if (m.fields) {
      const box = document.createElement("div");
      box.innerHTML = fieldRows(m.fields);
      el.appendChild(box);
    }
    if (m.text) {
      const pre = document.createElement("div"); pre.className = "cfa-body"; pre.textContent = m.text; el.appendChild(pre);
    } else if (m.html) {
      const pre = document.createElement("div"); pre.className = "cfa-body"; pre.textContent = m.html.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim(); el.appendChild(pre);
    }
    if (m.attachments && m.attachments.length) {
      const ul = document.createElement("ul"); ul.className = "cfa-atts";
      for (const a of m.attachments) {
        const li = document.createElement("li");
        const link = document.createElement("a");
        link.href = "/api/admin/attachment?id=" + encodeURIComponent(m.id) + "&name=" + encodeURIComponent(a.name);
        link.textContent = a.name + (a.size ? " (" + Math.round(a.size / 1024) + " Ko)" : "");
        li.appendChild(link); ul.appendChild(li);
      }
      el.appendChild(ul);
    }
    if (m.replies && m.replies.length) {
      const ul = document.createElement("ul"); ul.className = "cfa-thread";
      for (const r of m.replies) {
        const li = document.createElement("li");
        li.innerHTML = "<b></b> <span class='cfa-meta'></span><div class='cfa-body'></div>";
        li.querySelector("b").textContent = "Réponse à " + (r.to || "");
        li.querySelector("span").textContent = r.at ? r.at.replace("T", " ").slice(0, 19) : "";
        li.querySelector("div").textContent = r.text || "";
        ul.appendChild(li);
      }
      el.appendChild(ul);
    }
    const form = document.createElement("form");
    form.className = "cfa-reply";
    form.innerHTML = '<h3>Répondre</h3><label><span>Destinataire</span><input type="email" name="to" required></label><label><span>Objet</span><input type="text" name="subject"></label><label><span>Message</span><textarea name="text" required></textarea></label><button type="submit" class="cfa-btn">Envoyer</button><p class="cfa-hint" id="reply-hint"></p><p class="cfa-err" id="reply-err" hidden></p>';
    form.to.value = m.from || "";
    form.subject.value = m.subject && !/^re:/i.test(m.subject) ? "Re: " + m.subject : (m.subject || "CoupeFab");
    if (!outbound) {
      form.querySelector("button").disabled = true;
      form.querySelector("#reply-hint").textContent = "L’envoi n’est pas encore branché. Créez un compte Resend gratuit, ajoutez RESEND_API_KEY, puis les enregistrements DNS indiqués dans le rapport. Rien ne part tant que vous n’appuyez pas sur Envoyer.";
    } else {
      form.querySelector("#reply-hint").textContent = "Envoyé seulement lorsque vous cliquez sur Envoyer. Aucune réponse automatique.";
    }
    form.addEventListener("submit", async (ev) => {
      ev.preventDefault();
      const err = form.querySelector("#reply-err"); showErr(err, "");
      try {
        await api("/api/admin/reply", { method: "POST", body: JSON.stringify({ id: m.id, to: form.to.value, subject: form.subject.value, text: form.text.value }) });
        const fresh = await api("/api/admin/inbox?id=" + encodeURIComponent(m.id));
        renderDetail(fresh.message); await loadInbox();
      } catch (e) {
        showErr(err, (e.data && e.data.error) || "Envoi impossible.");
      }
    });
    el.appendChild(form);
  }

  const FLAG_LABELS = {
    featured_suppliers: ["Fournisseurs en vedette", "Bloc « En vedette » (payé) en haut des fournisseurs, prix, pièces, outillage"],
    affiliate_links: ["Liens affiliés", "Encadré « Où acheter » + texte de divulgation"],
    digest_sponsor: ["Commandite de l’infolettre", "Encadré « Commandité » dans le numéro"],
    quote_requests: ["Demandes de soumission", "Page /soumission/ publiée et liens dans le pied de page"],
    advertise_page: ["Page « Annoncer »", "Page /annoncer/ publiée (tarifs encore « à déterminer »)"]
  };
  const SP_FIELDS = ["id", "name", "logo", "url", "line1_fr", "line2_fr", "line1_en", "line2_en", "start", "end"];
  const AFF_FIELDS = ["key", "merchant", "label_fr", "label_en", "url"];

  async function loadSettings() {
    const data = await api("/api/admin/settings");
    settingsCache = data.settings;
    $("settings-note").textContent = data.settings.liveSiteNote || "";
    const flags = $("flags"); flags.innerHTML = "";
    for (const [k, lab] of Object.entries(FLAG_LABELS)) {
      const l = document.createElement("label");
      l.className = "row";
      l.innerHTML = '<input type="checkbox"> <b></b> <small></small>';
      l.querySelector("input").name = "flag"; l.querySelector("input").value = k;
      l.querySelector("input").checked = !!(settingsCache.flags && settingsCache.flags[k]);
      l.querySelector("b").textContent = lab[0];
      l.querySelector("small").textContent = lab[1];
      flags.appendChild(l);
    }
    const partners = $("partners"); partners.innerHTML = "";
    for (const p of settingsCache.partners || []) {
      const l = document.createElement("label");
      l.innerHTML = '<input type="checkbox"> <span></span>';
      l.querySelector("input").value = p.id; l.querySelector("input").checked = !!p.partner;
      l.querySelector("span").textContent = p.name + (p.city ? " (" + p.city + ")" : "");
      partners.appendChild(l);
    }
    renderSponsorTable();
    renderAffTable();
    const ft = $("featured");
    ft.innerHTML = "<thead><tr><th>Nom</th><th>Niveau</th><th>Abonnement</th><th>Période</th><th>Pages</th></tr></thead><tbody></tbody>";
    const tb = ft.querySelector("tbody");
    const rows = settingsCache.featured || [];
    if (!rows.length) tb.innerHTML = '<tr><td colspan="5"><i>Aucun abonnement payé pour l’instant.</i></td></tr>';
    for (const s of rows) {
      const tr = document.createElement("tr");
      for (const val of [s.name, s.tier, (s.subscription && s.subscription.status) || "—", (s.start || "") + " → " + (s.end || ""), (s.categories || []).join(", ")]) {
        const td = document.createElement("td"); td.textContent = val || "—"; tr.appendChild(td);
      }
      tb.appendChild(tr);
    }
  }

  function renderSponsorTable() {
    const table = $("sponsors");
    const sps = (settingsCache.sponsors || []).concat([{}]);
    table.innerHTML = "<thead><tr>" + SP_FIELDS.map((f) => "<th>" + f + "</th>").join("") + "<th>payé</th><th>suppr.</th></tr></thead><tbody></tbody>";
    const tb = table.querySelector("tbody");
    sps.forEach((s, i) => {
      const tr = document.createElement("tr");
      for (const f of SP_FIELDS) {
        const td = document.createElement("td");
        const inp = document.createElement("input");
        inp.name = "sp" + i + "_" + f; inp.value = s[f] || "";
        if (f === "start" || f === "end") inp.type = "date";
        td.appendChild(inp); tr.appendChild(td);
      }
      const tdP = document.createElement("td"); const c = document.createElement("input"); c.type = "checkbox"; c.name = "sp" + i + "_paid"; c.checked = !!s.paid; tdP.appendChild(c); tr.appendChild(tdP);
      const tdD = document.createElement("td"); const d = document.createElement("input"); d.type = "checkbox"; d.name = "sp" + i + "_del"; tdD.appendChild(d); tr.appendChild(tdD);
      tb.appendChild(tr);
    });
  }

  function renderAffTable() {
    const table = $("affiliates");
    table.innerHTML = "<thead><tr>" + AFF_FIELDS.map((f) => "<th>" + f + "</th>").join("") + "</tr></thead><tbody></tbody>";
    const tb = table.querySelector("tbody");
    (settingsCache.affiliates || []).forEach((l, i) => {
      const tr = document.createElement("tr");
      for (const f of AFF_FIELDS) {
        const td = document.createElement("td");
        const inp = document.createElement("input");
        inp.name = "af" + i + "_" + f; inp.value = l[f] || "";
        if (f === "key") inp.readOnly = true;
        td.appendChild(inp); tr.appendChild(td);
      }
      tb.appendChild(tr);
    });
  }

  $("settings-form").addEventListener("submit", async (ev) => {
    ev.preventDefault();
    const form = ev.target;
    const flags = {};
    form.querySelectorAll("#flags input[type=checkbox]").forEach((c) => { flags[c.value] = c.checked; });
    const partners = [];
    form.querySelectorAll("#partners label").forEach((l) => {
      const c = l.querySelector("input");
      const prev = (settingsCache.partners || []).find((p) => p.id === c.value) || { id: c.value, name: l.textContent.trim() };
      partners.push({ ...prev, partner: c.checked });
    });
    const sponsors = [];
    const idx = new Set();
    form.querySelectorAll("#sponsors input").forEach((inp) => {
      const m = inp.name && inp.name.match(/^sp(\d+)_/);
      if (m) idx.add(Number(m[1]));
    });
    [...idx].sort((a, b) => a - b).forEach((i) => {
      if (form["sp" + i + "_del"] && form["sp" + i + "_del"].checked) return;
      const row = {};
      SP_FIELDS.forEach((f) => { row[f] = (form["sp" + i + "_" + f] && form["sp" + i + "_" + f].value || "").trim(); });
      row.paid = !!(form["sp" + i + "_paid"] && form["sp" + i + "_paid"].checked);
      if (row.id || row.name || row.url) sponsors.push(row);
    });
    const affiliates = (settingsCache.affiliates || []).map((l, i) => {
      const n = { ...l };
      AFF_FIELDS.forEach((f) => { if (form["af" + i + "_" + f]) n[f] = form["af" + i + "_" + f].value.trim(); });
      return n;
    });
    try {
      const data = await api("/api/admin/settings", { method: "PUT", body: JSON.stringify({ flags, partners, sponsors, affiliates }) });
      settingsCache = data.settings;
      const msg = $("settings-msg"); msg.hidden = false; msg.textContent = "Enregistré dans l’admin. Un rebuild est encore requis pour publier sur le site public.";
    } catch (e) {
      const msg = $("settings-msg"); msg.hidden = false; msg.style.color = "#a3261b"; msg.textContent = (e.data && e.data.error) || "Échec.";
    }
  });

  $("export-settings").addEventListener("click", () => {
    const blob = new Blob([JSON.stringify(settingsCache || {}, null, 2)], { type: "application/json" });
    const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = "coupefab-admin-settings.json"; a.click();
  });

  if (/[?&]err=1\b/.test(location.search)) showErr($("login-err"), "Mot de passe incorrect.");
  checkSession();
})();

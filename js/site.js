/* CoupeFab site JS: nav, mega menu, search, guide filters, TOC scrollspy, forms. No dependencies. */
(function () {
  var lang = document.body.getAttribute("data-lang") || document.documentElement.lang.slice(0, 2) || "fr";
  var EN = lang === "en";

  /* ---- mobile menu ---- */
  var menuBtn = document.querySelector(".menu-btn");
  var nav = document.getElementById("mainnav");
  if (menuBtn && nav) {
    menuBtn.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
      document.body.classList.toggle("nav-open", open);
    });
  }

  /* ---- mega menu ---- */
  var mq = window.matchMedia("(min-width: 821px)");
  document.querySelectorAll(".has-mega").forEach(function (li) {
    var btn = li.querySelector(".nav-btn");
    var timer;
    function set(open) {
      li.classList.toggle("open", open);
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    }
    btn.addEventListener("click", function (e) { e.stopPropagation(); set(!li.classList.contains("open")); });
    li.addEventListener("mouseenter", function () { if (mq.matches) { clearTimeout(timer); set(true); } });
    li.addEventListener("mouseleave", function () { if (mq.matches) { timer = setTimeout(function () { set(false); }, 180); } });
    document.addEventListener("click", function (e) { if (mq.matches && !li.contains(e.target)) set(false); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && li.classList.contains("open")) { set(false); btn.focus(); } });
  });

  /* ---- search ---- */
  function norm(s) {
    return (s || "").toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/[’']/g, " ");
  }
  function escapeHtml(s) { return s.replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  var indexPromise = null;
  function loadIndex() {
    if (!indexPromise) {
      indexPromise = fetch(EN ? "/en/guides/search.json" : "/guides/recherche.json")
        .then(function (r) { return r.json(); })
        .then(function (rows) {
          rows.forEach(function (r) { r._t = norm(r.t); r._all = norm([r.t, r.d, r.h, r.c, r.k].join(" ")); });
          return rows;
        })
        .catch(function () { return []; });
    }
    return indexPromise;
  }
  function score(r, terms) {
    var s = 0;
    for (var i = 0; i < terms.length; i++) {
      var t = terms[i];
      if (r._all.indexOf(t) === -1) return 0;
      if (r._t.indexOf(t) !== -1) s += r._t.indexOf(t) === 0 ? 12 : 8;
      else s += 2;
      if (norm(r.k).indexOf(t) !== -1) s += 3;
    }
    return s;
  }
  function highlight(text, terms) {
    var out = escapeHtml(text);
    terms.forEach(function (t) {
      if (t.length < 2) return;
      var nt = norm(text), idx = nt.indexOf(t);
      if (idx > -1) {
        var raw = text.substr(idx, t.length);
        out = out.replace(escapeHtml(raw), "<mark>" + escapeHtml(raw) + "</mark>");
      }
    });
    return out;
  }
  function search(q) {
    var terms = norm(q).split(/[^a-z0-9.\-]+/).filter(function (t) { return t.length > 0; });
    return loadIndex().then(function (rows) {
      if (!terms.length) return { terms: terms, hits: [] };
      var hits = rows.map(function (r) { return { r: r, s: score(r, terms) }; })
        .filter(function (h) { return h.s > 0; })
        .sort(function (a, b) { return b.s - a.s; })
        .slice(0, 10);
      return { terms: terms, hits: hits };
    });
  }

  var dlg = document.getElementById("search-dlg");
  var input = document.getElementById("search-input");
  var list = document.getElementById("search-results");
  var empty = dlg ? dlg.querySelector(".search-empty") : null;
  var sel = -1, lastFocus = null;
  function render(res) {
    list.innerHTML = "";
    sel = -1;
    res.hits.forEach(function (h, i) {
      var li = document.createElement("li");
      li.setAttribute("role", "option");
      li.id = "sr-" + i;
      li.innerHTML = '<a href="' + h.r.u + '"><span class="r-c">' + escapeHtml(h.r.c) + '</span><span class="r-t">' +
        highlight(h.r.t, res.terms) + '</span><span class="r-d">' + highlight(h.r.d, res.terms) + "</span></a>";
      list.appendChild(li);
    });
    if (empty) empty.hidden = !(res.terms.length && !res.hits.length);
  }
  function openSearch(q) {
    if (!dlg) return;
    lastFocus = document.activeElement;
    dlg.hidden = false;
    document.body.style.overflow = "hidden";
    loadIndex();
    input.value = q || "";
    input.focus();
    if (q) search(q).then(render); else { list.innerHTML = ""; if (empty) empty.hidden = true; }
  }
  function closeSearch() {
    if (!dlg || dlg.hidden) return;
    dlg.hidden = true;
    document.body.style.overflow = "";
    if (lastFocus) lastFocus.focus();
  }
  if (dlg) {
    document.querySelectorAll("[data-search-open]").forEach(function (b) { b.addEventListener("click", function () { openSearch(""); }); });
    document.querySelectorAll("[data-search-q]").forEach(function (b) { b.addEventListener("click", function () { openSearch(b.getAttribute("data-search-q")); }); });
    dlg.querySelectorAll("[data-search-close]").forEach(function (b) { b.addEventListener("click", closeSearch); });
    dlg.addEventListener("click", function (e) { if (e.target === dlg) closeSearch(); });
    input.addEventListener("input", function () { search(input.value).then(render); });
    input.addEventListener("keydown", function (e) {
      var items = list.querySelectorAll("li");
      if (e.key === "ArrowDown" || e.key === "ArrowUp") {
        e.preventDefault();
        if (!items.length) return;
        if (sel > -1) items[sel].removeAttribute("aria-selected");
        sel = e.key === "ArrowDown" ? (sel + 1) % items.length : (sel - 1 + items.length) % items.length;
        items[sel].setAttribute("aria-selected", "true");
        items[sel].scrollIntoView({ block: "nearest" });
        input.setAttribute("aria-activedescendant", items[sel].id);
      } else if (e.key === "Enter") {
        var target = items[sel > -1 ? sel : 0];
        if (target) { e.preventDefault(); window.location.href = target.querySelector("a").getAttribute("href"); }
      }
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeSearch();
      var tag = (e.target.tagName || "").toLowerCase();
      if (e.key === "/" && tag !== "input" && tag !== "textarea" && !e.target.isContentEditable) { e.preventDefault(); openSearch(""); }
    });
  }

  /* ---- guides index: inline filter + hub chips + ?q= ---- */
  var filter = document.getElementById("guide-filter");
  if (filter) {
    var cards = Array.prototype.slice.call(document.querySelectorAll(".hub-sec .gcard"));
    var secs = Array.prototype.slice.call(document.querySelectorAll(".hub-sec"));
    var chips = Array.prototype.slice.call(document.querySelectorAll("[data-filter]"));
    var paths = document.querySelector(".paths");
    var fEmpty = document.querySelector(".filter-empty");
    var hub = "all";
    cards.forEach(function (c) { c._n = norm(c.textContent); });
    function apply() {
      var terms = norm(filter.value).split(/\s+/).filter(Boolean);
      var shown = 0;
      cards.forEach(function (c) {
        var ok = (hub === "all" || c.getAttribute("data-hub") === hub) && terms.every(function (t) { return c._n.indexOf(t) > -1; });
        c.hidden = !ok;
        if (ok) shown++;
      });
      secs.forEach(function (s) { s.hidden = !s.querySelector(".gcard:not([hidden])"); });
      if (paths) paths.hidden = !!(terms.length || hub !== "all");
      if (fEmpty) fEmpty.hidden = shown > 0;
    }
    filter.addEventListener("input", apply);
    chips.forEach(function (ch) {
      ch.addEventListener("click", function () {
        hub = ch.getAttribute("data-filter");
        chips.forEach(function (o) { o.setAttribute("aria-pressed", o === ch ? "true" : "false"); });
        apply();
      });
    });
    var q = new URLSearchParams(window.location.search).get("q");
    if (q) { filter.value = q; apply(); }
  }

  /* ---- TOC scrollspy ---- */
  var tocLinks = Array.prototype.slice.call(document.querySelectorAll(".toc a"));
  if (tocLinks.length && "IntersectionObserver" in window) {
    var map = {};
    tocLinks.forEach(function (a) { map[a.getAttribute("href").slice(1)] = a; });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          tocLinks.forEach(function (a) { a.classList.remove("is-active"); });
          var a = map[en.target.id];
          if (a) a.classList.add("is-active");
        }
      });
    }, { rootMargin: "-15% 0px -70% 0px" });
    Object.keys(map).forEach(function (id) { var h = document.getElementById(id); if (h) io.observe(h); });
    if (window.matchMedia("(max-width: 900px)").matches) {
      var d = document.querySelector(".toc"); if (d) d.removeAttribute("open");
    }
  }

  /* ---- forms (newsletter CASL + contact) ---- */
  function statusEl(form, type, text) {
    var el = form.querySelector(".form-status");
    if (!el) return;
    el.className = "form-status " + (type || "");
    el.textContent = text;
  }
  document.querySelectorAll("form[data-form]").forEach(function (form) {
    form.addEventListener("submit", async function (e) {
      e.preventDefault();
      var btn = form.querySelector('button[type="submit"]');
      var flang = form.getAttribute("data-lang") || "fr";
      var type = form.getAttribute("data-form");
      var consent = form.querySelector('input[name="consent"]');
      if (consent && !consent.checked) {
        statusEl(form, "err", flang === "en" ? "Please check the consent box to continue." : "Veuillez cocher la case de consentement pour continuer.");
        return;
      }
      var data = {
        type: type, lang: flang,
        name: (form.querySelector('[name="name"]') || {}).value || "",
        email: (form.querySelector('[name="email"]') || {}).value || "",
        message: (form.querySelector('[name="message"]') || {}).value || "",
        consent: !!(consent && consent.checked),
        website: (form.querySelector('[name="website"]') || {}).value || ""
      };
      if (btn) btn.disabled = true;
      statusEl(form, "", flang === "en" ? "Sending…" : "Envoi en cours…");
      try {
        var res = await fetch("/api/subscribe", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(data) });
        var body = await res.json().catch(function () { return {}; });
        if (!res.ok || !body.ok) throw new Error(body.error || "request failed");
        form.reset();
        statusEl(form, "ok", flang === "en"
          ? (type === "contact" ? "Message received. We will reply as soon as we can." : "You are on the list. Thank you — you can unsubscribe at any time.")
          : (type === "contact" ? "Message reçu. Nous répondrons dès que possible." : "Vous êtes bien inscrit. Merci — vous pourrez vous désabonner en tout temps."));
      } catch (err) {
        statusEl(form, "err", flang === "en"
          ? "Something went wrong. Please try again, or write to us from the contact page."
          : "Un problème est survenu. Réessayez, ou écrivez-nous depuis la page contact.");
      } finally {
        if (btn) btn.disabled = false;
      }
    });
  });
})();

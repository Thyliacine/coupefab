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
          rows.forEach(function (r) { r._t = norm(r.t); r._k = norm(r.k); r._all = norm([r.t, r.d, r.h, r.c, r.k].join(" ")); });
          return rows;
        })
        .catch(function () { return []; });
    }
    return indexPromise;
  }
  /* typo tolerance: Damerau-Levenshtein with a cutoff, against the index vocabulary */
  function dist(a, b, max) {
    if (Math.abs(a.length - b.length) > max) return max + 1;
    var prev2 = null, prev = [], cur, i, j;
    for (j = 0; j <= b.length; j++) prev[j] = j;
    for (i = 1; i <= a.length; i++) {
      cur = [i]; var rowMin = i;
      for (j = 1; j <= b.length; j++) {
        var c = a[i - 1] === b[j - 1] ? 0 : 1;
        var v = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + c);
        if (prev2 && i > 1 && j > 1 && a[i - 1] === b[j - 2] && a[i - 2] === b[j - 1]) v = Math.min(v, prev2[j - 2] + 1);
        cur[j] = v; if (v < rowMin) rowMin = v;
      }
      if (rowMin > max) return max + 1;
      prev2 = prev; prev = cur;
    }
    return prev[b.length];
  }
  function maxEdits(t) { return t.length >= 8 ? 2 : (t.length >= 4 ? 1 : 0); }
  /* returns the closest vocabulary word for a term, or null */
  function nearest(term, vocab) {
    var m = maxEdits(term); if (!m) return null;
    var best = null, bd = 99;
    for (var i = 0; i < vocab.length; i++) {
      var w = vocab[i], d = dist(term, w, m);
      if (w.length > term.length + 1) d = Math.min(d, dist(term, w.slice(0, term.length), m) + 0.5); /* typo in a prefix */
      if (d < bd || (d === bd && best && w.length < best.length)) { bd = d; best = w; }
    }
    return bd <= m ? best : null;
  }
  function vocabOf(texts) {
    var seen = {}, out = [];
    texts.forEach(function (t) { t.split(/[^a-z0-9]+/).forEach(function (w) { if (w.length > 2 && !seen[w]) { seen[w] = 1; out.push(w); } }); });
    return out;
  }
  var VOCAB = null;
  function score(r, terms) {
    var s = 0;
    for (var i = 0; i < terms.length; i++) {
      var t = terms[i];
      if (r._all.indexOf(t) === -1) return 0;
      if (r._t.indexOf(t) !== -1) s += r._t.indexOf(t) === 0 ? 12 : 8;
      else s += 2;
      if (r._k.indexOf(t) !== -1) s += 3;
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
  function rank(rows, terms) {
    return rows.map(function (r) { return { r: r, s: score(r, terms) }; })
      .filter(function (h) { return h.s > 0; })
      .sort(function (a, b) { return b.s - a.s; });
  }
  function search(q) {
    var terms = norm(q).split(/[^a-z0-9.\-]+/).filter(function (t) { return t.length > 0; });
    return loadIndex().then(function (rows) {
      if (!terms.length) return { terms: terms, hits: [] };
      var hits = rank(rows, terms), fixed = null;
      if (!hits.length) {
        if (!VOCAB) VOCAB = vocabOf(rows.map(function (r) { return r._all; }));
        var changed = false;
        var alt = terms.map(function (t) {
          var present = rows.some(function (r) { return r._all.indexOf(t) > -1; });
          if (present) return t;
          var n = nearest(t, VOCAB); if (n) { changed = true; return n; }
          return t;
        });
        if (changed) { hits = rank(rows, alt); if (hits.length) { fixed = alt.join(" "); terms = alt; } }
      }
      return { terms: terms, hits: hits.slice(0, 10), fixed: fixed };
    });
  }

  var dlg = document.getElementById("search-dlg");
  var input = document.getElementById("search-input");
  var list = document.getElementById("search-results");
  var empty = dlg ? dlg.querySelector(".search-empty") : null;
  var sel = -1, lastFocus = null;
  var SUGG = EN ? ["SheetCam", "Mastercam", "G-code", "K-factor", "dross", "feeds and speeds", "Fusion", "Inconel"]
                : ["SheetCam", "Mastercam", "G-code", "K-factor", "scories", "avances", "Fusion", "inox"];
  var fuzzyEl = null, suggEl = null;
  function ensureExtras() {
    if (fuzzyEl || !dlg) return;
    var panel = dlg.querySelector(".search-panel");
    fuzzyEl = document.createElement("p"); fuzzyEl.className = "search-fuzzy"; fuzzyEl.hidden = true; fuzzyEl.setAttribute("aria-live", "polite");
    panel.insertBefore(fuzzyEl, list);
    suggEl = document.createElement("div"); suggEl.className = "search-sugg";
    suggEl.innerHTML = "<p>" + (EN ? "Popular searches" : "Recherches populaires") + '</p><div class="chips">' +
      SUGG.map(function (q) { return '<button type="button" data-q="' + escapeHtml(q) + '">' + escapeHtml(q) + "</button>"; }).join("") + "</div>";
    panel.appendChild(suggEl);
    suggEl.addEventListener("click", function (e) { var b = e.target.closest("button[data-q]"); if (b) { input.value = b.getAttribute("data-q"); search(input.value).then(render); input.focus(); } });
    var hint = document.createElement("div"); hint.className = "search-hint";
    hint.innerHTML = EN ? "<span><kbd>↑</kbd><kbd>↓</kbd> navigate</span><span><kbd>Enter</kbd> open</span><span><kbd>Esc</kbd> close</span><span>Typos are OK</span>"
                        : "<span><kbd>↑</kbd><kbd>↓</kbd> naviguer</span><span><kbd>Entrée</kbd> ouvrir</span><span><kbd>Échap</kbd> fermer</span><span>Les fautes de frappe sont tolérées</span>";
    panel.appendChild(hint);
  }
  function render(res) {
    ensureExtras();
    list.innerHTML = "";
    sel = -1;
    if (fuzzyEl) {
      fuzzyEl.hidden = !res.fixed;
      if (res.fixed) fuzzyEl.innerHTML = (EN ? "Showing results for " : "Résultats pour ") + "<strong>" + escapeHtml(res.fixed) + "</strong>";
    }
    if (suggEl) suggEl.hidden = !!res.terms.length;
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
    if (q) search(q).then(render); else { render({ terms: [], hits: [] }); }
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
    var cardVocab = vocabOf(cards.map(function (c) { return c._n; }));
    function apply() {
      var terms = norm(filter.value).split(/\s+/).filter(Boolean).map(function (t) {
        if (cards.some(function (c) { return c._n.indexOf(t) > -1; })) return t;
        return nearest(t, cardVocab) || t;
      });
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

  /* ---- reading aids: progress, back-to-top, heading anchors, copy buttons, mobile TOC label ---- */
  var bar = document.querySelector(".readbar span");
  var article = document.querySelector(".guide-body");
  var totop = document.querySelector(".totop");
  if (totop) {
    totop.hidden = false;
    totop.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: "smooth" }); var h = document.querySelector("h1"); if (h) { h.setAttribute("tabindex", "-1"); h.focus({ preventScroll: true }); } });
  }
  var ticking = false;
  function onScroll() {
    ticking = false;
    var y = window.scrollY || document.documentElement.scrollTop;
    if (totop) totop.classList.toggle("show", y > 900);
    if (bar && article) {
      var r = article.getBoundingClientRect();
      var total = r.height - window.innerHeight * 0.6;
      var p = total > 0 ? Math.min(1, Math.max(0, -r.top / total)) : 0;
      bar.style.transform = "scaleX(" + p.toFixed(4) + ")";
    }
  }
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();
  document.querySelectorAll(".prose h2[id], .prose h3[id]").forEach(function (h) {
    if (h.closest(".news-band")) return;
    var a = document.createElement("a");
    a.className = "h-anchor"; a.href = "#" + h.id; a.textContent = "#";
    a.setAttribute("aria-label", (EN ? "Link to section: " : "Lien vers la section : ") + h.textContent);
    h.appendChild(a);
  });
  document.querySelectorAll(".prose pre").forEach(function (pre) {
    var wrap = document.createElement("div"); wrap.className = "code-wrap";
    pre.parentNode.insertBefore(wrap, pre); wrap.appendChild(pre);
    var m = (pre.className || "").match(/lang-([\w+-]+)/);
    var label = m ? m[1].replace(/^gcode$/i, "G-code") : (/^\s*[%(ON]?\s*[GMNT]\d/m.test(pre.textContent) ? "G-code" : (EN ? "Code" : "Code"));
    var bar2 = document.createElement("div"); bar2.className = "code-bar";
    var btn = document.createElement("button"); btn.type = "button"; btn.className = "copy-btn";
    var idle = EN ? "Copy" : "Copier", done = EN ? "Copied" : "Copié";
    btn.textContent = idle; btn.setAttribute("aria-label", (EN ? "Copy code: " : "Copier le code : ") + label);
    bar2.innerHTML = "<span>" + escapeHtml(label) + "</span>"; bar2.appendChild(btn);
    wrap.insertBefore(bar2, pre);
    btn.addEventListener("click", function () {
      var txt = pre.innerText;
      var ok = function () { btn.textContent = done; btn.classList.add("ok"); setTimeout(function () { btn.textContent = idle; btn.classList.remove("ok"); }, 1600); };
      if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(txt).then(ok, function () {});
      else { var ta = document.createElement("textarea"); ta.value = txt; document.body.appendChild(ta); ta.select(); try { document.execCommand("copy"); ok(); } catch (e) {} ta.remove(); }
    });
  });
  var tocEl = document.querySelector(".toc");
  if (tocEl) {
    var sum = tocEl.querySelector("summary");
    var cur = document.createElement("span"); cur.className = "toc-cur"; cur.setAttribute("aria-hidden", "true");
    sum.appendChild(cur);
    var mobile = window.matchMedia("(max-width: 900px)");
    tocEl.addEventListener("click", function (e) { if (e.target.closest("a") && mobile.matches) tocEl.removeAttribute("open"); });
    new MutationObserver(function () { var a = tocEl.querySelector("a.is-active"); cur.textContent = a ? a.textContent : ""; })
      .observe(tocEl, { subtree: true, attributes: true, attributeFilter: ["class"] });
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

/* Active states: mark filter dropdowns that left their "Tous / All" option, and briefly
   highlight result counts when a filter, tab or chip changes what is shown. */
(function () {
  function isFilter(s) { return s.tagName === "SELECT" && s.querySelector('option[value=""]'); }
  function sync() {
    document.querySelectorAll("main select").forEach(function (s) { if (isFilter(s)) s.classList.toggle("cf-set", s.value !== ""); });
  }
  function flash(el) {
    if (!el || !el.classList) return;
    el.classList.remove("cf-flash"); void el.offsetWidth; el.classList.add("cf-flash");
    clearTimeout(el._cfT); el._cfT = setTimeout(function () { el.classList.remove("cf-flash"); }, 1200);
  }
  window.cfFlash = flash;
  ["change", "input", "reset"].forEach(function (t) { document.addEventListener(t, function () { setTimeout(sync, 0); }, true); });
  document.addEventListener("click", function () { setTimeout(sync, 30); }, true);
  window.addEventListener("hashchange", function () { setTimeout(sync, 30); });
  sync(); setTimeout(sync, 600); setTimeout(sync, 2000);
  var ready = false; setTimeout(function () { ready = true; }, 1500);
  var sel = '[id$="-count"], #ec-status, .sp-count';
  if (window.MutationObserver) {
    var mo = new MutationObserver(function (ms) {
      if (!ready) return;
      ms.forEach(function (m) { var el = m.target.nodeType === 1 ? m.target : m.target.parentNode; if (el && el.matches && el.matches(sel)) flash(el); });
      sync();
    });
    document.querySelectorAll(sel).forEach(function (el) { mo.observe(el, { childList: true, characterData: true, subtree: true }); });
  }
})();

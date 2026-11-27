/* CoupeFab app shell for phones: service worker, « Plus » sheet, install prompt, sticky filters,
 * navigation feedback. Plain JS, no dependencies. Desktop: only the service worker registers. */
(function () {
  var MQ = "(max-width: 768px), (orientation: landscape) and (max-height: 520px) and (max-width: 1023px)";
  var mq = window.matchMedia(MQ);
  var doc = document.documentElement, body = document.body;
  var EN = (body.getAttribute("data-lang") || "fr") === "en";
  var standalone = window.matchMedia("(display-mode: standalone)").matches || window.navigator.standalone === true;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (_) { return null; } }
  if (standalone) doc.classList.add("cf-standalone");

  /* ---- service worker ---- */
  if ("serviceWorker" in navigator && (location.protocol === "https:" || location.hostname === "localhost")) {
    window.addEventListener("load", function () {
      navigator.serviceWorker.register("/sw.js", { scope: "/" }).then(function (reg) {
        // pick up a new build quickly: check on focus, at most every 10 minutes
        var last = Date.now();
        document.addEventListener("visibilitychange", function () {
          if (document.visibilityState === "visible" && Date.now() - last > 6e5) { last = Date.now(); reg.update().catch(function () {}); }
        });
      }).catch(function () {});
    });
  }

  /* ---- bottom sheets ---- */
  var lastFocus = null, openSheetEl = null, pushed = false;
  function openSheet(el, opener) {
    if (!el || openSheetEl === el) return;
    if (openSheetEl) closeSheet(openSheetEl, true);
    lastFocus = opener || document.activeElement;
    el.hidden = false;
    el.style.removeProperty("--cf-drag");
    body.classList.add("cf-sheet-open");
    openSheetEl = el;
    requestAnimationFrame(function () { requestAnimationFrame(function () { el.classList.add("is-open"); }); });
    var panel = el.querySelector(".cf-sheet-panel"); if (panel) panel.focus({ preventScroll: true });
    if (el.id === "cf-sheet") setMore(true);
    if (!pushed) { try { history.pushState({ cfSheet: el.id }, ""); pushed = true; } catch (_) {} }
  }
  function closeSheet(el, silent) {
    el = el || openSheetEl; if (!el) return;
    el.classList.remove("is-open");
    body.classList.remove("cf-sheet-open");
    if (el.id === "cf-sheet") setMore(false);
    openSheetEl = null;
    var done = function () { if (!el.classList.contains("is-open")) el.hidden = true; };
    if (reduce) done(); else setTimeout(done, 340);
    if (pushed) { pushed = false; if (!silent) { try { history.back(); } catch (_) {} } }
    if (lastFocus && lastFocus.focus) lastFocus.focus({ preventScroll: true });
  }
  window.addEventListener("popstate", function () { pushed = false; if (openSheetEl) closeSheet(openSheetEl, true); });
  window.addEventListener("pageshow", function (e) { if (e.persisted) { document.querySelectorAll(".cf-sheet").forEach(function (s) { s.classList.remove("is-open"); s.hidden = true; }); body.classList.remove("cf-sheet-open"); openSheetEl = null; setMore(false); } });
  var moreBtn = document.querySelector(".cf-tab-more");
  function setMore(open) { if (moreBtn) moreBtn.setAttribute("aria-expanded", open ? "true" : "false"); }
  var sheet = document.getElementById("cf-sheet");
  if (moreBtn && sheet) moreBtn.addEventListener("click", function () { openSheetEl === sheet ? closeSheet(sheet) : openSheet(sheet, moreBtn); });
  document.addEventListener("click", function (e) {
    var c = e.target.closest && e.target.closest("[data-cf-close]");
    if (c) { e.preventDefault(); closeSheet(c.closest(".cf-sheet")); }
  });
  document.addEventListener("keydown", function (e) {
    if (!openSheetEl) return;
    if (e.key === "Escape") { closeSheet(openSheetEl); return; }
    if (e.key === "Tab") { // keep focus inside the sheet
      var f = openSheetEl.querySelectorAll("a[href], button:not([hidden]), [tabindex='0']");
      if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  });
  // swipe the sheet down to dismiss
  document.querySelectorAll(".cf-sheet-panel").forEach(function (panel) {
    var y0 = null, dy = 0, el = panel.closest(".cf-sheet");
    panel.addEventListener("touchstart", function (e) {
      if (panel.scrollTop > 0) { y0 = null; return; }
      y0 = e.touches[0].clientY; dy = 0;
    }, { passive: true });
    panel.addEventListener("touchmove", function (e) {
      if (y0 === null) return;
      dy = Math.max(0, e.touches[0].clientY - y0);
      if (dy > 4) { el.classList.add("is-dragging"); el.style.setProperty("--cf-drag", dy + "px"); }
    }, { passive: true });
    panel.addEventListener("touchend", function () {
      if (y0 === null) return;
      el.classList.remove("is-dragging");
      if (dy > 90) closeSheet(el); else el.style.removeProperty("--cf-drag");
      y0 = null; dy = 0;
    });
  });
  // a link inside a sheet: close it without the history.back() racing the navigation
  document.querySelectorAll(".cf-sheet a[href]").forEach(function (a) {
    a.addEventListener("click", function () { if (openSheetEl) { openSheetEl.classList.remove("is-open"); body.classList.remove("cf-sheet-open"); } });
  });

  /* ---- install prompt (Android: beforeinstallprompt; iOS: instructions sheet) ---- */
  var KEY = "cf-install-dismissed";
  var deferred = null;
  var ua = navigator.userAgent || "";
  var isIOS = /iphone|ipad|ipod/i.test(ua) || (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);
  var banner = document.getElementById("cf-install");
  var iosSheet = document.getElementById("cf-ios");
  var installBtns = document.querySelectorAll("[data-cf-install]");
  function dismissed() { var t = +store(KEY) || 0; return t && Date.now() - t < 1000 * 60 * 60 * 24 * 60; } // remembered 60 days
  function views() { var n = (+store("cf-views") || 0) + 1; store("cf-views", String(n)); return n; }
  var nViews = views();
  function canInstall() { return !standalone && (deferred || isIOS); }
  function refreshInstall() {
    installBtns.forEach(function (b) { if (b.closest(".cf-sheet")) b.hidden = !canInstall(); });
    if (banner) banner.hidden = !(canInstall() && mq.matches && !dismissed() && nViews >= 2);
  }
  window.addEventListener("beforeinstallprompt", function (e) { e.preventDefault(); deferred = e; refreshInstall(); });
  window.addEventListener("appinstalled", function () { deferred = null; store(KEY, String(Date.now())); refreshInstall(); });
  installBtns.forEach(function (b) {
    b.addEventListener("click", function () {
      if (deferred) {
        deferred.prompt();
        deferred.userChoice.then(function (c) { if (c && c.outcome === "dismissed") store(KEY, String(Date.now())); deferred = null; refreshInstall(); });
      } else if (isIOS && iosSheet) {
        openSheet(iosSheet, b);
      }
      if (banner) banner.hidden = true;
    });
  });
  document.querySelectorAll("[data-cf-dismiss]").forEach(function (b) {
    b.addEventListener("click", function () { store(KEY, String(Date.now())); if (banner) banner.hidden = true; });
  });
  setTimeout(refreshInstall, 1200);

  /* ---- navigation feedback: progress bar on tap ---- */
  document.addEventListener("click", function (e) {
    if (!mq.matches || e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var a = e.target.closest && e.target.closest("a[href]");
    if (!a || a.target === "_blank" || a.hasAttribute("download")) return;
    var u; try { u = new URL(a.href, location.href); } catch (_) { return; }
    if (u.origin !== location.origin || /^\/(api|admin)\//.test(u.pathname) || /\.(json|csv|pdf)$/.test(u.pathname)) return;
    if (u.pathname === location.pathname && u.search === location.search) return; // hash or same page
    doc.classList.add("cf-going");
  });
  window.addEventListener("pageshow", function () { doc.classList.remove("cf-going"); });
  window.addEventListener("pagehide", function () { setTimeout(function () { doc.classList.remove("cf-going"); }, 50); });

  /* ---- suppliers list: compact sticky search with a Filtres toggle ---- */
  var sp = document.getElementById("sp-filters");
  if (sp && !sp.querySelector(".cf-ftog")) {
    var q = sp.querySelector(".sp-q");
    var tog = document.createElement("button");
    tog.type = "button"; tog.className = "cf-ftog"; tog.setAttribute("aria-expanded", "false"); tog.setAttribute("aria-controls", "sp-filters");
    tog.innerHTML = (EN ? "Filters" : "Filtres") + " <b></b>";
    function syncTog() {
      tog.hidden = !mq.matches;
      if (mq.matches) sp.classList.add("cf-fold"); else sp.classList.remove("cf-fold", "is-open");
      var n = 0; sp.querySelectorAll("select").forEach(function (s) { if (s.name !== "sort" && s.value) n++; });
      tog.querySelector("b").textContent = n ? String(n) : "";
    }
    tog.addEventListener("click", function () {
      var open = sp.classList.toggle("is-open");
      tog.setAttribute("aria-expanded", open ? "true" : "false");
    });
    if (q && q.nextSibling) sp.insertBefore(tog, q.nextSibling); else sp.appendChild(tog);
    sp.addEventListener("change", syncTog);
    if (mq.addEventListener) mq.addEventListener("change", syncTog);
    syncTog();
  }

  /* ---- keep bottom-sheet + bars sane when the viewport crosses the phone breakpoint ---- */
  if (mq.addEventListener) mq.addEventListener("change", function (e) { if (!e.matches && openSheetEl) closeSheet(openSheetEl, true); refreshInstall(); });
})();

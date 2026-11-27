/* CoupeFab guide tabs — progressive enhancement.
   Without JS: an in-page nav of anchor links and every section visible (also used for print).
   With JS: WAI-ARIA tabs (automatic activation, roving tabindex, Arrow/Home/End keys), deep links (#t-key or any heading id). */
(function () {
  "use strict";
  var root = document.querySelector("[data-gtabs]");
  if (!root) return;
  var list = root.querySelector(".gtabs-list");
  var links = Array.prototype.slice.call(list.querySelectorAll("a[data-tab]"));
  var panels = links.map(function (a) { return document.getElementById("t-" + a.getAttribute("data-tab")); });
  if (!links.length || panels.some(function (p) { return !p; })) return;

  root.classList.add("is-tabs");
  list.setAttribute("role", "tablist");
  list.setAttribute("aria-label", root.querySelector(".gtabs-nav").getAttribute("aria-label"));
  links.forEach(function (a, i) {
    var key = a.getAttribute("data-tab");
    a.parentNode.setAttribute("role", "presentation");
    a.setAttribute("role", "tab");
    a.id = "tab-" + key;
    a.setAttribute("aria-controls", "t-" + key);
    panels[i].setAttribute("role", "tabpanel");
    panels[i].setAttribute("aria-labelledby", a.id);
    panels[i].setAttribute("tabindex", "0");
  });

  function select(i, focus, push) {
    links.forEach(function (a, j) {
      var on = i === j;
      a.setAttribute("aria-selected", on ? "true" : "false");
      a.setAttribute("tabindex", on ? "0" : "-1");
      panels[j].hidden = !on;
    });
    document.querySelectorAll('.toc-tabs .toc-tab').forEach(function (li) {
      var a = li.querySelector("a[data-tab]");
      li.classList.toggle("is-current", !!a && a.getAttribute("data-tab") === links[i].getAttribute("data-tab"));
    });
    if (focus) links[i].focus();
    if (push && history.replaceState) history.replaceState(null, "", "#t-" + links[i].getAttribute("data-tab"));
  }

  function indexFor(id) {
    if (!id) return -1;
    var el = document.getElementById(id);
    if (!el) return -1;
    for (var i = 0; i < panels.length; i++) if (panels[i] === el || panels[i].contains(el)) return i;
    return -1;
  }

  function fromHash(scroll) {
    var id = decodeURIComponent((location.hash || "").slice(1));
    var i = indexFor(id);
    if (i < 0) { if (!links.some(function (a) { return a.getAttribute("aria-selected") === "true"; })) select(0, false, false); return; }
    select(i, false, false);
    var ae = document.activeElement;
    if (ae && ae.classList && ae.classList.contains("gtab-panel")) ae.blur();
    if (scroll) {
      var el = document.getElementById(id);
      if (el && !/^t-/.test(id)) el.scrollIntoView();
      else root.scrollIntoView();
    }
  }

  links.forEach(function (a, i) {
    a.addEventListener("click", function (e) { e.preventDefault(); select(i, true, true); });
    a.addEventListener("keydown", function (e) {
      var n = links.length, j = null;
      if (e.key === "ArrowRight" || e.key === "ArrowDown") j = (i + 1) % n;
      else if (e.key === "ArrowLeft" || e.key === "ArrowUp") j = (i - 1 + n) % n;
      else if (e.key === "Home") j = 0;
      else if (e.key === "End") j = n - 1;
      else if (e.key === " " || e.key === "Spacebar") { e.preventDefault(); select(i, true, true); return; }
      if (j !== null) { e.preventDefault(); select(j, true, true); }
    });
  });

  // TOC and in-body links pointing into a hidden panel switch to that tab first
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest('a[href^="#"]');
    if (!a || a.getAttribute("role") === "tab") return;
    var id = decodeURIComponent(a.getAttribute("href").slice(1));
    var i = indexFor(id);
    if (i < 0) return;
    e.preventDefault();
    select(i, false, false);
    if (history.pushState) history.pushState(null, "", "#" + id);
    var el = document.getElementById(id);
    if (/^t-/.test(id)) { links[i].focus(); root.scrollIntoView(); }
    else if (el) { el.scrollIntoView(); if (!el.hasAttribute("tabindex")) el.setAttribute("tabindex", "-1"); el.focus({ preventScroll: true }); }
  });
  window.addEventListener("hashchange", function () { fromHash(true); });
  window.addEventListener("beforeprint", function () { panels.forEach(function (p) { p.hidden = false; }); });
  window.addEventListener("afterprint", function () { fromHash(false); });
  fromHash(!!location.hash);
  // Chrome focuses a fragment target that has tabindex; drop that programmatic focus ring on load.
  function dropLoadFocus() { var ae = document.activeElement; if (ae && ae.classList && ae.classList.contains("gtab-panel")) ae.blur(); }
  if (location.hash) { window.addEventListener("load", function () { setTimeout(dropLoadFocus, 0); }); setTimeout(dropLoadFocus, 300); }
})();

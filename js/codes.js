/* CoupeFab error-code lookup: filters the server-rendered tables (works without JS: everything is listed). */
(function () {
  "use strict";
  var q = document.getElementById("ec-q"), sel = document.getElementById("ec-brand");
  if (!q || !sel) return;
  var fr = document.documentElement.lang.indexOf("fr") === 0;
  var rows = Array.prototype.slice.call(document.querySelectorAll(".ec-table tbody tr"));
  var brands = Array.prototype.slice.call(document.querySelectorAll(".ec-brand"));
  var kinds = Array.prototype.slice.call(document.querySelectorAll(".ec-kind"));
  var chips = Array.prototype.slice.call(document.querySelectorAll(".ec-kinds [data-kind]"));
  var empty = document.querySelector(".ec-empty"), status = document.getElementById("ec-status");
  var kind = "all", timer = null;
  function norm(s) {
    return (s || "").toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/[–—]/g, "-").trim();
  }
  rows.forEach(function (r) {
    var h = norm(r.getAttribute("data-q"));
    r._h = h; r._c = h.replace(/[\s\-.:_·/]/g, "");
  });
  function apply() {
    var raw = norm(q.value), b = sel.value, terms = raw.split(/\s+/).filter(Boolean), n = 0;
    var compact = raw.replace(/[\s\-.:_·/]/g, "");
    rows.forEach(function (r) {
      var ok = (!b || r.getAttribute("data-b") === b);
      if (ok && terms.length) ok = terms.every(function (t) { return r._h.indexOf(t) > -1; }) || (compact.length > 1 && r._c.indexOf(compact) > -1);
      r.hidden = !ok; if (ok) n++;
    });
    brands.forEach(function (s) {
      var vis = s.querySelector("tbody tr:not([hidden])") && (kind === "all" || s.getAttribute("data-kind") === kind);
      s.hidden = !vis;
    });
    var shown = 0;
    brands.forEach(function (s) { if (!s.hidden) shown += s.querySelectorAll("tbody tr:not([hidden])").length; });
    kinds.forEach(function (k) { k.hidden = !k.querySelector(".ec-brand:not([hidden])"); });
    var searching = !!(terms.length || b || kind !== "all");
    brands.forEach(function (s) {
      var fold = s.querySelector("details.ec-fold");
      if (!fold) return;
      if (searching && !s.hidden) fold.open = true;
      else if (!searching) fold.open = false;
    });
    empty.hidden = shown > 0;
    status.textContent = (terms.length || b || kind !== "all") ? (fr ? shown + " code" + (shown > 1 ? "s" : "") + " affiché" + (shown > 1 ? "s" : "") : shown + " code" + (shown === 1 ? "" : "s") + " shown") : "";
    var u = new URL(location.href);
    if (q.value) u.searchParams.set("q", q.value); else u.searchParams.delete("q");
    if (b) u.searchParams.set("b", b); else u.searchParams.delete("b");
    if (history.replaceState) history.replaceState(null, "", u.pathname + (u.search ? u.search : "") + location.hash);
  }
  q.addEventListener("input", function () { clearTimeout(timer); timer = setTimeout(apply, 120); });
  sel.addEventListener("change", apply);
  q.form.addEventListener("submit", function (e) { e.preventDefault(); apply(); });
  chips.forEach(function (c) {
    c.addEventListener("click", function () {
      kind = c.getAttribute("data-kind");
      chips.forEach(function (x) { x.setAttribute("aria-pressed", x === c ? "true" : "false"); });
      apply();
    });
  });
  var p = new URLSearchParams(location.search);
  if (p.get("q")) q.value = p.get("q");
  if (p.get("b")) sel.value = p.get("b");
  if (p.get("q") || p.get("b")) apply();
})();

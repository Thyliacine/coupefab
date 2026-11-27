/* CoupeFab — supplier directory: instant filters, sort, URL state. */
(function () {
  "use strict";
  var app = document.getElementById("sp-app");
  if (!app) return;
  var FR = app.getAttribute("data-lang") !== "en";
  var T = function (fr, en) { return FR ? fr : en; };
  var form = document.getElementById("sp-filters");
  if (!form) return;
  var grid = document.getElementById("sp-grid");
  var cards = [].slice.call(app.querySelectorAll(".sp-card"));
  var count = document.getElementById("sp-count"), empty = document.getElementById("sp-empty");
  var writing = false;
  var pager = null;

  function norm(s) {
    return String(s || "").toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
  }
  cards.forEach(function (c, i) {
    c._n = norm(c.getAttribute("data-name"));
    c._i = i;
    c._city = norm(c.getAttribute("data-city"));
    c._qc = (" " + (c.getAttribute("data-prov") || "") + " ").indexOf(" QC ") >= 0 ? 0 : 1;
    c._pub = c.getAttribute("data-pub") === "1" ? 0 : 1;
    c._name = norm((c.querySelector("h3") || {}).textContent || "");
  });

  function hasToken(attr, val) {
    return (" " + (attr || "") + " ").indexOf(" " + val + " ") >= 0;
  }

  function apply(push) {
    var q = norm(form.q.value.trim());
    var region = form.region.value, cat = form.cat.value, svc = form.svc.value, sort = form.sort.value || "qc";
    var shown = [];
    cards.forEach(function (c) {
      var ok = (!q || c._n.indexOf(q) >= 0) &&
        (!region || hasToken(c.getAttribute("data-prov"), region)) &&
        (!cat || hasToken(c.getAttribute("data-cats"), cat)) &&
        (!svc || hasToken(c.getAttribute("data-svc"), svc));
      c.hidden = !ok;
      if (ok) shown.push(c);
    });
    shown.sort(function (a, b) {
      if (sort === "name") return a._name < b._name ? -1 : a._name > b._name ? 1 : a._i - b._i;
      if (sort === "prices") return a._pub - b._pub || a._name.localeCompare(b._name);
      if (sort === "city") return (a._city || "zzz").localeCompare(b._city || "zzz") || a._name.localeCompare(b._name);
      return a._qc - b._qc || a._name.localeCompare(b._name);
    });
    shown.forEach(function (c) { grid.appendChild(c); });
    var n = shown.length;
    count.textContent = n + T(n > 1 ? " fournisseurs" : " fournisseur", n === 1 ? " supplier" : " suppliers");
    empty.hidden = n > 0;
    if (window.cfPager) {
      if (!pager) {
        pager = window.cfPager({
          mount: "#sp-pager",
          items: function () { return shown; },
          allItems: cards,
          pageSize: 24,
          lang: FR ? "fr" : "en",
          scrollTo: "#sp-grid"
        });
      }
      if (push === "keep") pager.apply();
      else pager.reset();
    }
    if (push !== false && push !== "keep") syncUrl(q, region, cat, svc, sort);
  }

  function syncUrl(q, region, cat, svc, sort) {
    var u = new URL(location.href);
    function set(k, v, def) {
      if (v && v !== (def || "")) u.searchParams.set(k, v); else u.searchParams.delete(k);
    }
    set("q", form.q.value.trim());
    set("region", region);
    set("cat", cat);
    set("svc", svc);
    set("sort", sort, "qc");
    var next = u.pathname + (u.search || "") + u.hash;
    if (next !== location.pathname + location.search + location.hash) {
      writing = true;
      history.replaceState(null, "", next);
      writing = false;
    }
  }

  function fromUrl() {
    var u = new URL(location.href);
    if (form.q) form.q.value = u.searchParams.get("q") || "";
    if (form.region) form.region.value = u.searchParams.get("region") || "";
    if (form.cat) form.cat.value = u.searchParams.get("cat") || "";
    if (form.svc) form.svc.value = u.searchParams.get("svc") || "";
    if (form.sort) form.sort.value = u.searchParams.get("sort") || "qc";
    apply("keep");
  }

  form.addEventListener("input", function () { apply(true); });
  form.addEventListener("change", function () { apply(true); });
  form.querySelector("[data-reset]").addEventListener("click", function () {
    form.reset();
    if (form.sort) form.sort.value = "qc";
    apply(true);
  });
  window.addEventListener("popstate", function () { if (!writing) fromUrl(); });
  fromUrl();
})();

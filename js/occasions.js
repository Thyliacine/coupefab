/* CoupeFab occasions: tabs, filters, sort. No dependencies. */
(function () {
  var app = document.getElementById("oc-app");
  if (!app) return;
  app.classList.add("js");

  var form = document.getElementById("oc-filters");
  var pager = null;
  var grid = document.getElementById("oc-grid");
  var countEl = document.getElementById("oc-count");
  var emptyEl = document.getElementById("oc-empty");
  var sortEl = document.getElementById("oc-sort");
  var tabs = app.querySelectorAll(".oc-tabs [role=tab]");
  var deals = document.getElementById("oc-deals");
  var cards = Array.prototype.slice.call(grid ? grid.querySelectorAll(".oc-card") : []);
  var cat = "";

  function val(name) {
    if (!form) return "";
    var el = form.elements[name];
    if (!el) return "";
    return el.type === "checkbox" ? (el.checked ? "1" : "") : (el.value || "");
  }

  function inRange(n, spec) {
    if (!spec) return true;
    if (spec === "quote") return n === "" || n === null;
    var parts = spec.split("-");
    var lo = parts[0] === "" ? -Infinity : Number(parts[0]);
    var hi = parts[1] === "" ? Infinity : Number(parts[1]);
    if (n === "" || n === null) return false;
    var x = Number(n);
    return x >= lo && x <= hi;
  }

  function yearOk(y, spec) {
    if (!spec) return true;
    if (y === "" || y == null) return false;
    return inRange(y, spec);
  }

  function regionOk(card, region) {
    var prov = (card.getAttribute("data-prov") || "").toUpperCase();
    var dist = card.getAttribute("data-dist");
    var d = dist === "" ? null : Number(dist);
    if (region === "all") return true;
    if (region === "qc") return prov === "QC";
    if (region === "qc-on") return prov === "QC" || prov === "ON";
    if (region === "near150") return d != null && d <= 150;
    if (region === "near300") return d != null && d <= 300;
    // default: Canada
    return ["QC", "ON", "BC", "AB", "SK", "MB", "NS", "NB", "PE", "NL", "YT", "NT", "NU"].indexOf(prov) !== -1;
  }

  function apply(keepPage) {
    var q = (val("q") || "").trim().toLowerCase();
    var region = val("region") || "all";
    var price = val("price");
    var year = val("year");
    var source = val("source");
    var dealsOnly = !!val("deals");
    var showGone = !!val("showgone");
    app.classList.toggle("show-gone", showGone);
    if (deals) deals.hidden = !!(q || price || year || source || dealsOnly || cat);

    var shown = 0;
    cards.forEach(function (c) {
      var status = c.getAttribute("data-status") || "active";
      var gone = status !== "active";
      var ok = true;
      if (gone && !showGone) ok = false;
      if (ok && cat && c.getAttribute("data-cat") !== cat) ok = false;
      if (ok && q) {
        var hay = (c.textContent || "").toLowerCase();
        if (hay.indexOf(q) === -1) ok = false;
      }
      if (ok && !regionOk(c, region)) ok = false;
      if (ok && price && !inRange(c.getAttribute("data-price"), price)) ok = false;
      if (ok && year && !yearOk(c.getAttribute("data-year"), year)) ok = false;
      if (ok && source && c.getAttribute("data-src") !== source) ok = false;
      if (ok && dealsOnly) {
        var b = c.getAttribute("data-badge");
        if (b !== "super" && b !== "good") ok = false;
      }
      c.classList.toggle("is-hidden", !ok);
      if (ok) shown += 1;
    });

    sortCards();
    if (countEl) {
      var lang = app.getAttribute("data-lang") || "fr";
      countEl.textContent = lang === "fr"
        ? (shown === 1 ? "1 annonce" : shown + " annonces")
        : (shown === 1 ? "1 listing" : shown + " listings");
    }
    if (emptyEl) emptyEl.hidden = shown !== 0;
    pageList(keepPage);
  }

  function pageList(keepPage) {
    if (!window.cfPager || !grid) return;
    if (!pager) {
      pager = window.cfPager({
        mount: "#oc-pager",
        items: function () { return cards.filter(function (c) { return !c.classList.contains("is-hidden"); }); },
        allItems: cards,
        pageSize: 24,
        lang: (app.getAttribute("data-lang") || "fr"),
        scrollTo: "#oc-results-title"
      });
    }
    if (keepPage) pager.apply();
    else pager.reset();
  }

  function sortCards() {
    var mode = (sortEl && sortEl.value) || "deal";
    var vis = cards.filter(function (c) { return !c.classList.contains("is-hidden"); });
    vis.sort(function (a, b) {
      function num(el, attr, missing) {
        var v = el.getAttribute(attr);
        if (v === "" || v == null) return missing;
        return Number(v);
      }
      if (mode === "newest") {
        return (b.getAttribute("data-seen") || "").localeCompare(a.getAttribute("data-seen") || "");
      }
      if (mode === "price-asc") {
        return num(a, "data-price", 1e12) - num(b, "data-price", 1e12);
      }
      if (mode === "price-desc") {
        return num(b, "data-price", -1) - num(a, "data-price", -1);
      }
      if (mode === "near") {
        return num(a, "data-dist", 1e9) - num(b, "data-dist", 1e9);
      }
      if (mode === "year-desc") {
        return num(b, "data-year", 0) - num(a, "data-year", 0);
      }
      // best deal: badge rank, then Quebec, then price
      var da = num(a, "data-deal", 9) - num(b, "data-deal", 9);
      if (da) return da;
      var pa = (a.getAttribute("data-prov") === "QC" ? 0 : a.getAttribute("data-prov") === "ON" ? 1 : 2);
      var pb = (b.getAttribute("data-prov") === "QC" ? 0 : b.getAttribute("data-prov") === "ON" ? 1 : 2);
      if (pa !== pb) return pa - pb;
      return num(a, "data-price", 1e12) - num(b, "data-price", 1e12);
    });
    vis.forEach(function (c) { grid.appendChild(c); });
  }

  function setTab(next) {
    cat = next || "";
    tabs.forEach(function (t) {
      var on = (t.getAttribute("data-cat") || "") === cat;
      t.setAttribute("aria-selected", on ? "true" : "false");
      t.tabIndex = on ? 0 : -1;
    });
    apply();
  }

  tabs.forEach(function (t, i) {
    t.addEventListener("click", function () { setTab(t.getAttribute("data-cat") || ""); });
    t.addEventListener("keydown", function (e) {
      var k = e.key;
      if (k !== "ArrowRight" && k !== "ArrowLeft" && k !== "Home" && k !== "End") return;
      e.preventDefault();
      var idx = i;
      if (k === "ArrowRight") idx = (i + 1) % tabs.length;
      if (k === "ArrowLeft") idx = (i - 1 + tabs.length) % tabs.length;
      if (k === "Home") idx = 0;
      if (k === "End") idx = tabs.length - 1;
      tabs[idx].focus();
      setTab(tabs[idx].getAttribute("data-cat") || "");
    });
  });

  // mobile: filters collapse behind a "Filtres" button so listings sit above the fold
  var ftog = app.querySelector(".oc-filters-toggle");
  function activeFilters() {
    if (!form) return 0;
    var n = 0;
    ["q", "region", "price", "year", "source"].forEach(function (k) { if (form.elements[k] && form.elements[k].value) n++; });
    if (form.elements.deals && form.elements.deals.checked) n++;
    return n;
  }
  function syncToggle() {
    if (!ftog) return;
    var n = activeFilters(), b = ftog.querySelector("[data-nf]");
    if (b) b.textContent = n ? "(" + n + ")" : "";
  }
  if (ftog && form) {
    form.classList.add("is-collapsible");
    ftog.addEventListener("click", function () {
      var open = ftog.getAttribute("aria-expanded") !== "true";
      ftog.setAttribute("aria-expanded", open ? "true" : "false");
      form.classList.toggle("is-open", open);
    });
  }
  if (form) {
    form.addEventListener("input", syncToggle);
    form.addEventListener("change", syncToggle);
    form.addEventListener("input", apply);
    form.addEventListener("change", apply);
    var reset = form.querySelector("[data-reset]");
    if (reset) reset.addEventListener("click", function () {
      form.reset();
      if (form.elements.region) form.elements.region.value = "";
      setTab("");
    });
  }
  if (sortEl) sortEl.addEventListener("change", apply);

  // Touch/keyboard: announce badge reason already in title; add click toggle on small screens
  app.addEventListener("click", function (e) {
    var tip = e.target.closest && e.target.closest("[data-tip]");
    if (!tip) return;
    // title already provides the reason; ensure it's focusable announcement
    if (!tip.getAttribute("aria-label")) tip.setAttribute("aria-label", tip.getAttribute("data-tip"));
  });

  apply(true);
})();

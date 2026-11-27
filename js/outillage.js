/* CoupeFab — /outillage/ and /en/tooling/ : filterable, sortable tooling price table */
(function () {
  var app = document.getElementById("tl-app");
  if (!app) return;
  var fr = (app.getAttribute("data-lang") || "fr") === "fr";
  var PAGE = 100;
  function $(s, r) { return (r || document).querySelector(s); }
  function $all(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function esc(s) { return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;"); }
  function money(x) {
    if (fr) return (x || 0).toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, "\u202f").replace(".", ",") + " $";
    return "$" + (x || 0).toLocaleString("en-CA", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }
  var MF = ["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"];
  var ME = ["January","February","March","April","May","June","July","August","September","October","November","December"];
  function dateLab(iso) {
    var p = String(iso || "").slice(0, 10).split("-"); if (p.length < 3) return iso || "";
    return fr ? (+p[2] + " " + MF[+p[1] - 1] + " " + p[0]) : (ME[+p[1] - 1] + " " + (+p[2]) + ", " + p[0]);
  }
  function norm(s) { return String(s || "").toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, ""); }

  /* tabs */
  var tabs = $all('[role="tab"]', app);
  function selectTab(id, user) {
    tabs.forEach(function (t) {
      var on = t.id === id, panel = document.getElementById(t.getAttribute("aria-controls"));
      t.setAttribute("aria-selected", on ? "true" : "false"); t.tabIndex = on ? 0 : -1;
      if (panel) { if (on) { panel.removeAttribute("hidden"); panel.classList.add("is-active"); } else { panel.setAttribute("hidden", ""); panel.classList.remove("is-active"); } }
    });
    if (user && history.replaceState) history.replaceState(null, "", "#" + id.replace("tl-tab-", ""));
  }
  tabs.forEach(function (t, i) {
    t.addEventListener("click", function () { selectTab(t.id, true); });
    t.addEventListener("keydown", function (e) {
      if (e.key !== "ArrowRight" && e.key !== "ArrowLeft") return;
      e.preventDefault(); var n = e.key === "ArrowRight" ? (i + 1) % tabs.length : (i - 1 + tabs.length) % tabs.length;
      tabs[n].focus(); selectTab(tabs[n].id, true);
    });
  });
  var h = (location.hash || "").slice(1);
  if (h === "shops" || h === "fournisseurs" || h === "suppliers") selectTab("tl-tab-shops");
  else if (h === "method" || h === "methode") selectTab("tl-tab-method");

  var form = $("#tl-filters"), body = $("#tl-body"), count = $("#tl-count"), more = $("#tl-more");
  var rows = [], view = [], shown = 0, sortKey = "unit", sortDir = 1, sups = [], catName = {};

  function rowHtml(r) {
    var s = sups[r.src] || {};
    var sub = r.brand ? '<div class="tl-sub">' + esc(r.brand) + (r.sku ? " · " + esc(r.sku) : "") + "</div>" : (r.sku ? '<div class="tl-sub">' + esc(r.sku) + "</div>" : "");
    var usd = r.cur === "USD" ? '<div class="tl-sub">' + (fr ? "affiché " : "listed ") + r.orig.toFixed(2) + " US$</div>" : "";
    var pack = r.pack ? '<div class="tl-sub">' + (fr ? "paquet de " : "pack of ") + r.pack + "</div>" : "";
    var stock = r.stock ? "" : '<div class="tl-sub tl-out">' + (fr ? "en rupture" : "out of stock") + "</div>";
    return "<tr><td>" + esc(r.name) + sub + '<div class="tl-sub tl-cat">' + esc(catName[r.cat] || "") + "</div></td>" +
      "<td>" + esc(r.spec || "—") + "</td>" +
      "<td>" + esc(s.name || "") + '<div class="tl-sub">' + esc(s.province || s.country || "") + "</div></td>" +
      '<td class="tl-r tl-num">' + money(r.price) + usd + "</td>" +
      '<td class="tl-r tl-num">' + money(r.unit) + pack + "</td>" +
      "<td>" + esc(dateLab(r.date)) + stock + "</td>" +
      '<td><a href="' + esc(r.url) + '" rel="noopener nofollow" target="_blank">' + (fr ? "Voir" : "View") + '<span class="tl-sr"> ' + esc(r.name) + " — " + esc(s.name || "") + "</span></a></td></tr>";
  }
  function regionOf(s) { return s.province === "QC" ? "qc" : (s.country === "CA" ? "ca" : "us"); }

  function apply() {
    if (!rows.length) return;
    var q = norm(form.q.value).trim(), words = q ? q.split(/\s+/) : [];
    var cat = form.cat.value, reg = form.region.value, src = form.src.value, brand = form.brand.value, stock = form.stock.value;
    view = rows.filter(function (r) {
      if (cat && r.cat !== cat) return false;
      if (reg && r.reg !== reg) return false;
      if (src !== "" && String(r.src) !== src) return false;
      if (brand && r.brand !== brand) return false;
      if (stock === "1" && !r.stock) return false;
      for (var i = 0; i < words.length; i++) if (r.text.indexOf(words[i]) === -1) return false;
      return true;
    });
    view.sort(function (a, b) {
      var x = a[sortKey], y = b[sortKey];
      if (sortKey === "src") { x = (sups[a.src] || {}).name; y = (sups[b.src] || {}).name; }
      if (typeof x === "string") return sortDir * x.localeCompare(y, fr ? "fr" : "en");
      return sortDir * (x - y);
    });
    shown = 0; body.innerHTML = ""; draw();
    $all(".tl-card", app).forEach(function (b) { var on = !!cat && b.getAttribute("data-cat") === cat; b.classList.toggle("is-on", on); b.setAttribute("aria-pressed", on ? "true" : "false"); });
  }
  function draw() {
    var next = view.slice(shown, shown + PAGE);
    if (!view.length) body.innerHTML = '<tr><td colspan="7" class="tl-empty">' + (fr ? "Aucun prix ne correspond. Essayez « Tout afficher »." : "No price matches. Try “Show all”.") + "</td></tr>";
    else body.insertAdjacentHTML("beforeend", next.map(rowHtml).join(""));
    shown += next.length;
    more.hidden = shown >= view.length;
    var n = view.length, tot = rows.length;
    count.textContent = fr
      ? (n.toLocaleString("fr-CA") + " prix sur " + tot.toLocaleString("fr-CA") + (n > shown ? " — " + shown + " affichés" : "") + ". Chaque ligne indique la source et la date.")
      : (n.toLocaleString("en-CA") + " of " + tot.toLocaleString("en-CA") + " prices" + (n > shown ? " — " + shown + " shown" : "") + ". Every row names the source and the date.");
  }
  more.addEventListener("click", draw);
  var t = null;
  form.addEventListener("input", function () { clearTimeout(t); t = setTimeout(apply, 120); });
  form.addEventListener("change", apply);
  form.addEventListener("reset", function () { setTimeout(apply, 0); });
  $all(".tl-sort", app).forEach(function (b) {
    b.addEventListener("click", function () {
      var k = b.getAttribute("data-sort");
      if (k === sortKey) sortDir = -sortDir; else { sortKey = k; sortDir = 1; }
      $all(".tl-sort", app).forEach(function (o) { o.removeAttribute("aria-sort"); o.closest("th").removeAttribute("aria-sort"); });
      var v = sortDir === 1 ? "ascending" : "descending"; b.setAttribute("aria-sort", v); b.closest("th").setAttribute("aria-sort", v);
      apply();
    });
  });
  $all(".tl-card", app).forEach(function (b) {
    b.addEventListener("click", function () {
      var c = b.getAttribute("data-cat");
      form.cat.value = form.cat.value === c ? "" : c;
      selectTab("tl-tab-prices", true); apply();
      var top = $(".tl-tabs", app); if (top && top.scrollIntoView) top.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });

  fetch(app.getAttribute("data-json"), { credentials: "same-origin" })
    .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then(function (j) {
      sups = j.suppliers || [];
      (j.categories || []).forEach(function (c) { catName[c.id] = fr ? c.fr : c.en; });
      var ix = {}; (j.cols || []).forEach(function (c, i) { ix[c] = i; });
      rows = j.rows.map(function (a) {
        var s = sups[a[ix.src]] || {};
        var r = { cat: a[ix.cat], name: a[ix.name], spec: a[ix.spec], brand: a[ix.brand], src: a[ix.src], price: a[ix.price], unit: a[ix.unit],
          pack: a[ix.pack], cur: a[ix.cur], orig: a[ix.orig], url: a[ix.url], date: a[ix.date], stock: a[ix.stock], sku: a[ix.sku], reg: regionOf(s) };
        r.text = norm([r.name, r.spec, r.brand, r.sku, s.name, catName[r.cat]].join(" "));
        return r;
      });
      var th = $('.tl-sort[data-sort="unit"]', app); if (th) th.closest("th").setAttribute("aria-sort", "ascending");
      apply();
    })
    .catch(function () {
      count.textContent = fr ? "Le tableau complet n’a pas pu être chargé ; voici un aperçu (les 3 prix les plus bas par catégorie)." : "The full table could not be loaded; here is a preview (the 3 lowest prices per category).";
    });
})();

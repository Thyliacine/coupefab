/* CoupeFab — comparateur de prix (vanilla JS, no deps) */
(function () {
  var app = document.getElementById("prix-app");
  if (!app) return;
  var FR = app.getAttribute("data-lang") !== "en";
  var T = function (fr, en) { return FR ? fr : en; };
  var D, ROWS = [], K = {};
  var sortKey = "spec", sortDir = 1;

  function num(x, d) {
    if (x === null || x === undefined || x === "") return "—";
    d = d === undefined ? 2 : d;
    var s = Number(x).toFixed(d);
    if (FR) { s = s.replace(".", ","); }
    return s.replace(/\B(?=(\d{3})+(?!\d))/g, FR ? "\u202f" : ",");
  }
  function money(x) { return x === null || x === undefined ? "—" : (FR ? num(x) + " $" : "$" + num(x)); }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function el(sel) { return app.querySelector(sel); }

  fetch("/prix/donnees.json").then(function (r) { return r.json(); }).then(function (d) {
    D = d;
    D.keys.forEach(function (k, i) { K[k] = i; });
    ROWS = D.rows.map(function (a) {
      var o = {}; D.keys.forEach(function (k, i) { o[k] = a[i]; }); return o;
    });
    initFilters(); render(); initCalc(); drawChart(); initCoverage();
  }).catch(function () {
    el("#cmp tbody").innerHTML = '<tr><td colspan="10">' + T("Impossible de charger les données.", "Could not load the data.") + "</td></tr>";
  });

  var SHEET = { tole: 1, plaque: 1 };
  function famLabel(f) { return (D.families[f] || [f, f])[FR ? 0 : 1]; }
  function formLabel(f) { return (D.forms[f] || [f, f])[FR ? 0 : 1]; }
  function supName(s) { return (D.suppliers[s] || {}).name || s; }
  function specLabel(r) { return FR ? r.spec_fr : r.spec_en; }
  function buyable(r) { var s = (D.suppliers[r.supplier] || {}).ships_qc; return s === "oui" || s === "cueillette" || s === "a_confirmer"; }

  function opts(select, list, keep) {
    var cur = select.value;
    var first = select.options[0].outerHTML;
    select.innerHTML = first + list.map(function (o) { return '<option value="' + esc(o[0]) + '">' + esc(o[1]) + "</option>"; }).join("");
    if (keep && list.some(function (o) { return o[0] === cur; })) select.value = cur;
  }
  function uniq(arr) { var s = {}; return arr.filter(function (x) { if (s[x]) return false; s[x] = 1; return true; }); }

  var F;
  function filtered(ignore) {
    var v = {
      family: F.family.value, grade: F.grade.value, form: F.form.value, spec: F.spec.value,
      supplier: F.supplier.value, q: F.q.value.trim().toLowerCase(), qc: F.qc.checked, cat: F.cat.checked
    };
    return ROWS.filter(function (r) {
      if (v.family && ignore !== "family" && r.family !== v.family) return false;
      if (v.grade && ignore !== "grade" && r.grade !== v.grade && !(v.grade.indexOf("A500") === 0 && r.grade === "A500")) return false;
      if (ignore !== "form") {
        if (v.form === "all") { /* all forms */ }
        else if (v.form) { if (r.form !== v.form) return false; }
        else if (!SHEET[r.form]) return false;
      }
      if (v.spec && ignore !== "spec" && r.spec !== v.spec) return false;
      if (v.supplier && ignore !== "supplier" && r.supplier !== v.supplier) return false;
      if (v.qc && !buyable(r)) return false;
      if (v.cat && !r.in_catalogue) return false;
      if (v.q) {
        var hay = (r.description + " " + r.grade + " " + specLabel(r) + " " + supName(r.supplier) + " " + r.size_label).toLowerCase();
        if (v.q.split(/\s+/).some(function (w) { return hay.indexOf(w) < 0; })) return false;
      }
      return true;
    });
  }

  function refreshOptions() {
    opts(F.family, uniq(filtered("family").map(function (r) { return r.family; })).map(function (f) { return [f, famLabel(f)]; }), true);
    opts(F.grade, uniq(filtered("grade").map(function (r) { return r.grade; }).filter(Boolean)).sort().map(function (g) { return [g, g]; }), true);
    var specs = {};
    filtered("spec").forEach(function (r) { if (r.spec) specs[r.spec] = [r.spec, specLabel(r), r.thickness_in || 0]; });
    opts(F.spec, Object.keys(specs).map(function (k) { return specs[k]; }).sort(function (a, b) { return a[2] - b[2] || (a[1] < b[1] ? -1 : 1); }), true);
    opts(F.supplier, uniq(filtered("supplier").map(function (r) { return r.supplier; })).map(function (s) { return [s, supName(s)]; }), true);
  }

  function initFilters() {
    var f = document.getElementById("filters");
    F = { family: f.family, grade: f.grade, form: f.form, spec: f.spec, supplier: f.supplier, q: f.q, qc: f.qc, cat: f.cat };
    var forms = uniq(ROWS.map(function (r) { return r.form; }));
    F.form.innerHTML = '<option value="">' + T("Tôle et plaque", "Sheet and plate") + '</option><option value="all">' + T("Toutes les formes", "All forms") + "</option>" +
      Object.keys(D.forms).filter(function (k) { return forms.indexOf(k) >= 0; }).map(function (k) { return '<option value="' + k + '">' + esc(formLabel(k)) + "</option>"; }).join("");
    var params = new URLSearchParams(location.hash.slice(1));
    ["family", "grade", "form", "supplier", "q"].forEach(function (k) { if (params.get(k)) F[k].value = params.get(k); });
    refreshOptions();
    if (params.get("grade")) F.grade.value = params.get("grade");
    f.addEventListener("input", function (e) { if (e.target.name !== "q") refreshOptions(); render(); });
    document.querySelectorAll("#cmp th[data-k] button").forEach(function (b) {
      b.addEventListener("click", function () {
        var k = b.parentNode.getAttribute("data-k");
        if (sortKey === k) sortDir = -sortDir; else { sortKey = k; sortDir = 1; }
        document.querySelectorAll("#cmp th").forEach(function (th) { th.removeAttribute("aria-sort"); });
        b.parentNode.setAttribute("aria-sort", sortDir > 0 ? "ascending" : "descending");
        render();
      });
    });
  }

  function val(r, k) {
    switch (k) {
      case "spec": return [r.spec ? 0 : 1, r.family, SHEET[r.form] ? ({ noir: "0", galv: "1", ar: "2" }[(r.spec || "").split("|")[1]] || (r.spec || "").split("|")[1] || "") : r.form, r.thickness_in || 0, specLabel(r) || ""];
      case "supplier": return supName(r.supplier);
      case "size": return (r.width_in || 0) * (r.length_in || 0) || r.length_ft || 0;
      case "price": return r.price_cad;
      case "cad": return r.price_cad;
      case "sqft": return r.price_per_sqft_cad == null ? Infinity : r.price_per_sqft_cad;
      case "lb": return r.price_per_lb_cad == null ? Infinity : r.price_per_lb_cad;
      case "kg": return r.price_per_kg_cad == null ? Infinity : r.price_per_kg_cad;
      case "ft": return r.price_per_ft_cad == null ? Infinity : r.price_per_ft_cad;
    }
  }
  function sink(r) { return (r.outlier || /rupture/i.test(r.availability || "")) ? 1 : 0; }
  function metric(r) { var m = SHEET[r.form] ? r.price_per_sqft_cad : (r.price_per_ft_cad || r.price_per_lb_cad); return m == null ? Infinity : m; }
  function cmp(a, b) {
    var sa = sink(a), sb = sink(b);
    if (sa !== sb) return sa - sb;
    var c = cmp0(a, b);
    if (c === 0 && sortKey === "spec") { var ma = metric(a), mb = metric(b); return ma < mb ? -1 : ma > mb ? 1 : 0; }
    return c;
  }
  function cmp0(a, b) {
    var x = val(a, sortKey), y = val(b, sortKey);
    if (Array.isArray(x)) {
      for (var i = 0; i < x.length; i++) { if (x[i] < y[i]) return -sortDir; if (x[i] > y[i]) return sortDir; }
      return 0;
    }
    if (x === y) return 0;
    if (x === Infinity) return 1; if (y === Infinity) return -1;
    return (x < y ? -1 : 1) * sortDir;
  }

  var LIMIT = 300;
  function render() {
    var rows = filtered().sort(cmp);
    var shown = rows.slice(0, LIMIT);
    var unitLbl = { each: T("/ unité", "/ each"), lb: "/lb", sqft: T("/pi²", "/sq ft"), ft: T("/pi", "/ft") };
    var html = shown.map(function (r) {
      var cls = r.best ? ' class="is-best"' : (r.outlier ? ' class="is-outlier"' : "");
      var flag = r.best ? ' <span class="badge best">' + T("meilleur prix", "best price") + "</span>" : "";
      if (r.outlier) flag += ' <span class="badge warn">' + T("à vérifier", "to check") + "</span>";
      if (r.availability && /rupture/i.test(r.availability)) flag += ' <span class="badge muted">' + T("rupture", "out of stock") + "</span>";
      var size = r.width_in && r.length_in ? (num(r.width_in, 0) + " × " + num(r.length_in, 0) + T(" po", " in")) : (r.size_label || "");
      var listed = (r.currency === "USD" ? "US" : "") + money(r.price) + " " + (unitLbl[r.unit] || "");
      var date = (r.fetched_at || "").slice(0, 10);
      return "<tr" + cls + "><td><span class=\"spec\">" + esc(specLabel(r) || r.description) + "</span>" + flag +
        '<br><span class="desc">' + esc(r.grade ? r.grade + " · " : "") + esc(r.description) + "</span></td>" +
        "<td>" + esc(supName(r.supplier)) + "</td><td>" + esc(size) + "</td>" +
        '<td class="num">' + esc(listed) + '</td><td class="num">' + money(r.price_cad) + "</td>" +
        '<td class="num">' + num(r.price_per_sqft_cad) + '</td><td class="num">' + num(r.price_per_lb_cad) + "</td>" +
        '<td class="num">' + num(r.price_per_kg_cad) + '</td><td class="num">' + num(r.price_per_ft_cad) + "</td>" +
        '<td><a href="' + esc(r.url) + '" rel="nofollow noopener" target="_blank">' + T("source", "source") + "</a><br><span class=\"desc\">" + date +
        (r.source_updated ? T(" · liste du ", " · list of ") + esc(r.source_updated) : "") + "</span></td></tr>";
    }).join("");
    document.querySelector("#cmp tbody").innerHTML = html || '<tr><td colspan="10">' + T("Aucun prix publié pour ces filtres : sur demande.", "No published price for these filters: quote only.") + "</td></tr>";
    document.getElementById("count").textContent = rows.length + T(" prix", " prices") + (rows.length > LIMIT ? T(" (300 premiers affichés : précisez les filtres)", " (first 300 shown: narrow the filters)") : "");
  }

  /* ---------- Calculator ---------- */
  function initCalc() {
    var c = document.getElementById("calc");
    var fams = uniq(ROWS.filter(function (r) { return SHEET[r.form] && r.price_per_sqft_cad; }).map(function (r) { return r.family; }));
    fams.sort(function (a, b) { return a === "acier" ? -1 : b === "acier" ? 1 : 0; });
    c.family.innerHTML = fams.map(function (f) { return '<option value="' + f + '">' + esc(famLabel(f)) + "</option>"; }).join("");
    function fillSpecs() {
      var specs = {};
      ROWS.forEach(function (r) {
        if (r.family === c.family.value && SHEET[r.form] && r.spec && r.price_per_sqft_cad && !r.outlier) specs[r.spec] = [r.spec, specLabel(r), r.thickness_in];
      });
      var list = Object.keys(specs).map(function (k) { return specs[k]; }).sort(function (a, b) { return a[2] - b[2]; });
      var cur = c.spec.value;
      c.spec.innerHTML = list.map(function (s) { return '<option value="' + esc(s[0]) + '">' + esc(s[1]) + "</option>"; }).join("");
      var dflt = list.filter(function (s) { return Math.abs(s[2] - 0.0747) < 0.003; })[0];
      if (list.some(function (s) { return s[0] === cur; })) c.spec.value = cur; else if (dflt) c.spec.value = dflt[0];
    }
    function calc() {
      var unit = c.unit.value, k = unit === "mm" ? 1 / 25.4 : 1;
      var w = parseFloat(c.w.value) * k, l = parseFloat(c.l.value) * k, q = Math.max(1, parseInt(c.qty.value, 10) || 1);
      var kerf = (parseFloat(c.kerf.value) || 0) / 25.4, waste = (parseFloat(c.waste.value) || 0) / 100;
      var rows = ROWS.filter(function (r) { return r.spec === c.spec.value && r.price_per_sqft_cad && !r.outlier && !/rupture/i.test(r.availability || ""); });
      var out = document.getElementById("calc-out");
      if (!(w > 0 && l > 0) || !rows.length) { out.innerHTML = ""; return; }
      var t = rows[0].thickness_in, fam = c.family.value;
      var dens = D.density[fam];
      var partLb = dens * t * w * l, totLb = partLb * q;
      var areaSqft = (w + kerf) * (l + kerf) * q / 144 / Math.max(0.1, 1 - waste);
      var per = {};
      rows.forEach(function (r) {
        var p = per[r.supplier];
        if (!p || r.price_per_sqft_cad < p.price_per_sqft_cad) per[r.supplier] = r;
      });
      var list = Object.keys(per).map(function (s) { return per[s]; }).sort(function (a, b) { return a.price_per_sqft_cad - b.price_per_sqft_cad; });
      var sheets = Math.ceil(areaSqft / 32);
      var h = '<div class="calc-kpis"><div><b>' + num(totLb, 1) + " lb</b><span>" + num(totLb / 2.20462, 1) + " kg " + T("net (", "net (") + q + " × " + num(partLb, 2) + " lb)</span></div>" +
        "<div><b>" + num(areaSqft, 2) + T(" pi²", " sq ft") + "</b><span>" + T("surface consommée", "consumed area") + " (" + num(areaSqft * 0.092903, 3) + " m²)</span></div>" +
        "<div><b>" + sheets + "</b><span>" + T("feuille(s) 48 × 96 po équivalente(s)", "equivalent 48 × 96 in sheet(s)") + "</span></div></div>";
      h += '<div class="table-wrap"><table><thead><tr><th>' + T("Fournisseur", "Supplier") + "</th><th>" + T("Nuance · format", "Grade · size") + '</th><th class="num">$/' + T("pi²", "sq ft") + '</th><th class="num">' + T("Coût matière estimé", "Estimated material cost") + "</th></tr></thead><tbody>";
      list.forEach(function (r, i) {
        h += "<tr" + (i === 0 ? ' class="is-best"' : "") + "><td>" + esc(supName(r.supplier)) + (buyable(r) ? "" : ' <span class="badge muted">' + T("hors QC", "outside QC") + "</span>") + "</td><td>" + esc(r.grade) + " · " + esc(FR ? r.size_label : String(r.size_label).replace(/ po\b/g, " in")) + '</td><td class="num">' + num(r.price_per_sqft_cad) + '</td><td class="num"><b>' + money(areaSqft * r.price_per_sqft_cad) + "</b></td></tr>";
      });
      h += "</tbody></table></div>";
      out.innerHTML = h;
    }
    c.family.addEventListener("change", function () { fillSpecs(); calc(); });
    c.addEventListener("input", calc);
    fillSpecs(); calc();
  }

  /* ---------- Trend chart (SVG) ---------- */
  function drawChart() {
    var box = document.getElementById("chart");
    var idx = (D.index || []).filter(function (x) { return x.form_group === "feuille_plaque"; });
    if (!idx.length) { box.textContent = T("Pas encore d’historique.", "No history yet."); return; }
    var dates = uniq(idx.map(function (x) { return x.date; })).sort();
    var fams = uniq(idx.map(function (x) { return x.family; }));
    var colors = { acier: "#2e3a3a", inox: "#1b4f8a", aluminium: "#b54300", cuivre: "#8c5a00", laiton: "#a68a00", bronze: "#6b3e26", bronze_alu: "#5c6b00" };
    var W = 720, H = 260, P = { l: 52, r: 16, t: 16, b: 36 };
    var ys = idx.map(function (x) { return +x.median_cad_per_lb; });
    var ymax = Math.max.apply(null, ys) * 1.1, ymin = 0;
    var step = Math.pow(10, Math.floor(Math.log10(ymax / 4))); var st = [1, 2, 2.5, 5, 10].map(function (m) { return m * step; }).filter(function (v) { return v * 4 >= ymax; })[0] || step * 10; ymax = st * 4;
    var xs = function (d) { var i = dates.indexOf(d); return dates.length === 1 ? (P.l + (W - P.l - P.r) / 2) : P.l + i * (W - P.l - P.r) / (dates.length - 1); };
    var yv = function (v) { return H - P.b - (v - ymin) / (ymax - ymin) * (H - P.t - P.b); };
    var s = '<svg viewBox="0 0 ' + W + " " + H + '" width="100%" preserveAspectRatio="xMidYMid meet">';
    for (var g = 0; g <= 4; g++) {
      var v = ymin + (ymax - ymin) * g / 4, y = yv(v);
      s += '<line x1="' + P.l + '" x2="' + (W - P.r) + '" y1="' + y + '" y2="' + y + '" stroke="#d5d0c4"/>';
      s += '<text x="' + (P.l - 6) + '" y="' + (y + 4) + '" text-anchor="end" font-size="11" fill="#5a5f57">' + num(v) + "</text>";
    }
    dates.forEach(function (d, i) {
      if (dates.length < 8 || i % Math.ceil(dates.length / 6) === 0) s += '<text x="' + xs(d) + '" y="' + (H - 12) + '" text-anchor="middle" font-size="11" fill="#5a5f57">' + d + "</text>";
    });
    var legend = "";
    fams.forEach(function (f) {
      var pts = idx.filter(function (x) { return x.family === f; }).sort(function (a, b) { return a.date < b.date ? -1 : 1; });
      var col = colors[f] || "#444";
      if (pts.length > 1) s += '<polyline fill="none" stroke="' + col + '" stroke-width="2.5" points="' + pts.map(function (p) { return xs(p.date) + "," + yv(+p.median_cad_per_lb); }).join(" ") + '"/>';
      pts.forEach(function (p) { s += '<circle cx="' + xs(p.date) + '" cy="' + yv(+p.median_cad_per_lb) + '" r="4" fill="' + col + '"><title>' + esc(famLabel(f)) + " " + p.date + " : " + num(+p.median_cad_per_lb) + " $/lb (n=" + p.n_rows + ")</title></circle>"; });
      var last = pts[pts.length - 1];
      legend += '<span><i style="background:' + col + '"></i>' + esc(famLabel(f)) + " " + num(+last.median_cad_per_lb) + " $/lb</span>";
    });
    s += "</svg>";
    box.innerHTML = s + '<div class="legend">' + legend + "</div>";
  }

  function initCoverage() {
    document.querySelectorAll(".grade-pick").forEach(function (b) {
      b.addEventListener("click", function () {
        F.family.value = ""; F.grade.value = ""; F.spec.value = ""; F.supplier.value = ""; F.q.value = "";
        F.form.value = "all"; F.cat.checked = false;
        refreshOptions();
        F.family.value = b.getAttribute("data-family"); refreshOptions();
        F.grade.value = b.getAttribute("data-grade"); refreshOptions();
        render();
        document.getElementById("comparateur").scrollIntoView({ behavior: "smooth" });
      });
    });
  }
})();

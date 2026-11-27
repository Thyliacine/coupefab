/* CoupeFab — comparateur de prix des métaux (vanilla JS, no deps).
   Loads the sheet/plate file first (small), the full file only when bar/tube/pipe are asked for. */
(function () {
  "use strict";
  var app = document.getElementById("prix-app");
  if (!app) return;
  var FR = app.getAttribute("data-lang") !== "en";
  var T = function (fr, en) { return FR ? fr : en; };
  var D = null, ROWS = [], FULL = false, loadingFull = null;
  var sortKey = "spec", sortDir = 1, LIMIT = 150, shown = LIMIT;
  var SHEET = { tole: 1, plaque: 1 };
  var TABS = [["comparer", "compare"], ["calculateur", "calculator"], ["tendances", "trends"], ["alliages", "grades"], ["methode", "method"]];
  var ALIAS = { comparateur: 0, meilleurs: 0, tendance: 2, catalogue: 3, calibres: 3, nuances: 3, fournisseurs: 4, alerte: 4 };
  var TIER = {
    best: T("Meilleur prix", "Best price"), good: T("Bon prix", "Good price"), avg: T("Dans la moyenne", "Average"),
    high: T("Cher", "Expensive"), ref: T("Repère", "Benchmark"), oos: T("Rupture", "Out of stock"), check: T("À vérifier", "To check"),
    surplus: T("Surplus / indicatif", "Surplus / indicative")
  };
  var SHIP = {
    oui: T("Livre au Québec", "Ships to Quebec"), cueillette: T("Cueillette au Québec", "Pickup in Quebec"),
    indicatif: T("Prix indicatif", "Indicative price"), a_confirmer: T("Livraison à confirmer", "Shipping TBC"),
    non: T("Repère hors Québec", "Benchmark, outside QC"), repere: T("Repère hors Québec", "Benchmark, outside QC")
  };

  /* ---------- formatting ---------- */
  function num(x, d) {
    if (x === null || x === undefined || x === "" || isNaN(x)) return "—";
    d = d === undefined ? 2 : d;
    var s = Number(x).toFixed(d), parts = s.split(".");
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, FR ? "\u202f" : ",");
    return parts.join(FR ? "," : ".");
  }
  function money(x, d) { return x == null ? "—" : (FR ? num(x, d) + "\u00a0$" : "$" + num(x, d)); }
  function pctTxt(p) { if (p == null) return ""; var s = (p > 0 ? "+" : p < 0 ? "−" : "±") + num(Math.abs(p), 0); return FR ? s + "\u00a0%" : s + "%"; }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function gradeTxt(g) { return String(g || "").replace(/(nuance|alliage) non précisée?/gi, T("alliage non précisé", "grade not specified")); }
  function inch(s) { return FR ? s : String(s || "").replace(/ po\b/g, " in"); }
  function uniq(arr) { var s = {}; return arr.filter(function (x) { if (x == null || s[x]) return false; s[x] = 1; return true; }); }
  function dateShort(iso) {
    if (!iso) return "";
    var d = new Date(iso.slice(0, 10) + "T12:00:00");
    return d.toLocaleDateString(FR ? "fr-CA" : "en-CA", { day: "numeric", month: "short", year: "numeric" });
  }

  /* ---------- tabs (hash per tab, ARIA, arrow keys) ---------- */
  var tabs = [].slice.call(app.querySelectorAll('[role="tab"]'));
  var panels = [].slice.call(app.querySelectorAll(".px-panel"));
  var cur = +(app.getAttribute("data-tab") || 0);
  function hashParts() {
    var h = location.hash.slice(1), i = h.indexOf("?");
    return { tab: (i < 0 ? h : h.slice(0, i)).toLowerCase(), q: new URLSearchParams(i < 0 ? "" : h.slice(i + 1)) };
  }
  function tabIndex(name) {
    for (var i = 0; i < TABS.length; i++) if (TABS[i][0] === name || TABS[i][1] === name) return i;
    return ALIAS[name] !== undefined ? ALIAS[name] : -1;
  }
  function tabId(i) { return TABS[i][FR ? 0 : 1]; }
  function show(i, opts) {
    opts = opts || {};
    cur = i; app.setAttribute("data-tab", i);
    tabs.forEach(function (t, k) { t.setAttribute("aria-selected", k === i ? "true" : "false"); t.tabIndex = k === i ? 0 : -1; });
    panels.forEach(function (p, k) { p.classList.toggle("is-active", k === i); });
    if (opts.push !== false && window.cfFlash) window.cfFlash(panels[i]);
    if (opts.focus) tabs[i].focus();
    if (opts.push !== false) writeHash(opts.push === "push");
    if (i === 2) drawChart();
    if (opts.scroll) { var nav = app.querySelector(".px-tabs"); var y = nav.getBoundingClientRect().top + window.scrollY - headerH() - 8; if (window.scrollY > y || opts.scroll === "force") window.scrollTo({ top: y, behavior: "smooth" }); }
  }
  tabs.forEach(function (t, k) {
    t.addEventListener("click", function (e) { e.preventDefault(); show(k, { push: "push" }); });
    t.addEventListener("keydown", function (e) {
      var n = { ArrowRight: k + 1, ArrowLeft: k - 1, Home: 0, End: tabs.length - 1 }[e.key];
      if (n === undefined) return;
      e.preventDefault(); show((n + tabs.length) % tabs.length, { focus: true });
    });
  });
  window.addEventListener("popstate", function () { var hp = hashParts(), i = tabIndex(hp.tab); if (i >= 0) { show(i, { push: false }); if (i === 0 && D) { applyQuery(hp.q); (needFull() ? ensureFull() : Promise.resolve()).then(function () { applyQuery(hp.q); refreshOptions(); applyQuery(hp.q); render(); }); } } });
  // the inline boot script runs before the tabs exist: apply the deep-linked tab (#tendances…) now
  show(cur, { push: false });
  function headerH() { var h = document.querySelector(".hdr, .site-header, body > header"); if (!h) return 0; var cs = getComputedStyle(h); return cs.position === "sticky" || cs.position === "fixed" ? h.offsetHeight : 0; }
  function setHeaderVar() { app.style.setProperty("--px-top", headerH() + "px"); }
  setHeaderVar(); window.addEventListener("resize", setHeaderVar);

  /* ---------- data ---------- */
  var S = document.getElementById("px-search");
  var F = { q: S.q, family: S.family, grade: S.grade, form: S.form, spec: S.spec, size: S.size, qc: S.qc, cmp: S.cmp, cat: S.cat };
  function ingest(d) {
    D = d; FULL = d.part === "all";
    ROWS = d.rows.map(function (a) { var o = {}; d.keys.forEach(function (k, i) { o[k] = a[i]; }); return o; });
  }
  function needFull() {
    var v = F.form.value;
    // a bar/tube spec (family|group|form|section), a non-sheet form, or a free-text search needs the full file
    return (v && v !== "sheet" && !SHEET[v]) || (F.spec.value.split("|").length > 3) || !!F.q.value.trim();
  }
  function ensureFull() {
    if (FULL) return Promise.resolve();
    if (!loadingFull) {
      setCount(T("Chargement des barres, tubes et tuyaux…", "Loading bar, tube and pipe…"));
      loadingFull = fetch("/prix/donnees.json").then(function (r) { return r.json(); }).then(function (d) { ingest(d); initFormOptions(); });
    }
    return loadingFull;
  }
  (window.__pxData || fetch("/prix/donnees-toles.json").then(function (r) { return r.json(); })).then(function (d) {
    ingest(d);
    initFormOptions();
    var hp = hashParts();
    applyQuery(hp.q);
    var go = needFull() ? ensureFull() : Promise.resolve();
    go.then(function () { applyQuery(hp.q); refreshOptions(); applyQuery(hp.q); render(); });
    initCalc(); initCoverage(); initCards();
    // "Toutes" shows sheet and plate first (small file); bar, tube and pipe load when the table comes into view
    var lazyFull = function () { ensureFull().then(function () { refreshOptions(); render(); }); };
    if (!FULL && "IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (es) { if (es.some(function (x) { return x.isIntersecting; })) { io.disconnect(); lazyFull(); } }, { rootMargin: "200px" });
      io.observe(document.getElementById("px-table-wrap"));
    } else if (!FULL) lazyFull();
    if (cur === 2) drawChart();
  }).catch(function (e) {
    app.querySelector("#px-table tbody").innerHTML = '<tr><td colspan="7">' + T("Impossible de charger les données. Le CSV reste disponible plus bas.", "Could not load the data. The CSV is still available below.") + "</td></tr>";
    if (window.console) console.error(e);
  });

  function sup(r) { return D.suppliers[r.supplier] || {}; }
  function supName(r) { return sup(r).name || r.supplier; }
  function famLabel(f) { return (D.families[f] || [f, f])[FR ? 0 : 1]; }
  function formLabel(f) { return (D.forms[f] || [f, f])[FR ? 0 : 1]; }
  function specLabel(r) { return FR ? r.spec_fr : r.spec_en; }
  function buyable(r) { var s = sup(r).ships_qc; return s === "oui" || s === "cueillette" || s === "a_confirmer"; }
  function sizeOf(r) {
    if (r.width_in && r.length_in) return num(r.width_in, r.width_in % 1 ? 1 : 0) + " × " + num(r.length_in, r.length_in % 1 ? 1 : 0) + T(" po", " in");
    if (r.length_ft) return num(r.length_ft, r.length_ft % 1 ? 1 : 0) + T(" pi", " ft");
    if (r.unit === "sqft") return T("Au pi² (sur mesure)", "Per sq ft (cut to size)");
    if (r.unit === "ft") return T("Au pied (sur mesure)", "Per foot (cut to length)");
    if (r.unit === "lb") return T("À la livre", "Per pound");
    return inch(r.size_label || "");
  }
  function munit(r) { return r.munit === "sqft" ? T("/pi²", "/sq ft") : r.munit === "ft" ? T("/pi", "/ft") : "/lb"; }
  function action(r) {
    var s = sup(r);
    if (s.ships_qc === "indicatif") return { kind: "quote", url: s.quote_url || r.url, label: T("Demander un prix", "Request a quote") };
    if (s.ships_qc === "oui") return { kind: "buy", url: r.buy_url || r.url, label: T("Acheter", "Buy") };
    return { kind: "see", url: r.buy_url || r.url, label: T("Voir chez ", "View at ") + s.name };
  }

  /* ---------- filters ---------- */
  function opts(select, list) {
    var v = select.value, first = select.options[0].outerHTML;
    select.innerHTML = first + list.map(function (o) { return '<option value="' + esc(o[0]) + '">' + esc(o[1]) + "</option>"; }).join("");
    if (list.some(function (o) { return o[0] === v; })) select.value = v;
  }
  function initFormOptions() {
    var forms = uniq(ROWS.map(function (r) { return r.form; }));
    var v = F.form.value;
    var all = Object.keys(D.forms).filter(function (k) { return !FULL || forms.indexOf(k) >= 0; });
    F.form.innerHTML = '<option value="">' + T("Toutes", "All") + '</option><option value="sheet">' + T("Tôle et plaque (toutes)", "Sheet and plate (all)") + "</option>" +
      all.map(function (k) { return '<option value="' + k + '">' + esc(formLabel(k)) + "</option>"; }).join("");
    if (v === "all") v = "";
    if (v) F.form.value = v;
  }
  function filtered(ignore) {
    var v = { family: F.family.value, grade: F.grade.value, form: F.form.value, spec: F.spec.value, size: F.size.value, q: F.q.value.trim().toLowerCase() };
    var words = v.q ? v.q.replace(/,/g, ".").split(/\s+/) : [];
    return ROWS.filter(function (r) {
      if (v.family && ignore !== "family" && r.family !== v.family) return false;
      if (v.grade && ignore !== "grade" && r.grade !== v.grade && !(v.grade.indexOf("A500") === 0 && r.grade === "A500")) return false;
      if (ignore !== "form") {
        if (!v.form || v.form === "all") { /* all forms */ } else if (v.form === "sheet") { if (!SHEET[r.form]) return false; } else if (r.form !== v.form) return false;
      }
      if (v.spec && ignore !== "spec" && r.spec !== v.spec) return false;
      if (v.size && ignore !== "size" && sizeOf(r) !== v.size) return false;
      if (F.qc.checked && !buyable(r)) return false;
      if (F.cat.checked && !r.in_catalogue) return false;
      if (F.cmp.checked && (!r.tier || r.tier === "surplus")) return false;
      if (words.length) {
        var hay = (r.description + " " + r.grade + " " + specLabel(r) + " " + supName(r) + " " + r.size_label + " " + (r.gauge ? r.gauge + " ga" : "")).toLowerCase().replace(/,/g, ".");
        for (var i = 0; i < words.length; i++) if (hay.indexOf(words[i]) < 0 && hay.indexOf(words[i].replace(/^0\./, ".")) < 0) return false;
      }
      return true;
    });
  }
  function refreshOptions() {
    opts(F.family, uniq(filtered("family").map(function (r) { return r.family; })).sort(function (a, b) { return a === "acier" ? -1 : b === "acier" ? 1 : famLabel(a).localeCompare(famLabel(b)); }).map(function (f) { return [f, famLabel(f)]; }));
    opts(F.grade, uniq(filtered("grade").map(function (r) { return r.grade; })).sort().map(function (g) { return [g, gradeTxt(g)]; }));
    var specs = {};
    filtered("spec").forEach(function (r) {
      if (!r.spec) return;
      var n = Math.max(r.n_src || 1, specs[r.spec] ? specs[r.spec][3] : 0);
      specs[r.spec] = [r.spec, specLabel(r), r.thickness_in || 0, n];
    });
    Object.keys(specs).forEach(function (k) { var s = specs[k]; s[1] = s[1] + " · " + s[3] + T(s[3] > 1 ? " fournisseurs" : " fournisseur", s[3] > 1 ? " suppliers" : " supplier"); });
    opts(F.spec, Object.keys(specs).map(function (k) { return specs[k]; }).sort(function (a, b) { return a[2] - b[2] || (a[1] < b[1] ? -1 : 1); }));
    var sizes = {};
    filtered("size").forEach(function (r) { var s = sizeOf(r); if (s) sizes[s] = (r.width_in || 0) * (r.length_in || 0) || (r.length_ft || 0); });
    opts(F.size, Object.keys(sizes).sort(function (a, b) { return sizes[a] - sizes[b]; }).map(function (s) { return [s, s]; }));
  }
  function applyQuery(q) {
    ["family", "grade", "form", "spec", "size", "q"].forEach(function (k) { if (q.has(k)) F[k].value = q.get(k); });
    var sp = (q.get("spec") || "").split("|");
    if (sp.length > 3 && !q.get("form")) q.set("form", sp[2]);
    if (q.get("form") === "all") q.delete("form");
    if (q.get("form") && F.form.value !== q.get("form")) { F.form.insertAdjacentHTML("beforeend", '<option value="' + esc(q.get("form")) + '">' + esc(q.get("form")) + "</option>"); F.form.value = q.get("form"); }
    if (q.get("spec") && F.spec.value !== q.get("spec")) { F.spec.insertAdjacentHTML("beforeend", '<option value="' + esc(q.get("spec")) + '"></option>'); F.spec.value = q.get("spec"); }
    if (q.get("grade") && F.grade.value !== q.get("grade")) { F.grade.insertAdjacentHTML("beforeend", '<option value="' + esc(q.get("grade")) + '"></option>'); F.grade.value = q.get("grade"); }
    if (q.has("all")) F.qc.checked = false;
  }
  function writeHash(push) {
    var p = new URLSearchParams();
    if (cur === 0) ["family", "grade", "form", "spec", "size", "q"].forEach(function (k) { if (F[k].value) p.set(k, F[k].value); });
    if (cur === 0 && !F.qc.checked) p.set("all", "1");
    var h = "#" + tabId(cur) + (p.toString() ? "?" + p.toString() : "");
    if (h !== location.hash) history[push ? "pushState" : "replaceState"](null, "", h);
  }
  // mobile: dropdowns fold behind a "Filtres" button so prices sit above the fold
  var ftog = S.querySelector(".px-ftog");
  function syncTog() {
    if (!ftog) return;
    var n = ["family", "grade", "form", "spec", "size"].filter(function (k) { return F[k].value; }).length;
    ftog.querySelector("[data-nf]").textContent = n ? "(" + n + ")" : "";
  }
  if (ftog) {
    S.classList.add("is-collapsible");
    ftog.addEventListener("click", function () {
      var open = ftog.getAttribute("aria-expanded") !== "true";
      ftog.setAttribute("aria-expanded", open ? "true" : "false");
      S.classList.toggle("is-open", open);
    });
    S.addEventListener("change", syncTog);
  }
  var tmr;
  S.addEventListener("input", function (e) {
    if (cur !== 0) show(0, { push: "push", scroll: true });
    clearTimeout(tmr);
    var go = function () {
      shown = LIMIT;
      ensureFull().then(function () { refreshOptions(); render(); writeHash(false); });
    };
    if (e.target.name === "q") tmr = setTimeout(go, 120); else go();
  });
  [F.qc, F.cmp, F.cat].forEach(function (cb) { cb.addEventListener("change", function () { shown = LIMIT; refreshOptions(); render(); writeHash(false); }); });
  app.querySelector("[data-reset]").addEventListener("click", function () {
    ["family", "grade", "form", "spec", "size", "q"].forEach(function (k) { F[k].value = ""; });
    F.cmp.checked = false; F.cat.checked = false; F.qc.checked = true;
    shown = LIMIT; refreshOptions(); render(); writeHash(false);
  });
  var sortSel = document.getElementById("px-sort");
  function setSort(k, dir) {
    sortKey = k; sortDir = dir || 1; sortSel.value = k;
    app.querySelectorAll("#px-table th[data-k]").forEach(function (th) {
      if (th.getAttribute("data-k") === k) th.setAttribute("aria-sort", sortDir > 0 ? "ascending" : "descending"); else th.removeAttribute("aria-sort");
    });
    render();
  }
  sortSel.addEventListener("change", function () { setSort(sortSel.value, 1); });
  app.querySelectorAll("#px-table th[data-k] button").forEach(function (b) {
    b.addEventListener("click", function () { var k = b.parentNode.getAttribute("data-k"); setSort(k, sortKey === k ? -sortDir : 1); });
  });
  document.getElementById("px-more").addEventListener("click", function () { shown += LIMIT * 2; render(); });

  /* ---------- table ---------- */
  var SUBORD = { noir: "0", galv: "1", ar: "2" };
  function inf(x) { return x == null ? Infinity : x; }
  function val(r, k) {
    switch (k) {
      case "spec": return [r.spec ? 0 : 1, r.family === "acier" ? "0" : r.family, SHEET[r.form] ? "0" : r.form, SHEET[r.form] ? (SUBORD[(r.spec || "").split("|")[1]] || (r.spec || "").split("|")[1] || "") : (r.grade || ""), r.thickness_in || 0, specLabel(r) || ""];
      case "supplier": return supName(r);
      case "size": return (r.width_in || 0) * (r.length_in || 0) || r.length_ft || 0;
      case "price": return inf(r.price_cad);
      case "metric": return inf(r.metric);
      case "pct": return inf(r.pct);
      case "lb": return inf(r.price_per_lb_cad);
    }
  }
  function sink(r) { return (r.tier === "check" || r.tier === "oos" || /rupture/i.test(r.availability || "")) ? 1 : 0; }
  function cmp(a, b) {
    var sa = sink(a), sb = sink(b);
    if (sa !== sb) return sa - sb;
    var x = val(a, sortKey), y = val(b, sortKey), c = 0;
    if (Array.isArray(x)) { for (var i = 0; i < x.length && !c; i++) c = x[i] < y[i] ? -1 : x[i] > y[i] ? 1 : 0; c *= sortDir; }
    else if (x !== y) c = x === Infinity ? 1 : y === Infinity ? -1 : (x < y ? -1 : 1) * sortDir;
    if (!c) { var ma = inf(a.metric), mb = inf(b.metric); c = ma < mb ? -1 : ma > mb ? 1 : 0; }
    return c;
  }
  function setCount(t) { document.getElementById("px-count").textContent = t; }
  /* "Affiché : Aluminium · Toutes les formes …" — the current filter, always visible above the table */
  var lastShowing = null;
  function optText(sel) {
    var o = sel.options[sel.selectedIndex];
    return o ? o.textContent.split(" · ")[0].replace(/\s*\(\d[\d\s ]*\)$/, "") : "";
  }
  function setShowing() {
    var el = document.getElementById("px-showing");
    if (!el) return;
    var tags = [];
    function tag(on, txt) { tags.push('<span class="cf-tag' + (on ? "" : " is-all") + '">' + esc(txt) + "</span>"); }
    tag(!!F.family.value, F.family.value ? optText(F.family) : T("Tous les métaux", "All metals"));
    if (F.grade.value) tag(true, optText(F.grade));
    var fv = F.form.value;
    tag(!!fv && fv !== "all", fv && fv !== "all" ? optText(F.form) : T("Toutes les formes", "All forms"));
    if (F.spec.value) tag(true, optText(F.spec));
    if (F.size.value) tag(true, optText(F.size));
    if (F.q.value.trim()) tag(true, "« " + F.q.value.trim() + " »");
    if (F.qc.checked) tag(true, T("Achetable au Québec", "Buyable in Quebec"));
    if (F.cmp.checked) tag(true, T("Comparables seulement", "Comparable only"));
    if (F.cat.checked) tag(true, T("Matériaux courants", "Common materials"));
    var html = "<b>" + T("Affiché :", "Showing:") + "</b>" + tags.join("");
    if (html === lastShowing) return;
    var first = lastShowing === null;
    el.innerHTML = html; lastShowing = html;
    if (!first && window.cfFlash) { window.cfFlash(el); window.cfFlash(document.getElementById("px-table-wrap")); }
  }
  function nsrc(r) {
    var n = r.n_src || 1;
    return '<span class="px-nsrc" title="' + esc(T("Nombre de fournisseurs qui publient un prix pour cette spécification", "Number of suppliers publishing a price for this spec")) + '">' + n + T(n > 1 ? " fournisseurs" : " fournisseur", n > 1 ? " suppliers" : " supplier") + "</span>";
  }
  function nearHtml(r) {
    var list = (D.near || {})[r.spec];
    if (!list || !list.length) return "";
    return '<details class="px-near"><summary>' + T("Specs proches comparables", "Nearby comparable specs") + "</summary><ul>" + list.map(function (m) {
      return '<li><a href="#" data-spec="' + esc(m[0]) + '">' + esc(FR ? m[1] : m[2]) + "</a> <small>" + T("dès ", "from ") + money(m[3]) + munitRaw(m[4]) + " · " + m[5] + T(" fourn.", " suppl.") + "</small></li>";
    }).join("") + "</ul></details>";
  }
  function badge(r) {
    if (!r.tier) return '<span class="px-solo">' + T("Seul prix publié", "Only published price") + "</span>" + nsrc(r) + nearHtml(r);
    if (r.tier === "surplus") return '<span class="px-tier px-t-surplus" title="' + esc(T("Surplus / déstockage : affiché, mais exclu de la médiane et du « Meilleur prix »", "Surplus / clearance: shown, but excluded from the median and from “Best price”")) + '">' + TIER.surplus + "</span>" + nsrc(r) + nearHtml(r);
    var p = r.pct != null && r.tier !== "check" ? '<span class="px-pct">' + pctTxt(r.pct) + "</span>" : "";
    var title = r.median ? ' title="' + esc(T("Médiane ", "Median ") + money(r.median) + munit(r) + " · " + r.n_suppliers + T(" fournisseurs", " suppliers")) + '"' : "";
    return '<span class="px-tier px-t-' + r.tier + '"' + title + ">" + TIER[r.tier] + "</span>" + p + nsrc(r);
  }
  function groupHead(r, m) {
    var n = r.n_src || 1;
    var mr = r.median != null ? r : m;
    var med = mr ? " · " + T("médiane ", "median ") + money(mr.median) + munit(mr) : "";
    return '<tr class="px-g"><th colspan="7" scope="rowgroup"><span class="px-g-t">' + esc(specLabel(r) || r.description) + '</span> <span class="px-g-m">' + n + T(n > 1 ? " fournisseurs" : " fournisseur", n > 1 ? " suppliers" : " supplier") + med + "</span></th></tr>";
  }
  function row(r, grouped) {
    var s = sup(r), a = action(r);
    var usd = r.currency === "USD";
    var listed = usd ? '<small>US' + money(r.price) + (r.unit && r.unit !== "each" ? munitRaw(r.unit) : "") + "</small>" : (r.unit && r.unit !== "each" ? "<small>" + money(r.price) + munitRaw(r.unit) + "</small>" : "");
    var chips = '<span class="px-chip px-ship-' + esc(s.ships_qc) + '">' + esc(SHIP[s.ships_qc] || "") + "</span>" + (usd ? ' <span class="px-chip px-chip-usd" title="' + esc(T("Converti en CAD. Ajoutez transport transfrontalier, courtage et droits/surtaxes éventuels.", "Converted to CAD. Add cross-border freight, brokerage and any duties/surtaxes.")) + '">USD</span>' : "");
    var lb = r.price_per_lb_cad != null && r.munit !== "lb" ? "<small>" + money(r.price_per_lb_cad) + "/lb</small>" : "";
    var btn = '<a class="px-btn px-btn-' + a.kind + '" href="' + esc(a.url) + '" target="_blank" rel="noopener nofollow">' + esc(a.label) + ' <span aria-hidden="true">↗</span></a>';
    var src = '<a class="px-src" href="' + esc(r.url) + '" target="_blank" rel="noopener nofollow">' + T("source", "source") + "</a> · " + esc(dateShort(r.fetched_at)) + (r.source_updated ? T(" (liste du ", " (list of ") + esc(r.source_updated) + ")" : "");
    var cls = "px-r px-r-" + (r.tier || "none");
    return '<tr class="' + cls + '">' +
      (grouped ? '<td class="px-c-spec px-c-spec-g"><span class="px-desc-g">' + esc(r.description) + "</span>" + (r.grade ? '<span class="px-desc">' + T("Alliage : ", "Grade: ") + esc(gradeTxt(r.grade)) + "</span>" : "") + "</td>"
        : '<td class="px-c-spec"><b>' + esc(specLabel(r) || r.description) + '</b><span class="px-desc">' + esc(r.description) + "</span></td>") +
      '<td class="px-c-sup" data-l="' + T("Fournisseur", "Supplier") + '"><b>' + esc(s.name) + "</b>" + chips + "</td>" +
      '<td class="px-c-size" data-l="' + T("Format", "Size") + '">' + esc(sizeOf(r)) + (r.availability && /rupture|out of stock/i.test(r.availability) ? '<small class="px-oos">' + T("rupture", "out of stock") + "</small>" : "") + "</td>" +
      '<td class="num px-c-price" data-l="' + T("Prix CAD", "CAD price") + '"><b>' + money(r.price_cad) + "</b>" + listed + "</td>" +
      '<td class="num px-c-unit" data-l="' + T("Prix unitaire", "Unit price") + '"><b>' + (r.metric != null ? money(r.metric) + "<i>" + munit(r) + "</i>" : "—") + "</b>" + lb + "</td>" +
      '<td class="px-c-tier">' + badge(r) + "</td>" +
      '<td class="px-c-buy">' + btn + '<span class="px-meta">' + src + "</span></td></tr>";
  }
  function munitRaw(u) { return { lb: "/lb", sqft: T("/pi²", "/sq ft"), ft: T("/pi", "/ft") }[u] || ""; }
  function render() {
    if (!D) return;
    app.classList.toggle("px-filtering", ["family", "grade", "spec", "size", "q"].some(function (k) { return F[k].value; }) || (F.form.value !== ""));
    var rows = filtered().sort(cmp);
    var grouped = sortKey === "spec", last = null, html = "", medOf = {};
    if (grouped) rows.forEach(function (r) { if (r.median != null && r.spec && !medOf[r.spec]) medOf[r.spec] = r; });
    rows.slice(0, shown).forEach(function (r) {
      var g = r.spec || specLabel(r) || r.description;
      if (grouped && g !== last) { html += groupHead(r, medOf[r.spec]); last = g; }
      html += row(r, grouped);
    });
    var tb = app.querySelector("#px-table tbody");
    tb.innerHTML = html || '<tr><td colspan="7" class="px-empty">' + T("Aucun prix publié pour ces filtres. Cette combinaison est « sur demande » : voyez l’onglet Méthode & sources pour demander un prix.", "No published price for these filters. This combination is “quote only”: see the Method & sources tab to request a quote.") + "</td></tr>";
    var n = rows.length, cmpN = rows.filter(function (r) { return r.tier && r.tier !== "ref" && r.tier !== "oos" && r.tier !== "check" && r.tier !== "surplus"; }).length;
    setCount(num(n, 0) + T(" prix", " prices") + (cmpN ? " · " + num(cmpN, 0) + T(" comparables", " comparable") : "") + (n > shown ? T(" · " + shown + " affichés", " · " + shown + " shown") : "") + (!FULL && !F.form.value ? T(" · barres, tubes et tuyaux en chargement…", " · loading bar, tube and pipe…") : ""));
    document.getElementById("px-more").hidden = n <= shown;
    setShowing();
    app.querySelectorAll(".grade-pick").forEach(function (b) {
      b.setAttribute("aria-pressed", F.grade.value && b.getAttribute("data-grade") === F.grade.value && b.getAttribute("data-family") === F.family.value ? "true" : "false");
    });
  }

  app.querySelector("#px-table").addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a[data-spec]");
    if (!a) return;
    e.preventDefault();
    var sp = a.getAttribute("data-spec");
    ["grade", "form", "size", "q"].forEach(function (k) { F[k].value = ""; });
    var parts = sp.split("|");
    F.family.value = parts[0]; F.spec.value = "";
    if (parts.length > 3) F.form.value = parts[2];
    refreshOptions();
    if (![].some.call(F.spec.options, function (o) { return o.value === sp; })) F.spec.insertAdjacentHTML("beforeend", '<option value="' + esc(sp) + '"></option>');
    F.spec.value = sp; refreshOptions(); F.spec.value = sp; shown = LIMIT; render(); writeHash(true);
    document.getElementById("px-results-title").scrollIntoView({ behavior: "smooth", block: "start" });
  });

  /* ---------- cards: "compare all" ---------- */
  function initCards() {
    app.querySelectorAll("[data-goto]").forEach(function (a) {
      a.addEventListener("click", function (e) {
        e.preventDefault();
        ["family", "grade", "form", "size", "q"].forEach(function (k) { F[k].value = ""; });
        var sp = a.getAttribute("data-goto"), parts = sp.split("|");
        F.family.value = parts[0]; F.qc.checked = true; refreshOptions();
        F.spec.value = sp; F.q.value = a.getAttribute("data-q") || "";
        shown = LIMIT; refreshOptions(); render(); writeHash(true);
        document.getElementById("px-results-title").scrollIntoView({ behavior: "smooth", block: "start" });
      });
    });
  }

  /* ---------- calculator ---------- */
  function initCalc() {
    var c = document.getElementById("px-calc");
    var fams = uniq(ROWS.filter(function (r) { return SHEET[r.form] && r.price_per_sqft_cad; }).map(function (r) { return r.family; }));
    fams.sort(function (a, b) { return a === "acier" ? -1 : b === "acier" ? 1 : 0; });
    c.family.innerHTML = fams.map(function (f) { return '<option value="' + f + '">' + esc(famLabel(f)) + "</option>"; }).join("");
    function fillSpecs() {
      var specs = {};
      ROWS.forEach(function (r) { if (r.family === c.family.value && SHEET[r.form] && r.spec && r.price_per_sqft_cad && r.tier !== "check") specs[r.spec] = [r.spec, specLabel(r), r.thickness_in]; });
      var list = Object.keys(specs).map(function (k) { return specs[k]; }).sort(function (a, b) { return a[2] - b[2]; });
      var v = c.spec.value;
      c.spec.innerHTML = list.map(function (s) { return '<option value="' + esc(s[0]) + '">' + esc(s[1]) + "</option>"; }).join("");
      var dflt = list.filter(function (s) { return Math.abs(s[2] - 0.0747) < 0.003; })[0];
      if (list.some(function (s) { return s[0] === v; })) c.spec.value = v; else if (dflt) c.spec.value = dflt[0];
    }
    function calc() {
      var k = c.unit.value === "mm" ? 1 / 25.4 : 1;
      var w = parseFloat(c.w.value) * k, l = parseFloat(c.l.value) * k, q = Math.max(1, parseInt(c.qty.value, 10) || 1);
      var kerf = (parseFloat(c.kerf.value) || 0) / 25.4, waste = Math.min(0.9, (parseFloat(c.waste.value) || 0) / 100);
      var rows = ROWS.filter(function (r) { return r.spec === c.spec.value && r.price_per_sqft_cad && r.tier !== "check" && !/rupture/i.test(r.availability || ""); });
      var out = document.getElementById("px-calc-out");
      if (!(w > 0 && l > 0) || !rows.length) { out.innerHTML = '<p class="px-empty">' + T("Entrez des dimensions.", "Enter dimensions.") + "</p>"; return; }
      var t = rows[0].thickness_in, dens = D.density[c.family.value];
      var partLb = dens * t * w * l, totLb = partLb * q;
      var area = (w + kerf) * (l + kerf) * q / 144 / (1 - waste);
      var per = {};
      rows.forEach(function (r) { var p = per[r.supplier]; if (!p || r.price_per_sqft_cad < p.price_per_sqft_cad) per[r.supplier] = r; });
      var list = Object.keys(per).map(function (s) { return per[s]; }).sort(function (a, b) { return a.price_per_sqft_cad - b.price_per_sqft_cad; });
      var h = '<div class="px-kpis"><div><b>' + num(totLb, 1) + " lb</b><span>" + num(totLb / 2.20462, 1) + " kg · " + q + " × " + num(partLb, 2) + " lb</span></div>" +
        "<div><b>" + num(area, 2) + T(" pi²", " sq ft") + "</b><span>" + T("surface consommée", "consumed area") + " (" + num(area * 0.092903, 3) + " m²)</span></div>" +
        "<div><b>" + Math.ceil(area / 32) + "</b><span>" + T("feuille(s) 48 × 96 po équivalente(s)", "equivalent 48 × 96 in sheet(s)") + "</span></div></div>";
      h += '<ol class="px-calc-list">';
      list.forEach(function (r, i) {
        var a = action(r), cost = area * r.price_per_sqft_cad;
        h += '<li class="' + (i === 0 ? "is-best" : "") + '"><div><b>' + esc(supName(r)) + "</b>" + (i === 0 && list.length > 1 ? ' <span class="px-tier px-t-best">' + T("Le moins cher", "Cheapest") + "</span>" : "") +
          (buyable(r) ? "" : ' <span class="px-chip">' + T("hors Québec", "outside QC") + "</span>") +
          '<span class="px-desc">' + esc(gradeTxt(r.grade)) + " · " + esc(sizeOf(r)) + " · " + money(r.price_per_sqft_cad) + T("/pi²", "/sq ft") + (r.currency === "USD" ? " · USD→CAD" : "") + "</span></div>" +
          '<div class="px-calc-cost"><b>' + money(cost) + "</b>" + (i > 0 ? "<small>+" + money(cost - area * list[0].price_per_sqft_cad) + "</small>" : "") + "</div>" +
          '<a class="px-btn px-btn-' + a.kind + '" href="' + esc(a.url) + '" target="_blank" rel="noopener nofollow">' + esc(a.label) + ' <span aria-hidden="true">↗</span></a></li>';
      });
      out.innerHTML = h + "</ol>";
    }
    c.family.addEventListener("change", function () { fillSpecs(); calc(); });
    c.addEventListener("input", calc);
    fillSpecs(); calc();
  }

  /* ---------- coverage (grades tab) ---------- */
  function initCoverage() {
    app.querySelectorAll(".grade-pick").forEach(function (b) {
      b.addEventListener("click", function () {
        ["family", "grade", "spec", "size", "q"].forEach(function (k) { F[k].value = ""; });
        F.form.value = "all"; F.cat.checked = false; F.cmp.checked = false;
        show(0, { push: "push", scroll: "force" });
        ensureFull().then(function () {
          F.form.value = "all"; F.family.value = b.getAttribute("data-family"); refreshOptions();
          F.grade.value = b.getAttribute("data-grade"); shown = LIMIT; refreshOptions(); render(); writeHash(false);
        });
      });
    });
  }

  /* ---------- trend chart (SVG) + supplier spread ---------- */
  var drawn = false;
  function drawChart() {
    if (!D || drawn) return; drawn = true;
    var box = document.getElementById("px-chart");
    var idx = (D.index || []).filter(function (x) { return x.form_group === "feuille_plaque"; });
    if (!idx.length) { box.textContent = T("Pas encore d’historique.", "No history yet."); return; }
    var dates = uniq(idx.map(function (x) { return x.date; })).sort();
    var fams = uniq(idx.map(function (x) { return x.family; }));
    var colors = { acier: "#2e3a3a", inox: "#1b4f8a", aluminium: "#b54300", cuivre: "#8c5a00", laiton: "#a68a00", bronze: "#6b3e26", bronze_alu: "#5c6b00" };
    var W = 720, H = 260, P = { l: 52, r: 16, t: 16, b: 36 };
    var ymax = Math.max.apply(null, idx.map(function (x) { return +x.median_cad_per_lb; })) * 1.1, ymin = 0;
    var step = Math.pow(10, Math.floor(Math.log10(ymax / 4)));
    var st = [1, 2, 2.5, 5, 10].map(function (m) { return m * step; }).filter(function (v) { return v * 4 >= ymax; })[0] || step * 10; ymax = st * 4;
    var xs = function (d) { var i = dates.indexOf(d); return dates.length === 1 ? (P.l + (W - P.l - P.r) / 2) : P.l + i * (W - P.l - P.r) / (dates.length - 1); };
    var yv = function (v) { return H - P.b - (v - ymin) / (ymax - ymin) * (H - P.t - P.b); };
    var s = '<svg viewBox="0 0 ' + W + " " + H + '" width="100%" preserveAspectRatio="xMidYMid meet">';
    for (var g = 0; g <= 4; g++) {
      var v = ymin + (ymax - ymin) * g / 4, y = yv(v);
      s += '<line x1="' + P.l + '" x2="' + (W - P.r) + '" y1="' + y + '" y2="' + y + '" stroke="#d5d0c4"/>';
      s += '<text x="' + (P.l - 6) + '" y="' + (y + 4) + '" text-anchor="end" font-size="11" fill="#5a5f57">' + num(v) + "</text>";
    }
    dates.forEach(function (d, i) { if (dates.length < 8 || i % Math.ceil(dates.length / 6) === 0) s += '<text x="' + xs(d) + '" y="' + (H - 12) + '" text-anchor="middle" font-size="11" fill="#5a5f57">' + d + "</text>"; });
    var legend = "";
    fams.forEach(function (f) {
      var pts = idx.filter(function (x) { return x.family === f; }).sort(function (a, b) { return a.date < b.date ? -1 : 1; });
      var col = colors[f] || "#444";
      if (pts.length > 1) s += '<polyline fill="none" stroke="' + col + '" stroke-width="2.5" points="' + pts.map(function (p) { return xs(p.date) + "," + yv(+p.median_cad_per_lb); }).join(" ") + '"/>';
      pts.forEach(function (p) { s += '<circle cx="' + xs(p.date) + '" cy="' + yv(+p.median_cad_per_lb) + '" r="4" fill="' + col + '"><title>' + esc(famLabel(f)) + " " + p.date + " : " + num(+p.median_cad_per_lb) + " $/lb (n=" + p.n_rows + ")</title></circle>"; });
      var last = pts[pts.length - 1];
      legend += '<span><i style="background:' + col + '"></i>' + esc(famLabel(f)) + " " + money(+last.median_cad_per_lb) + "/lb</span>";
    });
    box.innerHTML = s + '</svg><div class="px-chart-legend">' + legend + "</div>";
    // spread: cheapest vs priciest supplier per family (sheet & plate, comparable specs)
    var fam = {};
    ROWS.forEach(function (r) { if (SHEET[r.form] && r.tier && r.tier !== "ref" && r.tier !== "oos" && r.tier !== "check" && r.pct != null) (fam[r.family] = fam[r.family] || []).push(r.pct); });
    var t = '<h3 class="px-h3">' + T("Écart entre fournisseurs aujourd’hui", "Supplier spread today") + '</h3><table class="px-mini"><thead><tr><th>' + T("Famille", "Family") + '</th><th class="num">' + T("Lignes comparables", "Comparable rows") + '</th><th class="num">' + T("Le moins cher vs médiane", "Cheapest vs median") + '</th><th class="num">' + T("Le plus cher vs médiane", "Priciest vs median") + "</th></tr></thead><tbody>";
    Object.keys(fam).forEach(function (f) { var a = fam[f]; t += "<tr><td>" + esc(famLabel(f)) + '</td><td class="num">' + a.length + '</td><td class="num px-down">' + pctTxt(Math.min.apply(null, a)) + '</td><td class="num px-up">' + pctTxt(Math.max.apply(null, a)) + "</td></tr>"; });
    document.getElementById("px-spread").innerHTML = t + "</tbody></table>";
  }
})();

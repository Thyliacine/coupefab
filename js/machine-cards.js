/* CoupeFab machine cards: lazy-loaded by site.js when the search opens (or on a #machine= link).
   Facts only, normalized by CoupeFab; every card credits MachineToolIndex and the maker. No dependencies. */
(function () {
  if (window.CFMachines) return;
  var lang = document.body.getAttribute("data-lang") || document.documentElement.lang.slice(0, 2) || "fr";
  var EN = lang === "en";
  var me = document.currentScript, V = me && me.src.indexOf("?v=") > -1 ? me.src.split("?v=")[1] : "";
  var css = document.createElement("link"); css.rel = "stylesheet"; css.href = "/css/machines.css?v=" + V; document.head.appendChild(css);
  function T(fr, en) { return EN ? en : fr; }
  function esc(t) { return String(t == null ? "" : t).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function fold(t) { return (t || "").toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, ""); }
  function squash(t) { return fold(t).replace(/[^a-z0-9]/g, ""); }
  var TYPES = {
    vmc: ["Centre d’usinage vertical", "Vertical machining center"], hmc: ["Centre d’usinage horizontal", "Horizontal machining center"],
    "5ax": ["Centre d’usinage 5 axes", "5-axis machining center"], lathe: ["Tour CNC", "CNC lathe"], millturn: ["Tour multitâche", "Mill-turn center"],
    swiss: ["Tour de type suisse", "Swiss-type lathe"], grinder: ["Rectifieuse CNC", "CNC grinder"], boring: ["Aléseuse CNC", "CNC boring mill"],
    vtl: ["Tour vertical", "Vertical lathe"], router: ["Toupie CNC", "CNC router"], laser: ["Découpe laser", "Laser cutter"],
    plasma: ["Table plasma", "Plasma table"], waterjet: ["Jet d’eau", "Waterjet"], brake: ["Presse plieuse", "Press brake"],
    punch: ["Poinçonneuse", "Punch press"], wedm: ["Électroérosion à fil", "Wire EDM"], sedm: ["Électroérosion par enfonçage", "Sinker EDM"],
    multispindle: ["Tour multibroche", "Multi-spindle lathe"], gear: ["Taillage d’engrenages", "Gear cutting"], am: ["Fabrication additive métal", "Metal additive"],
    other: ["Machine-outil", "Machine tool"]
  };
  function typeLabel(t) { var x = TYPES[t] || TYPES.other; return EN ? x[1] : x[0]; }

  /* ---- index + search ---- */
  var idxP = null, IDX = null;
  function load() {
    if (!idxP) idxP = fetch("/js/machines/index.json?v=" + V).then(function (r) { return r.json(); }).then(function (d) {
      IDX = d.r.map(function (r) {
        var brand = d.b[r[1]], model = r[2], alias = r[4] || "";
        return { id: r[0], brand: brand, model: model, type: r[3], alias: alias, shard: d.s[r[1]],
                 hay: squash(brand + " " + model + " " + alias), msq: squash(model), bsq: squash(brand), asq: squash(alias),
                 words: fold(brand + " " + model + " " + alias).split(/[^a-z0-9]+/).filter(Boolean) };
      });
      return IDX;
    }).catch(function () { idxP = null; return []; });
    return idxP;
  }
  function search(q, max) {
    var toks = fold(q).split(/[\s,;\/]+/).map(squash).filter(Boolean), qsq = squash(q);
    if (qsq.length < 2) return Promise.resolve([]);
    return load().then(function (rows) {
      var hits = [];
      for (var i = 0; i < rows.length; i++) {
        var r = rows[i], s = 0;
        if (!toks.every(function (t) { return r.hay.indexOf(t) > -1; })) continue;
        var bm = r.bsq + r.msq;
        if (r.msq === qsq || bm === qsq || r.asq === qsq) s = 100;
        else if (r.msq.indexOf(qsq) === 0 || bm.indexOf(qsq) === 0) s = 70;
        else if (r.hay.indexOf(qsq) > -1) s = 45;
        else s = 25;
        /* a lone brand name ("haas") is fine; a lone short fragment that only matches mid-word is noise */
        if (s === 25 && !toks.some(function (t) { return r.words.some(function (w) { return w.indexOf(t) === 0; }); })) continue;
        if (s === 45 && qsq.length < 3 && !/\d/.test(qsq)) continue;
        hits.push({ r: r, s: s - r.msq.length * 0.3 });
      }
      hits.sort(function (a, b) { return b.s - a.s || (a.r.brand + a.r.model).localeCompare(b.r.brand + b.r.model); });
      return hits.slice(0, max || 5).map(function (h) { return { id: h.r.id, brand: h.r.brand, model: h.r.model, type: h.r.type, typeLabel: typeLabel(h.r.type), total: hits.length }; });
    });
  }

  /* ---- number formatting ---- */
  var LOC = EN ? "en-CA" : "fr-CA";
  function n(v, d) { return Number(v).toLocaleString(LOC, { maximumFractionDigits: d == null ? 0 : d }); }
  function inch(mm) { var v = mm / 25.4; return n(v, v < 10 ? 1 : 0); }
  var IN = T("po", "in");
  function mmIn(v) { return n(v) + " mm (" + inch(v) + " " + IN + ")"; }
  function triple(a, unitIn) {
    var mm = a.map(function (v) { return v == null ? "–" : n(v); }).join(" × ");
    var ins = a.map(function (v) { return v == null ? "–" : inch(v); }).join(" × ");
    return mm + " mm (" + ins + " " + IN + ")";
  }
  function specRows(s) {
    var o = [];
    function add(k, v) { if (v != null && v !== "") o.push([k, v]); }
    if (s.xyz) add(s.xyz[1] == null && s.turn_d ? T("Courses X / Z", "X / Z travel") : T("Courses X / Y / Z", "X / Y / Z travel"),
      s.xyz[1] == null && s.turn_d ? triple([s.xyz[0], s.xyz[2]]) : triple(s.xyz));
    if (s.swing) add(T("Diamètre admissible", "Max swing"), mmIn(s.swing));
    if (s.turn_d) add(T("Diamètre de tournage max", "Max turning diameter"), mmIn(s.turn_d));
    if (s.turn_l) add(T("Longueur de tournage max", "Max turning length"), mmIn(s.turn_l));
    if (s.bar) add(T("Passage de barre", "Bar capacity"), mmIn(s.bar));
    if (s.chuck) add(T("Mandrin", "Chuck"), mmIn(s.chuck));
    if (s.rpm) add(T("Vitesse de broche max", "Max spindle speed"), n(s.rpm) + T(" tr/min", " rpm"));
    if (s.taper) add(T("Cône / nez de broche", "Spindle taper / nose"), esc(s.taper));
    if (s.kw) add(T("Puissance de broche", "Spindle power"), n(s.kw, 1) + " kW (" + n(s.kw / 0.7457) + " hp)");
    if (s.tools) add(T("Capacité d’outils", "Tool capacity"), n(s.tools) + T(" outils", " tools"));
    if (s.turret) add(T("Tourelle", "Turret"), n(s.turret) + T(" postes", " stations"));
    if (s.table) add(T("Table", "Table"), triple(s.table));
    if (s.kg) add(T("Poids de la machine", "Machine weight"), n(s.kg) + " kg (" + n(s.kg / 0.45359237) + " lb)");
    add(T("Réservoir de liquide de coupe", "Coolant tank"), s.coolant_l ? n(s.coolant_l) + " L (" + n(s.coolant_l / 3.785411784, 1) + T(" gal US", " US gal") + ")"
      : '<span class="mc-muted">' + T("Non publié : entrez le vôtre dans le calculateur", "Not published: enter yours in the calculator") + "</span>");
    if (s.control) add(T("Commande CN", "CNC control"), esc(s.control));
    return o;
  }
  function host(u) { try { return new URL(u).hostname.replace(/^www\./, ""); } catch (e) { return u; } }

  /* ---- modal ---- */
  var back = null, dlg = null, opener = null, prevHash = "";
  function close() {
    if (!back || back.hidden) return;
    back.hidden = true; document.body.style.overflow = "";
    if (/^#machine=/.test(location.hash) && history.replaceState) history.replaceState(null, "", location.pathname + location.search + prevHash);
    var f = opener && document.contains(opener) && opener.offsetParent !== null ? opener : document.querySelector("[data-search-open]");
    if (f) f.focus();
  }
  function build() {
    back = document.createElement("div"); back.className = "mc-back"; back.hidden = true;
    back.innerHTML = '<div class="mc-dlg" role="dialog" aria-modal="true" aria-labelledby="mc-title" tabindex="-1"></div>';
    document.body.appendChild(back);
    dlg = back.firstChild;
    back.addEventListener("mousedown", function (e) { if (e.target === back) close(); });
    dlg.addEventListener("click", function (e) { if (e.target.closest("[data-mc-close]")) close(); });
    document.addEventListener("keydown", function (e) {
      if (back.hidden) return;
      if (e.key === "Escape") { e.preventDefault(); e.stopImmediatePropagation(); close(); return; }
      if (e.key === "/") { e.stopImmediatePropagation(); return; }
      if (e.key === "Tab") {
        var f = Array.prototype.filter.call(dlg.querySelectorAll("a[href],button:not([disabled]),[tabindex]:not([tabindex='-1'])"), function (x) { return x.offsetParent !== null; });
        if (!f.length) { e.preventDefault(); return; }
        var first = f[0], last = f[f.length - 1];
        if (e.shiftKey && (document.activeElement === first || document.activeElement === dlg)) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
        else if (!dlg.contains(document.activeElement)) { e.preventDefault(); first.focus(); }
      }
    }, true);
  }
  function open(id, from) {
    return load().then(function (rows) {
      var r = null; for (var i = 0; i < rows.length; i++) if (rows[i].id === id) { r = rows[i]; break; }
      if (!r) return false;
      return fetch("/js/machines/b/" + r.shard + ".json?v=" + V).then(function (x) { return x.json(); }).then(function (all) {
        var d = all[id] || {}, s = d.s || {};
        if (!back) build();
        opener = from || document.activeElement;
        var name = r.brand + " " + r.model;
        var calc = (EN ? "/en/tools/coolant-calculator/" : "/outils/calculateur-liquide-de-coupe/") + "?m=" + encodeURIComponent(d.c || name);
        var src = [];
        if (d.mti) src.push('<a href="' + esc(d.mti) + '" target="_blank" rel="noopener">MachineToolIndex</a>');
        if (d.mk) src.push('<a href="' + esc(d.mk) + '" target="_blank" rel="noopener nofollow">' + T("Site du fabricant", "Maker’s page") + " (" + esc(host(d.mk)) + ")</a>");
        if (d.cs) src.push('<a href="' + esc(d.cs) + '" target="_blank" rel="noopener nofollow">' + T("Source du réservoir", "Coolant tank source") + " (" + esc(host(d.cs)) + ")</a>");
        dlg.innerHTML =
          '<div class="mc-head"><div><p class="mc-kicker"><span class="mc-badge">Machine</span><span>' + esc(typeLabel(r.type)) + "</span></p>" +
          '<h2 id="mc-title">' + esc(name) + "</h2>" + (r.alias ? '<p class="mc-alias">' + T("Aussi appelée : ", "Also known as: ") + esc(r.alias) + "</p>" : "") + "</div>" +
          '<button type="button" class="mc-x" data-mc-close aria-label="' + T("Fermer", "Close") + '"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg></button></div>' +
          '<dl class="mc-specs">' + specRows(s).map(function (x) { return "<div><dt>" + x[0] + "</dt><dd>" + x[1] + "</dd></div>"; }).join("") + "</dl>" +
          '<div class="mc-actions"><a class="btn" href="' + calc + '">' + T("Calculer le liquide de coupe", "Calculate cutting fluid") + ' →</a>' +
          '<button type="button" class="btn-ghost" data-mc-close>' + T("Fermer", "Close") + "</button></div>" +
          '<p class="mc-src">' + T("Sources : ", "Sources: ") + src.join(" · ") + "<br>" +
          T("Données factuelles résumées et converties par CoupeFab. Vérifiez auprès du fabricant avant un achat ou une installation.",
            "Facts summarized and converted by CoupeFab. Check with the maker before buying or installing.") + "</p>";
        prevHash = /^#machine=/.test(location.hash) ? "" : location.hash;
        if (history.replaceState) history.replaceState(null, "", location.pathname + location.search + "#machine=" + encodeURIComponent(id));
        back.hidden = false; document.body.style.overflow = "hidden";
        dlg.scrollTop = 0;
        var x = dlg.querySelector(".mc-x"); (x || dlg).focus();
        return true;
      });
    });
  }
  window.CFMachines = { load: load, search: search, open: open, close: close };
})();

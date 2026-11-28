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

  /* ---- icons: tiny inline line SVGs, no network ---- */
  var IC = {
    vmc: "M9 3h6v4H9zM12 7v6M10.5 13l1.5 2 1.5-2M4 18h16M6 18v3M18 18v3",
    hmc: "M3 8h5v7H3zM8 11.5h6M16 6h4v10h-4zM3 19h18",
    "5ax": "M12 3v6M10 7l2 2 2-2M4 16a8 8 0 0 1 16 0M8 16h8M5 20h14",
    lathe: "M3 7h4v10H3zM7 10h9v4H7zM20 7h-4l-1.5 3M3 20h18",
    millturn: "M3 9h4v10H3zM7 12h8v4H7zM13 3v5M11.5 6.5 13 8l1.5-1.5M3 21h18",
    swiss: "M2 12h13M15 7v10M15 12h2M19 8l-3 4M5 9v6",
    grinder: "M12 4a6 6 0 1 0 0 12 6 6 0 0 0 0-12zM12 8.5a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3zM4 20h16M18 17l2 2M20 14l1.5 1",
    boring: "M3 9.5h4v5H3zM7 12h12M19 8v8M21 10v4",
    vtl: "M9 3h6M12 3v6M10.5 7.5 12 9l1.5-1.5M6 16v-4h12v4M4 19h16",
    router: "M3 8h18M10 8v6l2 3 2-3V8M3 20h18M5 8V5M19 8V5",
    laser: "M12 3v9M8 12h8M12 12v2M6.5 19l2.5-3M12 21v-5M17.5 19 15 16",
    plasma: "M13.5 3 6 13.5h5L10 21l8-11h-5.5z",
    waterjet: "M12 3c3.2 4 5.2 6.5 5.2 9.2a5.2 5.2 0 0 1-10.4 0C6.8 9.5 8.8 7 12 3z",
    brake: "M12 3v8M9.5 9 12 11.5 14.5 9M4 14h5l1.5 5h3L15 14h5",
    punch: "M10 3h4v9h-4zM4 15h16M4 19h16M7 15v4M17 15v4",
    wedm: "M12 2v12M12 17v2M4 14h16v6H4z",
    sedm: "M9 3h6v8H9zM12 11v3M8 14h8M4 17h16v4H4z",
    multispindle: "M8 3a3.2 3.2 0 1 0 0 6.4A3.2 3.2 0 0 0 8 3zM16 3a3.2 3.2 0 1 0 0 6.4A3.2 3.2 0 0 0 16 3zM8 13.6a3.2 3.2 0 1 0 0 6.4 3.2 3.2 0 0 0 0-6.4zM16 13.6a3.2 3.2 0 1 0 0 6.4 3.2 3.2 0 0 0 0-6.4z",
    gear: "M12 8.5a3.5 3.5 0 1 0 0 7 3.5 3.5 0 0 0 0-7zM12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M5.6 18.4l2.1-2.1M16.3 7.7l2.1-2.1",
    am: "M12 3 21 7.5 12 12 3 7.5zM3 12l9 4.5 9-4.5M3 16.5 12 21l9-4.5",
    other: "M12 8.5a3.5 3.5 0 1 0 0 7 3.5 3.5 0 0 0 0-7zM12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M5.6 18.4l2.1-2.1M16.3 7.7l2.1-2.1",
    /* spec tiles */
    t_travel: "M5 19V5M5 19h14M5 19 13 11M3 7l2-2 2 2M17 17l2 2-2 2",
    t_rpm: "M4 14a8 8 0 1 1 16 0M12 14l4-5M7 18h10",
    t_power: "M13.5 3 6 13.5h5L10 21l8-11h-5.5z",
    t_coolant: "M12 3c3.2 4 5.2 6.5 5.2 9.2a5.2 5.2 0 0 1-10.4 0C6.8 9.5 8.8 7 12 3z",
    t_dia: "M12 5a7 7 0 1 0 0 14 7 7 0 0 0 0-14zM5 19 19 5",
    t_tools: "M4 4h6v6H4zM14 4h6v6h-6zM4 14h6v6H4zM14 14h6v6h-6z",
    t_weight: "M6 8h12l2 12H4zM9.5 8a2.5 2.5 0 1 1 5 0",
    t_gen: "M4 8h16v8H4zM8 8v3M12 8v4M16 8v3"
  };
  function svg(k, cls) {
    return '<svg class="' + (cls || "mc-ic") + '" viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="' + (IC[k] || IC.other) + '"/></svg>';
  }

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
      return hits.slice(0, max || 5).map(function (h) { return { id: h.r.id, brand: h.r.brand, model: h.r.model, type: h.r.type, typeLabel: typeLabel(h.r.type), icon: svg(TYPES[h.r.type] ? h.r.type : "other", "mc-ic"), total: hits.length }; });
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
    function add(key, k, v) { if (v != null && v !== "") o.push({ key: key, label: k, html: v }); }
    if (s.xyz) add("xyz", s.xyz[1] == null && s.turn_d ? T("Courses X / Z", "X / Z travel") : T("Courses X / Y / Z", "X / Y / Z travel"),
      s.xyz[1] == null && s.turn_d ? triple([s.xyz[0], s.xyz[2]]) : triple(s.xyz));
    if (s.swing) add("swing", T("Diamètre admissible", "Max swing"), mmIn(s.swing));
    if (s.turn_d) add("turn_d", T("Diamètre de tournage max", "Max turning diameter"), mmIn(s.turn_d));
    if (s.turn_l) add("turn_l", T("Longueur de tournage max", "Max turning length"), mmIn(s.turn_l));
    if (s.bar) add("bar", T("Passage de barre", "Bar capacity"), mmIn(s.bar));
    if (s.chuck) add("chuck", T("Mandrin", "Chuck"), mmIn(s.chuck));
    if (s.rpm) add("rpm", T("Vitesse de broche max", "Max spindle speed"), n(s.rpm) + T(" tr/min", " rpm"));
    if (s.taper) add("taper", T("Cône / nez de broche", "Spindle taper / nose"), esc(s.taper));
    if (s.kw) add("kw", T("Puissance de broche", "Spindle power"), n(s.kw, 1) + " kW (" + n(s.kw / 0.7457) + " hp)");
    if (s.tools) add("tools", T("Capacité d’outils", "Tool capacity"), n(s.tools) + T(" outils", " tools"));
    if (s.turret) add("turret", T("Tourelle", "Turret"), n(s.turret) + T(" postes", " stations"));
    if (s.table) add("table", T("Table", "Table"), triple(s.table));
    if (s.kg) add("kg", T("Poids de la machine", "Machine weight"), n(s.kg) + " kg (" + n(s.kg / 0.45359237) + " lb)");
    if (s.control) add("control", T("Commande CN", "CNC control"), esc(s.control));
    return o;
  }
  /* big tiles: travels, spindle speed, power (+ fillers when a spec is missing); coolant tank gets its own band */
  function tileList(s) {
    var t = [], used = {};
    function mmn(a) { return a.map(function (v) { return v == null ? "–" : n(v); }).join(" × "); }
    function inn(a) { return a.map(function (v) { return v == null ? "–" : inch(v); }).join(" × ") + " " + IN; }
    function put(key, icon, label, val, unit, sub, wide) { t.push({ key: key, icon: icon, label: label, val: val, unit: unit, sub: sub || "", wide: !!wide }); used[key] = 1; }
    if (s.xyz) {
      var lat = s.xyz[1] == null && s.turn_d, a = lat ? [s.xyz[0], s.xyz[2]] : s.xyz;
      put("xyz", "t_travel", lat ? T("Courses X / Z", "X / Z travel") : T("Courses X / Y / Z", "X / Y / Z travel"), mmn(a), "mm", inn(a), true);
    }
    if (s.rpm) put("rpm", "t_rpm", T("Vitesse de broche", "Spindle speed"), n(s.rpm), T("tr/min", "rpm"));
    if (s.kw) put("kw", "t_power", T("Puissance", "Power"), n(s.kw, 1), "kW", n(s.kw / 0.7457) + " hp");
    var fill = [
      ["turn_d", "t_dia", T("Ø de tournage max", "Max turning Ø"), s.turn_d, "mm", function (v) { return inch(v) + " " + IN; }],
      ["swing", "t_dia", T("Diamètre admissible", "Max swing"), s.swing, "mm", function (v) { return inch(v) + " " + IN; }],
      ["tools", "t_tools", T("Outils", "Tools"), s.tools, T("outils", "tools"), null],
      ["turret", "t_tools", T("Tourelle", "Turret"), s.turret, T("postes", "stations"), null],
      ["bar", "t_dia", T("Passage de barre", "Bar capacity"), s.bar, "mm", function (v) { return inch(v) + " " + IN; }],
      ["chuck", "t_dia", T("Mandrin", "Chuck"), s.chuck, "mm", function (v) { return inch(v) + " " + IN; }],
      ["kg", "t_weight", T("Poids", "Weight"), s.kg, "kg", function (v) { return n(v / 0.45359237) + " lb"; }]
    ];
    for (var i = 0; i < fill.length && t.length < 3; i++) {
      var f = fill[i];
      if (f[3]) put(f[0], f[1], f[2], n(f[3]), f[4], f[5] ? f[5](f[3]) : "");
    }
    return { tiles: t, used: used };
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
        if (d.mti2) src.push('<a href="' + esc(d.mti2) + '" target="_blank" rel="noopener">MachineToolIndex</a>');
        if (d.mk) src.push('<a href="' + esc(d.mk) + '" target="_blank" rel="noopener nofollow">' + T("Site du fabricant", "Maker’s page") + " (" + esc(host(d.mk)) + ")</a>");
        if (d.cs) src.push('<a href="' + esc(d.cs) + '" target="_blank" rel="noopener nofollow">' + T("Source du réservoir", "Coolant tank source") + " (" + esc(host(d.cs)) + ")</a>");
        var tl = tileList(s), tiles = tl.tiles, rows = specRows(s).filter(function (x) { return !tl.used[x.key]; });
        var tkey = TYPES[r.type] ? r.type : "other";
        var bl = r.brand.length, nm = esc(name);
        var nameHtml = name.indexOf(r.brand) === 0 ? '<span class="mc-brandname">' + esc(r.brand) + "</span> " + esc(name.slice(bl).replace(/^\s+/, "")) : nm;
        var coolant = s.coolant_l
          ? '<span class="mc-tv"><b>' + n(s.coolant_l) + "</b> <i>L</i></span><span class=\"mc-ts\">" + n(s.coolant_l / 3.785411784, 1) + T(" gal US", " US gal") + "</span>"
          : '<span class="mc-ts mc-ts-na">' + T("Non publié : entrez le vôtre dans le calculateur", "Not published: enter yours in the calculator") + "</span>";
        dlg.innerHTML =
          '<div class="mc-hd"><div class="mc-hd-in"><span class="mc-hico">' + svg(tkey, "mc-ic") + "</span>" +
          '<div class="mc-hd-tx"><p class="mc-kicker"><span class="mc-badge">Machine</span><span class="mc-type">' + esc(typeLabel(r.type)) + "</span></p>" +
          '<h2 id="mc-title">' + nameHtml + "</h2>" + (r.alias ? '<p class="mc-alias">' + T("Aussi appelée : ", "Also known as: ") + esc(r.alias) + "</p>" : "") + "</div></div>" +
          '<button type="button" class="mc-x" data-mc-close aria-label="' + T("Fermer", "Close") + '"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg></button></div>' +
          '<div class="mc-bd">' +
          (tiles.length ? '<ul class="mc-tiles">' + tiles.map(function (x) {
            return '<li class="mc-tile' + (x.wide ? " mc-tile-w" : "") + '"><span class="mc-tico">' + svg(x.icon, "mc-ic") + '</span><span class="mc-tl">' + x.label + '</span><span class="mc-tv"><b>' + x.val + "</b> <i>" + x.unit + "</i></span>" + (x.sub ? '<span class="mc-ts">' + x.sub + "</span>" : "") + "</li>";
          }).join("") + "</ul>" : "") +
          '<div class="mc-cool' + (s.coolant_l ? "" : " mc-cool-na") + '"><span class="mc-tico">' + svg("t_coolant", "mc-ic") + '</span><div class="mc-cool-tx"><span class="mc-tl">' + T("Réservoir de liquide de coupe", "Coolant tank") + "</span>" + coolant + "</div>" +
          '<a class="mc-cta" href="' + calc + '">' + T("Calculer le liquide de coupe", "Calculate cutting fluid") + ' <span aria-hidden="true">→</span></a></div>' +
          (rows.length ? '<h3 class="mc-h3">' + T("Fiche technique", "Specifications") + '</h3><dl class="mc-specs">' + rows.map(function (x) { return "<div><dt>" + x.label + "</dt><dd>" + x.html + "</dd></div>"; }).join("") + "</dl>" : "") +
          '<p class="mc-src">' + T("Sources : ", "Sources: ") + src.join(" · ") + "<br>" +
          T("Données factuelles résumées et converties par CoupeFab. Vérifiez auprès du fabricant avant un achat ou une installation.",
            "Facts summarized and converted by CoupeFab. Check with the maker before buying or installing.") + "</p></div>";
        prevHash = /^#machine=/.test(location.hash) ? "" : location.hash;
        if (history.replaceState) history.replaceState(null, "", location.pathname + location.search + "#machine=" + encodeURIComponent(id));
        back.hidden = false; document.body.style.overflow = "hidden";
        dlg.scrollTop = 0;
        var x = dlg.querySelector(".mc-x"); (x || dlg).focus();
        return true;
      });
    });
  }
  window.CFMachines = { load: load, search: search, open: open, close: close, icon: svg };
})();

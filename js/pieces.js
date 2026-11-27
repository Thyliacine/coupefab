/* CoupeFab — /pieces/ and /en/parts/ */
(function () {
  var app = document.getElementById("pc-app");
  if (!app) return;
  var lang = app.getAttribute("data-lang") || "fr";
  var fr = lang === "fr";

  var piecesPagers = {};
  function pageRows(all, mountId, key) {
    if (!window.cfPager) return;
    var mount = document.getElementById(mountId);
    if (!mount) {
      var last = all && all[0] && all[0].closest("table");
      if (!last || !last.parentNode) return;
      mount = document.createElement("nav");
      mount.className = "cf-pager";
      mount.id = mountId;
      mount.hidden = true;
      last.parentNode.insertBefore(mount, last.nextSibling);
    }
    var vis = all.filter(function (el) { return !el.classList.contains("is-hidden") && !el.hidden; });
    if (!piecesPagers[key]) {
      piecesPagers[key] = window.cfPager({
        mount: mount,
        items: function () { return all.filter(function (el) { return !el.classList.contains("is-hidden") && !el.hidden; }); },
        allItems: all,
        pageSize: 24,
        lang: fr ? "fr" : "en",
        scrollTo: mount.previousElementSibling
      });
    }
    piecesPagers[key].reset();
  }
  var data = null;

  function $(sel, root) { return (root || document).querySelector(sel); }
  function $all(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }

  function money(amount, currency) {
    var cad = String(currency || "CAD").toUpperCase().indexOf("CA") === 0;
    if (fr) {
      var s = (amount || 0).toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, " ").replace(".", ",");
      return s + (cad ? " $" : " US$");
    }
    return "$" + (amount || 0).toLocaleString("en-CA", { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + (cad ? " CAD" : " USD");
  }

  function dateLabel(iso) {
    if (!iso) return "";
    var p = String(iso).slice(0, 10).split("-");
    if (p.length < 3) return iso;
    var y = +p[0], m = +p[1], d = +p[2];
    var monthsFr = ["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"];
    var monthsEn = ["January","February","March","April","May","June","July","August","September","October","November","December"];
    return fr ? (d + " " + monthsFr[m - 1] + " " + y) : (monthsEn[m - 1] + " " + d + ", " + y);
  }

  function originLabel(o) {
    if (o === "oem") return fr ? "Pièce d’origine" : "Genuine";
    if (o === "compatible") return fr ? "Pièce compatible" : "Compatible";
    return fr ? "Non précisé" : "Not stated";
  }

  function packLabel(n) {
    if (n) return fr ? ("paquet de " + n) : ("pack of " + n);
    return fr ? "à confirmer" : "check listing";
  }

  /* Tabs */
  var tabs = $all('[role="tab"]', app);
  var panels = {
    "pc-tab-guides": $("#pc-panel-guides", app),
    "pc-tab-shops": $("#pc-panel-shops"),
    "pc-tab-prices": $("#pc-panel-prices"),
    "pc-tab-market": $("#pc-panel-market")
  };
  function selectTab(id, fromUser) {
    tabs.forEach(function (t) {
      var on = t.id === id;
      t.setAttribute("aria-selected", on ? "true" : "false");
      t.tabIndex = on ? 0 : -1;
      var panel = panels[t.id];
      if (panel) {
        if (on) { panel.removeAttribute("hidden"); panel.classList.add("is-active"); }
        else { panel.setAttribute("hidden", ""); panel.classList.remove("is-active"); }
      }
    });
    if (fromUser && history.replaceState) {
      history.replaceState(null, "", "#" + id.replace("pc-tab-", ""));
    }
  }
  tabs.forEach(function (t) {
    t.addEventListener("click", function () { selectTab(t.id, true); });
  });
  tabs.forEach(function (t, i) {
    t.addEventListener("keydown", function (e) {
      if (e.key !== "ArrowRight" && e.key !== "ArrowLeft") return;
      e.preventDefault();
      var n = e.key === "ArrowRight" ? (i + 1) % tabs.length : (i - 1 + tabs.length) % tabs.length;
      tabs[n].focus();
      selectTab(tabs[n].id, true);
    });
  });
  var hash = (location.hash || "").replace("#", "");
  if (hash === "fournisseurs" || hash === "suppliers" || hash === "shops") selectTab("pc-tab-shops");
  else if (hash === "prix" || hash === "prices") selectTab("pc-tab-prices");
  else if (hash === "marche" || hash === "market") selectTab("pc-tab-market");

  /* Supplier filters (server-rendered rows) */
  var shopForm = $("#pc-shop-filters");
  var shopRows = $all("#pc-shop-table tbody tr");
  var shopCount = $("#pc-shop-count");
  var machineToCat = {
    plasma: "plasma",
    laser: "laser",
    usinage: "usinage|broche",
    plieuse: "plieuse",
    "jet-eau": "jet-eau",
    routeur: "routeur",
    mouvement: "mouvement",
    entretien: "filtre|entretien|lubrifiant|gaz"
  };
  function filterShops() {
    if (!shopForm) return;
    var q = (shopForm.q.value || "").trim().toLowerCase();
    var region = shopForm.region.value;
    var priced = shopForm.priced.value;
    var machine = shopForm.machine.value;
    var n = 0;
    shopRows.forEach(function (tr) {
      var ok = true;
      if (q && (tr.getAttribute("data-text") || "").toLowerCase().indexOf(q) === -1) ok = false;
      if (ok && region && tr.getAttribute("data-region") !== region) ok = false;
      if (ok && priced !== "" && tr.getAttribute("data-priced") !== priced) ok = false;
      if (ok && machine) {
        var cats = (tr.getAttribute("data-cats") || "").toLowerCase();
        var pat = machineToCat[machine] || machine;
        if (!new RegExp(pat).test(cats)) ok = false;
      }
      tr.classList.toggle("is-hidden", !ok);
      if (ok) n++;
    });
    if (shopCount) {
      shopCount.textContent = fr
        ? (n + " fournisseur" + (n > 1 ? "s" : "") + " affiché" + (n > 1 ? "s" : "") + " sur " + shopRows.length)
        : (n + " supplier" + (n === 1 ? "" : "s") + " shown of " + shopRows.length);
    }
    pageRows(shopRows, "pc-shop-pager", "shopPager");
  }
  if (shopForm) {
    shopForm.addEventListener("input", filterShops);
    shopForm.addEventListener("change", filterShops);
    shopForm.addEventListener("reset", function () { setTimeout(filterShops, 0); });
    filterShops();
  }

  /* Machine cards jump to prices and set the machine filter */
  $all(".pc-mcard", app).forEach(function (btn) {
    btn.addEventListener("click", function () {
      var id = btn.getAttribute("data-machine") || "";
      selectTab("pc-tab-prices", true);
      var form = $("#pc-price-filters");
      if (form && form.machine) {
        form.machine.value = id;
        form.dispatchEvent(new Event("change"));
      }
      $all(".pc-mcard", app).forEach(function (b) { b.classList.toggle("is-on", b === btn); b.setAttribute("aria-pressed", b === btn ? "true" : "false"); });
    });
  });

  function renderPrices(items) {
    var body = $("#pc-price-body");
    var form = $("#pc-price-filters");
    var count = $("#pc-price-count");
    if (!body || !form) return;
    var cats = (data && data.categories) || {};
    var macs = (data && data.machines) || {};

    function rowHtml(i) {
      var cat = cats[i.category] || {};
      var mac = macs[i.machine] || {};
      var catlab = (fr ? cat.fr : cat.en) || i.category || "";
      var maclab = (fr ? mac.fr : mac.en) || i.machine || "";
      var oem = i.oem_part || "—";
      var when = dateLabel(i.fetched);
      return (
        '<tr data-machine="' + esc(i.machine || "") + '" data-cat="' + esc(i.category || "") +
        '" data-origin="' + esc(i.origin || "") + '" data-source="' + esc(i.source || "") +
        '" data-brand="' + esc(i.brand || "") + '" data-text="' + esc([i.name, i.sku, i.oem_part, i.brand, i.source_name].join(" ")) + '">' +
        "<td>" + esc(i.name || "") + "</td>" +
        "<td><code>" + esc(i.sku || "—") + "</code></td>" +
        "<td><code>" + esc(oem) + "</code></td>" +
        "<td>" + esc(i.brand || "") + "</td>" +
        "<td>" + esc(maclab) + "</td>" +
        "<td>" + esc(catlab) + "</td>" +
        "<td>" + esc(originLabel(i.origin)) + "</td>" +
        "<td>" + esc(packLabel(i.pack_qty)) + "</td>" +
        '<td class="pc-num">' + esc(money(i.price, i.currency)) + "</td>" +
        "<td><a href=\"" + esc(i.source_url || "#") + "\" rel=\"noopener noreferrer\">" + esc(i.source_name || "") + "</a>" +
        '<div class="pc-when">' + esc(when) + "</div></td>" +
        "</tr>"
      );
    }
    function esc(s) {
      return String(s == null ? "" : s)
        .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
    }

    body.innerHTML = items.map(rowHtml).join("");
    var rows = $all("tr", body);

    function filter() {
      var q = (form.q.value || "").trim().toLowerCase();
      var machine = form.machine.value;
      var cat = form.cat.value;
      var origin = form.origin.value;
      var source = form.source.value;
      var brand = form.brand.value;
      var n = 0;
      rows.forEach(function (tr) {
        var ok = true;
        if (q && (tr.getAttribute("data-text") || "").toLowerCase().indexOf(q) === -1) ok = false;
        if (ok && machine && tr.getAttribute("data-machine") !== machine) ok = false;
        if (ok && cat && tr.getAttribute("data-cat") !== cat) ok = false;
        if (ok && origin && tr.getAttribute("data-origin") !== origin) ok = false;
        if (ok && source && tr.getAttribute("data-source") !== source) ok = false;
        if (ok && brand && tr.getAttribute("data-brand") !== brand) ok = false;
        tr.classList.toggle("is-hidden", !ok);
        if (ok) n++;
      });
      $all(".pc-mcard", app).forEach(function (b) {
        var on = !!machine && b.getAttribute("data-machine") === machine;
        b.classList.toggle("is-on", on); b.setAttribute("aria-pressed", on ? "true" : "false");
      });
      if (count) {
        count.textContent = fr
          ? (n + " prix affiché" + (n > 1 ? "s" : "") + " sur " + rows.length + " — chaque ligne indique la source et la date.")
          : (n + " price" + (n === 1 ? "" : "s") + " shown of " + rows.length + " — each row names the source and the date.");
      }
      pageRows(rows, "pc-price-pager", "pricePager");
    }
    form.addEventListener("input", filter);
    form.addEventListener("change", filter);
    form.addEventListener("reset", function () { setTimeout(filter, 0); });
    filter();
  }

  var jsonUrl = app.getAttribute("data-json") || "/pieces/donnees.json";
  fetch(jsonUrl, { credentials: "same-origin" })
    .then(function (r) { if (!r.ok) throw new Error("http " + r.status); return r.json(); })
    .then(function (j) {
      data = j;
      renderPrices(j.items || []);
    })
    .catch(function () {
      var count = $("#pc-price-count");
      if (count) {
        count.textContent = fr
          ? "Le tableau complet n’a pas pu être chargé. Les lignes ci-dessous sont un aperçu (torche Duramax)."
          : "The full table could not be loaded. The rows below are a preview (Duramax torch).";
      }
    });
})();

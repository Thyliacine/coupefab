/* CoupeFab list pager: ~24 items, ?page=N, prev/next + page numbers, FR+EN.
   All items stay in the HTML for crawlers; this only shows one page at a time. */
(function (w) {
  "use strict";
  var SIZE = 24;

  function langOf(el) {
    var n = el, doc = (el && el.ownerDocument) || document;
    while (n && n !== doc) {
      if (n.getAttribute && n.getAttribute("data-lang")) return n.getAttribute("data-lang");
      n = n.parentNode;
    }
    return (doc.documentElement.lang || "fr").slice(0, 2);
  }

  function readPage(param) {
    var n = parseInt(new URL(location.href).searchParams.get(param || "page") || "1", 10);
    return Number.isFinite(n) && n > 0 ? n : 1;
  }

  function writePage(param, page, replace) {
    var u = new URL(location.href);
    if (page <= 1) u.searchParams.delete(param || "page");
    else u.searchParams.set(param || "page", String(page));
    var next = u.pathname + (u.search || "") + u.hash;
    if (next === location.pathname + location.search + location.hash) return;
    if (replace !== false) history.replaceState(null, "", next);
    else history.pushState(null, "", next);
  }

  function pagesOf(total, size) { return Math.max(1, Math.ceil(Math.max(0, total) / size)); }

  function windowed(cur, totalPages) {
    var out = [], i;
    if (totalPages <= 7) {
      for (i = 1; i <= totalPages; i++) out.push(i);
      return out;
    }
    out.push(1);
    var a = Math.max(2, cur - 1), b = Math.min(totalPages - 1, cur + 1);
    if (a > 2) out.push("…");
    for (i = a; i <= b; i++) out.push(i);
    if (b < totalPages - 1) out.push("…");
    out.push(totalPages);
    return out;
  }

  function hrefFor(param, page) {
    var u = new URL(location.href);
    if (page <= 1) u.searchParams.delete(param);
    else u.searchParams.set(param, String(page));
    return u.pathname + (u.search || "") + u.hash;
  }

  function drawNav(mount, cur, totalPages, fr, param) {
    if (!mount) return;
    if (totalPages <= 1) { mount.hidden = true; mount.innerHTML = ""; return; }
    mount.hidden = false;
    mount.classList.add("cf-pager");
    if (!mount.getAttribute("aria-label")) mount.setAttribute("aria-label", fr ? "Pagination" : "Pagination");
    var html = "";
    if (cur > 1) html += '<a class="cf-pager-btn" rel="prev" href="' + hrefFor(param, cur - 1) + '" data-page="' + (cur - 1) + '">' + (fr ? "Précédent" : "Previous") + "</a>";
    else html += '<span class="cf-pager-btn is-disabled" aria-disabled="true">' + (fr ? "Précédent" : "Previous") + "</span>";
    html += '<ol class="cf-pager-pages">';
    windowed(cur, totalPages).forEach(function (x) {
      if (x === "…") { html += '<li class="cf-pager-gap" aria-hidden="true">…</li>'; return; }
      if (x === cur) html += '<li><a class="cf-pager-num" href="' + hrefFor(param, x) + '" aria-current="page" data-page="' + x + '">' + x + "</a></li>";
      else html += '<li><a class="cf-pager-num" href="' + hrefFor(param, x) + '" data-page="' + x + '">' + x + "</a></li>";
    });
    html += "</ol>";
    if (cur < totalPages) html += '<a class="cf-pager-btn" rel="next" href="' + hrefFor(param, cur + 1) + '" data-page="' + (cur + 1) + '">' + (fr ? "Suivant" : "Next") + "</a>";
    else html += '<span class="cf-pager-btn is-disabled" aria-disabled="true">' + (fr ? "Suivant" : "Next") + "</span>";
    mount.innerHTML = html;
  }

  w.cfPager = function (opts) {
    opts = opts || {};
    var size = opts.pageSize || SIZE;
    var param = opts.param || "page";
    var mount = typeof opts.mount === "string" ? document.querySelector(opts.mount) : opts.mount;
    var fr = (opts.lang || langOf(mount || document.body)) !== "en";
    var self = {};

    function total() {
      if (typeof opts.total === "function") return opts.total();
      if (opts.items) return (typeof opts.items === "function" ? opts.items() : opts.items).length;
      return opts.total || 0;
    }

    function page() {
      var p = readPage(param), max = pagesOf(total(), size);
      return Math.min(Math.max(1, p), max);
    }

    function apply(push) {
      var t = total(), max = pagesOf(t, size), p = page();
      if (p !== readPage(param)) writePage(param, p, true);
      else if (push) writePage(param, p, push !== "push");
      var start = (p - 1) * size, end = Math.min(start + size, t);
      if (opts.items) {
        var items = typeof opts.items === "function" ? opts.items() : opts.items;
        var all = opts.allItems || items;
        if (opts.allItems) {
          all.forEach(function (el) { el.classList.add("cf-off-page"); });
          items.forEach(function (el, i) {
            if (i >= start && i < end) el.classList.remove("cf-off-page");
            else el.classList.add("cf-off-page");
          });
        } else {
          items.forEach(function (el, i) {
            if (i >= start && i < end) el.classList.remove("cf-off-page");
            else el.classList.add("cf-off-page");
          });
        }
      }
      if (opts.render) opts.render(p, start, end, t);
      drawNav(mount, p, max, fr, param);
      if (opts.onChange) opts.onChange(p, start, end, t);
    }

    if (mount) {
      mount.addEventListener("click", function (e) {
        var a = e.target.closest("[data-page]");
        if (!a || !mount.contains(a)) return;
        e.preventDefault();
        writePage(param, parseInt(a.getAttribute("data-page"), 10), false);
        apply(false);
        if (opts.scrollTo) {
          var t = typeof opts.scrollTo === "string" ? document.querySelector(opts.scrollTo) : opts.scrollTo;
          if (t && t.scrollIntoView) t.scrollIntoView({ block: "start" });
        }
      });
    }
    w.addEventListener("popstate", function () { apply(false); });

    self.apply = function () { apply(true); };
    self.reset = function () { writePage(param, 1, true); apply(false); };
    self.page = page;
    self.pageSize = size;
    return self;
  };

  w.cfPager.SIZE = SIZE;
  w.cfPager.readPage = readPage;
  w.cfPager.writePage = writePage;

  function auto() {
    document.querySelectorAll("[data-pager]").forEach(function (box) {
      if (box._cfPager) return;
      var size = parseInt(box.getAttribute("data-pager") || String(SIZE), 10) || SIZE;
      var items = [].slice.call(box.children);
      if (items.length <= size) return;
      var mount = box.nextElementSibling && box.nextElementSibling.classList.contains("cf-pager")
        ? box.nextElementSibling
        : (function () { var n = document.createElement("nav"); n.className = "cf-pager"; n.hidden = true; box.parentNode.insertBefore(n, box.nextSibling); return n; })();
      box._cfPager = w.cfPager({ items: items, mount: mount, pageSize: size, lang: langOf(box), scrollTo: box });
      box._cfPager.apply();
    });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", auto);
  else auto();
})(window);

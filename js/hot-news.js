/* CoupeFab — topic chips for the hot-news list (homepage cap already in HTML; news page is paged). */
(function () {
  "use strict";
  function boot(root) {
    var chips = [].slice.call(root.querySelectorAll(".hn-chip"));
    var items = [].slice.call(root.querySelectorAll(".hn-item"));
    if (!chips.length || !items.length) return;
    var isPage = root.getAttribute("data-hot-news") === "page";
    var pager = null;

    function topicFromUrl() {
      return new URL(location.href).searchParams.get("topic") || "";
    }

    function apply(topic, resetPage) {
      var shown = [];
      items.forEach(function (el) {
        var ok = !topic || el.getAttribute("data-topic") === topic;
        el.hidden = !ok;
        if (ok) shown.push(el);
      });
      chips.forEach(function (c) {
        var on = (c.getAttribute("data-topic") || "") === topic;
        c.classList.toggle("is-on", on);
        c.setAttribute("aria-pressed", on ? "true" : "false");
      });
      if (isPage && window.cfPager) {
        if (!pager) {
          var mount = document.getElementById("hn-pager");
          pager = window.cfPager({
            mount: mount,
            items: function () { return shown; },
            allItems: items,
            pageSize: 24,
            lang: root.getAttribute("data-lang") || "fr",
            scrollTo: root.querySelector(".hn-list")
          });
        }
        if (resetPage) pager.reset();
        else pager.apply();
      }
    }

    function writeTopic(topic) {
      if (!isPage) return;
      var u = new URL(location.href);
      if (topic) u.searchParams.set("topic", topic);
      else u.searchParams.delete("topic");
      u.searchParams.delete("page");
      var next = u.pathname + (u.search || "") + u.hash;
      if (next !== location.pathname + location.search + location.hash) history.replaceState(null, "", next);
    }

    chips.forEach(function (c) {
      c.addEventListener("click", function () {
        var topic = c.getAttribute("data-topic") || "";
        writeTopic(topic);
        apply(topic, true);
      });
    });
    window.addEventListener("popstate", function () { apply(isPage ? topicFromUrl() : "", false); });
    apply(isPage ? topicFromUrl() : "", false);
  }
  function init() {
    document.querySelectorAll("[data-hot-news]").forEach(boot);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();

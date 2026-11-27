/* CoupeFab — coolant calculator UI (/outils/calculateur-liquide-de-coupe/, /en/tools/coolant-calculator/). Math in liquide-math.js. */
(function () {
  'use strict';
  var app = document.getElementById('lq-app'); if (!app || !window.CFCoolant) return;
  var M = window.CFCoolant, fr = app.getAttribute('data-lang') === 'fr';
  var T = function (a, b) { return fr ? a : b; };
  var $ = function (id) { return document.getElementById(id); };
  var rows = [];
  var TYPES = { vmc: T('CU vertical', 'VMC'), hmc: T('CU horizontal', 'HMC'), '5ax': T('5 axes', '5-axis'), lathe: T('tour', 'lathe'),
    millturn: T('tour axe Y', 'mill-turn'), vtl: T('tour vertical', 'VTL'), boring: T('aléseuse', 'boring mill'), router: T('routeur', 'router'),
    swiss: T('tour suisse', 'Swiss lathe'), grinder: T('rectifieuse', 'grinder') };
  var unit = 'L', machine = null;
  var KEY = 'cf-coolant-v1';

  function parse(v) { if (v == null) return NaN; v = String(v).trim().replace(/\s/g, '').replace(',', '.'); return v === '' ? NaN : Number(v); }
  function fmt(x, d) {
    if (!isFinite(x)) return '—';
    if (d == null) d = Math.abs(x) >= 100 ? 0 : Math.abs(x) >= 10 ? 1 : 2;
    return x.toLocaleString(fr ? 'fr-CA' : 'en-CA', { minimumFractionDigits: 0, maximumFractionDigits: d });
  }
  var uLab = function () { return unit === 'L' ? 'L' : T('gal US', 'US gal'); };
  function vol(x) { // x in current unit -> "12,5 L (3,3 gal US)"
    var other = unit === 'L' ? M.fromL(x, 'gal') : M.toL(x, 'gal');
    return '<b>' + fmt(x) + ' ' + uLab() + '</b> <span class="lq-alt">(' + fmt(other) + ' ' + (unit === 'L' ? T('gal US', 'US gal') : 'L') + ')</span>';
  }
  function small(x) { // concentrate amounts below 4 L also in ml / quarts help measuring
    if (unit === 'L' && x > 0 && x < 1) return ' <span class="lq-alt">= ' + fmt(x * 1000, 0) + ' ml</span>';
    if (unit === 'gal' && x > 0 && x < 1) return ' <span class="lq-alt">= ' + fmt(x * 4, 1) + ' ' + T('pintes US (qt)', 'US qt') + '</span>';
    return '';
  }
  function label(r) { return r[0] + ' ' + r[1]; }

  function esc(t) { return String(t == null ? '' : t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  // accent/case fold that keeps string length (so match offsets map back onto the label)
  function fold(t) { var o = ''; for (var i = 0; i < t.length; i++) { var c = t.charAt(i), d = c.normalize ? c.normalize('NFD').charAt(0) : c; o += d.toLowerCase().length === 1 ? d.toLowerCase() : c; } return o; }
  var squash = function (t) { return t.replace(/[^a-z0-9]/g, ''); };
  var idx = []; // [folded label, squashed label, folded model]
  function index() { idx = rows.map(function (r) { var f = fold(label(r)); return [f, squash(f), fold(r[1])]; }); }

  function find(q) { // exact label, else unique match (deep links, restore)
    q = fold((q || '').trim()); if (!q) return null;
    for (var i = 0; i < rows.length; i++) if (idx[i][0] === q) return rows[i];
    var hits = search(q).hits; return hits.length === 1 ? rows[hits[0].i] : null;
  }
  function search(q) {
    var toks = fold(q).split(/[\s,;\/]+/).filter(Boolean), hits = [];
    for (var i = 0; i < rows.length; i++) {
      var f = idx[i][0], sq = idx[i][1], m = idx[i][2], score = 0, ok = true;
      for (var k = 0; k < toks.length; k++) {
        var t = toks[k], p = f.indexOf(t);
        if (p < 0) { var st = squash(t); if (st && sq.indexOf(st) >= 0) { score += 1; continue; } ok = false; break; }
        if (m.indexOf(t) === 0 || squash(m).indexOf(squash(t)) === 0) score += 6; else if (p === 0 || f.charAt(p - 1) === ' ' || f.charAt(p - 1) === '-') score += 3; else score += 1;
        if (m === t || squash(m) === squash(t)) score += 10;
      }
      if (ok) hits.push({ i: i, s: score });
    }
    return { hits: hits, toks: toks };
  }
  function mark(text, toks) { // <mark> every token occurrence (accent-insensitive)
    if (!toks.length) return esc(text);
    var f = fold(text), on = new Array(text.length + 1).join('0').split('');
    toks.forEach(function (t) { var p = 0; while (t && (p = f.indexOf(t, p)) >= 0) { for (var j = p; j < p + t.length; j++) on[j] = '1'; p += t.length; } });
    var out = '', open = false;
    for (var i = 0; i < text.length; i++) {
      if (on[i] === '1' && !open) { out += '<mark>'; open = true; } else if (on[i] !== '1' && open) { out += '</mark>'; open = false; }
      out += esc(text.charAt(i));
    }
    return out + (open ? '</mark>' : '');
  }

  // ---- combobox ----
  var combo = $('lq-combo'), q = $('lq-q'), pop = $('lq-pop'), clr = $('lq-clear');
  var LIMIT = 150, opts = [], active = -1, isOpen = false, loaded = false;
  function capTxt(r) { return r[3] ? fmt(r[3], 0) + ' L <span>· ' + fmt(r[4], r[4] >= 100 ? 0 : 1) + ' gal</span>' : '<em>' + T('à entrer', 'enter own') + '</em>'; }
  function render() {
    if (!loaded) { pop.innerHTML = '<div class="lq-pop-msg">' + T('Chargement des machines…', 'Loading machines…') + '</div>'; opts = []; active = -1; return; }
    var v = q.value.trim(), res = v ? search(v) : { hits: rows.map(function (r, i) { return { i: i, s: 0 }; }), toks: [] };
    var hits = res.hits, total = hits.length;
    // group by brand; groups ordered by best score, then brand name
    var groups = {}, order = [];
    hits.forEach(function (h) { var b = rows[h.i][0]; if (!groups[b]) { groups[b] = { b: b, best: -1, list: [] }; order.push(groups[b]); } groups[b].list.push(h); if (h.s > groups[b].best) groups[b].best = h.s; });
    order.sort(function (a, b) { return b.best - a.best || a.b.localeCompare(b.b); });
    var html = '', n = 0; opts = [];
    for (var g = 0; g < order.length && n < LIMIT; g++) {
      var G = order[g]; G.list.sort(function (a, b) { return b.s - a.s || a.i - b.i; });
      html += '<div class="lq-grp" role="group" aria-label="' + esc(G.b) + '"><div class="lq-grp-h" aria-hidden="true">' + mark(G.b, res.toks) + '<span>' + G.list.length + '</span></div>';
      for (var k = 0; k < G.list.length && n < LIMIT; k++, n++) {
        var r = rows[G.list[k].i], id = 'lq-opt-' + G.list[k].i;
        opts.push(G.list[k].i);
        html += '<div class="lq-opt' + (machine === r ? ' is-sel' : '') + '" role="option" id="' + id + '" data-i="' + G.list[k].i + '" aria-selected="' + (machine === r) + '">'
          + '<span class="lq-opt-m">' + mark(r[1], res.toks) + '</span><span class="lq-opt-t">' + esc(TYPES[r[2]] || '') + '</span><span class="lq-opt-c">' + capTxt(r) + '</span></div>';
      }
      html += '</div>';
    }
    if (!total) html = '<div class="lq-pop-msg">' + T('Aucune machine trouvée pour « ', 'No machine found for “') + esc(v) + T(' ». Entrez la capacité vous-même dans le champ suivant.', '”. Enter the capacity yourself in the next field.') + '</div>';
    else if (total > n) html += '<div class="lq-pop-more">' + T(n + ' sur ' + fmt(total, 0) + ' — continuez à taper pour préciser', n + ' of ' + fmt(total, 0) + ' — keep typing to narrow down') + '</div>';
    pop.innerHTML = html; pop.scrollTop = 0;
    setActive(v && opts.length ? 0 : -1, true);
  }
  function setActive(k, noScroll) {
    var prev = pop.querySelector('.lq-opt.is-act'); if (prev) prev.classList.remove('is-act');
    active = k;
    if (k < 0 || k >= opts.length) { q.removeAttribute('aria-activedescendant'); active = -1; return; }
    var el = $('lq-opt-' + opts[k]); el.classList.add('is-act'); q.setAttribute('aria-activedescendant', el.id);
    if (!noScroll) { // keep row visible below the sticky brand header
      var head = el.parentNode.querySelector('.lq-grp-h'), hh = head ? head.offsetHeight : 0;
      var top = el.offsetTop - pop.offsetTop, pr = pop.getBoundingClientRect(), er = el.getBoundingClientRect();
      if (er.top < pr.top + hh) pop.scrollTop -= (pr.top + hh - er.top);
      else if (er.bottom > pr.bottom) pop.scrollTop += er.bottom - pr.bottom;
    }
  }
  function open() {
    if (isOpen) return; isOpen = true; render(); pop.hidden = false; combo.classList.add('is-open'); q.setAttribute('aria-expanded', 'true');
    if (window.matchMedia && window.matchMedia('(max-width: 34rem)').matches) { try { combo.scrollIntoView({ block: 'start', behavior: 'smooth' }); } catch (e) {} }
  }
  function close() { if (!isOpen) return; isOpen = false; pop.hidden = true; combo.classList.remove('is-open'); q.setAttribute('aria-expanded', 'false'); q.removeAttribute('aria-activedescendant'); active = -1; }
  function syncClear() { clr.hidden = !q.value; }
  function choose(i) { var r = rows[i]; q.value = label(r); syncClear(); close(); pickMachine(r); update(); }
  q.addEventListener('focus', open);
  q.addEventListener('click', open);
  q.addEventListener('input', function () {
    syncClear(); if (!isOpen) { isOpen = true; pop.hidden = false; combo.classList.add('is-open'); q.setAttribute('aria-expanded', 'true'); } render();
    if (machine && fold(q.value.trim()) !== fold(label(machine))) { pickMachine(null); update(); }
  });
  q.addEventListener('keydown', function (e) {
    var k = e.key;
    if (k === 'ArrowDown' || k === 'ArrowUp') {
      e.preventDefault(); if (!isOpen) { open(); }
      if (!opts.length) return;
      setActive(k === 'ArrowDown' ? (active + 1) % opts.length : (active <= 0 ? opts.length - 1 : active - 1));
    } else if (k === 'PageDown' || k === 'PageUp') {
      if (!isOpen || !opts.length) return; e.preventDefault(); setActive(Math.max(0, Math.min(opts.length - 1, (active < 0 ? 0 : active) + (k === 'PageDown' ? 8 : -8))));
    } else if (k === 'Enter') {
      if (isOpen && active >= 0) { e.preventDefault(); choose(opts[active]); }
      else if (isOpen) { var r = find(q.value); if (r) { e.preventDefault(); choose(rows.indexOf(r)); } }
    } else if (k === 'Escape') {
      if (isOpen) { e.preventDefault(); close(); } else if (q.value) { e.preventDefault(); q.value = ''; syncClear(); pickMachine(null); update(); }
    } else if (k === 'Tab') close();
  });
  pop.addEventListener('mousedown', function (e) { e.preventDefault(); }); // keep focus in the input
  pop.addEventListener('click', function (e) { var o = e.target.closest('.lq-opt'); if (o) choose(+o.getAttribute('data-i')); });
  pop.addEventListener('mousemove', function (e) { var o = e.target.closest('.lq-opt'); if (o) { var k = opts.indexOf(+o.getAttribute('data-i')); if (k !== active) setActive(k, true); } });
  clr.addEventListener('click', function () { q.value = ''; syncClear(); pickMachine(null); update(); q.focus(); if (isOpen) render(); else open(); });
  document.addEventListener('pointerdown', function (e) { if (isOpen && !combo.contains(e.target)) close(); });
  q.addEventListener('blur', function () { setTimeout(function () { if (document.activeElement !== q) close(); }, 0); });

  function setCap(liters) {
    $('lq-cap').value = fmt(unit === 'L' ? liters : M.fromL(liters, 'gal'), unit === 'L' ? 0 : 1);
  }
  function pickMachine(r) {
    machine = r;
    var info = $('lq-machine-info'), vbox = $('lq-variants');
    vbox.innerHTML = ''; vbox.hidden = true;
    if (!r) { info.textContent = T('Tapez une marque ou un modèle, ou entrez le volume vous-même.', 'Type a brand or model, or enter the volume yourself.'); return; }
    var note = fr ? r[6] : r[7];
    var src = r[5] ? ' <a href="' + r[5] + '" target="_blank" rel="nofollow noopener">' + T('source', 'source') + '</a>' : '';
    if (r[3]) {
      setCap(r[3]);
      info.innerHTML = '<b>' + label(r) + '</b>' + T(' : ', ': ') + fmt(r[3], 0) + ' L · ' + fmt(r[4], 1) + ' ' + T('gal US', 'US gal') + '.' + src + (note ? '<br>' + note : '');
    } else {
      $('lq-cap').value = '';
      info.innerHTML = '<b>' + label(r) + '</b>' + T(' : ', ': ') + T('capacité non publiée, entrez la vôtre.', 'capacity not published, enter your own.') + src + (note ? '<br>' + note : '');
      $('lq-cap').focus();
    }
    if (r[8] && r[8].length) {
      var mk = function (lab, L) { var b = document.createElement('button'); b.type = 'button'; b.className = 'chip'; b.textContent = lab + ' · ' + fmt(L, 0) + ' L'; b.addEventListener('click', function () { setCap(L); update(); }); return b; };
      vbox.appendChild(mk(T('standard', 'standard'), r[3]));
      r[8].forEach(function (v) { vbox.appendChild(mk(fr ? v[0] : v[1], v[2])); });
      vbox.hidden = false;
    }
  }

  function out(id, html) { $(id).innerHTML = html; }
  function line(k, v) { return '<div class="lq-line"><span>' + k + '</span><span>' + v + '</span></div>'; }

  function update() {
    var cap = parse($('lq-cap').value), ct = parse($('lq-target').value), f = parse($('lq-factor').value);
    if (!(f > 0)) f = 1;
    document.querySelectorAll('[data-u]').forEach(function (e) { e.textContent = '(' + uLab() + ')'; });
    // A — fresh fill
    var a = M.freshFill(cap, ct);
    if (a) {
      out('lq-fresh', line(T('Concentré', 'Concentrate'), vol(a.concentrate) + small(a.concentrate)) + line(T('Eau', 'Water'), vol(a.water))
        + line(T('Rapport', 'Ratio'), '1 : ' + fmt(a.ratio, 1) + ' <span class="lq-alt">(' + T('concentré : eau', 'concentrate : water') + ')</span>')
        + line(T('Lecture à viser', 'Reading to aim for'), '<b>' + fmt(M.targetBrix(ct, f), 1) + ' °Brix</b> <span class="lq-alt">(' + T('facteur', 'factor') + ' ' + fmt(f, 2) + ')</span>'));
    } else out('lq-fresh', '<p class="lq-wait">' + T('Entrez la capacité et une concentration entre 0 et 100 %.', 'Enter the capacity and a concentration between 0 and 100%.') + '</p>');

    // C — refractometer
    var b2 = parse($('lq-brix2').value);
    if (isFinite(b2) && b2 >= 0) {
      var tc = M.trueConc(b2, f), msg = '';
      if (isFinite(ct)) msg = tc < ct - 0.5 ? T('Trop pauvre pour la cible.', 'Too lean for the target.') : tc > ct + 0.5 ? T('Trop riche pour la cible.', 'Too rich for the target.') : T('Dans la cible (± 0,5 point).', 'On target (± 0.5 point).');
      out('lq-refr', line(T('Vraie concentration', 'True concentration'), '<b>' + fmt(tc, 1) + ' %</b>') + line(T('Calcul', 'Math'), fmt(b2, 1) + ' × ' + fmt(f, 2))
        + (isFinite(ct) ? line(T('Lecture pour', 'Reading for') + ' ' + fmt(ct, 1) + ' %', '<b>' + fmt(M.targetBrix(ct, f), 1) + ' °Brix</b>') : '') + (msg ? '<p class="lq-verdict">' + msg + '</p>' : ''));
    } else out('lq-refr', isFinite(ct) ? line(T('Lecture pour', 'Reading for') + ' ' + fmt(ct, 1) + ' %', '<b>' + fmt(M.targetBrix(ct, f), 1) + ' °Brix</b>') + '<p class="lq-wait">' + T('Entrez une lecture pour obtenir la vraie concentration.', 'Enter a reading to get the true concentration.') + '</p>' : '<p class="lq-wait">—</p>');

    // B — correction
    var brix = parse($('lq-brix').value), cur = parse($('lq-cur').value), fin = parse($('lq-final').value);
    if (!isFinite(fin)) fin = cap;
    if (!isFinite(brix) || !isFinite(cur) || !isFinite(fin)) { out('lq-fix', '<p class="lq-wait">' + T('Entrez la lecture et le niveau actuel (et la capacité).', 'Enter the reading and the current level (and the capacity).') + '</p>'); save(); return; }
    var cc = M.trueConc(brix, f);
    if (isFinite(cap) && fin > cap + 1e-9) { out('lq-fix', '<p class="lq-warn">' + T('Le niveau voulu dépasse la capacité du réservoir.', 'The wanted level is above the tank capacity.') + '</p>'); save(); return; }
    var r = M.correct(cur, cc, ct, fin);
    if (!r) { out('lq-fix', '<p class="lq-wait">' + T('Valeurs hors plage.', 'Values out of range.') + '</p>'); save(); return; }
    var h = line(T('Concentration actuelle', 'Current concentration'), '<b>' + fmt(cc, 1) + ' %</b> <span class="lq-alt">(' + fmt(brix, 1) + ' × ' + fmt(f, 2) + ')</span>');
    if (r.kind === 'ok') h += '<p class="lq-verdict lq-good">' + T('Rien à faire : niveau et concentration sur la cible.', 'Nothing to do: level and concentration on target.') + '</p>';
    else if (r.kind === 'add') {
      h += '<p class="lq-step">' + T('Pour arriver à', 'To reach') + ' ' + vol(fin) + ' ' + T('à', 'at') + ' ' + fmt(ct, 1) + ' %, ' + T('ajoutez :', 'add:') + '</p>'
        + line(T('Concentré', 'Concentrate'), vol(r.concentrate) + small(r.concentrate)) + line(T('Eau', 'Water'), vol(r.water));
      if (r.concentrate > 0 && r.water > 0) h += '<p class="lq-help">' + T('Soit un prémélange à', 'That is a premix at') + ' <b>' + fmt(r.premix, 1) + ' %</b>.</p>';
    } else {
      h += '<p class="lq-verdict lq-bad">' + (r.reason === 'rich' ? T('Trop riche pour corriger sans vidanger.', 'Too rich to fix without draining.') : T('Trop pauvre et pas assez de place pour le concentré.', 'Too lean and not enough room for the concentrate.')) + '</p>'
        + line('1. ' + T('Retirez', 'Remove'), vol(r.drain))
        + line('2. ' + T('Ajoutez', 'Add') + ' ' + (r.reason === 'rich' ? T('de l’eau', 'water') : T('du concentré', 'concentrate')), vol(r.reason === 'rich' ? r.water : r.concentrate))
        + '<p class="lq-help">' + T('Résultat :', 'Result:') + ' ' + vol(fin) + ' ' + T('à', 'at') + ' ' + fmt(ct, 1) + ' %.</p>';
    }
    if (r.kind !== 'ok' && (r.quick.concentrate > 0 || r.quick.water > 0)) {
      h += '<p class="lq-quick">' + T('Correction minimale (sans viser le niveau) :', 'Minimum fix (ignoring the level):') + ' '
        + (r.quick.concentrate > 0 ? T('ajouter seulement', 'add only') + ' ' + vol(r.quick.concentrate) + ' ' + T('de concentré', 'of concentrate') : T('ajouter seulement', 'add only') + ' ' + vol(r.quick.water) + ' ' + T('d’eau', 'of water'))
        + (r.quick.fits ? '.' : ' — ' + T('ne rentre pas dans le réservoir.', 'does not fit in the tank.')) + '</p>';
    }
    out('lq-fix', h);
    save();
  }

  function save() {
    try { localStorage.setItem(KEY, JSON.stringify({ unit: unit, m: machine ? label(machine) : '', cap: $('lq-cap').value, t: $('lq-target').value, f: $('lq-factor').value })); } catch (e) {}
  }
  function setUnit(u) {
    if (u === unit) return;
    ['lq-cap', 'lq-cur', 'lq-final'].forEach(function (id) {
      var v = parse($(id).value); if (isFinite(v)) $(id).value = fmt(u === 'gal' ? M.fromL(v, 'gal') : M.toL(v, 'gal'), u === 'gal' ? 1 : 0);
    });
    unit = u;
    document.querySelectorAll('[data-unit]').forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-unit') === u ? 'true' : 'false'); });
    update();
  }

  // events
  document.querySelectorAll('[data-unit]').forEach(function (b) { b.addEventListener('click', function () { setUnit(b.getAttribute('data-unit')); }); });
  document.querySelectorAll('[data-target]').forEach(function (b) { b.addEventListener('click', function () { $('lq-target').value = fmt(+b.getAttribute('data-target'), 1); update(); }); });
  document.querySelectorAll('[data-lvl]').forEach(function (b) { b.addEventListener('click', function () { var c = parse($('lq-cap').value); if (isFinite(c)) { $('lq-cur').value = fmt(c * b.getAttribute('data-lvl') / 100, 1); update(); } else $('lq-cap').focus(); }); });
  ['lq-cap', 'lq-target', 'lq-factor', 'lq-brix', 'lq-cur', 'lq-final', 'lq-brix2'].forEach(function (id) { $(id).addEventListener('input', update); });
  // machine table (all rows, 100 at a time, filtered with the same search)
  var fl = $('lq-filter'), tb = document.querySelector('#lq-table tbody'), more = $('lq-more'), cnt = $('lq-table-count'), shown = 100;
  function host(u) { try { return new URL(u).hostname.replace(/^www\./, ''); } catch (e) { return T('source', 'source'); } }
  function table() {
    if (!loaded || !tb) return;
    var v = fl ? fl.value.trim() : '', list = v ? search(v).hits.map(function (h) { return h.i; }) : rows.map(function (r, i) { return i; });
    var html = '';
    list.slice(0, shown).forEach(function (i) {
      var r = rows[i], note = fr ? r[6] : r[7];
      html += '<tr><td><b>' + esc(r[0]) + '</b> ' + esc(r[1]) + (note ? '<div class="lq-sub">' + esc(note) + '</div>' : '') + '</td><td>' + esc(TYPES[r[2]] || '') + '</td><td class="lq-r lq-num">'
        + (r[3] ? fmt(r[3], 0) + ' L · ' + fmt(r[4], 1) + ' gal' : T('non publiée — entrez la vôtre', 'not published — enter your own')) + '</td><td>'
        + (r[5] ? '<a href="' + esc(r[5]) + '" rel="nofollow noopener" target="_blank">' + esc(host(r[5])) + '</a>' : '')
        + (r[9] ? ' · <a href="' + esc(r[9]) + '" rel="nofollow noopener" target="_blank">' + T('fabricant', 'maker') + '</a>' : '') + '</td></tr>';
    });
    tb.innerHTML = html || '<tr><td colspan="4">' + T('Aucune machine.', 'No machine.') + '</td></tr>';
    if (cnt) cnt.textContent = T(fmt(Math.min(shown, list.length), 0) + ' sur ' + fmt(list.length, 0) + ' machines', fmt(Math.min(shown, list.length), 0) + ' of ' + fmt(list.length, 0) + ' machines');
    if (more) more.hidden = list.length <= shown;
  }
  if (fl) fl.addEventListener('input', function () { shown = 100; table(); });
  if (more) more.addEventListener('click', function () { shown += 100; table(); });

  function restore() {
    try {
      var st = JSON.parse(localStorage.getItem(KEY) || 'null');
      var qs = new URLSearchParams(location.search).get('m');
      if (st) { if (st.unit === 'gal') { unit = 'gal'; document.querySelectorAll('[data-unit]').forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-unit') === 'gal' ? 'true' : 'false'); }); }
        if (st.t) $('lq-target').value = st.t; if (st.f) $('lq-factor').value = st.f; }
      var want = qs || (st && st.m);
      if (want && !q.value) { var r0 = find(want); if (r0) { q.value = label(r0); syncClear(); pickMachine(r0); } }
      if (st && st.cap && !(machine && machine[3]) && !$('lq-cap').value) $('lq-cap').value = st.cap;
    } catch (e) {}
  }
  fetch(app.getAttribute('data-json')).then(function (r) { return r.json(); }).then(function (d) {
    rows = d.rows || []; index(); loaded = true; restore(); table(); if (isOpen) render(); update();
  }).catch(function () { loaded = true; if (isOpen) render(); });
  update();
})();

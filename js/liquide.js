/* CoupeFab — coolant calculator UI (/outils/calculateur-liquide-de-coupe/, /en/tools/coolant-calculator/). Math in liquide-math.js. */
(function () {
  'use strict';
  var app = document.getElementById('lq-app'); if (!app || !window.CFCoolant) return;
  var M = window.CFCoolant, fr = app.getAttribute('data-lang') === 'fr';
  var T = function (a, b) { return fr ? a : b; };
  var $ = function (id) { return document.getElementById(id); };
  var rows = []; try { rows = JSON.parse($('lq-data').textContent); } catch (e) {}
  var TYPES = { vmc: T('CU vertical', 'VMC'), hmc: T('CU horizontal', 'HMC'), '5ax': T('5 axes', '5-axis'), lathe: T('tour', 'lathe'),
    millturn: T('tour axe Y', 'mill-turn'), vtl: T('tour vertical', 'VTL'), boring: T('aléseuse', 'boring mill'), router: T('routeur', 'router') };
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

  // datalist
  var dl = $('lq-list'), frag = document.createDocumentFragment();
  rows.forEach(function (r) {
    var o = document.createElement('option');
    o.value = label(r);
    o.label = (r[3] ? fmt(r[3], 0) + ' L · ' + fmt(r[4], 1) + ' gal' : T('capacité à entrer', 'enter capacity')) + ' · ' + (TYPES[r[2]] || '');
    frag.appendChild(o);
  });
  dl.appendChild(frag);

  function find(q) {
    q = (q || '').toLowerCase().trim(); if (!q) return null;
    for (var i = 0; i < rows.length; i++) if (label(rows[i]).toLowerCase() === q) return rows[i];
    var hits = rows.filter(function (r) { return label(r).toLowerCase().indexOf(q) >= 0; });
    return hits.length === 1 ? hits[0] : null;
  }
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
  var q = $('lq-q');
  q.addEventListener('input', function () { var r = find(q.value); if (r && r !== machine) { pickMachine(r); update(); } });
  q.addEventListener('change', function () { var r = find(q.value); pickMachine(r); update(); });
  document.querySelectorAll('[data-unit]').forEach(function (b) { b.addEventListener('click', function () { setUnit(b.getAttribute('data-unit')); }); });
  document.querySelectorAll('[data-target]').forEach(function (b) { b.addEventListener('click', function () { $('lq-target').value = fmt(+b.getAttribute('data-target'), 1); update(); }); });
  document.querySelectorAll('[data-lvl]').forEach(function (b) { b.addEventListener('click', function () { var c = parse($('lq-cap').value); if (isFinite(c)) { $('lq-cur').value = fmt(c * b.getAttribute('data-lvl') / 100, 1); update(); } else $('lq-cap').focus(); }); });
  ['lq-cap', 'lq-target', 'lq-factor', 'lq-brix', 'lq-cur', 'lq-final', 'lq-brix2'].forEach(function (id) { $(id).addEventListener('input', update); });
  // table filter
  var fl = $('lq-filter'), trs = Array.prototype.slice.call(document.querySelectorAll('#lq-table tbody tr'));
  if (fl) fl.addEventListener('input', function () {
    var v = fl.value.toLowerCase().trim();
    trs.forEach(function (tr) { tr.hidden = v && tr.getAttribute('data-q').indexOf(v) < 0; });
  });

  // restore + ?m= deep link
  try {
    var st = JSON.parse(localStorage.getItem(KEY) || 'null');
    var qs = new URLSearchParams(location.search).get('m');
    if (st) { if (st.unit === 'gal') { unit = 'gal'; document.querySelectorAll('[data-unit]').forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-unit') === 'gal' ? 'true' : 'false'); }); }
      if (st.t) $('lq-target').value = st.t; if (st.f) $('lq-factor').value = st.f; }
    var want = qs || (st && st.m);
    if (want) { var r0 = find(want); if (r0) { q.value = label(r0); pickMachine(r0); } }
    if (st && st.cap && !(machine && machine[3])) $('lq-cap').value = st.cap;
  } catch (e) {}
  update();
})();

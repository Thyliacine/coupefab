/* CoupeFab — coolant mixing math (pure, unit-free: any volume unit in = same unit out).
   Concentrations are in percent (5 = 5 %). Used by js/liquide.js and tests/test_liquide_math.js. */
(function (root) {
  'use strict';
  var GAL = 3.785411784; // litres per US gallon

  function num(x) { return typeof x === 'number' && isFinite(x); }

  // Fresh fill: volume V at c % -> concentrate and water.
  function freshFill(V, c) {
    if (!num(V) || !num(c) || V <= 0 || c <= 0 || c >= 100) return null;
    var conc = V * c / 100;
    return { concentrate: conc, water: V - conc, ratio: (100 - c) / c }; // ratio = parts water per part concentrate
  }

  // Refractometer: true % = Brix x factor; target Brix = target % / factor.
  function trueConc(brix, factor) {
    if (!num(brix) || brix < 0) return null;
    var f = num(factor) && factor > 0 ? factor : 1;
    return brix * f;
  }
  function targetBrix(target, factor) {
    var f = num(factor) && factor > 0 ? factor : 1;
    return num(target) ? target / f : null;
  }

  // Correction / top-up.
  //   cur: current volume in the tank, cc: current true %, ct: target %, final: wanted final volume (<= capacity).
  // Returns the plan to reach exactly `final` at `ct` with the least work:
  //   {kind:'ok'}                         already on target and level
  //   {kind:'add', concentrate, water}    add both (premix at `premix` %), no draining
  //   {kind:'drain', drain, concentrate, water}  must remove `drain` first (too rich or too lean for the room left)
  // plus the quick "minimum" fix that ignores the level (only concentrate or only water) when it fits.
  function correct(cur, cc, ct, final) {
    if (![cur, cc, ct, final].every(num) || cur < 0 || final <= 0 || cc < 0 || cc >= 100 || ct <= 0 || ct >= 100) return null;
    var eps = 1e-9, out = {};
    var C = (final * ct - cur * cc) / 100;   // concentrate to add to land on target at `final`
    var W = final - cur - C;                 // water to add
    if (C >= -eps && W >= -eps) {
      C = Math.max(0, C); W = Math.max(0, W);
      out = { kind: (C + W) < eps ? 'ok' : 'add', drain: 0, concentrate: C, water: W, premix: (C + W) > eps ? 100 * C / (C + W) : ct };
    } else if (C < 0) {
      // too rich: keep y litres, then fill with water only. y*cc = final*ct
      var keepR = final * ct / cc;
      out = { kind: 'drain', drain: Math.max(0, cur - keepR), concentrate: 0, water: final - Math.min(cur, keepR), premix: 0, reason: 'rich' };
    } else {
      // too lean: keep y litres, then fill with concentrate only. y*(100-cc) = final*(100-ct)
      var keepL = final * (100 - ct) / (100 - cc);
      out = { kind: 'drain', drain: Math.max(0, cur - keepL), concentrate: final - Math.min(cur, keepL), water: 0, premix: 100, reason: 'lean' };
    }
    // quick fix (no level target): only concentrate when lean, only water when rich
    if (cc < ct) out.quick = { concentrate: cur * (ct - cc) / (100 - ct), water: 0 };
    else if (cc > ct) out.quick = { concentrate: 0, water: cur * (cc / ct - 1) };
    else out.quick = { concentrate: 0, water: 0 };
    out.quick.fits = (cur + out.quick.concentrate + out.quick.water) <= final + eps;
    return out;
  }

  var M = { GAL: GAL, freshFill: freshFill, trueConc: trueConc, targetBrix: targetBrix, correct: correct,
    toL: function (v, u) { return u === 'gal' ? v * GAL : v; }, fromL: function (v, u) { return u === 'gal' ? v / GAL : v; } };
  if (typeof module !== 'undefined' && module.exports) module.exports = M; else root.CFCoolant = M;
})(this);

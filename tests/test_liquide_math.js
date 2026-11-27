// node tests/test_liquide_math.js — unit checks for js/liquide-math.js
const M = require('../js/liquide-math.js');
let n = 0, bad = 0;
const near = (a, b, tol = 1e-6) => Math.abs(a - b) <= tol;
function ok(cond, msg) { n++; if (!cond) { bad++; console.error('FAIL', msg); } }
const conc = (vol, pct) => vol * pct / 100;

// fresh fill: Haas VF-2, 208 L at 6 % -> 12.48 L concentrate + 195.52 L water
let f = M.freshFill(208, 6);
ok(near(f.concentrate, 12.48) && near(f.water, 195.52), 'fresh fill 208 L @ 6 %');
ok(near(f.ratio, 94 / 6), 'water:concentrate ratio');
f = M.freshFill(55, 7.5); // Haas VF-4 example from GAL Manufacturing: 4.1 gal concentrate, 50.9 gal water
ok(near(f.concentrate, 4.125) && near(f.water, 50.875), 'fresh fill 55 gal @ 7.5 %');
ok(M.freshFill(0, 5) === null && M.freshFill(100, 0) === null && M.freshFill(100, 100) === null, 'fresh fill rejects bad input');

// refractometer
ok(near(M.trueConc(4, 1.5), 6), 'Brix 4 x factor 1.5 = 6 %');
ok(near(M.trueConc(5, undefined), 5), 'factor defaults to 1.0');
ok(near(M.targetBrix(7, 1.4), 5), 'target 7 % / factor 1.4 = Brix 5');

// correction: lean tank, room to top up. 150 L at 4 %, target 6 %, fill to 208 L
let r = M.correct(150, 4, 6, 208);
ok(r.kind === 'add', 'lean top-up is add');
ok(near(conc(150, 4) + r.concentrate, conc(208, 6)) && near(150 + r.concentrate + r.water, 208), 'lean top-up lands on 208 L @ 6 %');
ok(near(r.quick.concentrate, 150 * 2 / 94) && r.quick.fits, 'quick fix: concentrate only');

// rich tank (evaporation): 180 L at 9 %, target 6 %, fill to 208 L -> needs water and maybe concentrate
r = M.correct(180, 9, 6, 208);
// 180*9 = 1620 > 208*6 = 1248 -> too rich even when filled with water -> drain
ok(r.kind === 'drain' && r.reason === 'rich', 'rich tank must drain');
const keep = 180 - r.drain;
ok(near(conc(keep, 9), conc(208, 6)) && near(keep + r.water, 208), 'rich drain plan lands on 208 L @ 6 %');
ok(near(r.quick.water, 90) && !r.quick.fits, 'quick water fix (90 L) does not fit');

// slightly rich, room enough: 100 L at 8 %, target 6 %, final 208 L -> add water + some concentrate
r = M.correct(100, 8, 6, 208);
ok(r.kind === 'add' && near(conc(100, 8) + r.concentrate, conc(208, 6)) && near(100 + r.concentrate + r.water, 208), 'rich but room: premix top-up');
ok(r.premix < 6, 'premix leaner than target when sump is rich');

// very lean, full tank: 208 L at 1 %, target 8 %, final 208 -> drain then concentrate
r = M.correct(208, 1, 8, 208);
ok(r.kind === 'drain' && r.reason === 'lean', 'lean full tank must drain');
const keep2 = 208 - r.drain;
ok(near(conc(keep2, 1) + r.concentrate, conc(208, 8)) && near(keep2 + r.concentrate, 208), 'lean drain plan lands on target');

// on target and level
r = M.correct(208, 6, 6, 208);
ok(r.kind === 'ok' && near(r.concentrate, 0) && near(r.water, 0), 'already on target');
// same concentration, low level -> premix at target
r = M.correct(100, 6, 6, 208);
ok(r.kind === 'add' && near(r.premix, 6) && near(r.concentrate, 108 * 0.06), 'level-only top-up premix at target');

// units
ok(near(M.toL(55, 'gal'), 208.197648, 1e-6) && near(M.fromL(M.toL(10, 'gal'), 'gal'), 10), 'gallon conversion');
ok(M.correct(-1, 5, 6, 100) === null && M.correct(10, 5, 0, 100) === null, 'correct rejects bad input');

console.log(`${n - bad}/${n} checks passed`);
process.exit(bad ? 1 : 0);

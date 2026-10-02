/* panels.js — one drawing function per shot (shots 1-50). Panel space 1800x840.
   cam: [scale,x,y] -> [scale,x,y] over the shot (pan/zoom from the sheet's movement).
   subs: start seconds for each sub-scene when a shot alternates (shot-reverse-shot, montage). */
const PANELS = {};
(() => {
  const K = SK, W = 1800, H = 840, R = K.RED;
  const topCrowd = (x0, y0, x1, y1, n) => { K.G(); for (let i = 0; i < n; i++) { const x = x0 + K.rnd() * (x1 - x0), y = y0 + K.rnd() * (y1 - y0); K.ell(x, y, 5, 4, { w: 1.8 }); K.ell(x, y + 3, 8, 3.2, { w: 1.2, o: .6 }); } };
  const topStalls = (x0, y0, nx, ny, dx, dy) => { for (let r = 0; r < ny; r++) { K.G(); for (let c = 0; c < nx; c++) { const x = x0 + c * dx, y = y0 + r * dy; K.solid(K.box(x, y, dx - 24, 34)); K.rect(x, y, dx - 24, 34, { w: 2.2 }); K.hatch(K.box(x, y, dx - 24, 34), { a: c % 2 ? 60 : -60, g: 7, op: .55 }); } } };
  const wideBack = (bg) => { // generic mela backdrop: ground, stalls row, bulbs
    K.night(0, 0, W, 190, 11); K.bulbs(0, 150, 900, 120, 16, 30, true); K.bulbs(850, 120, 1800, 160, 16, 30, true);
    K.stall(80, 600, 260, 220, { goods: 'toy' }); K.stall(1380, 600, 300, 230, { goods: 'food' });
  };

  PANELS[1] = { seed: 1, cam: [[1, 0, 0], [1.28, -40, -60]], draw() { // ELS drone push-in over the mela
    K.night(0, 0, W, H, 18);
    K.wheel(560, 330, 250); K.G(); for (let i = 0; i < 24; i++) { const a = i * Math.PI / 12; K.ell(560 + Math.cos(a) * 250, 330 + Math.sin(a) * 250, 5, 5, { w: 2 }); }
    topStalls(900, 130, 8, 5, 110, 100); topStalls(120, 650, 6, 2, 130, 90);
    for (let r = 0; r < 5; r++) K.bulbs(880, 118 + r * 100, 1800, 118 + r * 100, 22, 8, true);
    K.G(); K.line(600, 120, 880, 120, { w: 2.2 }); topCrowd(860, 100, 1780, 640, 70); topCrowd(0, 560, 900, 800, 40); topCrowd(300, 590, 900, 640, 30); topCrowd(60, 60, 280, 340, 20);
    K.G(); [[1210, 300], [980, 510], [1500, 420]].forEach(p => K.disc(p[0], p[1], 7, 7, R, .95));
    K.sup(60, 90, 'GHANTA 00', { size: 46 });
  } };

  PANELS[2] = { seed: 2, cam: [[1.04, 0, 0], [1, 0, 0]], draw() { // crowd through ferris wheel spokes
    K.night(0, 0, W, 240, 12); K.G(); const cx = 900, cy = 380;
    for (let i = 0; i < 14; i++) { const a = i * Math.PI / 7 + .1; K.line(cx + Math.cos(a) * 120, cy + Math.sin(a) * 120, cx + Math.cos(a) * 900, cy + Math.sin(a) * 900, { w: 7 }); K.line(cx + Math.cos(a) * 130 + 10, cy + Math.sin(a) * 130, cx + Math.cos(a) * 900 + 10, cy + Math.sin(a) * 900, { w: 2, o: .6 }); }
    K.ell(cx, cy, 120, 120, { w: 8 }); K.ell(cx, cy, 340, 340, { w: 5 });
    K.crowd(0, W, 470, 4, 22);
    K.balloon(260, 380, 26, 'red'); K.balloon(700, 340, 22); K.balloon(1180, 360, 24); K.balloon(1540, 330, 22); K.balloon(1000, 300, 18);
    K.G(); for (let i = 0; i < 7; i++) { const x = 300 + i * 190; K.P(K.crv([[x, 520], [x + 20, 470], [x - 10, 430], [x + 22, 390]], false), { c: K.PEN, w: 2.4, o: .6 }); }
  } };

  PANELS[3] = { seed: 3, cam: [[1, 120, 0], [1.1, -140, 0]], draw() { // family walking from behind, arcs
    wideBack(); K.ground(700, 0, W); K.crowd(0, W, 450, 2, 16);
    K.fig({ x: 660, y: 700, h: 470, role: 'father', dir: 'b', pose: 'walk' }); K.fig({ x: 900, y: 700, h: 430, role: 'mother', dir: 'b', pose: 'walk' });
    K.fig({ x: 1180, y: 700, h: 300, role: 'dhruv', dir: 'b', pose: 'walk' }); K.fig({ x: 1380, y: 700, h: 330, role: 'girl', dir: 'b', pose: 'walk' });
    K.G(); K.arrow(500, 790, 1000, 790, { w: 2.6, c: K.PEN });
  } };

  PANELS[4] = { seed: 4, cam: [[1, 0, 0], [1.04, 0, 0]], draw() { // MCU Dhruv low angle, zip pin plant
    K.G(); K.hatch(K.box(0, 0, W, H), { a: 60, g: 26, op: .25 });
    K.fig({ x: 900, y: 1500, h: 1550, role: 'dhruv', dir: 'f', pose: 'grip', mood: 's' });
    K.G(); K.ell(906, 636, 60, 50, { w: 3, c: K.INK }); K.line(960, 600, 1200, 520, { w: 2.4 }); K.text(1210, 520, 'SAFETY PIN ON ZIP', { size: 34, font: 'Oswald', w: 600 }); K.text(1210, 560, '(plant - pays off in shot 78)', { size: 26, font: 'Mono', w: 400, fill: K.PEN });
    K.G(); // father's hand + finger from top right
    K.solid([[1180, 0], [1500, 0], [1500, 260], [1330, 300], [1230, 220]]); K.poly([[1180, 0], [1230, 220], [1330, 300], [1500, 260]], { w: 3 }, true);
    K.poly([[1240, 230], [1280, 340], [1320, 342], [1316, 250]], { w: 3 }, true); K.hatch([[1180, 0], [1500, 0], [1500, 260], [1330, 300], [1230, 220]], { a: 80, g: 11, op: .35 });
    K.G(); K.arrow(1000, 790, 1180, 640, { w: 2.4, c: K.PEN });
  } };

  PANELS[5] = { seed: 5, cam: [[1, 0, 0], [1.08, 0, 0]], draw() { // Dhruv POV balloons on pole, crowd soft foreground
    K.night(0, 0, W, 300, 12); K.bulbs(0, 90, W, 120, 20, 30, true);
    K.G(); K.line(1100, 760, 1100, 160, { w: 7 }); K.line(1112, 760, 1112, 160, { w: 2, o: .6 });
    const cols = [[1100, 230, 70], [1020, 340, 64], [1180, 330, 66], [960, 470, 60], [1260, 480, 62], [1090, 480, 66], [1010, 600, 58], [1200, 610, 60]];
    cols.forEach((c, i) => K.balloon(c[0], c[1], c[2], i === 2 ? 'red' : (i % 2 ? '#D8D4CA' : '#CFCBC2'), { sway: J2(i) }));
    K.crowd(-40, W + 40, 690, 3, 34);
  } };
  const J2 = i => (i % 2 ? 8 : -8);

  PANELS[6] = { seed: 6, cam: [[1.06, 0, 0], [1, 20, 0]], draw() { // Dhruv tugging mother's dupatta; parents cut at frame top
    wideBack(); K.stall(1100, 700, 560, 470, { goods: 'toy' });
    K.fig({ x: 960, y: 1180, h: 1120, role: 'mother', dir: 'r', pose: 'pointR' }); K.fig({ x: 1350, y: 1160, h: 1100, role: 'father', dir: 'l', pose: 'cross' });
    K.fig({ x: 720, y: 820, h: 500, role: 'dhruv', dir: 'r', pose: 'tug', mood: 'w' });
    K.G(); K.arrow(560, 360, 330, 300, { w: 2.6, c: K.PEN }); K.balloon(250, 270, 40, 'red');
  } };

  PANELS[7] = { seed: 7, cam: [[1.0, 0, 0], [1.1, 0, 0]], draw() { // ECU hand slips out of father's hand (slow motion)
    K.G(); K.hatch(K.box(0, 0, W, H), { a: 60, g: 30, op: .22 });
    K.G(); const big = [[260, 150], [620, 130], [760, 260], [800, 420], [700, 560], [420, 600], [240, 450]]; K.solid(big); K.wash(big, '#E8DCD0', .8); K.poly(big, { w: 4 }, true);
    for (let i = 0; i < 4; i++) { const y0 = 180 + i * 85; K.poly([[720, y0], [920, y0 + 20], [1010, y0 + 50], [980, y0 + 90], [720, y0 + 72]], { w: 3 }, true); }
    K.G(); const small = [[900, 470], [1020, 440], [1150, 470], [1270, 540], [1180, 610], [980, 610]]; K.solid(small); K.wash(small, '#EDE2D8', .8); K.poly(small, { w: 3.4 }, true);
    for (let i = 0; i < 3; i++) K.poly([[1180, 470 + i * 36], [1330, 490 + i * 36], [1325, 520 + i * 36], [1180, 505 + i * 36]], { w: 2.6 }, true);
    K.G(); K.arrow(1100, 760, 1500, 760, { w: 2.6, c: K.PEN }); K.line(1340, 420, 1500, 380, { w: 1.6, c: K.PEN, o: .6 }); K.line(1360, 560, 1530, 560, { w: 1.6, c: K.PEN, o: .6 });
    K.G(); K.hatch(K.box(1450, 300, 330, 400), { a: 80, g: 10, op: .3 });
  } };

  PANELS[8] = { seed: 8, cam: [[1, 0, 0], [1.03, 0, 0]], draw() { // deep staging: parents fg, Dhruv swallowed by crowd bg
    wideBack(); K.ground(700, 0, W); K.crowd(300, 1500, 440, 3, 14);
    K.fig({ x: 1180, y: 480, h: 150, role: 'dhruv', dir: 'r', pose: 'walk' });
    K.crowd(1060, 1500, 450, 1, 18);
    K.G(); K.hatch(K.box(0, 0, 700, H), { a: 60, g: 7, op: .13 });
    K.fig({ x: 380, y: 920, h: 940, role: 'father', dir: 'r', pose: 'hip' }); K.fig({ x: 640, y: 900, h: 870, role: 'mother', dir: 'r', pose: 'hip' });
  } };

  PANELS[9] = { seed: 9, cam: [[1.12, 0, 0], [1, 0, 0]], draw() { // mother turns, smile fading, looks down at empty space
    K.crowd(0, W, 150, 5, 30);
    K.G(); for (let i = 0; i < 12; i++) K.line(0, 60 + i * 70, W, 40 + i * 70 + J3(i), { w: 2, c: K.PEN, o: .5 });
    K.G(); K.solid(K.box(480, 0, 840, H));
    K.fig({ x: 900, y: 1420, h: 1500, role: 'mother', dir: 'f', pose: 'stand', mood: 's' });
    K.G(); K.sup(1180, 160, '+10 MIN', { size: 56 }); K.arrow(1000, 520, 700, 700, { w: 2.6, c: K.PEN });
  } };
  const J3 = i => (i % 3) * 9 - 9;

  PANELS[10] = { seed: 10, cam: [[1, 0, 0], [1.1, 0, 0]], draw() { // top-down: four figures splitting apart like a crack
    K.G(); topCrowd(0, 0, W, H, 150);
    K.G(); const c = [900, 420]; [[-620, -300], [560, -330], [-560, 300], [640, 330]].forEach(v => { const e = [c[0] + v[0], c[1] + v[1]]; K.P(K.crv([c, [c[0] + v[0] * .3 + 20, c[1] + v[1] * .3 - 14], [c[0] + v[0] * .62 - 18, c[1] + v[1] * .62 + 16], e], false), { c: K.INK, w: 3, o: 1 }); });
    K.G(); [[-620, -300], [560, -330], [-560, 300], [640, 330]].forEach((v, i) => { const x = c[0] + v[0], y = c[1] + v[1]; K.disc(x, y, 18, 15, i % 2 ? '#DAD6CC' : '#E4D9D3'); K.ell(x, y - 4, 10, 9, { w: 2.2 }); K.hatch(K.ellPts(x, y - 4, 10, 9, 8, 0), { a: 70, g: 3, c: K.INK, op: .9 }); });
  } };

  PANELS[11] = { seed: 11, budget: 2.6, draw() { // three quick inserts build up: father/jhoola, mother/toy stall, uncle/food cart
    const frame = (x, w, mk) => { K.G(); K.solid(K.box(x, 60, w, 720)); K.rect(x, 60, w, 720, { w: 4 }); mk(x, w); K.G(); K.sup(x + 24, 130, 'DHRUV!', { size: 60 }); };
    frame(30, 560, (x, w) => { K.night(x, 60, w, 140, 10); K.G(); K.line(x + 60, 220, x + 200, 560, { w: 2.4 }); K.line(x + 360, 220, x + 220, 560, { w: 2.4 }); K.rect(x + 150, 540, 140, 40, { w: 2.6 }); K.fig({ x: x + 320, y: 760, h: 620, role: 'father', dir: 'f', pose: 'callup', mood: 'o' }); });
    frame(620, 560, (x, w) => { K.stall(x + 20, 640, 300, 280, { goods: 'toy' }); K.fig({ x: x + 380, y: 760, h: 620, role: 'mother', dir: 'l', pose: 'wave', mood: 'o' }); });
    frame(1210, 560, (x, w) => { K.G(); K.rect(x + 40, 520, 280, 180, { w: 3 }); K.ell(x + 120, 480, 60, 24, { w: 3 }); K.ell(x + 120, 440, 40, 40, { w: 1.6, c: K.PEN, o: .6 }); K.fig({ x: x + 400, y: 760, h: 640, role: 'uncle', dir: 'l', pose: 'callup', mood: 'o' }); });
  } };

  PANELS[12] = { seed: 12, cam: [[1, 0, 0], [1.14, -40, 0]], draw() { // parents reach the balloon seller; balloons frame the foreground
    wideBack(); K.ground(700, 0, W);
    K.fig({ x: 1080, y: 700, h: 400, role: 'seller', dir: 'f', pose: 'stand', extra: 'mous' }); K.G(); K.line(1180, 700, 1180, 260, { w: 6 });
    [[1200, 330, 60], [1130, 250, 58], [1270, 280, 56], [1240, 430, 54], [1040, 230, 50]].forEach((b, i) => K.balloon(b[0], b[1], b[2], i === 1 ? 'red' : '#D8D4CA'));
    K.fig({ x: 400, y: 740, h: 330, role: 'father', dir: 'r', pose: 'walk', mood: 'w' }); K.fig({ x: 560, y: 740, h: 300, role: 'mother', dir: 'r', pose: 'walk', mood: 'w' });
    [[110, 260, 120], [260, 380, 110], [40, 520, 100]].forEach((b, i) => K.balloon(b[0], b[1], b[2], i === 2 ? '#CFCBC2' : '#D8D4CA'));
  } };
})();

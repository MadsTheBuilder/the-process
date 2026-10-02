/* panels2.js — shots 13-50 (continuation of panels.js). Same conventions. */
(() => {
  const K = SK, W = 1800, H = 840, R = K.RED, P = PANELS;
  const back = () => { K.night(0, 0, W, 190, 11); K.bulbs(0, 150, 900, 120, 16, 30, true); K.bulbs(850, 120, 1800, 160, 16, 30, true); };
  const frameBox = (x, y, w, h) => { K.G(); K.solid(K.box(x, y, w, h)); K.rect(x, y, w, h, { w: 4 }); };
  const gate = (x, y, w, h) => { K.G(); K.line(x, y, x, y - h, { w: 5 }); K.line(x + w, y, x + w, y - h, { w: 5 }); K.poly([[x - 20, y - h], [x + w / 2, y - h - 70], [x + w + 20, y - h]], { w: 4 }, true); K.text(x + w / 2, y - h - 18, 'MELA', { size: 40, font: 'Oswald', w: 600, anchor: 'middle' }); };
  const squig = (x, y, w, n, gap) => { K.G(); for (let i = 0; i < n; i++) K.line(x, y + i * gap, x + w * (.55 + K.rnd() * .45), y + i * gap + K.J(2), { w: 2, c: K.PEN, o: .8 }); };
  const mapWall = (x, y, w, h) => { K.G(); K.solid(K.box(x, y, w, h)); K.rect(x, y, w, h, { w: 3.4 }); K.hatch(K.box(x + 8, y + 8, w - 16, h - 16), { a: 45, g: 16, op: .25 });
    K.ell(x + w * .3, y + h * .45, h * .2, h * .2, { w: 2.4 }); for (let i = 0; i < 3; i++) for (let j = 0; j < 2; j++) K.rect(x + w * .55 + i * w * .13, y + h * .25 + j * h * .26, w * .09, h * .14, { w: 2 });
    K.P(K.crv([[x + 20, y + h * .85], [x + w * .4, y + h * .75], [x + w * .7, y + h * .88], [x + w - 20, y + h * .78]], false), { c: K.PEN, w: 2.4, o: 1 }); };

  P[13] = { seed: 13, cam: [[1, 0, 0], [1.07, 0, 0]], draw() { // father breathless, OTS seller
    back(); K.crowd(0, W, 560, 3, 18);
    K.fig({ x: 760, y: 1010, h: 1120, role: 'father', dir: 'f', pose: 'plead', mood: 'o', extra: 'sweat' });
    K.fig({ x: 1480, y: 1350, h: 1500, role: 'seller', dir: 'b', pose: 'stand' });
  } };

  P[14] = { seed: 14, cam: [[1, 0, 0], [1.03, 0, 0]], draw() { // seller answers quickly, pointing to gate
    K.night(0, 0, W, 170, 12); K.G(); K.line(430, 840, 430, 80, { w: 7 });
    [[430, 160, 80], [320, 270, 76], [540, 260, 78], [230, 420, 70], [630, 430, 72], [430, 380, 78]].forEach((b, i) => K.balloon(b[0], b[1], b[2], i === 4 ? 'red' : '#D8D4CA'));
    K.fig({ x: 1000, y: 1240, h: 1360, role: 'seller', dir: 'f', pose: 'pointR', mood: 'n', extra: 'mous' });
    gate(1560, 700, 200, 360);
  } };

  P[15] = { seed: 15, cam: [[1.02, 20, 0], [1.02, -20, 6]], draw() { // recreation: two men + Dhruv -> van (silhouettes)
    back(); K.ground(700, 0, W); gate(80, 700, 220, 380);
    K.van(1180, 700, 1.5, 'r');
    K.fig({ x: 640, y: 720, h: 520, role: 'man', dir: 'b', pose: 'pointR', silh: true, extra: 'cap' });
    K.fig({ x: 880, y: 720, h: 500, role: 'man', dir: 'b', pose: 'stand', silh: true });
    K.fig({ x: 820, y: 730, h: 320, role: 'dhruv', dir: 'b', pose: 'walk' });
    K.balloon(740, 400, 36, 'red');
    K.G(); K.hatch(K.box(0, 0, 240, H), { a: 60, g: 6, op: .28 }); K.hatch(K.box(1560, 0, 240, H), { a: 60, g: 6, op: .28 });
    K.G(); K.arrow(930, 800, 1180, 800, { w: 2.6, c: K.PEN });
  } };

  P[16] = { seed: 16, cam: [[1, 0, 0], [1.1, 0, 0]], draw() { // ECU father's face; mother's hand grips his arm
    K.G(); K.hatch(K.box(0, 0, W, H), { a: 60, g: 30, op: .18 });
    K.fig({ x: 800, y: 4350, h: 4500, role: 'father', dir: 'f', pose: 'rest', mood: 'w', extra: 'sweat' });
    K.G(); const hx = 1440, hy = 640; K.solid([[hx - 150, hy - 60], [hx + 160, hy - 90], [hx + 200, hy + 60], [hx - 120, hy + 100]]); K.poly([[hx - 150, hy - 60], [hx + 160, hy - 90], [hx + 200, hy + 60], [hx - 120, hy + 100]], { w: 4 }, true);
    for (let i = 0; i < 4; i++) K.poly([[hx - 150 + i * 30, hy - 60 + i * 12], [hx - 330 + i * 28, hy - 20 + i * 36], [hx - 310 + i * 28, hy + 30 + i * 36], [hx - 140 + i * 28, hy + 10 + i * 20]], { w: 3 }, true);
  } };

  P[17] = { seed: 17, subs: [0, 3], cam: [[1.9, 0, 260], [1, 0, 0]], budget: 2, draw() { // crane up into VFX map zoom-out
    K.night(0, 0, W, H, 16); K.ground(720, 0, W);
    K.fig({ x: 820, y: 720, h: 260, role: 'father', dir: 'b', pose: 'stand' }); K.fig({ x: 900, y: 720, h: 240, role: 'mother', dir: 'b', pose: 'stand' });
    K.nextSub();
    K.G(); K.solid(K.box(0, 0, W, H));
    K.P(K.crv([[420, 180], [700, 120], [1000, 160], [1320, 250], [1450, 430], [1360, 640], [1100, 760], [800, 740], [560, 650], [420, 470]], true), { c: K.INK, w: 3.6, o: 1 }); K.hatch([[420, 180], [700, 120], [1000, 160], [1320, 250], [1450, 430], [1360, 640], [1100, 760], [800, 740], [560, 650], [420, 470]], { a: 40, g: 18, op: .3 });
    K.text(620, 220, 'UTTAR PRADESH', { size: 46, font: 'Oswald', w: 600 });
    K.G(); K.ell(900, 540, 120, 90, { w: 3 }); K.text(900, 700, 'MIRZAPUR', { size: 34, font: 'Oswald', w: 600, anchor: 'middle' });
    K.G(); K.disc(900, 540, 12, 12, R, .95); K.text(930, 520, 'MELA', { size: 28, font: 'Oswald', w: 500 });
    K.G(); K.arrow(900, 540, 1110, 300, { w: 2.6, c: K.PEN }); K.pin(1130, 300, K.INK); K.text(1160, 290, 'LUCKNOW HQ', { size: 36, font: 'Oswald', w: 600 });
  } };

  P[18] = { seed: 18, subs: [0, 12], budget: 9, draw() { // macro montage of uniform details, ends on SHO? IO? CO?
    const cells = [[40, 50], [630, 50], [1220, 50], [40, 450], [630, 450], [1220, 450]];
    const v = (i, f) => { const [x, y] = cells[i]; frameBox(x, y, 540, 340); K.G(); K.hatch(K.box(x + 10, y + 10, 520, 320), { a: 45, g: 14, op: .22 }); f(x, y); };
    const strap = (x, y, n, rib) => { K.G(); K.solid(K.box(x + 60, y + 110, 420, 120)); K.wash(K.box(x + 60, y + 110, 420, 120), K.KHAKI, .9); K.rect(x + 60, y + 110, 420, 120, { w: 3.4 }); for (let i = 0; i < n; i++) K.star(x + 150 + i * 110, y + 170, 36, { w: 3, fill: K.GOLD }); if (rib) { K.rect(x + 80, y + 240, 380, 18, { w: 3 }); K.hatch(K.box(x + 82, y + 242, 376, 14), { a: 0, g: 4, c: K.INK, op: .8 }); } };
    v(0, (x, y) => strap(x, y, 3)); v(1, (x, y) => strap(x, y, 1, true));
    v(2, (x, y) => { K.G(); K.ell(x + 270, y + 170, 110, 110, { w: 3.4 }); K.ell(x + 270, y + 170, 90, 90, { w: 1.6 }); for (let i = 0; i < 3; i++) K.ell(x + 210 + i * 60, y + 130, 22, 24, { w: 2.6 }); K.rect(x + 200, y + 190, 140, 40, { w: 3 }); K.ell(x + 270, y + 210, 16, 16, { w: 2 }); for (let i = 0; i < 12; i++) { const a = i * Math.PI / 6; K.line(x + 270 + Math.cos(a) * 6, y + 210 + Math.sin(a) * 6, x + 270 + Math.cos(a) * 16, y + 210 + Math.sin(a) * 16, { w: 1, j: .2 }); } });
    v(3, (x, y) => { K.G(); K.rect(x + 40, y + 120, 460, 90, { w: 4 }); K.rect(x + 190, y + 100, 160, 130, { w: 4 }); K.star(x + 270, y + 165, 44, { w: 3, fill: K.GOLD }); K.hatch(K.box(x + 44, y + 124, 140, 82), { a: 0, g: 5, c: K.INK, op: .6 }); });
    v(4, (x, y) => { K.G(); K.solid(K.box(x + 70, y + 110, 400, 110)); K.rect(x + 70, y + 110, 400, 110, { w: 4 }); K.ell(x + 90, y + 130, 6, 6, { w: 2 }); K.ell(x + 450, y + 130, 6, 6, { w: 2 }); K.text(x + 270, y + 190, 'R A V I', { size: 70, font: 'Oswald', w: 600, anchor: 'middle' }); });
    v(5, (x, y) => { K.G(); const sh = [[x + 270, y + 60], [x + 400, y + 100], [x + 380, y + 230], [x + 270, y + 290], [x + 160, y + 230], [x + 140, y + 100]]; K.wash(sh, K.GOLD, .8); K.poly(sh, { w: 3.6 }, true); K.star(x + 270, y + 170, 50, { w: 3 }); K.ell(x + 270, y + 170, 70, 70, { w: 1.6 }); });
    K.nextSub(); K.G(); K.solid(K.box(0, 0, W, H));
    K.text(900, 360, 'SHO?', { size: 220, font: 'Oswald', w: 700, anchor: 'middle' }); K.text(900, 560, 'IO?', { size: 220, font: 'Oswald', w: 700, anchor: 'middle' }); K.text(900, 760, 'CO?', { size: 220, font: 'Oswald', w: 700, anchor: 'middle' });
  } };

  P[19] = { seed: 19, cam: [[1, 0, 0], [1, 0, 0]], budget: 3, draw() { // title card on black sky; red balloon rises
    K.G(); K.FILL('M0 0H1800V840H0Z', '#1E1C1A', 1);
    for (let i = 0; i < 40; i++) K.disc(K.rnd() * W, K.rnd() * H, 2, 2, K.PAPER, .6);
    K.tag('bal'); K.G(); K.FILL(K.crv(K.ellPts(900, 560, 60, 78, 12, 0).slice(0, -1), true), R, .96); K.ell(900, 560, 60, 78, { c: K.PAPER, w: 2.4 });
    K.P(K.crv([[900, 640], [880, 720], [915, 800], [895, 880]], false), { c: K.PAPER, w: 1.8, o: .9 });
    K.G(); K.text(900, 170, 'OPERATION', { size: 120, font: 'Oswald', w: 600, fill: K.PAPER, anchor: 'middle' });
    K.G(); K.text(900, 370, 'RED', { size: 190, font: 'Oswald', w: 700, fill: R, anchor: 'middle' }); K.text(900, 510, 'BALLOON', { size: 120, font: 'Oswald', w: 600, fill: K.PAPER, anchor: 'middle' });
  }, anim(tl, svg, t0, dur, q) { tl.fromTo(q('[data-n=bal]'), { y: 260 }, { y: -430, duration: dur, ease: 'power1.in' }, t0); } };

  P[20] = { seed: 20, cam: [[1, 0, 0], [1.05, 0, 0]], draw() { // parents + seller hurry to chowki; Ravi outside
    back(); K.ground(700, 0, W); K.tin(1100, 360, 520, 340);
    K.G(); K.poly([[1070, 360], [1650, 360], [1620, 300], [1100, 300]], { w: 3.4 }, true); K.rect(1250, 470, 140, 230, { w: 3 }); K.rect(1180, 160, 380, 70, { w: 3 }); K.text(1370, 215, 'MELA CHOWKI', { size: 46, font: 'Oswald', w: 600, anchor: 'middle' });
    K.G(); K.line(1060, 700, 1060, 360, { w: 4 });
    K.fig({ x: 1030, y: 700, h: 430, role: 'ravi', dir: 'l', pose: 'hold' });
    K.tag('w1'); K.fig({ x: 300, y: 740, h: 400, role: 'father', dir: 'r', pose: 'walk', mood: 'w' }); K.tag('w2'); K.fig({ x: 460, y: 740, h: 370, role: 'mother', dir: 'r', pose: 'walk', mood: 'w' }); K.tag('w3'); K.fig({ x: 640, y: 740, h: 380, role: 'seller', dir: 'r', pose: 'walk', extra: 'mous' });
    K.sup(60, 100, 'GHANTA 00:20', { size: 46 });
  }, anim(tl, svg, t0, dur, q) { ['w1', 'w2', 'w3'].forEach((n, i) => tl.fromTo(q(`[data-n=${n}]`), { x: -60 }, { x: 160 - i * 30, duration: dur, ease: 'none' }, t0)); } };

  P[21] = { seed: 21, cam: [[1, 0, 0], [1.04, 0, 0]], draw() { // Ravi turns (freeze) + lower third
    back(); K.tin(1250, 160, 500, 600); K.G(); K.hatch(K.box(0, 0, W, H), { a: 55, g: 36, op: .15 });
    K.fig({ x: 760, y: 1380, h: 1520, role: 'ravi', dir: 'f', pose: 'hold', mood: 'n' });
    K.lower3(60, 700, 'CONSTABLE', 'MELA DUTY');
  } };

  P[22] = { seed: 22, cam: [[1.04, 0, 0], [1, 10, 0]], draw() { // father pleading, mother behind; Ravi's shoulder at frame edge
    back(); K.tin(900, 200, 800, 500); K.ground(760, 0, W);
    K.fig({ x: 380, y: 1000, h: 1000, role: 'mother', dir: 'r', pose: 'clasp', mood: 'w' }); K.fig({ x: 760, y: 1060, h: 1100, role: 'father', dir: 'r', pose: 'plead', mood: 'o' });
    K.fig({ x: 1560, y: 1200, h: 1400, role: 'ravi', dir: 'l', pose: 'stand' });
  } };

  P[23] = { seed: 23, cam: [[1, 0, 0], [1.03, 0, 0]], draw() { // Ravi calm, immediate
    K.G(); K.hatch(K.box(0, 0, W, H), { a: 60, g: 34, op: .16 });
    K.fig({ x: 900, y: 2760, h: 2900, role: 'ravi', dir: 'f', pose: 'rest', mood: 'n' });
    K.radio(1180, 600, 3);
  } };

  P[24] = { seed: 24, cam: [[1, 0, 0], [1.05, 0, 0]], budget: 1.5, draw() { // phone screen top-down, Dhruv's photo arrives
    K.G(); K.hatch(K.box(0, 0, W, H), { a: 60, g: 30, op: .15 });
    K.phone(620, 30, 560, 780); frameBox(670, 140, 460, 560);
    K.G(); K.hatch(K.box(680, 150, 440, 540), { a: 0, g: 30, op: .15 });
    K.G(); K.solid(K.box(720, 220, 360, 300)); K.rect(720, 220, 360, 300, { w: 3 });
    K.fig({ x: 900, y: 560, h: 520, role: 'dhruv', dir: 'f', pose: 'rest', mood: 'n' });
    squig(720, 570, 300, 3, 34);
    K.G(); for (let i = 1; i <= 3; i++) K.P(K.crv([[1300 - i * 40, 150 + i * 10], [1300, 150 - i * 40], [1300 + i * 40, 150 + i * 10]], false), { c: K.INK, w: 3, o: 1 - i * .2 });
  } };

  P[25] = { seed: 25, cam: [[1, 0, 0], [1.05, -30, 0]], draw() { // Ravi rapid-fire questions; seller points to lane/gate
    back(); K.ground(740, 0, W); gate(1450, 740, 240, 380); K.van(980, 600, .8, 'l');
    K.fig({ x: 380, y: 1000, h: 1080, role: 'ravi', dir: 'r', pose: 'hold', mood: 'a' });
    K.fig({ x: 1000, y: 1000, h: 1020, role: 'seller', dir: 'l', pose: 'pointR', extra: 'mous' });
    K.G(); K.arrow(780, 330, 1000, 280, { w: 2.4, c: K.PEN });
  } };

  P[26] = { seed: 26, cam: [[1, 0, 0], [1.06, 0, 0]], budget: 2, draw() { // Ravi on wireless + radio grille insert
    K.G(); K.hatch(K.box(0, 0, W, H), { a: 60, g: 34, op: .15 });
    K.fig({ x: 760, y: 2500, h: 2640, role: 'ravi', dir: 'r', pose: 'rest', mood: 'a' });
    K.radio(1130, 340, 2.2); K.G(); K.P(K.crv([[1170, 300], [1240, 240], [1290, 100]], false), { c: K.INK, w: 4, o: 1 });
    K.G(); K.solid(K.ellPts(1480, 540, 230, 230, 14, 0).slice(0, -1)); K.ell(1480, 540, 230, 230, { w: 5 }); K.ell(1480, 540, 190, 190, { w: 2 });
    for (let i = 0; i < 6; i++) K.line(1360, 460 + i * 36, 1600, 460 + i * 36, { w: 3 });
    K.text(1480, 810, 'WIRELESS', { size: 34, font: 'Oswald', w: 600, anchor: 'middle' });
  } };

  P[27] = { seed: 27, budget: 4, draw() { // montage: constables across the mela receive the message
    const cell = (x, y, w, h, bgf, role, pose, label) => { frameBox(x, y, w, h); bgf(x, y, w, h); K.fig({ x: x + w * .6, y: y + h - 14, h: h * .84, role, dir: 'f', pose, mood: 'a' }); K.G(); K.text(x + 16, y + 42, label, { size: 30, font: 'Oswald', w: 600 }); };
    cell(30, 60, 560, 380, (x, y) => gate(x + 60, y + 360, 120, 150), 'cst', 'phone', 'GATE');
    cell(610, 60, 560, 380, (x, y) => { K.G(); K.rect(x + 40, y + 250, 120, 60, { w: 3 }); K.rect(x + 300, y + 250, 130, 60, { w: 3 }); K.ell(x + 70, y + 316, 14, 14, { w: 2 }); K.ell(x + 130, y + 316, 14, 14, { w: 2 }); }, 'cst', 'radio', 'PARKING');
    cell(1190, 60, 580, 380, (x, y) => { K.G(); K.line(x + 60, y + 60, x + 140, y + 270, { w: 3 }); K.line(x + 200, y + 60, x + 140, y + 270, { w: 3 }); K.rect(x + 100, y + 270, 80, 30, { w: 3 }); }, 'cst', 'phone', 'JHOOLA');
    cell(30, 460, 700, 340, (x, y) => { K.G(); K.rect(x + 40, y + 160, 150, 120, { w: 3 }); K.hatch(K.box(x + 44, y + 220, 142, 56), { a: 60, g: 7, op: .5 }); }, 'cst', 'radio', 'FOOD LANE');
    cell(750, 460, 1020, 340, (x, y) => { K.stall(x + 40, y + 330, 340, 230, { goods: 'food' }); K.stall(x + 440, y + 330, 300, 200, { goods: 'toy' }); }, 'cst', 'phone', 'STALLS');
    K.G(); for (let i = 0; i < 5; i++) { const px = [300, 880, 1480, 280, 1160][i], py = [190, 190, 190, 570, 570][i]; for (let k = 0; k < 6; k++) { const a = k * 1.05; K.line(px + Math.cos(a) * 36, py + Math.sin(a) * 36, px + Math.cos(a) * 58, py + Math.sin(a) * 58, { w: 1.6, o: .7, j: .3 }); } }
  } };

  P[28] = { seed: 28, cam: [[1, 0, 0], [1.1, 0, 0]], budget: 2, draw() { // top-down map, constables as glowing dots
    K.night(0, 0, W, H, 22); K.G(); K.rect(70, 70, 1660, 700, { w: 4 });
    K.wheel(520, 380, 230, { noCabins: true });
    for (let r = 0; r < 4; r++) { K.G(); for (let c = 0; c < 8; c++) { K.solid(K.box(900 + c * 100, 130 + r * 120, 70, 48)); K.rect(900 + c * 100, 130 + r * 120, 70, 48, { w: 2.4 }); } }
    K.G(); K.line(780, 70, 780, 770, { w: 2, c: K.PEN }); K.rect(120, 640, 460, 100, { w: 2.4 }); K.text(130, 720, 'PARKING', { size: 28, font: 'Oswald', w: 500, fill: K.PEN }); K.text(1520, 756, 'GATE', { size: 28, font: 'Oswald', w: 500, fill: K.PEN });
    [[300, 200], [740, 300], [1000, 560], [1380, 330], [560, 700], [1500, 640], [850, 120], [1250, 600]].forEach((p, i) => { K.tag('d' + i); K.G(); K.disc(p[0], p[1], 14, 14, K.GOLD, .95); K.ell(p[0], p[1], 34, 34, { w: 2, o: .6 }); K.ell(p[0], p[1], 56, 56, { w: 1.4, o: .35 }); });
  }, anim(tl, svg, t0, dur, q) { for (let i = 0; i < 8; i++) tl.to(q('[data-n=d' + i + ']'), { x: (i % 2 ? -1 : 1) * (60 + i * 14), y: (i % 3 - 1) * 70, duration: dur - 1, ease: 'sine.inOut' }, t0 + 1); } };

  P[29] = { seed: 29, budget: 5, draw() { // GOLDEN HOURS: hourglass draining; SP/DGP fade, constable glows
    K.G(); K.text(900, 130, 'GOLDEN HOURS', { size: 100, font: 'Oswald', w: 700, anchor: 'middle', fill: K.GOLD });
    K.G(); const cx = 520, top = 190, bot = 760; K.line(cx - 230, top, cx + 230, top, { w: 6 }); K.line(cx - 230, bot, cx + 230, bot, { w: 6 });
    K.P(K.crv([[cx - 190, top], [cx - 190, top + 120], [cx - 20, top + 260], [cx - 20, top + 290]], false), { c: K.INK, w: 4, o: 1 }); K.P(K.crv([[cx + 190, top], [cx + 190, top + 120], [cx + 20, top + 260], [cx + 20, top + 290]], false), { c: K.INK, w: 4, o: 1 });
    K.P(K.crv([[cx - 20, bot - 290], [cx - 20, bot - 260], [cx - 190, bot - 120], [cx - 190, bot]], false), { c: K.INK, w: 4, o: 1 }); K.P(K.crv([[cx + 20, bot - 290], [cx + 20, bot - 260], [cx + 190, bot - 120], [cx + 190, bot]], false), { c: K.INK, w: 4, o: 1 });
    K.tag('sandT'); K.G(); K.FILL('M' + (cx - 170) + ' ' + (top + 80) + 'L' + (cx + 170) + ' ' + (top + 80) + 'L' + (cx + 20) + ' ' + (top + 250) + 'L' + (cx - 20) + ' ' + (top + 250) + 'Z', K.GOLD, .85);
    K.tag('sandB'); K.G(); K.FILL('M' + (cx - 20) + ' ' + (bot - 80) + 'L' + (cx + 20) + ' ' + (bot - 80) + 'L' + (cx + 150) + ' ' + (bot - 4) + 'L' + (cx - 150) + ' ' + (bot - 4) + 'Z', K.GOLD, .85);
    // rank icons
    K.tag('sp'); K.G(); K.star(1050, 360, 60, { w: 3.4 }); K.text(1050, 480, 'SP', { size: 60, font: 'Oswald', w: 600, anchor: 'middle' });
    K.tag('dgp'); K.G(); for (let i = 0; i < 3; i++) K.star(1330 + i * 70 - 70, 360, 36, { w: 3 }); K.text(1330, 480, 'DGP', { size: 60, font: 'Oswald', w: 600, anchor: 'middle' });
    K.tag('cst'); K.G(); K.ell(1150, 650, 120, 120, { w: 3, c: K.GOLD }); K.ell(1150, 650, 90, 90, { w: 2, c: K.GOLD }); K.fig({ x: 1150, y: 740, h: 200, role: 'ravi', dir: 'f', pose: 'rest' }); K.text(1300, 670, 'CONSTABLE', { size: 56, font: 'Oswald', w: 600, fill: K.GOLD });
  }, anim(tl, svg, t0, dur, q) {
    tl.to(q('[data-n=sandT]'), { scaleY: .02, transformOrigin: '50% 100%', svgOrigin: '520 440', duration: dur - 3, ease: 'none' }, t0 + 3);
    tl.fromTo(q('[data-n=sandB]'), { scaleY: .2, svgOrigin: '520 760' }, { scaleY: 2.3, svgOrigin: '520 760', duration: dur - 3, ease: 'none' }, t0 + 3);
    tl.to(q('[data-n=sp]'), { opacity: .12, duration: 1.2 }, t0 + 5); tl.to(q('[data-n=dgp]'), { opacity: .12, duration: 1.2 }, t0 + 5.6);
  } };

  P[30] = { seed: 30, budget: 12, draw() { // POWER METER introduced, five bars one by one
    K.G(); K.text(180, 130, 'POWER METER', { size: 96, font: 'Oswald', w: 700 });
    K.meter(180, 210, 1440, [0, 0, 0, 0, 0], { rh: 106, fs: 56 });
  } };

  const meterShot = (n, role, extra, pose, vals, label, who) => {
    P[n] = { seed: n, cam: [[1, 0, 0], [1.03, 0, 0]], budget: 3, draw() {
      K.G(); K.hatch(K.box(0, 0, 780, H), { a: 60, g: 30, op: .13 });
      K.fig({ x: 420, y: 1300, h: 1480, role, dir: 'f', pose, mood: 'n', extra });
      K.G(); K.text(900, 100, 'POWER METER', { size: 58, font: 'Oswald', w: 700 }); K.text(900, 148, who, { size: 34, font: 'Oswald', w: 500, fill: K.PEN });
      K.meter(900, 190, 860, vals, { rh: 74, fs: 34 });
      K.mapInset(1020, 600, 620, 160, label);
    } };
  };
  meterShot(31, 'ravi', '', 'radio', [5, 1, 1, 0, 1], 'MAP: MELA GROUND', 'CONSTABLE RAVI');

  P[32] = { seed: 32, cam: [[1, 0, 0], [1.18, -110, 0]], draw() { // Ravi pushes into the chowki through the doorway
    K.tin(80, 100, 1640, 600); K.tube(560, 150, 700); K.ground(700, 80, 1720);
    K.desk(1050, 480, 480, 180); K.G(); K.rect(1150, 190, 280, 200, { w: 3 });
    K.fig({ x: 760, y: 780, h: 620, role: 'ravi', dir: 'r', pose: 'walk' });
    K.G(); K.solid(K.box(0, 0, 150, H)); K.solid(K.box(1650, 0, 150, H)); K.hatch(K.box(0, 0, 150, H), { a: 70, g: 8, c: K.INK, op: .8 }); K.hatch(K.box(1650, 0, 150, H), { a: 70, g: 8, c: K.INK, op: .8 }); K.line(150, 0, 150, H, { w: 8 }); K.line(1650, 0, 1650, H, { w: 8 });
  } };

  P[33] = { seed: 33, cam: [[1.02, 0, 0], [1, 0, 0]], draw() { // Mishra at desk, wireless set, hand-drawn map on wall
    K.tin(60, 60, 1680, 640); K.tube(600, 90, 500); mapWall(160, 180, 560, 380);
    K.fig({ x: 1150, y: 800, h: 700, role: 'mishra', dir: 'f', pose: 'desk', extra: 'mous' });
    K.desk(780, 560, 740, 260); K.radio(960, 470, 1.8);
    K.lower3(60, 720, 'HEAD CONSTABLE', 'CHOWKI DUTY');
  } };

  P[34] = { seed: 34, subs: [0], budget: 4, cam: [[1, 0, 0], [1.03, 0, 0]], draw() { // Mishra orders; finger taps map points
    K.G(); K.hatch(K.box(0, 0, 760, H), { a: 60, g: 30, op: .13 });
    K.fig({ x: 380, y: 1900, h: 2050, role: 'mishra', dir: 'f', pose: 'rest', mood: 'a', extra: 'mous' });
    mapWall(800, 80, 940, 680);
    [['EXIT GATE', 1500, 400], ['PARKING', 1000, 560], ['JHOOLE', 1180, 200]].forEach(p => { K.G(); K.pin(p[1], p[2], K.RED); K.text(p[1] + 18, p[2] - 14, p[0], { size: 30, font: 'Oswald', w: 600 }); });
    K.tag('finger'); K.G(); K.poly([[1500, 360], [1520, 330], [1545, 336], [1540, 420], [1600, 560], [1500, 570]], { w: 3.2 }, true);
  }, anim(tl, svg, t0, dur, q) { const f = q('[data-n=finger]'); tl.set(f, { x: 0, y: 0 }, t0); tl.to(f, { x: -500, y: 160, duration: .5 }, t0 + 3); tl.to(f, { x: -320, y: -160, duration: .5 }, t0 + 5.5); tl.to(f, { x: 0, y: 0, duration: .5 }, t0 + 8); } };

  P[35] = { seed: 35, budget: 4, draw() { // orders carried out: 4 mini-scenes
    const cell = (x, y, label, mk) => { frameBox(x, y, 860, 380); mk(x, y); K.G(); K.text(x + 18, y + 44, label, { size: 32, font: 'Oswald', w: 600 }); };
    cell(30, 50, 'GATE CHECKING', (x, y) => { K.G(); K.line(x + 100, y + 270, x + 700, y + 230, { w: 5 }); K.line(x + 100, y + 270, x + 100, y + 340, { w: 4 }); K.fig({ x: x + 560, y: y + 360, h: 280, role: 'cst', dir: 'l', pose: 'point' }); });
    cell(910, 50, 'PARKING CCTV', (x, y) => { K.G(); K.rect(x + 280, y + 80, 300, 170, { w: 4 }); for (let i = 0; i < 4; i++) K.rect(x + 296 + (i % 2) * 140, y + 96 + Math.floor(i / 2) * 76, 124, 64, { w: 2 }); K.fig({ x: x + 200, y: y + 370, h: 300, role: 'cst', dir: 'r', pose: 'rest' }); K.fig({ x: x + 660, y: y + 370, h: 300, role: 'cst', dir: 'l', pose: 'rest' }); });
    cell(30, 450, 'KAPIL + SNEHA: STALLS', (x, y) => { K.stall(x + 440, y + 340, 360, 220, { goods: 'toy' }); K.fig({ x: x + 160, y: y + 360, h: 280, role: 'cst', dir: 'r', pose: 'walk' }); K.fig({ x: x + 290, y: y + 360, h: 270, role: 'aditi', dir: 'r', pose: 'walk' }); });
    cell(910, 450, 'RAVI + PARENTS -> JEEP', (x, y) => { K.jeep(x + 470, y + 330, .9, 'r'); K.fig({ x: x + 120, y: y + 360, h: 280, role: 'ravi', dir: 'r', pose: 'point' }); K.fig({ x: x + 250, y: y + 360, h: 270, role: 'father', dir: 'r', pose: 'walk', mood: 'w' }); K.fig({ x: x + 350, y: y + 360, h: 250, role: 'mother', dir: 'r', pose: 'walk', mood: 'w' }); });
  } };

  P[36] = { seed: 36, budget: 3, draw() { // split screen REACTION vs PLAN
    K.G(); K.hatch(K.box(0, 0, 880, H), { a: 60, g: 32, op: .12 }); K.line(900, 0, 900, H, { w: 8 });
    K.text(60, 110, 'REACTION', { size: 80, font: 'Oswald', w: 700 }); K.text(960, 110, 'PLAN', { size: 80, font: 'Oswald', w: 700 });
    K.fig({ x: 450, y: 1010, h: 1000, role: 'ravi', dir: 'f', pose: 'radio', mood: 'a' });
    mapWall(960, 200, 780, 420); K.fig({ x: 1350, y: 1020, h: 900, role: 'mishra', dir: 'f', pose: 'pointR', extra: 'mous' });
  } };

  meterShot(37, 'mishra', 'mous', 'rest', [5, 2, 1, 2, 1], 'MAP: MELA CHOWKI', 'HEAD CONSTABLE MISHRA');

  P[38] = { seed: 38, cam: [[1.05, 110, 0], [1.05, -110, 0]], draw() { // jeep with parents + seller leaves; red-blue lights
    back(); K.stall(60, 600, 300, 230, { goods: 'toy' }); K.stall(1380, 600, 340, 240, { goods: 'food' }); K.ground(700, 0, W); K.crowd(0, W, 470, 2, 18);
    K.tag('jeep'); K.jeep(560, 700, 1.9, 'r');
    K.tag('lights'); K.G(); K.wash([[770, 360], [830, 360], [830, 410], [770, 410]], K.RED, .8); K.wash([[840, 360], [900, 360], [900, 410], [840, 410]], '#3A6EA5', .8);
    for (let i = 0; i < 6; i++) { K.line(800, 380, 800 + Math.cos(i * 1.04 - .6) * 160 - 60, 380 + Math.sin(i * 1.04 - .6) * 100 - 140, { w: 1.4, c: K.PEN, o: .6 }); }
  }, anim(tl, svg, t0, dur, q) { tl.fromTo(q('[data-n=jeep],[data-n=lights]'), { x: -120 }, { x: 420, duration: dur, ease: 'none' }, t0); } };

  P[39] = { seed: 39, cam: [[1, 0, 0], [1.05, 0, 0]], draw() { // police station exterior at night; jeep arrives
    K.night(0, 0, W, H, 9); K.ground(700, 0, W);
    K.G(); K.solid(K.box(480, 250, 900, 450)); K.rect(480, 250, 900, 450, { w: 4 }); K.poly([[460, 250], [1400, 250], [1400, 220], [460, 220]], { w: 3 }, true); K.rect(860, 440, 140, 260, { w: 3.4 }); K.rect(600, 330, 120, 100, { w: 3 }); K.rect(1140, 330, 120, 100, { w: 3 });
    K.rect(640, 120, 580, 80, { w: 3.4 }); K.text(930, 178, 'POLICE STATION', { size: 54, font: 'Oswald', w: 600, anchor: 'middle' });
    K.hatch(K.box(484, 254, 892, 440), { a: 70, g: 14, op: .25 }); K.tube(790, 225, 280);
    K.tag('jeep'); K.jeep(40, 700, 1.5, 'r');
    K.sup(60, 100, 'GHANTA 01:00', { size: 46 });
  }, anim(tl, svg, t0, dur, q) { tl.fromTo(q('[data-n=jeep]'), { x: -300 }, { x: 0, duration: 3, ease: 'power2.out' }, t0); } };

  P[40] = { seed: 40, cam: [[1.03, 0, 0], [1, 0, 0]], draw() { // ASI Aditi at duty desk, register open
    K.tin(60, 60, 1680, 640); K.G(); K.rect(1180, 150, 420, 260, { w: 3.4 }); for (let i = 0; i < 4; i++) K.rect(1210 + (i % 2) * 190, 180 + Math.floor(i / 2) * 110, 160, 90, { w: 1.6, c: K.PEN }); K.tube(600, 90, 500);
    K.fig({ x: 900, y: 800, h: 700, role: 'aditi', dir: 'f', pose: 'desk' });
    K.desk(520, 560, 780, 260); K.G(); K.poly([[740, 520], [900, 540], [1060, 520], [1050, 570], [900, 585], [750, 570]], { w: 2.6 }, true); K.line(900, 540, 900, 585, { w: 2 }); for (let i = 0; i < 3; i++) { K.line(770, 540 + i * 10, 880, 552 + i * 10, { w: 1, c: K.PEN }); K.line(920, 552 + i * 10, 1030, 540 + i * 10, { w: 1, c: K.PEN }); }
    K.lower3(60, 720, 'ASI', 'DUTY DESK');
  } };

  P[41] = { seed: 41, subs: [0, 2, 4, 6, 8, 10], show: [0, 1, 0, 1, 0, 1], budget: 1.2, draw() { // shot / reverse shot
    K.G(); K.tin(60, 60, 1680, 700);
    K.fig({ x: 900, y: 1620, h: 1750, role: 'aditi', dir: 'r', pose: 'desk', mood: 'n' });
    K.nextSub(); K.G(); K.hatch(K.box(60, 60, 1680, 700), { a: 55, g: 30, op: .14 }); K.G(); K.line(1500, 60, 1500, 760, { w: 3, c: K.PEN });
    K.fig({ x: 900, y: 1620, h: 1750, role: 'seller', dir: 'l', pose: 'clasp', mood: 'w', extra: 'mous' });
  } };

  P[42] = { seed: 42, cam: [[1, 0, 0], [1.04, 0, 0]], draw() { // mother leans in; Aditi answers firmly
    K.tin(60, 60, 1680, 700); K.G(); K.hatch(K.box(60, 60, 1680, 700), { a: 55, g: 30, op: .12 });
    K.fig({ x: 520, y: 1520, h: 1700, role: 'mother', dir: 'r', pose: 'plead', mood: 'w' }); K.fig({ x: 1280, y: 1520, h: 1700, role: 'aditi', dir: 'l', pose: 'desk', mood: 'g' });
  } };

  P[43] = { seed: 43, budget: 1.2, draw() { // FIR written and stamped
    K.G(); K.hatch(K.box(0, 0, W, H), { a: 60, g: 30, op: .14 });
    K.G(); const pg = [[480, 60], [1330, 40], [1360, 800], [450, 810]]; K.solid(pg); K.poly(pg, { w: 4 }, true);
    K.rect(540, 110, 760, 90, { w: 3 }); K.text(580, 175, 'FIR', { size: 70, font: 'Oswald', w: 700 }); K.rect(980, 120, 300, 70, { w: 2.4 });
    for (let i = 0; i < 9; i++) K.line(540, 260 + i * 56, 540 + 560 + K.J(120), 260 + i * 56 + K.J(3), { w: 2, c: K.PEN });
    K.tag('mark'); K.G(); K.ell(1100, 560, 120, 120, { w: 5 }); K.ell(1100, 560, 92, 92, { w: 2 }); K.star(1100, 560, 44, { w: 3 }); K.line(1100, 420, 1100, 360, { w: 2, o: .6 });
    K.tag('stamp'); K.G(); K.solid(K.box(1030, 150, 140, 280)); K.rect(1030, 330, 140, 100, { w: 5 }); K.rect(1060, 150, 80, 190, { w: 4 }); K.ell(1100, 140, 60, 24, { w: 4 });
    K.G(); for (let i = 0; i < 8; i++) { const a = i * .78; K.line(1100 + Math.cos(a) * 140, 560 + Math.sin(a) * 140, 1100 + Math.cos(a) * 190, 560 + Math.sin(a) * 190, { w: 3 }); }
  }, anim(tl, svg, t0, dur, q) { tl.set(q('[data-n=mark]'), { opacity: 0 }, t0); tl.fromTo(q('[data-n=stamp]'), { y: -190 }, { y: 130, duration: .5, ease: 'power2.in' }, t0 + 1.4); tl.to(q('[data-n=stamp]'), { y: -190, duration: .6 }, t0 + 2.2); tl.set(q('[data-n=mark]'), { opacity: 1 }, t0 + 1.9); } };

  P[44] = { seed: 44, cam: [[1, 0, 0], [1.16, 0, 0]], budget: 6, draw() { // push in on FIR; question cards appear
    K.G(); K.hatch(K.box(0, 0, W, H), { a: 60, g: 30, op: .14 });
    K.G(); const pg = [[640, 60], [1160, 50], [1180, 800], [620, 810]]; K.solid(pg); K.poly(pg, { w: 4 }, true); K.rect(680, 100, 440, 70, { w: 3 }); K.text(710, 154, 'FIR', { size: 54, font: 'Oswald', w: 700 });
    for (let i = 0; i < 9; i++) K.line(680, 230 + i * 60, 680 + 340 + K.J(60), 230 + i * 60, { w: 2, c: K.PEN });
    [['WITNESS?', 140, 180], ['CCTV?', 1260, 180], ['VAN?', 140, 540], ['IO?', 1260, 540]].forEach((c, i) => { K.G(); K.solid(K.box(c[1], c[2], 380, 190)); K.rect(c[1], c[2], 380, 190, { w: 4 }); K.text(c[1] + 190, c[2] + 125, c[0], { size: 76, font: 'Oswald', w: 700, anchor: 'middle' }); K.ell(c[1] + 20, c[2] + 20, 7, 7, { w: 2 }); });
  } };

  P[45] = { seed: 45, subs: [0, 5, 9], show: [0, 1, 0], budget: 2, draw() { // Aditi on phone / Khan silhouette at another scene
    K.tin(60, 60, 1680, 700); K.fig({ x: 900, y: 1600, h: 1740, role: 'aditi', dir: 'f', pose: 'phone', mood: 'n' });
    K.nextSub(); K.night(0, 0, W, H, 12); K.ground(720, 0, W);
    K.G(); K.line(100, 620, 800, 560, { w: 5 }); K.line(1000, 560, 1700, 620, { w: 5 }); for (let i = 0; i < 16; i++) { const t = i / 16; K.hatch(K.box(100 + t * 700, 590 - t * 50, 40, 20), { a: 45, g: 5, c: K.INK, op: .9, w: 2 }); K.hatch(K.box(1000 + t * 700, 560 + t * 40, 40, 20), { a: 45, g: 5, c: K.INK, op: .9, w: 2 }); }
    K.fig({ x: 900, y: 760, h: 760, role: 'khan', dir: 'b', pose: 'phone', silh: true });
    K.fig({ x: 1420, y: 740, h: 300, role: 'cst', dir: 'f', pose: 'rest', silh: true });
  } };

  meterShot(46, 'aditi', '', 'rest', [4, 2, 2, 1, 1], 'MAP: POLICE STATION PROCESS', 'ASI ADITI');

  P[47] = { seed: 47, cam: [[1, 0, 0], [1.04, 10, 0]], draw() { // father asks to speak to the Inspector
    K.tin(60, 60, 1680, 700); K.tube(600, 90, 500);
    K.fig({ x: 1260, y: 760, h: 760, role: 'aditi', dir: 'l', pose: 'desk' }); K.desk(900, 540, 700, 260);
    K.fig({ x: 520, y: 1000, h: 1040, role: 'father', dir: 'r', pose: 'plead', mood: 'w' });
  } };

  P[48] = { seed: 48, budget: 9, draw() { // RANK vs POST
    K.G(); K.line(900, 80, 900, 780, { w: 4 });
    K.text(60, 120, 'RANK', { size: 90, font: 'Oswald', w: 700 }); K.text(1000, 120, 'POST', { size: 90, font: 'Oswald', w: 700 });
    K.G(); K.solid(K.box(100, 220, 680, 260)); K.wash(K.box(100, 220, 680, 260), K.KHAKI, .9); K.rect(100, 220, 680, 260, { w: 5 }); for (let i = 0; i < 3; i++) K.star(250 + i * 170, 350, 66, { w: 4, fill: K.GOLD });
    K.text(440, 580, 'INSPECTOR', { size: 90, font: 'Oswald', w: 600, anchor: 'middle' });
    K.G(); K.text(900, 440, 'vs', { size: 70, font: 'Mono', w: 400, anchor: 'middle', fill: K.PEN });
    K.G(); K.solid(K.box(1020, 250, 680, 200)); K.rect(1020, 250, 680, 200, { w: 6 }); K.ell(1050, 280, 8, 8, { w: 2 }); K.ell(1670, 280, 8, 8, { w: 2 }); K.ell(1050, 420, 8, 8, { w: 2 }); K.ell(1670, 420, 8, 8, { w: 2 }); K.text(1360, 395, 'SHO', { size: 190, font: 'Oswald', w: 700, anchor: 'middle' });
    K.text(1360, 580, 'STATION HOUSE OFFICER', { size: 52, font: 'Oswald', w: 600, anchor: 'middle' });
  } };

  P[49] = { seed: 49, cam: [[1, 0, 0], [1.1, 0, 0]], draw() { // seller unprompted: too helpful
    K.tin(60, 60, 1680, 700); K.G(); K.hatch(K.box(60, 60, 1680, 700), { a: 55, g: 30, op: .12 });
    K.fig({ x: 900, y: 1720, h: 1900, role: 'seller', dir: 'f', pose: 'clasp', mood: 's', extra: 'mous' });
  } };

  P[50] = { seed: 50, cam: [[1, 0, 0], [1, 0, 0]], draw() { // Aditi nods; mother on the wooden bench behind
    K.tin(60, 60, 1680, 700); K.tube(600, 90, 500);
    K.fig({ x: 1260, y: 618, h: 520, role: 'mother', dir: 'f', pose: 'clasp', mood: 'w' }); K.bench(1000, 560, 520);
    K.tag('aditi'); K.fig({ x: 500, y: 780, h: 640, role: 'aditi', dir: 'r', pose: 'desk', mood: 'n' }); K.desk(220, 560, 560, 220);
  }, anim(tl, svg, t0, dur, q) { tl.to(q('[data-n=aditi]'), { y: 10, duration: .3, yoyo: true, repeat: 3 }, t0 + 1); } };
})();

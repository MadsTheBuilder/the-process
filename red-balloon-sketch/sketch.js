/* sketch.js — procedural pencil-sketch engine. Deterministic (seeded). Panel space is 1800x840.
   A shot = begin(seed) ... end() -> SVG markup. Shapes are collected into groups (one group per
   figure/prop, call G()); index.html draws each group on, group by group.                       */
const SK = (() => {
  const INK = '#26231F', PEN = '#8A857B', BLUE = '#C3CDDB', KHAKI = '#D9CFAE', RED = '#D62D20', GOLD = '#D9A21B', PAPER = '#F3EFE6', DARK = '#3A3631';
  let s = 1, subs, sub, cur, pend = null;
  const rnd = () => { s |= 0; s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  const J = a => (rnd() - .5) * 2 * a;
  const f = n => Math.round(n * 10) / 10;
  const st0 = { c: INK, w: 2.6, o: 1 };
  const S = (o) => Object.assign({}, st0, o || {});

  function begin(seed) { s = seed * 7919 + 13; subs = []; sub = []; subs.push(sub); G(); }
  function nextSub() { sub = []; subs.push(sub); G(); }
  function G() { cur = { items: [], n: pend }; pend = null; sub.push(cur); }
  function tag(n) { pend = n; }
  function P(d, st) {
    const k = st.c + '|' + st.w + '|' + st.o, last = cur.items[cur.items.length - 1];
    if (last && last.k === k && !last.fill) last.d += d; else cur.items.push({ k, d, st });
  }
  function FILL(d, color, op) { cur.items.push({ k: 'f' + color, d, fill: color, op: op == null ? 1 : op }); }
  function TEXT(x, y, str, o) { o = o || {}; cur.items.push({ text: str, x, y, o }); }

  // ---- primitives -------------------------------------------------------------------------
  function seg(x1, y1, x2, y2, jit) {
    const L = Math.hypot(x2 - x1, y2 - y1) || 1, nx = -(y2 - y1) / L, ny = (x2 - x1) / L;
    const j = jit == null ? Math.min(2.2, L * .02 + .6) : jit, m = .35 + rnd() * .3, b = J(j);
    return `M${f(x1 + J(.7))} ${f(y1 + J(.7))}Q${f(x1 + (x2 - x1) * m + nx * b)} ${f(y1 + (y2 - y1) * m + ny * b)} ${f(x2 + J(.7))} ${f(y2 + J(.7))}`;
  }
  function line(x1, y1, x2, y2, o) {
    const L = Math.hypot(x2 - x1, y2 - y1), n = Math.max(1, Math.round(L / 140)); let d = '';
    for (let i = 0; i < n; i++) d += seg(x1 + (x2 - x1) * i / n, y1 + (y2 - y1) * i / n, x1 + (x2 - x1) * (i + 1) / n, y1 + (y2 - y1) * (i + 1) / n, o && o.j);
    P(d, S(o));
    if (L > 60 && rnd() < .35) { const q = seg(x1 + J(2), y1 + J(2), x2 + J(2), y2 + J(2), 1.2); P(q, S({ w: .9, o: .45, c: o && o.c })); }
  }
  function crv(pts, closed) { // catmull-rom -> bezier
    const n = pts.length, g = i => pts[(i + n) % n]; let d = `M${f(pts[0][0])} ${f(pts[0][1])}`;
    const last = closed ? n : n - 1;
    for (let i = 0; i < last; i++) {
      const p0 = closed ? g(i - 1) : pts[Math.max(i - 1, 0)], p1 = g(i), p2 = g(i + 1), p3 = closed ? g(i + 2) : pts[Math.min(i + 2, n - 1)];
      d += `C${f(p1[0] + (p2[0] - p0[0]) / 6)} ${f(p1[1] + (p2[1] - p0[1]) / 6)} ${f(p2[0] - (p3[0] - p1[0]) / 6)} ${f(p2[1] - (p3[1] - p1[1]) / 6)} ${f(p2[0])} ${f(p2[1])}`;
    }
    return d;
  }
  function ellPts(cx, cy, rx, ry, n, over) {
    const a0 = rnd() * 6.28, pts = [], tot = 6.283 * (1 + (over || 0));
    for (let i = 0; i <= n * (1 + (over || 0)); i++) { const a = a0 + tot * i / n, k = 1 + J(.025) + (over ? i / n * .02 : 0); pts.push([cx + Math.cos(a) * rx * k, cy + Math.sin(a) * ry * k]); }
    return pts;
  }
  function ell(cx, cy, rx, ry, o) { P(crv(ellPts(cx, cy, rx, ry, Math.max(9, Math.round((rx + ry) / 7)), .1), false), S(o)); }
  function disc(cx, cy, rx, ry, color, o) { FILL(crv(ellPts(cx + 2, cy + 1.5, rx, ry, 12, 0).slice(0, -1), true), color, o); ell(cx, cy, rx, ry, o && o.st); }
  function poly(pts, o, open) {
    const n = pts.length;
    for (let i = 0; i < (open ? n - 1 : n); i++) { const a = pts[i], b = pts[(i + 1) % n]; line(a[0], a[1], b[0], b[1], o); }
  }
  function rect(x, y, w, h, o) { poly([[x, y], [x + w, y], [x + w, y + h], [x, y + h]], o); }
  function pd(pts) { return 'M' + pts.map(p => f(p[0] + J(1)) + ' ' + f(p[1] + J(1))).join('L') + 'Z'; }
  function wash(pts, color, op) { FILL(pd(pts.map(p => [p[0] + 2, p[1] + 1.5])), color, op); }
  function solid(pts, color) { FILL('M' + pts.map(p => f(p[0]) + ' ' + f(p[1])).join('L') + 'Z', color || PAPER, 1); }
  function hatch(pts, o) { // scanline hatch of polygon
    o = o || {}; const a = (o.a == null ? 45 : o.a) * Math.PI / 180, g = o.g || 9, dx = Math.cos(a), dy = Math.sin(a), nx = -dy, ny = dx;
    let mn = 1e9, mx = -1e9; pts.forEach(p => { const v = p[0] * nx + p[1] * ny; mn = Math.min(mn, v); mx = Math.max(mx, v); });
    const st = S({ c: o.c || PEN, w: o.w || 1.3, o: o.op == null ? .75 : o.op });
    for (let v = mn + g / 2; v < mx; v += g * (.85 + rnd() * .3)) {
      const xs = [];
      for (let i = 0; i < pts.length; i++) {
        const A = pts[i], B = pts[(i + 1) % pts.length], va = A[0] * nx + A[1] * ny, vb = B[0] * nx + B[1] * ny;
        if ((va - v) * (vb - v) < 0) { const t = (v - va) / (vb - va), X = A[0] + (B[0] - A[0]) * t, Y = A[1] + (B[1] - A[1]) * t; xs.push(X * dx + Y * dy); }
      }
      xs.sort((p, q) => p - q);
      for (let i = 0; i + 1 < xs.length; i += 2) { const u1 = xs[i] + 2 + J(2), u2 = xs[i + 1] - 2 + J(2); if (u2 > u1) P(seg(u1 * dx + v * nx, u1 * dy + v * ny, u2 * dx + v * nx, u2 * dy + v * ny, .8), st); }
    }
  }
  function box(x, y, w, h) { return [[x, y], [x + w, y], [x + w, y + h], [x, y + h]]; }
  function text(x, y, str, o) { TEXT(x, y, str, o); }

  // ---- figures -------------------------------------------------------------------------
  // arm angles are [upper, fore] in degrees: 0 = hanging down, +90 = toward screen-right, 180 = straight up
  const POSE = {
    stand: [[-7, -3], [7, 3]], walk: [[-24, -34], [26, 42]], pointR: [[-7, -3], [78, 82]], pointL: [[-78, -82], [7, 3]],
    plead: [[-20, -80], [20, 80]], callup: [[-130, -165], [130, 165]], hip: [[-35, 55], [35, -55]], wave: [[-7, -3], [140, 175]],
    handsup: [[-100, -135], [100, 135]], cross: [[12, 100], [-12, -100]], desk: [[12, 38], [-12, -38]], hold: [[-14, -22], [50, 28]],
    radio: [[-7, -3], [22, 150]], phone: [[-7, -3], [28, 160]], tug: [[-10, -4], [62, 130]], grip: [[-6, -3], [118, 150]],
    point: [[-7, -3], [95, 95]], clasp: [[10, 140], [-10, -140]], rest: [[-4, -2], [4, 2]], sit: [[10, 38], [-10, -38]]
  };
  const WASH = { dhruv: BLUE, father: '#DAD6CC', mother: '#E4D9D3', seller: '#DAD6CC', ravi: KHAKI, mishra: KHAKI, aditi: KHAKI, khan: KHAKI, cst: KHAKI, cap: DARK, man: '#CFCBC2', girl: '#E4D9D3', uncle: '#D7D2C6', kid: '#D8D2C4' };
  const UNI = r => r === 'ravi' || r === 'mishra' || r === 'aditi' || r === 'khan' || r === 'cst';
  const rot = (pts, cx, cy, a) => { const c = Math.cos(a), s2 = Math.sin(a); return pts.map(p => [cx + (p[0] - cx) * c - (p[1] - cy) * s2, cy + (p[0] - cx) * s2 + (p[1] - cy) * c]); };
  const lerp = (a, b, t) => [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t];
  const mid = (a, b) => a + (b - a) * .55;
  function ellR(cx, cy, rx, ry, a, color, w) { const pts = rot(ellPts(cx, cy, rx, ry, 10, 0).slice(0, -1), cx, cy, a); if (color) FILL(crv(pts, true), color, 1); P(crv(rot(ellPts(cx, cy, rx, ry, 10, .08), cx, cy, a), false), S({ w })); }
  function tlimb(ax, ay, bx, by, w1, w2, color, w, shade) { // tapered limb
    const L = Math.hypot(bx - ax, by - ay) || 1, nx = -(by - ay) / L, ny = (bx - ax) / L;
    const q = [[ax + nx * w1 / 2, ay + ny * w1 / 2], [bx + nx * w2 / 2, by + ny * w2 / 2], [bx - nx * w2 / 2, by - ny * w2 / 2], [ax - nx * w1 / 2, ay - ny * w1 / 2]];
    solid(q); if (color) wash(q, color, .95);
    if (shade) hatch([q[3], q[2], lerp(q[2], q[1], .42), lerp(q[3], q[0], .42)], { a: 60, g: Math.max(4, w * 2), w: Math.max(1, w * .42), op: .55 });
    line(q[0][0], q[0][1], q[1][0], q[1][1], { w }); line(q[3][0], q[3][1], q[2][0], q[2][1], { w });
  }
  function fig(o) {
    const { x, y, h, role = 'father', dir = 'f', pose = 'stand', mood = 'n', silh } = o, kid = role === 'dhruv' || role === 'kid';
    const side = dir === 'l' || dir === 'r', sgn = dir === 'l' ? -1 : 1, uni = UNI(role), wc = silh ? DARK : (WASH[role] || '#DAD6CC');
    const lwf = Math.max(1, Math.min(2.1, h / 300)), W1 = 2.4 * lwf, W2 = 1.7 * lwf;
    const hr = h * (kid ? .105 : .066), hipY = y - h * (kid ? .42 : .5), shY = y - h * (kid ? .7 : .8);
    const sw = h * (kid ? .105 : .118) * (side ? .62 : 1), hw = sw * (role === 'mother' || role === 'girl' ? .92 : .8);
    const hcy = shY - h * .03 - hr, ua = h * (kid ? .15 : .165), fa = h * (kid ? .135 : .15), lw = Math.max(6, h * .046) * (kid ? .85 : 1);
    const arms = o.arms || POSE[pose] || POSE.stand, bodyX = x + (side ? sgn * hr * .1 : 0);
    if (o.n) tag(o.n); G();
    const ang = (d, L, ox, oy) => [ox + Math.sin(d * Math.PI / 180) * L, oy + Math.cos(d * Math.PI / 180) * L];
    const lc = silh ? DARK : (uni ? '#CBC1A0' : (kid ? '#CFCBC2' : '#C9C5BB'));
    // legs
    const stride = pose === 'walk' ? 1 : 0, ll = y - hipY, th = ll * .5, sh = ll * .5;
    const legs = side ? (stride ? [[sgn * 26, sgn * 4], [sgn * -22, sgn * -40]] : [[sgn * 4, 0], [sgn * -4, 0]]) : (stride ? [[-14, -6], [16, 8]] : [[-3, -1], [3, 1]]);
    const hipX = [bodyX - hw * .5, bodyX + hw * .5];
    [0, 1].forEach(i => {
      const hp = [hipX[i], hipY], k = ang(legs[i][0], th, hp[0], hp[1]), fo = ang(legs[i][1], sh, k[0], k[1]); if (stride && i === 1) fo[1] -= 7;
      tlimb(hp[0], hp[1], k[0], k[1], hw * .9, hw * .7, lc, W1, true); tlimb(k[0], k[1], fo[0], fo[1], hw * .7, hw * .5, lc, W1, true);
      const fx = fo[0] + (side ? sgn * hw * .45 : (i ? hw * .12 : -hw * .12)); ellR(fx, fo[1] + 4, hw * (side ? .75 : .42), 6 * lwf, 0, silh ? DARK : '#4A4540', W2);
    });
    // torso
    const hem = hipY + h * (role === 'mother' ? .17 : .03), md = shY + (hipY - shY) * .62, tx = bodyX;
    const L1 = [[tx - sw, shY + h * .012], [tx - sw * .88, shY + h * .1], [tx - hw * .9, md], [tx - hw * 1.06, hem]], R1 = [[tx + sw, shY + h * .012], [tx + sw * .88, shY + h * .1], [tx + hw * .9, md], [tx + hw * 1.06, hem]];
    const area = [[tx - sw, shY + 3], [tx, shY - 3], [tx + sw, shY + 3]].concat(R1.slice(1)).concat(L1.slice(1).reverse());
    solid(area); wash(area, wc, .95);
    if (!silh) hatch([[tx + sw * .35, shY + 6], [tx + sw, shY + 6], [tx + hw * 1.06, hem], [tx + hw * .45, hem]], { a: 65, g: Math.max(4, 3.2 * lwf), w: Math.max(1, lwf * .7), op: .45 });
    P(crv([[tx - sw, shY + 4], [tx, shY - 3], [tx + sw, shY + 4]], false), S({ w: W1 })); P(crv(L1, false), S({ w: W1 })); P(crv(R1, false), S({ w: W1 }));
    P(crv([[tx - hw * 1.06, hem], [tx, hem + 4], [tx + hw * 1.06, hem]], false), S({ w: W1 }));
    if (!silh) detail(o, { x: tx, shY, hipY, hem, sw, hw, h, uni, kid, side });
    // arms
    const sl = [tx - sw * .9, shY + h * .02], sr = [tx + sw * .9, shY + h * .02], hands = [];
    [[sl, arms[0]], [sr, arms[1]]].forEach(([sp, a]) => {
      const e = ang(a[0], ua, sp[0], sp[1]), wr = ang(a[1], fa, e[0], e[1]);
      tlimb(sp[0], sp[1], e[0], e[1], lw, lw * .82, silh ? DARK : wc, W1, true); tlimb(e[0], e[1], wr[0], wr[1], lw * .8, lw * .56, silh ? DARK : (uni || role === 'dhruv' ? wc : '#E6DED2'), W1, false);
      const aa = Math.atan2(wr[1] - e[1], wr[0] - e[0]); ellR(wr[0] + Math.cos(aa) * lw * .4, wr[1] + Math.sin(aa) * lw * .4, lw * .62, lw * .42, aa, silh ? DARK : PAPER, W2); hands.push(wr);
    });
    // neck + head
    solid([[tx - hr * .35, shY], [tx + hr * .35, shY], [tx + hr * .35, hcy + hr * .8], [tx - hr * .35, hcy + hr * .8]]);
    line(tx - hr * .35, shY, tx - hr * .33, hcy + hr * .85, { w: W2 }); line(tx + hr * .35, shY, tx + hr * .33, hcy + hr * .85, { w: W2 });
    head({ x: tx, y: hcy, r: hr, dir, mood, role, silh, h, lwf, extra: o.extra || '' });
    return { head: [tx, hcy], hands, hr, shY, hipY };
  }
  function detail(o, g) {
    const { x, shY, hipY, hem, sw, hw, h, uni, kid, side } = g, role = o.role, wf = Math.max(1.3, Math.min(2, h / 380));
    if (role === 'dhruv' || (role === 'kid' && o.zip)) { // jacket zip + safety pin (plant)
      line(x, shY, x, hem, { w: 2 * wf }); const px = x + 1, py = shY + (hipY - shY) * .42, r = Math.max(3.5, h * .017);
      for (let i = 1; i < 7; i++) line(x - 3, shY + (hem - shY) * i / 7, x + 3, shY + (hem - shY) * i / 7, { w: 1.2, o: .7, j: .2 });
      ell(px, py, r, r * .75, { w: 2.4 * wf }); ell(px, py, r * .45, r * .35, { w: 1.4 * wf }); line(px - r * .5, py + r * .6, px + r * 2.6, py + r * 1.9, { w: 2.2 * wf }); line(px + r * 2.6, py + r * 1.9, px + r * 2.6, py + r * .2, { w: 1.6 * wf });
      if (!side) { line(x - sw * .42, shY + 3, x - r * 1.2, shY + h * .045, { w: 2 * wf }); line(x + sw * .42, shY + 3, x + r * 1.2, shY + h * .045, { w: 2 * wf }); }
    }
    if (role === 'mother' && !side) { // dupatta band + dangling end
      const d = [[x - sw, shY + 2], [x + sw * .55, shY + 8], [x + hw * 1.05, hipY + 24], [x + hw * .5, hipY + 20], [x - sw * .7, shY + h * .1]]; hatch(d, { a: 60, g: 6, op: .8 }); poly(d, { w: 2 * wf });
      const e = [[x + hw * .5, hipY + 20], [x + hw * 1.1, hem - 4], [x + hw * .45, hem - 2]]; hatch(e, { a: 60, g: 6, op: .8 }); poly(e, { w: 2 * wf });
    }
    if (uni && h > 230) {
      line(x - hw, hipY - 6, x + hw, hipY - 6, { w: 3.4 * wf });
      if (!side) { rect(x - sw * .62, shY + h * .09, sw * .38, h * .045, { w: 1.6 * wf }); rect(x + sw * .24, shY + h * .09, sw * .38, h * .045, { w: 1.6 * wf }); line(x, shY, x, hipY - 6, { w: 1.4 * wf, o: .8 });
        line(x - sw * .28, shY, x, shY + h * .05, { w: 2 * wf }); line(x + sw * .28, shY, x, shY + h * .05, { w: 2 * wf }); }
      const ins = { mishra: 2, aditi: 1, khan: 3, ravi: 0 }[role] || 0;
      for (let i = 0; i < ins; i++) { const sx = x + sw * (.55 - i * .2), sy = shY + 8; line(sx - 5 * wf, sy, sx + 5 * wf, sy, { w: 2 }); line(sx, sy - 5 * wf, sx, sy + 5 * wf, { w: 2 }); }
    }
    if (role === 'seller' && !side) { const sc = [[x - sw * .5, shY - 2], [x + sw * .5, shY - 2], [x + sw * .3, shY + h * .06], [x - sw * .3, shY + h * .06]]; hatch(sc, { a: 0, g: 5, op: .9 }); hatch(sc, { a: 90, g: 5, op: .6 }); poly(sc, { w: 1.8 * wf }); }
    if (role === 'father' || role === 'uncle') { line(x, shY, x - 7 * wf, shY + h * .04, { w: 1.8 }); line(x, shY, x + 7 * wf, shY + h * .04, { w: 1.8 }); line(x, shY + h * .04, x, hem, { w: 1.2, o: .7 }); }
    if (h > 260) { const m = mid(shY, hipY); line(x - hw * .5, m, x - hw * .1, m + h * .03, { w: 1.2, o: .55, c: PEN, j: .4 }); line(x + hw * .2, hipY - h * .08, x + hw * .55, hipY - h * .05, { w: 1.2, o: .55, c: PEN, j: .4 }); }
  }
  function head(o) {
    const { x, y, r, dir, mood, role, silh } = o, side = dir === 'l' || dir === 'r', sgn = dir === 'l' ? -1 : 1, rx = r * (side ? .88 : .82), ry = r, w = 2.4 * o.lwf, w2 = 1.7 * o.lwf, cap = (role === 'ravi' || role === 'mishra' || role === 'cst' || role === 'khan' || o.extra.includes('cap'));
    const hp = [[x - rx, y - ry * .15], [x - rx * .96, y + ry * .4], [x - rx * .6, y + ry * .88], [x, y + ry * 1.04], [x + rx * .6, y + ry * .88], [x + rx * .96, y + ry * .4], [x + rx, y - ry * .15], [x + rx * .82, y - ry * .8], [x, y - ry * 1.02], [x - rx * .82, y - ry * .8]];
    if (silh) { FILL(crv(hp, true), DARK, .95); P(crv(hp.concat([hp[0]]), false), S({ w, c: DARK })); if (cap) capDraw(x, y, rx, ry, dir, true, role, w); return; }
    FILL(crv(hp, true), PAPER, 1); P(crv(hp.concat([hp[0], hp[1]]), false), S({ w }));
    if (dir !== 'b') hatch([[x + rx * .4, y + ry * .1], [x + rx * .96, y + ry * .1], [x + rx * .6, y + ry * .9], [x + rx * .2, y + ry * .95]], { a: 70, g: 4, w: 1, op: .35 });
    if (!side) { ell(x - rx * 1.02, y + ry * .15, rx * .14, ry * .24, { w: w2 }); ell(x + rx * 1.02, y + ry * .15, rx * .14, ry * .24, { w: w2 }); }
    if (cap) capDraw(x, y, rx, ry, dir, false, role, w);
    else {
      const long = role === 'mother' || role === 'girl' || role === 'aditi', gg = role === 'dhruv' ? 3.4 : 4.4;
      const hr0 = [[x - rx * 1.02, y + (long ? ry * .45 : ry * .05)], [x - rx * .96, y - ry * .55], [x - rx * .5, y - ry * 1.0], [x, y - ry * 1.12], [x + rx * .5, y - ry * 1.0], [x + rx * .96, y - ry * .55], [x + rx * 1.02, y + (long ? ry * .45 : ry * .05)]];
      const fr = dir === 'b' ? [[x + rx * .8, y + ry * .6], [x - rx * .8, y + ry * .6]] : [[x + rx * .85, y - ry * .35], [x + rx * .3, y - ry * .5], [x - rx * .3, y - ry * .38], [x - rx * .85, y - ry * .3]];
      hatch(hr0.concat(fr), { a: 68, g: gg, c: INK, w: 1.2 * o.lwf, op: .9 }); P(crv(hr0, false), S({ w })); P(crv(fr, false), S({ w: w2 }));
      if (role === 'aditi') { if (dir === 'f' || dir === 'b') { ell(x, y - ry * 1.35, rx * .5, rx * .42, { w }); hatch(ellPts(x, y - ry * 1.35, rx * .5, rx * .42, 8, 0), { a: 40, g: 3.5, c: INK, op: .9 }); } else { ell(x - sgn * rx * 1.0, y - ry * .35, rx * .5, rx * .5, { w }); } }
    }
    if (dir === 'b') return;
    const er = Math.max(1.8, r * .085), ey = y + ry * .02, ex = side ? sgn * rx * .42 : rx * .43, bs = mood === 'w' ? 1 : (mood === 'g' || mood === 'a' ? -1 : 0), bw = 2.2 * o.lwf;
    const eye = (px, sd) => { P(crv([[px - er * 1.9, ey + er * .2], [px, ey - er * 1.15], [px + er * 1.9, ey + er * .2]], false), S({ w: bw })); P(crv([[px - er * 1.7, ey + er * .3], [px, ey + er * 1.1], [px + er * 1.7, ey + er * .3]], false), S({ w: bw * .5, o: .7 })); FILL(crv(ellPts(px + (sd || 0) * er * .3, ey, er * .62, er * .62, 6, 0).slice(0, -1), true), INK, 1); };
    if (side) { eye(x + ex, sgn); line(x + ex - er * 2.2, ey - er * 2.7 + bs * er * .6, x + ex + er * 2, ey - er * 2.6 - bs * er * .6, { w: bw * 1.1 });
      poly([[x + sgn * rx * .95, y - ry * .02], [x + sgn * rx * 1.22, y + ry * .34], [x + sgn * rx * .88, y + ry * .4]], { w: w2 }, true);
      mouth(x + sgn * rx * .5, y + ry * .64, r * .3, mood, true, w2); ell(x - sgn * rx * .22, y + ry * .12, rx * .15, ry * .24, { w: w2 });
    } else { eye(x - ex, 0); eye(x + ex, 0);
      line(x - ex - er * 2.4, ey - er * 2.9 + bs * er * 1.1, x - ex + er * 2.2, ey - er * 2.8 - bs * er * 1.1, { w: bw * 1.15 }); line(x + ex - er * 2.2, ey - er * 2.8 - bs * er * 1.1, x + ex + er * 2.4, ey - er * 2.9 + bs * er * 1.1, { w: bw * 1.15 });
      P(crv([[x + er * .4, ey + er * 1.5], [x - er * .6, ey + er * 4.2], [x + er * .9, ey + er * 4.5]], false), S({ w: w2 }));
      mouth(x, y + ry * .62, r * .34, mood, false, w2);
    }
    if (o.extra.includes('mous')) { const my = y + ry * .5; hatch([[x - rx * .6, my - 2], [x + rx * .6, my - 2], [x + rx * .5, my + r * .13], [x - rx * .5, my + r * .13]], { a: 0, g: 2.2, c: INK, op: 1, w: 1.8 }); }
    if (o.extra.includes('sweat')) for (let i = 0; i < 3; i++) { const sx = x + rx * (.78 + i * .14), sy = y - ry * (.7 - i * .5); poly([[sx, sy - r * .13], [sx - r * .07, sy + r * .03], [sx + r * .07, sy + r * .03]], { w: w2 }); }
  }
  function mouth(x, y, w, mood, side, lw) {
    const o = { w: lw || 2 };
    if (mood === 's') P(crv([[x - w, y - w * .2], [x, y + w * .45], [x + w, y - w * .2]], false), S(o));
    else if (mood === 'w') P(crv([[x - w * .8, y + w * .3], [x, y - w * .15], [x + w * .8, y + w * .3]], false), S(o));
    else if (mood === 'o') { FILL(crv(ellPts(x, y + w * .2, w * .55, w * .8, 8, 0).slice(0, -1), true), INK, .85); ell(x, y + w * .2, w * .55, w * .8, o); }
    else if (mood === 'a') { ell(x, y + w * .1, w * .75, w * .5, o); line(x - w * .7, y + w * .1, x + w * .7, y + w * .1, { w: 1.2 }); }
    else line(x - w * .7, y, x + w * .7, y + (side ? 0 : 1), o);
  }
  function capDraw(x, y, rx, ry, dir, silh, role, w) {
    const side = dir === 'l' || dir === 'r', sgn = dir === 'l' ? -1 : 1, top = [[x - rx * 1.06, y - ry * .18], [x - rx * 1.02, y - ry * .8], [x - rx * .4, y - ry * 1.28], [x + rx * .4, y - ry * 1.28], [x + rx * 1.02, y - ry * .8], [x + rx * 1.06, y - ry * .18]];
    const col = silh ? DARK : (role === 'ravi' || role === 'mishra' || role === 'cst' || role === 'khan' ? KHAKI : '#4A4540');
    solid(top); wash(top, col, silh ? 1 : .95); P(crv(top.concat([top[0]]), false), S({ w }));
    const b = side ? [[x + sgn * rx * .5, y - ry * .25], [x + sgn * rx * 1.55, y - ry * .18]] : [[x - rx * 1.15, y - ry * .2], [x + rx * 1.15, y - ry * .2]];
    line(b[0][0], b[0][1], b[1][0], b[1][1], { w: w * 1.5 });
    if (role && !side && !silh) { ell(x, y - ry * .7, rx * .13, rx * .13, { w: 1.8 }); hatch(top, { a: 30, g: 6, w: 1, op: .35 }); }
  }

  // ---- props ---------------------------------------------------------------------------
  function balloon(x, y, r, color, o) {
    o = o || {}; const red = color === 'red', col = red ? RED : (color || '#D8D4CA');
    G(); if (o.string !== false) P(crv([[x, y + r * 1.15], [x + J(6) + (o.sway || 0) * .5, y + r * 2.2], [x + (o.sway || 0), y + r * 3.4]], false), S({ c: PEN, w: 1.5 }));
    FILL(crv(ellPts(x + 2, y + 1.5, r * .82, r, 12, 0).slice(0, -1), true), col, red ? .95 : .55);
    P(crv(ellPts(x, y, r * .82, r, 12, .08), false), S({ c: red ? INK : INK, w: 2.2 }));
    poly([[x - 4, y + r * 1.02], [x + 4, y + r * 1.02], [x, y + r * 1.15]], { w: 1.6 });
    if (r > 14) { P(crv([[x - r * .45, y - r * .3], [x - r * .5, y - r * .6], [x - r * .2, y - r * .8]], false), S({ c: PAPER, w: 3, o: .9 })); }
  }
  function bulbs(x1, y1, x2, y2, n, sag, glow) {
    G(); const pts = []; for (let i = 0; i <= 12; i++) { const t = i / 12; pts.push([x1 + (x2 - x1) * t, y1 + (y2 - y1) * t + Math.sin(t * Math.PI) * sag]); }
    P(crv(pts, false), S({ w: 1.6, o: .85 }));
    for (let i = 1; i < n; i++) { const t = i / n, bx = x1 + (x2 - x1) * t, by = y1 + (y2 - y1) * t + Math.sin(t * Math.PI) * sag;
      ell(bx, by + 6, 4, 5, { w: 1.6 }); if (glow) for (let k = 0; k < 6; k++) { const a = k * 1.05 + .3; line(bx + Math.cos(a) * 8, by + 6 + Math.sin(a) * 8, bx + Math.cos(a) * 14, by + 6 + Math.sin(a) * 14, { w: 1.2, o: .6, j: .3 }); } }
  }
  function stall(x, y, w, h, o) { // y = ground
    o = o || {}; G(); const top = y - h, cw = w * .1;
    solid(box(x, top + h * .35, w, h * .65)); rect(x, top + h * .35, w, h * .65, { w: 2.4 }); hatch(box(x + 4, top + h * .65, w - 8, h * .33), { a: 70, g: 8 });
    line(x + 6, top + h * .12, x + 6, y, { w: 2.4 }); line(x + w - 6, top + h * .12, x + w - 6, y, { w: 2.4 });
    const roof = [[x - 14, top + h * .14], [x + w + 14, top + h * .14], [x + w + 4, top], [x - 4, top]]; solid(roof);
    for (let i = 0; i < 8; i++) { const a = x - 14 + (w + 28) * i / 8, b = x - 14 + (w + 28) * (i + 1) / 8; if (i % 2) hatch([[a, top], [b, top], [b, top + h * .14], [a, top + h * .14]], { a: 70, g: 4, c: INK, op: .7 }); }
    poly(roof, { w: 2.4 }); for (let i = 0; i < 9; i++) { const a = x - 14 + (w + 28) * i / 8; P(crv([[a, top + h * .14], [a + (w + 28) / 16, top + h * .2], [a + (w + 28) / 8, top + h * .14]], false), S({ w: 1.8 })); }
    if (o.goods === 'balloon') for (let i = 0; i < 5; i++) { const bx = x + w * (.15 + i * .17); balloon(bx, top + h * .5, h * .07, i === 2 ? 'red' : '#D8D4CA'); }
    else if (o.goods === 'toy') for (let i = 0; i < 6; i++) { ell(x + w * (.1 + i * .15), top + h * .5, 9, 9, { w: 2 }); rect(x + w * (.1 + i * .15) - 7, top + h * .5 + 9, 14, 14, { w: 1.6 }); }
    else for (let i = 0; i < 6; i++) ell(x + w * (.12 + i * .15), top + h * .56, 11, 6, { w: 2 });
  }
  function wheel(cx, cy, r, o) {
    G(); o = o || {}; ell(cx, cy, r, r, { w: 3.2 }); ell(cx, cy, r * .86, r * .86, { w: 1.6 }); ell(cx, cy, r * .08, r * .08, { w: 2.4 });
    for (let i = 0; i < 12; i++) { const a = i * Math.PI / 6 + .13; line(cx, cy, cx + Math.cos(a) * r, cy + Math.sin(a) * r, { w: 1.8 }); const bx = cx + Math.cos(a) * r, by = cy + Math.sin(a) * r; if (!o.noCabins) { solid(box(bx - 14, by - 4, 28, 24)); rect(bx - 14, by - 4, 28, 24, { w: 2 }); } }
    line(cx, cy, cx - r * .7, cy + r * 1.35, { w: 3 }); line(cx, cy, cx + r * .7, cy + r * 1.35, { w: 3 });
  }
  function head3(x, y, r, o) { // blob head+shoulders for crowds
    o = o || {}; solid([[x - r * 1.5, y + r * 3], [x - r * 1.4, y + r * 1.1], [x - r * .5, y + r * .9], [x + r * .5, y + r * .9], [x + r * 1.4, y + r * 1.1], [x + r * 1.5, y + r * 3]]);
    ell(x, y, r * .85, r, { w: 2 }); P(crv([[x - r * 1.5, y + r * 3], [x - r * 1.4, y + r * 1.3], [x - r * .6, y + r * 1.0]], false), S({ w: 2 })); P(crv([[x + r * 1.5, y + r * 3], [x + r * 1.4, y + r * 1.3], [x + r * .6, y + r * 1.0]], false), S({ w: 2 }));
    hatch([[x - r * .85, y - r * .1], [x - r * .5, y - r * .9], [x + r * .5, y - r * .9], [x + r * .85, y - r * .1]], { a: 70, g: 4, c: INK, op: .85 });
    if (o.hat) ell(x, y + r * 2, r * .1, r * .1, { w: 1 });
  }
  function crowd(x0, x1, y, rows, r, o) {
    o = o || {}; for (let k = 0; k < rows; k++) { G(); const yy = y + k * r * 1.7, rr = r * (1 + k * .22), n = Math.round((x1 - x0) / (rr * 2.2));
      for (let i = 0; i < n; i++) { const x = x0 + (i + .5 + J(.3) + (k % 2) * .5) * (x1 - x0) / n; head3(x, yy + J(rr * .3), rr * (.9 + rnd() * .2)); } }
  }
  function ground(y, x0, x1, o) { o = o || {}; G(); line(x0 == null ? 0 : x0, y, x1 == null ? 1800 : x1, y, { w: 2.4 }); const g = o.g || 26; for (let x = (x0 || 0) + 20; x < (x1 || 1800); x += g * (.7 + rnd() * .8)) line(x, y + 6 + rnd() * 6, x - 18, y + 22 + rnd() * 12, { w: 1.1, o: .5, c: PEN, j: .3 }); }
  function night(x, y, w, h, dens) { G(); hatch(box(x, y, w, h), { a: 55, g: dens || 8, w: 1.3, op: .5 }); hatch(box(x, y, w, h * .5), { a: -50, g: (dens || 8) * 1.4, w: 1.1, op: .4 }); }
  function van(x, y, sc, dir) { // x,y = front-bottom-left; white van side view
    G(); const d = dir === 'l' ? -1 : 1, m = (px, py) => [x + d * px * sc, y - py * sc];
    const body = [m(0, 40), m(0, 120), m(70, 160), m(200, 160), m(330, 160), m(330, 40)].map(p => p); solid(body); poly(body, { w: 3 });
    poly([m(10, 122), m(70, 152), m(125, 152), m(125, 122)], { w: 2 }); line(...m(125, 50).concat(m(125, 152)), { w: 2 }); line(...m(0, 70).concat(m(330, 70)), { w: 1.6, o: .7 });
    [m(70, 36), m(250, 36)].forEach(p => { disc(p[0], p[1], 34 * sc, 34 * sc, '#4A4540', .9); ell(p[0], p[1], 14 * sc, 14 * sc, { w: 2 }); });
  }
  function jeep(x, y, sc, dir) {
    G(); const d = dir === 'l' ? -1 : 1, m = (px, py) => [x + d * px * sc, y - py * sc];
    const body = [m(0, 40), m(0, 90), m(40, 105), m(80, 150), m(210, 150), m(260, 105), m(280, 100), m(280, 40)]; solid(body); wash(body, '#CBD0D6', .5); poly(body, { w: 3 });
    poly([m(90, 108), m(95, 144), m(150, 144), m(150, 108)], { w: 2 }); poly([m(158, 108), m(158, 144), m(205, 144), m(215, 108)], { w: 2 });
    [m(60, 36), m(225, 36)].forEach(p => { disc(p[0], p[1], 30 * sc, 30 * sc, '#4A4540', .9); ell(p[0], p[1], 12 * sc, 12 * sc, { w: 2 }); });
    ell(...m(140, 156).concat([22 * sc, 8 * sc]), { w: 2.4 });
  }
  function tin(x, y, w, h) { G(); solid(box(x, y, w, h)); rect(x, y, w, h, { w: 2.6 }); for (let i = x + 18; i < x + w; i += 26) line(i, y + 3, i + J(2), y + h - 3, { w: 1.2, c: PEN, o: .8, j: .5 }); }
  function tube(x, y, w) { G(); line(x, y, x + w, y, { w: 5 }); line(x + 6, y - 14, x + 6, y, { w: 1.6 }); line(x + w - 6, y - 14, x + w - 6, y, { w: 1.6 }); for (let i = 0; i < 9; i++) { const a = 1.1 + i * .22; line(x + w / 2 + Math.cos(a) * 30, y + Math.sin(a) * 14, x + w / 2 + Math.cos(a) * 120, y + Math.sin(a) * 70, { w: 1, c: PEN, o: .35, j: .3 }); } }
  function desk(x, y, w, h) { G(); const t = [[x, y], [x + w, y], [x + w - 20, y + 26], [x + 20, y + 26]]; solid(t); poly(t, { w: 2.8 }); solid(box(x + 24, y + 26, w - 48, h)); rect(x + 24, y + 26, w - 48, h, { w: 2.4 }); hatch(box(x + 28, y + 30, w - 56, h - 8), { a: 70, g: 9 }); }
  function phone(x, y, w, h) { G(); solid(box(x, y, w, h)); rect(x, y, w, h, { w: 3.4 }); rect(x + 12, y + 18, w - 24, h - 40, { w: 2 }); ell(x + w / 2, y + h - 12, 5, 5, { w: 1.6 }); }
  function radio(x, y, s) { G(); solid(box(x, y, 40 * s, 66 * s)); rect(x, y, 40 * s, 66 * s, { w: 2.6 }); line(x + 30 * s, y, x + 36 * s, y - 40 * s, { w: 3 }); for (let i = 0; i < 4; i++) line(x + 6 * s, y + (12 + i * 6) * s, x + 30 * s, y + (12 + i * 6) * s, { w: 1.4 }); rect(x + 6 * s, y + 42 * s, 28 * s, 14 * s, { w: 1.6 }); }
  function bench(x, y, w) { G(); solid(box(x, y, w, 72)); rect(x, y, w, 16, { w: 2.6 }); hatch(box(x + 2, y + 2, w - 4, 12), { a: 0, g: 5, op: .6 }); line(x + 14, y + 16, x + 10, y + 70, { w: 2.6 }); line(x + w - 14, y + 16, x + w - 10, y + 70, { w: 2.6 }); line(x + 6, y - 60, x + 6, y, { w: 2.6 }); line(x + 6, y - 58, x + w, y - 58, { w: 2.2 }); }
  function pin(x, y, c) { G(); ell(x, y - 10, 8, 8, { w: 2.4 }); FILL(crv(ellPts(x, y - 10, 6, 6, 8, 0).slice(0, -1), true), c || INK, .85); line(x, y - 2, x, y + 14, { w: 2 }); }
  function star(x, y, r, o) { const p = []; for (let i = 0; i < 10; i++) { const a = -Math.PI / 2 + i * Math.PI / 5, rr = i % 2 ? r * .42 : r; p.push([x + Math.cos(a) * rr, y + Math.sin(a) * rr]); } if (o && o.fill) wash(p, o.fill, 1); poly(p, o); }
  function arrow(x1, y1, x2, y2, o) { line(x1, y1, x2, y2, o); const a = Math.atan2(y2 - y1, x2 - x1); line(x2, y2, x2 - Math.cos(a - .5) * 16, y2 - Math.sin(a - .5) * 16, o); line(x2, y2, x2 - Math.cos(a + .5) * 16, y2 - Math.sin(a + .5) * 16, o); }
  function meter(x, y, w, vals, o) {
    o = o || {}; const lab = ['RESPONSE', 'DECISION', 'INVESTIGATION', 'COMMAND', 'REACH'], key = ['R', 'D', 'I', 'C', 'Re'], rh = o.rh || 62, labW = w * .5, bw = (w - labW) / 5 - 6;
    G(); if (o.title) TEXT(x, y - 22, o.title, { size: 30, font: 'Oswald', w: 600 });
    for (let i = 0; i < 5; i++) {
      G(); const yy = y + i * rh; TEXT(x, yy + rh * .62, lab[i], { size: o.fs || 28, font: 'Oswald', w: 500 });
      for (let k = 0; k < 5; k++) { const bx = x + labW + k * (bw + 6); rect(bx, yy + 8, bw, rh - 22, { w: 2.2 }); if (vals && k < vals[i]) { wash(box(bx + 2, yy + 10, bw - 4, rh - 26), INK, .85); } }
    }
  }
  function mapInset(x, y, w, h, label) { G(); solid(box(x, y, w, h)); rect(x, y, w, h, { w: 3 }); hatch(box(x + 6, y + 6, w - 12, h - 12), { a: 45, g: 12, op: .35 }); for (let i = 0; i < 4; i++) rect(x + 20 + i * (w - 50) / 4, y + 26 + (i % 2) * 20, 28, 20, { w: 1.6 }); ell(x + w * .7, y + h * .55, 26, 26, { w: 2 }); pin(x + w * .38, y + h * .62, RED); TEXT(x + 10, y + h + 34, label, { size: 24, font: 'Oswald', w: 500 }); }
  function lower3(x, y, rank, role) { G(); const str = '[RANK: ' + rank + '  |  ROLE: ' + role + ']', w = 50 + str.length * 14.5; solid(box(x, y, w, 60)); rect(x, y, w, 60, { w: 3 }); line(x, y + 60, x + w + 8, y + 60, { w: 5 }); TEXT(x + 16, y + 41, str, { size: 28, font: 'Oswald', w: 500 }); }
  function sup(x, y, str, o) { G(); o = o || {}; TEXT(x, y, str, { size: o.size || 40, font: 'Oswald', w: 600, fill: o.fill || INK, anchor: o.anchor }); }

  function end() {
    let out = '';
    subs.forEach((sb, si) => {
      out += `<g class="sub" data-i="${si}">`;
      sb.forEach(g => {
        if (!g.items.length) return; out += `<g class="gr"${g.n ? ` data-n="${g.n}"` : ''}>`;
        g.items.forEach(it => {
          if (it.text != null) { const o = it.o; out += `<text class="f" x="${f(it.x)}" y="${f(it.y)}" font-family="${o.font === 'Mono' ? 'Space Mono' : (o.font || 'Oswald')}" font-size="${o.size || 28}" font-weight="${o.w || 500}" fill="${o.fill || INK}" text-anchor="${o.anchor || 'start'}"${o.rot ? ` transform="rotate(${o.rot} ${f(it.x)} ${f(it.y)})"` : ''}>${it.text}</text>`; }
          else if (it.fill) out += `<path class="f" d="${it.d}" fill="${it.fill}" opacity="${it.op}"/>`;
          else out += `<path class="d" d="${it.d}" pathLength="1" stroke="${it.st.c}" stroke-width="${it.st.w}" stroke-opacity="${it.st.o}" stroke-dasharray="1 2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`;
        });
        out += '</g>';
      });
      out += '</g>';
    });
    return out;
  }
  return { begin, nextSub, end, G, tag, tlimb, ellR, rot, lerp, line, ell, disc, poly, rect, crv, hatch, wash, solid, text, box, fig, balloon, bulbs, stall, wheel, crowd, head3, ground, night, van, jeep, tin, tube, desk, phone, radio, bench, pin, star, arrow, meter, mapInset, lower3, sup, rnd, J, ellPts, FILL, P, INK, PEN, BLUE, KHAKI, RED, GOLD, PAPER, DARK };
})();

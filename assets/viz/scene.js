/* Mesh Town explainer: builds the scene SVG. Browser: MeshScene.build(layout) returns an SVGElement.
   Node (no document): returns the SVG markup as a string. layout: 'h' (wide) or 'v' (narrow). */
(function (root) {
  'use strict';
  var NS = 'http://www.w3.org/2000/svg';
  var NAMES = ['nas', 'laptop', 'pc'];
  var PLACES = ['Home', 'Café', 'Office'];
  var PCLS = ['p-home', 'p-cafe', 'p-office'];

  function el(n, o, c) {
    var s = '<' + n, k;
    for (k in o) { if (o[k] !== undefined) { s += ' ' + k + '="' + o[k] + '"'; } }
    return s + (c === undefined ? '/>' : '>' + c + '</' + n + '>');
  }
  function g(cls, c) { return el('g', { 'class': cls }, c.join('')); }
  function rect(x, y, w, h, rx, cls) { return el('rect', { 'class': cls, x: x, y: y, width: w, height: h, rx: rx }); }
  function line(x1, y1, x2, y2, cls) { return el('line', { 'class': cls, x1: x1, y1: y1, x2: x2, y2: y2 }); }
  function path(d, cls) { return el('path', { 'class': cls, d: d }); }
  function text(x, y, s, size, cls) { return el('text', { 'class': cls, x: x, y: y, 'font-size': size }, s); }
  function pkt(cls, d) { return el('circle', { 'class': 'v-pkt ' + cls, r: 4.5, style: "offset-path:path('" + d + "')" }); }
  function rec(d) { return el('circle', { 'class': 'v-rec', r: 5, style: "offset-path:path('" + d + "')" }); }
  function lock(cx, cy, cls) {
    return g('v-lock ' + cls, [
      el('circle', { cx: cx, cy: cy, r: 9 }),
      rect(cx - 4, cy - 1, 8, 6, 1),
      path('M' + (cx - 2.5) + ' ' + (cy - 1) + 'v-2.5a2.5 2.5 0 0 1 5 0v2.5')
    ]);
  }

  /* One place: frame, name, router with two antennas, NAT label. a = geometry of the layout. */
  function frame(i, a) { return rect(a.px[i], a.py[i], a.pw, a.ph, a.prx, 'v-place ' + PCLS[i]); }

  /* Labels go above the directory lines. */
  function place(i, a) {
    var x = a.px[i], y = a.py[i], r = a.rt, rx = x + r[0], ry = y + r[1];
    var out = [text(x + a.pn[0], y + a.pn[1], PLACES[i], a.pn[2], 'v-place-name' + (i === 1 ? ' n-cafe' : ''))];
    if (i === 1) { out.push(text(x + a.pn[0], y + a.pn[1], 'Mobile network', a.pn[2], 'v-place-name v-place-name-alt')); }
    out.push(g('v-router', [rect(rx, ry, r[2], r[3], 3), line(rx + r[2] / 4, ry, rx + r[2] / 4, ry - 8),
      line(rx + r[2] * 3 / 4, ry, rx + r[2] * 3 / 4, ry - 8)]));
    out.push(text(x + a.nat[0], y + a.nat[1], 'NAT', 11, 'v-nat' + (i === 2 ? ' o-nat' : '')));
    return out.join('');
  }

  function node(i, a) {
    var n = a.nd, x = a.px[i], y = a.ny(i);
    return g('v-node n-' + NAMES[i], [rect(x + n[0], y, n[1], n[2], 8),
      text(x + n[3], y + n[4], NAMES[i], n[5], 'm')]);
  }

  function frames(a) { return [frame(0, a), frame(1, a), frame(2, a)]; }
  function labels(a) { return [place(0, a), place(1, a), place(2, a)].join(''); }

  function wide() {
    var a = { px: [40, 290, 540], py: [150, 150, 150], pw: 220, ph: 240, prx: 12, pn: [16, 28, 15],
      rt: [160, 14, 40, 12], nat: [180, 44], nd: [55, 110, 44, 110, 27, 15], ny: function () { return 278; } };
    var d = ['M150 278L330 86', 'M400 278L400 88', 'M650 278L470 86'], s = frames(a), i;
    s.push(el('ellipse', { cx: 400, cy: 56, rx: 118, ry: 32, 'class': 'v-cloud-bg' }));
    s[s.length - 1] = g('v-cloud', [s[s.length - 1], text(400, 61, 'public directory (DHT)', 14, 'mu')]);
    for (i = 0; i < 3; i++) { s.push(path(d[i], 'v-dht')); }
    s.push(labels(a));
    for (i = 0; i < 3; i++) { s.push(node(i, a)); }
    s.push(g('v-panel', [line(150, 136, 150, 278), rect(50, 104, 200, 32, 8), text(150, 125, 'NAS · web panel', 13, 'as b')]));
    s.push(g('v-addr', [line(400, 136, 400, 278), rect(300, 104, 200, 32, 16), text(400, 125, 'http://nas.meshtown', 13, 'm')]));
    s.push(g('v-proxy', [line(400, 136, 400, 278), rect(300, 104, 200, 32, 16), text(400, 125, 'proxy 127.0.0.1:1080', 13, 'm')]));
    s.push(path('M205 300L345 300', 'v-link l-nl'), path('M455 300L595 300', 'v-link l-lo'),
      path('M150 322C150 430 650 430 650 322', 'v-link l-no'));
    s.push(lock(275, 300, 'lk-nl'), lock(525, 300, 'lk-lo'), lock(400, 403, 'lk-no'));
    s.push(path('M650 278C650 190 706 170 706 82', 'v-exit'));
    s.push(g('v-service', [rect(632, 28, 148, 52, 10), text(706, 50, 'a service', 13, 'b'),
      text(706, 68, 'accepts the office IP only', 11, 'mu')]));
    s.push(g('v-badge-exit', [rect(600, 244, 100, 24, 12), text(650, 260, 'exit', 12, 'as b')]));
    s.push(g('v-badge-pub', [rect(600, 244, 100, 24, 12), text(650, 260, 'public address', 12, 'as b')]));
    s.push(g('v-net', [rect(24, 22, 118, 30, 15), text(83, 42, 'home-lab', 14, 'as b m')]));
    for (i = 0; i < 3; i++) { s.push(rec(d[i])); }
    s.push(pkt('k-req', 'M345 300L205 300'), pkt('k-res', 'M205 300L345 300'),
      pkt('k-exit', 'M455 300L650 300C650 190 706 170 706 82'),
      pkt('k-relay', 'M455 300L650 300L650 322C650 430 150 430 150 322'));
    return { vb: '0 0 800 450', body: s.join('') };
  }

  function narrow() {
    var a = { px: [28, 28, 28], py: [84, 212, 340], pw: 316, ph: 96, prx: 10, pn: [14, 24, 14],
      rt: [266, 12, 36, 11], nat: [284, 40], nd: [24, 100, 38, 74, 24, 14],
      ny: function (i) { return [126, 254, 382][i]; } };
    var d = ['M102 126L218 66', 'M102 254L218 66', 'M102 382L218 66'], s = frames(a), i, y, slot;
    s.push(g('v-cloud', [el('ellipse', { cx: 218, cy: 40, rx: 100, ry: 26 }), text(218, 44, 'public directory (DHT)', 13, 'mu')]));
    for (i = 0; i < 3; i++) { s.push(path(d[i], 'v-dht')); }
    s.push(labels(a));
    for (i = 0; i < 3; i++) { s.push(node(i, a)); }
    slot = function (cls, label, size, cap, y0) {
      return g(cls, [line(152, y0 + 61, 168, y0 + 61), rect(168, y0 + 45, 160, 30, cap), text(248, y0 + 64, label, size, cap === 8 ? 'as b' : 'm')]);
    };
    s.push(slot('v-panel', 'NAS · web panel', 13, 8, 84));
    s.push(slot('v-addr', 'http://nas.meshtown', 12, 15, 212));
    s.push(slot('v-proxy', 'proxy 127.0.0.1:1080', 12, 15, 212));
    s.push(path('M102 164L102 254', 'v-link l-nl'), path('M102 292L102 382', 'v-link l-lo'),
      path('M52 145C8 145 8 401 52 401', 'v-link l-no'));
    s.push(lock(102, 209, 'lk-nl'), lock(102, 337, 'lk-lo'), lock(19, 273, 'lk-no'));
    s.push(path('M102 420L102 462Q102 470 110 470L168 470', 'v-exit'));
    s.push(g('v-service', [rect(168, 452, 160, 36, 8), text(248, 466, 'a service', 12, 'b'),
      text(248, 481, 'accepts the office IP only', 10.5, 'mu')]));
    y = 340;
    s.push(g('v-badge-exit', [rect(168, y + 48, 120, 24, 12), text(228, y + 64, 'exit', 12, 'as b')]));
    s.push(g('v-badge-pub', [rect(168, y + 48, 120, 24, 12), text(228, y + 64, 'public address', 12, 'as b')]));
    s.push(g('v-net', [rect(12, 14, 100, 26, 13), text(62, 31, 'home-lab', 13, 'as b m')]));
    for (i = 0; i < 3; i++) { s.push(rec(d[i])); }
    s.push(pkt('k-req', 'M102 254L102 164'), pkt('k-res', 'M102 164L102 254'),
      pkt('k-exit', 'M102 292L102 382L102 420L102 462Q102 470 110 470L168 470'),
      pkt('k-relay', 'M102 292L102 382L52 401C8 401 8 145 52 145'));
    return { vb: '0 0 360 500', body: s.join('') };
  }

  /* Palette for standalone SVG files, which cannot see the page CSS. Same values as the site theme. */
  function staticStyle() {
    return '.v-svg{--bg:#fff;--surface:#f4f6f8;--surface-2:#e8ecf0;--border:#d6dce2;--fg:#171b1f;--muted:#4d565f;' +
      '--accent:#0b6e63;--accent-strong:#085a50;--accent-soft:#dcf1ec;--line-muted:#7c868f;' +
      '--font-sans:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;' +
      '--font-mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}' +
      '@media(prefers-color-scheme:dark){.v-svg{--bg:#0e1216;--surface:#161c22;--surface-2:#1e262d;--border:#2b353e;' +
      '--fg:#e7eaed;--muted:#a7b0b9;--accent:#58d0bc;--accent-strong:#86e2d3;--accent-soft:#113b35;--line-muted:#6f7a84}}';
  }

  /* opts: cls (extra classes), style (inline style), css (embedded stylesheet). */
  function build(layout, opts) {
    opts = opts || {};
    var L = layout === 'v' ? narrow() : wide();
    var cls = 'v-svg layout-' + layout + (opts.cls ? ' ' + opts.cls : '');
    var markup = '<svg xmlns="' + NS + '" viewBox="' + L.vb + '" class="' + cls + '"' +
      (opts.style ? ' style="' + opts.style + '"' : '') + (opts.css ? '' : ' aria-hidden="true"') + '>' +
      (opts.css ? '<style>' + opts.css + '</style>' : '') + L.body + '</svg>';
    if (typeof document === 'undefined') { return markup; }
    return document.importNode(new DOMParser().parseFromString(markup, 'image/svg+xml').documentElement, true);
  }

  root.MeshScene = { build: build, staticStyle: staticStyle };
  if (typeof module !== 'undefined' && module.exports) { module.exports = root.MeshScene; }
})(typeof window !== 'undefined' ? window : this);

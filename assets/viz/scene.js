/* Mesh Town explainer: builds the SVG scene and per-frame state classes. */
(function () {
  'use strict';
  var NS = 'http://www.w3.org/2000/svg';
  var FRAME_CLASSES = ['', 'k', 'k up', 'k direct', 'k direct lock dim', 'k direct lock dim addr',
    'k direct lock dim hop', 'k direct lock bad'];
  var CAFE_NAME = ['Café', 'Café', 'Café', 'Café', 'Café', 'Café', 'Hotel', 'Mobile network'];
  var PLACES = [
    { id: 'home', name: 'Home', x: 30, node: 'nas' },
    { id: 'cafe', name: 'Café', x: 290, node: 'laptop' },
    { id: 'office', name: 'Office', x: 550, node: 'pc' }
  ];

  function el(name, attrs, parent, cls) {
    var e = document.createElementNS(NS, name);
    Object.keys(attrs || {}).forEach(function (k) { e.setAttribute(k, attrs[k]); });
    if (cls) { e.setAttribute('class', cls); }
    if (parent) { parent.appendChild(e); }
    return e;
  }

  function text(parent, x, y, str, cls, anchor) {
    var t = el('text', { x: x, y: y, 'text-anchor': anchor || 'middle' }, parent, cls);
    t.textContent = str;
    return t;
  }

  function lock(parent, x, y, cls) {
    var g = el('g', { transform: 'translate(' + x + ' ' + y + ')' }, parent, 'v-lock ' + cls);
    el('circle', { r: 13 }, g, 'v-lock-bg');
    el('path', { d: 'M-4 -1V-4a4 4 0 0 1 8 0V-1' }, g, 'v-lock-arc');
    el('rect', { x: -6, y: -1, width: 12, height: 9, rx: 2 }, g, 'v-lock-body');
    return g;
  }

  function cross(parent, x, y, cls) {
    var g = el('g', { transform: 'translate(' + x + ' ' + y + ')' }, parent, 'v-cross ' + cls);
    el('circle', { r: 13 }, g, 'v-cross-bg');
    el('path', { d: 'M-6 -6L6 6M6 -6L-6 6' }, g, 'v-cross-x');
    return g;
  }

  function place(svg, p) {
    var g = el('g', { 'data-place': p.id }, svg, 'v-place');
    var cx = p.x + 110;
    el('rect', { x: p.x, y: 230, width: 220, height: 210, rx: 12 }, g, 'v-place-bg');
    p.label = text(g, p.x + 14, 254, p.name, 'v-place-name', 'start');
    el('rect', { x: p.x + 152, y: 240, width: 44, height: 16, rx: 4 }, g, 'v-router');
    el('path', { d: 'M' + (p.x + 164) + ' 240v-6M' + (p.x + 184) + ' 240v-6' }, g, 'v-antenna');
    text(g, p.x + 174, 272, 'NAT', 'v-nat');
    var key = el('g', { 'class': 'v-key' }, g);
    el('rect', { x: cx - 48, y: 288, width: 96, height: 20, rx: 10 }, key, 'v-key-bg');
    text(key, cx, 302, 'home-lab', 'v-key-text');
    var node = el('g', { 'data-node': p.node }, g, 'v-node');
    el('rect', { x: cx - 50, y: 322, width: 100, height: 40, rx: 8 }, node, 'v-node-bg');
    text(node, cx, 347, p.node, 'v-node-text');
  }

  function dhtLinks(svg) {
    [[0, 'M202 234Q250 150 340 98'], [0, 'M472 234Q440 150 410 100'],
      [0, 'M722 234Q640 130 460 92']].forEach(function (d) {
      el('path', { d: d[1] }, svg, 'v-dht-link');
    });
  }

  function links(svg) {
    var defs = [['nl', 'M190 342H350', 270, 342], ['lo', 'M450 342H610', 530, 342],
      ['no', 'M140 364Q400 450 660 364', 400, 407]];
    defs.forEach(function (d) {
      var g = el('g', {}, svg, 'v-link v-link-' + d[0]);
      el('path', { d: d[1] }, g, 'v-dash');
      el('path', { d: d[1] }, g, 'v-solid');
      lock(g, d[2], d[3], 'v-lock-' + d[0]);
      if (d[0] !== 'no') { cross(g, d[2], d[3], 'v-cross-' + d[0]); }
    });
  }

  function cloud(svg) {
    var g = el('g', {}, svg, 'v-cloud');
    el('ellipse', { cx: 400, cy: 66, rx: 120, ry: 34 }, g, 'v-cloud-bg');
    text(g, 400, 71, 'public DHT', 'v-cloud-text');
    lock(svg, 540, 70, 'v-dht-lock');
  }

  function extras(svg) {
    var bar = el('g', {}, svg, 'v-addr');
    el('rect', { x: 296, y: 186, width: 208, height: 30, rx: 15 }, bar, 'v-addr-bg');
    text(bar, 400, 206, 'http://nas.meshtown', 'v-addr-text');
    var panel = el('g', {}, svg, 'v-panel');
    el('rect', { x: 50, y: 186, width: 180, height: 30, rx: 6 }, panel, 'v-panel-bg');
    text(panel, 140, 206, 'NAS · web panel', 'v-panel-text');
    el('circle', { cx: 196, cy: 342, r: 6 }, svg, 'v-packet');
  }

  function build(stage, alt) {
    var svg = el('svg', { viewBox: '0 0 800 460', role: 'img', 'aria-labelledby': 'viz-title',
      'data-frame': '1' }, null, 'viz-svg');
    var title = el('title', { id: 'viz-title' }, svg);
    title.textContent = alt || 'How Mesh Town connects your devices';
    cloud(svg);
    dhtLinks(svg);
    PLACES.forEach(function (p) { place(svg, p); });
    links(svg);
    extras(svg);
    svg._cafe = PLACES[1].label;
    setFrame(svg, 1);
    if (stage) { stage.appendChild(svg); }
    return svg;
  }

  function setFrame(svg, n) {
    var i = Math.max(1, Math.min(8, n)) - 1;
    svg.setAttribute('data-frame', String(i + 1));
    svg.setAttribute('class', ('viz-svg ' + FRAME_CLASSES[i === 7 ? 7 : Math.min(i, 6)]).trim() + ' f' + (i + 1));
    if (svg._cafe) { svg._cafe.textContent = CAFE_NAME[i]; }
  }

  window.MeshVizScene = { build: build, setFrame: setFrame, count: 8 };
}());

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

  var DHT = ['M202 234Q250 150 340 98', 'M472 234Q440 150 410 100', 'M722 234Q640 130 460 92'];
  var ROUTES = { nl: 'M190 342H350', lo: 'M450 342H610', no: 'M140 364Q400 450 660 364' };

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
    var o = el('g', { transform: 'translate(' + x + ' ' + y + ')' }, parent, 'v-lock ' + cls);
    var g = el('g', {}, o, 'v-pop');
    el('circle', { r: 13 }, g, 'v-lock-bg');
    el('path', { d: 'M-4 -1V-4a4 4 0 0 1 8 0V-1' }, g, 'v-lock-arc');
    el('rect', { x: -6, y: -1, width: 12, height: 9, rx: 2 }, g, 'v-lock-body');
    return o;
  }

  function cross(parent, x, y, cls) {
    var o = el('g', { transform: 'translate(' + x + ' ' + y + ')' }, parent, 'v-cross ' + cls);
    var g = el('g', {}, o, 'v-pop');
    el('circle', { r: 13 }, g, 'v-cross-bg');
    el('path', { d: 'M-6 -6L6 6M6 -6L-6 6' }, g, 'v-cross-x');
    return o;
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
    el('rect', { x: cx - 64, y: 284, width: 128, height: 30, rx: 15 }, key, 'v-key-bg');
    text(key, cx, 305, 'home-lab', 'v-key-text');
    var node = el('g', { 'data-node': p.node }, g, 'v-node');
    el('rect', { x: cx - 50, y: 322, width: 100, height: 40, rx: 8 }, node, 'v-node-bg');
    text(node, cx, 347, p.node, 'v-node-text');
  }

  function dhtLinks(svg) {
    DHT.forEach(function (d) { el('path', { d: d }, svg, 'v-dht-link'); });
  }

  function links(svg) {
    var defs = [['nl', 'M190 342H350', 270, 342], ['lo', 'M450 342H610', 530, 342],
      ['no', 'M140 364Q400 450 660 364', 400, 407]];
    defs.forEach(function (d) {
      var g = el('g', {}, svg, 'v-link v-link-' + d[0]);
      d[1] = ROUTES[d[0]];
      el('path', { d: d[1] }, g, 'v-dash');
      el('path', { d: d[1], pathLength: 1 }, g, 'v-solid');
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

  // A glowing dot that runs along a path (CSS offset-path); phase in seconds.
  function packet(svg, d, cls, phase) {
    var c = el('circle', { r: 5 }, svg, 'v-pk ' + cls);
    c.style.setProperty('offset-path', "path('" + d + "')");
    c.style.setProperty('--ph', phase + 's');
    return c;
  }

  function packets(svg) {
    Object.keys(ROUTES).forEach(function (k) {
      packet(svg, ROUTES[k], 'pk-' + k, 0);
      packet(svg, ROUTES[k], 'pk-' + k + ' pk-r', 1.5);
    });
    DHT.forEach(function (d, i) { packet(svg, d, 'v-wr', i * 0.8); });
    packet(svg, 'M350 342H190', 'v-req', 0.5);
  }

  function defs(svg) {
    var d = el('defs', {}, svg);
    var g = el('linearGradient', { id: 'v-grad', x1: 0, y1: 0, x2: 0, y2: 1 }, d);
    el('stop', { offset: 0, 'class': 'v-grad-a' }, g);
    el('stop', { offset: 1, 'class': 'v-grad-b' }, g);
  }

  function extras(svg) {
    var bar = el('g', {}, svg, 'v-addr');
    el('rect', { x: 256, y: 182, width: 288, height: 38, rx: 19 }, bar, 'v-addr-bg');
    text(bar, 400, 207, 'http://nas.meshtown', 'v-addr-text');
    var panel = el('g', {}, svg, 'v-panel');
    el('rect', { x: 10, y: 182, width: 240, height: 38, rx: 8 }, panel, 'v-panel-bg');
    text(panel, 130, 207, 'NAS · web panel', 'v-panel-text');
  }

  function build(stage, alt) {
    var svg = el('svg', { viewBox: '0 20 800 432', role: 'img', 'aria-labelledby': 'viz-title',
      'data-frame': '1' }, null, 'viz-svg');
    var title = el('title', { id: 'viz-title' }, svg);
    title.textContent = alt || 'How Mesh Town connects your devices';
    defs(svg);
    cloud(svg);
    dhtLinks(svg);
    PLACES.forEach(function (p) { place(svg, p); });
    links(svg);
    packets(svg);
    extras(svg);
    svg._cafe = PLACES[1].label;
    setFrame(svg, 1);
    if (stage) { stage.appendChild(svg); }
    return svg;
  }

  function setFrame(svg, n) {
    var i = Math.max(1, Math.min(8, n)) - 1;
    svg.setAttribute('data-frame', String(i + 1));
    svg.setAttribute('class', ('viz-svg ' + FRAME_CLASSES[i === 7 ? 7 : Math.min(i, 6)]).trim() + ' f' + (i + 1) + (svg._go ? ' go' : ''));
    if (svg._cafe) { svg._cafe.textContent = CAFE_NAME[i]; }
  }

  function start(svg) { svg._go = true; svg.classList.add('go'); }

  window.MeshVizScene = { build: build, setFrame: setFrame, start: start, count: 8 };
}());

/* Mesh Town explainer: step controls, autoplay and captions. */
(function () {
  'use strict';
  var figure = document.querySelector('[data-viz]');
  var scene = window.MeshVizScene;
  if (!figure || !scene) { return; }
  var items = figure.querySelectorAll('[data-viz-frames] li');
  var stage = figure.querySelector('[data-viz-stage]');
  if (items.length !== 8 || !stage) { return; }

  var COUNT = 8, DELAY = 7000;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  var frame = 1, want = !reduce.matches, visible = false, timer = 0, running = false;
  var img = stage.querySelector('.viz-static');
  var svg = scene.build(null, img ? img.getAttribute('alt') : '');
  if (img) { stage.replaceChild(svg, img); } else { stage.appendChild(svg); }

  function mk(tag, cls, parent) {
    var e = document.createElement(tag);
    if (cls) { e.className = cls; }
    if (parent) { parent.appendChild(e); }
    return e;
  }
  function titleOf(n) {
    return items[n - 1].querySelector('strong').textContent.replace(/\.\s*$/, '');
  }

  var ICON = {
    prev: '<path d="M15 5 7 12l8 7z"/>', next: '<path d="m9 5 8 7-8 7z"/>',
    pause: '<path d="M7 5h4v14H7zM13 5h4v14h-4z"/>', play: '<path d="m7 5 11 7-11 7z"/>'
  };
  function icon(btn, name) {
    btn.innerHTML = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" focusable="false">' + ICON[name] + '</svg>';
  }

  var head = mk('div', 'viz-head', null);
  figure.insertBefore(head, stage);
  var slides = [];
  for (var n = 1; n <= COUNT; n++) {
    var li = items[n - 1];
    var slide = mk('div', 'viz-slide', head);
    mk('h3', 'viz-title', slide).textContent = titleOf(n);
    var text = mk('p', 'viz-text', slide);
    for (var c = li.firstChild; c; c = c.nextSibling) {
      if (c.nodeName !== 'STRONG') { text.appendChild(c.cloneNode(true)); }
    }
    text.firstChild.nodeValue = text.firstChild.nodeValue.replace(/^\s+/, '');
    slides.push(slide);
  }
  var live = mk('div', 'viz-sr', figure);
  live.setAttribute('data-viz-caption', '');

  stage.tabIndex = 0;
  stage.setAttribute('role', 'group');
  stage.setAttribute('aria-label', 'Diagram. Use the left and right arrow keys to change the step.');

  var controls = mk('div', 'viz-controls', null);
  controls.setAttribute('role', 'group');
  controls.setAttribute('aria-label', 'Diagram steps');
  figure.insertBefore(controls, stage.nextSibling);
  var prevBtn = mk('button', 'viz-btn viz-prev', controls);
  var playBtn = mk('button', 'viz-btn viz-play', controls);
  var nextBtn = mk('button', 'viz-btn viz-next', controls);
  var dots = mk('div', 'viz-dots', controls);
  [prevBtn, playBtn, nextBtn].forEach(function (b) { b.type = 'button'; });
  icon(prevBtn, 'prev');
  icon(nextBtn, 'next');
  prevBtn.setAttribute('aria-label', 'Previous step');
  nextBtn.setAttribute('aria-label', 'Next step');
  var steps = [];
  for (var i = 1; i <= COUNT; i++) {
    var b = mk('button', 'viz-dot', dots);
    b.type = 'button';
    mk('span', 'viz-dot-fill', b);
    b.setAttribute('aria-label', 'Step ' + i + ': ' + titleOf(i));
    b.title = titleOf(i);
    b.setAttribute('data-step', String(i));
    steps.push(b);
  }
  figure.querySelector('[data-viz-frames]').hidden = true;

  function stop() { clearTimeout(timer); timer = 0; running = false; }
  function schedule() {
    clearTimeout(timer);
    running = want && visible && !document.hidden && !reduce.matches;
    if (running) { timer = setTimeout(tick, DELAY); }
  }
  function tick() {
    if (frame >= COUNT) { want = false; stop(); render(false); return; }
    show(frame + 1);
    schedule();
    render(false);
  }

  function show(n) {
    frame = Math.max(1, Math.min(COUNT, n));
    scene.setFrame(svg, frame);
    figure.setAttribute('data-frame', String(frame));
    slides.forEach(function (sl, k) { sl.classList.toggle('is-active', k + 1 === frame); });
    live.textContent = 'Step ' + frame + ' of ' + COUNT + ': ' + titleOf(frame);
    steps.forEach(function (s, k) {
      if (k + 1 === frame) { s.setAttribute('aria-current', 'step'); } else { s.removeAttribute('aria-current'); }
    });
    prevBtn.disabled = frame === 1;
    nextBtn.disabled = frame === COUNT;
    figure.dispatchEvent(new CustomEvent('meshviz:frame', { detail: { frame: frame, title: titleOf(frame) } }));
  }

  function render() {
    figure.setAttribute('data-playing', running ? 'true' : 'false');
    icon(playBtn, want ? 'pause' : 'play');
    playBtn.setAttribute('aria-label', want ? 'Pause autoplay' : 'Play autoplay');
    live.setAttribute('aria-live', running ? 'off' : 'polite');
  }

  function user(n) {
    want = false;
    stop();
    render();
    show(n);
  }
  function play() {
    if (frame >= COUNT) { show(1); }
    want = true;
    schedule();
    render();
  }
  function pause() { want = false; stop(); render(); }

  prevBtn.addEventListener('click', function () { user(frame - 1); });
  nextBtn.addEventListener('click', function () { user(frame + 1); });
  playBtn.addEventListener('click', function () { if (want) { pause(); } else { play(); } });
  steps.forEach(function (s, k) { s.addEventListener('click', function () { user(k + 1); }); });
  figure.addEventListener('keydown', function (e) {
    if (e.altKey || e.ctrlKey || e.metaKey) { return; }
    if (e.key === 'ArrowRight') { e.preventDefault(); user(frame + 1); }
    if (e.key === 'ArrowLeft') { e.preventDefault(); user(frame - 1); }
  });
  var sx = 0, sy = 0;
  stage.addEventListener('touchstart', function (e) {
    sx = e.changedTouches[0].clientX;
    sy = e.changedTouches[0].clientY;
  }, { passive: true });
  stage.addEventListener('touchend', function (e) {
    var dx = e.changedTouches[0].clientX - sx, dy = e.changedTouches[0].clientY - sy;
    if (Math.abs(dx) > 40 && Math.abs(dx) > 1.5 * Math.abs(dy)) { user(frame + (dx < 0 ? 1 : -1)); }
  }, { passive: true });
  figure.addEventListener('focusin', function (e) {
    if (want && e.target.matches(':focus-visible')) { pause(); }
  });
  document.addEventListener('visibilitychange', function () { schedule(); render(); });
  if (reduce.addEventListener) {
    reduce.addEventListener('change', function () { if (reduce.matches) { want = false; } schedule(); render(); });
  }
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      visible = entries[entries.length - 1].isIntersecting;
      if (visible) { scene.start(svg); }
      schedule();
      render();
    }, { threshold: 0.5 }).observe(stage);
  }

  if (!('IntersectionObserver' in window)) { scene.start(svg); }
  show(1);
  render();
  figure.setAttribute('data-viz-ready', '');
  window.MeshViz = {
    count: COUNT,
    go: user, next: function () { user(frame + 1); }, prev: function () { user(frame - 1); },
    play: play, pause: pause,
    get frame() { return frame; }, get playing() { return running; }
  };
}());

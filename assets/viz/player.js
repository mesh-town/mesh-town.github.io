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
    parent.appendChild(e);
    return e;
  }
  function titleOf(n) {
    return items[n - 1].querySelector('strong').textContent.replace(/\.\s*$/, '');
  }

  var controls = mk('div', 'viz-controls', figure);
  controls.setAttribute('role', 'group');
  controls.setAttribute('aria-label', 'Diagram steps');
  figure.insertBefore(controls, stage.nextSibling);
  var prevBtn = mk('button', 'viz-prev', controls);
  var playBtn = mk('button', 'viz-play', controls);
  var nextBtn = mk('button', 'viz-next', controls);
  mk('span', 'viz-sep', controls);
  [prevBtn, playBtn, nextBtn].forEach(function (b) { b.type = 'button'; });
  prevBtn.textContent = 'Previous';
  nextBtn.textContent = 'Next';
  var steps = [];
  for (var i = 1; i <= COUNT; i++) {
    var b = mk('button', 'viz-step-btn', controls);
    b.type = 'button';
    b.textContent = String(i);
    b.setAttribute('aria-label', 'Step ' + i + ': ' + titleOf(i));
    b.setAttribute('data-step', String(i));
    steps.push(b);
  }
  var caption = document.createElement('p');
  caption.className = 'viz-caption';
  caption.setAttribute('data-viz-caption', '');
  figure.insertBefore(caption, controls.nextSibling);
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
    var li = items[frame - 1];
    caption.textContent = '';
    mk('span', 'viz-step', caption).textContent = 'Step ' + frame + ' of ' + COUNT;
    for (var c = li.firstChild; c; c = c.nextSibling) { caption.appendChild(c.cloneNode(true)); }
    steps.forEach(function (s, k) {
      if (k + 1 === frame) { s.setAttribute('aria-current', 'step'); } else { s.removeAttribute('aria-current'); }
    });
    prevBtn.disabled = frame === 1;
    nextBtn.disabled = frame === COUNT;
    figure.dispatchEvent(new CustomEvent('meshviz:frame', { detail: { frame: frame, title: titleOf(frame) } }));
  }

  function render() {
    figure.setAttribute('data-playing', running ? 'true' : 'false');
    playBtn.textContent = want ? 'Pause' : 'Play';
    playBtn.setAttribute('aria-label', want ? 'Pause autoplay' : 'Play autoplay');
    caption.setAttribute('aria-live', running ? 'off' : 'polite');
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
  controls.addEventListener('focusin', function (e) {
    if (want && e.target.matches(':focus-visible')) { pause(); }
  });
  document.addEventListener('visibilitychange', function () { schedule(); render(); });
  if (reduce.addEventListener) {
    reduce.addEventListener('change', function () { if (reduce.matches) { want = false; } schedule(); render(); });
  }
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      visible = entries[entries.length - 1].isIntersecting;
      schedule();
      render();
    }, { threshold: 0.5 }).observe(stage);
  }

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

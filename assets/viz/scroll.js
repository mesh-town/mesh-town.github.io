/* Mesh Town explainer: picks the active step from the scroll position and sets classes and --p on the scene. */
(function () {
  'use strict';
  var section = document.querySelector('[data-scene]');
  if (!section || !window.MeshScene) { return; }
  var STEP_CLASSES = ['', '', 'net', 'net dht', 'net links', 'net links name', 'net links exit', 'net links move'];
  var stage = section.querySelector('[data-scene-stage]');
  var steps = [].slice.call(section.querySelectorAll('li[data-step]'));
  var sr = section.querySelector('[data-scene-sr]');
  var narrow = window.matchMedia('(max-width: 47.99rem)');
  var motion = window.matchMedia('(prefers-reduced-motion: reduce)');
  var layout, svg, shownStep = 0, lastKey = '', queued = false;

  function mount() {
    var next = narrow.matches ? 'v' : 'h';
    if (next === layout) { return; }
    var fresh = window.MeshScene.build(next);
    if (svg) { stage.replaceChild(fresh, svg); } else { stage.insertBefore(fresh, stage.firstChild); }
    svg = fresh;
    layout = next;
    shownStep = 0;
    lastKey = '';
  }

  function state() {
    var box = section.getBoundingClientRect();
    var line = window.innerHeight * (layout === 'v' ? 0.8 : 0.6);
    var active = 1, p = 0, i, r;
    if (box.bottom < 0) { return { active: 7, p: 1 }; }
    if (box.top > window.innerHeight) { return { active: 1, p: 0 }; }
    for (i = 0; i < steps.length; i++) {
      r = steps[i].getBoundingClientRect();
      if (r.top <= line) { active = i + 1; p = Math.min(1, Math.max(0, (line - r.top) / r.height)); }
    }
    return { active: active, p: p };
  }

  function apply(s) {
    var key = layout + s.active + (motion.matches ? '1' : s.p.toFixed(3));
    var i;
    if (key === lastKey) { return; }
    lastKey = key;
    svg.className.baseVal = 'v-svg layout-' + layout + ' ' + STEP_CLASSES[s.active];
    svg.style.setProperty('--p', motion.matches ? '1' : s.p.toFixed(3));
    section.dataset.step = s.active;
    for (i = 0; i < steps.length; i++) { steps[i].classList.toggle('is-active', i + 1 === s.active); }
    if (s.active !== shownStep) {
      shownStep = s.active;
      if (sr) { sr.textContent = 'Step ' + s.active + ' of 7: ' + steps[s.active - 1].querySelector('h3').textContent; }
    }
  }

  function frame() { queued = false; apply(state()); }
  function request() { if (!queued) { queued = true; window.requestAnimationFrame(frame); } }
  function relayout() { mount(); request(); }

  mount();
  section.setAttribute('data-scene-ready', '');
  window.addEventListener('scroll', request, { passive: true });
  window.addEventListener('resize', request);
  if (narrow.addEventListener) { narrow.addEventListener('change', relayout); } else { narrow.addListener(relayout); }
  if (motion.addEventListener) { motion.addEventListener('change', request); }
  frame();
})();

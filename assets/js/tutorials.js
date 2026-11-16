(function () {
  "use strict";

  var KEY = "meshtown.tutorials";
  var OSES = ["windows", "macos", "android"];
  var NETS = ["invite", "create"];
  var root = document.querySelector("[data-tut]");
  if (!root) { return; }

  var steps = Array.prototype.slice.call(root.querySelectorAll("[data-tut-step]"));
  var strip = root.querySelector("[data-tut-strip]");
  var prompt = root.querySelector("[data-tut-prompt]");
  var endBox = root.querySelector("[data-tut-end]");
  var androidNote = root.querySelector("[data-tut-android-note]");
  var state = { os: null, net: null, done: [], open: null };
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function pick(list, value) { return list.indexOf(value) >= 0 ? value : null; }
  function words(el, name) { return (el.getAttribute(name) || "").split(" "); }

  function detectOS() {
    var nav = window.navigator || {};
    var ua = nav.userAgent || "";
    if (/Android/.test(ua)) { return "android"; }
    if (/iPhone|iPad|iPod/.test(ua) || (/Macintosh/.test(ua) && (nav.maxTouchPoints || 0) > 1)) { return null; }
    if (/Windows/.test(ua)) { return "windows"; }
    return /Macintosh/.test(ua) ? "macos" : null;
  }

  function load() {
    try { return JSON.parse(window.localStorage.getItem(KEY)) || {}; } catch (e) { return {}; }
  }

  function save() {
    try { window.localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) { /* storage blocked */ }
  }

  function stepById(id) {
    return steps.filter(function (s) { return s.id === id; })[0] || null;
  }

  function visible(step) {
    return !!state.os && !!state.net && words(step, "data-oses").indexOf(state.os) >= 0 && words(step, "data-nets").indexOf(state.net) >= 0;
  }

  function shown() { return steps.filter(visible); }
  function isDone(step) { return state.done.indexOf(step.id) >= 0; }

  function nextOpen(list) {
    var left = list.filter(function (s) { return !isDone(s); });
    return left.length ? left[0].id : null;
  }

  function fromUrl() {
    var q = new URLSearchParams(window.location.search);
    return { os: pick(OSES, q.get("os")), net: pick(NETS, q.get("net")) };
  }

  function topicFromHash() {
    var id = window.location.hash.replace("#", "");
    return id ? stepById(id) : null;
  }

  function syncUrl() {
    if (!window.history || !window.history.replaceState) { return; }
    var q = [];
    if (state.os) { q.push("os=" + state.os); }
    if (state.net) { q.push("net=" + state.net); }
    var search = q.length ? "?" + q.join("&") : "";
    window.history.replaceState(null, "", window.location.pathname + search + window.location.hash);
  }

  function setButtons() {
    Array.prototype.forEach.call(root.querySelectorAll("[data-tut-os]"), function (b) {
      b.setAttribute("aria-pressed", b.getAttribute("data-tut-os") === state.os ? "true" : "false");
    });
    Array.prototype.forEach.call(root.querySelectorAll("[data-tut-net]"), function (b) {
      var create = b.getAttribute("data-tut-net") === "create";
      b.hidden = create && state.os === "android";
      b.setAttribute("aria-pressed", b.getAttribute("data-tut-net") === state.net ? "true" : "false");
    });
    androidNote.hidden = state.os !== "android";
  }

  function setVariants() {
    Array.prototype.forEach.call(root.querySelectorAll("[data-os-only]"), function (el) {
      el.hidden = !state.os || words(el, "data-os-only").indexOf(state.os) < 0;
    });
  }

  function buildStrip(list, current) {
    strip.textContent = "";
    var label = document.createElement("p");
    label.className = "tut-strip-label";
    var n = current < 0 ? list.length : current + 1;
    label.textContent = "Step " + n + " of " + list.length;
    var ol = document.createElement("ol");
    list.forEach(function (step, i) {
      var li = document.createElement("li");
      var b = document.createElement("button");
      b.type = "button";
      b.textContent = String(i + 1);
      b.setAttribute("aria-label", "Step " + (i + 1) + ": " + step.querySelector(".tut-title").textContent);
      b.disabled = !isDone(step) && i !== current;
      if (isDone(step)) { b.className = "is-done"; }
      if (i === current) { b.setAttribute("aria-current", "step"); }
      b.addEventListener("click", function () { openStep(step.id, true); });
      li.appendChild(b);
      ol.appendChild(li);
    });
    strip.appendChild(label);
    strip.appendChild(ol);
  }

  function render() {
    var list = shown();
    var ready = !!state.os && !!state.net;
    setButtons();
    setVariants();
    prompt.hidden = ready;
    strip.hidden = !ready;
    steps.forEach(function (s) { s.hidden = !visible(s); });
    var open = state.open && list.some(function (s) { return s.id === state.open; }) ? state.open : nextOpen(list);
    list.forEach(function (s, i) {
      s.querySelector(".tut-num").textContent = String(i + 1);
      s.classList.toggle("is-done", isDone(s));
      s.classList.toggle("is-open", s.id === open);
      s.querySelector(".tut-body").hidden = s.id !== open;
      s.querySelector(".tut-toggle").setAttribute("aria-expanded", s.id === open ? "true" : "false");
      s.querySelector("[data-tut-done]").textContent = i === list.length - 1 ? "Done" : "Done — next step";
    });
    var current = list.indexOf(stepById(nextOpen(list)));
    if (ready) { buildStrip(list, current); }
    endBox.hidden = !(ready && list.length && nextOpen(list) === null);
    syncUrl();
    save();
  }

  function scrollTo(el) {
    if (el && el.scrollIntoView) { el.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" }); }
  }

  function openStep(id, scroll) {
    state.open = id;
    render();
    if (scroll) { scrollTo(stepById(id)); }
  }

  // A step opened from its own heading keeps that heading where it was on screen: the step that closes above it
  // would otherwise pull it up and out of view, and the step would seem to open upwards.
  function openInPlace(step, heading) {
    var before = heading.getBoundingClientRect().top;
    openStep(step.id, false);
    window.scrollBy({ top: heading.getBoundingClientRect().top - before, behavior: "instant" });
  }

  function markDone(step) {
    if (!isDone(step)) { state.done.push(step.id); }
    var list = shown();
    state.open = nextOpen(list);
    render();
    scrollTo(state.open ? stepById(state.open) : endBox);
  }

  function choose(kind, value) {
    state[kind] = value;
    if (state.os === "android") { state.net = "invite"; }
    state.open = null;
    render();
  }

  function applyHash() {
    var step = topicFromHash();
    if (!step) { return; }
    if (!state.net) { state.net = words(step, "data-nets")[0]; }
    if (state.os === "android" && !visible(step)) { return; }
    if (state.net && !visible(step) && words(step, "data-oses").indexOf(state.os) >= 0) { state.net = words(step, "data-nets")[0]; }
    state.open = step.id;
    render();
    if (visible(step)) { scrollTo(step); }
  }

  function wrapHeading(step) {
    var h = step.querySelector("h2");
    var title = h.querySelector(".tut-title");
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "tut-toggle";
    btn.setAttribute("aria-expanded", "true");
    while (h.firstChild) { btn.appendChild(h.firstChild); }
    h.appendChild(btn);
    btn.addEventListener("click", function () { openInPlace(step, btn); });
    return title;
  }

  function addDone(step) {
    var p = document.createElement("p");
    p.className = "tut-actions";
    var b = document.createElement("button");
    b.type = "button";
    b.className = "btn btn-primary";
    b.setAttribute("data-tut-done", "");
    b.addEventListener("click", function () { markDone(step); });
    p.appendChild(b);
    step.querySelector(".tut-body").appendChild(p);
  }

  function reset() {
    try { window.localStorage.removeItem(KEY); } catch (e) { /* storage blocked */ }
    state = { os: detectOS(), net: null, done: [], open: null };
    window.history.replaceState(null, "", window.location.pathname);
    render();
    window.scrollTo(0, 0);
  }

  function bind() {
    Array.prototype.forEach.call(root.querySelectorAll("[data-tut-os]"), function (b) {
      b.addEventListener("click", function () { choose("os", b.getAttribute("data-tut-os")); });
    });
    Array.prototype.forEach.call(root.querySelectorAll("[data-tut-net]"), function (b) {
      b.addEventListener("click", function () { choose("net", b.getAttribute("data-tut-net")); });
    });
    root.querySelector("[data-tut-reset]").addEventListener("click", reset);
    window.addEventListener("hashchange", applyHash);
  }

  function init() {
    var saved = load();
    var url = fromUrl();
    state.os = url.os || pick(OSES, saved.os) || detectOS();
    state.net = url.net || pick(NETS, saved.net);
    state.done = Array.isArray(saved.done) ? saved.done : [];
    state.open = typeof saved.open === "string" ? saved.open : null;
    if (state.os === "android") { state.net = "invite"; }
    steps.forEach(function (s) { wrapHeading(s); addDone(s); });
    root.querySelector("[data-tut-controls]").hidden = false;
    bind();
    render();
    applyHash();
  }

  init();
})();

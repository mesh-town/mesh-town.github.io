/* Tutorials as a wizard: one question at a time (device, then invite or new network), then one step at a time.
   Nothing is stored: the answers and the open step live in the address (?os=&net=#step), so a link or a reload
   opens the same place, and the plain address starts from the first question. Without JS the page reads as a list. */
(function () {
  "use strict";

  var OSES = ["windows", "macos", "android"];
  var NETS = ["invite", "create"];
  var root = document.querySelector("[data-tut]");
  if (!root) { return; }

  function one(sel) { return root.querySelector(sel); }
  function all(sel) { return Array.prototype.slice.call(root.querySelectorAll(sel)); }
  function pick(list, value) { return list.indexOf(value) >= 0 ? value : null; }
  function words(el, name) { return (el.getAttribute(name) || "").split(" "); }

  var steps = all("[data-tut-step]");
  var ui = {
    os: one('[data-tut-stage="os"]'), net: one('[data-tut-stage="net"]'), pick: one("[data-tut-pick]"),
    note: one("[data-tut-android-note]"), strip: one("[data-tut-strip]"), list: one(".tut-steps"),
    end: one("[data-tut-end]"), nav: one("[data-tut-nav]"), back: one("[data-tut-back]"), next: one("[data-tut-next]")
  };
  // A tutorial without the invite question shows its steps by device alone.
  var hasNet = !!ui.net;
  // os, net: the answers. at: the open step, counted among the shown ones. reached: the furthest step opened.
  // ended: the closing box is open. want: a step a link asked for; it opens when the answers are known.
  var state = { os: null, net: null, at: 0, reached: 0, ended: false, want: null };
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function detectOS() {
    var nav = window.navigator || {};
    var ua = nav.userAgent || "";
    if (/Android/.test(ua)) { return "android"; }
    if (/iPhone|iPad|iPod/.test(ua) || (/Macintosh/.test(ua) && (nav.maxTouchPoints || 0) > 1)) { return null; }
    if (/Windows/.test(ua)) { return "windows"; }
    return /Macintosh/.test(ua) ? "macos" : null;
  }

  function stepById(id) {
    return steps.filter(function (s) { return s.id === id; })[0] || null;
  }

  function stage() {
    if (!state.os) { return "os"; }
    return hasNet && !state.net ? "net" : "steps";
  }

  function visible(step) {
    return words(step, "data-oses").indexOf(state.os) >= 0 && (!hasNet || words(step, "data-nets").indexOf(state.net) >= 0);
  }

  function shown() { return stage() === "steps" ? steps.filter(visible) : []; }

  // What the current screen starts with: a question, the open step or the closing box.
  function current() {
    var st = stage();
    if (st !== "steps") { return ui[st]; }
    return state.ended ? ui.end : shown()[state.at];
  }

  function fromUrl() {
    var q = new URLSearchParams(window.location.search);
    return { os: pick(OSES, q.get("os")), net: pick(NETS, q.get("net")) };
  }

  function stepFromHash() {
    var id = window.location.hash.replace("#", "");
    return id ? stepById(id) : null;
  }

  function hashNow() {
    if (stage() !== "steps") { return state.want ? "#" + state.want : ""; }
    return "#" + current().id;
  }

  function syncUrl() {
    if (!window.history || !window.history.replaceState) { return; }
    var q = [];
    if (state.os) { q.push("os=" + state.os); }
    if (state.net) { q.push("net=" + state.net); }
    window.history.replaceState(null, "", window.location.pathname + (q.length ? "?" + q.join("&") : "") + hashNow());
  }

  function setIcon(holder, name) {
    var use = holder.querySelector("use");
    use.setAttribute("href", use.getAttribute("href").replace(/#.*$/, "#" + name));
  }

  function card(kind, value) { return one("[data-tut-" + kind + '="' + value + '"]'); }

  function setPick(st) {
    var osCard = state.os && card("os", state.os);
    ui.pick.hidden = st === "os";
    if (ui.note) { ui.note.hidden = !(st === "steps" && state.os === "android"); }
    if (!osCard) { return; }
    var text = [osCard.getAttribute("data-label")];
    if (hasNet && state.net) { text.push(card("net", state.net).getAttribute("data-label")); }
    one("[data-tut-pick-text]").textContent = text.join(" · ");
    setIcon(ui.pick, osCard.querySelector("use").getAttribute("href").split("#")[1]);
  }

  function setVariants() {
    all("[data-os-only]").forEach(function (el) {
      el.hidden = words(el, "data-os-only").indexOf(state.os) < 0;
    });
  }

  function dot(step, i) {
    var li = document.createElement("li");
    var b = document.createElement("button");
    var here = i === state.at && !state.ended;
    b.type = "button";
    b.textContent = String(i + 1);
    b.setAttribute("aria-label", "Step " + (i + 1) + ": " + step.querySelector(".tut-title").textContent);
    b.disabled = i > state.reached && !state.ended;
    if (!b.disabled && !here) { b.className = "is-done"; }
    if (here) { b.setAttribute("aria-current", "step"); }
    b.addEventListener("click", function () { openAt(i); });
    li.appendChild(b);
    return li;
  }

  function buildStrip(list) {
    var label = document.createElement("p");
    var ol = document.createElement("ol");
    label.className = "tut-strip-label";
    label.textContent = state.ended ? "All steps done" : "Step " + (state.at + 1) + " of " + list.length;
    list.forEach(function (step, i) { ol.appendChild(dot(step, i)); });
    ui.strip.replaceChildren(label, ol);
  }

  function setNav(list) {
    var last = state.at === list.length - 1;
    ui.back.hidden = !state.ended && state.at === 0;
    ui.next.hidden = state.ended;
    one("[data-tut-next-label]").textContent = last ? "Finish" : "Next step";
    setIcon(ui.next, last ? "check" : "arrow-right");
  }

  function render() {
    var st = stage();
    var list = shown();
    var open = st === "steps" && !state.ended ? list[state.at] : null;
    ui.os.hidden = st !== "os";
    if (ui.net) { ui.net.hidden = st !== "net"; }
    [ui.strip, ui.list, ui.nav].forEach(function (el) { el.hidden = st !== "steps"; });
    ui.end.hidden = !(st === "steps" && state.ended);
    steps.forEach(function (s) { s.hidden = s !== open; });
    list.forEach(function (s, i) { s.querySelector(".tut-num").textContent = String(i + 1); });
    setPick(st);
    setVariants();
    buildStrip(list);
    setNav(list);
  }

  // Height of what stays pinned on top while scrolling: the site header on wide screens and, above a step, the strip.
  function pinned(el) {
    var header = document.querySelector(".site-header");
    var top = header && window.getComputedStyle(header).position === "sticky" ? header.offsetHeight : 0;
    return top + (ui.strip.hidden || el === ui.pick ? 0 : ui.strip.offsetHeight);
  }

  function scrollTo(el, jump) {
    var mark = el.querySelector("h2") || el;
    var top = mark.getBoundingClientRect().top + window.pageYOffset - pinned(el) - 16;
    window.scrollTo({ top: Math.max(0, top), behavior: jump || reduce ? "auto" : "smooth" });
  }

  function whenLoaded(run) {
    if (document.readyState === "complete") { run(); return; }
    window.addEventListener("load", run);
  }

  // A page opened by a link to a step: the browser puts the step under the site header, this puts it under the strip
  // as well, and once more when the page has loaded and the browser has done its own jump.
  function landOnLoad() {
    scrollTo(current(), true);
    whenLoaded(function () { scrollTo(current(), true); });
  }

  // Draws the screen and brings its start into view. `fromPick` starts the view from the line with the answers.
  function go(fromPick) {
    render();
    syncUrl();
    var el = current();
    scrollTo(fromPick && !ui.pick.hidden ? ui.pick : el);
    el.querySelector("h2").focus({ preventScroll: true });
  }

  // What follows from the answers alone: a phone can only join, and a linked step may belong to one path only.
  function settle() {
    var step = stepById(state.want);
    if (!hasNet || !state.os) { return; }
    if (state.os === "android") { state.net = "invite"; return; }
    if (step && words(step, "data-nets").length === 1) { state.net = words(step, "data-nets")[0]; }
  }

  // Once the answers are known: opens the step a link asked for, or the first one.
  function begin() {
    settle();
    if (stage() !== "steps") { return; }
    state.at = Math.max(0, shown().indexOf(stepById(state.want)));
    state.reached = state.at;
    state.ended = false;
    state.want = null;
  }

  function choose(kind, value) {
    state[kind] = value;
    begin();
    go(true);
  }

  function change() {
    state = { os: null, net: null, at: 0, reached: 0, ended: false, want: null };
    go(false);
  }

  function openAt(i) {
    state.at = i;
    state.reached = Math.max(state.reached, i);
    state.ended = false;
    go(false);
  }

  function back() {
    openAt(state.ended ? state.at : state.at - 1);
  }

  function next() {
    if (state.at < shown().length - 1) { openAt(state.at + 1); return; }
    state.ended = true;
    go(false);
  }

  function onHash() {
    var step = stepFromHash();
    if (!step) { return; }
    state.want = step.id;
    begin();
    go(false);
  }

  function markHere() {
    var here = card("os", detectOS());
    if (here) { here.querySelector("[data-tut-here]").hidden = false; }
  }

  function bind() {
    all("[data-tut-os]").forEach(function (b) {
      b.addEventListener("click", function () { choose("os", b.getAttribute("data-tut-os")); });
    });
    all("[data-tut-net]").forEach(function (b) {
      b.addEventListener("click", function () { choose("net", b.getAttribute("data-tut-net")); });
    });
    one("[data-tut-change]").addEventListener("click", change);
    ui.back.addEventListener("click", back);
    ui.next.addEventListener("click", next);
    window.addEventListener("hashchange", onHash);
  }

  function init() {
    var url = fromUrl();
    var step = stepFromHash();
    state.os = url.os;
    state.net = hasNet ? url.net : null;
    state.want = step ? step.id : null;
    markHere();
    bind();
    begin();
    render();
    // The address gets its #step only after the page has loaded: a browser jumps to the #step it finds at that moment.
    whenLoaded(syncUrl);
    if (step) { landOnLoad(); }
  }

  init();
})();

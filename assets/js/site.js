(function () {
  "use strict";

  var SLUGS = ["macos", "windows", "linux", "android", "router"];
  var NAMES = { macos: "macOS", windows: "Windows", linux: "Linux", android: "Android", router: "a router" };
  var HERO = {
    macos: ["Install for macOS", "install/macos/index.html"],
    windows: ["Install for Windows", "install/windows/index.html"],
    linux: ["Install for Linux", "install/linux/index.html"],
    android: ["Install for Android", "install/android/index.html"],
    router: ["Install on a router", "#install"]
  };
  var DEFAULT_HERO = ["Install Mesh Town", "install/index.html"];
  var IOS_HERO = ["See other systems", "#install"];
  var IOS_LINE = "Mesh Town does not run on iOS. It runs on macOS, Windows, Linux, Android and routers.";

  var current = null;
  var tabs = [];
  var panels = [];

  function detectOS(env) {
    env = env || {};
    var ua = env.ua || "";
    var platform = env.platform || "";
    var uaPlatform = env.uaPlatform || "";
    if (/Android/.test(ua)) { return "android"; }
    if (/iPhone|iPad|iPod/.test(ua)) { return "ios"; }
    if (/Macintosh/.test(ua) && (env.maxTouchPoints || 0) > 1) { return "ios"; }
    if (uaPlatform === "macOS") { return "macos"; }
    if (uaPlatform === "Windows") { return "windows"; }
    if (uaPlatform === "Linux") { return "linux"; }
    if (/^Mac/.test(platform)) { return "macos"; }
    if (/^Win/.test(platform)) { return "windows"; }
    if (/Linux/.test(platform)) { return "linux"; }
    return null;
  }

  function readEnv() {
    var nav = window.navigator || {};
    var uad = nav.userAgentData;
    return {
      ua: nav.userAgent || "",
      platform: nav.platform || "",
      uaPlatform: uad && uad.platform ? uad.platform : "",
      maxTouchPoints: nav.maxTouchPoints || 0
    };
  }

  function setHero(pair, showIosLine) {
    var cta = document.querySelector("[data-hero-cta]");
    var line = document.querySelector("[data-ios-note]");
    if (cta) {
      cta.textContent = pair[0];
      cta.setAttribute("href", pair[1]);
    }
    if (line) {
      line.textContent = showIosLine ? IOS_LINE : "";
      line.hidden = !showIosLine;
    }
  }

  function setNote(text) {
    var note = document.querySelector("[data-os-note]");
    if (note) { note.textContent = text || ""; }
  }

  function select(slug, opts) {
    opts = opts || {};
    if (SLUGS.indexOf(slug) < 0) { return; }
    current = slug;
    tabs.forEach(function (tab) {
      var on = tab.getAttribute("data-os-tab") === slug;
      tab.setAttribute("aria-selected", on ? "true" : "false");
      tab.setAttribute("tabindex", on ? "0" : "-1");
    });
    panels.forEach(function (panel) {
      panel.hidden = panel.getAttribute("data-os-panel") !== slug;
    });
    if (!opts.keepHero) { setHero(HERO[slug], false); }
    if (opts.focus) {
      tabs.forEach(function (tab) {
        if (tab.getAttribute("data-os-tab") === slug) { tab.focus(); }
      });
    }
    if (opts.record && window.history && window.history.replaceState) {
      window.history.replaceState(null, "", "#os=" + slug);
    }
  }

  function onKey(event) {
    var i = tabs.indexOf(event.currentTarget);
    var next = -1;
    if (event.key === "ArrowRight") { next = (i + 1) % tabs.length; }
    else if (event.key === "ArrowLeft") { next = (i + tabs.length - 1) % tabs.length; }
    else if (event.key === "Home") { next = 0; }
    else if (event.key === "End") { next = tabs.length - 1; }
    if (next < 0) { return; }
    event.preventDefault();
    setNote("");
    select(tabs[next].getAttribute("data-os-tab"), { focus: true, record: true });
  }

  function hashSlug() {
    var m = /^#os=([a-z]+)$/.exec(window.location.hash || "");
    return m && SLUGS.indexOf(m[1]) >= 0 ? m[1] : null;
  }

  function setupTabs() {
    var bar = document.querySelector("[data-os-tabs]");
    if (!bar) { return false; }
    tabs = Array.prototype.slice.call(bar.querySelectorAll("[data-os-tab]"));
    panels = Array.prototype.slice.call(document.querySelectorAll("[data-os-panel]"));
    bar.setAttribute("role", "tablist");
    bar.setAttribute("aria-label", "Operating system");
    bar.hidden = false;
    tabs.forEach(function (tab) {
      var slug = tab.getAttribute("data-os-tab");
      tab.setAttribute("role", "tab");
      tab.setAttribute("id", "os-tab-" + slug);
      tab.setAttribute("aria-controls", "os-panel-" + slug);
      tab.addEventListener("click", function () {
        setNote("");
        select(slug, { record: true });
      });
      tab.addEventListener("keydown", onKey);
    });
    panels.forEach(function (panel) {
      var slug = panel.getAttribute("data-os-panel");
      var h3 = panel.querySelector("h3");
      panel.setAttribute("role", "tabpanel");
      panel.setAttribute("id", "os-panel-" + slug);
      panel.setAttribute("aria-labelledby", "os-tab-" + slug);
      if (h3) { h3.classList.add("visually-hidden"); }
    });
    return true;
  }

  function initialSelection() {
    var fromHash = hashSlug();
    if (fromHash) {
      select(fromHash);
      return;
    }
    var os = detectOS(readEnv());
    if (os === "ios") {
      select("macos", { keepHero: true });
      setHero(IOS_HERO, true);
      setNote("Mesh Town does not run on iOS. Pick another device's system.");
    } else if (os) {
      select(os);
      setNote("Detected: " + NAMES[os] + ". Not your system? Pick another one.");
    } else {
      select("macos", { keepHero: true });
      setHero(DEFAULT_HERO, false);
    }
  }

  function init() {
    if (!setupTabs()) { return; }
    initialSelection();
    window.addEventListener("hashchange", function () {
      var slug = hashSlug();
      if (slug && slug !== current) { setNote(""); select(slug); }
    });
  }

  window.MeshSite = {
    detectOS: detectOS,
    select: function (slug) { select(slug, { record: true }); },
    get selected() { return current; }
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();

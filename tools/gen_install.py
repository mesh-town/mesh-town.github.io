"""Generator: writes install/**/index.html from install_data.py.

Usage: python3 -I tools/gen_install.py .   (from the repository root, stdlib only)
"""
import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from install_data import INDEX, OSES  # noqa: E402

BASE = "https://mesh-town.github.io/"
REPO = "https://github.com/mesh-town/meshtown"


def inline(text):
    s = html.escape(text, quote=False)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s.replace("\n", "<br>")


def block(b):
    kind, val = b
    if kind == "h3":
        return "<h3>%s</h3>" % inline(val)
    if kind == "p":
        return "<p>%s</p>" % inline(val)
    if kind == "warn":
        return '<p class="note-warn"><strong>Note.</strong> %s</p>' % inline(val)
    if kind == "cmd":
        return '<pre class="cmd"><code>%s</code></pre>' % html.escape(val, quote=False)
    if kind == "out":
        return '<pre class="out"><code>%s</code></pre>' % html.escape(val, quote=False)
    if kind == "label":
        return '<p class="cmd-label">%s</p>' % inline(val)
    if kind == "ol":
        return "<ol>\n" + "\n".join("<li>%s</li>" % inline(x) for x in val) + "\n</ol>"
    if kind == "tabs":
        return tabs(*val)
    raise ValueError(kind)


def tabs(group, variants):
    bar = "\n".join('<button type="button" class="var-tab" data-var-tab="%s">%s</button>'
                    % (k, html.escape(l)) for k, l, _ in variants)
    panels = "\n".join('<div class="var-panel" data-var-panel="%s">\n<h3>%s</h3>\n%s\n</div>'
                       % (k, html.escape(l), "\n".join(block(b) for b in bs)) for k, l, bs in variants)
    return ('<div class="var-group" data-var-group="%s">\n<div class="var-tabs" data-var-tabs hidden>\n%s\n</div>\n%s\n</div>'
            % (group, bar, panels))


def section(title, blocks, anchor=None):
    attr = ' id="%s"' % html.escape(anchor) if anchor else ""
    return "<h2%s>%s</h2>\n%s" % (attr, html.escape(title), "\n".join(block(b) for b in blocks))


def head(title, desc, canon):
    t = html.escape(title if title.endswith("Mesh Town") else title + " — Mesh Town")
    d = html.escape(desc)
    url = BASE + canon
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<link rel="canonical" href="%s">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Mesh Town">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:url" content="%s">
<link rel="icon" href="../../assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="../../assets/css/theme.css">
<link rel="stylesheet" href="../../assets/css/base.css">
<link rel="stylesheet" href="../../assets/css/sections.css">
</head>
<body>
""" % (t, d, url, t, d, url)


CHROME_TOP = """<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="../../index.html"><img class="brand-logo" src="../../assets/favicon.svg" alt="" width="28" height="28"><span class="brand-name">Mesh Town</span></a>
    <nav class="site-nav" aria-label="Main">
      <ul>
        <li><a href="../../index.html#see-it">How it works</a></li>
        <li><a href="../index.html">Install</a></li>
        <li><a href="%(r)s/tree/main/docs">Docs</a></li>
        <li><a href="%(r)s">GitHub</a></li>
      </ul>
    </nav>
  </div>
</header>
<main id="main" class="wrap page" tabindex="-1">
""" % {"r": REPO}

CHROME_BOTTOM = """</main>
<footer class="site-footer">
  <div class="wrap">
    <ul>
      <li>Mesh Town</li>
      <li><a href="%(r)s">Source</a></li>
      <li><a href="%(r)s/tree/main/docs">Docs</a></li>
      <li><a href="%(r)s-dist">Downloads</a></li>
      <li>License: <a href="%(r)s/blob/main/LICENSE">AGPL-3.0-only</a></li>
    </ul>
  </div>
</footer>
%(js)s</body>
</html>
""" % {"r": REPO, "js": '<script src="../../assets/js/variants.js" defer></script>\n<script src="../../assets/js/copy.js" defer></script>\n'}


def os_strip(current):
    items = []
    for o in OSES:
        cur = ' aria-current="page"' if o["slug"] == current else ""
        href = "../%s/index.html" % o["slug"]
        items.append('<li><a href="%s"%s>%s</a></li>' % (href, cur, html.escape(o["name"])))
    return '<nav class="os-strip" aria-label="Other systems">\n<ul>\n%s\n</ul>\n</nav>' % "\n".join(items)


def breadcrumb(name):
    return ('<nav class="breadcrumb" aria-label="Breadcrumb">\n<ol>\n'
            '<li><a href="../../index.html">Home</a></li>\n<li><a href="../index.html">Install</a></li>\n'
            '<li>%s</li>\n</ol>\n</nav>\n' % html.escape(name))


def step(title, blocks, anchor):
    attr = ' id="%s"' % html.escape(anchor) if anchor else ""
    return '<li class="step">\n<h2%s>%s</h2>\n%s\n</li>' % (attr, html.escape(title), "\n".join(block(b) for b in blocks))


def trouble(items):
    rows = "\n".join("<details><summary>%s</summary><p>%s</p></details>" % (html.escape(q), inline(a)) for q, a in items)
    return "<h2>Troubleshooting</h2>\n" + rows


def page(o):
    steps = "\n".join(step(*st) for st in o["steps"])
    parts = [breadcrumb(o["name"]),
             '<div class="page-head">\n<h1>%s</h1>\n<p class="lede">%s</p>\n<p class="meta">%s</p>\n%s\n</div>'
             % (html.escape(o["title"]), inline(o["lede"]), inline(o["meta"]), os_strip(o["slug"])),
             '<ol class="steps">\n%s\n</ol>' % steps]
    if o["after"]:
        parts.append(section(*o["after"]))
    parts.append(section(*o["maintain"]))
    parts.append(trouble(o["trouble"]))
    docs = " ".join('<a href="%s">%s →</a>' % (html.escape(u), html.escape(l)) for l, u in o["docs"])
    parts.append('<p class="links-line page-refs">%s</p>' % docs)
    canon = "install/%s/" % o["slug"]
    return head(o["title"], o["description"], canon) + CHROME_TOP + "\n".join(parts) + "\n" + CHROME_BOTTOM


def index_page():
    cards = "\n".join('<li><a href="%s/index.html"><strong>%s</strong><span>%s</span></a></li>'
                      % (s, html.escape(n), html.escape(d)) for s, n, d in INDEX["cards"])
    after = "\n".join('<p class="meta">%s</p>' % inline(t) for t in INDEX["after"])
    body = ('<nav class="breadcrumb" aria-label="Breadcrumb">\n<ol>\n<li><a href="../index.html">Home</a></li>\n'
            '<li>Install</li>\n</ol>\n</nav>\n<div class="page-head">\n<h1>%s</h1>\n<p class="lede">%s</p>\n</div>\n<ul class="cards">\n%s\n</ul>\n%s\n'
            % (html.escape(INDEX["title"]), html.escape(INDEX["lede"]), cards, after))
    top = CHROME_TOP.replace("../../", "../").replace('href="../index.html">Install', 'href="index.html">Install')
    bottom = CHROME_BOTTOM
    h = head(INDEX["title"], INDEX["description"], "install/").replace("../../", "../")
    return h + top + body + bottom.replace("../../", "../")


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def main():
    site = sys.argv[1]
    write(os.path.join(site, "install", "index.html"), index_page())
    for o in OSES:
        write(os.path.join(site, "install", o["slug"], "index.html"), page(o))


main()

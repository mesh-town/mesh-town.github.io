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
    if kind == "ol":
        return "<ol>\n" + "\n".join("<li>%s</li>" % inline(x) for x in val) + "\n</ol>"
    raise ValueError(kind)


def section(title, blocks):
    return "<h2>%s</h2>\n%s" % (html.escape(title), "\n".join(block(b) for b in blocks))


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
    <a class="brand" href="../../index.html">Mesh Town</a>
    <nav class="site-nav" aria-label="Main">
      <ul>
        <li><a href="../../index.html#how-it-works">How it works</a></li>
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
""" % {"r": REPO, "js": '<script src="../../assets/js/copy.js" defer></script>\n'}


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


def trouble(items):
    rows = "\n".join("<dt>%s</dt>\n<dd>%s</dd>" % (html.escape(q), inline(a)) for q, a in items)
    return '<h2>Troubleshooting</h2>\n<dl class="trouble">\n%s\n</dl>' % rows


def page(o):
    parts = [breadcrumb(o["name"]), "<h1>%s</h1>" % html.escape(o["title"]),
             '<p class="lede">%s</p>' % inline(o["lede"]), os_strip(o["slug"]),
             section("1. Install", o["install"])]
    if o["check"]:
        parts.append(section("2. Make sure it works", o["check"]))
    parts.append(section(*o["network"]))
    if o["open"]:
        parts.append(section(*o["open"]))
    up = list(o["update"]) + list(o["remove"])
    if up:
        blocks = [("p", "Update:")] + o["update"] if o["remove"] else list(o["update"])
        if o["remove"]:
            blocks += [("p", "Remove:")] + o["remove"]
        parts.append(section("Update and remove" if o["remove"] else "Update", blocks))
    parts.append(trouble(o["trouble"]))
    docs = " · ".join('<a href="%s">%s</a>' % (html.escape(u), html.escape(l)) for l, u in o["docs"])
    parts.append('<h2>More details</h2>\n<p class="links-line">%s</p>' % docs)
    canon = "install/%s/" % o["slug"]
    return head(o["title"], o["description"], canon) + CHROME_TOP + "\n".join(parts) + "\n" + CHROME_BOTTOM


def index_page():
    cards = "\n".join('<li><a href="%s/index.html"><strong>%s</strong><span>%s</span></a></li>'
                      % (s, html.escape(n), html.escape(d)) for s, n, d in INDEX["cards"])
    after = "\n".join("<p>%s</p>" % inline(t) for t in INDEX["after"])
    body = ('<nav class="breadcrumb" aria-label="Breadcrumb">\n<ol>\n<li><a href="../index.html">Home</a></li>\n'
            '<li>Install</li>\n</ol>\n</nav>\n<h1>%s</h1>\n<p class="lede">%s</p>\n<ul class="cards">\n%s\n</ul>\n%s\n'
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

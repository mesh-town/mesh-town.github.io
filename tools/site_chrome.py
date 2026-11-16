"""Shared page chrome for the generated pages (install/**, tutorials/): head, header, footer, inline markup.

`up` is the relative prefix from the page to the site root: "../../" for install/<os>/, "../" for install/ and tutorials/.
"""
import html
import re

BASE = "https://mesh-town.github.io/"
REPO = "https://github.com/mesh-town/meshtown"
DEFAULT_SCRIPTS = ("variants.js", "copy.js")


def icon(name, up, cls=""):
    """An icon from the sprite assets/icons/lucide.svg (tools/build_icons.py); it takes the colour of the text."""
    return ('<svg class="icon%s" aria-hidden="true" focusable="false"><use href="%sassets/icons/lucide.svg#%s"></use></svg>'
            % (" " + cls if cls else "", up, name))


def inline(text):
    """Escapes text; `code`, [label](url) and [[button name]] (a program button, checked against the program texts)."""
    ui = []
    text = re.sub(r"\[\[(.+?)\]\]", lambda m: ui.append(m.group(1)) or "\x00%d\x00" % (len(ui) - 1), text)
    s = html.escape(text, quote=False)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\x00(\d+)\x00", lambda m: '<span class="ui" data-ui="%s">%s</span>'
               % (html.escape(ui[int(m.group(1))]), html.escape(ui[int(m.group(1))], quote=False)), s)
    return s.replace("\n", "<br>")


def block(b, ext=None):
    kind, val = b[0], b[1:]
    val = val[0] if len(val) == 1 else val
    if ext and kind in ext:
        return ext[kind](*b[1:])
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
        return tabs(val[0], val[1], ext, val[2] if len(val) > 2 else "")
    raise ValueError(kind)


def tabs(group, variants, ext=None, label=""):
    bar = "\n".join('<button type="button" class="var-tab" data-var-tab="%s">%s</button>'
                    % (k, html.escape(l)) for k, l, _ in variants)
    panels = "\n".join('<div class="var-panel" data-var-panel="%s">\n<h3>%s</h3>\n%s\n</div>'
                       % (k, html.escape(l), "\n".join(block(b, ext) for b in bs)) for k, l, bs in variants)
    aria = ' data-var-label="%s"' % html.escape(label) if label else ""
    return ('<div class="var-group" data-var-group="%s"%s>\n<div class="var-tabs" data-var-tabs hidden>\n%s\n</div>\n%s\n</div>'
            % (group, aria, bar, panels))


def head(title, desc, canon, up, css=(), js_class=False):
    t = html.escape(title if title.endswith("Mesh Town") else title + " — Mesh Town")
    d = html.escape(desc)
    url = BASE + canon
    sheets = ("theme.css", "base.css", "sections.css") + tuple(css)
    links = "\n".join('<link rel="stylesheet" href="%sassets/css/%s">' % (up, c) for c in sheets)
    jsline = "<script>document.documentElement.classList.add('js')</script>\n" if js_class else ""
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
%s<title>%s</title>
<meta name="description" content="%s">
<link rel="canonical" href="%s">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Mesh Town">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:url" content="%s">
<link rel="icon" href="%sassets/favicon.svg" type="image/svg+xml">
%s
</head>
<body>
""" % (jsline, t, d, url, t, d, url, up, links)


def chrome_top(up):
    return """<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="%(u)sindex.html"><img class="brand-logo" src="%(u)sassets/favicon.svg" alt="" width="28" height="28"><span class="brand-name">Mesh Town</span></a>
    <nav class="site-nav" aria-label="Main">
      <ul>
        <li><a href="%(u)sindex.html#see-it">How it works</a></li>
        <li><a href="%(u)sinstall/index.html">Install</a></li>
        <li><a href="%(u)stutorials/index.html">Tutorials</a></li>
        <li><a href="%(r)s/tree/main/docs">Docs</a></li>
        <li><a href="%(r)s">GitHub</a></li>
      </ul>
    </nav>
  </div>
</header>
<main id="main" class="wrap page" tabindex="-1">
""" % {"r": REPO, "u": up}


def chrome_bottom(up, scripts=DEFAULT_SCRIPTS):
    js = "".join('<script src="%sassets/js/%s" defer></script>\n' % (up, s) for s in scripts)
    return """</main>
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
""" % {"r": REPO, "js": js}


def write(path, text):
    import os
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

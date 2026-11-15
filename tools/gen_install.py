"""Generator: writes install/**/index.html from install_data.py.

Usage: python3 -I tools/gen_install.py .   (from the repository root, stdlib only)
"""
import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from install_data import INDEX, OSES  # noqa: E402
from site_chrome import block, chrome_bottom, chrome_top, head, inline, write  # noqa: E402


def section(title, blocks, anchor=None):
    attr = ' id="%s"' % html.escape(anchor) if anchor else ""
    return "<h2%s>%s</h2>\n%s" % (attr, html.escape(title), "\n".join(block(b) for b in blocks))


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
    return head(o["title"], o["description"], canon, "../../") + chrome_top("../../") + "\n".join(parts) + "\n" + chrome_bottom("../../")


def index_page():
    cards = "\n".join('<li><a href="%s/index.html"><strong>%s</strong><span>%s</span></a></li>'
                      % (s, html.escape(n), html.escape(d)) for s, n, d in INDEX["cards"])
    after = "\n".join('<p class="meta">%s</p>' % inline(t) for t in INDEX["after"])
    body = ('<nav class="breadcrumb" aria-label="Breadcrumb">\n<ol>\n<li><a href="../index.html">Home</a></li>\n'
            '<li>Install</li>\n</ol>\n</nav>\n<div class="page-head">\n<h1>%s</h1>\n<p class="lede">%s</p>\n</div>\n<ul class="cards">\n%s\n</ul>\n%s\n'
            % (html.escape(INDEX["title"]), html.escape(INDEX["lede"]), cards, after))
    return head(INDEX["title"], INDEX["description"], "install/", "../") + chrome_top("../") + body + chrome_bottom("../")


def main():
    site = sys.argv[1]
    write(os.path.join(site, "install", "index.html"), index_page())
    for o in OSES:
        write(os.path.join(site, "install", o["slug"], "index.html"), page(o))


main()

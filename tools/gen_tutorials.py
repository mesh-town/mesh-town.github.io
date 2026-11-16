"""Generator: writes tutorials/index.html from tutorials_data.py and fills the home page tile section.

Usage: python3 -I tools/gen_tutorials.py .   (from the repository root, stdlib only)
A figure is placed only when its file exists in assets/tutorials/ (<id>-light.webp and <id>-dark.webp for the
program's own screens, <id>.webp for other programs' windows).
"""
import html
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from site_chrome import block, chrome_bottom, chrome_top, head, inline, write  # noqa: E402
from tutorials_data import END, FIGS, PAGE, STEPS  # noqa: E402

OS_NAMES = {"windows": "Windows", "macos": "macOS", "android": "Android"}
NET_LABELS = {"invite": "I have an invite", "create": "I am starting a new network"}
SITE = "."


def webp_size(path):
    """Width and height of a WebP file (VP8, VP8L or VP8X), or None."""
    with open(path, "rb") as f:
        d = f.read(40)
    kind = d[12:16]
    if kind == b"VP8X":
        return 1 + int.from_bytes(d[24:27], "little"), 1 + int.from_bytes(d[27:30], "little")
    if kind == b"VP8L":
        bits = struct.unpack("<I", d[21:25])[0]
        return (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1
    if kind == b"VP8 ":
        w, h = struct.unpack("<HH", d[26:30])
        return w & 0x3FFF, h & 0x3FFF
    return None


# A figure is captioned as a screenshot, so nobody takes it for the live page and clicks its buttons; a click opens
# it larger instead (tut-zoom.js).
FIG_KIND = {"devices-scheme": "Diagram"}


def figure(fid):
    alt, own = FIGS[fid]
    names = [fid + "-light.webp", fid + "-dark.webp"] if own else [fid + ".webp"]
    paths = [os.path.join(SITE, "assets", "tutorials", n) for n in names]
    if not all(os.path.exists(p) for p in paths):
        return ""
    size = webp_size(paths[0])
    dims = ' width="%d" height="%d"' % size if size else ""
    src = lambda n: "../assets/tutorials/" + n
    dark = '<source media="(prefers-color-scheme: dark)" srcset="%s">' % src(names[1]) if own else ""
    img = '<img src="%s" alt="%s"%s loading="lazy">' % (src(names[0]), html.escape(alt), dims)
    zoom = '<a class="tut-fig-zoom" href="%s" title="Show larger"><picture>%s%s</picture></a>' % (src(names[0]), dark, img)
    cap = '<figcaption><span class="tut-fig-kind">%s:</span> %s</figcaption>' % (FIG_KIND.get(fid, "Screenshot"), html.escape(alt))
    return '<figure class="tut-fig" data-fig="%s">%s%s</figure>' % (fid, zoom, cap)


def os_block(systems, blocks):
    title = " and ".join(OS_NAMES[s] for s in systems)
    return ('<div class="tut-os" data-os-only="%s">\n<h3 class="tut-os-title">%s</h3>\n%s\n</div>'
            % (" ".join(systems), title, "\n".join(body(b) for b in blocks)))


def fig_os(mapping):
    parts = [(s, figure(f)) for s, f in mapping.items()]
    return "\n".join('<div class="tut-os" data-os-only="%s">%s</div>' % (s, p) for s, p in parts if p)


def note(text):
    return '<p class="meta tut-note">%s</p>' % inline(text)


EXT = {"os": os_block, "fig": figure, "fig-os": fig_os, "note": note}


def body(b):
    return block(b, EXT)


def step(s):
    sid, nets, oses, title, tag, blocks = s
    parts = [x for x in (body(b) for b in blocks) if x]
    tagp = '<p class="meta tut-tag">%s</p>\n' % html.escape(tag) if tag else ""
    return ('<li class="tut-step" id="%s" data-tut-step data-nets="%s" data-oses="%s">\n'
            '<h2><span class="tut-num" aria-hidden="true"></span><span class="tut-title">%s</span></h2>\n%s'
            '<div class="tut-body">\n%s\n</div>\n</li>'
            % (sid, " ".join(nets), " ".join(oses), html.escape(title), tagp, "\n".join(parts)))


def choice(label, qid, attr, items):
    btns = "\n".join('<button type="button" class="os-tab" %s="%s">%s</button>' % (attr, k, html.escape(v)) for k, v in items)
    return ('<div class="tut-q">\n<p class="tut-q-label" id="%s">%s</p>\n<div class="os-tabs" role="group" aria-labelledby="%s">\n%s\n</div>\n</div>'
            % (qid, label, qid, btns))


def controls():
    return ('<div class="tut-controls" data-tut-controls hidden>\n%s\n%s\n<p class="os-note" data-tut-android-note hidden>%s</p>\n'
            '<p><button type="button" class="btn" data-tut-reset>Start over</button></p>\n</div>\n'
            '<p class="meta" data-tut-prompt hidden>Pick your device and your network to see the steps.</p>\n'
            '<div class="tut-strip" data-tut-strip hidden></div>'
            % (choice("Your device", "tut-q-os", "data-tut-os", OS_NAMES.items()),
               choice("Your network", "tut-q-net", "data-tut-net", NET_LABELS.items()),
               html.escape(PAGE["android_note"])))


def end_section():
    lines = "\n".join("<li>%s</li>" % inline(x) for x in END["lines"])
    links = " ".join('<a href="%s">%s →</a>' % (html.escape(u), html.escape(t)) for t, u in END["links"])
    return ('<section class="tut-end" id="done" data-tut-end>\n<h2>%s</h2>\n<ul>\n%s\n</ul>\n<p class="links-line">%s</p>\n</section>'
            % (END["title"], lines, links))


def page():
    steps = "\n".join(step(s) for s in STEPS)
    crumbs = ('<nav class="breadcrumb" aria-label="Breadcrumb">\n<ol>\n<li><a href="../index.html">Home</a></li>\n'
              '<li>Tutorials</li>\n</ol>\n</nav>\n')
    headblock = ('<div class="page-head">\n<h1>%s</h1>\n<p class="lede">%s</p>\n<p class="meta">%s</p>\n</div>\n'
                 % (html.escape(PAGE["title"]), html.escape(PAGE["lede"]), inline(PAGE["other"])))
    main = '<div data-tut>\n%s\n<ol class="tut-steps">\n%s\n</ol>\n%s\n</div>\n' % (controls(), steps, end_section())
    top = head(PAGE["title"], PAGE["description"], "tutorials/", "../", css=("tutorials.css",), js_class=True)
    return top + chrome_top("../") + crumbs + headblock + main + chrome_bottom("../", ("tutorials.js", "tut-zoom.js", "variants.js", "copy.js"))


def main():
    global SITE
    SITE = sys.argv[1]
    write(os.path.join(SITE, "tutorials", "index.html"), page())


main()

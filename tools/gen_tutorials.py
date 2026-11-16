"""Generator: writes the tutorial pages, tutorials/index.html (set up, tutorials_data.py) and
tutorials/devices/index.html (open your devices, tutorials_devices.py).

Usage: python3 -I tools/gen_tutorials.py .   (from the repository root, stdlib only)
A figure is placed only when its file exists in assets/tutorials/ (<id>-light.webp and <id>-dark.webp for the
program's own screens, <id>.webp for other programs' windows).
"""
import html
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from site_chrome import block, chrome_bottom, chrome_top, head, icon, inline, write  # noqa: E402
import tutorials_data  # noqa: E402
import tutorials_devices  # noqa: E402
from tutorials_data import FIGS  # noqa: E402
from tutorials_marks import MARKS  # noqa: E402

OS_NAMES = {"windows": "Windows", "macos": "macOS", "android": "Android"}
# Card: (key, icon, title, text). SHORT is how a choice reads in the line above the steps.
OS_CARDS = (("windows", "monitor", "Windows", "A PC or a laptop"), ("macos", "laptop", "macOS", "A Mac"),
            ("android", "smartphone", "Android", "A phone or a tablet"))
NET_QUESTION = "Do you have an invite?"
NET_HINT = "An invite is a long text or a QR code. Someone who is already in a network makes it for you."
NET_CARDS = (("invite", "mail-open", "Yes, I have an invite", "Join a network that already exists."),
             ("create", "circle-plus", "No, I am starting a new network", "Create your own network here. Then invite your other devices and people."))
SHORT = {"windows": "Windows", "macos": "macOS", "android": "Android", "invite": "I have an invite", "create": "New network"}
SITE = "."
UP = "../"
TUTORIALS = (tutorials_data.TUTORIAL, tutorials_devices.TUTORIAL)


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


def ring_set(boxes, theme):
    box = '<span class="tut-mark%s" aria-hidden="true" style="left:%.1f%%;top:%.1f%%;width:%.1f%%;height:%.1f%%"></span>'
    return "".join(box % ((theme,) + tuple(v * 100 for v in b)) for b in boxes)


def rings(fid):
    """Rings over a figure; a "<fid>-dark" entry gives the dark picture its own rings when it is laid out differently."""
    if fid + "-dark" not in MARKS:
        return ring_set(MARKS.get(fid, []), "")
    return ring_set(MARKS[fid], " tut-mark-light") + ring_set(MARKS[fid + "-dark"], " tut-mark-dark")


def figure(fid):
    alt, own = FIGS[fid]
    names = [fid + "-light.webp", fid + "-dark.webp"] if own else [fid + ".webp"]
    paths = [os.path.join(SITE, "assets", "tutorials", n) for n in names]
    if not all(os.path.exists(p) for p in paths):
        return ""
    size = webp_size(paths[0])
    dims = ' width="%d" height="%d"' % size if size else ""
    src = lambda n: UP + "assets/tutorials/" + n
    dark = '<source media="(prefers-color-scheme: dark)" srcset="%s">' % src(names[1]) if own else ""
    img = '<img src="%s" alt="%s"%s loading="lazy">' % (src(names[0]), html.escape(alt), dims)
    pic = '<span class="tut-fig-pic"><picture>%s%s</picture>%s</span>' % (dark, img, rings(fid))
    zoom = '<a class="tut-fig-zoom" href="%s" title="Show larger">%s</a>' % (src(names[0]), pic)
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


def wait(question, answer):
    """A box for what to do when the step seems stuck: a reader skims past a grey note while waiting."""
    return ('<div class="tut-wait">%s<p><strong>%s</strong> %s</p></div>'
            % (icon("clock", UP, "tut-wait-icon"), html.escape(question), inline(answer)))


EXT = {"os": os_block, "fig": figure, "fig-os": fig_os, "note": note, "wait": wait}


def body(b):
    return block(b, EXT)


def step(s):
    sid, nets, oses, title, tag, blocks = s
    parts = [x for x in (body(b) for b in blocks) if x]
    tagp = '<p class="meta tut-tag">%s</p>\n' % html.escape(tag) if tag else ""
    return ('<li class="tut-step" id="%s" data-tut-step data-nets="%s" data-oses="%s">\n'
            '<h2 tabindex="-1"><span class="tut-num" aria-hidden="true"></span><span class="tut-title">%s</span></h2>\n%s'
            '<div class="tut-body">\n%s\n</div>\n</li>'
            % (sid, " ".join(nets), " ".join(oses), html.escape(title), tagp, "\n".join(parts)))


def card(attr, key, icon_name, title, text):
    badge = '<span class="tut-card-badge" data-tut-here hidden>This device</span>' if attr == "data-tut-os" else ""
    return ('<li><button type="button" class="tut-card" %s="%s" data-label="%s">%s<span class="tut-card-words">'
            '<span class="tut-card-title">%s</span><span class="tut-card-text">%s</span></span>%s</button></li>'
            % (attr, key, html.escape(SHORT[key]), icon(icon_name, UP, "tut-card-icon"), html.escape(title), html.escape(text), badge))


def stage(name, qid, question, hint, attr, cards):
    """One question of the wizard with its answers as cards. Shown by tutorials.js: without it the page reads as a list."""
    hintp = '<p class="tut-hint">%s</p>\n' % html.escape(hint) if hint else ""
    items = "\n".join(card(attr, *c) for c in cards)
    return ('<section class="tut-stage" data-tut-stage="%s" aria-labelledby="%s" hidden>\n<h2 id="%s" tabindex="-1">%s</h2>\n%s'
            '<ul class="tut-cards tut-cards-%d">\n%s\n</ul>\n</section>\n' % (name, qid, qid, html.escape(question), hintp, len(cards), items))


def net_stage(t):
    """The invite question; a tutorial with no "nets" asks only for the device."""
    if not t["nets"]:
        return ""
    return stage("net", "tut-q-net", NET_QUESTION, NET_HINT, "data-tut-net", NET_CARDS)


def picked():
    """What was chosen, with the way back to the first question."""
    return ('<div class="tut-pick" data-tut-pick hidden>\n<p class="tut-pick-what">%s<span data-tut-pick-text></span></p>\n'
            '<button type="button" class="tut-change" data-tut-change>%sChange</button>\n</div>\n' % (icon("monitor", UP), icon("pencil", UP)))


def strip(t):
    """The strip of steps; above it, on a phone, why nobody asked about an invite."""
    note = t["page"]["android_note"]
    notep = '<p class="tut-pick-note" data-tut-android-note hidden>%s</p>\n' % html.escape(note) if note else ""
    return notep + '<div class="tut-strip" data-tut-strip hidden></div>'


def controls(t):
    return stage("os", "tut-q-os", t["page"]["question"], "", "data-tut-os", OS_CARDS) + picked() + net_stage(t) + strip(t)


def nav():
    return ('<p class="tut-nav" data-tut-nav hidden>\n<button type="button" class="btn" data-tut-back>%sBack</button>\n'
            '<button type="button" class="btn btn-primary" data-tut-next><span data-tut-next-label>Next step</span>%s</button>\n</p>'
            % (icon("arrow-left", UP), icon("arrow-right", UP)))


def end_section(end):
    lines = "\n".join("<li>%s</li>" % inline(x) for x in end["lines"])
    links = " ".join('<a href="%s">%s →</a>' % (html.escape(u), html.escape(t)) for t, u in end["links"])
    return ('<section class="tut-end" id="done" data-tut-end>\n<h2 tabindex="-1">%s%s</h2>\n<ul>\n%s\n</ul>\n<p class="links-line">%s</p>\n</section>'
            % (icon("circle-check-big", UP), end["title"], lines, links))


def crumbs(t):
    here = '<li>%s</li>' % html.escape(t["page"]["title"]) if t["key"] else ""
    tut = '<li><a href="../index.html">Tutorials</a></li>' if t["key"] else "<li>Tutorials</li>"
    return ('<nav class="breadcrumb" aria-label="Breadcrumb">\n<ol>\n<li><a href="%sindex.html">Home</a></li>\n%s%s\n</ol>\n</nav>\n'
            % (UP, tut, here))


def page(t):
    pg = t["page"]
    steps = "\n".join(step(s) for s in t["steps"])
    headblock = ('<div class="page-head">\n<h1>%s</h1>\n<p class="lede">%s</p>\n<p class="meta">%s</p>\n</div>\n'
                 % (html.escape(pg["title"]), html.escape(pg["lede"]), inline(pg["other"])))
    main = ('<div data-tut="%s">\n%s\n<ol class="tut-steps">\n%s\n</ol>\n%s\n%s\n</div>\n'
            % (t["key"], controls(t), steps, end_section(t["end"]), nav()))
    top = head(pg["title"], pg["description"], t["dir"] + "/", UP, css=("tutorials.css",), js_class=True)
    return top + chrome_top(UP) + crumbs(t) + headblock + main + chrome_bottom(UP, ("tutorials.js", "tut-zoom.js", "variants.js", "copy.js"))


def main():
    global SITE, UP
    SITE = sys.argv[1]
    for t in TUTORIALS:
        UP = t["up"]
        write(os.path.join(SITE, t["dir"], "index.html"), page(t))


main()

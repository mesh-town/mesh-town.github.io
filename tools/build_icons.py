"""Builds the icon sprite assets/icons/lucide.svg from Lucide icon files (https://lucide.dev, ISC license).

Usage: python3 -I tools/build_icons.py <folder with Lucide .svg files> .   (from the repository root, stdlib only)
The folder is `icons/` of the npm package lucide-static. To add an icon, put its name into ICONS and run the tool again.
A page shows an icon with site_chrome.icon(name, up), or by hand:
<svg class="icon" aria-hidden="true"><use href="assets/icons/lucide.svg#NAME"></use></svg>
"""
import os
import re
import sys

ICONS = ("arrow-left", "arrow-right", "check", "circle-check-big", "circle-plus", "clock", "laptop", "mail-open", "monitor",
         "pencil", "smartphone")
STYLE = 'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
HEAD = '<svg xmlns="http://www.w3.org/2000/svg">\n<!-- Lucide icons, ISC license: see LICENSE-lucide.txt -->\n'


def shapes(path):
    """The drawing of one icon file: what stands between <svg ...> and </svg>, on one line."""
    with open(path, encoding="utf-8") as f:
        inner = re.search(r"<svg[^>]*>(.*)</svg>", f.read(), re.S).group(1)
    return "".join(line.strip() for line in inner.splitlines())


def symbol(src, name):
    return '<symbol id="%s" %s>%s</symbol>\n' % (name, STYLE, shapes(os.path.join(src, name + ".svg")))


def main():
    src, site = sys.argv[1], sys.argv[2]
    out = os.path.join(site, "assets", "icons", "lucide.svg")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(HEAD + "".join(symbol(src, n) for n in ICONS) + "</svg>\n")


main()

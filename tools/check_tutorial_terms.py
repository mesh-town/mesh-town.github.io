"""Check: every button or screen name marked [[...]] in tutorials_data.py occurs in the program's text files.

Usage: python3 -I tools/check_tutorial_terms.py <site root> <path to the program sources>
Text files: web page texts (*-texts.ts), tray texts (*texts*.rs) and the Android app (*.java, *.xml).
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tutorials_data import STEPS  # noqa: E402

NAME_TOKENS = ("${NET_NAME}", '" + NET_NAME + "', "{NET_NAME}", "{APP_NAME}")
ROOTS = ("core/web_gui/ui/vue/src", "core/gui/tray", "platforms/android/gui/app/src/main")
WANTED = (re.compile(r".*-texts\.ts$"), re.compile(r"words\.ts$"), re.compile(r".*texts.*\.rs$"), re.compile(r".*\.(java|xml)$"))


def text_files(src):
    for root in ROOTS:
        for d, _, names in os.walk(os.path.join(src, root)):
            yield from (os.path.join(d, n) for n in names if any(w.match(n) for w in WANTED))


def corpus(src):
    parts = []
    for path in text_files(src):
        with open(path, encoding="utf-8", errors="replace") as f:
            parts.append(f.read())
    text = "\n".join(parts).replace('\\"', '"')
    for token in NAME_TOKENS:
        text = text.replace(token, "Mesh Town")
    return text


def strings(blocks):
    for b in blocks:
        yield from walk(b)


def walk(x):
    if isinstance(x, str):
        yield from re.findall(r"\[\[(.+?)\]\]", x)
    elif isinstance(x, dict):
        yield from walk(list(x.values()))
    elif isinstance(x, (list, tuple)):
        for y in x:
            yield from walk(y)


def main():
    text = corpus(sys.argv[2])
    names = sorted(set(strings([s[5] for s in STEPS])))
    missing = [n for n in names if n not in text]
    for n in missing:
        print("not found in the program texts: %r" % n)
    print("%d names checked, %d mismatches" % (len(names), len(missing)))
    sys.exit(1 if missing else 0)


main()

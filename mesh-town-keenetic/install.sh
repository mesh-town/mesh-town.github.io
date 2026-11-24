#!/bin/sh
# Mesh Town for Keenetic: this address forwards to the installer of the package feed,
#   wget -O- https://mesh-town.github.io/meshtown-keenetic/install.sh | sh
# so both spellings of the name work.
set -e
TMPD="$(mktemp -d)"
trap 'rm -rf "$TMPD"' EXIT
wget -q -O "$TMPD/install.sh" https://mesh-town.github.io/meshtown-keenetic/install.sh
sh "$TMPD/install.sh"

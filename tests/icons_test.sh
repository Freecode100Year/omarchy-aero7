#!/bin/bash
# Checks the Aero7 icon set: one SVG for every app icon name Omarchy's sets cover
# (tools/icon-names.txt), each valid SVG Tiny-style markup that renders, with an
# accessible title, and no filters, masks or clip paths (Qt SVG ignores them).
#   bash tests/icons_test.sh      (needs rsvg-convert for the render check)
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
D="$ROOT/icons/aero7"
fails=0
tmp="$(mktemp --suffix=.png)"
trap 'rm -f "$tmp"' EXIT
bad() { echo "  FAIL $1"; fails=$((fails + 1)); }
while read -r n; do
  [[ -z $n ]] && continue
  f="$D/$n.svg"
  [[ -f $f ]] || { bad "missing $n.svg"; continue; }
  python3 -c 'import sys,xml.dom.minidom as m; d=m.parse(sys.argv[1]).documentElement; assert d.getAttribute("viewBox")=="0 0 512 512"; assert d.getElementsByTagName("title")[0].firstChild.data.strip()' "$f" 2>/dev/null || bad "$n.svg: not valid, no 512 viewBox or no title"
  grep -qE '<(filter|mask|clipPath|foreignObject|script|image)[ >]|href=' "$f" && bad "$n.svg uses filter/mask/clipPath/script/image/href"
  if command -v rsvg-convert >/dev/null; then rsvg-convert -w 32 "$f" -o "$tmp" 2>/dev/null || bad "$n.svg does not render"; fi
done <"$ROOT/tools/icon-names.txt"
extra=$(comm -13 <(sort "$ROOT/tools/icon-names.txt") <(ls "$D" | sed -n 's/\.svg$//p' | sort))
[[ -z $extra ]] || bad "icons without a name in icon-names.txt: $extra"
[[ -f $D/preview.png ]] || bad "preview.png missing"
n=$(grep -c . "$ROOT/tools/icon-names.txt")
if ((fails)); then echo "$fails 项失败 failed"; exit 1; fi
echo "图标全部通过 all $n icons ok"

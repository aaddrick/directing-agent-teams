#!/usr/bin/env bash
# Regenerate every diagram SVG from its .d2 source.
#
# Each diagram body is rendered twice, once against theme-light.d2 and once
# against theme-dark.d2, because d2 inlines custom fills rather than emitting
# them into its prefers-color-scheme block. A single SVG cannot carry both
# palettes. The docs pair the two through a <picture> element.
#
# Needs d2 on PATH (https://d2lang.com/tour/install), or D2 pointing at it:
#   D2=/path/to/d2 ./render.sh
set -euo pipefail

cd "$(dirname "$0")"
D2="${D2:-d2}"

if ! command -v "$D2" >/dev/null 2>&1; then
  echo "render.sh: d2 not found. Install it, or set D2=/path/to/d2." >&2
  exit 1
fi

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

shopt -s nullglob
bodies=()
for f in *.d2; do
  case "$f" in theme-*.d2) ;; *) bodies+=("$f") ;; esac
done

for body in "${bodies[@]}"; do
  name="${body%.d2}"
  for mode in light dark; do
    cat "theme-$mode.d2" "$body" > "$tmp/$name-$mode.d2"
    "$D2" --pad 28 "$tmp/$name-$mode.d2" "$name-$mode.svg" >/dev/null
    echo "  $name-$mode.svg"
  done
done

echo "rendered ${#bodies[@]} diagrams (light + dark)"

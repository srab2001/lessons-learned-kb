#!/usr/bin/env bash
set -e
DOCS="$(dirname "$0")/../docs/retrospectives"
OUT="$(dirname "$0")/../docs/downloads"
mkdir -p "$OUT"

for mdfile in "$DOCS"/*.md; do
  [ -e "$mdfile" ] || continue
  slug=$(basename "$mdfile" .md)
  [ "$slug" = "index" ] && continue
  python3 "$(dirname "$0")/md_to_brief.py" "$mdfile" > "$OUT/retro-${slug}.html"
  echo "Generated: docs/downloads/retro-${slug}.html"
done
echo "Done."

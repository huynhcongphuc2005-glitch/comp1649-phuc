#!/usr/bin/env bash
# Capture every figma/*.html screen as a 2x PNG (860 x 1864) with headless Chrome.
# Usage: bash scripts/capture.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
mkdir -p "$ROOT/figma/png"
for f in "$ROOT"/figma/[0-9]*.html; do
  name="$(basename "$f" .html)"
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars \
    --window-size=430,932 --force-device-scale-factor=2 \
    --virtual-time-budget=4000 \
    --screenshot="$ROOT/figma/png/$name.png" "file://$f" >/dev/null 2>&1
  echo "captured $name.png"
done

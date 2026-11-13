#!/usr/bin/env bash
# Render the hand-drawn style sketches to report/figures/sketches/*.png (2x).
# These are references to redraw on paper; replace a PNG with a photo of your
# own drawing (same file name) and rebuild the report.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
OUT="$ROOT/report/figures/sketches"
mkdir -p "$OUT"
render() { # name width height
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars --allow-file-access-from-files \
    --window-size="$2,$3" --force-device-scale-factor=2 --virtual-time-budget=6000 \
    --screenshot="$OUT/$1.png" "file://$ROOT/scripts/sketches/sketch.html?fig=$1" >/dev/null 2>&1
  echo "sketch $1.png"
}
for s in today plan step focus rest calm settings progress focus_v1; do render "$s" 660 700; done
render idea_flow 1400 720
render settings_v1 1000 700
render storyboard 1500 900
render cards 1500 1130

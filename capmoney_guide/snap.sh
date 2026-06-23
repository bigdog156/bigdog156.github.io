#!/bin/zsh
# Capture the QuickTime iPhone-mirror window by its current bounds (robust to moves).
# Finds the window via Quartz (no AppleEvents -> no hangs), then -R region capture.
# Usage: ./snap.sh <output.png>
OUT="${1:-/tmp/snap.png}"
DIR="$(cd "$(dirname "$0")" && pwd)"
SCR="$DIR/screens"
mkdir -p "$SCR"
[[ "$OUT" != /* ]] && OUT="$SCR/$OUT"

INFO=$(/tmp/pmd3venv/bin/python "$DIR/find_window.py")
[[ -z "$INFO" ]] && { echo "ERR: QuickTime window not found" >&2; exit 1; }
read X Y W H <<< "$INFO"

# Trim the QuickTime title bar (~22 pts) so we capture just the phone screen.
TITLE=22
Y=$((Y + TITLE)); H=$((H - TITLE))

screencapture -x -R${X},${Y},${W},${H} "$OUT"
echo "saved $OUT (region ${X},${Y},${W},${H})"

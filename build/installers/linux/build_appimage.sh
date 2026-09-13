#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
OUT_DIR="$ROOT/dist"
APPDIR="$OUT_DIR/AppDir"
mkdir -p "$APPDIR/usr/bin" "$APPDIR/usr/share/applications" "$APPDIR/usr/share/icons/hicolor/256x256/apps"

cp "$ROOT/build/installers/linux/tinforge.desktop" "$APPDIR/usr/share/applications/tinforge.desktop"
if [[ -f "$ROOT/build/installers/linux/app_icon.png" ]]; then
  cp "$ROOT/build/installers/linux/app_icon.png" "$APPDIR/usr/share/icons/hicolor/256x256/apps/tinforge.png"
fi

if [[ -f "$OUT_DIR/tinforge-v2/tinforge-v2" ]]; then
  cp "$OUT_DIR/tinforge-v2/tinforge-v2" "$APPDIR/usr/bin/tinforge-v2"
  chmod +x "$APPDIR/usr/bin/tinforge-v2"
fi

echo "AppDir prepared at $APPDIR"

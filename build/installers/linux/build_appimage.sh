#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
OUT_DIR="$ROOT/dist"
APPDIR="$OUT_DIR/AppDir"
APPIMAGE_PATH="$OUT_DIR/TinForge-v2.AppImage"
APPIMAGETOOL="${APPIMAGETOOL:-$ROOT/.cache/appimagetool-x86_64.AppImage}"

mkdir -p "$APPDIR/usr/bin" "$APPDIR/usr/share/applications" "$APPDIR/usr/share/icons/hicolor/256x256/apps"
cp "$ROOT/build/installers/linux/tinforge.desktop" "$APPDIR/usr/share/applications/tinforge.desktop"
cp "$ROOT/build/installers/linux/tinforge.desktop" "$APPDIR/tinforge.desktop"
cp "$ROOT/build/installers/linux/AppRun" "$APPDIR/AppRun"
chmod +x "$APPDIR/AppRun"

ICON_SOURCE="$ROOT/src/tinforge_v2/assets/icons/app.png"
if [[ -f "$ICON_SOURCE" ]]; then
  cp "$ICON_SOURCE" "$APPDIR/usr/share/icons/hicolor/256x256/apps/tinforge.png"
  cp "$ICON_SOURCE" "$APPDIR/tinforge.png"
fi

if [[ -f "$OUT_DIR/tinforge-v2/tinforge-v2" ]]; then
  cp "$OUT_DIR/tinforge-v2/tinforge-v2" "$APPDIR/usr/bin/tinforge-v2"
  chmod +x "$APPDIR/usr/bin/tinforge-v2"
fi

mkdir -p "$(dirname "$APPIMAGETOOL")"
if [[ ! -x "$APPIMAGETOOL" ]]; then
  curl -fsSL -o "$APPIMAGETOOL" \
    "https://github.com/AppImage/appimagetool/releases/download/continuous/appimagetool-x86_64.AppImage"
  chmod +x "$APPIMAGETOOL"
fi

ARCH=x86_64 APPIMAGE_EXTRACT_AND_RUN=1 "$APPIMAGETOOL" "$APPDIR" "$APPIMAGE_PATH"
echo "Created $APPIMAGE_PATH"

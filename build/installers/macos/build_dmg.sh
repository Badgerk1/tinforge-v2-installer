#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
OUT_DIR="${DIST_DIR:-$ROOT/dist}"
APP_PATH="$OUT_DIR/tinforge-v2.app"
DMG_PATH="$OUT_DIR/TinForge-v2.dmg"

if [[ ! -d "$APP_PATH" ]]; then
  echo "Expected app bundle at $APP_PATH"
  exit 1
fi

hdiutil create -volname "TinForge v2" -srcfolder "$APP_PATH" -ov -format UDZO "$DMG_PATH"
echo "Created $DMG_PATH"

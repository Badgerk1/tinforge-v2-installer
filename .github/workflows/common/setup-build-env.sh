#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
source "$ROOT_DIR/.github/workflows/common/functions.sh"

TARGET_PLATFORM="${1:-auto}"
if [[ "$TARGET_PLATFORM" == "auto" ]]; then
  case "${RUNNER_OS:-}" in
    Windows) TARGET_PLATFORM="windows" ;;
    macOS) TARGET_PLATFORM="macos" ;;
    Linux) TARGET_PLATFORM="linux" ;;
  esac
fi

log "Setting up build environment for $TARGET_PLATFORM"
ensure_python

python -m pip install --upgrade pip
python -m pip install -r "$ROOT_DIR/requirements-build.txt"
python -m pip install -r "$ROOT_DIR/requirements.txt"

case "$TARGET_PLATFORM" in
  windows)
    if command -v choco >/dev/null 2>&1; then
      choco install nsis --no-progress -y || true
    fi
    ;;
  macos)
    if command -v brew >/dev/null 2>&1; then
      brew install create-dmg || true
    fi
    ;;
  linux)
    if command -v sudo >/dev/null 2>&1; then
      sudo apt-get update
      sudo apt-get install -y fuse libfuse2 desktop-file-utils appstream
    fi
    ;;
esac

log "Build environment ready"

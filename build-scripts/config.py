"""Configuration values for build/release orchestration."""

from __future__ import annotations

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
ARTIFACTS_DIR = ROOT_DIR / ".artifacts"
DIST_DIR = ROOT_DIR / "dist"
EXPECTED_ARTIFACTS = {
    "windows": "TinForge-v2-Setup.exe",
    "macos": "TinForge-v2.dmg",
    "linux": "TinForge-v2.AppImage",
}

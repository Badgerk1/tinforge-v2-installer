"""Application constants and default paths."""

from __future__ import annotations

import os
import platform
from pathlib import Path

APP_NAME = "TinForge v2"
APP_SLUG = "tinforge-v2"
ORG_NAME = "Badgerk1"
PROJECT_FILE_SUFFIX = ".tinforge-project.json"
DEFAULT_EXPORT_FORMATS = ["TP3", "DBX", "LandXML", "DXF", "CSV"]
SUPPORTED_SOURCE_EXTENSIONS = {".csv", ".pdf", ".txt", ".xml", ".dxf", ".dbx", ".tp3"}
RECENT_PROJECTS_LIMIT = 10

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
SRC_ROOT = REPOSITORY_ROOT / "src"
PACKAGE_ROOT = SRC_ROOT / "tinforge_v2"
ASSETS_DIR = PACKAGE_ROOT / "assets"
ICONS_DIR = ASSETS_DIR / "icons"
STYLES_DIR = PACKAGE_ROOT / "gui" / "styles"
REPO_CONFIG_DIR = REPOSITORY_ROOT / "config"
VERSION_PATH = REPO_CONFIG_DIR / "version.json"


def _default_user_config_dir() -> Path:
    if os.name == "nt":
        base = Path(os.getenv("APPDATA", str(Path.home() / "AppData" / "Roaming")))
    elif platform.system() == "Darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(os.getenv("XDG_CONFIG_HOME", str(Path.home() / ".config")))
    return base / APP_SLUG


CONFIG_DIR = _default_user_config_dir()
DEFAULT_SETTINGS_PATH = CONFIG_DIR / "settings.json"
DEFAULT_EXPORT_DIR = Path.home() / "Documents" / APP_NAME / "Exports"
DEFAULT_PROJECT_DIR = Path.home() / "Documents" / APP_NAME / "Projects"

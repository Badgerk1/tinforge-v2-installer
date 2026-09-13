"""Application constants and default paths."""

from pathlib import Path

APP_NAME = "TinForge v2"
APP_SLUG = "tinforge-v2"
ORG_NAME = "Badgerk1"

ROOT_DIR = Path(__file__).resolve().parents[2]
CONFIG_DIR = ROOT_DIR / "config"
DEFAULT_SETTINGS_PATH = CONFIG_DIR / "settings.json"
VERSION_PATH = CONFIG_DIR / "version.json"
DEFAULT_EXPORT_FORMATS = ["TP3", "DBX", "LandXML", "DXF", "CSV"]

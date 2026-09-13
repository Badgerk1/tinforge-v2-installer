"""User and application configuration management."""

from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .constants import (
    CONFIG_DIR,
    DEFAULT_EXPORT_DIR,
    DEFAULT_EXPORT_FORMATS,
    DEFAULT_PROJECT_DIR,
    DEFAULT_SETTINGS_PATH,
)


@dataclass(frozen=True)
class DefaultSettings:
    theme: str = "dark"
    language: str = "en"
    auto_update: bool = True
    default_export_formats: tuple[str, ...] = tuple(DEFAULT_EXPORT_FORMATS)
    default_project_dir: str = str(DEFAULT_PROJECT_DIR)
    default_export_dir: str = str(DEFAULT_EXPORT_DIR)
    logging_level: str = "INFO"
    recent_projects: tuple[str, ...] = ()


class ConfigManager:
    """Load and persist installer application settings."""

    def __init__(self, settings_path: Path | None = None) -> None:
        self.settings_path = settings_path or DEFAULT_SETTINGS_PATH
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        DEFAULT_PROJECT_DIR.mkdir(parents=True, exist_ok=True)
        DEFAULT_EXPORT_DIR.mkdir(parents=True, exist_ok=True)
        self.settings_path.parent.mkdir(parents=True, exist_ok=True)

    def default_settings(self) -> dict[str, Any]:
        defaults = DefaultSettings()
        return {
            "theme": defaults.theme,
            "language": defaults.language,
            "auto_update": defaults.auto_update,
            "default_export_formats": list(defaults.default_export_formats),
            "default_project_dir": defaults.default_project_dir,
            "default_export_dir": defaults.default_export_dir,
            "logging_level": defaults.logging_level,
            "recent_projects": list(defaults.recent_projects),
        }

    def load(self) -> dict[str, Any]:
        defaults = self.default_settings()
        if not self.settings_path.exists():
            self.save(defaults)
            return defaults

        with self.settings_path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)

        merged = deepcopy(defaults)
        merged.update(data)
        merged["default_export_formats"] = list(merged.get("default_export_formats") or defaults["default_export_formats"])
        merged["recent_projects"] = list(merged.get("recent_projects") or [])
        return merged

    def save(self, settings: dict[str, Any]) -> None:
        normalized = deepcopy(self.default_settings())
        normalized.update(settings)
        with self.settings_path.open("w", encoding="utf-8") as handle:
            json.dump(normalized, handle, indent=2, sort_keys=True)
            handle.write("\n")


def load_config(settings_path: Path | None = None) -> dict[str, Any]:
    return ConfigManager(settings_path=settings_path).load()

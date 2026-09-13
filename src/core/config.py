"""User and application configuration management."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from src.core.constants import DEFAULT_SETTINGS_PATH


@dataclass(frozen=True)
class DefaultSettings:
    theme: str = "dark"
    language: str = "en"
    auto_update: bool = True
    default_export_formats: tuple[str, ...] = ("TP3", "DBX")


class ConfigManager:
    """Load and persist installer application settings."""

    def __init__(self, settings_path: Path | None = None) -> None:
        self.settings_path = settings_path or DEFAULT_SETTINGS_PATH
        self.settings_path.parent.mkdir(parents=True, exist_ok=True)

    def default_settings(self) -> dict[str, Any]:
        defaults = DefaultSettings()
        return {
            "theme": defaults.theme,
            "language": defaults.language,
            "auto_update": defaults.auto_update,
            "default_export_formats": list(defaults.default_export_formats),
        }

    def load(self) -> dict[str, Any]:
        if not self.settings_path.exists():
            defaults = self.default_settings()
            self.save(defaults)
            return defaults

        with self.settings_path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)

        merged = self.default_settings()
        merged.update(data)
        return merged

    def save(self, settings: dict[str, Any]) -> None:
        with self.settings_path.open("w", encoding="utf-8") as handle:
            json.dump(settings, handle, indent=2, sort_keys=True)
            handle.write("\n")

"""Version and build metadata."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from src.core.constants import VERSION_PATH


@dataclass(frozen=True)
class VersionInfo:
    version: str
    channel: str = "stable"
    build: str = "local"


class VersionManager:
    def __init__(self, version_path: Path | None = None) -> None:
        self.version_path = version_path or VERSION_PATH

    def current(self) -> VersionInfo:
        if not self.version_path.exists():
            return VersionInfo(version="0.1.0")

        with self.version_path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        return VersionInfo(
            version=str(data.get("version", "0.1.0")),
            channel=str(data.get("channel", "stable")),
            build=str(data.get("build", "local")),
        )

    @staticmethod
    def is_newer(candidate: str, current: str) -> bool:
        def _parts(value: str) -> tuple[int, ...]:
            normalized = value.lstrip("v").split("-")[0].split("+")[0]
            return tuple(int(part) for part in normalized.split("."))

        return _parts(candidate) > _parts(current)

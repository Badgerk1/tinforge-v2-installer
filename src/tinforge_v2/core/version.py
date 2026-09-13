"""Version and build metadata."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from .constants import VERSION_PATH


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
        def _numeric_prefix(segment: str) -> int:
            match = re.match(r"(\d+)", segment)
            return int(match.group(1)) if match else 0

        def _parse(value: str) -> tuple[tuple[int, ...], tuple[str, ...]]:
            normalized = value.lstrip("v").split("+")[0]
            core, _, prerelease = normalized.partition("-")
            core_parts = tuple(_numeric_prefix(part) for part in core.split("."))
            prerelease_parts = tuple(segment for segment in prerelease.split(".") if segment) if prerelease else ()
            return core_parts, prerelease_parts

        def _compare_prerelease(left: tuple[str, ...], right: tuple[str, ...]) -> int:
            if not left and not right:
                return 0
            if not left:
                return 1
            if not right:
                return -1

            size = max(len(left), len(right))
            for index in range(size):
                if index >= len(left):
                    return -1
                if index >= len(right):
                    return 1
                l_value = left[index]
                r_value = right[index]
                if l_value == r_value:
                    continue
                l_is_num = l_value.isdigit()
                r_is_num = r_value.isdigit()
                if l_is_num and r_is_num:
                    return 1 if int(l_value) > int(r_value) else -1
                if l_is_num != r_is_num:
                    return -1 if l_is_num else 1
                return 1 if l_value > r_value else -1
            return 0

        candidate_core, candidate_pre = _parse(candidate)
        current_core, current_pre = _parse(current)
        width = max(len(candidate_core), len(current_core))
        padded_candidate = candidate_core + (0,) * (width - len(candidate_core))
        padded_current = current_core + (0,) * (width - len(current_core))
        if padded_candidate != padded_current:
            return padded_candidate > padded_current
        return _compare_prerelease(candidate_pre, current_pre) > 0

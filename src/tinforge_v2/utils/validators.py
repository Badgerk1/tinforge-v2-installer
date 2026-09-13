"""Input validators for file and project operations."""

from __future__ import annotations

from pathlib import Path

from ..core.constants import PROJECT_FILE_SUFFIX, SUPPORTED_SOURCE_EXTENSIONS


def is_supported_source(path: str | Path) -> bool:
    return Path(path).suffix.lower() in SUPPORTED_SOURCE_EXTENSIONS


def is_project_file(path: str | Path) -> bool:
    return str(path).lower().endswith(PROJECT_FILE_SUFFIX)

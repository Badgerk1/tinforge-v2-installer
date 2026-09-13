"""File helpers used by the GUI and project manager."""

from __future__ import annotations

from pathlib import Path


def safe_project_name(name: str) -> str:
    cleaned = "_".join(name.strip().split())
    return cleaned.lower() or "project"


def read_text_preview(path: str | Path, limit: int = 2000) -> str:
    file_path = Path(path)
    try:
        return file_path.read_text(encoding="utf-8", errors="replace")[:limit]
    except OSError:
        return "Preview unavailable."


def human_size(path: str | Path) -> str:
    size = Path(path).stat().st_size
    units = ["B", "KB", "MB", "GB"]
    value = float(size)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} {unit}"
        value /= 1024
    return f"{int(size)} B"

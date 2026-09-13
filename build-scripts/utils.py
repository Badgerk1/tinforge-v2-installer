"""Shared helpers for CI build scripts."""

from __future__ import annotations

import subprocess
from pathlib import Path


def run(command: list[str], cwd: Path | None = None) -> None:
    subprocess.run(command, cwd=cwd, check=True)


def ensure_file(path: Path, label: str) -> Path:
    if not path.is_file():
        raise FileNotFoundError(f"Expected {label} at: {path}")
    return path


def ensure_executable(path: Path) -> Path:
    path.chmod(path.stat().st_mode | 0o111)
    return path


def prepare_directory(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_placeholder(path: Path, text: str) -> Path:
    path.write_text(text, encoding="utf-8")
    return path

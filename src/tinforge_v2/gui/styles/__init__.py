"""Stylesheet loader helpers."""

from __future__ import annotations

from pathlib import Path

_ROOT = Path(__file__).resolve().parent

DARK_THEME = (_ROOT / "dark_theme.qss").read_text(encoding="utf-8")
LIGHT_THEME = (_ROOT / "light_theme.qss").read_text(encoding="utf-8")


def load_theme(name: str) -> str:
    return LIGHT_THEME if name == "light" else DARK_THEME

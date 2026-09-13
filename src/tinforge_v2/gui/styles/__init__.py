"""Stylesheet loader helpers."""

from __future__ import annotations

from importlib import resources


def _read_theme(name: str) -> str:
    return resources.files(__package__).joinpath(name).read_text(encoding="utf-8")


DARK_THEME = _read_theme("dark_theme.qss")
LIGHT_THEME = _read_theme("light_theme.qss")


def load_theme(name: str) -> str:
    return LIGHT_THEME if name == "light" else DARK_THEME

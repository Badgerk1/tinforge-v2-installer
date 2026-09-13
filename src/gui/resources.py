"""Resource helpers."""

from pathlib import Path

from src.core.constants import ROOT_DIR


class Resources:
    @staticmethod
    def branding_dir() -> Path:
        return ROOT_DIR / "build" / "branding"

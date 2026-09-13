"""Update installer logic."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class InstallResult:
    success: bool
    message: str


class UpdateInstaller:
    def install(self, package_path: str | Path) -> InstallResult:
        package = Path(package_path)
        if not package.exists():
            return InstallResult(False, "Update package not found")
        if package.suffix.lower() not in {".exe", ".dmg", ".appimage"}:
            return InstallResult(False, "Unsupported package format")
        return InstallResult(True, f"Ready to install {package.name}")

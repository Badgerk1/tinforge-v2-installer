"""Run all platform builders."""

from __future__ import annotations

import platform
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    system = platform.system().lower()
    if system == "windows":
        target = ROOT / "build" / "pyinstaller" / "build_windows.py"
    elif system == "darwin":
        target = ROOT / "build" / "pyinstaller" / "build_macos.py"
    else:
        target = ROOT / "build" / "pyinstaller" / "build_linux.py"

    subprocess.run(["python", str(target)], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

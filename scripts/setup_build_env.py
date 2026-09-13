"""Prepare local build environment."""

from __future__ import annotations

import platform
import subprocess
import sys


MIN_PYTHON = (3, 10)


def main() -> int:
    if sys.version_info < MIN_PYTHON:
        print("Python 3.10+ required")
        return 1

    print(f"Using Python {platform.python_version()}")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements-build.txt"], check=True)
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    print("Build environment ready")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

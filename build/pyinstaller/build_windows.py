"""Build Windows executable and NSIS installer."""

from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPEC = ROOT / "build" / "pyinstaller" / "tinforge_v2.spec"


def main() -> int:
    subprocess.run(["pyinstaller", str(SPEC), "--clean"], check=True)
    nsis = ROOT / "build" / "installers" / "windows" / "tinforge.nsi"
    if nsis.exists():
        subprocess.run(["makensis", str(nsis)], check=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

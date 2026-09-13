"""Build Linux executable and AppImage."""

from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPEC = ROOT / "build" / "pyinstaller" / "tinforge_v2.spec"


def main() -> int:
    subprocess.run(["pyinstaller", str(SPEC), "--clean"], check=True)
    appimage_script = ROOT / "build" / "installers" / "linux" / "build_appimage.sh"
    if appimage_script.exists():
        subprocess.run(["bash", str(appimage_script)], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

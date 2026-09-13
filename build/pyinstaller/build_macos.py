"""Build macOS application bundle and DMG."""

from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPEC = ROOT / "build" / "pyinstaller" / "tinforge_v2.spec"


def main() -> int:
    subprocess.run(["pyinstaller", str(SPEC), "--clean"], check=True)
    dmg_script = ROOT / "build" / "installers" / "macos" / "build_dmg.sh"
    if dmg_script.exists():
        subprocess.run(["bash", str(dmg_script)], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

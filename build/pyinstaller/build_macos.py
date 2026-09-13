"""Build macOS application bundle and DMG."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPEC = ROOT / "build" / "pyinstaller" / "tinforge_v2.spec"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build macOS artifacts")
    parser.add_argument("--version", default="0.1.0")
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    subprocess.run(["pyinstaller", str(SPEC), "--clean"], check=True)
    dmg_script = ROOT / "build" / "installers" / "macos" / "build_dmg.sh"
    if dmg_script.exists():
        subprocess.run(["bash", str(dmg_script)], check=True)
    print(f"Built macOS artifacts for version {args.version} in {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

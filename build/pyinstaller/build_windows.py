"""Build Windows executable and NSIS installer."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPEC = ROOT / "build" / "pyinstaller" / "tinforge_v2.spec"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Windows artifacts")
    parser.add_argument("--version", default="0.1.0")
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    subprocess.run(["pyinstaller", str(SPEC), "--clean"], check=True)
    nsis = ROOT / "build" / "installers" / "windows" / "tinforge.nsi"
    if nsis.exists():
        subprocess.run(["makensis", str(nsis)], check=False)
    print(f"Built Windows artifacts for version {args.version} in {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

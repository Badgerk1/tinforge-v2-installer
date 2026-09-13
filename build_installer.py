"""Main build entrypoint for TinForge v2 installers."""

from __future__ import annotations

import argparse
import platform
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build TinForge v2 installer")
    parser.add_argument("--platform", choices=["windows", "macos", "linux", "auto"], default="auto")
    parser.add_argument("--version", default="0.1.0")
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    return parser.parse_args()


def pick_builder(target: str) -> Path:
    if target == "auto":
        system = platform.system().lower()
        target = "macos" if system == "darwin" else system
    mapping = {
        "windows": ROOT / "build" / "pyinstaller" / "build_windows.py",
        "macos": ROOT / "build" / "pyinstaller" / "build_macos.py",
        "linux": ROOT / "build" / "pyinstaller" / "build_linux.py",
    }
    if target not in mapping:
        msg = f"Unsupported platform: {target}"
        raise ValueError(msg)
    builder = mapping[target]
    if not builder.exists():
        msg = f"Builder script not found: {builder}"
        raise FileNotFoundError(msg)
    return builder


def main() -> int:
    args = parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    builder = pick_builder(args.platform)
    subprocess.run(
        [sys.executable, str(builder), "--version", args.version, "--output", str(args.output)],
        check=True,
    )
    print(f"Build complete for {args.platform} {args.version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

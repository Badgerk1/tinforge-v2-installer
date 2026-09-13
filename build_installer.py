"""Main build entrypoint for TinForge v2 installers."""

from __future__ import annotations

import argparse
import platform
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SPEC = ROOT / "build" / "pyinstaller" / "tinforge_v2.spec"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build TinForge v2 installer")
    parser.add_argument("--platform", choices=["windows", "macos", "linux", "auto"], default="auto")
    parser.add_argument("--version", default="0.1.0")
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    return parser.parse_args()


def resolve_platform(target: str) -> str:
    if target != "auto":
        return target

    system = platform.system().lower()
    if system == "darwin":
        return "macos"
    if system in {"windows", "linux"}:
        return system

    msg = f"Unsupported host platform: {system}"
    raise ValueError(msg)


def run_pyinstaller() -> None:
    subprocess.run(["pyinstaller", str(SPEC), "--clean"], check=True)


def build_windows() -> None:
    run_pyinstaller()
    nsis = ROOT / "build" / "installers" / "windows" / "tinforge.nsi"
    if nsis.exists():
        subprocess.run(["makensis", str(nsis)], check=True)


def build_macos() -> None:
    run_pyinstaller()
    dmg_script = ROOT / "build" / "installers" / "macos" / "build_dmg.sh"
    if dmg_script.exists():
        subprocess.run(["bash", str(dmg_script)], check=True)


def build_linux() -> None:
    run_pyinstaller()
    appimage_script = ROOT / "build" / "installers" / "linux" / "build_appimage.sh"
    if appimage_script.exists():
        subprocess.run(["bash", str(appimage_script)], check=True)


def main() -> int:
    args = parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    selected = resolve_platform(args.platform)
    builders = {
        "windows": build_windows,
        "macos": build_macos,
        "linux": build_linux,
    }
    builders[selected]()
    print(f"Build complete for {selected} {args.version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

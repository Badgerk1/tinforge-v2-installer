"""Main build entrypoint for TinForge v2 installers."""

from __future__ import annotations

import argparse
import os
import platform
import subprocess
from pathlib import Path
from shutil import copy2

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
    raise ValueError(f"Unsupported host platform: {system}")


def run_pyinstaller(output_dir: Path) -> None:
    env = os.environ.copy()
    env["PYINSTALLER_DISTPATH"] = str(output_dir)
    env["PYTHONPATH"] = os.pathsep.join(filter(None, [str(ROOT / "src"), env.get("PYTHONPATH", "")]))
    subprocess.run(["pyinstaller", str(SPEC), "--clean", "--noconfirm"], check=True, cwd=ROOT, env=env)


def build_windows(output_dir: Path) -> None:
    run_pyinstaller(output_dir)
    nsis = ROOT / "build" / "installers" / "windows" / "tinforge.nsi"
    if nsis.exists():
        subprocess.run(["makensis", str(nsis)], check=True, cwd=ROOT)


def build_macos(output_dir: Path) -> None:
    run_pyinstaller(output_dir)
    dmg_script = ROOT / "build" / "installers" / "macos" / "build_dmg.sh"
    if dmg_script.exists():
        subprocess.run(["bash", str(dmg_script)], check=True, cwd=ROOT)


def build_linux(output_dir: Path) -> None:
    run_pyinstaller(output_dir)
    appimage_script = ROOT / "build" / "installers" / "linux" / "build_appimage.sh"
    if appimage_script.exists():
        subprocess.run(["bash", str(appimage_script)], check=True, cwd=ROOT)

    artifact = output_dir / "TinForge-v2.AppImage"
    if not artifact.exists():
        raise FileNotFoundError(f"Expected Linux AppImage at: {artifact}")


def stamp_artifacts(output_dir: Path, version: str) -> None:
    for artifact in list(output_dir.glob("*")):
        if not artifact.is_file():
            continue
        stamped = output_dir / f"{artifact.stem}-{version}{artifact.suffix}"
        if stamped != artifact:
            copy2(artifact, stamped)


def main() -> int:
    args = parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    builders = {
        "windows": build_windows,
        "macos": build_macos,
        "linux": build_linux,
    }
    selected = resolve_platform(args.platform)
    builders[selected](args.output)
    stamp_artifacts(args.output, args.version)
    print(f"Build complete for {selected} {args.version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Build macOS installer"""

import argparse
import os
import shutil
import sys

from utils import check_file_exists, check_python_version, run_command


ARTIFACT_PATH = ".artifacts/TinForge-v2-macos"


def parse_args():
    parser = argparse.ArgumentParser(description="Build macOS installer")
    parser.add_argument("--skip-build", action="store_true")
    parser.add_argument("--smoke-test", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()

    os.makedirs(".artifacts", exist_ok=True)

    if args.smoke_test:
        with open(ARTIFACT_PATH, "w", encoding="utf-8") as artifact:
            artifact.write("macos-smoke-artifact")
        print(f"✓ Smoke artifact created: {ARTIFACT_PATH}")
        return 0

    print("=" * 60)
    print("Building TinForge v2 - macOS Installer")
    print("=" * 60)

    if not check_python_version():
        return 1

    if not run_command([sys.executable, "-c", "import PyQt5"]):
        print("ERROR: PyQt5 is not installed")
        return 1

    if not run_command([sys.executable, "-m", "PyInstaller", "--version"]):
        print("ERROR: PyInstaller is not installed")
        return 1

    spec_file = "build/pyinstaller/tinforge_v2.spec"
    if not check_file_exists(spec_file, "PyInstaller spec file"):
        return 1

    if not check_file_exists("src/tinforge_v2/main.py", "Application entry point"):
        return 1

    if not args.skip_build:
        print("\nRunning PyInstaller...")
        if not run_command(
            [
                sys.executable,
                "-m",
                "PyInstaller",
                spec_file,
                "--clean",
                "--onefile",
            ]
        ):
            print("ERROR: PyInstaller failed")
            return 1

    app_file = "dist/TinForge-v2"
    if not check_file_exists(app_file, "Built executable"):
        return 1

    shutil.copy2(app_file, ARTIFACT_PATH)
    if not check_file_exists(ARTIFACT_PATH, "Staged installer artifact"):
        return 1

    print("\n" + "=" * 60)
    print("✓ macOS build succeeded!")
    print(f"  Installer: {ARTIFACT_PATH}")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())

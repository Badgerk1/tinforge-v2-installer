"""Build Linux installer"""

import argparse
import os
import shutil
import sys

from utils import check_file_exists, check_python_version, run_command


ARTIFACT_PATH = ".artifacts/TinForge-v2.AppImage"
BUILT_INSTALLER_PATH = "dist/TinForge-v2.AppImage"


def parse_args():
    parser = argparse.ArgumentParser(description="Build Linux installer")
    parser.add_argument("--skip-build", action="store_true")
    parser.add_argument("--smoke-test", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()

    os.makedirs(".artifacts", exist_ok=True)

    if args.smoke_test:
        with open(ARTIFACT_PATH, "w", encoding="utf-8") as artifact:
            artifact.write("linux-smoke-artifact")
        print(f"✓ Smoke artifact created: {ARTIFACT_PATH}")
        return 0

    print("=" * 60)
    print("Building TinForge v2 - Linux Installer")
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
        print("\nRunning installer build...")
        if not run_command(
            [
                sys.executable,
                "build_installer.py",
                "--platform",
                "linux",
                "--output",
                "dist",
            ]
        ):
            print("ERROR: Installer build failed")
            return 1

    if not check_file_exists(BUILT_INSTALLER_PATH, "Built installer"):
        return 1

    shutil.copy2(BUILT_INSTALLER_PATH, ARTIFACT_PATH)
    mode = os.stat(ARTIFACT_PATH).st_mode
    os.chmod(ARTIFACT_PATH, mode | 0o111)
    if not check_file_exists(ARTIFACT_PATH, "Staged installer artifact"):
        return 1

    print("\n" + "=" * 60)
    print("✓ Linux build succeeded!")
    print(f"  Installer: {ARTIFACT_PATH}")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())

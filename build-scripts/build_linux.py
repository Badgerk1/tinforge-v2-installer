"""Linux installer build orchestrator."""

from __future__ import annotations

import argparse
import shutil

from config import ARTIFACTS_DIR, DIST_DIR, EXPECTED_ARTIFACTS, ROOT_DIR
from utils import ensure_executable, ensure_file, prepare_directory, run, write_placeholder


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Linux installer")
    parser.add_argument("--skip-build", action="store_true", help="Skip running build_installer.py")
    parser.add_argument("--smoke-test", action="store_true", help="Allow placeholder artifact generation")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    prepare_directory(ARTIFACTS_DIR)

    if not args.skip_build:
        run(["python", "build_installer.py", "--platform", "linux"], cwd=ROOT_DIR)

    expected_name = EXPECTED_ARTIFACTS["linux"]
    source = DIST_DIR / expected_name
    binary_fallback = DIST_DIR / "tinforge-v2" / "tinforge-v2"
    destination = ARTIFACTS_DIR / expected_name

    if source.is_file():
        shutil.copy2(source, destination)
    elif binary_fallback.is_file():
        shutil.copy2(binary_fallback, destination)
    elif args.smoke_test:
        write_placeholder(destination, "linux-smoke-artifact")
    else:
        ensure_file(source, "Linux AppImage")

    ensure_executable(destination)
    ensure_file(destination, "Linux artifact")
    print(f"Created {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

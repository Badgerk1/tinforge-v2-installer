"""macOS installer build orchestrator."""

from __future__ import annotations

import argparse
import shutil

from config import ARTIFACTS_DIR, DIST_DIR, EXPECTED_ARTIFACTS, ROOT_DIR
from utils import ensure_file, prepare_directory, run, write_placeholder


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build macOS installer")
    parser.add_argument("--skip-build", action="store_true", help="Skip running build_installer.py")
    parser.add_argument("--smoke-test", action="store_true", help="Allow placeholder artifact generation")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    prepare_directory(ARTIFACTS_DIR)

    if not args.skip_build:
        run(["python", "build_installer.py", "--platform", "macos"], cwd=ROOT_DIR)

    expected_name = EXPECTED_ARTIFACTS["macos"]
    source = DIST_DIR / expected_name
    destination = ARTIFACTS_DIR / expected_name

    if source.is_file():
        shutil.copy2(source, destination)
    elif args.smoke_test:
        write_placeholder(destination, "macos-smoke-artifact")
    else:
        ensure_file(source, "macOS installer")

    ensure_file(destination, "macOS artifact")
    print(f"Created {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

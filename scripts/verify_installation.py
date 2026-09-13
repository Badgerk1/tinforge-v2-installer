"""Verify a built installer directory contains expected files."""

from __future__ import annotations

import argparse
from pathlib import Path


REQUIRED = ["config", "resources"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify installer payload")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()

    missing = [name for name in REQUIRED if not (args.path / name).exists()]
    if missing:
        print(f"Missing required items: {', '.join(missing)}")
        return 1

    print("Installation payload verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

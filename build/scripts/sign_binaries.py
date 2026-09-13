"""Optional code-signing helper."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Sign build artifacts")
    parser.add_argument("artifact", type=Path)
    args = parser.parse_args()

    if not args.artifact.exists():
        print(f"Artifact not found: {args.artifact}")
        return 1

    print(f"Signing placeholder for {args.artifact}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

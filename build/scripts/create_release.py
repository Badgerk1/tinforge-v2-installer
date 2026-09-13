"""Create a GitHub release using gh CLI."""

from __future__ import annotations

import argparse
import subprocess


def main() -> int:
    parser = argparse.ArgumentParser(description="Create release")
    parser.add_argument("tag")
    parser.add_argument("--title", default="TinForge v2 release")
    parser.add_argument("--notes", default="Automated installer release")
    args = parser.parse_args()

    subprocess.run(["gh", "release", "create", args.tag, "--title", args.title, "--notes", args.notes], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

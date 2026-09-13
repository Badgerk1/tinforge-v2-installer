"""Release metadata creator for installer artifacts."""

from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
from pathlib import Path

from config import ARTIFACTS_DIR, EXPECTED_ARTIFACTS


def sha256sum(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def collect_artifacts(directory: Path) -> list[Path]:
    required = [directory / name for name in EXPECTED_ARTIFACTS.values()]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"Missing expected artifacts: {', '.join(missing)}")
    return required


def collect_commit_summaries(limit: int = 10) -> list[str]:
    try:
        output = subprocess.check_output(
            ["git", "log", f"--pretty=format:%h %s", f"-n{limit}"],
            text=True,
        ).strip()
    except Exception:
        return []
    return [line for line in output.splitlines() if line]


def build_release_notes(version: str, artifacts: list[Path], checksums: dict[str, str]) -> str:
    lines = [
        f"# TinForge v2 {version}",
        "",
        "## Downloads",
    ]
    lines.extend([f"- `{artifact.name}`" for artifact in artifacts])
    lines.extend([
        "",
        "## SHA256 Checksums",
    ])
    lines.extend([f"- `{name}`: `{value}`" for name, value in checksums.items()])

    commits = collect_commit_summaries()
    lines.extend(["", "## Recent Commits"])
    if commits:
        lines.extend([f"- {line}" for line in commits])
    else:
        lines.append("- Commit history unavailable in this environment.")

    lines.extend([
        "",
        "## Installation",
        "- Windows: run `TinForge-v2-Setup.exe`",
        "- macOS: open `TinForge-v2.dmg`",
        "- Linux: `chmod +x TinForge-v2.AppImage && ./TinForge-v2.AppImage`",
    ])
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create release notes and checksums")
    parser.add_argument("--artifacts-dir", type=Path, default=ARTIFACTS_DIR)
    parser.add_argument("--checksums-file", type=Path, default=ARTIFACTS_DIR / "SHA256SUMS.txt")
    parser.add_argument("--notes-file", type=Path, default=ARTIFACTS_DIR / "RELEASE_NOTES.md")
    parser.add_argument("--version", default=os.getenv("GITHUB_REF_NAME", "local-build"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    artifacts = collect_artifacts(args.artifacts_dir)
    checksums = {artifact.name: sha256sum(artifact) for artifact in artifacts}

    args.checksums_file.write_text(
        "".join(f"{value}  {name}\n" for name, value in checksums.items()),
        encoding="utf-8",
    )

    notes = build_release_notes(args.version, artifacts, checksums)
    args.notes_file.write_text(notes, encoding="utf-8")

    print(f"Wrote {args.checksums_file}")
    print(f"Wrote {args.notes_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

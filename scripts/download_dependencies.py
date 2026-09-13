"""Pre-download Python dependencies for offline build cache."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    cache_dir = Path(".cache/wheels")
    cache_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run([sys.executable, "-m", "pip", "download", "-r", "requirements.txt", "-d", str(cache_dir)], check=True)
    print(f"Downloaded dependencies to {cache_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

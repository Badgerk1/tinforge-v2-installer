"""Check for updates from GitHub releases."""

from __future__ import annotations

import json
from dataclasses import dataclass
from urllib.error import URLError
from urllib.request import urlopen

from src.core.version import VersionManager


@dataclass(frozen=True)
class UpdateInfo:
    version: str
    url: str
    notes: str


class UpdateChecker:
    def __init__(self, repo: str = "Badgerk1/tinforge-v2-installer") -> None:
        self.repo = repo

    def check(self, current_version: str) -> UpdateInfo | None:
        endpoint = f"https://api.github.com/repos/{self.repo}/releases/latest"
        try:
            with urlopen(endpoint, timeout=5) as response:  # noqa: S310
                payload = json.loads(response.read().decode("utf-8"))
        except URLError:
            return None

        candidate = str(payload.get("tag_name", "")).lstrip("v")
        if not candidate:
            return None

        if VersionManager.is_newer(candidate, current_version):
            return UpdateInfo(
                version=candidate,
                url=str(payload.get("html_url", "")),
                notes=str(payload.get("body", "")).strip(),
            )
        return None

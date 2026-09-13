"""Release notes formatter."""

from __future__ import annotations


def render_changelog(version: str, notes: str) -> str:
    clean_notes = notes.strip() or "No release notes provided."
    return f"TinForge v2 {version}\n\n{clean_notes}"

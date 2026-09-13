"""Application controller and workflow coordinator."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from src.core.config import ConfigManager
from src.core.constants import DEFAULT_EXPORT_FORMATS
from src.core.version import VersionManager


@dataclass
class Project:
    name: str
    source_files: list[Path] = field(default_factory=list)


class AppManager:
    """Coordinates project state and export requests."""

    def __init__(self, config: ConfigManager | None = None, version: VersionManager | None = None) -> None:
        self.config = config or ConfigManager()
        self.version = version or VersionManager()
        self.settings = self.config.load()
        self.current_project: Project | None = None

    def create_project(self, name: str) -> Project:
        self.current_project = Project(name=name)
        return self.current_project

    def open_project(self, name: str, sources: Iterable[str | Path]) -> Project:
        project = Project(name=name, source_files=[Path(p) for p in sources])
        self.current_project = project
        return project

    def export(self, output_dir: str | Path, formats: Iterable[str] | None = None) -> list[Path]:
        if self.current_project is None:
            msg = "No project loaded"
            raise RuntimeError(msg)

        selected_formats = list(formats or self.settings.get("default_export_formats") or DEFAULT_EXPORT_FORMATS)
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        generated: list[Path] = []
        safe_name = self.current_project.name.replace(" ", "_").lower()
        for fmt in selected_formats:
            ext = fmt.lower().replace("landxml", "xml")
            output_file = out_dir / f"{safe_name}.{ext}"
            output_file.write_text(f"TinForge export placeholder for {fmt}\n", encoding="utf-8")
            generated.append(output_file)
        return generated

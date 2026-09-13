"""Project management for the installer GUI."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable

from ..utils.file_utils import safe_project_name
from ..utils.validators import is_project_file
from .config import ConfigManager
from .constants import DEFAULT_EXPORT_FORMATS, PROJECT_FILE_SUFFIX, RECENT_PROJECTS_LIMIT

EXTENSION_MAP = {
    "TP3": "tp3",
    "DBX": "dbx",
    "LandXML": "xml",
    "DXF": "dxf",
    "CSV": "csv",
}


@dataclass
class Project:
    name: str
    source_files: list[Path] = field(default_factory=list)
    metadata: dict[str, str] = field(default_factory=dict)
    project_path: Path | None = None

    def as_serializable(self) -> dict[str, object]:
        payload = asdict(self)
        payload["source_files"] = [str(path) for path in self.source_files]
        payload["project_path"] = str(self.project_path) if self.project_path else None
        return payload


class ProjectManager:
    """Create, load, save, and export installer projects."""

    def __init__(self, config: ConfigManager | None = None, settings: dict | None = None) -> None:
        self.config = config or ConfigManager()
        self.settings = settings or self.config.load()
        self.current_project: Project | None = None

    def create_project(self, name: str) -> Project:
        self.current_project = Project(name=name.strip() or "Untitled Project")
        return self.current_project

    def import_files(self, name: str, sources: Iterable[str | Path]) -> Project:
        files = [Path(path) for path in sources]
        self.current_project = Project(name=name.strip() or "Imported Project", source_files=files)
        return self.current_project

    def save_project(self, path: str | Path) -> Path:
        if self.current_project is None:
            raise RuntimeError("No project loaded")

        target = Path(path)
        if not str(target).lower().endswith(PROJECT_FILE_SUFFIX.lower()):
            target = target.with_suffix("")
            target = target.parent / f"{target.name}{PROJECT_FILE_SUFFIX}"
        target.parent.mkdir(parents=True, exist_ok=True)
        self.current_project.project_path = target
        target.write_text(json.dumps(self.current_project.as_serializable(), indent=2), encoding="utf-8")
        self._remember_project(target)
        return target

    def load_project(self, path: str | Path) -> Project:
        target = Path(path)
        if not is_project_file(target):
            raise ValueError(f"Unsupported project file: {target}")
        payload = json.loads(target.read_text(encoding="utf-8"))
        project = Project(
            name=str(payload.get("name", target.stem)),
            source_files=[Path(item) for item in payload.get("source_files", [])],
            metadata=dict(payload.get("metadata", {})),
            project_path=target,
        )
        self.current_project = project
        self._remember_project(target)
        return project

    def export(self, output_dir: str | Path, formats: Iterable[str] | None = None) -> list[Path]:
        if self.current_project is None:
            raise RuntimeError("No project loaded")

        selected_formats = list(formats or self.settings.get("default_export_formats") or DEFAULT_EXPORT_FORMATS)
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        generated: list[Path] = []
        safe_name = safe_project_name(self.current_project.name)
        for fmt in selected_formats:
            ext = EXTENSION_MAP.get(fmt, fmt.lower())
            output_file = out_dir / f"{safe_name}.{ext}"
            output_file.write_text(
                f"TinForge export placeholder for {fmt}\nSources: {len(self.current_project.source_files)}\n",
                encoding="utf-8",
            )
            generated.append(output_file)
        return generated

    def recent_projects(self) -> list[str]:
        return list(self.settings.get("recent_projects") or [])

    def _remember_project(self, path: Path) -> None:
        recent = [str(path)]
        recent.extend(item for item in self.recent_projects() if item != str(path))
        self.settings["recent_projects"] = recent[:RECENT_PROJECTS_LIMIT]
        self.config.save(self.settings)

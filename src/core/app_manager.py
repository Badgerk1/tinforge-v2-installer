"""Application controller and workflow coordinator."""

from __future__ import annotations

from typing import Iterable

from src.tinforge_v2.core.config import ConfigManager
from src.tinforge_v2.core.project import Project, ProjectManager
from src.tinforge_v2.core.version import VersionManager


class AppManager:
    """Coordinates project state and export requests."""

    def __init__(self, config: ConfigManager | None = None, version: VersionManager | None = None) -> None:
        self.config = config or ConfigManager()
        self.version = version or VersionManager()
        self.settings = self.config.load()
        self.project_manager = ProjectManager(config=self.config, settings=self.settings)

    @property
    def current_project(self) -> Project | None:
        return self.project_manager.current_project

    def create_project(self, name: str) -> Project:
        return self.project_manager.create_project(name)

    def open_project(self, name: str, sources: Iterable[str]) -> Project:
        return self.project_manager.import_files(name, sources)

    def export(self, output_dir, formats=None):
        self.project_manager.settings = self.settings
        return self.project_manager.export(output_dir, formats)

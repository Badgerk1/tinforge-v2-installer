from pathlib import Path

from src.core.app_manager import AppManager
from src.core.config import ConfigManager


def test_export_requires_project(tmp_path: Path):
    manager = AppManager(config=ConfigManager(settings_path=tmp_path / "settings.json"))
    try:
        manager.export(tmp_path)
    except RuntimeError as exc:
        assert "No project" in str(exc)
    else:
        raise AssertionError("Expected RuntimeError")


def test_export_creates_files(tmp_path: Path):
    manager = AppManager(config=ConfigManager(settings_path=tmp_path / "settings.json"))
    manager.create_project("Demo")
    files = manager.export(tmp_path / "out", ["TP3", "CSV"])
    assert len(files) == 2
    assert all(file.exists() for file in files)

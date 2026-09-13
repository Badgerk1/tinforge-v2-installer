from pathlib import Path

from src.tinforge_v2.core.config import ConfigManager
from src.tinforge_v2.core.project import ProjectManager
from src.tinforge_v2.gui.styles import DARK_THEME, LIGHT_THEME


def test_config_manager_persists_recent_projects(tmp_path: Path):
    config = ConfigManager(settings_path=tmp_path / "settings.json")
    settings = config.load()
    settings["recent_projects"] = ["alpha"]
    config.save(settings)

    reloaded = config.load()
    assert reloaded["recent_projects"] == ["alpha"]
    assert reloaded["default_export_dir"]


def test_project_manager_saves_and_loads_project(tmp_path: Path):
    config = ConfigManager(settings_path=tmp_path / "settings.json")
    manager = ProjectManager(config=config, settings=config.load())
    source = tmp_path / "sample.csv"
    source.write_text("x,y\n1,2\n", encoding="utf-8")

    manager.import_files("Demo Project", [source])
    saved_path = manager.save_project(tmp_path / "demo")

    loaded = manager.load_project(saved_path)
    assert loaded.name == "Demo Project"
    assert loaded.source_files == [source]
    assert str(saved_path) in manager.recent_projects()


def test_stylesheets_cover_both_themes():
    assert "QMainWindow" in DARK_THEME
    assert "QMainWindow" in LIGHT_THEME

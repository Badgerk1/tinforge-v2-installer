from pathlib import Path
import importlib.resources
import sys

from src.tinforge_v2.core.config import ConfigManager
from src.tinforge_v2.core.project import ProjectManager
from src.tinforge_v2.core.version import VersionManager
from src.tinforge_v2.gui.styles import DARK_THEME, LIGHT_THEME, load_theme
from src.tinforge_v2.utils.logger import setup_logger


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
    assert load_theme("light") == LIGHT_THEME
    assert load_theme("anything-else") == DARK_THEME


def test_version_manager_handles_prerelease_and_non_numeric_segments():
    assert VersionManager.is_newer("1.0.1", "1.0.0") is True
    assert VersionManager.is_newer("1.0.0-rc2", "1.0.0-rc1") is True
    assert VersionManager.is_newer("1.0.0", "1.0.0-rc1") is True
    assert VersionManager.is_newer("1.0rc1", "1.0.0") is False
    assert VersionManager.is_newer("1.0rc2", "1.0rc1") is True
    assert VersionManager.is_newer("1.0rc2", "1.0-rc1") is True
    assert VersionManager.is_newer("1.0rc10", "1.0rc2") is True


def test_package_assets_are_discoverable():
    styles_root = importlib.resources.files("src.tinforge_v2.gui.styles")
    assets_root = importlib.resources.files("src.tinforge_v2")
    assert (styles_root / "dark_theme.qss").is_file()
    assert (styles_root / "light_theme.qss").is_file()
    assert (assets_root / "assets" / "icons" / "app.png").is_file()
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
    installed_styles_root = importlib.resources.files("tinforge_v2.gui.styles")
    installed_assets_root = importlib.resources.files("tinforge_v2")
    assert (installed_styles_root / "dark_theme.qss").is_file()
    assert (installed_assets_root / "assets" / "icons" / "app.png").is_file()


def test_setup_logger_reuses_existing_file_handler():
    logger = setup_logger("tinforge_test_reuse", "DEBUG")
    logger = setup_logger("tinforge_test_reuse", "ERROR")
    assert logger.level > 0
    assert len([handler for handler in logger.handlers if getattr(handler, "baseFilename", "").endswith("tinforge-v2.log")]) == 1

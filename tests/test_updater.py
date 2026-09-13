from src.updater.changelog import render_changelog
from src.updater.update_installer import UpdateInstaller


def test_render_changelog_has_version():
    text = render_changelog("1.2.3", "Added updates")
    assert "1.2.3" in text
    assert "Added updates" in text


def test_update_installer_rejects_unknown_extension(tmp_path):
    file = tmp_path / "update.zip"
    file.write_text("x", encoding="utf-8")
    result = UpdateInstaller().install(file)
    assert result.success is False


def test_update_installer_accepts_supported_package(tmp_path):
    file = tmp_path / "update.exe"
    file.write_text("x", encoding="utf-8")
    result = UpdateInstaller().install(file)
    assert result.success is True


def test_update_installer_rejects_missing_package(tmp_path):
    result = UpdateInstaller().install(tmp_path / "missing.exe")
    assert result.success is False

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

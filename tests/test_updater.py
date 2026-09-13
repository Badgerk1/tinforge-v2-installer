import json

from src.updater.changelog import render_changelog
from src.updater.update_checker import UpdateChecker
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
    assert result.message == "Unsupported package format"


def test_update_installer_accepts_supported_package(tmp_path):
    file = tmp_path / "update.exe"
    file.write_text("x", encoding="utf-8")
    result = UpdateInstaller().install(file)
    assert result.success is True
    assert "update.exe" in result.message


def test_update_installer_accepts_dmg_and_appimage(tmp_path):
    dmg = tmp_path / "update.dmg"
    dmg.write_text("x", encoding="utf-8")
    appimage = tmp_path / "update.appimage"
    appimage.write_text("x", encoding="utf-8")

    dmg_result = UpdateInstaller().install(dmg)
    appimage_result = UpdateInstaller().install(appimage)
    assert dmg_result.success is True
    assert appimage_result.success is True
    assert "update.dmg" in dmg_result.message
    assert "update.appimage" in appimage_result.message


def test_update_installer_rejects_missing_package(tmp_path):
    result = UpdateInstaller().install(tmp_path / "missing.exe")
    assert result.success is False
    assert result.message == "Update package not found"


def test_update_checker_returns_none_on_failure(monkeypatch):
    def _boom(*_args, **_kwargs):
        raise TimeoutError("network issue")

    monkeypatch.setattr("src.updater.update_checker.urlopen", _boom)
    assert UpdateChecker().check("1.0.0") is None


def test_update_checker_selects_platform_asset(monkeypatch):
    payload = {
        "tag_name": "v1.0.1",
        "html_url": "https://example.com/release",
        "body": "notes",
        "assets": [
            {"name": "TinForge-v2.dmg", "browser_download_url": "https://example.com/macos.dmg"},
            {"name": "TinForge-v2.exe", "browser_download_url": "https://example.com/windows.exe"},
        ],
    }

    class _Response:
        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

        def read(self):
            return json.dumps(payload).encode("utf-8")

    monkeypatch.setattr("src.updater.update_checker.urlopen", lambda *_args, **_kwargs: _Response())
    monkeypatch.setattr("src.updater.update_checker.platform.system", lambda: "Windows")

    update = UpdateChecker().check("1.0.0")
    assert update is not None
    assert update.url.endswith(".exe")

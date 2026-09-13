from pathlib import Path

import pytest

import build_installer


def test_ensure_prerequisites_requires_pyinstaller(monkeypatch):
    monkeypatch.setattr(build_installer, "which", lambda _name: None)
    with pytest.raises(RuntimeError, match="PyInstaller is not installed"):
        build_installer.ensure_prerequisites()


def test_build_linux_uses_output_dir_for_packaging(monkeypatch, tmp_path):
    output_dir = tmp_path / "dist-out"
    output_dir.mkdir()
    artifact = output_dir / "TinForge-v2.AppImage"
    artifact.write_text("appimage", encoding="utf-8")

    monkeypatch.setattr(build_installer, "run_pyinstaller", lambda _output_dir: None)
    script = tmp_path / "build" / "installers" / "linux" / "build_appimage.sh"
    script.parent.mkdir(parents=True)
    script.write_text("#!/usr/bin/env bash\n", encoding="utf-8")

    calls = []

    def fake_run(command, check, cwd, env):
        calls.append((command, check, cwd, env))

    monkeypatch.setattr(build_installer.subprocess, "run", fake_run)
    monkeypatch.setattr(build_installer, "ROOT", tmp_path)

    build_installer.build_linux(output_dir)

    assert calls[0][0] == ["bash", str(script)]
    assert calls[0][3]["DIST_DIR"] == str(output_dir)


def test_build_macos_uses_output_dir_for_packaging(monkeypatch, tmp_path):
    output_dir = tmp_path / "dist-out"
    output_dir.mkdir()
    artifact = output_dir / "TinForge-v2.dmg"
    artifact.write_text("dmg", encoding="utf-8")

    monkeypatch.setattr(build_installer, "run_pyinstaller", lambda _output_dir: None)
    script = tmp_path / "build" / "installers" / "macos" / "build_dmg.sh"
    script.parent.mkdir(parents=True)
    script.write_text("#!/usr/bin/env bash\n", encoding="utf-8")

    calls = []

    def fake_run(command, check, cwd, env):
        calls.append((command, check, cwd, env))

    monkeypatch.setattr(build_installer.subprocess, "run", fake_run)
    monkeypatch.setattr(build_installer, "ROOT", tmp_path)

    build_installer.build_macos(output_dir)

    assert calls[0][0] == ["bash", str(script)]
    assert calls[0][3]["DIST_DIR"] == str(output_dir)


def test_build_windows_copies_nsis_output_to_output_dir(monkeypatch, tmp_path):
    output_dir = tmp_path / "dist-out"
    output_dir.mkdir()
    installer = tmp_path / "TinForge-v2-Setup.exe"
    installer.write_text("exe", encoding="utf-8")

    monkeypatch.setattr(build_installer, "run_pyinstaller", lambda _output_dir: None)
    monkeypatch.setattr(build_installer, "ROOT", tmp_path)
    monkeypatch.setattr(build_installer.subprocess, "run", lambda *_args, **_kwargs: None)

    build_installer.build_windows(output_dir)
    copied = output_dir / "TinForge-v2-Setup.exe"
    assert copied.is_file()
    assert copied.read_text(encoding="utf-8") == "exe"


def test_build_windows_fails_when_installer_missing(monkeypatch, tmp_path):
    output_dir = tmp_path / "dist-out"
    output_dir.mkdir()

    monkeypatch.setattr(build_installer, "run_pyinstaller", lambda _output_dir: None)
    monkeypatch.setattr(build_installer, "ROOT", tmp_path)
    monkeypatch.setattr(build_installer.subprocess, "run", lambda *_args, **_kwargs: None)

    with pytest.raises(FileNotFoundError, match="Expected Windows installer"):
        build_installer.build_windows(output_dir)

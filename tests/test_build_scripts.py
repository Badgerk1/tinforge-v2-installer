from pathlib import Path
from types import SimpleNamespace

import pytest


@pytest.fixture
def release_module(monkeypatch):
    import importlib.util

    scripts_dir = Path(__file__).resolve().parents[1] / "build-scripts"
    module_path = scripts_dir / "create_release.py"
    monkeypatch.syspath_prepend(str(scripts_dir))
    spec = importlib.util.spec_from_file_location("create_release", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def windows_build_module(monkeypatch):
    import importlib.util

    scripts_dir = Path(__file__).resolve().parents[1] / "build-scripts"
    module_path = scripts_dir / "build_windows.py"
    monkeypatch.syspath_prepend(str(scripts_dir))
    spec = importlib.util.spec_from_file_location("build_windows", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_sha256sum_returns_hash(release_module, tmp_path):
    sample = tmp_path / "sample.bin"
    sample.write_bytes(b"tinforge")

    result = release_module.sha256sum(sample)
    assert len(result) == 64


def test_collect_artifacts_requires_all_expected(release_module, tmp_path):
    (tmp_path / "TinForge-v2-Setup.exe").write_text("x", encoding="utf-8")
    (tmp_path / "TinForge-v2.dmg").write_text("x", encoding="utf-8")

    with pytest.raises(FileNotFoundError):
        release_module.collect_artifacts(tmp_path)


def test_build_release_notes_contains_sections(release_module, tmp_path):
    artifacts = [
        tmp_path / "TinForge-v2-Setup.exe",
        tmp_path / "TinForge-v2.dmg",
        tmp_path / "TinForge-v2.AppImage",
    ]
    for artifact in artifacts:
        artifact.write_text("x", encoding="utf-8")

    checksums = {artifact.name: "abc123" for artifact in artifacts}
    notes = release_module.build_release_notes("v1.2.3", artifacts, checksums)

    assert "TinForge v2 v1.2.3" in notes
    assert "SHA256 Checksums" in notes
    assert "TinForge-v2.AppImage" in notes


def test_build_release_notes_includes_recent_commits(release_module, tmp_path, monkeypatch):
    artifacts = [
        tmp_path / "TinForge-v2-Setup.exe",
        tmp_path / "TinForge-v2.dmg",
        tmp_path / "TinForge-v2.AppImage",
    ]
    for artifact in artifacts:
        artifact.write_text("x", encoding="utf-8")

    monkeypatch.setattr(release_module, "collect_commit_summaries", lambda *_args, **_kwargs: ["abc123 Add CI"])
    notes = release_module.build_release_notes("v1.2.3", artifacts, {artifact.name: "abc123" for artifact in artifacts})
    assert "## Recent Commits" in notes
    assert "- abc123 Add CI" in notes


def test_build_release_notes_handles_missing_commit_history(release_module, tmp_path, monkeypatch):
    artifacts = [
        tmp_path / "TinForge-v2-Setup.exe",
        tmp_path / "TinForge-v2.dmg",
        tmp_path / "TinForge-v2.AppImage",
    ]
    for artifact in artifacts:
        artifact.write_text("x", encoding="utf-8")

    monkeypatch.setattr(release_module, "collect_commit_summaries", lambda *_args, **_kwargs: [])
    notes = release_module.build_release_notes("v1.2.3", artifacts, {artifact.name: "abc123" for artifact in artifacts})
    assert "## Recent Commits" in notes
    assert "Commit history unavailable in this environment." in notes


def test_windows_build_non_smoke_copies_expected_artifact(windows_build_module, tmp_path, monkeypatch):
    root_dir = tmp_path / "repo"
    root_dir.mkdir()
    artifact_dir = tmp_path / "artifacts"
    source = root_dir / "TinForge-v2-Setup.exe"
    source.write_text("binary", encoding="utf-8")

    monkeypatch.setattr(
        windows_build_module,
        "parse_args",
        lambda: SimpleNamespace(skip_build=True, smoke_test=False),
    )
    monkeypatch.setattr(windows_build_module, "ROOT_DIR", root_dir)
    monkeypatch.setattr(windows_build_module, "ARTIFACTS_DIR", artifact_dir)

    result = windows_build_module.main()
    destination = artifact_dir / "TinForge-v2-Setup.exe"

    assert result == 0
    assert destination.exists()
    assert destination.read_text(encoding="utf-8") == "binary"

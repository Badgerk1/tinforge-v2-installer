from pathlib import Path
import sys

import pytest


@pytest.fixture
def release_module():
    import importlib.util

    scripts_dir = Path(__file__).resolve().parents[1] / "build-scripts"
    module_path = scripts_dir / "create_release.py"
    sys.path.insert(0, str(scripts_dir))
    spec = importlib.util.spec_from_file_location("create_release", module_path)
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

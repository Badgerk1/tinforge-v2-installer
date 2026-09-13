from pathlib import Path
from types import SimpleNamespace

import importlib.util
import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "build-scripts"


def _load_script(module_name: str):
    import sys

    if str(SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPTS_DIR))
    spec = importlib.util.spec_from_file_location(module_name, SCRIPTS_DIR / f"{module_name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_run_command_returns_false_on_failure(monkeypatch):
    utils = _load_script("utils")

    def _raise(*_args, **_kwargs):
        raise utils.subprocess.CalledProcessError(returncode=1, cmd="bad")

    monkeypatch.setattr(utils.subprocess, "run", _raise)
    assert utils.run_command(["bad"]) is False


def test_run_command_returns_true_on_success(monkeypatch):
    utils = _load_script("utils")
    monkeypatch.setattr(utils.subprocess, "run", lambda *_args, **_kwargs: SimpleNamespace(returncode=0))
    assert utils.run_command(["ok"]) is True


def test_windows_build_returns_error_when_spec_missing(monkeypatch, tmp_path):
    module = _load_script("build_windows")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(module, "parse_args", lambda: SimpleNamespace(skip_build=False, smoke_test=False))
    assert module.main() == 1


def test_windows_build_returns_error_when_dependencies_missing(monkeypatch, tmp_path):
    module = _load_script("build_windows")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(module, "parse_args", lambda: SimpleNamespace(skip_build=False, smoke_test=False))
    monkeypatch.setattr(module, "check_python_version", lambda: True)
    monkeypatch.setattr(module, "run_command", lambda *_args, **_kwargs: False)
    assert module.main() == 1


def test_windows_build_stages_non_smoke_artifact(monkeypatch, tmp_path):
    module = _load_script("build_windows")
    monkeypatch.chdir(tmp_path)
    (tmp_path / "build/pyinstaller").mkdir(parents=True)
    (tmp_path / "src/tinforge_v2").mkdir(parents=True)
    (tmp_path / "build/pyinstaller/tinforge_v2.spec").write_text("", encoding="utf-8")
    (tmp_path / "src/tinforge_v2/main.py").write_text("", encoding="utf-8")
    (tmp_path / "dist").mkdir()
    (tmp_path / "dist/TinForge-v2-Setup.exe").write_text("exe", encoding="utf-8")

    monkeypatch.setattr(module, "parse_args", lambda: SimpleNamespace(skip_build=True, smoke_test=False))
    monkeypatch.setattr(module, "check_python_version", lambda: True)
    monkeypatch.setattr(module, "run_command", lambda *_args, **_kwargs: True)
    assert module.main() == 0
    assert (tmp_path / ".artifacts" / "TinForge-v2-Setup.exe").read_text(encoding="utf-8") == "exe"


def test_windows_build_smoke_creates_placeholder(monkeypatch, tmp_path):
    module = _load_script("build_windows")
    monkeypatch.chdir(tmp_path)

    monkeypatch.setattr(module, "parse_args", lambda: SimpleNamespace(skip_build=True, smoke_test=True))
    assert module.main() == 0
    assert (tmp_path / ".artifacts" / "TinForge-v2-Setup.exe").is_file()


def test_macos_build_stages_non_smoke_artifact(monkeypatch, tmp_path):
    module = _load_script("build_macos")
    monkeypatch.chdir(tmp_path)
    (tmp_path / "build/pyinstaller").mkdir(parents=True)
    (tmp_path / "src/tinforge_v2").mkdir(parents=True)
    (tmp_path / "build/pyinstaller/tinforge_v2.spec").write_text("", encoding="utf-8")
    (tmp_path / "src/tinforge_v2/main.py").write_text("", encoding="utf-8")
    (tmp_path / "dist").mkdir()
    (tmp_path / "dist/TinForge-v2.dmg").write_text("mac", encoding="utf-8")

    monkeypatch.setattr(module, "parse_args", lambda: SimpleNamespace(skip_build=True, smoke_test=False))
    monkeypatch.setattr(module, "check_python_version", lambda: True)
    monkeypatch.setattr(module, "run_command", lambda *_args, **_kwargs: True)
    assert module.main() == 0
    assert (tmp_path / ".artifacts" / "TinForge-v2.dmg").read_text(encoding="utf-8") == "mac"


def test_macos_build_smoke_creates_placeholder(monkeypatch, tmp_path):
    module = _load_script("build_macos")
    monkeypatch.chdir(tmp_path)

    monkeypatch.setattr(module, "parse_args", lambda: SimpleNamespace(skip_build=True, smoke_test=True))
    assert module.main() == 0
    assert (tmp_path / ".artifacts" / "TinForge-v2.dmg").is_file()


def test_linux_build_stages_non_smoke_artifact_and_sets_executable(monkeypatch, tmp_path):
    module = _load_script("build_linux")
    monkeypatch.chdir(tmp_path)
    (tmp_path / "build/pyinstaller").mkdir(parents=True)
    (tmp_path / "src/tinforge_v2").mkdir(parents=True)
    (tmp_path / "build/pyinstaller/tinforge_v2.spec").write_text("", encoding="utf-8")
    (tmp_path / "src/tinforge_v2/main.py").write_text("", encoding="utf-8")
    (tmp_path / "dist").mkdir()
    (tmp_path / "dist/TinForge-v2.AppImage").write_text("linux", encoding="utf-8")

    monkeypatch.setattr(module, "parse_args", lambda: SimpleNamespace(skip_build=True, smoke_test=False))
    monkeypatch.setattr(module, "check_python_version", lambda: True)
    monkeypatch.setattr(module, "run_command", lambda *_args, **_kwargs: True)
    assert module.main() == 0
    artifact = tmp_path / ".artifacts" / "TinForge-v2.AppImage"
    assert artifact.read_text(encoding="utf-8") == "linux"
    assert artifact.stat().st_mode & 0o111


def test_linux_build_smoke_creates_placeholder(monkeypatch, tmp_path):
    module = _load_script("build_linux")
    monkeypatch.chdir(tmp_path)

    monkeypatch.setattr(module, "parse_args", lambda: SimpleNamespace(skip_build=True, smoke_test=True))
    assert module.main() == 0
    assert (tmp_path / ".artifacts" / "TinForge-v2.AppImage").is_file()


def test_platform_workflows_support_release_and_reusable_upload_paths():
    workflows = {
        "build-windows.yml": ("windows-installer", ".artifacts/TinForge-v2-Setup.exe"),
        "build-macos.yml": ("macos-installer", ".artifacts/TinForge-v2.dmg"),
        "build-linux.yml": ("linux-installer", ".artifacts/TinForge-v2.AppImage"),
    }

    for filename, (artifact_name, artifact_path) in workflows.items():
        workflow = yaml.safe_load((REPO_ROOT / ".github" / "workflows" / filename).read_text(encoding="utf-8"))
        triggers = workflow.get("on", workflow.get(True))
        assert triggers is not None
        assert "workflow_call" in triggers
        assert "workflow_dispatch" in triggers

        steps = workflow["jobs"]["build"]["steps"]
        upload_artifact = next(step for step in steps if step["name"] == "Upload workflow artifact")
        assert upload_artifact["if"] == "github.event_name != 'release'"
        assert upload_artifact["uses"] == "actions/upload-artifact@v4"
        assert upload_artifact["with"]["name"] == artifact_name
        assert upload_artifact["with"]["path"] == artifact_path

        upload_release = next(step for step in steps if step["name"] == "Upload to release")
        assert upload_release["if"] == "github.event_name == 'release'"
        assert upload_release["uses"] == "softprops/action-gh-release@v1"
        assert upload_release["with"]["files"] == artifact_path

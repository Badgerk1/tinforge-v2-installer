from pathlib import Path
from types import SimpleNamespace

import importlib.util


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


def test_windows_build_returns_error_when_spec_missing(monkeypatch, tmp_path):
    module = _load_script("build_windows")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(module, "parse_args", lambda: SimpleNamespace(skip_build=False, smoke_test=False))
    assert module.main() == 1


def test_windows_build_smoke_creates_placeholder(monkeypatch, tmp_path):
    module = _load_script("build_windows")
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".artifacts").mkdir(parents=True)

    monkeypatch.setattr(module, "parse_args", lambda: SimpleNamespace(skip_build=True, smoke_test=True))
    assert module.main() == 0
    assert (tmp_path / ".artifacts" / "TinForge-v2-Setup.exe").is_file()


def test_macos_build_smoke_creates_placeholder(monkeypatch, tmp_path):
    module = _load_script("build_macos")
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".artifacts").mkdir(parents=True)

    monkeypatch.setattr(module, "parse_args", lambda: SimpleNamespace(skip_build=True, smoke_test=True))
    assert module.main() == 0
    assert (tmp_path / ".artifacts" / "TinForge-v2.dmg").is_file()


def test_linux_build_smoke_creates_placeholder(monkeypatch, tmp_path):
    module = _load_script("build_linux")
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".artifacts").mkdir(parents=True)

    monkeypatch.setattr(module, "parse_args", lambda: SimpleNamespace(skip_build=True, smoke_test=True))
    assert module.main() == 0
    assert (tmp_path / ".artifacts" / "TinForge-v2.AppImage").is_file()

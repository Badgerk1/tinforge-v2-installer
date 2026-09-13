from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_required_minimal_files_exist():
    required = [
        "src/tinforge_v2/main.py",
        "src/tinforge_v2/__init__.py",
        "src/tinforge_v2/ui/__init__.py",
        "src/tinforge_v2/ui/main_window.py",
        "build/pyinstaller/tinforge_v2.spec",
        "build-scripts/build_windows.py",
        "build-scripts/build_macos.py",
        "build-scripts/build_linux.py",
        "build-scripts/utils.py",
        ".github/workflows/build-windows.yml",
        ".github/workflows/build-macos.yml",
        ".github/workflows/build-linux.yml",
    ]
    for rel_path in required:
        assert (REPO_ROOT / rel_path).is_file(), rel_path


def test_requirements_are_exact():
    content = (REPO_ROOT / "requirements.txt").read_text(encoding="utf-8").strip().splitlines()
    assert content == [
        "PyQt5==5.15.9",
        "PyQt5-sip==12.13.0",
        "PyInstaller==6.1.0",
    ]


def test_setup_contains_console_entrypoint():
    content = (REPO_ROOT / "setup.py").read_text(encoding="utf-8")
    assert 'name="tinforge-v2"' in content
    assert 'version="2.1.0"' in content
    assert '"tinforge-v2=tinforge_v2.main:main"' in content


def test_spec_targets_src_entrypoint():
    content = (REPO_ROOT / "build/pyinstaller/tinforge_v2.spec").read_text(encoding="utf-8")
    assert "entry_point = ['src/tinforge_v2/main.py']" in content

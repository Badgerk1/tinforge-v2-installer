import importlib.util
from pathlib import Path

from PyQt5.QtWidgets import QApplication, QPushButton

from src.tinforge_v2.ui.main_window import MainWindow


def test_main_window_has_expected_title_and_button():
    app = QApplication.instance() or QApplication([])
    window = MainWindow()

    assert window.windowTitle() == "TinForge v2 Installer"
    buttons = window.findChildren(QPushButton)
    assert any(button.text() == "Click Me!" for button in buttons)

    window.close()
    app.quit()


def test_main_entrypoint_module_loads_without_import_errors():
    main_path = Path(__file__).resolve().parents[1] / "src" / "tinforge_v2" / "main.py"
    spec = importlib.util.spec_from_file_location("tinforge_v2_main", main_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    assert callable(module.main)


def test_main_entrypoint_inserts_src_on_sys_path():
    main_path = Path(__file__).resolve().parents[1] / "src" / "tinforge_v2" / "main.py"
    spec = importlib.util.spec_from_file_location("tinforge_v2_main_path", main_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    assert str(main_path.parent.parent) in module.sys.path


def test_main_executes_application_bootstrap(monkeypatch):
    import src.tinforge_v2.main as main_module

    created_apps = []

    class FakeApp:
        def __init__(self, _args):
            self.name = None
            self.version = None
            created_apps.append(self)

        def setApplicationName(self, name):
            self.name = name

        def setApplicationVersion(self, version):
            self.version = version

        def exec_(self):
            return 0

    class FakeWindow:
        shown = False

        def show(self):
            self.shown = True

    fake_window = FakeWindow()

    monkeypatch.setattr(main_module, "QApplication", FakeApp)
    monkeypatch.setattr(main_module, "MainWindow", lambda: fake_window)

    assert main_module.main() == 0
    assert fake_window.shown is True
    assert created_apps[0].name == "TinForge v2"
    assert created_apps[0].version == "2.1.0"

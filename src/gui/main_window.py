"""Main GUI window."""

from __future__ import annotations

from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QStatusBar,
    QToolBar,
)

from src.core.app_manager import AppManager
from src.gui.about_dialog import show_about
from src.gui.export_wizard import ExportWizard
from src.gui.project_manager import ProjectManagerWidget
from src.gui.settings_dialog import SettingsDialog
from src.gui.styles import DARK_THEME


class MainWindow(QMainWindow):
    def __init__(self, manager: AppManager) -> None:
        super().__init__()
        self.manager = manager
        self.setWindowTitle("TinForge v2 Installer")
        self.resize(1000, 640)
        self.setAcceptDrops(True)

        self.project_widget = ProjectManagerWidget(self)
        self.setCentralWidget(self.project_widget)

        self._build_menu()
        self._build_toolbar()
        self._build_status_bar()
        self._refresh_recent_projects()

    def _build_menu(self) -> None:
        file_menu = self.menuBar().addMenu("File")
        export_action = QAction("Export", self)
        export_action.triggered.connect(self.export_project)
        file_menu.addAction(export_action)

        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.open_settings)
        file_menu.addAction(settings_action)

        help_menu = self.menuBar().addMenu("Help")
        about_action = QAction("About", self)
        about_action.triggered.connect(lambda: show_about(self))
        help_menu.addAction(about_action)

    def _build_toolbar(self) -> None:
        toolbar = QToolBar("Main", self)
        self.addToolBar(toolbar)

        new_action = QAction("New Project", self)
        new_action.triggered.connect(self.new_project)
        toolbar.addAction(new_action)

        open_action = QAction("Open Data", self)
        open_action.triggered.connect(self.open_sources)
        toolbar.addAction(open_action)

    def _build_status_bar(self) -> None:
        status = QStatusBar(self)
        self.progress = QProgressBar(self)
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        status.addPermanentWidget(self.progress)
        status.showMessage("Ready")
        self.setStatusBar(status)

    def _refresh_recent_projects(self) -> None:
        current = self.manager.current_project
        names = [current.name] if current else []
        self.project_widget.set_projects(names)

    def new_project(self) -> None:
        self.manager.create_project("Untitled Project")
        self.statusBar().showMessage("Created project")
        self._refresh_recent_projects()

    def open_sources(self) -> None:
        files, _ = QFileDialog.getOpenFileNames(self, "Select source files", "", "Data Files (*.csv *.pdf)")
        if not files:
            return
        project = self.manager.open_project("Imported Project", files)
        self.statusBar().showMessage(f"Loaded {len(project.source_files)} source files")
        self._refresh_recent_projects()

    def export_project(self) -> None:
        wizard = ExportWizard(self)
        if wizard.exec_() != wizard.Accepted:
            return

        output = QFileDialog.getExistingDirectory(self, "Select output folder")
        if not output:
            return

        self.progress.setValue(30)
        try:
            files = self.manager.export(Path(output), wizard.selected_formats())
        except RuntimeError as exc:
            QMessageBox.warning(self, "Export failed", str(exc))
        else:
            self.progress.setValue(100)
            QMessageBox.information(self, "Export complete", f"Generated {len(files)} files in {output}")
        finally:
            self.progress.setValue(0)

    def open_settings(self) -> None:
        dialog = SettingsDialog(self.manager.settings, self)
        if dialog.exec_() == dialog.Accepted:
            self.manager.settings.update(dialog.updated_settings())
            self.manager.config.save(self.manager.settings)
            self.statusBar().showMessage("Settings saved")

    def dragEnterEvent(self, event):  # noqa: N802
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):  # noqa: N802
        sources = [u.toLocalFile() for u in event.mimeData().urls() if Path(u.toLocalFile()).suffix.lower() in {".csv", ".pdf"}]
        if not sources:
            return
        self.manager.open_project("Dropped Project", sources)
        self.statusBar().showMessage(f"Loaded {len(sources)} dropped files")
        self._refresh_recent_projects()


def run_app(manager: AppManager) -> int:
    app = QApplication.instance()
    if app is None:
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        app = QApplication([])
    app.setStyleSheet(DARK_THEME)
    window = MainWindow(manager)
    window.show()
    return app.exec_()

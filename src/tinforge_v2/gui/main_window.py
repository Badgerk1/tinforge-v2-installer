"""Main window UI."""

from __future__ import annotations

from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QDockWidget,
    QFileDialog,
    QInputDialog,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QStatusBar,
    QTextEdit,
    QToolBar,
)

from ..core.config import ConfigManager
from ..core.constants import APP_NAME, PROJECT_FILE_SUFFIX
from ..core.project import ProjectManager
from ..utils.validators import is_project_file, is_supported_source
from .dialogs.about import show_about
from .dialogs.export import ExportWizard
from .dialogs.settings import SettingsDialog
from .styles import load_theme
from .widgets.file_browser import FileBrowserWidget
from .widgets.preview_panel import PreviewPanel
from .widgets.project_manager import ProjectManagerWidget


class MainWindow(QMainWindow):
    def __init__(self, config: dict | None = None, config_manager: ConfigManager | None = None, project_manager: ProjectManager | None = None) -> None:
        super().__init__()
        self.config_manager = config_manager or ConfigManager()
        self.config = config or self.config_manager.load()
        self.project_manager = project_manager or ProjectManager(self.config_manager, self.config)
        self._recent_project_actions: list[QAction] = []

        self.setWindowTitle(APP_NAME)
        self.resize(1280, 780)
        self.setAcceptDrops(True)

        self.summary = QTextEdit(self)
        self.summary.setReadOnly(True)
        self.summary.setPlainText("Create or open a project to begin.")
        self.setCentralWidget(self.summary)

        self.project_widget = ProjectManagerWidget(self)
        self.project_widget.fileActivated.connect(self.preview_file)
        self.project_widget.removeRequested.connect(self.remove_project_file)

        self.file_browser = FileBrowserWidget(self)
        self.file_browser.fileActivated.connect(self.preview_file)

        self.preview_panel = PreviewPanel(self)

        self._create_actions()
        self._build_menu()
        self._build_toolbar()
        self._build_docks()
        self._build_status_bar()
        self.apply_theme(self.config.get("theme", "dark"))
        self._refresh_recent_projects_menu()
        self._update_project_views()

    def _create_actions(self) -> None:
        self.new_action = QAction("New Project", self)
        self.new_action.setShortcut("Ctrl+N")
        self.new_action.triggered.connect(self.new_project)

        self.open_project_action = QAction("Open Project", self)
        self.open_project_action.setShortcut("Ctrl+O")
        self.open_project_action.triggered.connect(self.open_project_dialog)

        self.save_project_action = QAction("Save Project", self)
        self.save_project_action.setShortcut("Ctrl+S")
        self.save_project_action.triggered.connect(self.save_project)

        self.import_files_action = QAction("Import Files", self)
        self.import_files_action.triggered.connect(self.import_files)

        self.export_action = QAction("Export", self)
        self.export_action.setShortcut("Ctrl+E")
        self.export_action.triggered.connect(self.export_project)

        self.settings_action = QAction("Settings", self)
        self.settings_action.triggered.connect(self.open_settings)

        self.toggle_theme_action = QAction("Toggle Theme", self)
        self.toggle_theme_action.triggered.connect(self.toggle_theme)

        self.about_action = QAction("About", self)
        self.about_action.triggered.connect(lambda: show_about(self))

        self.exit_action = QAction("Exit", self)
        self.exit_action.triggered.connect(self.close)

    def _build_menu(self) -> None:
        file_menu = self.menuBar().addMenu("File")
        for action in [self.new_action, self.open_project_action, self.save_project_action, self.import_files_action, self.export_action]:
            file_menu.addAction(action)
        self.recent_projects_menu = file_menu.addMenu("Recent Projects")
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        edit_menu = self.menuBar().addMenu("Edit")
        edit_menu.addAction(self.settings_action)

        view_menu = self.menuBar().addMenu("View")
        view_menu.addAction(self.toggle_theme_action)

        help_menu = self.menuBar().addMenu("Help")
        help_menu.addAction(self.about_action)

    def _build_toolbar(self) -> None:
        toolbar = QToolBar("Main", self)
        self.addToolBar(toolbar)
        for action in [self.new_action, self.open_project_action, self.save_project_action, self.import_files_action, self.export_action]:
            toolbar.addAction(action)

    def _build_docks(self) -> None:
        projects_dock = QDockWidget("Projects", self)
        projects_dock.setWidget(self.project_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, projects_dock)

        browser_dock = QDockWidget("File Browser", self)
        browser_dock.setWidget(self.file_browser)
        self.addDockWidget(Qt.LeftDockWidgetArea, browser_dock)
        self.tabifyDockWidget(projects_dock, browser_dock)

        preview_dock = QDockWidget("Preview", self)
        preview_dock.setWidget(self.preview_panel)
        self.addDockWidget(Qt.RightDockWidgetArea, preview_dock)

    def _build_status_bar(self) -> None:
        status = QStatusBar(self)
        self.progress = QProgressBar(self)
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        status.addPermanentWidget(self.progress)
        status.showMessage("Ready")
        self.setStatusBar(status)

    def _refresh_recent_projects_menu(self) -> None:
        self.recent_projects_menu.clear()
        recent = self.project_manager.recent_projects()
        if not recent:
            empty = QAction("No recent projects", self)
            empty.setEnabled(False)
            self.recent_projects_menu.addAction(empty)
            return
        self._recent_project_actions = []
        for path in recent:
            action = QAction(path, self)
            action.triggered.connect(lambda _checked=False, p=path: self.open_recent_project(p))
            self.recent_projects_menu.addAction(action)
            self._recent_project_actions.append(action)

    def _update_project_views(self) -> None:
        project = self.project_manager.current_project
        self.project_widget.set_project(project)
        if project is None:
            self.summary.setPlainText("Create or open a project to begin.")
            self.preview_panel.show_message("No project selected", "Import files or open a saved TinForge project.")
            return
        details = [
            f"Project: {project.name}",
            f"Files: {len(project.source_files)}",
        ]
        if project.project_path:
            details.append(f"Saved at: {project.project_path}")
        if project.source_files:
            details.append("")
            details.append("Sources:")
            details.extend(f"- {path}" for path in project.source_files)
        self.summary.setPlainText("\n".join(details))
        if project.source_files:
            self.preview_file(str(project.source_files[0]))
        else:
            self.preview_panel.show_message(project.name, "No files in this project yet.")

    def apply_theme(self, theme: str) -> None:
        app = QApplication.instance()
        if app is not None:
            app.setStyleSheet(load_theme(theme))
        self.config["theme"] = theme

    def toggle_theme(self) -> None:
        next_theme = "light" if self.config.get("theme") == "dark" else "dark"
        self.apply_theme(next_theme)
        self.config_manager.save(self.config)
        self.statusBar().showMessage(f"Switched to {next_theme} theme")

    def new_project(self) -> None:
        name, accepted = QInputDialog.getText(self, "New Project", "Project name:", text="Untitled Project")
        if not accepted:
            return
        self.project_manager.create_project(name)
        self.statusBar().showMessage("Created project")
        self._update_project_views()

    def open_project_dialog(self) -> None:
        default_dir = self.config.get("default_project_dir", "")
        path, _ = QFileDialog.getOpenFileName(self, "Open project", default_dir, f"TinForge Project (*{PROJECT_FILE_SUFFIX})")
        if not path:
            return
        self.open_recent_project(path)

    def open_recent_project(self, path: str) -> None:
        try:
            self.project_manager.load_project(path)
        except (OSError, ValueError) as exc:
            QMessageBox.warning(self, "Open project failed", str(exc))
            return
        self.statusBar().showMessage(f"Opened {path}")
        self._refresh_recent_projects_menu()
        self._update_project_views()

    def save_project(self) -> None:
        if self.project_manager.current_project is None:
            QMessageBox.information(self, "Save project", "Create or open a project first.")
            return
        suggested_name = f"{self.project_manager.current_project.name}{PROJECT_FILE_SUFFIX}"
        default_dir = self.config.get("default_project_dir", "")
        selected, _ = QFileDialog.getSaveFileName(
            self,
            "Save project",
            str(Path(default_dir) / suggested_name if default_dir else suggested_name),
            f"TinForge Project (*{PROJECT_FILE_SUFFIX})",
        )
        if not selected:
            return
        saved = self.project_manager.save_project(selected)
        self.statusBar().showMessage(f"Saved project to {saved}")
        self._refresh_recent_projects_menu()
        self._update_project_views()

    def import_files(self) -> None:
        default_dir = self.file_browser.location.text().strip() or self.config.get("default_project_dir", "")
        files, _ = QFileDialog.getOpenFileNames(self, "Select source files", default_dir, "Data Files (*.csv *.pdf *.txt *.xml *.dxf *.dbx *.tp3)")
        if not files:
            return
        current = self.project_manager.current_project
        if current is None:
            project = self.project_manager.import_files(Path(files[0]).stem, files)
        else:
            existing = [str(path) for path in current.source_files]
            merged = existing + [path for path in files if path not in existing]
            project = self.project_manager.import_files(current.name, merged)
        self.statusBar().showMessage(f"Loaded {len(project.source_files)} source files")
        self._update_project_views()

    def export_project(self) -> None:
        wizard = ExportWizard(self)
        if wizard.exec_() != wizard.Accepted:
            return
        output = wizard.selected_output_dir() or self.config.get("default_export_dir", "")
        if not output:
            output = QFileDialog.getExistingDirectory(self, "Select output folder")
        if not output:
            return
        self.progress.setValue(30)
        try:
            files = self.project_manager.export(Path(output), wizard.selected_formats())
        except RuntimeError as exc:
            QMessageBox.warning(self, "Export failed", str(exc))
        else:
            self.progress.setValue(100)
            QMessageBox.information(self, "Export complete", f"Generated {len(files)} files in {output}")
            self.statusBar().showMessage("Export complete")
        finally:
            self.progress.setValue(0)

    def open_settings(self) -> None:
        dialog = SettingsDialog(self.config, self)
        if dialog.exec_() == dialog.Accepted:
            self.config.update(dialog.updated_settings())
            self.config_manager.save(self.config)
            self.project_manager.settings = self.config
            self.apply_theme(self.config.get("theme", "dark"))
            self.statusBar().showMessage("Settings saved")
            self._refresh_recent_projects_menu()

    def preview_file(self, path: str) -> None:
        self.preview_panel.show_file(path)

    def remove_project_file(self, path: str) -> None:
        project = self.project_manager.current_project
        if project is None:
            return
        project.source_files = [item for item in project.source_files if str(item) != path]
        if project.project_path is not None:
            self.project_manager.save_project(project.project_path)
        self.statusBar().showMessage(f"Removed {Path(path).name}")
        self._update_project_views()

    def dragEnterEvent(self, event):  # noqa: N802
        if event.mimeData().hasUrls():
            urls = [url.toLocalFile() for url in event.mimeData().urls()]
            if any(is_supported_source(path) or is_project_file(path) for path in urls):
                event.acceptProposedAction()
                return
        event.ignore()

    def dropEvent(self, event):  # noqa: N802
        urls = [url.toLocalFile() for url in event.mimeData().urls()]
        project_files = [path for path in urls if is_project_file(path)]
        if project_files:
            self.open_recent_project(project_files[0])
            return
        sources = [path for path in urls if is_supported_source(path)]
        if not sources:
            return
        current = self.project_manager.current_project
        if current is None:
            self.project_manager.import_files(Path(sources[0]).stem, sources)
        else:
            existing = [str(path) for path in current.source_files]
            merged = existing + [path for path in sources if path not in existing]
            self.project_manager.import_files(current.name, merged)
        self.statusBar().showMessage(f"Loaded {len(sources)} dropped files")
        self._update_project_views()

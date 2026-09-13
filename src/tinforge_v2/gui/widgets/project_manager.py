"""Project manager tree view."""

from __future__ import annotations

from pathlib import Path

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QAction, QMenu, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget

from ...core.project import Project


class ProjectManagerWidget(QWidget):
    fileActivated = pyqtSignal(str)
    removeRequested = pyqtSignal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.tree = QTreeWidget(self)
        self.tree.setHeaderLabels(["Project Files"])
        self.tree.itemDoubleClicked.connect(self._on_item_double_clicked)
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self._open_context_menu)

        layout = QVBoxLayout(self)
        layout.addWidget(self.tree)

    def set_project(self, project: Project | None) -> None:
        self.tree.clear()
        if project is None:
            return
        root = QTreeWidgetItem([project.name])
        root.setData(0, Qt.UserRole, "")
        self.tree.addTopLevelItem(root)
        for source in project.source_files:
            item = QTreeWidgetItem([Path(source).name])
            item.setData(0, Qt.UserRole, str(source))
            root.addChild(item)
        root.setExpanded(True)

    def set_projects(self, names: list[str]) -> None:
        self.tree.clear()
        for name in names:
            self.tree.addTopLevelItem(QTreeWidgetItem([name]))

    def _on_item_double_clicked(self, item: QTreeWidgetItem, _column: int) -> None:
        source = item.data(0, Qt.UserRole)
        if source:
            self.fileActivated.emit(source)

    def _open_context_menu(self, position) -> None:
        item = self.tree.itemAt(position)
        if item is None:
            return
        source = item.data(0, Qt.UserRole)
        if not source:
            return
        menu = QMenu(self)
        remove_action = QAction("Remove from project", self)
        remove_action.triggered.connect(lambda: self.removeRequested.emit(source))
        menu.addAction(remove_action)
        menu.exec_(self.tree.viewport().mapToGlobal(position))

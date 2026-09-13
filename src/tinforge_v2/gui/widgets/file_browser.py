"""File browser widget."""

from __future__ import annotations

from pathlib import Path

from PyQt5.QtCore import QDir, QModelIndex, pyqtSignal
from PyQt5.QtWidgets import (
    QComboBox,
    QFileSystemModel,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QTreeView,
    QVBoxLayout,
    QWidget,
)


class FileBrowserWidget(QWidget):
    fileActivated = pyqtSignal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.location = QLineEdit(str(Path.home()), self)
        self.filter_box = QComboBox(self)
        self.filter_box.addItems(["All files", "Data files", "Project files"])
        self.go_button = QPushButton("Go", self)
        self.go_button.clicked.connect(self.set_root_path)

        controls = QHBoxLayout()
        controls.addWidget(self.location)
        controls.addWidget(self.filter_box)
        controls.addWidget(self.go_button)

        self.model = QFileSystemModel(self)
        self.model.setRootPath(str(Path.home()))
        self.model.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot | QDir.Files)

        self.view = QTreeView(self)
        self.view.setModel(self.model)
        self.view.setRootIndex(self.model.index(str(Path.home())))
        self.view.doubleClicked.connect(self._activate_index)
        for column in range(1, 4):
            self.view.hideColumn(column)

        layout = QVBoxLayout(self)
        layout.addLayout(controls)
        layout.addWidget(self.view)

    def set_root_path(self) -> None:
        path = Path(self.location.text().strip() or Path.home())
        if not path.exists():
            return
        self.view.setRootIndex(self.model.index(str(path)))

    def _activate_index(self, index: QModelIndex) -> None:
        path = self.model.filePath(index)
        if Path(path).is_file():
            self.fileActivated.emit(path)

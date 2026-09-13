"""Project management UI panel."""

from PyQt5.QtWidgets import QLabel, QListWidget, QPushButton, QVBoxLayout, QWidget


class ProjectManagerWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Recent Projects"))
        self.projects = QListWidget(self)
        layout.addWidget(self.projects)
        self.open_button = QPushButton("Open Project", self)
        layout.addWidget(self.open_button)

    def set_projects(self, names: list[str]) -> None:
        self.projects.clear()
        self.projects.addItems(names)

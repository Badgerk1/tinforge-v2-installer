"""About dialog."""

from __future__ import annotations

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QLabel, QVBoxLayout, QWidget

from ...core.constants import APP_NAME
from ...core.version import VersionManager


class AboutDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle(f"About {APP_NAME}")
        version = VersionManager().current().version

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"<h2>{APP_NAME}</h2><p>Version {version}</p>"))

        details = QLabel(
            '<p>Professional installer and launcher system for TinForge v2.</p>'
            '<p><a href="https://github.com/Badgerk1/tinforge-v2-installer">GitHub Repository</a></p>'
            '<p>Licensed under MIT.</p>'
        )
        details.setTextFormat(Qt.RichText)
        details.setOpenExternalLinks(True)
        layout.addWidget(details)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok, self)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)


def show_about(parent: QWidget | None = None) -> None:
    AboutDialog(parent).exec_()

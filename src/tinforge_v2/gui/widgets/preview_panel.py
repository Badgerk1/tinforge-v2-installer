"""Preview panel for files and project metadata."""

from __future__ import annotations

from pathlib import Path

from PyQt5.QtWidgets import QLabel, QPlainTextEdit, QVBoxLayout, QWidget

from ...utils.file_utils import human_size, read_text_preview


class PreviewPanel(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.title = QLabel("No file selected", self)
        self.meta = QLabel("", self)
        self.preview = QPlainTextEdit(self)
        self.preview.setReadOnly(True)

        layout = QVBoxLayout(self)
        layout.addWidget(self.title)
        layout.addWidget(self.meta)
        layout.addWidget(self.preview)

    def show_file(self, path: str | Path) -> None:
        target = Path(path)
        if not target.exists():
            self.title.setText(target.name)
            self.meta.setText("Missing file")
            self.preview.setPlainText("")
            return
        self.title.setText(target.name)
        self.meta.setText(f"{target.suffix or 'file'} • {human_size(target)}")
        self.preview.setPlainText(read_text_preview(target))

    def show_message(self, title: str, message: str) -> None:
        self.title.setText(title)
        self.meta.setText("")
        self.preview.setPlainText(message)

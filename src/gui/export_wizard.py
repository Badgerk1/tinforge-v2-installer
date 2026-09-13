"""Export wizard UI."""

from __future__ import annotations

from PyQt5.QtWidgets import QCheckBox, QDialog, QDialogButtonBox, QVBoxLayout

from src.core.constants import DEFAULT_EXPORT_FORMATS


class ExportWizard(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Export Wizard")
        self._format_boxes: dict[str, QCheckBox] = {}

        layout = QVBoxLayout(self)
        for fmt in DEFAULT_EXPORT_FORMATS:
            box = QCheckBox(fmt, self)
            box.setChecked(True)
            layout.addWidget(box)
            self._format_boxes[fmt] = box

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def selected_formats(self) -> list[str]:
        return [name for name, box in self._format_boxes.items() if box.isChecked()]

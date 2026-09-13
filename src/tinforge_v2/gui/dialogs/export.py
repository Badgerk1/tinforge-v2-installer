"""Export wizard."""

from __future__ import annotations

from PyQt5.QtWidgets import (
    QCheckBox,
    QFileDialog,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWizard,
    QWizardPage,
)

from ...core.constants import DEFAULT_EXPORT_FORMATS


class _FormatsPage(QWizardPage):
    def __init__(self) -> None:
        super().__init__()
        self.setTitle("Choose export formats")
        self._format_boxes: dict[str, QCheckBox] = {}
        layout = QVBoxLayout(self)
        for fmt in DEFAULT_EXPORT_FORMATS:
            box = QCheckBox(fmt, self)
            box.setChecked(True)
            layout.addWidget(box)
            self._format_boxes[fmt] = box

    def selected_formats(self) -> list[str]:
        return [name for name, box in self._format_boxes.items() if box.isChecked()]


class _OptionsPage(QWizardPage):
    def __init__(self) -> None:
        super().__init__()
        self.setTitle("Configure export")
        self.quality = QLineEdit("Standard", self)
        self.output_dir = QLineEdit(self)
        browse = QPushButton("Browse", self)
        browse.clicked.connect(self._choose_dir)

        layout = QFormLayout(self)
        layout.addRow("Quality", self.quality)
        layout.addRow("Output folder", self.output_dir)
        layout.addRow("", browse)

    def _choose_dir(self) -> None:
        selected = QFileDialog.getExistingDirectory(self, "Select export folder")
        if selected:
            self.output_dir.setText(selected)


class _SummaryPage(QWizardPage):
    def __init__(self) -> None:
        super().__init__()
        self.setTitle("Ready to export")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Click Finish to generate the selected export files."))


class ExportWizard(QWizard):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Export Wizard")
        self.formats_page = _FormatsPage()
        self.options_page = _OptionsPage()
        self.summary_page = _SummaryPage()
        self.addPage(self.formats_page)
        self.addPage(self.options_page)
        self.addPage(self.summary_page)

    def selected_formats(self) -> list[str]:
        return self.formats_page.selected_formats()

    def selected_output_dir(self) -> str:
        return self.options_page.output_dir.text().strip()

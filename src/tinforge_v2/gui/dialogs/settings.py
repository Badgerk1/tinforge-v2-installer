"""Settings dialog."""

from __future__ import annotations

from PyQt5.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
)


class SettingsDialog(QDialog):
    def __init__(self, settings: dict, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Settings")

        self.theme = QComboBox(self)
        self.theme.addItems(["dark", "light"])
        self.theme.setCurrentText(str(settings.get("theme", "dark")))

        self.language = QComboBox(self)
        self.language.addItems(["en", "es", "fr"])
        self.language.setCurrentText(str(settings.get("language", "en")))

        self.default_project_dir = QLineEdit(str(settings.get("default_project_dir", "")), self)
        self.default_export_dir = QLineEdit(str(settings.get("default_export_dir", "")), self)
        self.export_formats = QLineEdit(", ".join(settings.get("default_export_formats", [])), self)

        self.logging_level = QComboBox(self)
        self.logging_level.addItems(["DEBUG", "INFO", "WARNING", "ERROR"])
        self.logging_level.setCurrentText(str(settings.get("logging_level", "INFO")))

        self.auto_update = QCheckBox("Enable auto-updates", self)
        self.auto_update.setChecked(bool(settings.get("auto_update", True)))

        layout = QFormLayout(self)
        layout.addRow("Theme", self.theme)
        layout.addRow("Language", self.language)
        layout.addRow("Default project folder", self.default_project_dir)
        layout.addRow("Default export folder", self.default_export_dir)
        layout.addRow("Default export formats", self.export_formats)
        layout.addRow("Logging level", self.logging_level)
        layout.addRow("", self.auto_update)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def updated_settings(self) -> dict:
        formats = [item.strip() for item in self.export_formats.text().split(",") if item.strip()]
        return {
            "theme": self.theme.currentText(),
            "language": self.language.currentText(),
            "auto_update": self.auto_update.isChecked(),
            "default_project_dir": self.default_project_dir.text().strip(),
            "default_export_dir": self.default_export_dir.text().strip(),
            "default_export_formats": formats,
            "logging_level": self.logging_level.currentText(),
        }

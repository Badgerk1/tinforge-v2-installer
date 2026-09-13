"""Settings dialog."""

from __future__ import annotations

from PyQt5.QtWidgets import QCheckBox, QComboBox, QDialog, QDialogButtonBox, QFormLayout


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

        self.auto_update = QCheckBox("Enable auto-updates", self)
        self.auto_update.setChecked(bool(settings.get("auto_update", True)))

        layout = QFormLayout(self)
        layout.addRow("Theme", self.theme)
        layout.addRow("Language", self.language)
        layout.addRow("", self.auto_update)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def updated_settings(self) -> dict:
        return {
            "theme": self.theme.currentText(),
            "language": self.language.currentText(),
            "auto_update": self.auto_update.isChecked(),
        }

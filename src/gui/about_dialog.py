"""About dialog."""

from PyQt5.QtWidgets import QMessageBox, QWidget

from src.core.constants import APP_NAME


def show_about(parent: QWidget) -> None:
    QMessageBox.information(parent, f"About {APP_NAME}", f"{APP_NAME}\nProfessional installer and launcher")

"""
Main Application Window

Simple, working GUI that displays properly.
"""

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QMainWindow, QMessageBox, QPushButton, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize the UI"""
        self.setWindowTitle("TinForge v2 Installer")
        self.setGeometry(100, 100, 600, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        title = QLabel("Welcome to TinForge v2")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        desc = QLabel(
            "Professional TIN generation and multi-format export software\n"
            "with automatic Python bundling and auto-updates."
        )
        desc.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc)

        button = QPushButton("Click Me!")
        button.clicked.connect(self.on_button_click)
        layout.addWidget(button)

        central_widget.setLayout(layout)

    def on_button_click(self):
        """Handle button click"""
        QMessageBox.information(
            self,
            "TinForge v2",
            "Application is working!\n\n"
            "This is a simple test to verify the application runs correctly.",
        )

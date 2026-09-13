#!/usr/bin/env python3
"""
TinForge v2 Application Entry Point

This is the MAIN ENTRY POINT for the application.
It MUST work when run directly.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5.QtWidgets import QApplication

from tinforge_v2.ui.main_window import MainWindow


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)

    app.setApplicationName("TinForge v2")
    app.setApplicationVersion("2.1.0")

    window = MainWindow()
    window.show()

    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Application entry point."""

from __future__ import annotations

import logging
import sys

from PyQt5.QtWidgets import QApplication

try:  # pragma: no cover - import path depends on how the app is launched
    from tinforge_v2.core.config import load_config
    from tinforge_v2.gui.main_window import MainWindow
except ImportError:  # pragma: no cover
    from src.tinforge_v2.core.config import load_config
    from src.tinforge_v2.gui.main_window import MainWindow


def setup_logging() -> logging.Logger:
    """Setup application logging."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger(__name__)


def main() -> int:
    """Main application entry point."""
    logger = setup_logging()
    logger.info("Starting TinForge v2 Installer")

    app = QApplication(sys.argv)
    app.setApplicationName("TinForge v2")
    app.setApplicationVersion("1.0.0")

    config = load_config()
    window = MainWindow(config=config)
    window.show()

    return app.exec_()


if __name__ == "__main__":
    raise SystemExit(main())

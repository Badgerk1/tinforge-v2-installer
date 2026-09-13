#!/usr/bin/env python3
"""Application entry point."""

from __future__ import annotations

import logging
import sys

from PyQt5.QtWidgets import QApplication

try:  # pragma: no cover - import path depends on how the app is launched
    from tinforge_v2.core.config import load_config
    from tinforge_v2.gui.main_window import MainWindow
    from tinforge_v2.utils.logger import setup_logger
except ImportError:  # pragma: no cover
    from src.tinforge_v2.core.config import load_config
    from src.tinforge_v2.gui.main_window import MainWindow
    from src.tinforge_v2.utils.logger import setup_logger


def setup_logging(config: dict[str, object] | None = None) -> logging.Logger:
    """Setup application logging."""
    level = str((config or {}).get("logging_level", "INFO"))
    resolved_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(level=resolved_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    return setup_logger(__name__, level=level)


def main() -> int:
    """Main application entry point."""
    config = load_config()
    logger = setup_logging(config)
    logger.info("Starting TinForge v2 Installer")

    app = QApplication(sys.argv)
    app.setApplicationName("TinForge v2")
    app.setApplicationVersion("1.0.0")
    window = MainWindow(config=config)
    window.show()

    return app.exec_()


if __name__ == "__main__":
    raise SystemExit(main())

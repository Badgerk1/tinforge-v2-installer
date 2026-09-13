"""Application logging helpers."""

from __future__ import annotations

import logging
from pathlib import Path

from ..core.constants import CONFIG_DIR


def setup_logger(name: str = "tinforge_v2", level: str = "INFO") -> logging.Logger:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    log_dir = CONFIG_DIR / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    resolved_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(resolved_level)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_path = log_dir / "tinforge-v2.log"
    existing_handler = next(
        (
            handler for handler in logger.handlers
            if isinstance(handler, logging.FileHandler) and Path(handler.baseFilename) == file_path
        ),
        None,
    )
    if existing_handler is None:
        existing_handler = logging.FileHandler(file_path, encoding="utf-8")
        logger.addHandler(existing_handler)
    existing_handler.setLevel(resolved_level)
    existing_handler.setFormatter(formatter)
    return logger

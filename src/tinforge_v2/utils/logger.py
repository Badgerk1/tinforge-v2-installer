"""Application logging helpers."""

from __future__ import annotations

import logging

from ..core.constants import CONFIG_DIR


def setup_logger(name: str = "tinforge_v2", level: str = "INFO") -> logging.Logger:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    log_dir = CONFIG_DIR / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    if not logger.handlers:
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler = logging.FileHandler(log_dir / "tinforge-v2.log", encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger

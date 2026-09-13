"""TinForge v2 installer application entry point."""

from src.core.app_manager import AppManager
from src.gui.main_window import run_app


def main() -> int:
    manager = AppManager()
    return run_app(manager)


if __name__ == "__main__":
    raise SystemExit(main())

"""TinForge v2 installer application package."""

from .core.constants import APP_NAME
from .core.version import VersionManager

__all__ = ["APP_NAME", "VersionManager"]
__version__ = VersionManager().current().version

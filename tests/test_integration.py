from src.core.version import VersionManager


def test_version_comparison():
    assert VersionManager.is_newer("1.0.1", "1.0.0") is True
    assert VersionManager.is_newer("1.0.0", "1.0.0") is False

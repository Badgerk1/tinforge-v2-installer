from src.gui.styles import DARK_THEME


def test_theme_contains_main_window_rule():
    assert "QMainWindow" in DARK_THEME

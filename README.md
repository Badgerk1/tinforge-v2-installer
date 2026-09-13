# tinforge-v2-installer

Professional installer and launcher system for TinForge v2.

## Highlights

- Standalone desktop app packaging with PyInstaller
- Platform installer pipelines:
  - Windows: NSIS (`TinForge-v2-Setup.exe`)
  - macOS: DMG (`TinForge-v2.dmg`)
  - Linux: portable launcher artifact (`TinForge-v2.AppImage`)
- PyQt5 GUI shell with project manager, file browser, preview panel, export wizard, settings dialog, and about dialog
- Auto-update scaffolding based on GitHub releases
- Build scripts and GitHub Actions workflows for multi-platform release automation

## Quick start

```bash
python -m pip install -r requirements-build.txt
python -m pip install -r requirements.txt
python -m pytest tests/test_app_manager.py tests/test_updater.py tests/test_integration.py tests/test_gui.py
```

Run local app:

```bash
PYTHONPATH=src python -m tinforge_v2.main
```

Build installer for current OS:

```bash
python build_installer.py --platform auto --version 0.1.0
```

## Project layout

- `src/tinforge_v2/` packageable GUI application, core services, utilities, styles, and assets
- `build/` PyInstaller specs, installer templates, branding, and scripts
- `resources/` docs, licenses, and sample data
- `tests/` targeted tests for core/updater/gui/build behavior
- `config/` default app settings and version metadata
- `.github/workflows/` CI build/release automation

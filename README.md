# tinforge-v2-installer

Professional installer and launcher system for TinForge v2.

## Highlights

- Standalone desktop app packaging with PyInstaller
- Platform installer pipelines:
  - Windows: NSIS (`TinForge-v2-Setup.exe`)
  - macOS: DMG (`TinForge-v2.dmg`)
  - Linux: AppImage (`TinForge-v2.AppImage`)
- PyQt5 GUI shell with project manager, export wizard, settings dialog, and about dialog
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
python -m src.main
```

Build installer for current OS:

```bash
python build_installer.py --platform auto --version 0.1.0
```

## Project layout

This repository follows the full installer-oriented layout with:

- `src/` GUI + core + updater modules
- `build/` PyInstaller specs, installer templates, branding, and scripts
- `resources/` docs, licenses, and sample data
- `tests/` targeted tests for core/updater/gui stubs
- `config/` default app settings and version metadata
- `.github/workflows/` CI build/release automation

## Notes

Branding image/icon files are currently placeholders and can be replaced directly under `build/branding/` and `build/installers/**`.

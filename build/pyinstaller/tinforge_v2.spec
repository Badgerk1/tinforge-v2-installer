# -*- mode: python ; coding: utf-8 -*-
import sys
from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

SPEC_ROOT = Path(globals().get("SPECPATH", Path.cwd())).resolve()
ROOT = SPEC_ROOT.parents[1] if SPEC_ROOT.name == "pyinstaller" else Path.cwd().resolve()
SRC_ROOT = ROOT / "src"
PACKAGE_ROOT = SRC_ROOT / "tinforge_v2"
sys.path.insert(0, str(SRC_ROOT))

hiddenimports = collect_submodules("tinforge_v2")
datas = collect_data_files("tinforge_v2") + [
    (str(ROOT / "config"), "config"),
    (str(ROOT / "resources"), "resources"),
]

win_icon = PACKAGE_ROOT / "assets" / "icons" / "app.ico"
mac_icon = ROOT / "build" / "installers" / "macos" / "app_icon.icns"

a = Analysis(
    [str(PACKAGE_ROOT / "main.py")],
    pathex=[str(SRC_ROOT)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports + [
        "PyQt5.QtCore",
        "PyQt5.QtGui",
        "PyQt5.QtWidgets",
        "PyQt5.sip",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="tinforge-v2",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon=str(win_icon) if win_icon.exists() and sys.platform == "win32" else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="tinforge-v2",
)

if sys.platform == "darwin":
    app = BUNDLE(
        coll,
        name="tinforge-v2.app",
        icon=str(mac_icon) if mac_icon.exists() else None,
        bundle_identifier="com.tinforge.v2",
        info_plist={
            "CFBundleDisplayName": "TinForge v2",
            "CFBundleName": "TinForge v2",
            "NSPrincipalClass": "NSApplication",
            "NSHighResolutionCapable": "True",
        },
    )

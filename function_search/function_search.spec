# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

block_cipher = None
project_root = Path(SPECPATH)
src_data = project_root / "src" / "function_search" / "data"

a = Analysis(
    ["src/function_search/main.py"],
    pathex=[str(project_root / "src")],
    binaries=[],
    datas=[
        (str(src_data / "functions.db"), "function_search/data"),
        (str(src_data / "python_common.json"), "function_search/data"),
        (str(src_data / "backend_common.json"), "function_search/data"),
    ],
    hiddenimports=[
        "customtkinter",
        "rapidfuzz",
        "rapidfuzz.fuzz",
        "rapidfuzz.process",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["torch", "tensorflow", "matplotlib", "numpy"],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="FunctionSearch",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="FunctionSearch",
)

app = BUNDLE(
    coll,
    name="FunctionSearch.app",
    icon=None,
    bundle_identifier="com.functionsearch.app",
    info_plist={
        "CFBundleName": "FunctionSearch",
        "CFBundleDisplayName": "Function Search",
        "CFBundleVersion": "1.0.0",
        "CFBundleShortVersionString": "1.0.0",
        "NSHighResolutionCapable": True,
    },
)

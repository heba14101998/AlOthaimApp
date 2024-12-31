# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

# Function to get the path to a file within a package using importlib
import importlib.util
def get_package_data_path(package_name, relative_path):
    spec = importlib.util.find_spec(package_name)
    if spec is None:
        raise ImportError(f"Package '{package_name}' not found.")
    package_dir = os.path.dirname(spec.origin)  # Get the directory of the package
    return os.path.join(package_dir, relative_path)

altair_schema_path = get_package_data_path("altair", "vegalite/v5/schema/vega-lite-schema.json")
streamlit_static_path = get_package_data_path("streamlit", "static")
streamlit_runtime_path = get_package_data_path("streamlit", "runtime")
frontend_path = get_package_data_path("streamlit_option_menu", "frontend")

a = Analysis(
    ['AlOthaimRun.py'],
    binaries=[],
    datas=[
        (altair_schema_path, "./altair/vegalite/v5/schema/"),
        (streamlit_static_path, "./streamlit/static"),
        (streamlit_runtime_path, "./streamlit/runtime"),
        (frontend_path, "streamlit_option_menu/frontend"),
        ('src/style.css', 'style.css'),
        ('assets/branch_data.json', 'branch_data.json')
    ],
    hiddenimports=['streamlit_option_menu', 'pandas', 'pyodbc'],  #No need to collect submodules here
    hookspath=['./hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AlOthaimApp',
    icon='assets\icon.ico',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity="Heba Mohamed",
    entitlements_file=None,
)
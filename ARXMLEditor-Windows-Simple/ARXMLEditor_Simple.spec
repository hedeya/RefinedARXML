# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from pathlib import Path

# Get the project root directory
project_root = Path.cwd()

block_cipher = None

# Collect PyQt6 binaries and data files
def collect_pyqt6_files():
    """Collect PyQt6 Qt6 binaries and platform plugins"""
    binaries = []
    datas = []
    
    try:
        import PyQt6
        pyqt6_path = Path(PyQt6.__file__).parent
        
        # Add Qt6 DLLs
        qt6_dlls = [
            'Qt6Core.dll',
            'Qt6Gui.dll', 
            'Qt6Widgets.dll',
            'Qt6OpenGL.dll',
            'Qt6Svg.dll',
            'Qt6Network.dll',
            'Qt6PrintSupport.dll',
        ]
        
        for dll in qt6_dlls:
            dll_path = pyqt6_path / 'Qt6' / 'bin' / dll
            if dll_path.exists():
                binaries.append((str(dll_path), 'Qt6/bin'))
        
        # Add platform plugins
        plugins_path = pyqt6_path / 'Qt6' / 'plugins'
        if plugins_path.exists():
            datas.append((str(plugins_path), 'Qt6/plugins'))
        
        # Add Qt6 libraries
        lib_path = pyqt6_path / 'Qt6' / 'lib'
        if lib_path.exists():
            datas.append((str(lib_path), 'Qt6/lib'))
            
    except ImportError:
        print("Warning: PyQt6 not found, skipping Qt6 binary collection")
    
    return binaries, datas

# Collect PyQt6 files
pyqt6_binaries, pyqt6_datas = collect_pyqt6_files()

a = Analysis(
    ['main_simple.py'],
    pathex=[str(project_root)],
    binaries=pyqt6_binaries,
    datas=[
        ('examples', 'examples'),
        ('README.md', '.'),
        ('arxml_editor.ico', '.'),
    ] + pyqt6_datas,
    hiddenimports=[
        # PyQt6 modules
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'PyQt6.QtOpenGL',
        'PyQt6.QtSvg',
        'PyQt6.QtNetwork',
        'PyQt6.QtPrintSupport',
        'PyQt6.sip',
        'PyQt6.Qt6',
        # PyQt6 platform plugins
        'PyQt6.Qt6.plugins.platforms',
        'PyQt6.Qt6.plugins.platforms.qwindows',
        'PyQt6.Qt6.plugins.platforms.qminimal',
        'PyQt6.Qt6.plugins.platforms.qoffscreen',
        'PyQt6.Qt6.plugins.styles',
        'PyQt6.Qt6.plugins.imageformats',
        # Basic modules
        'xml.etree.ElementTree',
        'pathlib',
        'lxml',
        'lxml.etree',
        'xmlschema',
        'xmlschema.validators',
        # System modules
        'sys',
        'os',
        'logging',
        'threading',
        'queue',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'unittest',
        'test',
        'pytest',
        'matplotlib',
        'networkx',
        'pydantic',
        'autosar_data',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ARXMLEditor_Simple',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Enable console for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='arxml_editor.ico' if os.path.exists('arxml_editor.ico') else None,
)

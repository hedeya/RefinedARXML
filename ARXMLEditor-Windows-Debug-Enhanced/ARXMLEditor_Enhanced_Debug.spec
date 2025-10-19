# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from pathlib import Path

# Get the project root directory
project_root = Path.cwd()

block_cipher = None

# Enhanced PyQt6 binary collection
def collect_pyqt6_files():
    """Enhanced PyQt6 binary collection with multiple fallback strategies"""
    binaries = []
    datas = []
    
    print("Collecting PyQt6 files...")
    
    try:
        import PyQt6
        pyqt6_path = Path(PyQt6.__file__).parent
        print(f"PyQt6 found at: {pyqt6_path}")
        
        # Qt6 DLLs to collect
        qt6_dlls = [
            'Qt6Core.dll',
            'Qt6Gui.dll', 
            'Qt6Widgets.dll',
            'Qt6OpenGL.dll',
            'Qt6Svg.dll',
            'Qt6Network.dll',
            'Qt6PrintSupport.dll',
        ]
        
        # Multiple possible locations for Qt6 DLLs
        possible_locations = [
            pyqt6_path / 'Qt6' / 'bin',
            pyqt6_path / 'Qt6' / 'lib',
            pyqt6_path / 'bin',
            pyqt6_path / 'lib',
            pyqt6_path / 'Qt6' / 'DLLs',
        ]
        
        for dll in qt6_dlls:
            found = False
            for location in possible_locations:
                dll_path = location / dll
                if dll_path.exists():
                    binaries.append((str(dll_path), 'Qt6/bin'))
                    print(f"Found {dll} at {dll_path}")
                    found = True
                    break
            if not found:
                print(f"Warning: {dll} not found in any location")
        
        # Collect platform plugins
        possible_plugin_locations = [
            pyqt6_path / 'Qt6' / 'plugins',
            pyqt6_path / 'plugins',
        ]
        
        for plugins_path in possible_plugin_locations:
            if plugins_path.exists():
                datas.append((str(plugins_path), 'Qt6/plugins'))
                print(f"Found plugins at {plugins_path}")
                break
        
        # Collect Qt6 libraries
        possible_lib_locations = [
            pyqt6_path / 'Qt6' / 'lib',
            pyqt6_path / 'lib',
        ]
        
        for lib_path in possible_lib_locations:
            if lib_path.exists():
                datas.append((str(lib_path), 'Qt6/lib'))
                print(f"Found lib at {lib_path}")
                break
                
    except ImportError as e:
        print(f"Warning: PyQt6 not found: {e}")
        print("Skipping Qt6 binary collection")
    
    print(f"Collected {len(binaries)} binaries and {len(datas)} data directories")
    return binaries, datas

# Collect PyQt6 files
pyqt6_binaries, pyqt6_datas = collect_pyqt6_files()

a = Analysis(
    ['main_enhanced_debug.py'],
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
        # Additional PyQt6 modules
        'PyQt6.Qt6.QtCore',
        'PyQt6.Qt6.QtGui',
        'PyQt6.Qt6.QtWidgets',
        'PyQt6.Qt6.QtOpenGL',
        'PyQt6.Qt6.QtSvg',
        'PyQt6.Qt6.QtNetwork',
        'PyQt6.Qt6.QtPrintSupport',
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
    name='ARXMLEditor_Enhanced_Debug',
    debug=True,  # Enable debug mode
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # Disable UPX for debugging
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Always show console for debug
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='arxml_editor.ico' if os.path.exists('arxml_editor.ico') else None,
)

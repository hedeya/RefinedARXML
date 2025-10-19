# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for ARXML Editor Windows build
Optimized for Windows compatibility and performance
"""

import os
import sys
from pathlib import Path

# Get the project root directory - use current working directory instead of __file__
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

# Analysis configuration
a = Analysis(
    ['main_compatible.py'],
    pathex=[str(project_root)],
    binaries=pyqt6_binaries,
    datas=[
        ('examples', 'examples'),
        ('arxml_editor/validation', 'arxml_editor/validation'),
        ('README.md', '.'),
        ('requirements_windows.txt', '.'),
        ('gui_compatibility.py', '.'),
        ('gui_framework_detector.py', '.'),
        ('simple_arxml_model.py', '.'),
    ] + pyqt6_datas,
    hiddenimports=[
        # PySide6 modules (for Python < 3.14)
        'PySide6.QtCore',
        'PySide6.QtGui', 
        'PySide6.QtWidgets',
        'PySide6.QtOpenGL',
        'PySide6.QtOpenGLWidgets',
        'PySide6.QtSvg',
        'PySide6.QtSvgWidgets',
        # PyQt6 modules (for Python >= 3.14)
        'PyQt6.QtCore',
        'PyQt6.QtGui', 
        'PyQt6.QtWidgets',
        'PyQt6.QtOpenGL',
        'PyQt6.QtOpenGLWidgets',
        'PyQt6.QtSvg',
        'PyQt6.QtSvgWidgets',
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
        
        # XML processing
        'xml.etree.ElementTree',
        'lxml',
        'lxml.etree',
        'lxml._elementpath',
        'lxml.html',
        'lxml.html.clean',
        
        # Schema validation
        'xmlschema',
        'xmlschema.validators',
        'xmlschema.validators.schemas',
        
        # Graph algorithms
        'networkx',
        'networkx.algorithms',
        'networkx.algorithms.shortest_paths',
        
        # Plotting and visualization
        'matplotlib',
        'matplotlib.backends.backend_qt5agg',
        'matplotlib.backends.backend_qt5cairo',
        'matplotlib.backends.backend_agg',
        'matplotlib.figure',
        'matplotlib.pyplot',
        
        # Data validation
        'pydantic',
        'pydantic.fields',
        'pydantic.validators',
        'typing_extensions',
        
        # ARXML processing (optional - may not be available)
        # 'autosar_data',
        # 'autosar_data.core',
        # 'autosar_data.schema',
        # 'autosar_data.validation',
        
        # Additional modules that might be needed
        'encodings',
        'encodings.utf_8',
        'encodings.cp1252',
        'encodings.latin_1',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude unnecessary modules to reduce size
        'tkinter',
        'unittest',
        'test',
        'pytest',
        'IPython',
        'jupyter',
        'notebook',
        'sphinx',
        'docutils',
        'setuptools',
        'distutils',
        'pip',
        'wheel',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Remove duplicate binaries and optimize
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Create the executable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ARXMLEditor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(project_root / 'arxml_editor.ico') if (project_root / 'arxml_editor.ico').exists() else None,
    version_file=None,
)

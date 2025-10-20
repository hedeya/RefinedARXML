# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for ARXML Editor Windows build
Optimized for Windows compatibility and performance
"""

import os
import sys
from pathlib import Path

# Get the project root directory. When PyInstaller executes a spec, __file__ may not be
# defined. Fall back to the current working directory in that case.
try:
    project_root = Path(__file__).parent
except NameError:
    project_root = Path('.').resolve()

block_cipher = None

# Analysis configuration
a = Analysis(
    ['arxml_editor/main.py'],
    pathex=[str(project_root)],
    binaries=[],
    datas=[
        ('examples', 'examples'),
        ('arxml_editor/validation', 'arxml_editor/validation'),
        ('README.md', '.'),
        ('requirements_windows.txt', '.'),
    ],
    hiddenimports=[
        # PySide6 modules
        'PySide6.QtCore',
        'PySide6.QtGui', 
        'PySide6.QtWidgets',
        'PySide6.QtOpenGL',
        'PySide6.QtOpenGLWidgets',
        'PySide6.QtSvg',
        'PySide6.QtSvgWidgets',
        
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
        
        # ARXML processing
        'autosar_data',
        'autosar_data.core',
        'autosar_data.schema',
        'autosar_data.validation',
        
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

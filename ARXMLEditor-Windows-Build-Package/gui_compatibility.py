#!/usr/bin/env python3
"""
GUI Compatibility Layer for ARXML Editor

This module provides compatibility between PySide6 and PyQt6
by dynamically importing the appropriate GUI framework.
"""

import sys

def get_gui_imports():
    """Get the appropriate GUI imports based on available framework"""
    # Try PySide6 first (for Python < 3.14)
    try:
        import PySide6
        return {
            'QtCore': 'PySide6.QtCore',
            'QtGui': 'PySide6.QtGui',
            'QtWidgets': 'PySide6.QtWidgets',
            'QtOpenGL': 'PySide6.QtOpenGL',
            'QtOpenGLWidgets': 'PySide6.QtOpenGLWidgets',
            'QtSvg': 'PySide6.QtSvg',
            'QtSvgWidgets': 'PySide6.QtSvgWidgets',
        }
    except ImportError:
        # Fallback to PyQt6 (for Python >= 3.14)
        try:
            import PyQt6
            return {
                'QtCore': 'PyQt6.QtCore',
                'QtGui': 'PyQt6.QtGui',
                'QtWidgets': 'PyQt6.QtWidgets',
                'QtOpenGL': 'PyQt6.QtOpenGL',
                'QtOpenGLWidgets': 'PyQt6.QtOpenGLWidgets',
                'QtSvg': 'PyQt6.QtSvg',
                'QtSvgWidgets': 'PyQt6.QtSvgWidgets',
            }
        except ImportError:
            raise ImportError("Neither PySide6 nor PyQt6 is available. Please install one of them.")

def import_gui_modules():
    """Import GUI modules dynamically"""
    imports = get_gui_imports()
    
    # Import the modules
    QtCore = __import__(imports['QtCore'], fromlist=['QtCore'])
    QtGui = __import__(imports['QtGui'], fromlist=['QtGui'])
    QtWidgets = __import__(imports['QtWidgets'], fromlist=['QtWidgets'])
    
    # Return the modules
    return QtCore, QtGui, QtWidgets

# Make the modules available at module level
try:
    QtCore, QtGui, QtWidgets = import_gui_modules()
except ImportError as e:
    print(f"Error importing GUI framework: {e}")
    print("Please install PySide6 (for Python < 3.14) or PyQt6 (for Python >= 3.14)")
    sys.exit(1)

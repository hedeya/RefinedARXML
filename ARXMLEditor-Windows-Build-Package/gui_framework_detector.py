#!/usr/bin/env python3
"""
GUI Framework Detector for ARXML Editor

This script detects which GUI framework is available and provides
compatibility imports for both PySide6 and PyQt6.
"""

import sys

def detect_gui_framework():
    """Detect which GUI framework is available"""
    try:
        import PySide6
        return 'PySide6'
    except ImportError:
        try:
            import PyQt6
            return 'PyQt6'
        except ImportError:
            return None

def get_gui_imports():
    """Get the appropriate GUI imports based on available framework"""
    framework = detect_gui_framework()
    
    if framework == 'PySide6':
        return {
            'QtCore': 'PySide6.QtCore',
            'QtGui': 'PySide6.QtGui',
            'QtWidgets': 'PySide6.QtWidgets',
            'QtOpenGL': 'PySide6.QtOpenGL',
            'QtOpenGLWidgets': 'PySide6.QtOpenGLWidgets',
            'QtSvg': 'PySide6.QtSvg',
            'QtSvgWidgets': 'PySide6.QtSvgWidgets',
        }
    elif framework == 'PyQt6':
        return {
            'QtCore': 'PyQt6.QtCore',
            'QtGui': 'PyQt6.QtGui',
            'QtWidgets': 'PyQt6.QtWidgets',
            'QtOpenGL': 'PyQt6.QtOpenGL',
            'QtOpenGLWidgets': 'PyQt6.QtOpenGLWidgets',
            'QtSvg': 'PyQt6.QtSvg',
            'QtSvgWidgets': 'PyQt6.QtSvgWidgets',
        }
    else:
        raise ImportError("Neither PySide6 nor PyQt6 is available. Please install one of them.")

def install_gui_framework():
    """Install the appropriate GUI framework based on Python version"""
    if sys.version_info >= (3, 14):
        print("Python 3.14+ detected - installing PyQt6...")
        import subprocess
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'PyQt6', 'PyQt6-Qt6', 'PyQt6-sip'])
    else:
        print("Python < 3.14 detected - installing PySide6...")
        import subprocess
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'PySide6'])

if __name__ == "__main__":
    framework = detect_gui_framework()
    if framework:
        print(f"GUI framework detected: {framework}")
    else:
        print("No GUI framework detected. Installing appropriate framework...")
        install_gui_framework()
        framework = detect_gui_framework()
        if framework:
            print(f"GUI framework installed: {framework}")
        else:
            print("Failed to install GUI framework")
            sys.exit(1)

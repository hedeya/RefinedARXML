"""
PyQt6 Runtime Hook for PyInstaller
This hook helps with PyQt6 DLL loading on Windows
"""

import os
import sys
from pathlib import Path

def hook():
    """Runtime hook to help with PyQt6 loading"""
    if hasattr(sys, '_MEIPASS'):
        # We're running from a PyInstaller bundle
        meipass = Path(sys._MEIPASS)
        
        # Add Qt6 bin directory to PATH
        qt6_bin = meipass / 'Qt6' / 'bin'
        if qt6_bin.exists():
            current_path = os.environ.get('PATH', '')
            os.environ['PATH'] = str(qt6_bin) + os.pathsep + current_path
            print(f"Added Qt6 bin to PATH: {qt6_bin}")
        
        # Set Qt6 plugin path
        qt6_plugins = meipass / 'Qt6' / 'plugins'
        if qt6_plugins.exists():
            os.environ['QT_PLUGIN_PATH'] = str(qt6_plugins)
            print(f"Set QT_PLUGIN_PATH: {qt6_plugins}")
        
        # Set Qt6 library path
        qt6_lib = meipass / 'Qt6' / 'lib'
        if qt6_lib.exists():
            os.environ['QT_LIBRARY_PATH'] = str(qt6_lib)
            print(f"Set QT_LIBRARY_PATH: {qt6_lib}")

# Call the hook when this module is imported
hook()

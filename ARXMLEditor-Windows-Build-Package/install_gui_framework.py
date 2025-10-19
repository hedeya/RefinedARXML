#!/usr/bin/env python3
"""
GUI Framework Installation Script

This script installs the appropriate GUI framework based on Python version.
"""

import sys
import subprocess

def install_gui_framework():
    """Install the appropriate GUI framework based on Python version"""
    print(f"Python version: {sys.version}")
    
    if sys.version_info >= (3, 14):
        print("Python 3.14+ detected - installing PyQt6...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'PyQt6', 'PyQt6-Qt6', 'PyQt6-sip'], check=True)
            print("PyQt6 installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install PyQt6: {e}")
            return False
    else:
        print("Python < 3.14 detected - installing PySide6...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'PySide6'], check=True)
            print("PySide6 installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install PySide6: {e}")
            return False
    
    return True

if __name__ == "__main__":
    success = install_gui_framework()
    if success:
        print("GUI framework installation completed successfully!")
    else:
        print("GUI framework installation failed!")
        sys.exit(1)

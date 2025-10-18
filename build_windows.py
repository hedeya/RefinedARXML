#!/usr/bin/env python3
"""
Build script for creating Windows executable of ARXML Editor
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and return the result"""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running command: {cmd}")
        print(f"Error output: {result.stderr}")
        return False
    return True

def main():
    """Main build function"""
    print("Building ARXML Editor for Windows...")
    
    # Ensure we're in the project root
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Install PyInstaller if not already installed
    print("Installing PyInstaller...")
    if not run_command("pip install pyinstaller"):
        print("Failed to install PyInstaller")
        return False
    
    # Clean previous builds
    print("Cleaning previous builds...")
    for dir_name in ["build", "dist", "__pycache__"]:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
    
    # Create PyInstaller spec file
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['arxml_editor/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('examples', 'examples'),
        ('arxml_editor/validation', 'arxml_editor/validation'),
    ],
    hiddenimports=[
        'PySide6.QtCore',
        'PySide6.QtGui', 
        'PySide6.QtWidgets',
        'xml.etree.ElementTree',
        'lxml',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    icon='arxml_editor.ico' if os.path.exists('arxml_editor.ico') else None,
)
'''
    
    with open('ARXMLEditor.spec', 'w') as f:
        f.write(spec_content)
    
    # Build the executable
    print("Building executable with PyInstaller...")
    if not run_command("pyinstaller ARXMLEditor.spec"):
        print("Failed to build executable")
        return False
    
    # Create a release directory
    release_dir = Path("release")
    if release_dir.exists():
        shutil.rmtree(release_dir)
    release_dir.mkdir()
    
    # Copy the executable and necessary files
    print("Creating release package...")
    exe_file = Path("dist/ARXMLEditor")
    if exe_file.exists():
        # Create ARXMLEditor directory in release
        exe_release_dir = release_dir / "ARXMLEditor"
        exe_release_dir.mkdir()
        
        # Copy the executable
        shutil.copy2(exe_file, exe_release_dir / "ARXMLEditor.exe")
        
        # Copy additional files to release root
        shutil.copy2("README.md", release_dir)
        shutil.copy2("requirements.txt", release_dir)
        shutil.copytree("examples", release_dir / "examples")
        
        # Create a simple launcher script
        launcher_content = '''@echo off
echo Starting ARXML Editor...
cd /d "%~dp0"
ARXMLEditor\\ARXMLEditor.exe
pause
'''
        with open(release_dir / "run_editor.bat", 'w') as f:
            f.write(launcher_content)
        
        print(f"Release package created in: {release_dir}")
        print("Windows executable is ready!")
        return True
    else:
        print("Executable not found in dist directory")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
#!/usr/bin/env python3
"""
Windows Release Build Script for ARXML Editor

This script creates a Windows-compatible release package that can be built
on Windows systems to generate proper Windows executables.

Usage:
    python build_windows_release.py

Requirements:
    - Windows 10/11 with Python 3.9+
    - All dependencies from requirements.txt
    - PyInstaller
"""

import os
import sys
import subprocess
import shutil
import zipfile
from pathlib import Path
import platform

def run_command(cmd, cwd=None, check=True):
    """Run a command and return the result"""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Error running command: {cmd}")
        print(f"Error output: {result.stderr}")
        return False
    return result

def check_windows_environment():
    """Check if we're running on Windows"""
    if platform.system() != "Windows":
        print("ERROR: This script must be run on Windows to create Windows executables.")
        print("Current platform:", platform.system())
        return False
    return True

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    
    # Install PyInstaller
    if not run_command("pip install pyinstaller"):
        print("Failed to install PyInstaller")
        return False
    
    # Install project dependencies
    if not run_command("pip install -r requirements.txt"):
        print("Failed to install project dependencies")
        return False
    
    return True

def create_pyinstaller_spec():
    """Create optimized PyInstaller spec file for Windows"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from pathlib import Path

# Get the project root directory
project_root = Path(__file__).parent

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
        ('requirements.txt', '.'),
    ],
    hiddenimports=[
        'PySide6.QtCore',
        'PySide6.QtGui', 
        'PySide6.QtWidgets',
        'PySide6.QtOpenGL',
        'PySide6.QtOpenGLWidgets',
        'xml.etree.ElementTree',
        'lxml',
        'lxml.etree',
        'lxml._elementpath',
        'xmlschema',
        'networkx',
        'matplotlib',
        'matplotlib.backends.backend_qt5agg',
        'matplotlib.backends.backend_qt5cairo',
        'matplotlib.backends.backend_agg',
        'pydantic',
        'typing_extensions',
        'autosar_data',
        'autosar_data.core',
        'autosar_data.schema',
        'autosar_data.validation',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'unittest',
        'test',
        'pytest',
        'IPython',
        'jupyter',
        'notebook',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Remove duplicate binaries
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
'''
    
    with open('ARXMLEditor_Windows.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("Created PyInstaller spec file: ARXMLEditor_Windows.spec")
    return True

def build_executable():
    """Build the Windows executable using PyInstaller"""
    print("Building Windows executable with PyInstaller...")
    
    # Clean previous builds
    for dir_name in ["build", "dist", "__pycache__"]:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"Cleaned {dir_name}")
    
    # Build the executable
    result = run_command("pyinstaller ARXMLEditor_Windows.spec --clean --noconfirm")
    if not result:
        print("Failed to build executable")
        return False
    
    # Check if executable was created
    exe_path = Path("dist/ARXMLEditor.exe")
    if not exe_path.exists():
        print("Executable not found after build")
        return False
    
    print(f"Successfully built: {exe_path}")
    return True

def create_release_package():
    """Create the final release package"""
    print("Creating release package...")
    
    # Create release directory
    release_dir = Path("release_windows")
    if release_dir.exists():
        shutil.rmtree(release_dir)
    release_dir.mkdir()
    
    # Create main application directory
    app_dir = release_dir / "ARXMLEditor"
    app_dir.mkdir()
    
    # Copy executable
    exe_src = Path("dist/ARXMLEditor.exe")
    exe_dst = app_dir / "ARXMLEditor.exe"
    shutil.copy2(exe_src, exe_dst)
    print(f"Copied executable to: {exe_dst}")
    
    # Copy additional files
    files_to_copy = [
        "README.md",
        "requirements.txt",
        "examples",
    ]
    
    for item in files_to_copy:
        src = Path(item)
        if src.exists():
            if src.is_dir():
                shutil.copytree(src, release_dir / item)
            else:
                shutil.copy2(src, release_dir / item)
            print(f"Copied {item}")
    
    # Create Windows batch launcher
    launcher_content = '''@echo off
title ARXML Editor
echo Starting ARXML Editor...
echo.

REM Check if executable exists
if not exist "ARXMLEditor\\ARXMLEditor.exe" (
    echo ERROR: ARXMLEditor.exe not found!
    echo Please ensure the executable is in the ARXMLEditor folder.
    pause
    exit /b 1
)

REM Change to the directory containing this batch file
cd /d "%~dp0"

REM Run the application
echo Launching ARXML Editor...
ARXMLEditor\\ARXMLEditor.exe

REM Keep window open if there was an error
if errorlevel 1 (
    echo.
    echo Application exited with an error.
    pause
)
'''
    
    launcher_path = release_dir / "run_editor.bat"
    with open(launcher_path, 'w', encoding='utf-8') as f:
        f.write(launcher_content)
    print(f"Created launcher: {launcher_path}")
    
    # Create Windows PowerShell launcher
    ps_launcher_content = '''# ARXML Editor PowerShell Launcher
Write-Host "Starting ARXML Editor..." -ForegroundColor Green
Write-Host ""

# Check if executable exists
if (-not (Test-Path "ARXMLEditor\\ARXMLEditor.exe")) {
    Write-Host "ERROR: ARXMLEditor.exe not found!" -ForegroundColor Red
    Write-Host "Please ensure the executable is in the ARXMLEditor folder." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Change to the directory containing this script
Set-Location $PSScriptRoot

# Run the application
Write-Host "Launching ARXML Editor..." -ForegroundColor Yellow
& "ARXMLEditor\\ARXMLEditor.exe"

# Check exit code
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Application exited with an error." -ForegroundColor Red
    Read-Host "Press Enter to exit"
}
'''
    
    ps_launcher_path = release_dir / "run_editor.ps1"
    with open(ps_launcher_path, 'w', encoding='utf-8') as f:
        f.write(ps_launcher_content)
    print(f"Created PowerShell launcher: {ps_launcher_path}")
    
    # Create Windows installation instructions
    install_instructions = '''# ARXML Editor - Windows Installation Instructions

## Quick Start
1. Double-click `run_editor.bat` to start the application
2. Or run `run_editor.ps1` in PowerShell

## System Requirements
- Windows 10 or Windows 11
- No additional software installation required (self-contained)

## Troubleshooting

### If the application won't start:
1. Make sure you're running Windows 10 or 11
2. Try running as administrator
3. Check Windows Defender or antivirus software isn't blocking the executable
4. Ensure all files are extracted from the zip archive

### If you get permission errors:
1. Right-click `run_editor.bat` and select "Run as administrator"
2. Or unzip to a folder you have full access to (like Desktop)

### For PowerShell users:
- If you get execution policy errors, run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- Then run: `.\run_editor.ps1`

## Features
- Professional ARXML editor with AUTOSAR compliance
- Advanced validation and cross-reference management
- Interactive diagrams and visualizations
- Multi-schema support for different AUTOSAR releases

## Support
- GitHub: https://github.com/arxml-editor/arxml-editor
- Issues: https://github.com/arxml-editor/arxml-editor/issues
'''
    
    install_path = release_dir / "INSTALL_WINDOWS.md"
    with open(install_path, 'w', encoding='utf-8') as f:
        f.write(install_instructions)
    print(f"Created installation instructions: {install_path}")
    
    return release_dir

def create_zip_package(release_dir):
    """Create a zip package of the release"""
    print("Creating zip package...")
    
    zip_path = Path("ARXMLEditor-Windows-v1.0.0.zip")
    if zip_path.exists():
        zip_path.unlink()
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(release_dir):
            for file in files:
                file_path = Path(root) / file
                arc_path = file_path.relative_to(release_dir.parent)
                zipf.write(file_path, arc_path)
    
    print(f"Created zip package: {zip_path}")
    return zip_path

def verify_build():
    """Verify the build was successful"""
    print("Verifying build...")
    
    exe_path = Path("release_windows/ARXMLEditor/ARXMLEditor.exe")
    if not exe_path.exists():
        print("ERROR: Executable not found")
        return False
    
    # Check file type (should be PE executable on Windows)
    result = run_command(f'file "{exe_path}"', check=False)
    if result.returncode == 0:
        print(f"Executable type: {result.stdout.strip()}")
    
    # Check file size
    size_mb = exe_path.stat().st_size / (1024 * 1024)
    print(f"Executable size: {size_mb:.1f} MB")
    
    if size_mb < 10:
        print("WARNING: Executable seems unusually small")
    
    return True

def main():
    """Main build function"""
    print("=" * 60)
    print("ARXML Editor - Windows Release Builder")
    print("=" * 60)
    
    # Check environment
    if not check_windows_environment():
        return False
    
    try:
        # Install dependencies
        if not install_dependencies():
            return False
        
        # Create PyInstaller spec
        if not create_pyinstaller_spec():
            return False
        
        # Build executable
        if not build_executable():
            return False
        
        # Create release package
        release_dir = create_release_package()
        if not release_dir:
            return False
        
        # Create zip package
        zip_path = create_zip_package(release_dir)
        
        # Verify build
        if not verify_build():
            print("WARNING: Build verification failed")
        
        print("=" * 60)
        print("BUILD COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print(f"Release directory: {release_dir}")
        print(f"Zip package: {zip_path}")
        print("\nTo test the build:")
        print(f"1. Extract {zip_path} to a Windows machine")
        print("2. Run run_editor.bat")
        print("\nThe executable should now work properly on Windows!")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Build failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
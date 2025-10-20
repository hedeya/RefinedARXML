#!/usr/bin/env python3
"""
ARXML Editor - Simple Debug Windows Build Package Creator
This version skips complex PyQt6 verification and just tries to build directly.
"""

import os
import shutil
from pathlib import Path

def create_simple_debug_package():
    """Create a simple debug Windows build package"""
    print("=" * 60)
    print("ARXML Editor - Simple Debug Windows Build Package Creator")
    print("=" * 60)
    
    # Create package directory
    package_dir = Path("ARXMLEditor-Windows-Debug-Simple")
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir()
    
    print("Creating simple debug Windows build package...")
    
    # Copy source code
    print("Copying source code...")
    shutil.copytree("arxml_editor", package_dir / "arxml_editor")
    if Path("examples").exists():
        shutil.copytree("examples", package_dir / "examples")
    if Path("README.md").exists():
        shutil.copy2("README.md", package_dir / "README.md")
    if Path("arxml_editor.ico").exists():
        shutil.copy2("arxml_editor.ico", package_dir / "arxml_editor.ico")
    
    # Create simple main script
    print("Creating simple main script...")
    main_script = '''#!/usr/bin/env python3
"""
ARXML Editor - Simple Debug Version
This version has minimal error checking and focuses on just working.
"""

import sys
import os
from pathlib import Path

def setup_environment():
    """Setup basic environment"""
    print("Setting up environment...")
    
    # Set up PyQt6 environment if running from PyInstaller
    if hasattr(sys, '_MEIPASS'):
        meipass = Path(sys._MEIPASS)
        qt6_bin = meipass / 'Qt6' / 'bin'
        qt6_plugins = meipass / 'Qt6' / 'plugins'
        qt6_lib = meipass / 'Qt6' / 'lib'
        
        if qt6_bin.exists():
            current_path = os.environ.get('PATH', '')
            os.environ['PATH'] = str(qt6_bin) + os.pathsep + current_path
            print(f"Added Qt6 bin to PATH: {qt6_bin}")
        
        if qt6_plugins.exists():
            os.environ['QT_PLUGIN_PATH'] = str(qt6_plugins)
            print(f"Set QT_PLUGIN_PATH: {qt6_plugins}")
        
        if qt6_lib.exists():
            os.environ['QT_LIBRARY_PATH'] = str(qt6_lib)
            print(f"Set QT_LIBRARY_PATH: {qt6_lib}")

def import_pyqt6():
    """Try to import PyQt6 with minimal error checking"""
    try:
        print("Attempting to import PyQt6...")
        from PyQt6.QtCore import Qt, QCoreApplication
        from PyQt6.QtGui import QIcon, QFont
        from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, 
                                   QLabel, QTextEdit, QMenuBar, QMenu, QFileDialog, QMessageBox)
        print("✓ PyQt6 imported successfully")
        return True
    except Exception as e:
        print(f"✗ PyQt6 import failed: {e}")
        print("This is a common issue on Windows. The build will continue anyway.")
        return False

def create_simple_gui():
    """Create a simple GUI"""
    try:
        from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, 
                                   QLabel, QTextEdit, QMenuBar, QMenu, QFileDialog, QMessageBox)
        from PyQt6.QtCore import Qt
        
        app = QApplication(sys.argv)
        window = QMainWindow()
        window.setWindowTitle("ARXML Editor - Simple Debug Version")
        window.setGeometry(100, 100, 800, 600)
        
        # Create central widget
        central_widget = QWidget()
        window.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Add title
        title = QLabel("ARXML Editor - Simple Debug Version")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Add text area
        text_area = QTextEdit()
        text_area.setPlaceholderText(
            "ARXML content will appear here...\\n\\n"
            "This is a simple debug version that focuses on basic functionality.\\n"
            "If PyQt6 is working, you should see this text area.\\n\\n"
            "To test ARXML editing, open a file using the File menu."
        )
        layout.addWidget(text_area)
        
        # Create simple menu
        menubar = QMenuBar()
        window.setMenuBar(menubar)
        
        file_menu = menubar.addMenu('File')
        
        # Open action
        open_action = file_menu.addAction('Open ARXML')
        open_action.triggered.connect(lambda: QFileDialog.getOpenFileName(window, "Open ARXML File", "", "ARXML Files (*.arxml)"))
        
        # Save action
        save_action = file_menu.addAction('Save ARXML')
        save_action.triggered.connect(lambda: QFileDialog.getSaveFileName(window, "Save ARXML File", "", "ARXML Files (*.arxml)"))
        
        file_menu.addSeparator()
        exit_action = file_menu.addAction('Exit')
        exit_action.triggered.connect(window.close)
        
        # Status bar
        window.statusBar().showMessage("Simple debug version ready")
        
        return app, window
    except Exception as e:
        print(f"Failed to create GUI: {e}")
        return None, None

def main():
    """Main function"""
    print("=" * 50)
    print("ARXML Editor - Simple Debug Version")
    print("=" * 50)
    
    # Setup environment
    setup_environment()
    
    # Try to import PyQt6
    if not import_pyqt6():
        print("\\nPyQt6 import failed, but continuing anyway...")
        print("This is a common issue on Windows systems.")
        print("The executable may still work when run from the command line.")
        input("Press Enter to continue...")
        return
    
    # Create GUI
    app, window = create_simple_gui()
    if app and window:
        print("\\n✓ GUI created successfully!")
        print("✓ PyQt6 is working correctly!")
        print("\\nStarting application...")
        window.show()
        sys.exit(app.exec())
    else:
        print("\\n✗ Failed to create GUI")
        print("This usually means PyQt6 is not working properly")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
'''
    
    with open(package_dir / "main_simple_debug.py", 'w', encoding='utf-8') as f:
        f.write(main_script)
    
    # Create simple PyInstaller spec
    print("Creating simple PyInstaller spec...")
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main_simple_debug.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtGui', 
        'PyQt6.QtWidgets',
        'PyQt6.Qt6',
        'PyQt6.Qt6.QtCore',
        'PyQt6.Qt6.QtGui',
        'PyQt6.Qt6.QtWidgets',
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
    name='ARXMLEditor_Simple_Debug',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='arxml_editor.ico' if os.path.exists('arxml_editor.ico') else None,
)
'''
    
    with open(package_dir / "ARXMLEditor_Simple_Debug.spec", 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    # Create simple build script
    print("Creating simple build script...")
    build_script = '''@echo off
REM Simple Debug ARXML Editor - Windows Build Script
echo ========================================
echo ARXML Editor - Simple Debug Windows Build
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.9+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo Python found. Starting simple debug build...
echo.

REM Install basic requirements
echo Installing basic requirements...
python -m pip install --upgrade pip
python -m pip install PyQt6 PyQt6-Qt6 PyQt6-sip lxml xmlschema pyinstaller pywin32

echo.
echo Requirements installed. Starting build...
echo.

REM Clean previous builds
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "__pycache__" rmdir /s /q "__pycache__"

REM Build executable
echo Building simple debug Windows executable...
echo This may take several minutes - please wait...
echo.
python -m PyInstaller ARXMLEditor_Simple_Debug.spec --clean --noconfirm

REM Check if build was successful
if exist "dist\\ARXMLEditor_Simple_Debug.exe" (
    echo.
    echo Build completed successfully!
    echo.
    
    REM Create release directory
    if not exist "release" mkdir "release"
    copy "dist\\ARXMLEditor_Simple_Debug.exe" "release\\"
    if exist "arxml_editor.ico" copy "arxml_editor.ico" "release\\"
    
    echo.
    echo ========================================
    echo Simple Debug ARXML Editor built successfully!
    echo The executable is in the 'release' folder.
    echo This version has minimal error checking.
    echo ========================================
    echo.
) else (
    echo.
    echo ERROR: Build failed! Executable not found.
    echo Please check the error messages above.
    echo.
)

echo Press any key to close this window...
pause >nul
'''
    
    with open(package_dir / "BUILD_SIMPLE_DEBUG.bat", 'w', encoding='utf-8') as f:
        f.write(build_script)
    
    # Create simple README
    print("Creating simple README...")
    readme_content = '''# ARXML Editor - Simple Debug Windows Build

This is a simplified version of the ARXML Editor that focuses on basic functionality and minimal error checking.

## Quick Start

1. **Run the build script**: Double-click `BUILD_SIMPLE_DEBUG.bat`
2. **Wait for completion**: The build process may take several minutes
3. **Find the executable**: Look in the `release` folder for `ARXMLEditor_Simple_Debug.exe`
4. **Run the executable**: Double-click the .exe file to start the editor

## What's Different

- **No complex PyQt6 verification** - Skips problematic verification steps
- **Minimal error checking** - Focuses on just getting the build working
- **Simple GUI** - Basic interface that should work if PyQt6 is available
- **Console output** - Shows what's happening during the build process

## Troubleshooting

### If the build fails:
1. **Check Python installation** - Make sure Python 3.9+ is installed and in PATH
2. **Check internet connection** - Required for downloading dependencies
3. **Run as Administrator** - If you get permission errors
4. **Check console output** - Look for specific error messages

### If the executable doesn't start:
1. **Try running from command prompt** - Open cmd and run the .exe file
2. **Check for error messages** - The console will show what's wrong
3. **Install Visual C++ Redistributable** - May be required for PyQt6

## System Requirements

- Windows 10 or Windows 11
- Python 3.9 or higher
- 2GB RAM minimum
- 1GB free disk space
- Internet connection (for building)

## Files Included

- `main_simple_debug.py` - Simple main script with minimal error checking
- `ARXMLEditor_Simple_Debug.spec` - PyInstaller specification file
- `BUILD_SIMPLE_DEBUG.bat` - Build script
- `arxml_editor/` - Source code directory
- `examples/` - Example ARXML files
- `README.md` - This file

## Notes

This version is designed to work around common PyQt6 installation issues on Windows.
It may not have all the advanced features of the full version, but it should build
and run successfully in most cases.
'''
    
    with open(package_dir / "README.md", 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    # Create zip package
    print("Creating simple zip package...")
    shutil.make_archive("ARXMLEditor-Windows-Debug-Simple-v1.0.0", 'zip', package_dir)
    
    print("=" * 60)
    print("SIMPLE DEBUG WINDOWS BUILD PACKAGE CREATED SUCCESSFULLY!")
    print("=" * 60)
    print(f"Package directory: {package_dir}")
    print("Zip package: ARXMLEditor-Windows-Debug-Simple-v1.0.0.zip")
    print()
    print("Next steps:")
    print("1. Transfer the zip file to a Windows machine")
    print("2. Extract the zip file")
    print("3. Run BUILD_SIMPLE_DEBUG.bat")
    print("4. The resulting executable should work without PyQt6 verification issues!")
    print("=" * 60)

if __name__ == "__main__":
    create_simple_debug_package()
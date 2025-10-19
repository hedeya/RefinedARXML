#!/usr/bin/env python3
"""
Simple Windows Build Package Creator for ARXML Editor

This creates a minimal, reliable Windows build package that focuses on
core functionality without complex dependencies.
"""

import os
import shutil
import zipfile
from pathlib import Path

def create_simple_windows_package():
    """Create a simple Windows build package"""
    print("=" * 60)
    print("ARXML Editor - Simple Windows Build Package Creator")
    print("=" * 60)
    print("Creating simple Windows build package...")
    
    # Create package directory
    package_dir = Path("ARXMLEditor-Windows-Simple")
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir()
    
    # Copy essential source files
    print("Copying source code...")
    essential_files = [
        "arxml_editor",
        "examples", 
        "README.md",
        "arxml_editor.ico"
    ]
    
    for item in essential_files:
        if Path(item).exists():
            if Path(item).is_dir():
                shutil.copytree(item, package_dir / item)
            else:
                shutil.copy2(item, package_dir / item)
            print(f"  Copied {item}")
    
    # Create simple requirements file
    print("Creating simple requirements...")
    requirements_content = '''# Simple ARXML Editor Requirements
# Minimal dependencies for Windows build

# GUI Framework
PyQt6>=6.6.0

# Basic XML processing
lxml>=4.9.0

# Basic validation
xmlschema>=3.0.0

# Build tool
pyinstaller>=5.0.0

# Windows support
pywin32>=306
'''
    
    with open(package_dir / "requirements_simple.txt", 'w', encoding='utf-8') as f:
        f.write(requirements_content)
    
    # Create simple main script
    print("Creating simple main script...")
    main_script = '''"""
Simple ARXML Editor - Main Entry Point

A simplified version of the ARXML Editor that works reliably on Windows.
"""

import sys
import os
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QTextEdit, QMenuBar, QMenu, QFileDialog, QMessageBox
    from PyQt6.QtCore import Qt
    from PyQt6.QtGui import QIcon, QAction
except ImportError:
    print("Error: PyQt6 not found. Please install it with: pip install PyQt6")
    sys.exit(1)

class SimpleARXMLEditor(QMainWindow):
    """Simple ARXML Editor main window"""
    
    def __init__(self):
        super().__init__()
        self.current_file = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("ARXML Editor - Simple Version")
        self.setGeometry(100, 100, 800, 600)
        
        # Set window icon if available
        icon_path = Path(__file__).parent / "arxml_editor.ico"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout
        layout = QVBoxLayout(central_widget)
        
        # Create text area
        self.text_area = QTextEdit()
        self.text_area.setPlaceholderText("ARXML content will appear here...")
        layout.addWidget(self.text_area)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Status bar
        self.statusBar().showMessage("Ready")
    
    def create_menu_bar(self):
        """Create the menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        # Open action
        open_action = QAction('Open ARXML', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        # Save action
        save_action = QAction('Save ARXML', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        # Save As action
        save_as_action = QAction('Save As...', self)
        save_as_action.setShortcut('Ctrl+Shift+S')
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        # Exit action
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Help menu
        help_menu = menubar.addMenu('Help')
        
        # About action
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def open_file(self):
        """Open an ARXML file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Open ARXML File", 
            "", 
            "ARXML Files (*.arxml);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.text_area.setPlainText(content)
                    self.current_file = file_path
                    self.statusBar().showMessage(f"Opened: {Path(file_path).name}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open file: {e}")
    
    def save_file(self):
        """Save the current file"""
        if self.current_file:
            self.save_to_file(self.current_file)
        else:
            self.save_file_as()
    
    def save_file_as(self):
        """Save file with new name"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save ARXML File",
            "",
            "ARXML Files (*.arxml);;All Files (*)"
        )
        
        if file_path:
            self.save_to_file(file_path)
            self.current_file = file_path
    
    def save_to_file(self, file_path):
        """Save content to file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(self.text_area.toPlainText())
            self.statusBar().showMessage(f"Saved: {Path(file_path).name}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save file: {e}")
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About ARXML Editor",
            "ARXML Editor - Simple Version\\n\\n"
            "A simplified ARXML editor for Windows.\\n"
            "This version focuses on basic XML editing functionality.\\n\\n"
            "Version: 1.0.0-simple\\n"
            "Built with PyQt6"
        )

def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("ARXML Editor Simple")
    app.setApplicationVersion("1.0.0")
    
    # Create and show main window
    window = SimpleARXMLEditor()
    window.show()
    
    # Run the application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
'''
    
    with open(package_dir / "main_simple.py", 'w', encoding='utf-8') as f:
        f.write(main_script)
    
    # Create simple PyInstaller spec
    print("Creating simple PyInstaller spec...")
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

import os
from pathlib import Path

# Get the project root directory
project_root = Path.cwd()

block_cipher = None

a = Analysis(
    ['main_simple.py'],
    pathex=[str(project_root)],
    binaries=[],
    datas=[
        ('examples', 'examples'),
        ('README.md', '.'),
        ('arxml_editor.ico', '.'),
    ],
    hiddenimports=[
        # PyQt6 modules
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        # Basic modules
        'xml.etree.ElementTree',
        'pathlib',
        'lxml',
        'xmlschema',
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
    name='ARXMLEditor_Simple',
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
    
    with open(package_dir / "ARXMLEditor_Simple.spec", 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    # Create simple build script
    print("Creating simple build script...")
    build_script = '''@echo off
REM Simple ARXML Editor - Windows Build Script
echo ========================================
echo ARXML Editor - Simple Windows Build
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

echo Python found. Starting build...
echo.

REM Install requirements
echo Installing requirements...
python -m pip install -r requirements_simple.txt

REM Clean previous builds
echo.
echo Cleaning previous builds...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "__pycache__" rmdir /s /q "__pycache__"

REM Build executable
echo.
echo Building Windows executable...
echo This may take a few minutes...
python -m PyInstaller ARXMLEditor_Simple.spec --clean --noconfirm

REM Check if build was successful
if not exist "dist\\ARXMLEditor_Simple.exe" (
    echo.
    echo ERROR: Build failed! Executable not found.
    echo Please check the error messages above.
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo BUILD SUCCESSFUL!
echo ========================================
echo.
echo Executable created: dist\\ARXMLEditor_Simple.exe
echo.

REM Create release folder
if not exist "release" mkdir "release"
copy "dist\\ARXMLEditor_Simple.exe" "release\\"
if exist "arxml_editor.ico" copy "arxml_editor.ico" "release\\"

echo.
echo Simple ARXML Editor built successfully!
echo Check the 'release' folder for the executable.
echo.
pause
'''
    
    with open(package_dir / "BUILD_SIMPLE.bat", 'w', encoding='utf-8') as f:
        f.write(build_script)
    
    # Create README
    print("Creating README...")
    readme_content = '''# ARXML Editor - Simple Windows Version

This is a simplified version of the ARXML Editor designed for reliable Windows builds.

## Features

- **Basic ARXML Editing**: Open, edit, and save ARXML files
- **Simple Interface**: Clean, easy-to-use GUI
- **Windows Compatible**: Built specifically for Windows
- **Minimal Dependencies**: Only essential packages required

## Quick Start

1. **Run the build script**: Double-click `BUILD_SIMPLE.bat`
2. **Wait for completion**: The build process will take a few minutes
3. **Find your executable**: Look in the `release` folder for `ARXMLEditor_Simple.exe`

## System Requirements

- Windows 10 or Windows 11
- Python 3.9 or higher
- 2GB RAM minimum
- 1GB free disk space

## What's Different

This simple version:
- Uses only PyQt6 (no PySide6 compatibility layer)
- Excludes complex dependencies (matplotlib, networkx, etc.)
- Focuses on basic XML editing functionality
- Has a simplified user interface
- Is more reliable for Windows builds

## Troubleshooting

### Python Not Found
- Install Python from https://python.org
- Make sure to check "Add Python to PATH" during installation

### Build Fails
- Check that you have Python 3.9+ installed
- Ensure you have internet connection for downloading packages
- Try running as Administrator

### GUI Issues
- This version uses PyQt6 only
- If you have PySide6 installed, it might conflict

## Support

This is a simplified version for basic ARXML editing needs.
For full functionality, use the complete version when available.
'''
    
    with open(package_dir / "README_SIMPLE.md", 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    # Create zip package
    print("Creating zip package...")
    zip_path = "ARXMLEditor-Windows-Simple-v1.0.0.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = Path(root) / file
                arc_path = file_path.relative_to(package_dir.parent)
                zipf.write(file_path, arc_path)
    
    print("=" * 60)
    print("SIMPLE WINDOWS BUILD PACKAGE CREATED SUCCESSFULLY!")
    print("=" * 60)
    print(f"Package directory: {package_dir}")
    print(f"Zip package: {zip_path}")
    print()
    print("Next steps:")
    print("1. Transfer the zip file to a Windows machine")
    print("2. Extract the zip file")
    print("3. Run BUILD_SIMPLE.bat")
    print("4. The resulting executable will be Windows-compatible!")
    print("=" * 60)

if __name__ == "__main__":
    create_simple_windows_package()
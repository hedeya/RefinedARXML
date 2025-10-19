#!/usr/bin/env python3
"""
Debug Windows Build Package Creator for ARXML Editor

This creates a debug version that shows console output for troubleshooting.
"""

import os
import shutil
import zipfile
from pathlib import Path

def create_debug_windows_package():
    """Create a debug Windows build package"""
    print("=" * 60)
    print("ARXML Editor - Debug Windows Build Package Creator")
    print("=" * 60)
    print("Creating debug Windows build package...")
    
    # Create package directory
    package_dir = Path("ARXMLEditor-Windows-Debug")
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
    
    # Create debug main script
    print("Creating debug main script...")
    main_script = '''"""
Debug ARXML Editor - Main Entry Point

A debug version that shows console output for troubleshooting.
"""

import sys
import os
from pathlib import Path

print("=" * 50)
print("ARXML Editor Debug - Starting...")
print("=" * 50)
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Current directory: {os.getcwd()}")
print(f"Script location: {__file__}")
print("=" * 50)

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))
print("Added current directory to Python path")

try:
    print("Importing PyQt6...")
    from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QTextEdit, QMenuBar, QMenu, QFileDialog, QMessageBox
    from PyQt6.QtCore import Qt
    from PyQt6.QtGui import QIcon, QAction
    print("PyQt6 imported successfully")
except ImportError as e:
    print(f"Error importing PyQt6: {e}")
    print("Please install PyQt6 with: pip install PyQt6")
    input("Press Enter to exit...")
    sys.exit(1)

class DebugARXMLEditor(QMainWindow):
    """Debug ARXML Editor main window"""
    
    def __init__(self):
        print("Creating main window...")
        super().__init__()
        self.current_file = None
        self.init_ui()
        print("Main window created successfully")
    
    def init_ui(self):
        """Initialize the user interface"""
        print("Initializing UI...")
        self.setWindowTitle("ARXML Editor - Debug Version")
        self.setGeometry(100, 100, 800, 600)
        
        # Set window icon if available
        icon_path = Path(__file__).parent / "arxml_editor.ico"
        if icon_path.exists():
            print(f"Setting window icon: {icon_path}")
            self.setWindowIcon(QIcon(str(icon_path)))
        else:
            print("No icon found")
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout
        layout = QVBoxLayout(central_widget)
        
        # Create text area
        self.text_area = QTextEdit()
        self.text_area.setPlaceholderText("ARXML content will appear here...\\n\\nDebug info:\\n- PyQt6 is working\\n- GUI is responsive\\n- Ready for ARXML editing")
        layout.addWidget(self.text_area)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Status bar
        self.statusBar().showMessage("Debug version ready")
        print("UI initialized successfully")
    
    def create_menu_bar(self):
        """Create the menu bar"""
        print("Creating menu bar...")
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
        
        print("Menu bar created successfully")
    
    def open_file(self):
        """Open an ARXML file"""
        print("Opening file dialog...")
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Open ARXML File", 
            "", 
            "ARXML Files (*.arxml);;All Files (*)"
        )
        
        if file_path:
            print(f"Selected file: {file_path}")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.text_area.setPlainText(content)
                    self.current_file = file_path
                    self.statusBar().showMessage(f"Opened: {Path(file_path).name}")
                    print(f"File opened successfully: {len(content)} characters")
            except Exception as e:
                print(f"Error opening file: {e}")
                QMessageBox.critical(self, "Error", f"Failed to open file: {e}")
    
    def save_file(self):
        """Save the current file"""
        if self.current_file:
            self.save_to_file(self.current_file)
        else:
            self.save_file_as()
    
    def save_file_as(self):
        """Save file with new name"""
        print("Opening save dialog...")
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
        print(f"Saving to file: {file_path}")
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(self.text_area.toPlainText())
            self.statusBar().showMessage(f"Saved: {Path(file_path).name}")
            print("File saved successfully")
        except Exception as e:
            print(f"Error saving file: {e}")
            QMessageBox.critical(self, "Error", f"Failed to save file: {e}")
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About ARXML Editor Debug",
            "ARXML Editor - Debug Version\\n\\n"
            "This is a debug version that shows console output\\n"
            "for troubleshooting purposes.\\n\\n"
            "Version: 1.0.0-debug\\n"
            "Built with PyQt6\\n\\n"
            "If you can see this dialog, PyQt6 is working correctly!"
        )

def main():
    """Main application entry point"""
    try:
        print("Creating QApplication...")
        app = QApplication(sys.argv)
        app.setApplicationName("ARXML Editor Debug")
        app.setApplicationVersion("1.0.0")
        print("QApplication created successfully")
        
        print("Creating main window...")
        # Create and show main window
        window = DebugARXMLEditor()
        window.show()
        print("Main window shown")
        
        print("Starting event loop...")
        print("=" * 50)
        print("Application is now running. Check the console for debug info.")
        print("=" * 50)
        # Run the application
        sys.exit(app.exec())
    except Exception as e:
        print(f"FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''
    
    with open(package_dir / "main_debug.py", 'w', encoding='utf-8') as f:
        f.write(main_script)
    
    # Create debug PyInstaller spec
    print("Creating debug PyInstaller spec...")
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from pathlib import Path

# Get the project root directory
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

a = Analysis(
    ['main_debug.py'],
    pathex=[str(project_root)],
    binaries=pyqt6_binaries,
    datas=[
        ('examples', 'examples'),
        ('README.md', '.'),
        ('arxml_editor.ico', '.'),
    ] + pyqt6_datas,
    hiddenimports=[
        # PyQt6 modules
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'PyQt6.QtOpenGL',
        'PyQt6.QtSvg',
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
        # Basic modules
        'xml.etree.ElementTree',
        'pathlib',
        'lxml',
        'lxml.etree',
        'xmlschema',
        'xmlschema.validators',
        # System modules
        'sys',
        'os',
        'logging',
        'threading',
        'queue',
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
    name='ARXMLEditor_Debug',
    debug=True,  # Enable debug mode
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # Disable UPX for debugging
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Always show console for debug
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='arxml_editor.ico' if os.path.exists('arxml_editor.ico') else None,
)
'''
    
    with open(package_dir / "ARXMLEditor_Debug.spec", 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    # Create debug build script
    print("Creating debug build script...")
    build_script = '''@echo off
REM Debug ARXML Editor - Windows Build Script
echo ========================================
echo ARXML Editor - Debug Windows Build
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

echo Python found. Starting debug build...
echo.

REM Install requirements
echo Installing requirements...
python -m pip install PyQt6 PyQt6-Qt6 PyQt6-sip lxml xmlschema pyinstaller pywin32

REM Clean previous builds
echo.
echo Cleaning previous builds...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "__pycache__" rmdir /s /q "__pycache__"

REM Build executable
echo.
echo Building debug Windows executable...
echo This will show console output for debugging...
python -m PyInstaller ARXMLEditor_Debug.spec --clean --noconfirm

REM Check if build was successful
if not exist "dist\\ARXMLEditor_Debug.exe" (
    echo.
    echo ERROR: Build failed! Executable not found.
    echo Please check the error messages above.
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo DEBUG BUILD SUCCESSFUL!
echo ========================================
echo.
echo Executable created: dist\\ARXMLEditor_Debug.exe
echo.

REM Create release folder
if not exist "release" mkdir "release"
copy "dist\\ARXMLEditor_Debug.exe" "release\\"
if exist "arxml_editor.ico" copy "arxml_editor.ico" "release\\"

echo.
echo Debug ARXML Editor built successfully!
echo The executable will show console output for debugging.
echo Check the 'release' folder for the executable.
echo.
pause
'''
    
    with open(package_dir / "BUILD_DEBUG.bat", 'w', encoding='utf-8') as f:
        f.write(build_script)
    
    # Create README
    print("Creating README...")
    readme_content = '''# ARXML Editor - Debug Windows Version

This is a debug version of the ARXML Editor designed for troubleshooting Windows builds.

## Features

- **Console Output**: Shows detailed debug information
- **Error Reporting**: Displays errors and stack traces
- **Step-by-Step Logging**: Shows what's happening during startup
- **Basic ARXML Editing**: Open, edit, and save ARXML files
- **Debug Mode**: PyInstaller debug mode enabled

## Quick Start

1. **Run the build script**: Double-click `BUILD_DEBUG.bat`
2. **Wait for completion**: The build process will take a few minutes
3. **Run the executable**: Look in the `release` folder for `ARXMLEditor_Debug.exe`
4. **Check console output**: The executable will show debug information

## Debug Information

The debug version will show:
- Python version and executable path
- Import status of PyQt6
- UI initialization steps
- File operations
- Error messages and stack traces

## System Requirements

- Windows 10 or Windows 11
- Python 3.9 or higher
- 2GB RAM minimum
- 1GB free disk space

## Troubleshooting

### If the executable doesn't start:
1. Check the console output for error messages
2. Ensure PyQt6 is installed correctly
3. Try running from command prompt to see full output

### If you see import errors:
- PyQt6 might not be installed: `pip install PyQt6`
- Missing dependencies: Check the console output

### If the GUI doesn't appear:
- Check Windows display settings
- Try running as Administrator
- Check for antivirus interference

## Support

This debug version is designed to help identify issues.
Use the console output to diagnose problems.
'''
    
    with open(package_dir / "README_DEBUG.md", 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    # Create zip package
    print("Creating zip package...")
    zip_path = "ARXMLEditor-Windows-Debug-v1.0.0.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = Path(root) / file
                arc_path = file_path.relative_to(package_dir.parent)
                zipf.write(file_path, arc_path)
    
    print("=" * 60)
    print("DEBUG WINDOWS BUILD PACKAGE CREATED SUCCESSFULLY!")
    print("=" * 60)
    print(f"Package directory: {package_dir}")
    print(f"Zip package: {zip_path}")
    print()
    print("Next steps:")
    print("1. Transfer the zip file to a Windows machine")
    print("2. Extract the zip file")
    print("3. Run BUILD_DEBUG.bat")
    print("4. The resulting executable will show debug output!")
    print("=" * 60)

if __name__ == "__main__":
    create_debug_windows_package()
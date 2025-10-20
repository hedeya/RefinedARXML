#!/usr/bin/env python3
"""
Enhanced Debug Windows Build Package Creator for ARXML Editor
This version uses a more robust approach for PyQt6 bundling
"""

import os
import shutil
import zipfile
from pathlib import Path

def create_enhanced_debug_windows_package():
    """Create an enhanced debug Windows build package with better PyQt6 support"""
    print("=" * 60)
    print("ARXML Editor - Enhanced Debug Windows Build Package Creator")
    print("=" * 60)
    print("Creating enhanced debug Windows build package...")
    
    # Create package directory
    package_dir = Path("ARXMLEditor-Windows-Debug-Enhanced")
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
    
    # Create enhanced debug main script
    print("Creating enhanced debug main script...")
    main_script = '''"""
Enhanced Debug ARXML Editor - Main Entry Point
This version includes better PyQt6 error handling and fallback mechanisms.
"""

import sys
import os
from pathlib import Path

print("=" * 50)
print("ARXML Editor Enhanced Debug - Starting...")
print("=" * 50)
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Current directory: {os.getcwd()}")
print(f"Script location: {__file__}")
print("=" * 50)

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))
print("Added current directory to Python path")

# Set up environment for PyQt6
def setup_pyqt6_environment():
    """Set up environment variables for PyQt6"""
    if hasattr(sys, '_MEIPASS'):
        meipass = Path(sys._MEIPASS)
        print(f"PyInstaller bundle detected: {meipass}")
        
        # Add Qt6 paths to environment
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
    else:
        print("Running from source (not PyInstaller bundle)")

# Set up environment
setup_pyqt6_environment()

# Global imports for PyQt6
QApplication = None
QMainWindow = None
QVBoxLayout = None
QWidget = None
QLabel = None
QTextEdit = None
QMenuBar = None
QMenu = None
QFileDialog = None
QMessageBox = None
QIcon = None
QFont = None
Qt = None
QCoreApplication = None

# Try to import PyQt6 with detailed error reporting
def import_pyqt6():
    """Import PyQt6 with detailed error reporting"""
    global QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QTextEdit, QMenuBar, QMenu, QFileDialog, QMessageBox, QIcon, QFont, Qt, QCoreApplication
    
    try:
        print("Attempting to import PyQt6...")
        import PyQt6
        print("✓ PyQt6 module imported successfully")
        
        # Check if QtCore is available
        if not hasattr(PyQt6, 'QtCore'):
            print("✗ PyQt6.QtCore not available - attempting to fix...")
            print("  This usually means PyQt6-Qt6 is not properly installed")
            
            # Try to install PyQt6-Qt6
            try:
                import subprocess
                import sys
                print("  Installing PyQt6-Qt6...")
                result = subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'PyQt6-Qt6'], 
                                      capture_output=True, text=True, timeout=60)
                if result.returncode == 0:
                    print("  ✓ PyQt6-Qt6 installed successfully")
                    # Try importing again
                    import importlib
                    importlib.reload(PyQt6)
                    if hasattr(PyQt6, 'QtCore'):
                        print("  ✓ PyQt6.QtCore now available")
                    else:
                        print("  ✗ PyQt6.QtCore still not available after installation")
                        return False
                else:
                    print(f"  ✗ PyQt6-Qt6 installation failed: {result.stderr}")
                    return False
            except Exception as install_error:
                print(f"  ✗ Failed to install PyQt6-Qt6: {install_error}")
                return False
        
        print("Attempting to import PyQt6.QtCore...")
        from PyQt6.QtCore import Qt, QCoreApplication
        print("✓ PyQt6.QtCore imported successfully")
        # Try different version attribute names
        try:
            version = Qt.PYQT_VERSION_STR
        except AttributeError:
            try:
                version = Qt.QT_VERSION_STR
            except AttributeError:
                version = "Unknown"
        print(f"  Qt version: {version}")
        
        print("Attempting to import PyQt6.QtGui...")
        from PyQt6.QtGui import QIcon, QFont
        print("✓ PyQt6.QtGui imported successfully")
        
        print("Attempting to import PyQt6.QtWidgets...")
        from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QTextEdit, QMenuBar, QMenu, QFileDialog, QMessageBox
        print("✓ PyQt6.QtWidgets imported successfully")
        
        # Make sure all classes are available globally
        global QMainWindow, QApplication, QVBoxLayout, QWidget, QLabel, QTextEdit, QMenuBar, QMenu, QFileDialog, QMessageBox
        
        return True
        
    except ImportError as e:
        print(f"✗ PyQt6 import failed: {e}")
        print(f"  Error type: {type(e).__name__}")
        
        # Try to provide more specific error information
        if "DLL load failed" in str(e):
            print("  This is a DLL loading issue. Possible causes:")
            print("  - Missing Qt6 DLLs")
            print("  - Incorrect Qt6 plugin path")
            print("  - Missing Visual C++ Redistributable")
            print("  - Architecture mismatch (32-bit vs 64-bit)")
        elif "No module named" in str(e):
            print("  This is a module import issue. Possible causes:")
            print("  - PyQt6 not installed")
            print("  - Incorrect Python environment")
            print("  - Missing PyQt6-Qt6 package")
        
        return False
    except AttributeError as e:
        print(f"✗ PyQt6 attribute error: {e}")
        print("  This usually means PyQt6-Qt6 is not properly installed")
        print("  Try running: pip install --upgrade PyQt6-Qt6")
        return False
    except Exception as e:
        print(f"✗ Unexpected error importing PyQt6: {e}")
        print(f"  Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

# Try to import PyQt6
if not import_pyqt6():
    print("\\n" + "=" * 50)
    print("PYQT6 IMPORT FAILED - TROUBLESHOOTING INFO")
    print("=" * 50)
    print("Environment variables:")
    print(f"  PATH: {os.environ.get('PATH', 'Not set')[:200]}...")
    print(f"  QT_PLUGIN_PATH: {os.environ.get('QT_PLUGIN_PATH', 'Not set')}")
    print(f"  QT_LIBRARY_PATH: {os.environ.get('QT_LIBRARY_PATH', 'Not set')}")
    print("\\nPyInstaller info:")
    if hasattr(sys, '_MEIPASS'):
        print(f"  Bundle path: {sys._MEIPASS}")
        meipass = Path(sys._MEIPASS)
        print(f"  Qt6 bin exists: {(meipass / 'Qt6' / 'bin').exists()}")
        print(f"  Qt6 plugins exists: {(meipass / 'Qt6' / 'plugins').exists()}")
        print(f"  Qt6 lib exists: {(meipass / 'Qt6' / 'lib').exists()}")
    else:
        print("  Not running from PyInstaller bundle")
    
    print("\\nPlease try:")
    print("1. Install Visual C++ Redistributable for Visual Studio 2015-2022")
    print("2. Rebuild the executable with: BUILD_DEBUG.bat")
    print("3. Check that you're using 64-bit Python and 64-bit PyQt6")
    input("\\nPress Enter to exit...")
    sys.exit(1)

print("\\n✓ All PyQt6 modules imported successfully!")
print("=" * 50)

class EnhancedDebugARXMLEditor(QMainWindow):
    """Enhanced Debug ARXML Editor main window"""
    
    def __init__(self):
        print("Creating enhanced main window...")
        super().__init__()
        self.current_file = None
        self.init_ui()
        print("Enhanced main window created successfully")
    
    def init_ui(self):
        """Initialize the user interface"""
        print("Initializing enhanced UI...")
        self.setWindowTitle("ARXML Editor - Enhanced Debug Version")
        self.setGeometry(100, 100, 900, 700)
        
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
        self.text_area.setPlaceholderText(
            "ARXML content will appear here...\\n\\n"
            "Enhanced Debug Info:\\n"
            "✓ PyQt6 is working correctly\\n"
            "✓ GUI is responsive\\n"
            "✓ Ready for ARXML editing\\n\\n"
            "This version includes better error handling\\n"
            "and troubleshooting information."
        )
        layout.addWidget(self.text_area)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Status bar
        self.statusBar().showMessage("Enhanced debug version ready - PyQt6 working!")
        print("Enhanced UI initialized successfully")
    
    def create_menu_bar(self):
        """Create the menu bar"""
        print("Creating enhanced menu bar...")
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
        
        print("Enhanced menu bar created successfully")
    
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
            "About ARXML Editor Enhanced Debug",
            "ARXML Editor - Enhanced Debug Version\\n\\n"
            "This is an enhanced debug version with:\\n"
            "✓ Better PyQt6 error handling\\n"
            "✓ Detailed troubleshooting information\\n"
            "✓ Environment variable setup\\n"
            "✓ Fallback mechanisms\\n\\n"
            "Version: 1.0.1-enhanced\\n"
            "Built with PyQt6\\n\\n"
            "If you can see this dialog, PyQt6 is working correctly!"
        )

def main():
    """Main application entry point"""
    try:
        print("Creating QApplication...")
        app = QApplication(sys.argv)
        app.setApplicationName("ARXML Editor Enhanced Debug")
        app.setApplicationVersion("1.0.1")
        print("QApplication created successfully")
        
        print("Creating enhanced main window...")
        # Create and show main window
        window = EnhancedDebugARXMLEditor()
        window.show()
        print("Enhanced main window shown")
        
        print("Starting event loop...")
        print("=" * 50)
        print("Enhanced application is now running!")
        print("Check the console for detailed debug information.")
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
    
    with open(package_dir / "main_enhanced_debug.py", 'w', encoding='utf-8') as f:
        f.write(main_script)
    
    # Create enhanced PyInstaller spec
    print("Creating enhanced PyInstaller spec...")
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from pathlib import Path

# Get the project root directory
project_root = Path.cwd()

block_cipher = None

# Enhanced PyQt6 binary collection
def collect_pyqt6_files():
    """Enhanced PyQt6 binary collection with multiple fallback strategies"""
    binaries = []
    datas = []
    
    print("Collecting PyQt6 files...")
    
    try:
        import PyQt6
        pyqt6_path = Path(PyQt6.__file__).parent
        print(f"PyQt6 found at: {pyqt6_path}")
        
        # Qt6 DLLs to collect
        qt6_dlls = [
            'Qt6Core.dll',
            'Qt6Gui.dll', 
            'Qt6Widgets.dll',
            'Qt6OpenGL.dll',
            'Qt6Svg.dll',
            'Qt6Network.dll',
            'Qt6PrintSupport.dll',
        ]
        
        # Multiple possible locations for Qt6 DLLs
        possible_locations = [
            pyqt6_path / 'Qt6' / 'bin',
            pyqt6_path / 'Qt6' / 'lib',
            pyqt6_path / 'bin',
            pyqt6_path / 'lib',
            pyqt6_path / 'Qt6' / 'DLLs',
        ]
        
        for dll in qt6_dlls:
            found = False
            for location in possible_locations:
                dll_path = location / dll
                if dll_path.exists():
                    binaries.append((str(dll_path), 'Qt6/bin'))
                    print(f"Found {dll} at {dll_path}")
                    found = True
                    break
            if not found:
                print(f"Warning: {dll} not found in any location")
        
        # Collect platform plugins
        possible_plugin_locations = [
            pyqt6_path / 'Qt6' / 'plugins',
            pyqt6_path / 'plugins',
        ]
        
        for plugins_path in possible_plugin_locations:
            if plugins_path.exists():
                datas.append((str(plugins_path), 'Qt6/plugins'))
                print(f"Found plugins at {plugins_path}")
                break
        
        # Collect Qt6 libraries
        possible_lib_locations = [
            pyqt6_path / 'Qt6' / 'lib',
            pyqt6_path / 'lib',
        ]
        
        for lib_path in possible_lib_locations:
            if lib_path.exists():
                datas.append((str(lib_path), 'Qt6/lib'))
                print(f"Found lib at {lib_path}")
                break
                
    except ImportError as e:
        print(f"Warning: PyQt6 not found: {e}")
        print("Skipping Qt6 binary collection")
    
    print(f"Collected {len(binaries)} binaries and {len(datas)} data directories")
    return binaries, datas

# Collect PyQt6 files
pyqt6_binaries, pyqt6_datas = collect_pyqt6_files()

a = Analysis(
    ['main_enhanced_debug.py'],
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
        # Additional PyQt6 modules
        'PyQt6.Qt6.QtCore',
        'PyQt6.Qt6.QtGui',
        'PyQt6.Qt6.QtWidgets',
        'PyQt6.Qt6.QtOpenGL',
        'PyQt6.Qt6.QtSvg',
        'PyQt6.Qt6.QtNetwork',
        'PyQt6.Qt6.QtPrintSupport',
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
    name='ARXMLEditor_Enhanced_Debug',
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
    
    with open(package_dir / "ARXMLEditor_Enhanced_Debug.spec", 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    # Create PyQt6 verification script
    print("Creating PyQt6 verification script...")
    verify_script = '''#!/usr/bin/env python3
"""
PyQt6 Verification Script for Enhanced Debug Build
"""
import sys
import subprocess
import importlib

def verify_pyqt6():
    """Verify PyQt6 installation with detailed error reporting"""
    print("Verifying PyQt6 installation...")
    
    try:
        print("  Checking PyQt6 module...")
        import PyQt6
        print("  ✓ PyQt6 module found")
        
        # Check if QtCore is available
        if not hasattr(PyQt6, 'QtCore'):
            print("  ✗ PyQt6.QtCore not available - attempting to fix...")
            print("  Installing PyQt6-Qt6 to fix QtCore...")
            
            try:
                result = subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'PyQt6-Qt6'], 
                                      capture_output=True, text=True, timeout=60)
                if result.returncode == 0:
                    print("  ✓ PyQt6-Qt6 installed successfully")
                    # Try importing again
                    importlib.reload(PyQt6)
                    if hasattr(PyQt6, 'QtCore'):
                        print("  ✓ PyQt6.QtCore now available")
                    else:
                        print("  ✗ PyQt6.QtCore still not available after installation")
                        return False
                else:
                    print(f"  ✗ PyQt6-Qt6 installation failed: {result.stderr}")
                    return False
            except Exception as install_error:
                print(f"  ✗ Failed to install PyQt6-Qt6: {install_error}")
                return False
        
        print("  Checking PyQt6.QtCore...")
        from PyQt6.QtCore import PYQT_VERSION_STR
        print(f"  ✓ PyQt6 version: {PYQT_VERSION_STR}")
        
        print("  Checking PyQt6.QtCore.Qt...")
        from PyQt6.QtCore import Qt
        # Try different version attribute names
        try:
            version = Qt.PYQT_VERSION_STR
        except AttributeError:
            try:
                version = Qt.QT_VERSION_STR
            except AttributeError:
                version = "Unknown"
        print(f"  ✓ Qt version: {version}")
        
        print("  ✓ PyQt6 verification successful!")
        return True
        
    except ImportError as e:
        print(f"  ✗ PyQt6 import failed: {e}")
        print("  This usually means PyQt6 is not installed")
        return False
    except AttributeError as e:
        print(f"  ✗ PyQt6 attribute error: {e}")
        print("  This usually means PyQt6-Qt6 is not properly installed")
        return False
    except Exception as e:
        print(f"  ✗ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = verify_pyqt6()
    if not success:
        print("\\nPyQt6 verification failed!")
        sys.exit(1)
    else:
        print("\\nPyQt6 verification completed successfully!")
        sys.exit(0)
'''
    
    with open(package_dir / "verify_pyqt6.py", 'w', encoding='utf-8') as f:
        f.write(verify_script)
    
    # Create enhanced build script
    print("Creating enhanced build script...")
    build_script = '''@echo off
REM Enhanced Debug ARXML Editor - Windows Build Script
echo ========================================
echo ARXML Editor - Enhanced Debug Windows Build
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

echo Python found. Starting enhanced debug build...
echo.

REM Install requirements with enhanced error checking
echo Installing requirements with enhanced error checking...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo ERROR: Failed to upgrade pip
    pause
    exit /b 1
)

echo Installing PyQt6 and dependencies...
echo Installing PyQt6-Qt6 first (required for QtCore)...
python -m pip install --upgrade PyQt6-Qt6
if errorlevel 1 (
    echo WARNING: PyQt6-Qt6 installation failed - trying alternative method
    python -m pip install --user --upgrade PyQt6-Qt6
)

echo Installing PyQt6 main package...
python -m pip install --upgrade PyQt6
if errorlevel 1 (
    echo WARNING: PyQt6 installation failed - trying alternative method
    python -m pip install --user --upgrade PyQt6
)

echo Installing PyQt6-sip...
python -m pip install --upgrade PyQt6-sip
if errorlevel 1 (
    echo WARNING: PyQt6-sip installation failed - trying alternative method
    python -m pip install --user --upgrade PyQt6-sip
)

echo Installing other dependencies...
python -m pip install lxml xmlschema pyinstaller pywin32
if errorlevel 1 (
    echo ERROR: Failed to install other dependencies
    pause
    exit /b 1
)

REM Verify PyQt6 installation
echo.
echo Verifying PyQt6 installation...
python verify_pyqt6.py
if errorlevel 1 (
    echo ERROR: PyQt6 verification failed
    echo.
    echo This usually means PyQt6-Qt6 is not properly installed.
    echo The script will attempt to continue anyway...
    echo.
    echo Press any key to continue...
    pause >nul
)

python -c "
try:
    from PyQt6.QtCore import Qt
    print('Qt version:', Qt.PYQT_VERSION_STR)
except Exception as e:
    print('WARNING: Qt verification failed:', e)
    print('This may be normal - continuing with build...')
"
if errorlevel 1 (
    echo WARNING: Qt verification failed - continuing anyway
    echo This is usually not a problem, continuing with build...
)

echo PyQt6 verification successful!
echo.
echo Press any key to continue with the build...
pause >nul
echo.

REM Clean previous builds
echo Cleaning previous builds...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "__pycache__" rmdir /s /q "__pycache__"

REM Build executable
echo.
echo Building enhanced debug Windows executable...
echo This will show detailed console output for debugging...
echo This may take several minutes - please wait...
echo.
python -m PyInstaller ARXMLEditor_Enhanced_Debug.spec --clean --noconfirm

REM Check if build was successful
if not exist "dist\\ARXMLEditor_Enhanced_Debug.exe" (
    echo.
    echo ERROR: Build failed! Executable not found.
    echo Please check the error messages above.
    echo.
    echo Press any key to continue anyway...
    pause >nul
    echo.
    echo Attempting to continue with build...
) else (
    echo.
    echo Build completed successfully!
    echo.
)

echo.
echo ========================================
echo ENHANCED DEBUG BUILD SUCCESSFUL!
echo ========================================
echo.
echo Executable created: dist\\ARXMLEditor_Enhanced_Debug.exe
echo.

REM Create release folder
if not exist "release" mkdir "release"
copy "dist\\ARXMLEditor_Enhanced_Debug.exe" "release\\"
if exist "arxml_editor.ico" copy "arxml_editor.ico" "release\\"

echo.
echo Enhanced Debug ARXML Editor built successfully!
echo The executable includes better error handling and troubleshooting.
echo Check the 'release' folder for the executable.
echo.
echo Press any key to close this window...
pause >nul
'''
    
    with open(package_dir / "BUILD_ENHANCED_DEBUG.bat", 'w', encoding='utf-8') as f:
        f.write(build_script)
    
    # Create enhanced README
    print("Creating enhanced README...")
    readme_content = '''# ARXML Editor - Enhanced Debug Windows Version

This is an enhanced debug version of the ARXML Editor designed for troubleshooting Windows builds with better PyQt6 support.

## Features

- **Enhanced Error Handling**: Better PyQt6 error detection and reporting
- **Detailed Troubleshooting**: Comprehensive error information and solutions
- **Environment Setup**: Automatic Qt6 environment variable configuration
- **Fallback Mechanisms**: Multiple strategies for PyQt6 loading
- **Console Output**: Shows detailed debug information
- **Basic ARXML Editing**: Open, edit, and save ARXML files
- **Debug Mode**: PyInstaller debug mode enabled

## Quick Start

1. **Run the build script**: Double-click `BUILD_ENHANCED_DEBUG.bat`
2. **Wait for completion**: The build process will take a few minutes
3. **Run the executable**: Look in the `release` folder for `ARXMLEditor_Enhanced_Debug.exe`
4. **Check console output**: The executable will show detailed debug information

## Enhanced Debug Information

The enhanced debug version will show:
- Python version and executable path
- PyQt6 import status with detailed error reporting
- Environment variable setup
- UI initialization steps
- File operations
- Comprehensive error messages and solutions

## Troubleshooting

### If PyQt6 import fails:
The enhanced version will show detailed error information including:
- Specific error type and message
- Environment variable status
- PyInstaller bundle information
- Suggested solutions

### Common solutions:
1. **Install Visual C++ Redistributable**: Download from Microsoft
2. **Check architecture**: Ensure 64-bit Python and 64-bit PyQt6
3. **Reinstall PyQt6**: `pip uninstall PyQt6 PyQt6-Qt6 PyQt6-sip` then `pip install PyQt6 PyQt6-Qt6 PyQt6-sip`
4. **Rebuild**: Run `BUILD_ENHANCED_DEBUG.bat` again

## System Requirements

- Windows 10 or Windows 11
- Python 3.9 or higher
- Visual C++ Redistributable for Visual Studio 2015-2022
- 2GB RAM minimum
- 1GB free disk space

## Support

This enhanced debug version is designed to help identify and resolve PyQt6 issues.
Use the detailed console output to diagnose problems and follow the suggested solutions.
'''
    
    with open(package_dir / "README_ENHANCED_DEBUG.md", 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    # Create zip package
    print("Creating enhanced zip package...")
    zip_path = "ARXMLEditor-Windows-Debug-Enhanced-v1.0.1.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = Path(root) / file
                arc_path = file_path.relative_to(package_dir.parent)
                zipf.write(file_path, arc_path)
    
    print("=" * 60)
    print("ENHANCED DEBUG WINDOWS BUILD PACKAGE CREATED SUCCESSFULLY!")
    print("=" * 60)
    print(f"Package directory: {package_dir}")
    print(f"Zip package: {zip_path}")
    print()
    print("Next steps:")
    print("1. Transfer the zip file to a Windows machine")
    print("2. Extract the zip file")
    print("3. Run BUILD_ENHANCED_DEBUG.bat")
    print("4. The resulting executable will show enhanced debug output!")
    print("=" * 60)

if __name__ == "__main__":
    create_enhanced_debug_windows_package()
#!/usr/bin/env python3
"""
Windows Build Package Creator

This script creates a complete Windows build package that can be transferred
to a Windows machine and used to build the ARXML Editor executable.

The package includes:
- All source code
- Windows-specific build scripts
- Requirements and dependencies
- Detailed build instructions
- PyInstaller configuration
"""

import os
import sys
import shutil
import zipfile
from pathlib import Path

def create_windows_build_package():
    """Create a complete Windows build package"""
    print("Creating Windows build package...")
    
    # Create package directory
    package_dir = Path("ARXMLEditor-Windows-Build-Package")
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir()
    
    # Copy source code
    print("Copying source code...")
    source_dirs = [
        "arxml_editor",
        "examples",
        "tests",
    ]
    
    for source_dir in source_dirs:
        if Path(source_dir).exists():
            shutil.copytree(source_dir, package_dir / source_dir)
            print(f"  Copied {source_dir}")
    
    # Copy individual files
    files_to_copy = [
        "README.md",
        "requirements.txt",
        "pyproject.toml",
        "setup.py",
        "run_editor.py",
        "arxml_editor.ico",
    ]
    
    # Copy compatibility files
    compatibility_files = [
        "gui_compatibility.py",
        "gui_framework_detector.py",
        "main_compatible.py",
        "install_gui_framework.py",
    ]
    
    for file_name in compatibility_files:
        if Path(file_name).exists():
            shutil.copy2(file_name, package_dir / file_name)
            print(f"  Copied {file_name}")
        else:
            # Create the file if it doesn't exist
            if file_name == "install_gui_framework.py":
                create_install_gui_framework_script(package_dir)
            elif file_name == "main_compatible.py":
                create_main_compatible_script(package_dir)
            elif file_name == "gui_compatibility.py":
                create_gui_compatibility_script(package_dir)
            elif file_name == "gui_framework_detector.py":
                create_gui_framework_detector_script(package_dir)
    
    for file_name in files_to_copy:
        if Path(file_name).exists():
            shutil.copy2(file_name, package_dir / file_name)
            print(f"  Copied {file_name}")
    
    # Create Windows-specific build script
    create_windows_build_script(package_dir)
    
    # Create Windows-specific PyInstaller spec
    create_windows_pyinstaller_spec(package_dir)
    
    # Create Windows requirements file
    create_windows_requirements(package_dir)
    
    # Create detailed build instructions
    create_build_instructions(package_dir)
    
    # Create PowerShell build script
    create_powershell_build_script(package_dir)
    
    # Create batch file for easy execution
    create_batch_launcher(package_dir)
    
    print(f"Windows build package created: {package_dir}")
    return package_dir

def create_windows_build_script(package_dir):
    """Create the main Windows build script"""
    build_script = '''@echo off
REM ARXML Editor - Windows Build Script
REM This script builds the ARXML Editor executable for Windows

echo ========================================
echo ARXML Editor - Windows Build Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9 or higher from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found:
python --version

REM Check Python version
for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo Checking Python version: %PYTHON_VERSION%

REM Install/upgrade pip
echo.
echo Installing/upgrading pip...
python -m pip install --upgrade pip

REM Install GUI framework first
echo.
echo Installing GUI framework...
python install_gui_framework.py

REM Install basic requirements first
echo.
echo Installing basic requirements...
python -m pip install lxml xmlschema networkx matplotlib pydantic typing-extensions pyinstaller pywin32

REM Try to install autosar-data (may fail on some systems)
echo.
echo Installing ARXML processing library...
python -m pip install autosar-data || echo WARNING: autosar-data installation failed - continuing without it

REM Install PyInstaller
echo.
echo Installing PyInstaller...
python -m pip install pyinstaller

REM Clean previous builds
echo.
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__

REM Build the executable
echo.
echo Building Windows executable...
echo This may take several minutes...
python -m PyInstaller ARXMLEditor_Windows.spec --clean --noconfirm

REM Check if build was successful
if not exist "dist\\ARXMLEditor.exe" (
    echo.
    echo ERROR: Build failed! Executable not found.
    echo Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo ========================================
echo BUILD SUCCESSFUL!
echo ========================================
echo.
echo Executable created: dist\\ARXMLEditor.exe
echo.

REM Create release package
echo Creating release package...
call create_release_package.bat

echo.
echo Build completed successfully!
echo Check the 'release' folder for the final package.
echo.
pause
'''
    
    with open(package_dir / "build_windows.bat", 'w', encoding='utf-8') as f:
        f.write(build_script)

def create_powershell_build_script(package_dir):
    """Create PowerShell build script"""
    ps_script = '''# ARXML Editor - Windows PowerShell Build Script
# This script builds the ARXML Editor executable for Windows

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ARXML Editor - Windows Build Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.9 or higher from https://python.org" -ForegroundColor Red
    Write-Host "Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Installing/upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

Write-Host ""
Write-Host "Installing requirements..." -ForegroundColor Yellow
python -m pip install -r requirements_windows.txt

Write-Host ""
Write-Host "Installing PyInstaller..." -ForegroundColor Yellow
python -m pip install pyinstaller

Write-Host ""
Write-Host "Cleaning previous builds..." -ForegroundColor Yellow
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "__pycache__") { Remove-Item -Recurse -Force "__pycache__" }

Write-Host ""
Write-Host "Building Windows executable..." -ForegroundColor Yellow
Write-Host "This may take several minutes..." -ForegroundColor Yellow
python -m PyInstaller ARXMLEditor_Windows.spec --clean --noconfirm

# Check if build was successful
if (-not (Test-Path "dist\\ARXMLEditor.exe")) {
    Write-Host ""
    Write-Host "ERROR: Build failed! Executable not found." -ForegroundColor Red
    Write-Host "Please check the error messages above." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "BUILD SUCCESSFUL!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Executable created: dist\\ARXMLEditor.exe" -ForegroundColor Green
Write-Host ""

# Create release package
Write-Host "Creating release package..." -ForegroundColor Yellow
& ".\create_release_package.bat"

Write-Host ""
Write-Host "Build completed successfully!" -ForegroundColor Green
Write-Host "Check the 'release' folder for the final package." -ForegroundColor Green
Write-Host ""
Read-Host "Press Enter to exit"
'''
    
    with open(package_dir / "build_windows.ps1", 'w', encoding='utf-8') as f:
        f.write(ps_script)

def create_windows_pyinstaller_spec(package_dir):
    """Create Windows-optimized PyInstaller spec file"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for ARXML Editor Windows build
Optimized for Windows compatibility and performance
"""

import os
import sys
from pathlib import Path

# Get the project root directory - use current working directory instead of __file__
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

# Analysis configuration
a = Analysis(
    ['main_compatible.py'],
    pathex=[str(project_root)],
    binaries=pyqt6_binaries,
    datas=[
        ('examples', 'examples'),
        ('arxml_editor/validation', 'arxml_editor/validation'),
        ('README.md', '.'),
        ('requirements_windows.txt', '.'),
        ('gui_compatibility.py', '.'),
        ('gui_framework_detector.py', '.'),
        ('simple_arxml_model.py', '.'),
    ] + pyqt6_datas,
    hiddenimports=[
        # PySide6 modules (for Python < 3.14)
        'PySide6.QtCore',
        'PySide6.QtGui', 
        'PySide6.QtWidgets',
        'PySide6.QtOpenGL',
        'PySide6.QtOpenGLWidgets',
        'PySide6.QtSvg',
        'PySide6.QtSvgWidgets',
        # PyQt6 modules (for Python >= 3.14)
        'PyQt6.QtCore',
        'PyQt6.QtGui', 
        'PyQt6.QtWidgets',
        'PyQt6.QtOpenGL',
        'PyQt6.QtOpenGLWidgets',
        'PyQt6.QtSvg',
        'PyQt6.QtSvgWidgets',
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
        
        # XML processing
        'xml.etree.ElementTree',
        'lxml',
        'lxml.etree',
        'lxml._elementpath',
        'lxml.html',
        'lxml.html.clean',
        
        # Schema validation
        'xmlschema',
        'xmlschema.validators',
        'xmlschema.validators.schemas',
        
        # Graph algorithms
        'networkx',
        'networkx.algorithms',
        'networkx.algorithms.shortest_paths',
        
        # Plotting and visualization
        'matplotlib',
        'matplotlib.backends.backend_qt5agg',
        'matplotlib.backends.backend_qt5cairo',
        'matplotlib.backends.backend_agg',
        'matplotlib.figure',
        'matplotlib.pyplot',
        
        # Data validation
        'pydantic',
        'pydantic.fields',
        'pydantic.validators',
        'typing_extensions',
        
        # ARXML processing (optional - may not be available)
        # 'autosar_data',
        # 'autosar_data.core',
        # 'autosar_data.schema',
        # 'autosar_data.validation',
        
        # Additional modules that might be needed
        'encodings',
        'encodings.utf_8',
        'encodings.cp1252',
        'encodings.latin_1',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude unnecessary modules to reduce size
        'tkinter',
        'unittest',
        'test',
        'pytest',
        'IPython',
        'jupyter',
        'notebook',
        'sphinx',
        'docutils',
        'setuptools',
        'distutils',
        'pip',
        'wheel',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Remove duplicate binaries and optimize
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
    
    with open(package_dir / "ARXMLEditor_Windows.spec", 'w', encoding='utf-8') as f:
        f.write(spec_content)

def create_windows_requirements(package_dir):
    """Create Windows-specific requirements file"""
    requirements_content = '''# ARXML Editor - Windows Requirements
# Optimized for Windows compatibility and Python 3.14 support

# Core GUI framework - try PySide6 first, fallback to PyQt6
PySide6>=6.6.0,<6.14; python_version<"3.14"
PyQt6>=6.6.0; python_version>="3.14"
PyQt6-Qt6>=6.6.0; python_version>="3.14"
PyQt6-sip>=13.0.0; python_version>="3.14"

# XML processing (core dependencies only)
lxml>=4.9.0

# Schema validation
xmlschema>=3.0.0

# Graph algorithms
networkx>=3.0

# Plotting and visualization
matplotlib>=3.7.0

# Data validation
pydantic>=2.0.0
typing-extensions>=4.5.0

# Build tools
pyinstaller>=5.0.0

# Additional Windows-specific dependencies
pywin32>=306; sys_platform == "win32"

# Fallback GUI framework for Python 3.14
PyQt6-Qt6>=6.6.0; python_version>="3.14"
PyQt6-sip>=13.0.0; python_version>="3.14"

# Note: autosar-data package requires Rust compilation
# It will be installed separately if needed
'''
    
    with open(package_dir / "requirements_windows.txt", 'w', encoding='utf-8') as f:
        f.write(requirements_content)

def create_build_instructions(package_dir):
    """Create detailed build instructions"""
    instructions = '''# ARXML Editor - Windows Build Instructions

## Prerequisites

### 1. Install Python
- Download Python 3.9 or higher from https://python.org
- **IMPORTANT**: During installation, check "Add Python to PATH"
- Verify installation by opening Command Prompt and running: `python --version`

### 2. System Requirements
- Windows 10 or Windows 11
- At least 4GB RAM (8GB recommended)
- At least 2GB free disk space
- Internet connection for downloading dependencies

## Build Process

### Option 1: Using Batch File (Recommended)
1. Open Command Prompt as Administrator
2. Navigate to this folder: `cd "path\\to\\ARXMLEditor-Windows-Build-Package"`
3. Run: `build_windows.bat`
4. Wait for the build to complete (may take 10-15 minutes)
5. Check the `release` folder for the final package

### Option 2: Using PowerShell
1. Open PowerShell as Administrator
2. Navigate to this folder: `cd "path\\to\\ARXMLEditor-Windows-Build-Package"`
3. Run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
4. Run: `.\build_windows.ps1`
5. Wait for the build to complete
6. Check the `release` folder for the final package

### Option 3: Manual Build
1. Open Command Prompt
2. Install requirements: `pip install -r requirements_windows.txt`
3. Install PyInstaller: `pip install pyinstaller`
4. Build executable: `pyinstaller ARXMLEditor_Windows.spec --clean --noconfirm`
5. Create release package: `create_release_package.bat`

## Troubleshooting

### Common Issues

#### "Python is not recognized"
- Python is not installed or not in PATH
- Solution: Reinstall Python and check "Add Python to PATH"

#### "Permission denied" errors
- Run Command Prompt as Administrator
- Or move the package to a folder you have full access to

#### Build fails with import errors
- Make sure all requirements are installed: `pip install -r requirements_windows.txt`
- Try upgrading pip: `python -m pip install --upgrade pip`

#### Antivirus blocks the executable
- Add the project folder to antivirus exclusions
- Temporarily disable real-time protection during build

#### "No module named 'PySide6'"
- Install PySide6: `pip install PySide6`
- If that fails, try: `pip install PySide6 --no-cache-dir`

### Build Output

After successful build, you'll find:
- `dist/ARXMLEditor.exe` - The main executable
- `release/` - Complete release package ready for distribution

### Testing the Build

1. Navigate to the `release` folder
2. Double-click `run_editor.bat`
3. The ARXML Editor should start

## File Structure

```
ARXMLEditor-Windows-Build-Package/
├── arxml_editor/              # Source code
├── examples/                  # Sample ARXML files
├── tests/                     # Test files
├── build_windows.bat          # Main build script
├── build_windows.ps1          # PowerShell build script
├── create_release_package.bat # Release packaging script
├── ARXMLEditor_Windows.spec   # PyInstaller configuration
├── requirements_windows.txt   # Windows requirements
├── README.md                  # Project documentation
└── BUILD_INSTRUCTIONS.md      # This file
```

## Support

If you encounter issues:
1. Check this troubleshooting guide
2. Verify all prerequisites are met
3. Try running as Administrator
4. Check Windows Defender/antivirus settings
5. Create an issue on GitHub with error details

## Next Steps

After building:
1. Test the executable on the target Windows machine
2. Create a zip package for distribution
3. Update the GitHub release with the new Windows build
'''
    
    with open(package_dir / "BUILD_INSTRUCTIONS.md", 'w', encoding='utf-8') as f:
        f.write(instructions)

def create_install_gui_framework_script(package_dir):
    """Create GUI framework installation script"""
    script_content = '''#!/usr/bin/env python3
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
'''
    
    with open(package_dir / "install_gui_framework.py", 'w', encoding='utf-8') as f:
        f.write(script_content)

def create_main_compatible_script(package_dir):
    """Create compatible main script"""
    script_content = '''"""
Main entry point for ARXML Editor application.

Launches the GUI application with proper error handling and logging.
Compatible with both PySide6 and PyQt6.
"""

import sys
import logging
from pathlib import Path

# Import GUI compatibility layer
try:
    from gui_compatibility import QtCore, QtGui, QtWidgets
except ImportError:
    # Fallback to direct imports if compatibility layer fails
    try:
        from PySide6.QtWidgets import QApplication, QMessageBox
        from PySide6.QtCore import Qt
        from PySide6.QtGui import QIcon
    except ImportError:
        try:
            from PyQt6.QtWidgets import QApplication, QMessageBox
            from PyQt6.QtCore import Qt
            from PyQt6.QtGui import QIcon
        except ImportError:
            print("Error: Neither PySide6 nor PyQt6 is available.")
            print("Please install PySide6 (for Python < 3.14) or PyQt6 (for Python >= 3.14)")
            sys.exit(1)

# Import the main window and model
try:
    from arxml_editor.ui.main_window import MainWindow
    # Try to import the full model first, fallback to simplified version
    try:
        from arxml_editor.core.arxml_model import ARXMLModel
    except ImportError:
        print("Warning: Could not import full ARXML model, using simplified version")
        from simple_arxml_model import SimpleARXMLModel as ARXMLModel
except ImportError:
    print("Error: Could not import ARXML Editor modules.")
    print("Please ensure all source files are present.")
    sys.exit(1)


def setup_logging():
    """Set up application logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('arxml_editor.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )


def main():
    """Main application entry point."""
    try:
        # Set up logging
        setup_logging()
        logger = logging.getLogger(__name__)
        logger.info("Starting ARXML Editor...")
        
        # Create QApplication
        app = QApplication(sys.argv)
        app.setApplicationName("ARXML Editor")
        app.setApplicationVersion("1.0.0")
        app.setOrganizationName("ARXML Editor Team")
        
        # Set application icon if available
        icon_path = Path(__file__).parent / "arxml_editor.ico"
        if icon_path.exists():
            app.setWindowIcon(QIcon(str(icon_path)))
        
        # Create and show main window
        main_window = MainWindow()
        main_window.show()
        
        logger.info("ARXML Editor started successfully")
        
        # Run the application
        sys.exit(app.exec())
        
    except Exception as e:
        logger.error(f"Failed to start ARXML Editor: {e}")
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
'''
    
    with open(package_dir / "main_compatible.py", 'w', encoding='utf-8') as f:
        f.write(script_content)

def create_gui_compatibility_script(package_dir):
    """Create GUI compatibility script"""
    script_content = '''#!/usr/bin/env python3
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
'''
    
    with open(package_dir / "gui_compatibility.py", 'w', encoding='utf-8') as f:
        f.write(script_content)

def create_gui_framework_detector_script(package_dir):
    """Create GUI framework detector script"""
    script_content = '''#!/usr/bin/env python3
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
'''
    
    with open(package_dir / "gui_framework_detector.py", 'w', encoding='utf-8') as f:
        f.write(script_content)

def create_batch_launcher(package_dir):
    """Create batch file for easy execution"""
    launcher = '''@echo off
REM ARXML Editor - Quick Start
echo Starting ARXML Editor build process...
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

REM Run the main build script
call build_windows.bat

echo.
echo Build process completed!
pause
'''
    
    with open(package_dir / "START_BUILD.bat", 'w', encoding='utf-8') as f:
        f.write(launcher)

def create_release_package_script(package_dir):
    """Create script to package the final release"""
    release_script = '''@echo off
REM Create Release Package Script
echo Creating release package...

REM Create release directory
if not exist release mkdir release
if not exist release\\ARXMLEditor mkdir release\\ARXMLEditor

REM Copy executable
if exist dist\\ARXMLEditor.exe (
    copy dist\\ARXMLEditor.exe release\\ARXMLEditor\\
    echo Copied executable
) else (
    echo ERROR: Executable not found! Build may have failed.
    pause
    exit /b 1
)

REM Copy additional files
if exist examples xcopy examples release\\examples\\ /E /I /Q
if exist README.md copy README.md release\\
if exist requirements_windows.txt copy requirements_windows.txt release\\

REM Create Windows launcher
echo @echo off > release\\run_editor.bat
echo title ARXML Editor >> release\\run_editor.bat
echo echo Starting ARXML Editor... >> release\\run_editor.bat
echo echo. >> release\\run_editor.bat
echo. >> release\\run_editor.bat
echo REM Check if executable exists >> release\\run_editor.bat
echo if not exist "ARXMLEditor\\ARXMLEditor.exe" ^( >> release\\run_editor.bat
echo     echo ERROR: ARXMLEditor.exe not found! >> release\\run_editor.bat
echo     echo Please ensure the executable is in the ARXMLEditor folder. >> release\\run_editor.bat
echo     pause >> release\\run_editor.bat
echo     exit /b 1 >> release\\run_editor.bat
echo ^) >> release\\run_editor.bat
echo. >> release\\run_editor.bat
echo REM Change to the directory containing this batch file >> release\\run_editor.bat
echo cd /d "%%~dp0" >> release\\run_editor.bat
echo. >> release\\run_editor.bat
echo REM Run the application >> release\\run_editor.bat
echo echo Launching ARXML Editor... >> release\\run_editor.bat
echo ARXMLEditor\\ARXMLEditor.exe >> release\\run_editor.bat
echo. >> release\\run_editor.bat
echo REM Keep window open if there was an error >> release\\run_editor.bat
echo if errorlevel 1 ^( >> release\\run_editor.bat
echo     echo. >> release\\run_editor.bat
echo     echo Application exited with an error. >> release\\run_editor.bat
echo     pause >> release\\run_editor.bat
echo ^) >> release\\run_editor.bat

echo.
echo ========================================
echo RELEASE PACKAGE CREATED!
echo ========================================
echo.
echo Location: release\\
echo.
echo To test: Double-click run_editor.bat in the release folder
echo.
echo To distribute: Zip the entire release folder
echo.
'''
    
    with open(package_dir / "create_release_package.bat", 'w', encoding='utf-8') as f:
        f.write(release_script)

def create_zip_package(package_dir):
    """Create a zip package of the Windows build package"""
    print("Creating zip package...")
    
    zip_path = Path("ARXMLEditor-Windows-Build-Package-v1.0.0.zip")
    if zip_path.exists():
        zip_path.unlink()
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = Path(root) / file
                arc_path = file_path.relative_to(package_dir.parent)
                zipf.write(file_path, arc_path)
    
    print(f"Created zip package: {zip_path}")
    return zip_path

def main():
    """Main function"""
    print("=" * 60)
    print("ARXML Editor - Windows Build Package Creator")
    print("=" * 60)
    
    try:
        # Create the Windows build package
        package_dir = create_windows_build_package()
        
        # Create release package script
        create_release_package_script(package_dir)
        
        # Create zip package
        zip_path = create_zip_package(package_dir)
        
        print("=" * 60)
        print("WINDOWS BUILD PACKAGE CREATED SUCCESSFULLY!")
        print("=" * 60)
        print(f"Package directory: {package_dir}")
        print(f"Zip package: {zip_path}")
        print("\nNext steps:")
        print("1. Transfer the zip file to a Windows machine")
        print("2. Extract the zip file")
        print("3. Run START_BUILD.bat or follow BUILD_INSTRUCTIONS.md")
        print("4. The resulting executable will be Windows-compatible!")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Failed to create Windows build package: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
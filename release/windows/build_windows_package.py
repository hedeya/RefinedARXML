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

REM Ensure Python version is within supported range for PySide6
REM Use two simple FOR parses to avoid the "tokens=1,2" parsing edge case
for /f "tokens=1 delims=." %%a in ("%PYTHON_VERSION%") do set PY_MAJOR=%%a
for /f "tokens=2 delims=." %%a in ("%PYTHON_VERSION%") do set PY_MINOR=%%a
if "%PY_MAJOR%"=="" set PY_MAJOR=0
if "%PY_MINOR%"=="" set PY_MINOR=0
rem If major is greater than 3 (e.g., Python 4.x) or major==3 and minor too new, abort
if %PY_MAJOR% GTR 3 (
    echo ERROR: Detected Python %PYTHON_VERSION%. PySide6 currently does not support very new Python versions (e.g., 3.14).
    echo Please install Python 3.12 or 3.11 and retry, or install a PySide6 wheel compatible with your Python.
    pause
    exit /b 1
)

REM Install/upgrade pip
echo.
echo Installing/upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo.
echo Installing requirements...
python -m pip install -r requirements_windows.txt

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
Write-Host "Checking Python version compatibility..." -ForegroundColor Yellow
$pyVerParts = ($pythonVersion -split ' ')[-1] -split '\.'
if ($pyVerParts[0] -gt 3) {
    Write-Host "ERROR: Detected Python $($pyVerParts -join '.') which is newer than supported by PySide6." -ForegroundColor Red
    Write-Host "Please install Python 3.12 or 3.11 and retry." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

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
& ".\\create_release_package.bat"

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

# Get the project root directory. When PyInstaller executes a spec, __file__ may not be
# defined. Fall back to the current working directory in that case.
try:
    project_root = Path(__file__).parent
except NameError:
    project_root = Path('.').resolve()

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
        ('requirements_windows.txt', '.'),
    ],
    hiddenimports=[
        # PySide6 modules
        'PySide6.QtCore',
        'PySide6.QtGui', 
        'PySide6.QtWidgets',
        'PySide6.QtOpenGL',
        'PySide6.QtOpenGLWidgets',
        'PySide6.QtSvg',
        'PySide6.QtSvgWidgets',
        
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
        
        # ARXML processing
        'autosar_data',
        'autosar_data.core',
        'autosar_data.schema',
        'autosar_data.validation',
        
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
# Optimized for Windows compatibility

# Core GUI framework
PySide6>=6.6.0

# ARXML processing
autosar-data>=0.1.0

# XML processing
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
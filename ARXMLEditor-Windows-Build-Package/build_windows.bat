@echo off
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
REM Use simpler FOR parsing to avoid syntax issues with parentheses
for /f "tokens=1 delims=." %%a in ("%PYTHON_VERSION%") do set PY_MAJOR=%%a
for /f "tokens=2 delims=." %%a in ("%PYTHON_VERSION%") do set PY_MINOR=%%a
if "%PY_MAJOR%"=="" (
    set PY_MAJOR=0
)
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
if not exist "dist\ARXMLEditor.exe" (
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
echo Executable created: dist\ARXMLEditor.exe
echo.

REM Create release package
echo Creating release package...
call create_release_package.bat

echo.
echo Build completed successfully!
echo Check the 'release' folder for the final package.
echo.
pause

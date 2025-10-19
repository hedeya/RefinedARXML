@echo off
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
if not exist "dist\ARXMLEditor_Simple.exe" (
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
echo Executable created: dist\ARXMLEditor_Simple.exe
echo.

REM Create release folder
if not exist "release" mkdir "release"
copy "dist\ARXMLEditor_Simple.exe" "release\"
if exist "arxml_editor.ico" copy "arxml_editor.ico" "release\"

echo.
echo Simple ARXML Editor built successfully!
echo Check the 'release' folder for the executable.
echo.
pause

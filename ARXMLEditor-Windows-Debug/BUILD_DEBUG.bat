@echo off
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
if not exist "dist\ARXMLEditor_Debug.exe" (
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
echo Executable created: dist\ARXMLEditor_Debug.exe
echo.

REM Create release folder
if not exist "release" mkdir "release"
copy "dist\ARXMLEditor_Debug.exe" "release\"
if exist "arxml_editor.ico" copy "arxml_editor.ico" "release\"

echo.
echo Debug ARXML Editor built successfully!
echo The executable will show console output for debugging.
echo Check the 'release' folder for the executable.
echo.
pause

@echo off
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

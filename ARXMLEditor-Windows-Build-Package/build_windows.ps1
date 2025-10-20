# ARXML Editor - Windows PowerShell Build Script
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
if (-not (Test-Path "dist\ARXMLEditor.exe")) {
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
Write-Host "Executable created: dist\ARXMLEditor.exe" -ForegroundColor Green
Write-Host ""

# Create release package
Write-Host "Creating release package..." -ForegroundColor Yellow
& ".\create_release_package.bat"

Write-Host ""
Write-Host "Build completed successfully!" -ForegroundColor Green
Write-Host "Check the 'release' folder for the final package." -ForegroundColor Green
Write-Host ""
Read-Host "Press Enter to exit"

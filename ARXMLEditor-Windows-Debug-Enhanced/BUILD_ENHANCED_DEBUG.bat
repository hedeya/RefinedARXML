@echo off
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
python -m pip install PyQt6 PyQt6-Qt6 PyQt6-sip
if errorlevel 1 (
    echo ERROR: Failed to install PyQt6
    echo Please check your internet connection and try again
    pause
    exit /b 1
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
python -c "import PyQt6; print('PyQt6 version:', PyQt6.QtCore.PYQT_VERSION_STR)"
if errorlevel 1 (
    echo ERROR: PyQt6 verification failed
    pause
    exit /b 1
)

python -c "from PyQt6.QtCore import Qt; print('Qt version:', Qt.PYQT_VERSION_STR)"
if errorlevel 1 (
    echo ERROR: Qt verification failed
    pause
    exit /b 1
)

echo PyQt6 verification successful!
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
python -m PyInstaller ARXMLEditor_Enhanced_Debug.spec --clean --noconfirm

REM Check if build was successful
if not exist "dist\ARXMLEditor_Enhanced_Debug.exe" (
    echo.
    echo ERROR: Build failed! Executable not found.
    echo Please check the error messages above.
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo ENHANCED DEBUG BUILD SUCCESSFUL!
echo ========================================
echo.
echo Executable created: dist\ARXMLEditor_Enhanced_Debug.exe
echo.

REM Create release folder
if not exist "release" mkdir "release"
copy "dist\ARXMLEditor_Enhanced_Debug.exe" "release\"
if exist "arxml_editor.ico" copy "arxml_editor.ico" "release\"

echo.
echo Enhanced Debug ARXML Editor built successfully!
echo The executable includes better error handling and troubleshooting.
echo Check the 'release' folder for the executable.
echo.
pause

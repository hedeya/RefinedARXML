@echo off
REM Create Release Package Script
echo Creating release package...

REM Create release directory
if not exist release mkdir release
if not exist release\ARXMLEditor mkdir release\ARXMLEditor

REM Copy executable
if exist dist\ARXMLEditor.exe (
    copy dist\ARXMLEditor.exe release\ARXMLEditor\
    echo Copied executable
) else (
    echo ERROR: Executable not found! Build may have failed.
    pause
    exit /b 1
)

REM Copy additional files
if exist examples xcopy examples release\examples\ /E /I /Q
if exist README.md copy README.md release\
if exist requirements_windows.txt copy requirements_windows.txt release\

REM Create Windows launcher
echo @echo off > release\run_editor.bat
echo title ARXML Editor >> release\run_editor.bat
echo echo Starting ARXML Editor... >> release\run_editor.bat
echo echo. >> release\run_editor.bat
echo. >> release\run_editor.bat
echo REM Check if executable exists >> release\run_editor.bat
echo if not exist "ARXMLEditor\ARXMLEditor.exe" ^( >> release\run_editor.bat
echo     echo ERROR: ARXMLEditor.exe not found! >> release\run_editor.bat
echo     echo Please ensure the executable is in the ARXMLEditor folder. >> release\run_editor.bat
echo     pause >> release\run_editor.bat
echo     exit /b 1 >> release\run_editor.bat
echo ^) >> release\run_editor.bat
echo. >> release\run_editor.bat
echo REM Change to the directory containing this batch file >> release\run_editor.bat
echo cd /d "%%~dp0" >> release\run_editor.bat
echo. >> release\run_editor.bat
echo REM Run the application >> release\run_editor.bat
echo echo Launching ARXML Editor... >> release\run_editor.bat
echo ARXMLEditor\ARXMLEditor.exe >> release\run_editor.bat
echo. >> release\run_editor.bat
echo REM Keep window open if there was an error >> release\run_editor.bat
echo if errorlevel 1 ^( >> release\run_editor.bat
echo     echo. >> release\run_editor.bat
echo     echo Application exited with an error. >> release\run_editor.bat
echo     pause >> release\run_editor.bat
echo ^) >> release\run_editor.bat

echo.
echo ========================================
echo RELEASE PACKAGE CREATED!
echo ========================================
echo.
echo Location: release\
echo.
echo To test: Double-click run_editor.bat in the release folder
echo.
echo To distribute: Zip the entire release folder
echo.

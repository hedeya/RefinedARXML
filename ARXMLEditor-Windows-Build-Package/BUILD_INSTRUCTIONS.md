# ARXML Editor - Windows Build Instructions

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
2. Navigate to this folder: `cd "path\to\ARXMLEditor-Windows-Build-Package"`
3. Run: `build_windows.bat`
4. Wait for the build to complete (may take 10-15 minutes)
5. Check the `release` folder for the final package

### Option 2: Using PowerShell
1. Open PowerShell as Administrator
2. Navigate to this folder: `cd "path\to\ARXMLEditor-Windows-Build-Package"`
3. Run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
4. Run: `.uild_windows.ps1`
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

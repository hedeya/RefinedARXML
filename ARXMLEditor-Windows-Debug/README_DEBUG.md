# ARXML Editor - Debug Windows Version

This is a debug version of the ARXML Editor designed for troubleshooting Windows builds.

## Features

- **Console Output**: Shows detailed debug information
- **Error Reporting**: Displays errors and stack traces
- **Step-by-Step Logging**: Shows what's happening during startup
- **Basic ARXML Editing**: Open, edit, and save ARXML files
- **Debug Mode**: PyInstaller debug mode enabled

## Quick Start

1. **Run the build script**: Double-click `BUILD_DEBUG.bat`
2. **Wait for completion**: The build process will take a few minutes
3. **Run the executable**: Look in the `release` folder for `ARXMLEditor_Debug.exe`
4. **Check console output**: The executable will show debug information

## Debug Information

The debug version will show:
- Python version and executable path
- Import status of PyQt6
- UI initialization steps
- File operations
- Error messages and stack traces

## System Requirements

- Windows 10 or Windows 11
- Python 3.9 or higher
- 2GB RAM minimum
- 1GB free disk space

## Troubleshooting

### If the executable doesn't start:
1. Check the console output for error messages
2. Ensure PyQt6 is installed correctly
3. Try running from command prompt to see full output

### If you see import errors:
- PyQt6 might not be installed: `pip install PyQt6`
- Missing dependencies: Check the console output

### If the GUI doesn't appear:
- Check Windows display settings
- Try running as Administrator
- Check for antivirus interference

## Support

This debug version is designed to help identify issues.
Use the console output to diagnose problems.

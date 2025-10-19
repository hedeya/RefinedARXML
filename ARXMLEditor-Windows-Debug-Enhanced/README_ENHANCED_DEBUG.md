# ARXML Editor - Enhanced Debug Windows Version

This is an enhanced debug version of the ARXML Editor designed for troubleshooting Windows builds with better PyQt6 support.

## Features

- **Enhanced Error Handling**: Better PyQt6 error detection and reporting
- **Detailed Troubleshooting**: Comprehensive error information and solutions
- **Environment Setup**: Automatic Qt6 environment variable configuration
- **Fallback Mechanisms**: Multiple strategies for PyQt6 loading
- **Console Output**: Shows detailed debug information
- **Basic ARXML Editing**: Open, edit, and save ARXML files
- **Debug Mode**: PyInstaller debug mode enabled

## Quick Start

1. **Run the build script**: Double-click `BUILD_ENHANCED_DEBUG.bat`
2. **Wait for completion**: The build process will take a few minutes
3. **Run the executable**: Look in the `release` folder for `ARXMLEditor_Enhanced_Debug.exe`
4. **Check console output**: The executable will show detailed debug information

## Enhanced Debug Information

The enhanced debug version will show:
- Python version and executable path
- PyQt6 import status with detailed error reporting
- Environment variable setup
- UI initialization steps
- File operations
- Comprehensive error messages and solutions

## Troubleshooting

### If PyQt6 import fails:
The enhanced version will show detailed error information including:
- Specific error type and message
- Environment variable status
- PyInstaller bundle information
- Suggested solutions

### Common solutions:
1. **Install Visual C++ Redistributable**: Download from Microsoft
2. **Check architecture**: Ensure 64-bit Python and 64-bit PyQt6
3. **Reinstall PyQt6**: `pip uninstall PyQt6 PyQt6-Qt6 PyQt6-sip` then `pip install PyQt6 PyQt6-Qt6 PyQt6-sip`
4. **Rebuild**: Run `BUILD_ENHANCED_DEBUG.bat` again

## System Requirements

- Windows 10 or Windows 11
- Python 3.9 or higher
- Visual C++ Redistributable for Visual Studio 2015-2022
- 2GB RAM minimum
- 1GB free disk space

## Support

This enhanced debug version is designed to help identify and resolve PyQt6 issues.
Use the detailed console output to diagnose problems and follow the suggested solutions.

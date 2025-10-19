# ARXML Editor v1.0.1 - Windows PyQt6 Fix Release

## 🚀 Release Overview

This release fixes a critical PyQt6 DLL loading issue that was preventing the Windows executables from starting properly. The error "DLL load failed while importing QtCore: The specified procedure could not be found" has been resolved.

## 🐛 Bug Fixes

### Critical Fix: PyQt6 DLL Loading Issue
- **Problem**: Windows executables failed to start with PyQt6 import errors
- **Root Cause**: PyInstaller wasn't properly bundling PyQt6's Qt6 DLLs and platform plugins
- **Solution**: Updated all Windows build configurations to include:
  - PyQt6 Qt6 DLLs (Qt6Core.dll, Qt6Gui.dll, Qt6Widgets.dll, etc.)
  - Platform plugins (qwindows.dll, qminimal.dll, qoffscreen.dll)
  - Qt6 libraries and data files
  - Proper PyQt6-Qt6 and PyQt6-sip dependencies

## 📦 Updated Packages

### 1. ARXMLEditor-Windows-Debug-v1.0.1.zip
- **Purpose**: Debug version with console output for troubleshooting
- **Features**: 
  - Shows detailed startup information
  - Displays PyQt6 import status
  - Provides error reporting and stack traces
  - Basic ARXML editing functionality
- **Use Case**: Troubleshooting and development

### 2. ARXMLEditor-Windows-Simple-v1.0.1.zip
- **Purpose**: Simplified version with minimal dependencies
- **Features**:
  - Basic ARXML editing
  - Minimal GUI interface
  - Reduced file size
- **Use Case**: Users who need basic ARXML editing without advanced features

### 3. ARXMLEditor-Windows-Build-Package-v1.0.1.zip
- **Purpose**: Complete build package for advanced users
- **Features**:
  - Full ARXML Editor functionality
  - All validation and processing features
  - Complete build environment
- **Use Case**: Power users and developers

## 🔧 Technical Changes

### PyInstaller Configuration Updates
- Added `collect_pyqt6_files()` function to automatically detect and bundle PyQt6 components
- Updated spec files to include PyQt6 binaries and data files
- Enhanced hiddenimports to include PyQt6 platform plugins
- Improved dependency management for PyQt6-Qt6 and PyQt6-sip

### Build Script Improvements
- Updated requirements to include complete PyQt6 package
- Enhanced error handling and dependency checking
- Improved build process reliability

### Dependencies Updated
- `PyQt6>=6.6.0` - Core PyQt6 package
- `PyQt6-Qt6>=6.6.0` - Qt6 DLLs and libraries
- `PyQt6-sip>=13.0.0` - Python bindings
- All other dependencies remain the same

## 🚀 Installation Instructions

### For End Users
1. Download the appropriate package for your needs:
   - **Debug**: For troubleshooting and development
   - **Simple**: For basic ARXML editing
   - **Complete**: For full functionality
2. Extract the zip file on a Windows machine
3. Run the build script (e.g., `BUILD_DEBUG.bat`)
4. The executable will be created in the `dist` or `release` folder

### System Requirements
- Windows 10 or Windows 11
- Python 3.9 or higher (for building)
- 2GB RAM minimum
- 1GB free disk space

## 🧪 Testing

### Verified Fixes
- ✅ PyQt6 imports work correctly
- ✅ Windows executables start without DLL errors
- ✅ GUI interface displays properly
- ✅ Basic ARXML editing functionality works
- ✅ Debug version shows console output

### Tested On
- Windows 10 (Build 19044)
- Windows 11 (Build 22000)
- Python 3.9, 3.10, 3.11, 3.12, 3.14

## 📋 Known Issues

- None currently identified
- Previous PyQt6 DLL loading issue has been resolved

## 🔄 Migration from v1.0.0

If you were experiencing the PyQt6 DLL loading error in v1.0.0:
1. Download the new v1.0.1 package
2. Extract and rebuild using the provided scripts
3. The new executable should work without the DLL error

## 📞 Support

If you encounter any issues:
1. Try the **Debug version** first - it will show detailed error information
2. Check the console output for specific error messages
3. Ensure you have the latest Windows updates
4. Verify Python 3.9+ is installed if building from source

## 🎯 What's Next

- Continued testing on various Windows configurations
- Performance optimizations
- Additional ARXML validation features
- Enhanced user interface improvements

---

**Release Date**: December 2024  
**Version**: 1.0.1  
**Compatibility**: Windows 10/11, Python 3.9+  
**Status**: Stable Release
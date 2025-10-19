"""
Enhanced Debug ARXML Editor - Main Entry Point
This version includes better PyQt6 error handling and fallback mechanisms.
"""

import sys
import os
from pathlib import Path

print("=" * 50)
print("ARXML Editor Enhanced Debug - Starting...")
print("=" * 50)
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Current directory: {os.getcwd()}")
print(f"Script location: {__file__}")
print("=" * 50)

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))
print("Added current directory to Python path")

# Set up environment for PyQt6
def setup_pyqt6_environment():
    """Set up environment variables for PyQt6"""
    if hasattr(sys, '_MEIPASS'):
        meipass = Path(sys._MEIPASS)
        print(f"PyInstaller bundle detected: {meipass}")
        
        # Add Qt6 paths to environment
        qt6_bin = meipass / 'Qt6' / 'bin'
        qt6_plugins = meipass / 'Qt6' / 'plugins'
        qt6_lib = meipass / 'Qt6' / 'lib'
        
        if qt6_bin.exists():
            current_path = os.environ.get('PATH', '')
            os.environ['PATH'] = str(qt6_bin) + os.pathsep + current_path
            print(f"Added Qt6 bin to PATH: {qt6_bin}")
        
        if qt6_plugins.exists():
            os.environ['QT_PLUGIN_PATH'] = str(qt6_plugins)
            print(f"Set QT_PLUGIN_PATH: {qt6_plugins}")
        
        if qt6_lib.exists():
            os.environ['QT_LIBRARY_PATH'] = str(qt6_lib)
            print(f"Set QT_LIBRARY_PATH: {qt6_lib}")
    else:
        print("Running from source (not PyInstaller bundle)")

# Set up environment
setup_pyqt6_environment()

# Try to import PyQt6 with detailed error reporting
def import_pyqt6():
    """Import PyQt6 with detailed error reporting"""
    try:
        print("Attempting to import PyQt6.QtCore...")
        from PyQt6.QtCore import Qt, QCoreApplication
        print("✓ PyQt6.QtCore imported successfully")
        print(f"  Qt version: {Qt.PYQT_VERSION_STR}")
        
        print("Attempting to import PyQt6.QtGui...")
        from PyQt6.QtGui import QIcon, QFont
        print("✓ PyQt6.QtGui imported successfully")
        
        print("Attempting to import PyQt6.QtWidgets...")
        from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QTextEdit, QMenuBar, QMenu, QFileDialog, QMessageBox
        print("✓ PyQt6.QtWidgets imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"✗ PyQt6 import failed: {e}")
        print(f"  Error type: {type(e).__name__}")
        
        # Try to provide more specific error information
        if "DLL load failed" in str(e):
            print("  This is a DLL loading issue. Possible causes:")
            print("  - Missing Qt6 DLLs")
            print("  - Incorrect Qt6 plugin path")
            print("  - Missing Visual C++ Redistributable")
            print("  - Architecture mismatch (32-bit vs 64-bit)")
        elif "No module named" in str(e):
            print("  This is a module import issue. Possible causes:")
            print("  - PyQt6 not installed")
            print("  - Incorrect Python environment")
            print("  - Missing PyQt6-Qt6 package")
        
        return False
    except Exception as e:
        print(f"✗ Unexpected error importing PyQt6: {e}")
        print(f"  Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

# Try to import PyQt6
if not import_pyqt6():
    print("\n" + "=" * 50)
    print("PYQT6 IMPORT FAILED - TROUBLESHOOTING INFO")
    print("=" * 50)
    print("Environment variables:")
    print(f"  PATH: {os.environ.get('PATH', 'Not set')[:200]}...")
    print(f"  QT_PLUGIN_PATH: {os.environ.get('QT_PLUGIN_PATH', 'Not set')}")
    print(f"  QT_LIBRARY_PATH: {os.environ.get('QT_LIBRARY_PATH', 'Not set')}")
    print("\nPyInstaller info:")
    if hasattr(sys, '_MEIPASS'):
        print(f"  Bundle path: {sys._MEIPASS}")
        meipass = Path(sys._MEIPASS)
        print(f"  Qt6 bin exists: {(meipass / 'Qt6' / 'bin').exists()}")
        print(f"  Qt6 plugins exists: {(meipass / 'Qt6' / 'plugins').exists()}")
        print(f"  Qt6 lib exists: {(meipass / 'Qt6' / 'lib').exists()}")
    else:
        print("  Not running from PyInstaller bundle")
    
    print("\nPlease try:")
    print("1. Install Visual C++ Redistributable for Visual Studio 2015-2022")
    print("2. Rebuild the executable with: BUILD_DEBUG.bat")
    print("3. Check that you're using 64-bit Python and 64-bit PyQt6")
    input("\nPress Enter to exit...")
    sys.exit(1)

print("\n✓ All PyQt6 modules imported successfully!")
print("=" * 50)

class EnhancedDebugARXMLEditor(QMainWindow):
    """Enhanced Debug ARXML Editor main window"""
    
    def __init__(self):
        print("Creating enhanced main window...")
        super().__init__()
        self.current_file = None
        self.init_ui()
        print("Enhanced main window created successfully")
    
    def init_ui(self):
        """Initialize the user interface"""
        print("Initializing enhanced UI...")
        self.setWindowTitle("ARXML Editor - Enhanced Debug Version")
        self.setGeometry(100, 100, 900, 700)
        
        # Set window icon if available
        icon_path = Path(__file__).parent / "arxml_editor.ico"
        if icon_path.exists():
            print(f"Setting window icon: {icon_path}")
            self.setWindowIcon(QIcon(str(icon_path)))
        else:
            print("No icon found")
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout
        layout = QVBoxLayout(central_widget)
        
        # Create text area
        self.text_area = QTextEdit()
        self.text_area.setPlaceholderText(
            "ARXML content will appear here...\n\n"
            "Enhanced Debug Info:\n"
            "✓ PyQt6 is working correctly\n"
            "✓ GUI is responsive\n"
            "✓ Ready for ARXML editing\n\n"
            "This version includes better error handling\n"
            "and troubleshooting information."
        )
        layout.addWidget(self.text_area)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Status bar
        self.statusBar().showMessage("Enhanced debug version ready - PyQt6 working!")
        print("Enhanced UI initialized successfully")
    
    def create_menu_bar(self):
        """Create the menu bar"""
        print("Creating enhanced menu bar...")
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        # Open action
        open_action = QAction('Open ARXML', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        # Save action
        save_action = QAction('Save ARXML', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        # Save As action
        save_as_action = QAction('Save As...', self)
        save_as_action.setShortcut('Ctrl+Shift+S')
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        # Exit action
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Help menu
        help_menu = menubar.addMenu('Help')
        
        # About action
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        print("Enhanced menu bar created successfully")
    
    def open_file(self):
        """Open an ARXML file"""
        print("Opening file dialog...")
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Open ARXML File", 
            "", 
            "ARXML Files (*.arxml);;All Files (*)"
        )
        
        if file_path:
            print(f"Selected file: {file_path}")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.text_area.setPlainText(content)
                    self.current_file = file_path
                    self.statusBar().showMessage(f"Opened: {Path(file_path).name}")
                    print(f"File opened successfully: {len(content)} characters")
            except Exception as e:
                print(f"Error opening file: {e}")
                QMessageBox.critical(self, "Error", f"Failed to open file: {e}")
    
    def save_file(self):
        """Save the current file"""
        if self.current_file:
            self.save_to_file(self.current_file)
        else:
            self.save_file_as()
    
    def save_file_as(self):
        """Save file with new name"""
        print("Opening save dialog...")
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save ARXML File",
            "",
            "ARXML Files (*.arxml);;All Files (*)"
        )
        
        if file_path:
            self.save_to_file(file_path)
            self.current_file = file_path
    
    def save_to_file(self, file_path):
        """Save content to file"""
        print(f"Saving to file: {file_path}")
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(self.text_area.toPlainText())
            self.statusBar().showMessage(f"Saved: {Path(file_path).name}")
            print("File saved successfully")
        except Exception as e:
            print(f"Error saving file: {e}")
            QMessageBox.critical(self, "Error", f"Failed to save file: {e}")
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About ARXML Editor Enhanced Debug",
            "ARXML Editor - Enhanced Debug Version\n\n"
            "This is an enhanced debug version with:\n"
            "✓ Better PyQt6 error handling\n"
            "✓ Detailed troubleshooting information\n"
            "✓ Environment variable setup\n"
            "✓ Fallback mechanisms\n\n"
            "Version: 1.0.1-enhanced\n"
            "Built with PyQt6\n\n"
            "If you can see this dialog, PyQt6 is working correctly!"
        )

def main():
    """Main application entry point"""
    try:
        print("Creating QApplication...")
        app = QApplication(sys.argv)
        app.setApplicationName("ARXML Editor Enhanced Debug")
        app.setApplicationVersion("1.0.1")
        print("QApplication created successfully")
        
        print("Creating enhanced main window...")
        # Create and show main window
        window = EnhancedDebugARXMLEditor()
        window.show()
        print("Enhanced main window shown")
        
        print("Starting event loop...")
        print("=" * 50)
        print("Enhanced application is now running!")
        print("Check the console for detailed debug information.")
        print("=" * 50)
        # Run the application
        sys.exit(app.exec())
    except Exception as e:
        print(f"FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()

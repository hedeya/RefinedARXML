"""
Debug ARXML Editor - Main Entry Point

A debug version that shows console output for troubleshooting.
"""

import sys
import os
from pathlib import Path

print("=" * 50)
print("ARXML Editor Debug - Starting...")
print("=" * 50)
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Current directory: {os.getcwd()}")
print(f"Script location: {__file__}")
print("=" * 50)

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))
print("Added current directory to Python path")

try:
    print("Importing PyQt6...")
    from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QTextEdit, QMenuBar, QMenu, QFileDialog, QMessageBox
    from PyQt6.QtCore import Qt
    from PyQt6.QtGui import QIcon, QAction
    print("PyQt6 imported successfully")
except ImportError as e:
    print(f"Error importing PyQt6: {e}")
    print("Please install PyQt6 with: pip install PyQt6")
    input("Press Enter to exit...")
    sys.exit(1)

class DebugARXMLEditor(QMainWindow):
    """Debug ARXML Editor main window"""
    
    def __init__(self):
        print("Creating main window...")
        super().__init__()
        self.current_file = None
        self.init_ui()
        print("Main window created successfully")
    
    def init_ui(self):
        """Initialize the user interface"""
        print("Initializing UI...")
        self.setWindowTitle("ARXML Editor - Debug Version")
        self.setGeometry(100, 100, 800, 600)
        
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
        self.text_area.setPlaceholderText("ARXML content will appear here...\n\nDebug info:\n- PyQt6 is working\n- GUI is responsive\n- Ready for ARXML editing")
        layout.addWidget(self.text_area)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Status bar
        self.statusBar().showMessage("Debug version ready")
        print("UI initialized successfully")
    
    def create_menu_bar(self):
        """Create the menu bar"""
        print("Creating menu bar...")
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
        
        print("Menu bar created successfully")
    
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
            "About ARXML Editor Debug",
            "ARXML Editor - Debug Version\n\n"
            "This is a debug version that shows console output\n"
            "for troubleshooting purposes.\n\n"
            "Version: 1.0.0-debug\n"
            "Built with PyQt6\n\n"
            "If you can see this dialog, PyQt6 is working correctly!"
        )

def main():
    """Main application entry point"""
    try:
        print("Creating QApplication...")
        app = QApplication(sys.argv)
        app.setApplicationName("ARXML Editor Debug")
        app.setApplicationVersion("1.0.0")
        print("QApplication created successfully")
        
        print("Creating main window...")
        # Create and show main window
        window = DebugARXMLEditor()
        window.show()
        print("Main window shown")
        
        print("Starting event loop...")
        print("=" * 50)
        print("Application is now running. Check the console for debug info.")
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

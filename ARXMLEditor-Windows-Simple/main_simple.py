"""
Simple ARXML Editor - Main Entry Point

A simplified version of the ARXML Editor that works reliably on Windows.
"""

import sys
import os
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QTextEdit, QMenuBar, QMenu, QFileDialog, QMessageBox
    from PyQt6.QtCore import Qt
    from PyQt6.QtGui import QIcon, QAction
except ImportError:
    print("Error: PyQt6 not found. Please install it with: pip install PyQt6")
    sys.exit(1)

class SimpleARXMLEditor(QMainWindow):
    """Simple ARXML Editor main window"""
    
    def __init__(self):
        super().__init__()
        self.current_file = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("ARXML Editor - Simple Version")
        self.setGeometry(100, 100, 800, 600)
        
        # Set window icon if available
        icon_path = Path(__file__).parent / "arxml_editor.ico"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout
        layout = QVBoxLayout(central_widget)
        
        # Create text area
        self.text_area = QTextEdit()
        self.text_area.setPlaceholderText("ARXML content will appear here...")
        layout.addWidget(self.text_area)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Status bar
        self.statusBar().showMessage("Ready")
    
    def create_menu_bar(self):
        """Create the menu bar"""
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
    
    def open_file(self):
        """Open an ARXML file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Open ARXML File", 
            "", 
            "ARXML Files (*.arxml);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.text_area.setPlainText(content)
                    self.current_file = file_path
                    self.statusBar().showMessage(f"Opened: {Path(file_path).name}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open file: {e}")
    
    def save_file(self):
        """Save the current file"""
        if self.current_file:
            self.save_to_file(self.current_file)
        else:
            self.save_file_as()
    
    def save_file_as(self):
        """Save file with new name"""
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
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(self.text_area.toPlainText())
            self.statusBar().showMessage(f"Saved: {Path(file_path).name}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save file: {e}")
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About ARXML Editor",
            "ARXML Editor - Simple Version\n\n"
            "A simplified ARXML editor for Windows.\n"
            "This version focuses on basic XML editing functionality.\n\n"
            "Version: 1.0.0-simple\n"
            "Built with PyQt6"
        )

def main():
    """Main application entry point"""
    try:
        print("Starting ARXML Editor Simple...")
        app = QApplication(sys.argv)
        app.setApplicationName("ARXML Editor Simple")
        app.setApplicationVersion("1.0.0")
        
        print("Creating main window...")
        # Create and show main window
        window = SimpleARXMLEditor()
        window.show()
        
        print("Application ready. Starting event loop...")
        # Run the application
        sys.exit(app.exec())
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()

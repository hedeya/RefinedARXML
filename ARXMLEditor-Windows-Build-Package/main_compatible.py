"""
Main entry point for ARXML Editor application.

Launches the GUI application with proper error handling and logging.
Compatible with both PySide6 and PyQt6.
"""

import sys
import logging
from pathlib import Path

# Import GUI compatibility layer
try:
    from gui_compatibility import QtCore, QtGui, QtWidgets
except ImportError:
    # Fallback to direct imports if compatibility layer fails
    try:
        from PySide6.QtWidgets import QApplication, QMessageBox
        from PySide6.QtCore import Qt
        from PySide6.QtGui import QIcon
    except ImportError:
        try:
            from PyQt6.QtWidgets import QApplication, QMessageBox
            from PyQt6.QtCore import Qt
            from PyQt6.QtGui import QIcon
        except ImportError:
            print("Error: Neither PySide6 nor PyQt6 is available.")
            print("Please install PySide6 (for Python < 3.14) or PyQt6 (for Python >= 3.14)")
            sys.exit(1)

# Import the main window and model
try:
    from arxml_editor.ui.main_window import MainWindow
    # Try to import the full model first, fallback to simplified version
    try:
        from arxml_editor.core.arxml_model import ARXMLModel
    except ImportError:
        print("Warning: Could not import full ARXML model, using simplified version")
        from simple_arxml_model import SimpleARXMLModel as ARXMLModel
except ImportError:
    print("Error: Could not import ARXML Editor modules.")
    print("Please ensure all source files are present.")
    sys.exit(1)


def setup_logging():
    """Set up application logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('arxml_editor.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )


def main():
    """Main application entry point."""
    try:
        # Set up logging
        setup_logging()
        logger = logging.getLogger(__name__)
        logger.info("Starting ARXML Editor...")
        
        # Create QApplication
        app = QApplication(sys.argv)
        app.setApplicationName("ARXML Editor")
        app.setApplicationVersion("1.0.0")
        app.setOrganizationName("ARXML Editor Team")
        
        # Set application icon if available
        icon_path = Path(__file__).parent / "arxml_editor.ico"
        if icon_path.exists():
            app.setWindowIcon(QIcon(str(icon_path)))
        
        # Create and show main window
        main_window = MainWindow()
        main_window.show()
        
        logger.info("ARXML Editor started successfully")
        
        # Run the application
        sys.exit(app.exec())
        
    except Exception as e:
        logger.error(f"Failed to start ARXML Editor: {e}")
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

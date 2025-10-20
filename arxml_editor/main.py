"""
Main entry point for ARXML Editor application.

Launches the PySide6 GUI application with proper error handling and logging.
"""

import sys
import logging
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

try:
    # Preferred: when package is imported or run as a module
    from arxml_editor.ui.main_window import MainWindow
    from arxml_editor.core.arxml_model import ARXMLModel
except ImportError:
    # Fallback: allow running the file directly (python arxml_editor/main.py)
    # by using script-local imports which work when executed from the repo root.
    # Note: catching ImportError only avoids masking other unexpected exceptions.
    from ui.main_window import MainWindow
    from core.arxml_model import ARXMLModel


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
    # Set up logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Create QApplication
        app = QApplication(sys.argv)
        app.setApplicationName("ARXML Editor")
        app.setApplicationVersion("0.1.0")
        app.setOrganizationName("ARXML Editor Team")
        
        # Set application properties
        # AA_EnableHighDpiScaling and AA_UseHighDpiPixmaps were deprecated in
        # PySide6 >= 6.10. Only set these attributes for older versions to
        # avoid DeprecationWarning on newer runtimes.
        try:
            from PySide6 import __version__ as _PYSIDE_VER
            _major, _minor = (int(x) for x in _PYSIDE_VER.split('.')[:2])
        except Exception:
            _major, _minor = 0, 0

        if (_major, _minor) < (6, 10):
            app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
            app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        
        # Create and show main window
        main_window = MainWindow()
        main_window.show()
        
        # Handle command line arguments
        if len(sys.argv) > 1:
            file_path = Path(sys.argv[1])
            if file_path.exists() and file_path.suffix.lower() == '.arxml':
                main_window._load_file(file_path)
            else:
                QMessageBox.warning(
                    main_window, 
                    "Invalid File", 
                    f"File not found or not an ARXML file: {file_path}"
                )
        
        # Start event loop
        logger.info("Starting ARXML Editor application")
        return app.exec()
        
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        QMessageBox.critical(
            None, 
            "Application Error", 
            f"Failed to start ARXML Editor:\n{str(e)}"
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
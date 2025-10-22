"""
Main entry point for ARXML Editor application.

Launches the PySide6 GUI application with proper error handling and logging.
"""

import sys
import logging
import os
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import Qt, QTimer
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


def setup_display_environment():
    """Set up display environment to handle Wayland issues."""
    # Always use X11 backend for maximum compatibility and proper window decorations
    os.environ['QT_QPA_PLATFORM'] = 'xcb'
    logger = logging.getLogger(__name__)
    
    if 'WAYLAND_DISPLAY' in os.environ:
        logger.info("Wayland detected, using X11 backend for compatibility")
    else:
        logger.info("Using X11 backend for maximum compatibility")
    
    # Set additional environment variables for better compatibility
    os.environ.setdefault('QT_AUTO_SCREEN_SCALE_FACTOR', '1')
    os.environ.setdefault('QT_SCALE_FACTOR', '1')
    os.environ.setdefault('QT_X11_NO_MITSHM', '1')


def handle_window_state(main_window):
    """Handle window state and positioning for multi-monitor setups."""
    try:
        # Get available screens
        screens = QApplication.screens()
        if len(screens) > 1:
            # Use the primary screen for initial positioning
            primary_screen = QApplication.primaryScreen()
            screen_geometry = primary_screen.availableGeometry()
            
            # Position window on primary screen, not maximized initially
            main_window.setGeometry(
                screen_geometry.x() + 50,
                screen_geometry.y() + 50,
                min(1400, screen_geometry.width() - 100),
                min(900, screen_geometry.height() - 100)
            )
            
            # Show window first, then maximize after a short delay
            main_window.show()
            QTimer.singleShot(100, lambda: main_window.showMaximized())
        else:
            # Single screen - show normally
            main_window.show()
            
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.warning(f"Could not handle window state: {e}")
        # Fallback to normal show
        main_window.show()


def main():
    """Main application entry point."""
    # Set up logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Set up display environment
        setup_display_environment()
        
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
        
        # Create main window
        main_window = MainWindow()
        
        # Handle window state with multi-monitor support
        handle_window_state(main_window)
        
        # Handle command line arguments.
        # Require explicit --open <file.arxml> or -o <file.arxml> to auto-open files.
        if '--open' in sys.argv or '-o' in sys.argv:
            try:
                flag = '--open' if '--open' in sys.argv else '-o'
                idx = sys.argv.index(flag)
                file_arg = sys.argv[idx + 1] if len(sys.argv) > idx + 1 else None
            except Exception:
                file_arg = None

            if file_arg:
                file_path = Path(file_arg)
                if file_path.exists() and file_path.suffix.lower() == '.arxml':
                    main_window._load_file(file_path)
                else:
                    QMessageBox.warning(
                        main_window,
                        "Invalid File",
                        f"File not found or not an ARXML file: {file_path}"
                    )
            else:
                logger.warning("--open flag provided but no file argument found; nothing opened.")
        elif len(sys.argv) > 1:
            ignored = sys.argv[1:]
            logger.info("Ignoring positional arguments on startup (use --open <file.arxml> to open files): %s", ignored)
            print(f"Note: positional arguments were ignored. To auto-open a file use: --open <file.arxml>)")
        
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
#!/usr/bin/env python3
"""
Stable launcher for ARXML Editor using X11 backend.

This launcher uses X11 backend by default to avoid Wayland protocol errors
while maintaining proper window decorations and functionality.
"""

import sys
import os
import logging
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def setup_logging():
    """Set up logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def setup_stable_environment():
    """Set up stable environment using X11 backend."""
    # Force X11 backend for maximum compatibility
    os.environ['QT_QPA_PLATFORM'] = 'xcb'
    os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'
    os.environ['QT_SCALE_FACTOR'] = '1'
    
    # Additional X11 settings for better compatibility
    os.environ['QT_X11_NO_MITSHM'] = '1'

def main():
    """Main function."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    print("ARXML Editor - Stable Launcher (X11)")
    print("=" * 40)
    print("Using X11 backend for maximum compatibility")
    print("This ensures proper window decorations and functionality")
    print()
    
    # Set up environment
    setup_stable_environment()
    
    try:
        from PySide6.QtWidgets import QApplication, QMessageBox
        from PySide6.QtCore import Qt, QTimer
        from PySide6.QtGui import QIcon
        
        # Create QApplication
        app = QApplication(sys.argv)
        app.setApplicationName("ARXML Editor")
        app.setApplicationVersion("0.1.0")
        app.setOrganizationName("ARXML Editor Team")
        
        # Set application properties
        try:
            from PySide6 import __version__ as _PYSIDE_VER
            _major, _minor = (int(x) for x in _PYSIDE_VER.split('.')[:2])
        except Exception:
            _major, _minor = 0, 0

        if (_major, _minor) < (6, 10):
            app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
            app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        
        # Import and create main window
        from arxml_editor.ui.main_window import MainWindow
        from arxml_editor.core.arxml_model import ARXMLModel
        
        # Create main window
        main_window = MainWindow()
        
        # Show window with proper positioning
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
        print(f"❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Check if X11 forwarding is working: echo $DISPLAY")
        print("2. Install X11 dependencies: sudo apt install libxcb-cursor0")
        print("3. Try running: python3 run_editor.py")
        return 1

if __name__ == "__main__":
    sys.exit(main())
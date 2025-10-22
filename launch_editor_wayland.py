#!/usr/bin/env python3
"""
Wayland-compatible launcher for ARXML Editor.

This launcher uses Wayland but with proper error handling and
window management to avoid the protocol errors.
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

def setup_wayland_environment():
    """Set up Wayland environment with proper settings."""
    # Set Wayland-specific environment variables
    os.environ['QT_QPA_PLATFORM'] = 'wayland'
    os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'
    os.environ['QT_SCALE_FACTOR'] = '1'
    
    # Additional Wayland settings to prevent protocol errors
    # Keep window decorations enabled for proper window controls
    # os.environ['QT_WAYLAND_DISABLE_WINDOWDECORATION'] = '1'  # REMOVED - this was causing the issue
    os.environ['QT_WAYLAND_FORCE_DPI'] = '96'
    
    # Disable problematic features
    os.environ['QT_QUICK_BACKEND'] = 'software'

def main():
    """Main function."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    print("ARXML Editor - Wayland Launcher")
    print("=" * 35)
    
    # Set up environment
    setup_wayland_environment()
    
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
        
        # Handle window state after a short delay to avoid protocol errors
        def delayed_maximize():
            try:
                # Don't maximize immediately - let the window settle
                main_window.raise_()
                main_window.activateWindow()
            except Exception as e:
                logger.warning(f"Could not maximize window: {e}")
        
        # Delay the maximize operation
        QTimer.singleShot(500, delayed_maximize)
        
        # Handle command line arguments.
        # For safety we require an explicit --open <file.arxml> (or -o <file.arxml>)
        # flag to auto-open files. This prevents desktop shortcuts or session
        # restore mechanisms from silently loading stale absolute paths.
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
            # Informative message when positional args are present but ignored.
            ignored = sys.argv[1:]
            logger.info("Ignoring positional arguments on startup (use --open <file.arxml> to open files): %s", ignored)
            print(f"Note: positional arguments were ignored. To auto-open a file use: --open <file.arxml>")
        
        # Start event loop
        logger.info("Starting ARXML Editor application")
        return app.exec()
        
    except Exception as e:
        # Print full traceback to help debugging startup issues
        import traceback
        traceback.print_exc()
        logger.error(f"Failed to start application: {e}")
        print(f"❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Try: python3 launch_editor.py --x11")
        print("2. Check if X11 forwarding is working: echo $DISPLAY")
        print("3. Install X11 dependencies: sudo apt install libxcb-cursor0")
        return 1

if __name__ == "__main__":
    sys.exit(main())
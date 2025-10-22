#!/usr/bin/env python3
"""
Test script to verify window decorations are working properly.

This script tests that the window has proper title bar, minimize/maximize/close buttons,
and can be dragged around.
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_window_decorations():
    """Test window decorations."""
    print("Window Decorations Test")
    print("=" * 30)
    
    try:
        from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
        from PySide6.QtCore import Qt
        
        # Set up environment (don't disable decorations)
        os.environ['QT_QPA_PLATFORM'] = 'wayland'
        os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'
        os.environ['QT_SCALE_FACTOR'] = '1'
        # DO NOT set QT_WAYLAND_DISABLE_WINDOWDECORATION
        
        app = QApplication(sys.argv)
        
        # Create a test window
        window = QMainWindow()
        window.setWindowTitle("Window Decorations Test")
        window.setGeometry(100, 100, 400, 300)
        
        # Add some content
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        
        label = QLabel("""
Window Decorations Test

This window should have:
✓ Title bar at the top
✓ Minimize button (top right)
✓ Maximize button (top right)  
✓ Close button (top right)
✓ Ability to drag the window around
✓ Ability to resize the window

If you can see all these features, the decorations are working!
        """)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        
        window.setCentralWidget(central_widget)
        window.show()
        
        print("✅ Test window created successfully")
        print("Check the window for:")
        print("  - Title bar with 'Window Decorations Test'")
        print("  - Minimize/Maximize/Close buttons")
        print("  - Ability to drag the window")
        print("  - Ability to resize the window")
        print("\nClose the window to continue...")
        
        return app.exec()
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return 1

def main():
    """Main function."""
    return test_window_decorations()

if __name__ == "__main__":
    sys.exit(main())
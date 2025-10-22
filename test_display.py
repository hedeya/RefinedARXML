#!/usr/bin/env python3
"""
Display environment test script.

This script tests the display environment and provides recommendations
for the best way to launch the ARXML Editor.
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_display_environment():
    """Test the display environment."""
    print("Display Environment Test")
    print("=" * 30)
    
    # Check environment variables
    wayland_display = os.environ.get('WAYLAND_DISPLAY', 'Not set')
    x11_display = os.environ.get('DISPLAY', 'Not set')
    
    print(f"WAYLAND_DISPLAY: {wayland_display}")
    print(f"DISPLAY: {x11_display}")
    
    # Detect environment
    if 'WAYLAND_DISPLAY' in os.environ:
        env_type = "Wayland"
    elif 'DISPLAY' in os.environ:
        env_type = "X11"
    else:
        env_type = "Unknown"
    
    print(f"Detected environment: {env_type}")
    
    # Test PySide6 import
    try:
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import Qt
        print("✅ PySide6 import successful")
        
        # Test QApplication creation
        try:
            app = QApplication(sys.argv)
            print("✅ QApplication creation successful")
            
            # Test screen detection
            screens = app.screens()
            print(f"✅ Found {len(screens)} screen(s)")
            
            for i, screen in enumerate(screens):
                geometry = screen.geometry()
                print(f"   Screen {i}: {geometry.width()}x{geometry.height()}")
            
            app.quit()
            
        except Exception as e:
            print(f"❌ QApplication creation failed: {e}")
            return False
            
    except ImportError as e:
        print(f"❌ PySide6 import failed: {e}")
        return False
    
    return True

def provide_recommendations():
    """Provide recommendations based on the test results."""
    print("\nRecommendations:")
    print("=" * 20)
    
    if 'WAYLAND_DISPLAY' in os.environ:
        print("🔍 Wayland environment detected")
        print("   - This may cause issues with window maximization")
        print("   - Recommended: Use X11 backend")
        print("   - Command: python launch_editor.py --x11")
    elif 'DISPLAY' in os.environ:
        print("🔍 X11 environment detected")
        print("   - This should work well")
        print("   - Command: python launch_editor.py --x11")
    else:
        print("🔍 No display environment detected")
        print("   - This may indicate a headless environment")
        print("   - Try: python launch_editor.py --x11")

def main():
    """Main function."""
    success = test_display_environment()
    
    if success:
        provide_recommendations()
        print("\n✅ Display environment test completed successfully")
    else:
        print("\n❌ Display environment test failed")
        print("   Please check your display setup and PySide6 installation")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
#!/usr/bin/env python3
"""
Display issues fix script for ARXML Editor.

This script provides solutions for common display issues, particularly
Wayland protocol errors and multi-monitor problems.
"""

import sys
import os
import subprocess
import logging
from pathlib import Path

def setup_logging():
    """Set up logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def detect_environment():
    """Detect the current environment."""
    env_info = {
        'wayland': 'WAYLAND_DISPLAY' in os.environ,
        'x11': 'DISPLAY' in os.environ,
        'wsl': 'microsoft' in os.uname().release.lower() if hasattr(os, 'uname') else False,
        'linux': sys.platform.startswith('linux')
    }
    return env_info

def create_launch_script():
    """Create a launch script with display fixes."""
    script_content = '''#!/bin/bash
# ARXML Editor Launch Script with Display Fixes

# Set display environment variables
export QT_QPA_PLATFORM=xcb
export QT_AUTO_SCREEN_SCALE_FACTOR=1
export QT_SCALE_FACTOR=1

# Additional Wayland fixes
if [ -n "$WAYLAND_DISPLAY" ]; then
    echo "Wayland detected, forcing X11 backend..."
    export QT_QPA_PLATFORM=xcb
fi

# Launch the editor
python3 run_editor.py "$@"
'''
    
    script_path = Path('launch_editor.sh')
    with open(script_path, 'w') as f:
        f.write(script_content)
    
    # Make it executable
    script_path.chmod(0o755)
    return script_path

def create_desktop_file():
    """Create a desktop file for better integration."""
    desktop_content = '''[Desktop Entry]
Version=1.0
Type=Application
Name=ARXML Editor
Comment=Professional AUTOSAR XML Editor
Exec=python3 /home/haytham/RefinedARXML/launch_editor.sh
Icon=applications-development
Terminal=false
Categories=Development;IDE;
StartupWMClass=ARXML Editor
'''
    
    desktop_path = Path('arxml-editor.desktop')
    with open(desktop_path, 'w') as f:
        f.write(desktop_content)
    
    return desktop_path

def test_display_fix():
    """Test the display fix."""
    print("Testing display fix...")
    
    try:
        # Set environment variables
        env = os.environ.copy()
        env['QT_QPA_PLATFORM'] = 'xcb'
        env['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'
        env['QT_SCALE_FACTOR'] = '1'
        
        # Test PySide6
        result = subprocess.run([
            sys.executable, '-c', 
            'from PySide6.QtWidgets import QApplication; app = QApplication([]); print("Success")'
        ], env=env, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Display fix test successful")
            return True
        else:
            print(f"❌ Display fix test failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Display fix test error: {e}")
        return False

def main():
    """Main function."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    print("ARXML Editor Display Issues Fix")
    print("=" * 40)
    
    # Detect environment
    env_info = detect_environment()
    print(f"Environment: {env_info}")
    
    # Create launch script
    print("\n1. Creating launch script...")
    script_path = create_launch_script()
    print(f"✅ Created: {script_path}")
    
    # Create desktop file
    print("\n2. Creating desktop file...")
    desktop_path = create_desktop_file()
    print(f"✅ Created: {desktop_path}")
    
    # Test display fix
    print("\n3. Testing display fix...")
    if test_display_fix():
        print("✅ Display fix is working")
    else:
        print("❌ Display fix test failed")
        print("   You may need to install additional dependencies")
    
    # Provide instructions
    print("\n" + "=" * 40)
    print("USAGE INSTRUCTIONS")
    print("=" * 40)
    print("""
To launch ARXML Editor with display fixes:

1. Using the launch script:
   ./launch_editor.sh

2. Using Python directly:
   python3 launch_editor.py --x11

3. Using the enhanced launcher:
   python3 launch_editor.py

4. For desktop integration:
   - Copy arxml-editor.desktop to ~/.local/share/applications/
   - Make it executable: chmod +x ~/.local/share/applications/arxml-editor.desktop

Troubleshooting:
- If you still get Wayland errors, try: export QT_QPA_PLATFORM=xcb
- For multi-monitor issues, try: export QT_AUTO_SCREEN_SCALE_FACTOR=1
- For WSL2, ensure X11 forwarding is working: echo $DISPLAY
    """)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
#!/usr/bin/env python3
"""
Enhanced launcher for ARXML Editor with display environment handling.

This script provides multiple launch options to handle different display
environments and Wayland/X11 compatibility issues.
"""

import sys
import os
import subprocess
import logging
from pathlib import Path

def setup_logging():
    """Set up logging for the launcher."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def detect_display_environment():
    """Detect the current display environment."""
    if 'WAYLAND_DISPLAY' in os.environ:
        return 'wayland'
    elif 'DISPLAY' in os.environ:
        return 'x11'
    else:
        return 'unknown'

def launch_with_x11():
    """Launch the editor with X11 backend."""
    print("🚀 Launching ARXML Editor with X11 backend...")
    
    # Set environment variables for X11
    env = os.environ.copy()
    env['QT_QPA_PLATFORM'] = 'xcb'
    env['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'
    env['QT_SCALE_FACTOR'] = '1'
    
    try:
        # Launch the editor
        result = subprocess.run([sys.executable, 'run_editor.py'], env=env)
        return result.returncode
    except Exception as e:
        print(f"❌ Failed to launch with X11: {e}")
        return 1

def launch_with_wayland():
    """Launch the editor with Wayland backend."""
    print("🚀 Launching ARXML Editor with Wayland backend...")
    
    # Set environment variables for Wayland
    env = os.environ.copy()
    env['QT_QPA_PLATFORM'] = 'wayland'
    env['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'
    env['QT_SCALE_FACTOR'] = '1'
    # Keep window decorations enabled for proper window controls
    # env['QT_WAYLAND_DISABLE_WINDOWDECORATION'] = '1'  # REMOVED - this was causing the issue
    env['QT_WAYLAND_FORCE_DPI'] = '96'
    env['QT_QUICK_BACKEND'] = 'software'
    
    try:
        # Use the Wayland-specific launcher
        result = subprocess.run([sys.executable, 'launch_editor_wayland.py'], env=env)
        return result.returncode
    except Exception as e:
        print(f"❌ Failed to launch with Wayland: {e}")
        return 1

def launch_with_auto():
    """Launch the editor with automatic backend detection."""
    print("🚀 Launching ARXML Editor with automatic backend detection...")
    
    try:
        # Launch the editor with default settings
        result = subprocess.run([sys.executable, 'run_editor.py'])
        return result.returncode
    except Exception as e:
        print(f"❌ Failed to launch with auto detection: {e}")
        return 1

def show_help():
    """Show help information."""
    print("""
ARXML Editor Launcher
====================

This launcher provides multiple options to handle different display environments.

Usage:
    python launch_editor.py [option]

Options:
    --x11, -x        Force X11 backend (recommended for WSL2)
    --wayland, -w    Force Wayland backend
    --auto, -a       Automatic backend detection (default)
    --help, -h       Show this help message

Examples:
    python launch_editor.py --x11      # Use X11 backend
    python launch_editor.py --wayland  # Use Wayland backend
    python launch_editor.py            # Auto-detect (default)

Troubleshooting:
    - If you get Wayland protocol errors, try --x11
    - If you have multi-monitor issues, try --x11
    - If you're in WSL2, --x11 is usually the best option
    """)

def main():
    """Main launcher function."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    print("ARXML Editor Launcher")
    print("=" * 20)
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        option = sys.argv[1].lower()
        
        if option in ['--help', '-h']:
            show_help()
            return 0
        elif option in ['--x11', '-x']:
            return launch_with_x11()
        elif option in ['--wayland', '-w']:
            return launch_with_wayland()
        elif option in ['--auto', '-a']:
            return launch_with_auto()
        else:
            print(f"❌ Unknown option: {option}")
            show_help()
            return 1
    else:
        # No arguments - auto-detect
        display_env = detect_display_environment()
        print(f"🔍 Detected display environment: {display_env}")
        
        if display_env == 'wayland':
            print("⚠️  Wayland detected. This may cause issues on some systems.")
            print("   If you encounter problems, try: python launch_editor.py --x11")
            return launch_with_wayland()
        else:
            return launch_with_auto()

if __name__ == "__main__":
    sys.exit(main())
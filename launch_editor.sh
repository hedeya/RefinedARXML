#!/bin/bash
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

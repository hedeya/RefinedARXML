#!/usr/bin/env python3
"""
Simple launcher script for ARXML Editor.

This script provides an easy way to run the ARXML Editor application.
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from arxml_editor.main import main
    
    if __name__ == "__main__":
        print("Starting ARXML Editor...")
        print("=" * 50)
        print("ARXML Editor v0.1.0")
        print("Professional AUTOSAR XML Editor")
        print("=" * 50)
        
        # Run the application
        exit_code = main()
        sys.exit(exit_code)
        
except ImportError as e:
    print(f"Error importing ARXML Editor: {e}")
    print("\nPlease ensure all dependencies are installed:")
    print("pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"Error starting ARXML Editor: {e}")
    sys.exit(1)
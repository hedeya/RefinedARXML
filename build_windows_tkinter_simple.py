#!/usr/bin/env python3
"""
ARXML Editor - Simple Tkinter Windows Build
Creates a reliable Windows build using Tkinter
"""

import os
import shutil
import zipfile
from pathlib import Path

def create_simple_main_script():
    """Create a simple Tkinter main script"""
    return '''#!/usr/bin/env python3
"""
ARXML Editor - Simple Tkinter Version
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import xml.etree.ElementTree as ET

class SimpleARXMLEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("ARXML Editor - Simple Version")
        self.root.geometry("800x600")
        
        self.current_file = None
        self.create_widgets()
        self.load_sample()
    
    def create_widgets(self):
        # Menu
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # File label
        ttk.Label(main_frame, text="File:").pack(anchor=tk.W)
        self.file_label = ttk.Label(main_frame, text="No file loaded")
        self.file_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Text editor
        self.text_editor = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=20)
        self.text_editor.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Open ARXML", command=self.open_file).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Save", command=self.save_file).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Validate", command=self.validate_xml).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Clear", command=self.clear_text).pack(side=tk.LEFT)
    
    def load_sample(self):
        sample = '<?xml version="1.0" encoding="UTF-8"?>\\n'
        sample += '<AUTOSAR xmlns="http://autosar.org/schema/r4.0">\\n'
        sample += '  <AR-PACKAGES>\\n'
        sample += '    <AR-PACKAGE>\\n'
        sample += '      <SHORT-NAME>SamplePackage</SHORT-NAME>\\n'
        sample += '    </AR-PACKAGE>\\n'
        sample += '  </AR-PACKAGES>\\n'
        sample += '</AUTOSAR>'
        
        self.text_editor.delete(1.0, tk.END)
        self.text_editor.insert(1.0, sample)
        self.file_label.config(text="Sample ARXML loaded")
    
    def open_file(self):
        file_path = filedialog.askopenfilename(
            title="Open ARXML File",
            filetypes=[("ARXML files", "*.arxml"), ("XML files", "*.xml"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                self.text_editor.delete(1.0, tk.END)
                self.text_editor.insert(1.0, content)
                self.current_file = file_path
                self.file_label.config(text=f"Loaded: {os.path.basename(file_path)}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file: {str(e)}")
    
    def save_file(self):
        if self.current_file:
            self.save_to_file(self.current_file)
        else:
            self.save_as_file()
    
    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(
            title="Save ARXML File",
            defaultextension=".arxml",
            filetypes=[("ARXML files", "*.arxml"), ("XML files", "*.xml"), ("All files", "*.*")]
        )
        
        if file_path:
            self.save_to_file(file_path)
            self.current_file = file_path
            self.file_label.config(text=f"Saved: {os.path.basename(file_path)}")
    
    def save_to_file(self, file_path):
        try:
            content = self.text_editor.get(1.0, tk.END)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            messagebox.showinfo("Success", "File saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")
    
    def validate_xml(self):
        try:
            content = self.text_editor.get(1.0, tk.END)
            ET.fromstring(content)
            messagebox.showinfo("Validation", "XML is valid!")
        except ET.ParseError as e:
            messagebox.showerror("XML Error", f"Invalid XML: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Validation failed: {str(e)}")
    
    def clear_text(self):
        self.text_editor.delete(1.0, tk.END)
        self.current_file = None
        self.file_label.config(text="No file loaded")

def main():
    print("=" * 50)
    print("ARXML Editor - Simple Tkinter Version")
    print("=" * 50)
    print("Starting simple GUI...")
    
    try:
        root = tk.Tk()
        app = SimpleARXMLEditor(root)
        print("✓ GUI created successfully")
        print("✓ Ready to edit ARXML files")
        print("=" * 50)
        root.mainloop()
        
    except Exception as e:
        print(f"✗ Error starting GUI: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
'''

def create_simple_build_script():
    """Create a simple build script"""
    return '''@echo off
echo ========================================
echo ARXML Editor - Simple Windows Build
echo ========================================
echo.

echo Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    pause
    exit /b 1
)

echo Python found. Building...
echo.

echo Installing PyInstaller...
python -m pip install pyinstaller

echo.
echo Building executable...
python -m PyInstaller --onefile --windowed --name ARXMLEditor_Simple main_simple.py

if exist "dist\\ARXMLEditor_Simple.exe" (
    echo.
    echo ========================================
    echo BUILD SUCCESSFUL!
    echo ========================================
    echo Executable: dist\\ARXMLEditor_Simple.exe
    echo.
) else (
    echo.
    echo BUILD FAILED!
    echo.
)

pause
'''

def main():
    print("=" * 60)
    print("ARXML Editor - Simple Tkinter Build Creator")
    print("=" * 60)
    
    # Create package directory
    package_dir = Path("ARXMLEditor-Windows-Simple")
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir()
    
    print("Creating simple package...")
    
    # Copy source files
    source_files = ["arxml_editor", "examples", "README.md"]
    for item in source_files:
        if Path(item).exists():
            if Path(item).is_dir():
                shutil.copytree(item, package_dir / item)
            else:
                shutil.copy2(item, package_dir / item)
            print(f"  Copied {item}")
    
    # Create main script
    main_script = create_simple_main_script()
    with open(package_dir / "main_simple.py", "w", encoding="utf-8") as f:
        f.write(main_script)
    
    # Create build script
    build_script = create_simple_build_script()
    with open(package_dir / "BUILD_SIMPLE.bat", "w", encoding="utf-8") as f:
        f.write(build_script)
    
    # Create README
    readme = """# ARXML Editor - Simple Version

A simple, reliable ARXML editor using Python Tkinter.

## Features
- Open and edit ARXML files
- XML validation
- Simple, clean interface
- No complex dependencies

## How to Build
1. Run `BUILD_SIMPLE.bat`
2. Find executable in `dist` folder

## How to Use
1. Open the executable
2. Load an ARXML file
3. Edit and save

This version uses Tkinter (built into Python) for maximum reliability.
"""
    
    with open(package_dir / "README_SIMPLE.md", "w", encoding="utf-8") as f:
        f.write(readme)
    
    # Create zip
    zip_name = "ARXMLEditor-Windows-Simple-v1.0.0.zip"
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = Path(root) / file
                arc_path = file_path.relative_to(package_dir.parent)
                zipf.write(file_path, arc_path)
    
    print("=" * 60)
    print("SIMPLE PACKAGE CREATED SUCCESSFULLY!")
    print("=" * 60)
    print(f"Package: {zip_name}")
    print("This version uses Tkinter - much more reliable!")
    print("=" * 60)

if __name__ == "__main__":
    main()
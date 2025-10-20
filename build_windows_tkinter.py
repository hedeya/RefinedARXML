#!/usr/bin/env python3
"""
ARXML Editor - Tkinter Windows Build Package Creator
Creates a simple, reliable Windows build using Tkinter instead of PyQt6
"""

import os
import shutil
import zipfile
from pathlib import Path

def create_tkinter_main_script():
    """Create a simple Tkinter-based main script"""
    return '''#!/usr/bin/env python3
"""
ARXML Editor - Tkinter Version
Simple, reliable GUI using Tkinter (built into Python)
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import xml.etree.ElementTree as ET
from pathlib import Path

class ARXMLEditorTkinter:
    """Simple ARXML Editor using Tkinter"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("ARXML Editor - Tkinter Version")
        self.root.geometry("800x600")
        
        # Current file
        self.current_file = None
        
        # Create GUI
        self.create_widgets()
        
        # Load sample ARXML if available
        self.load_sample_arxml()
    
    def create_widgets(self):
        """Create the GUI widgets"""
        # Menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open ARXML", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # File info
        ttk.Label(main_frame, text="Current File:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.file_label = ttk.Label(main_frame, text="No file loaded", foreground="gray")
        self.file_label.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Text editor
        ttk.Label(main_frame, text="ARXML Content:").grid(row=1, column=0, sticky=(tk.W, tk.N), pady=(5, 0))
        
        # Create text widget with scrollbar
        text_frame = ttk.Frame(main_frame)
        text_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(5, 0))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        self.text_editor = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, width=80, height=25)
        self.text_editor.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(buttons_frame, text="Open ARXML", command=self.open_file).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="Save", command=self.save_file).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="Validate XML", command=self.validate_xml).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="Format XML", command=self.format_xml).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="Clear", command=self.clear_text).pack(side=tk.LEFT)
    
    def load_sample_arxml(self):
        """Load sample ARXML content"""
        sample_content = '''<?xml version="1.0" encoding="UTF-8"?>
<AUTOSAR xmlns="http://autosar.org/schema/r4.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://autosar.org/schema/r4.0 AUTOSAR_4-4-0.xsd">
    <AR-PACKAGES>
        <AR-PACKAGE>
            <SHORT-NAME>SamplePackage</SHORT-NAME>
            <ELEMENTS>
                <ECU-INSTANCE>
                    <SHORT-NAME>SampleECU</SHORT-NAME>
                    <LONG-NAME>Sample ECU Instance</LONG-NAME>
                </ECU-INSTANCE>
            </ELEMENTS>
        </AR-PACKAGE>
    </AR-PACKAGES>
</AUTOSAR>'''
        
        self.text_editor.delete(1.0, tk.END)
        self.text_editor.insert(1.0, sample_content)
        self.file_label.config(text="Sample ARXML loaded", foreground="blue")
    
    def open_file(self):
        """Open an ARXML file"""
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
                self.file_label.config(text=f"Loaded: {os.path.basename(file_path)}", foreground="green")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file: {str(e)}")
    
    def save_file(self):
        """Save the current content"""
        if self.current_file:
            self.save_to_file(self.current_file)
        else:
            self.save_as_file()
    
    def save_as_file(self):
        """Save as a new file"""
        file_path = filedialog.asksaveasfilename(
            title="Save ARXML File",
            defaultextension=".arxml",
            filetypes=[("ARXML files", "*.arxml"), ("XML files", "*.xml"), ("All files", "*.*")]
        )
        
        if file_path:
            self.save_to_file(file_path)
            self.current_file = file_path
            self.file_label.config(text=f"Saved: {os.path.basename(file_path)}", foreground="green")
    
    def save_to_file(self, file_path):
        """Save content to file"""
        try:
            content = self.text_editor.get(1.0, tk.END)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            messagebox.showinfo("Success", f"File saved successfully: {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")
    
    def validate_xml(self):
        """Validate XML syntax"""
        try:
            content = self.text_editor.get(1.0, tk.END)
            ET.fromstring(content)
            messagebox.showinfo("Validation", "XML is valid!")
        except ET.ParseError as e:
            messagebox.showerror("XML Error", f"Invalid XML: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Validation failed: {str(e)}")
    
    def format_xml(self):
        """Format XML content"""
        try:
            content = self.text_editor.get(1.0, tk.END)
            root = ET.fromstring(content)
            
            # Pretty print
            self.indent_xml(root)
            formatted = ET.tostring(root, encoding='unicode')
            
            self.text_editor.delete(1.0, tk.END)
            self.text_editor.insert(1.0, formatted)
            messagebox.showinfo("Format", "XML formatted successfully!")
            
        except ET.ParseError as e:
            messagebox.showerror("XML Error", f"Cannot format invalid XML: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Formatting failed: {str(e)}")
    
    def indent_xml(self, elem, level=0):
        """Add indentation to XML element"""
        i = "\\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for child in elem:
                self.indent_xml(child, level + 1)
            if not child.tail or not child.tail.strip():
                child.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
    
    def clear_text(self):
        """Clear the text editor"""
        self.text_editor.delete(1.0, tk.END)
        self.current_file = None
        self.file_label.config(text="No file loaded", foreground="gray")
    
    def show_about(self):
        """Show about dialog"""
        about_text = """ARXML Editor - Tkinter Version

A simple, reliable ARXML editor using Tkinter.

Features:
• Open and edit ARXML files
• XML validation
• XML formatting
• Simple, clean interface

Built with Python Tkinter for maximum compatibility."""
        
        messagebox.showinfo("About ARXML Editor", about_text)

def main():
    """Main function"""
    print("=" * 50)
    print("ARXML Editor - Tkinter Version")
    print("=" * 50)
    print("Starting Tkinter GUI...")
    
    try:
        # Create main window
        root = tk.Tk()
        
        # Create application
        app = ARXMLEditorTkinter(root)
        
        print("✓ GUI created successfully")
        print("✓ Ready to edit ARXML files")
        print("=" * 50)
        
        # Start GUI
        root.mainloop()
        
    except Exception as e:
        print(f"✗ Error starting GUI: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
'''

def create_tkinter_build_script():
    """Create a simple build script for Tkinter version"""
    return '''@echo off
echo ========================================
echo ARXML Editor - Tkinter Windows Build
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.6+ and try again.
    pause
    exit /b 1
)

echo Python found. Starting build...
echo.

echo Installing requirements...
python -m pip install --upgrade pip
python -m pip install pyinstaller lxml xmlschema

echo.
echo Building executable...
pyinstaller --onefile --windowed --name ARXMLEditor_Tkinter main_tkinter.py

if exist "dist\\ARXMLEditor_Tkinter.exe" (
    echo.
    echo ========================================
    echo BUILD SUCCESSFUL!
    echo ========================================
    echo Executable created: dist\\ARXMLEditor_Tkinter.exe
    echo.
    echo You can now run the executable!
    echo.
) else (
    echo.
    echo ========================================
    echo BUILD FAILED!
    echo ========================================
    echo Please check the error messages above.
    echo.
)

pause
'''

def create_tkinter_readme():
    """Create README for Tkinter version"""
    return '''# ARXML Editor - Tkinter Version

A simple, reliable ARXML editor using Python Tkinter.

## Features

- **Simple GUI**: Clean, easy-to-use interface
- **ARXML Support**: Open, edit, and save ARXML files
- **XML Validation**: Check XML syntax
- **XML Formatting**: Pretty-print XML content
- **Reliable**: Uses Tkinter (built into Python)
- **No Dependencies**: No complex GUI frameworks

## How to Build

1. **Run the build script**:
   ```
   BUILD_TKINTER.bat
   ```

2. **Find your executable**:
   - Look in the `dist` folder
   - Run `ARXMLEditor_Tkinter.exe`

## How to Use

1. **Open the executable**
2. **Load an ARXML file** using File → Open
3. **Edit the content** in the text editor
4. **Validate XML** using the Validate button
5. **Format XML** using the Format button
6. **Save your changes** using File → Save

## Advantages of Tkinter Version

- ✅ **No PyQt6 issues** - Tkinter is built into Python
- ✅ **Reliable builds** - No complex dependencies
- ✅ **Fast startup** - Lightweight GUI framework
- ✅ **Cross-platform** - Works on Windows, Mac, Linux
- ✅ **Simple maintenance** - Easy to debug and modify

## Troubleshooting

If you encounter any issues:

1. **Make sure Python is installed**
2. **Run the build script as Administrator** if needed
3. **Check that all files are in the same directory**

## Technical Details

- **GUI Framework**: Python Tkinter
- **XML Processing**: xml.etree.ElementTree
- **Build Tool**: PyInstaller
- **Python Version**: 3.6+
'''

def main():
    """Main function to create the Tkinter package"""
    print("=" * 60)
    print("ARXML Editor - Tkinter Windows Build Package Creator")
    print("=" * 60)
    print("Creating simple, reliable Tkinter-based Windows build...")
    
    # Create package directory
    package_dir = Path("ARXMLEditor-Windows-Tkinter")
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir()
    
    print("Copying source code...")
    
    # Copy source files
    source_files = [
        "arxml_editor",
        "examples", 
        "README.md",
        "arxml_editor.ico"
    ]
    
    for item in source_files:
        if Path(item).exists():
            if Path(item).is_dir():
                shutil.copytree(item, package_dir / item)
                print(f"  Copied {item}")
            else:
                shutil.copy2(item, package_dir / item)
                print(f"  Copied {item}")
    
    print("Creating Tkinter main script...")
    
    # Create main Tkinter script
    main_script = create_tkinter_main_script()
    with open(package_dir / "main_tkinter.py", "w", encoding="utf-8") as f:
        f.write(main_script)
    
    print("Creating build script...")
    
    # Create build script
    build_script = create_tkinter_build_script()
    with open(package_dir / "BUILD_TKINTER.bat", "w", encoding="utf-8") as f:
        f.write(build_script)
    
    print("Creating README...")
    
    # Create README
    readme_content = create_tkinter_readme()
    with open(package_dir / "README_TKINTER.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("Creating zip package...")
    
    # Create zip package
    zip_name = "ARXMLEditor-Windows-Tkinter-v1.0.0.zip"
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = Path(root) / file
                arc_path = file_path.relative_to(package_dir.parent)
                zipf.write(file_path, arc_path)
    
    print("=" * 60)
    print("TKINTER WINDOWS BUILD PACKAGE CREATED SUCCESSFULLY!")
    print("=" * 60)
    print(f"Package directory: {package_dir}")
    print(f"Zip package: {zip_name}")
    print()
    print("Next steps:")
    print("1. Transfer the zip file to a Windows machine")
    print("2. Extract the zip file")
    print("3. Run BUILD_TKINTER.bat")
    print("4. The resulting executable will be simple and reliable!")
    print("=" * 60)

if __name__ == "__main__":
    main()
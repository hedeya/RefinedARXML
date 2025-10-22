#!/usr/bin/env python3
"""
Demonstration script for ARXML Hierarchy Visualization.

This script shows how to use the hierarchy visualization feature.
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QLabel, QTextEdit
from PySide6.QtCore import Qt

from arxml_editor.core.arxml_model import ARXMLModel
from arxml_editor.ui.hierarchy_view import HierarchyViewWidget


class HierarchyDemoWindow(QMainWindow):
    """Demo window for hierarchy visualization."""
    
    def __init__(self):
        super().__init__()
        self.arxml_model = ARXMLModel()
        self.hierarchy_view = HierarchyViewWidget(self.arxml_model)
        
        self._setup_ui()
        self._load_demo_data()
    
    def _setup_ui(self):
        """Set up the UI."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Title
        title_label = QLabel("ARXML Hierarchy Visualization Demo")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(title_label)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        load_button = QPushButton("Load Demo ARXML")
        load_button.clicked.connect(self._load_demo_data)
        button_layout.addWidget(load_button)
        
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self._clear_data)
        button_layout.addWidget(clear_button)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Hierarchy view
        layout.addWidget(self.hierarchy_view)
        
        # Status text
        self.status_text = QTextEdit()
        self.status_text.setMaximumHeight(100)
        self.status_text.setPlainText("Ready to load ARXML file...")
        layout.addWidget(self.status_text)
        
        # Connect signals
        self.hierarchy_view.element_selected.connect(self._on_element_selected)
        
        self.setWindowTitle("ARXML Hierarchy Visualization Demo")
        self.setGeometry(100, 100, 1400, 900)
    
    def _load_demo_data(self):
        """Load demo ARXML data."""
        demo_file = project_root / "examples" / "hierarchy_sample.arxml"
        
        if not demo_file.exists():
            self.status_text.setPlainText(f"Demo file not found: {demo_file}")
            return
        
        if self.arxml_model.load_file(demo_file):
            # Set the root element for hierarchy view
            root_path = "/AUTOSAR/AR-PACKAGES/AR-PACKAGE[1]"
            self.hierarchy_view.set_element(root_path)
            self.status_text.setPlainText(f"Loaded demo ARXML file: {demo_file.name}\nRoot element: {root_path}")
        else:
            self.status_text.setPlainText("Failed to load demo ARXML file")
    
    def _clear_data(self):
        """Clear the loaded data."""
        self.arxml_model = ARXMLModel()
        self.hierarchy_view = HierarchyViewWidget(self.arxml_model)
        
        # Recreate the UI
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Title
        title_label = QLabel("ARXML Hierarchy Visualization Demo")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(title_label)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        load_button = QPushButton("Load Demo ARXML")
        load_button.clicked.connect(self._load_demo_data)
        button_layout.addWidget(load_button)
        
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self._clear_data)
        button_layout.addWidget(clear_button)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Hierarchy view
        layout.addWidget(self.hierarchy_view)
        
        # Status text
        self.status_text = QTextEdit()
        self.status_text.setMaximumHeight(100)
        self.status_text.setPlainText("Data cleared. Ready to load ARXML file...")
        layout.addWidget(self.status_text)
        
        # Connect signals
        self.hierarchy_view.element_selected.connect(self._on_element_selected)
        
        self.status_text.setPlainText("Data cleared. Ready to load ARXML file...")
    
    def _on_element_selected(self, path: str):
        """Handle element selection."""
        element = self.arxml_model.get_element_by_path(path)
        if element:
            info = f"Selected: {path}\n"
            info += f"Name: {element.short_name}\n"
            info += f"Type: {element.element_type}\n"
            info += f"UUID: {element.uuid or 'N/A'}\n"
            info += f"Parent: {element.parent_path or 'Root'}"
            self.status_text.setPlainText(info)
        else:
            self.status_text.setPlainText(f"Element not found: {path}")


def main():
    """Main function."""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("ARXML Hierarchy Demo")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("ARXML Editor")
    
    # Create and show window
    window = HierarchyDemoWindow()
    window.show()
    
    # Run the application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
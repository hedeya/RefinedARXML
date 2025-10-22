#!/usr/bin/env python3
"""
Test script for diagram view toggle functionality.

This script tests the toggle functionality for hiding/showing the diagram view.
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QLabel
from PySide6.QtCore import Qt

from arxml_editor.core.arxml_model import ARXMLModel
from arxml_editor.ui.main_window import MainWindow


class DiagramToggleTestWindow(QMainWindow):
    """Test window for diagram toggle functionality."""
    
    def __init__(self):
        super().__init__()
        self.main_window = MainWindow()
        self.main_window.show()
        
        # Create a simple test interface
        self._setup_test_ui()
    
    def _setup_test_ui(self):
        """Set up test UI."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Title
        title_label = QLabel("Diagram View Toggle Test")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(title_label)
        
        # Instructions
        instructions = QLabel("""
Instructions:
1. The main ARXML Editor window should be visible
2. The Diagram View should be hidden by default
3. Use the 'Diagram View' button in the toolbar or View menu to toggle it
4. Both the menu and toolbar buttons should stay synchronized
5. Load an ARXML file to test the functionality with actual data
        """)
        instructions.setStyleSheet("margin: 10px; padding: 10px; background-color: #f0f0f0;")
        layout.addWidget(instructions)
        
        # Test buttons
        button_layout = QHBoxLayout()
        
        load_sample_button = QPushButton("Load Sample ARXML")
        load_sample_button.clicked.connect(self._load_sample_arxml)
        button_layout.addWidget(load_sample_button)
        
        toggle_diagram_button = QPushButton("Toggle Diagram View (Programmatic)")
        toggle_diagram_button.clicked.connect(self._toggle_diagram_programmatically)
        button_layout.addWidget(toggle_diagram_button)
        
        check_status_button = QPushButton("Check Diagram Status")
        check_status_button.clicked.connect(self._check_diagram_status)
        button_layout.addWidget(check_status_button)
        
        layout.addLayout(button_layout)
        
        # Status display
        self.status_label = QLabel("Ready to test diagram toggle functionality...")
        self.status_label.setStyleSheet("margin: 10px; padding: 10px; background-color: #e0e0e0;")
        layout.addWidget(self.status_label)
        
        self.setWindowTitle("Diagram Toggle Test")
        self.setGeometry(50, 50, 600, 400)
    
    def _load_sample_arxml(self):
        """Load sample ARXML file."""
        sample_file = project_root / "examples" / "hierarchy_sample.arxml"
        
        if sample_file.exists():
            if self.main_window.arxml_model.load_file(sample_file):
                self.status_label.setText(f"✓ Loaded sample ARXML: {sample_file.name}")
            else:
                self.status_label.setText("✗ Failed to load sample ARXML")
        else:
            self.status_label.setText(f"✗ Sample file not found: {sample_file}")
    
    def _toggle_diagram_programmatically(self):
        """Toggle diagram view programmatically."""
        self.main_window._toggle_diagram_view()
        self._check_diagram_status()
    
    def _check_diagram_status(self):
        """Check and display diagram view status."""
        is_visible = self.main_window.diagram_dock.isVisible()
        menu_checked = self.main_window.diagram_toggle_action.isChecked()
        toolbar_checked = self.main_window.diagram_toolbar_action.isChecked()
        
        status = f"""
Diagram View Status:
- Visible: {'Yes' if is_visible else 'No'}
- Menu Checked: {'Yes' if menu_checked else 'No'}
- Toolbar Checked: {'Yes' if toolbar_checked else 'No'}
- Synchronized: {'Yes' if menu_checked == toolbar_checked else 'No'}
        """
        
        self.status_label.setText(status)


def main():
    """Main function."""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Diagram Toggle Test")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("ARXML Editor")
    
    # Create and show test window
    test_window = DiagramToggleTestWindow()
    test_window.show()
    
    # Run the application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Test script for the hierarchy view widget.

This script demonstrates the hierarchy visualization functionality.
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt

from arxml_editor.core.arxml_model import ARXMLModel
from arxml_editor.ui.hierarchy_view import HierarchyViewWidget


class TestWindow(QMainWindow):
    """Test window for hierarchy view."""
    
    def __init__(self):
        super().__init__()
        self.arxml_model = ARXMLModel()
        self.hierarchy_view = HierarchyViewWidget(self.arxml_model)
        
        self._setup_ui()
        self._load_sample_data()
    
    def _setup_ui(self):
        """Set up the UI."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        load_button = QPushButton("Load Sample ARXML")
        load_button.clicked.connect(self._load_sample_data)
        button_layout.addWidget(load_button)
        
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self._clear_data)
        button_layout.addWidget(clear_button)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Hierarchy view
        layout.addWidget(self.hierarchy_view)
        
        # Connect signals
        self.hierarchy_view.element_selected.connect(self._on_element_selected)
        
        self.setWindowTitle("ARXML Hierarchy View Test")
        self.setGeometry(100, 100, 1200, 800)
    
    def _load_sample_data(self):
        """Load sample ARXML data for testing."""
        # Create a sample ARXML structure
        sample_arxml = '''<?xml version="1.0" encoding="UTF-8"?>
<AUTOSAR xmlns="http://autosar.org/schema/r4.2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://autosar.org/schema/r4.2 AUTOSAR_4-2-0.xsd">
  <AR-PACKAGES>
    <AR-PACKAGE>
      <SHORT-NAME>TestPackage</SHORT-NAME>
      <LONG-NAME>Test Package for Hierarchy Visualization</LONG-NAME>
      <ELEMENTS>
        <ELEMENT>
          <SHORT-NAME>EngineControl</SHORT-NAME>
          <LONG-NAME>Engine Control Software Component</LONG-NAME>
          <ELEMENTS>
            <CONTAINER>
              <SHORT-NAME>EngineParams</SHORT-NAME>
              <LONG-NAME>Engine Parameters</LONG-NAME>
              <ELEMENTS>
                <PARAMETER>
                  <SHORT-NAME>MaxRPM</SHORT-NAME>
                  <LONG-NAME>Maximum RPM</LONG-NAME>
                  <VALUE>6000</VALUE>
                </PARAMETER>
                <PARAMETER>
                  <SHORT-NAME>IdleRPM</SHORT-NAME>
                  <LONG-NAME>Idle RPM</LONG-NAME>
                  <VALUE>800</VALUE>
                </PARAMETER>
              </ELEMENTS>
            </CONTAINER>
            <CONTAINER>
              <SHORT-NAME>EngineSensors</SHORT-NAME>
              <LONG-NAME>Engine Sensors</LONG-NAME>
              <ELEMENTS>
                <ELEMENT>
                  <SHORT-NAME>TemperatureSensor</SHORT-NAME>
                  <LONG-NAME>Temperature Sensor</LONG-NAME>
                </ELEMENT>
                <ELEMENT>
                  <SHORT-NAME>PressureSensor</SHORT-NAME>
                  <LONG-NAME>Pressure Sensor</LONG-NAME>
                </ELEMENT>
              </ELEMENTS>
            </CONTAINER>
          </ELEMENTS>
        </ELEMENT>
        <ELEMENT>
          <SHORT-NAME>TransmissionControl</SHORT-NAME>
          <LONG-NAME>Transmission Control Software Component</LONG-NAME>
          <ELEMENTS>
            <CONTAINER>
              <SHORT-NAME>GearParams</SHORT-NAME>
              <LONG-NAME>Gear Parameters</LONG-NAME>
              <ELEMENTS>
                <PARAMETER>
                  <SHORT-NAME>MaxGear</SHORT-NAME>
                  <LONG-NAME>Maximum Gear</LONG-NAME>
                  <VALUE>6</VALUE>
                </PARAMETER>
              </ELEMENTS>
            </CONTAINER>
          </ELEMENTS>
        </ELEMENT>
      </ELEMENTS>
    </AR-PACKAGE>
  </AR-PACKAGES>
</AUTOSAR>'''
        
        # Write sample file
        sample_file = project_root / "test_sample.arxml"
        with open(sample_file, 'w', encoding='utf-8') as f:
            f.write(sample_arxml)
        
        # Load the file
        if self.arxml_model.load_file(sample_file):
            # Set the root element for hierarchy view
            root_path = "/AUTOSAR/AR-PACKAGES/AR-PACKAGE[1]"
            self.hierarchy_view.set_element(root_path)
            print(f"Loaded sample ARXML file: {sample_file}")
        else:
            print("Failed to load sample ARXML file")
    
    def _clear_data(self):
        """Clear the loaded data."""
        self.arxml_model = ARXMLModel()
        self.hierarchy_view = HierarchyViewWidget(self.arxml_model)
        
        # Recreate the UI
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        load_button = QPushButton("Load Sample ARXML")
        load_button.clicked.connect(self._load_sample_data)
        button_layout.addWidget(load_button)
        
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self._clear_data)
        button_layout.addWidget(clear_button)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Hierarchy view
        layout.addWidget(self.hierarchy_view)
        
        # Connect signals
        self.hierarchy_view.element_selected.connect(self._on_element_selected)
        
        print("Cleared data")
    
    def _on_element_selected(self, path: str):
        """Handle element selection."""
        print(f"Selected element: {path}")


def main():
    """Main function."""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("ARXML Hierarchy View Test")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("ARXML Editor")
    
    # Create and show window
    window = TestWindow()
    window.show()
    
    # Run the application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
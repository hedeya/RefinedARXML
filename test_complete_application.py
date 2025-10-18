#!/usr/bin/env python3
"""
Complete application test for ARXML Editor.

This script tests the full application functionality including UI components,
model operations, validation, and serialization.
"""

import sys
import tempfile
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from arxml_editor.core.arxml_model import ARXMLModel
from arxml_editor.core.schema_manager import AUTOSARRelease
from arxml_editor.validation.validator import ARXMLValidator
from arxml_editor.serialization.arxml_serializer import ARXMLSerializer
from arxml_editor.ui.main_window import MainWindow


def test_core_functionality():
    """Test core ARXML model functionality."""
    print("Testing core functionality...")
    
    # Create model
    model = ARXMLModel()
    assert model is not None
    print("✓ Model creation successful")
    
    # Test schema detection
    sample_content = '''<?xml version="1.0" encoding="UTF-8"?>
<AUTOSAR xmlns="http://autosar.org/schema/r4.2">
  <AR-PACKAGES>
    <AR-PACKAGE>
      <SHORT-NAME>TestPackage</SHORT-NAME>
      <ELEMENTS>
        <ELEMENT>
          <SHORT-NAME>TestElement</SHORT-NAME>
        </ELEMENT>
      </ELEMENTS>
    </AR-PACKAGE>
  </AR-PACKAGES>
</AUTOSAR>'''
    
    detected_release = model.schema_manager.detect_schema_version(sample_content)
    assert detected_release == AUTOSARRelease.R22_11
    print("✓ Schema detection successful")
    
    # Test file loading
    with tempfile.NamedTemporaryFile(mode='w', suffix='.arxml', delete=False) as f:
        f.write(sample_content)
        temp_path = Path(f.name)
    
    try:
        success = model.load_file(temp_path)
        assert success
        print("✓ File loading successful")
        
        # Test element indexing
        stats = model.element_index.get_statistics()
        assert stats["total_elements"] > 0
        print("✓ Element indexing successful")
        
        # Test element creation
        new_path = model.create_element("/TestPackage", "ELEMENT", "NewElement")
        assert new_path is not None
        print("✓ Element creation successful")
        
        # Test validation
        errors = model.get_validation_errors()
        print(f"✓ Validation completed with {len(errors)} issues")
        
    finally:
        temp_path.unlink()


def test_validation_system():
    """Test validation system."""
    print("\nTesting validation system...")
    
    model = ARXMLModel()
    
    # Create a file with validation issues
    invalid_content = '''<?xml version="1.0" encoding="UTF-8"?>
<AUTOSAR xmlns="http://autosar.org/schema/r4.2">
  <AR-PACKAGES>
    <AR-PACKAGE>
      <SHORT-NAME>TestPackage</SHORT-NAME>
      <ELEMENTS>
        <ELEMENT>
          <!-- Missing SHORT-NAME -->
        </ELEMENT>
      </ELEMENTS>
    </AR-PACKAGE>
  </AR-PACKAGES>
</AUTOSAR>'''
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.arxml', delete=False) as f:
        f.write(invalid_content)
        temp_path = Path(f.name)
    
    try:
        model.load_file(temp_path)
        
        # Test validator
        validator = ARXMLValidator(
            model.schema_manager,
            model.element_index,
            model.reference_manager
        )
        
        errors = validator.validate_all()
        assert len(errors) > 0
        print("✓ Validation system working")
        
        # Test error levels
        error_count = len([e for e in errors if e.level.value == "error"])
        warning_count = len([e for e in errors if e.level.value == "warning"])
        print(f"✓ Found {error_count} errors, {warning_count} warnings")
        
    finally:
        temp_path.unlink()


def test_serialization():
    """Test serialization system."""
    print("\nTesting serialization system...")
    
    # Create sample element
    import xml.etree.ElementTree as ET
    
    root = ET.Element("AUTOSAR")
    root.set("xmlns", "http://autosar.org/schema/r4.2")
    
    ar_packages = ET.SubElement(root, "AR-PACKAGES")
    ar_package = ET.SubElement(ar_packages, "AR-PACKAGE")
    
    short_name = ET.SubElement(ar_package, "SHORT-NAME")
    short_name.text = "TestPackage"
    
    # Test serializer
    serializer = ARXMLSerializer(AUTOSARRelease.R22_11)
    
    # Test deterministic serialization
    options = serializer._get_serialization_rules()
    assert "namespace" in options
    print("✓ Serialization rules loaded")
    
    # Test element serialization
    serialized = serializer.serialize_element(ar_package)
    assert "TestPackage" in serialized
    print("✓ Element serialization successful")
    
    # Test document serialization
    doc = serializer.serialize_document(root)
    assert "<?xml version=" in doc
    assert "<AUTOSAR" in doc
    print("✓ Document serialization successful")


def test_ui_components():
    """Test UI components (without showing windows)."""
    print("\nTesting UI components...")
    
    # Create QApplication (required for Qt widgets)
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    try:
        # Test main window creation
        model = ARXMLModel()
        main_window = MainWindow()
        assert main_window is not None
        print("✓ Main window creation successful")
        
        # Test package tree
        package_tree = main_window.package_tree
        assert package_tree is not None
        print("✓ Package tree creation successful")
        
        # Test property editor
        property_editor = main_window.property_editor
        assert property_editor is not None
        print("✓ Property editor creation successful")
        
        # Test diagram view
        diagram_view = main_window.diagram_view
        assert diagram_view is not None
        print("✓ Diagram view creation successful")
        
        # Test validation panel
        validation_panel = main_window.validation_panel
        assert validation_panel is not None
        print("✓ Validation panel creation successful")
        
    except Exception as e:
        print(f"✗ UI component test failed: {e}")
        raise


def test_naming_conventions():
    """Test naming convention conversions."""
    print("\nTesting naming conventions...")
    
    from arxml_editor.utils.naming_conventions import ARXMLNamingConventions
    
    naming = ARXMLNamingConventions()
    
    # Test camelCase to UPPERCASE-HYPHENATED
    result = naming.camel_case_to_uppercase_hyphenated("shortName")
    assert result == "SHORT-NAME"
    print("✓ CamelCase to UPPERCASE-HYPHENATED conversion")
    
    # Test UPPERCASE-HYPHENATED to camelCase
    result = naming.uppercase_hyphenated_to_camel_case("SHORT-NAME")
    assert result == "shortName"
    print("✓ UPPERCASE-HYPHENATED to camelCase conversion")
    
    # Test validation
    is_valid, error = naming.validate_short_name("ValidName123")
    assert is_valid
    print("✓ SHORT-NAME validation")
    
    is_valid, error = naming.validate_attribute_name("camelCase")
    assert is_valid
    print("✓ Attribute name validation")


def test_path_utilities():
    """Test path utility functions."""
    print("\nTesting path utilities...")
    
    from arxml_editor.utils.path_utils import PathUtils
    
    # Test path building
    path = PathUtils.build_autosar_path(["Package1", "Element1"])
    assert path == "/Package1/Element1"
    print("✓ Path building")
    
    # Test path parsing
    parts = PathUtils.parse_autosar_path("/Package1/Element1")
    assert parts == ["Package1", "Element1"]
    print("✓ Path parsing")
    
    # Test reference resolution
    resolved = PathUtils.resolve_reference("Element1", "/Package1")
    assert resolved == "/Package1/Element1"
    print("✓ Reference resolution")
    
    # Test path validation
    is_valid, error = PathUtils.validate_arxml_path("/Valid/Path")
    assert is_valid
    print("✓ Path validation")


def run_comprehensive_test():
    """Run comprehensive application test."""
    print("=" * 60)
    print("ARXML Editor - Comprehensive Application Test")
    print("=" * 60)
    
    try:
        test_core_functionality()
        test_validation_system()
        test_serialization()
        test_ui_components()
        test_naming_conventions()
        test_path_utilities()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("ARXML Editor is ready for use.")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)
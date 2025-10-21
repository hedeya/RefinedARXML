"""
Tests for ARXML model functionality.
"""

import tempfile
from pathlib import Path
from arxml_editor.core.arxml_model import ARXMLModel
from arxml_editor.core.schema_manager import AUTOSARRelease


class TestARXMLModel:
    """Test cases for ARXMLModel."""
    
    def test_model_creation(self):
        """Test creating a new ARXML model."""
        model = ARXMLModel()
        assert model is not None
        assert not model.is_modified
        assert model.current_file is None
    
    def test_load_sample_file(self):
        """Test loading a sample ARXML file."""
        model = ARXMLModel()
        
        # Create a temporary ARXML file
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
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.arxml', delete=False) as f:
            f.write(sample_content)
            temp_path = Path(f.name)
        
        try:
            success = model.load_file(temp_path)
            assert success
            assert model.current_file == temp_path
            assert len(model.files) == 1
        finally:
            temp_path.unlink()
    
    def test_element_indexing(self):
        """Test element indexing functionality."""
        model = ARXMLModel()
        
        # Create and load a sample file
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
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.arxml', delete=False) as f:
            f.write(sample_content)
            temp_path = Path(f.name)
        
        try:
            model.load_file(temp_path)
            
            # Check that elements are indexed
            stats = model.element_index.get_statistics()
            assert stats["total_elements"] > 0
            
            # Test element lookup
            element = model.get_element_by_path("/TestPackage")
            assert element is not None
            assert element.short_name == "TestPackage"
            
        finally:
            temp_path.unlink()
    
    def test_schema_detection(self):
        """Test schema version detection."""
        model = ARXMLModel()
        
        # Test R22.11 detection
        r22_content = '''<?xml version="1.0" encoding="UTF-8"?>
<AUTOSAR xmlns="http://autosar.org/schema/r4.2">
  <AR-PACKAGES></AR-PACKAGES>
</AUTOSAR>'''
        
        detected_release = model.schema_manager.detect_schema_version(r22_content)
        assert detected_release == AUTOSARRelease.R22_11
    
    def test_validation(self):
        """Test validation functionality."""
        model = ARXMLModel()
        
        # Create a file with validation errors
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
            
            # Run validation
            errors = model.get_validation_errors()
            assert len(errors) > 0  # Should have validation errors
            
        finally:
            temp_path.unlink()
    
    def test_element_creation(self):
        """Test creating new elements."""
        model = ARXMLModel()
        
        # Create a basic model
        sample_content = '''<?xml version="1.0" encoding="UTF-8"?>
<AUTOSAR xmlns="http://autosar.org/schema/r4.2">
  <AR-PACKAGES>
    <AR-PACKAGE>
      <SHORT-NAME>TestPackage</SHORT-NAME>
      <ELEMENTS></ELEMENTS>
    </AR-PACKAGE>
  </AR-PACKAGES>
</AUTOSAR>'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.arxml', delete=False) as f:
            f.write(sample_content)
            temp_path = Path(f.name)
        
        try:
            model.load_file(temp_path)
            
            # Create a new element
            new_path = model.create_element("/TestPackage", "ELEMENT", "NewElement")
            assert new_path is not None
            assert new_path == "/TestPackage/NewElement"
            
            # Check that element was created
            element = model.get_element_by_path(new_path)
            assert element is not None
            assert element.short_name == "NewElement"
            
        finally:
            temp_path.unlink()
    
    def test_element_deletion(self):
        """Test deleting elements."""
        model = ARXMLModel()
        
        # Create a model with elements
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
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.arxml', delete=False) as f:
            f.write(sample_content)
            temp_path = Path(f.name)
        
        try:
            model.load_file(temp_path)
            
            # Delete an element
            success = model.delete_element("/TestPackage/TestElement")
            assert success
            
            # Check that element was deleted
            element = model.get_element_by_path("/TestPackage/TestElement")
            assert element is None
            
        finally:
            temp_path.unlink()
    
    def test_search_functionality(self):
        """Test element search functionality."""
        model = ARXMLModel()
        
        # Create a model with searchable elements
        sample_content = '''<?xml version="1.0" encoding="UTF-8"?>
<AUTOSAR xmlns="http://autosar.org/schema/r4.2">
  <AR-PACKAGES>
    <AR-PACKAGE>
      <SHORT-NAME>TestPackage</SHORT-NAME>
      <ELEMENTS>
        <ELEMENT>
          <SHORT-NAME>TestElement</SHORT-NAME>
        </ELEMENT>
        <ELEMENT>
          <SHORT-NAME>AnotherElement</SHORT-NAME>
        </ELEMENT>
      </ELEMENTS>
    </AR-PACKAGE>
  </AR-PACKAGES>
</AUTOSAR>'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.arxml', delete=False) as f:
            f.write(sample_content)
            temp_path = Path(f.name)
        
        try:
            model.load_file(temp_path)
            
            # Search for elements
            results = model.search_elements("Test")
            assert len(results) > 0
            
            # Search by type
            element_results = model.search_elements("", "ELEMENT")
            assert len(element_results) == 2
            
        finally:
            temp_path.unlink()


if __name__ == "__main__":
    # Simple test runner
    test_instance = TestARXMLModel()
    test_methods = [method for method in dir(test_instance) if method.startswith('test_')]
    
    passed = 0
    failed = 0
    
    print(f"Running {len(test_methods)} tests...")
    print("=" * 50)
    
    for test_method in test_methods:
        print(f"Running {test_method}...", end=" ")
        try:
            getattr(test_instance, test_method)()
            print("PASSED")
            passed += 1
        except Exception as e:
            print(f"FAILED: {e}")
            failed += 1
    
    print("=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
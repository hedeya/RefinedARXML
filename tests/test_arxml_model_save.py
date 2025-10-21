"""
Tests for ARXML model save and save-as functionality.
"""

import tempfile
import os
from pathlib import Path
from arxml_editor.core.arxml_model import ARXMLModel
from arxml_editor.core.schema_manager import AUTOSARRelease


class TestARXMLModelSave:
    """Test cases for ARXMLModel save and save-as functionality."""
    
    def test_save_file_basic(self):
        """Test basic save functionality."""
        model = ARXMLModel()
        
        # Create a sample ARXML file
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
            # Load the file
            success = model.load_file(temp_path)
            assert success
            assert model.current_file == temp_path
            
            # Create a new file to save to
            with tempfile.NamedTemporaryFile(mode='w', suffix='.arxml', delete=False) as f:
                save_path = Path(f.name)
            
            try:
                # Save to new file
                success = model.save_file(save_path)
                assert success
                
                # Verify the file was created and has content
                assert save_path.exists()
                with open(save_path, 'r', encoding='utf-8') as f:
                    saved_content = f.read()
                assert 'TestPackage' in saved_content
                assert 'TestElement' in saved_content
                
                # Verify current_file was updated
                assert model.current_file == save_path
                
            finally:
                if save_path.exists():
                    save_path.unlink()
                    
        finally:
            if temp_path.exists():
                temp_path.unlink()
    
    def test_save_as_functionality(self):
        """Test save-as functionality (saving to a different file)."""
        model = ARXMLModel()
        
        # Create a sample ARXML file
        sample_content = '''<?xml version="1.0" encoding="UTF-8"?>
<AUTOSAR xmlns="http://autosar.org/schema/r4.2">
  <AR-PACKAGES>
    <AR-PACKAGE>
      <SHORT-NAME>OriginalPackage</SHORT-NAME>
      <ELEMENTS>
        <ELEMENT>
          <SHORT-NAME>OriginalElement</SHORT-NAME>
        </ELEMENT>
      </ELEMENTS>
    </AR-PACKAGE>
  </AR-PACKAGES>
</AUTOSAR>'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.arxml', delete=False) as f:
            f.write(sample_content)
            original_path = Path(f.name)
        
        try:
            # Load the original file
            success = model.load_file(original_path)
            assert success
            assert model.current_file == original_path
            
            # Create a new file for save-as
            with tempfile.NamedTemporaryFile(mode='w', suffix='.arxml', delete=False) as f:
                save_as_path = Path(f.name)
            
            try:
                # Perform save-as operation
                success = model.save_file(save_as_path)
                assert success
                
                # Verify the new file was created
                assert save_as_path.exists()
                with open(save_as_path, 'r', encoding='utf-8') as f:
                    saved_content = f.read()
                assert 'OriginalPackage' in saved_content
                assert 'OriginalElement' in saved_content
                
                # Verify current_file was updated to the new path
                assert model.current_file == save_as_path
                
                # Verify the original file still exists (save-as doesn't delete original)
                assert original_path.exists()
                
            finally:
                if save_as_path.exists():
                    save_as_path.unlink()
                    
        finally:
            if original_path.exists():
                original_path.unlink()
    
    def test_save_with_modifications(self):
        """Test saving a file after making modifications."""
        model = ARXMLModel()
        
        # Create a sample ARXML file
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
            # Load the file
            success = model.load_file(temp_path)
            assert success
            
            # Make a modification
            new_path = model.create_element("/TestPackage", "ELEMENT", "NewElement")
            assert new_path is not None
            assert model.is_modified
            
            # Save the modified file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.arxml', delete=False) as f:
                save_path = Path(f.name)
            
            try:
                success = model.save_file(save_path)
                assert success
                
                # Verify the modification was saved
                with open(save_path, 'r', encoding='utf-8') as f:
                    saved_content = f.read()
                assert 'NewElement' in saved_content
                assert 'TestElement' in saved_content  # Original element should still be there
                
                # Verify modification flag was cleared
                assert not model.is_modified
                
            finally:
                if save_path.exists():
                    save_path.unlink()
                    
        finally:
            if temp_path.exists():
                temp_path.unlink()
    
    def test_save_with_different_schema(self):
        """Test saving with a different schema version."""
        model = ARXMLModel()
        
        # Create a sample ARXML file
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
            # Load the file
            success = model.load_file(temp_path)
            assert success
            
            # Save with a different schema version
            with tempfile.NamedTemporaryFile(mode='w', suffix='.arxml', delete=False) as f:
                save_path = Path(f.name)
            
            try:
                success = model.save_file(save_path, AUTOSARRelease.R22_11)
                assert success
                
                # Verify the file was saved
                assert save_path.exists()
                with open(save_path, 'r', encoding='utf-8') as f:
                    saved_content = f.read()
                assert 'TestPackage' in saved_content
                
                # Verify the schema version was updated in the model
                assert model.files[save_path].schema_version == AUTOSARRelease.R22_11
                
            finally:
                if save_path.exists():
                    save_path.unlink()
                    
        finally:
            if temp_path.exists():
                temp_path.unlink()
    
    def test_save_nonexistent_file(self):
        """Test saving when no file is loaded."""
        model = ARXMLModel()
        
        # Try to save without loading a file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.arxml', delete=False) as f:
            save_path = Path(f.name)
        
        try:
            success = model.save_file(save_path)
            assert not success  # Should fail because no file is loaded
            
        finally:
            if save_path.exists():
                save_path.unlink()
    
    def test_save_to_same_file(self):
        """Test saving to the same file (overwrite)."""
        model = ARXMLModel()
        
        # Create a sample ARXML file
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
            # Load the file
            success = model.load_file(temp_path)
            assert success
            
            # Make a modification
            new_path = model.create_element("/TestPackage", "ELEMENT", "NewElement")
            assert new_path is not None
            
            # Save to the same file (overwrite)
            success = model.save_file(temp_path)
            assert success
            
            # Verify the file was updated
            with open(temp_path, 'r', encoding='utf-8') as f:
                updated_content = f.read()
            assert 'NewElement' in updated_content
            assert 'TestElement' in updated_content
            
            # Verify modification flag was cleared
            assert not model.is_modified
            
        finally:
            if temp_path.exists():
                temp_path.unlink()
    
    def test_save_error_handling(self):
        """Test save error handling with invalid paths."""
        model = ARXMLModel()
        
        # Create a sample ARXML file
        sample_content = '''<?xml version="1.0" encoding="UTF-8"?>
<AUTOSAR xmlns="http://autosar.org/schema/r4.2">
  <AR-PACKAGES>
    <AR-PACKAGE>
      <SHORT-NAME>TestPackage</SHORT-NAME>
    </AR-PACKAGE>
  </AR-PACKAGES>
</AUTOSAR>'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.arxml', delete=False) as f:
            f.write(sample_content)
            temp_path = Path(f.name)
        
        try:
            # Load the file
            success = model.load_file(temp_path)
            assert success
            
            # Try to save to an invalid path (directory that doesn't exist)
            invalid_path = Path("/nonexistent/directory/file.arxml")
            success = model.save_file(invalid_path)
            assert not success  # Should fail due to invalid path
            
        finally:
            if temp_path.exists():
                temp_path.unlink()
    
    def test_save_file_metadata_preservation(self):
        """Test that file metadata is preserved during save operations."""
        model = ARXMLModel()
        
        # Create a sample ARXML file
        sample_content = '''<?xml version="1.0" encoding="UTF-8"?>
<AUTOSAR xmlns="http://autosar.org/schema/r4.2">
  <AR-PACKAGES>
    <AR-PACKAGE>
      <SHORT-NAME>TestPackage</SHORT-NAME>
    </AR-PACKAGE>
  </AR-PACKAGES>
</AUTOSAR>'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.arxml', delete=False) as f:
            f.write(sample_content)
            temp_path = Path(f.name)
        
        try:
            # Load the file
            success = model.load_file(temp_path)
            assert success
            
            # Get original file metadata
            original_file = model.files[temp_path]
            original_schema = original_file.schema_version
            original_size = original_file.file_size
            
            # Save to a new file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.arxml', delete=False) as f:
                save_path = Path(f.name)
            
            try:
                success = model.save_file(save_path)
                assert success
                
                # Verify metadata was preserved/updated correctly
                saved_file = model.files[save_path]
                assert saved_file.schema_version == original_schema
                assert saved_file.file_size > 0
                assert not saved_file.is_modified
                
            finally:
                if save_path.exists():
                    save_path.unlink()
                    
        finally:
            if temp_path.exists():
                temp_path.unlink()


if __name__ == "__main__":
    # Simple test runner
    test_instance = TestARXMLModelSave()
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
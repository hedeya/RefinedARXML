"""
Core ARXML model for loading, editing, and saving ARXML files.

Provides the main interface for ARXML manipulation with proper schema handling
and cross-reference management.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Union
import xml.etree.ElementTree as ET
from dataclasses import dataclass

from .schema_manager import SchemaManager, AUTOSARRelease
from .element_index import ElementIndex, ElementInfo
from .reference_manager import ReferenceManager
from ..utils.xml_utils import XMLUtils
from ..utils.path_utils import PathUtils
from ..utils.naming_conventions import ARXMLNamingConventions


@dataclass
class ARXMLFile:
    """Represents an ARXML file with metadata."""
    path: Path
    content: str
    root_element: ET.Element
    schema_version: Optional[AUTOSARRelease]
    is_modified: bool = False
    file_size: int = 0


class ARXMLModel:
    """Main ARXML model for file management and editing."""
    
    def __init__(self, schema_dir: Optional[Path] = None):
        self.schema_manager = SchemaManager(schema_dir)
        self.element_index = ElementIndex()
        self.reference_manager = ReferenceManager(self.element_index)
        self.naming_conventions = ARXMLNamingConventions()
        
        self.files: Dict[Path, ARXMLFile] = {}
        self.current_file: Optional[Path] = None
        self.is_modified = False
        
        # Performance optimization
        self._lazy_loading = True
        self._loaded_packages: Set[str] = set()
    
    def load_file(self, file_path: Union[str, Path]) -> bool:
        """Load an ARXML file into the model."""
        file_path = Path(file_path)
        
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse XML
            root_element = ET.fromstring(content)
            
            # Detect schema version
            schema_version = self.schema_manager.detect_schema_version(content)
            
            # Create file object
            arxml_file = ARXMLFile(
                path=file_path,
                content=content,
                root_element=root_element,
                schema_version=schema_version,
                file_size=len(content)
            )
            
            # Store file
            self.files[file_path] = arxml_file
            self.current_file = file_path
            
            # Index elements
            self._index_file(arxml_file)
            
            # Analyze references
            self.reference_manager.analyze_references()
            
            return True
            
        except Exception as e:
            print(f"Error loading file {file_path}: {e}")
            return False
    
    def save_file(self, file_path: Optional[Path] = None, target_schema: Optional[AUTOSARRelease] = None) -> bool:
        """Save current model to file."""
        if not self.current_file and not file_path:
            return False
        
        target_file = file_path or self.current_file
        if not target_file:
            return False
        
        try:
            # Get target schema
            if target_schema:
                schema_version = target_schema
            else:
                schema_version = self.files[target_file].schema_version
            
            if not schema_version:
                schema_version = AUTOSARRelease.R22_11  # Default
            
            # Serialize content
            content = self._serialize_file(target_file, schema_version)
            
            # Write to file
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Update file metadata
            if target_file in self.files:
                self.files[target_file].content = content
                self.files[target_file].is_modified = False
                self.files[target_file].schema_version = schema_version
            
            self.is_modified = False
            return True
            
        except Exception as e:
            print(f"Error saving file {target_file}: {e}")
            return False
    
    def _index_file(self, arxml_file: ARXMLFile) -> None:
        """Index all elements in an ARXML file."""
        self._index_element_recursive(
            arxml_file.root_element, 
            "", 
            str(arxml_file.path)
        )
    
    def _index_element_recursive(self, element: ET.Element, parent_path: str, file_path: str) -> None:
        """Recursively index elements in the tree."""
        # Build current path
        short_name = XMLUtils.get_short_name(element)
        if short_name:
            current_path = PathUtils.build_autosar_path(
                PathUtils.parse_autosar_path(parent_path) + [short_name]
            )
        else:
            current_path = parent_path
        
        # Only index elements that have SHORT-NAME (actual named elements)
        # Skip container elements that don't have names themselves
        should_index = short_name is not None and short_name != ""
        
        if should_index:
            # Index element
            self.element_index.add_element(element, current_path, file_path)
        
        # Process children
        for child in element:
            self._index_element_recursive(child, current_path, file_path)
    
    def _serialize_file(self, file_path: Path, schema_version: AUTOSARRelease) -> str:
        """Serialize file content with proper formatting."""
        arxml_file = self.files.get(file_path)
        if not arxml_file:
            return ""
        
        # Get serialization rules
        rules = self.schema_manager.get_serialization_rules(schema_version)
        
        # Format XML with proper indentation
        formatted_xml = XMLUtils.format_xml_pretty(arxml_file.root_element)
        
        # Add XML declaration
        xml_declaration = self.naming_conventions.format_xml_declaration()
        
        # Add namespace information
        namespace = self.schema_manager.schemas[schema_version].namespace
        schema_location = f"{namespace} {schema_version.value.replace('-', '.')}.xsd"
        root_element = self.naming_conventions.format_root_element(namespace, schema_location)
        
        return f"{xml_declaration}\n{root_element}\n{formatted_xml}\n</AUTOSAR>"
    
    def get_element_by_path(self, path: str) -> Optional[ElementInfo]:
        """Get element by AUTOSAR path."""
        return self.element_index.get_element_by_path(path)
    
    def get_children(self, path: str) -> List[ElementInfo]:
        """Get direct children of element at path."""
        return self.element_index.get_children(path)
    
    def get_element_tree(self, root_path: str = "") -> Dict[str, Any]:
        """Get hierarchical tree structure of elements."""
        if not root_path:
            # Get root elements
            root_elements = self.element_index.get_children("")
            return {
                "path": "",
                "short_name": "ROOT",
                "element_type": "AUTOSAR",
                "children": [self._build_tree_node(elem) for elem in root_elements]
            }
        else:
            element_info = self.get_element_by_path(root_path)
            if element_info:
                return self._build_tree_node(element_info)
            return {}
    
    def _build_tree_node(self, element_info: ElementInfo) -> Dict[str, Any]:
        """Build tree node from element info."""
        children = self.element_index.get_children(element_info.path)
        
        return {
            "path": element_info.path,
            "short_name": element_info.short_name,
            "element_type": element_info.element_type,
            "uuid": element_info.uuid,
            "is_reference": element_info.is_reference,
            "children": [self._build_tree_node(child) for child in children]
        }
    
    def create_element(self, parent_path: str, element_type: str, short_name: str, 
                      attributes: Optional[Dict[str, str]] = None) -> Optional[str]:
        """Create a new element in the model."""
        parent_element = self.element_index.get_element_by_path(parent_path)
        if not parent_element:
            return None
        
        # Create new element
        new_element = ET.Element(element_type)
        
        # Add SHORT-NAME
        XMLUtils.set_short_name(new_element, short_name)
        
        # Add attributes
        if attributes:
            for attr_name, attr_value in attributes.items():
                XMLUtils.set_element_attribute(new_element, attr_name, attr_value)
        
        # Add to parent
        parent_element.element.append(new_element)
        
        # Build new path
        new_path = PathUtils.build_autosar_path(
            PathUtils.parse_autosar_path(parent_path) + [short_name]
        )
        
        # Update index
        self.element_index.add_element(new_element, new_path, parent_element.file_path)
        
        # Mark as modified
        self.is_modified = True
        if parent_element.file_path:
            file_path = Path(parent_element.file_path)
            if file_path in self.files:
                self.files[file_path].is_modified = True
        
        return new_path
    
    def delete_element(self, path: str) -> bool:
        """Delete an element from the model."""
        element_info = self.element_index.get_element_by_path(path)
        if not element_info:
            return False
        
        # Remove from parent
        parent_path = PathUtils.get_parent_path(path)
        if parent_path:
            parent_element = self.element_index.get_element_by_path(parent_path)
            if parent_element:
                parent_element.element.remove(element_info.element)
        
        # Remove from index
        self.element_index.remove_element(path)
        
        # Mark as modified
        self.is_modified = True
        if element_info.file_path:
            file_path = Path(element_info.file_path)
            if file_path in self.files:
                self.files[file_path].is_modified = True
        
        return True
    
    def update_element_attribute(self, path: str, attribute: str, value: str) -> bool:
        """Update element attribute."""
        element_info = self.element_index.get_element_by_path(path)
        if not element_info:
            return False
        
        XMLUtils.set_element_attribute(element_info.element, attribute, value)
        
        # Update index if this affects indexing
        if attribute == "UUID":
            self.element_index.update_element(path, element_info.element)
        
        # Mark as modified
        self.is_modified = True
        if element_info.file_path:
            file_path = Path(element_info.file_path)
            if file_path in self.files:
                self.files[file_path].is_modified = True
        
        return True
    
    def update_element_text(self, path: str, text: str) -> bool:
        """Update element text content."""
        element_info = self.element_index.get_element_by_path(path)
        if not element_info:
            return False
        
        XMLUtils.set_element_text(element_info.element, text)
        
        # Update index if this affects SHORT-NAME
        if element_info.element.tag.endswith("SHORT-NAME"):
            # This is a SHORT-NAME element, need to update parent
            parent_path = PathUtils.get_parent_path(path)
            if parent_path:
                parent_element = self.element_index.get_element_by_path(parent_path)
                if parent_element:
                    self.element_index.update_element(parent_path, parent_element.element)
        
        # Mark as modified
        self.is_modified = True
        if element_info.file_path:
            file_path = Path(element_info.file_path)
            if file_path in self.files:
                self.files[file_path].is_modified = True
        
        return True
    
    def search_elements(self, query: str, element_type: Optional[str] = None) -> List[ElementInfo]:
        """Search for elements by name."""
        results = self.element_index.search_by_name(query)
        
        if element_type:
            results = [r for r in results if r.element_type == element_type]
        
        return results
    
    def get_validation_errors(self) -> List[Tuple[str, str]]:
        """Get all validation errors in the model."""
        errors = []
        
        # XSD validation errors
        for file_path, arxml_file in self.files.items():
            if arxml_file.schema_version:
                xsd_errors = self.schema_manager.validate_xsd(
                    arxml_file.content, 
                    arxml_file.schema_version
                )
                for error in xsd_errors:
                    errors.append((str(file_path), error))
        
        # Reference validation errors
        ref_errors = self.reference_manager.validate_all_references()
        errors.extend(ref_errors)
        
        # Element structure validation
        for element_info in self.element_index.get_all_elements():
            struct_errors = XMLUtils.validate_xml_structure(element_info.element)
            for error in struct_errors:
                errors.append((element_info.path, error))
        
        return errors
    
    def get_reference_statistics(self) -> Dict[str, Any]:
        """Get reference statistics."""
        return self.reference_manager.get_reference_statistics()
    
    def get_model_statistics(self) -> Dict[str, Any]:
        """Get overall model statistics."""
        element_stats = self.element_index.get_statistics()
        ref_stats = self.get_reference_statistics()
        
        return {
            "files": len(self.files),
            "current_file": str(self.current_file) if self.current_file else None,
            "is_modified": self.is_modified,
            "elements": element_stats,
            "references": ref_stats
        }
    
    def clear(self) -> None:
        """Clear the entire model."""
        self.files.clear()
        self.current_file = None
        self.is_modified = False
        self.element_index.clear()
        self.reference_manager = ReferenceManager(self.element_index)
    
    def get_supported_schemas(self) -> List[AUTOSARRelease]:
        """Get list of supported AUTOSAR schemas."""
        return self.schema_manager.get_supported_releases()
    
    def can_convert_schema(self, target_schema: AUTOSARRelease) -> bool:
        """Check if current model can be converted to target schema."""
        if not self.current_file or not self.files[self.current_file].schema_version:
            return True  # No current schema, can convert to any
        
        return self.schema_manager.can_convert_to(
            self.files[self.current_file].schema_version,
            target_schema
        )
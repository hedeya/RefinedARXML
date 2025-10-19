"""
ARXML serialization with proper naming conventions and deterministic output.

Implements AUTOSAR serialization rules for consistent XML output.
"""

import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

from .naming_converter import NamingConverter
from .xml_formatter import XMLFormatter
from ..core.schema_manager import AUTOSARRelease
from ..utils.naming_conventions import ARXMLNamingConventions


class SerializationMode(Enum):
    """Serialization modes."""
    DETERMINISTIC = "deterministic"  # Consistent ordering, no comments
    PRESERVE_FORMATTING = "preserve"  # Preserve existing formatting
    MINIMAL = "minimal"  # Minimal whitespace


@dataclass
class SerializationOptions:
    """Options for ARXML serialization."""
    mode: SerializationMode = SerializationMode.DETERMINISTIC
    indent_size: int = 2
    line_ending: str = "\n"
    encoding: str = "UTF-8"
    include_xml_declaration: bool = True
    sort_attributes: bool = True
    sort_elements: bool = True
    preserve_comments: bool = False
    canonical_naming: bool = True


class ARXMLSerializer:
    """Serializes ARXML elements with proper naming conventions."""
    
    def __init__(self, schema_release: AUTOSARRelease = AUTOSARRelease.R22_11):
        self.schema_release = schema_release
        self.naming_converter = NamingConverter()
        self.xml_formatter = XMLFormatter()
        self.naming_conventions = ARXMLNamingConventions()
        
        # Get serialization rules for this release
        self.serialization_rules = self._get_serialization_rules()
    
    def _get_serialization_rules(self) -> Dict[str, Any]:
        """Get serialization rules for the current schema release."""
        rules = {
            "tag_naming": "UPPERCASE-HYPHENATED",
            "attribute_naming": "camelCase",
            "indentation": "2 spaces",
            "root_element": "AUTOSAR",
            "file_extension": ".arxml",
            "namespace": self._get_namespace_for_release(),
            "schema_location": self._get_schema_location_for_release()
        }
        return rules
    
    def _get_namespace_for_release(self) -> str:
        """Get namespace for current release."""
        namespaces = {
            AUTOSARRelease.R20_11: "http://autosar.org/schema/r4.0",
            AUTOSARRelease.R21_11: "http://autosar.org/schema/r4.1",
            AUTOSARRelease.R22_11: "http://autosar.org/schema/r4.2",
            AUTOSARRelease.R24_11: "http://autosar.org/schema/r4.4"
        }
        return namespaces.get(self.schema_release, namespaces[AUTOSARRelease.R22_11])
    
    def _get_schema_location_for_release(self) -> str:
        """Get schema location for current release."""
        schema_locations = {
            AUTOSARRelease.R20_11: "http://autosar.org/schema/r4.0 AUTOSAR_4-0-0.xsd",
            AUTOSARRelease.R21_11: "http://autosar.org/schema/r4.1 AUTOSAR_4-1-0.xsd",
            AUTOSARRelease.R22_11: "http://autosar.org/schema/r4.2 AUTOSAR_4-2-0.xsd",
            AUTOSARRelease.R24_11: "http://autosar.org/schema/r4.4 AUTOSAR_4-4-0.xsd"
        }
        return schema_locations.get(self.schema_release, schema_locations[AUTOSARRelease.R22_11])
    
    def serialize_element(self, element: ET.Element, options: Optional[SerializationOptions] = None) -> str:
        """Serialize a single element to ARXML string."""
        if options is None:
            options = SerializationOptions()
        
        # Apply naming conventions
        if options.canonical_naming:
            element = self._apply_naming_conventions(element)
        
        # Sort elements and attributes if requested
        if options.sort_elements:
            element = self._sort_element_children(element)
        
        if options.sort_attributes:
            element = self._sort_element_attributes(element)
        
        # Format XML
        if options.mode == SerializationMode.DETERMINISTIC:
            return self._serialize_deterministic(element, options)
        elif options.mode == SerializationMode.PRESERVE_FORMATTING:
            return self._serialize_preserve_formatting(element, options)
        else:
            return self._serialize_minimal(element, options)
    
    def serialize_document(self, root_element: ET.Element, options: Optional[SerializationOptions] = None) -> str:
        """Serialize a complete ARXML document."""
        if options is None:
            options = SerializationOptions()
        
        # Create document structure
        lines = []
        
        # XML declaration
        if options.include_xml_declaration:
            declaration = self.naming_conventions.format_xml_declaration(options.encoding)
            lines.append(declaration)
        
        # Root element with namespace
        namespace = self.serialization_rules["namespace"]
        schema_location = self.serialization_rules["schema_location"]
        root_start = self.naming_conventions.format_root_element(namespace, schema_location)
        lines.append(root_start)
        
        # Serialize content
        content = self.serialize_element(root_element, options)
        lines.append(content)
        
        # Close root element
        lines.append("</AUTOSAR>")
        
        return options.line_ending.join(lines)
    
    def _apply_naming_conventions(self, element: ET.Element) -> ET.Element:
        """Apply AUTOSAR naming conventions to element."""
        # Convert element tag to UPPERCASE-HYPHENATED
        if '}' in element.tag:
            namespace, local_name = element.tag.split('}', 1)
            converted_name = self.naming_converter.to_uppercase_hyphenated(local_name)
            element.tag = f"{namespace}}}{converted_name}"
        else:
            element.tag = self.naming_converter.to_uppercase_hyphenated(element.tag)
        
        # Convert attributes to camelCase
        new_attrib = {}
        for attr_name, attr_value in element.attrib.items():
            if not attr_name.startswith('xmlns') and not attr_name.startswith('xsi:'):
                converted_name = self.naming_converter.to_camel_case(attr_name)
                new_attrib[converted_name] = attr_value
            else:
                new_attrib[attr_name] = attr_value
        element.attrib = new_attrib
        
        # Recursively apply to children
        for child in element:
            self._apply_naming_conventions(child)
        
        return element
    
    def _sort_element_children(self, element: ET.Element) -> ET.Element:
        """Sort element children for deterministic output."""
        if not element:
            return element
        
        # Define element ordering
        element_order = {
            "SHORT-NAME": 0,
            "LONG-NAME": 1,
            "DESC": 2,
            "L-1": 3, "L-2": 4, "L-3": 5, "L-4": 6, "L-5": 7,
            "L-6": 8, "L-7": 9, "L-8": 10, "L-9": 11, "L-10": 12,
            "ELEMENTS": 20,
            "ELEMENT": 21,
            "CONTAINERS": 30,
            "CONTAINER": 31,
            "PARAMETERS": 40,
            "PARAMETER": 41,
            "REFERENCES": 50,
            "REFERENCE": 51,
            "REF": 60,
            "DEST": 61,
            "DEFINITION-REF": 70,
            "VALUE-REF": 71,
            "VALUE": 80,
            "ECUC-VALUE-COLLECTION": 90,
            "ECUC-PARAM-CONF-CONTAINER-VALUE": 91,
            "ECUC-TEXTUAL-PARAM-VALUE": 92,
            "ECUC-NUMERICAL-PARAM-VALUE": 93,
            "ECUC-BOOLEAN-PARAM-VALUE": 94,
            "ECUC-ENUMERATION-PARAM-VALUE": 95
        }
        
        # Sort children
        children = list(element)
        children.sort(key=lambda child: self._get_element_order(child, element_order))
        
        # Remove all children
        for child in children:
            element.remove(child)
        
        # Add back in sorted order
        for child in children:
            element.append(child)
        
        # Recursively sort children
        for child in element:
            self._sort_element_children(child)
        
        return element
    
    def _get_element_order(self, element: ET.Element, order_map: Dict[str, int]) -> int:
        """Get sort order for element."""
        tag_name = element.tag
        if '}' in tag_name:
            tag_name = tag_name.split('}', 1)[1]
        
        return order_map.get(tag_name, 999)
    
    def _sort_element_attributes(self, element: ET.Element) -> ET.Element:
        """Sort element attributes for deterministic output."""
        if not element.attrib:
            return element
        
        # Define attribute ordering
        attr_order = {
            "xmlns": 0,
            "xmlns:xsi": 1,
            "xsi:schemaLocation": 2,
            "DEST": 10,
            "UUID": 11,
            "S": 12,
            "T": 13
        }
        
        # Sort attributes
        sorted_attrs = sorted(element.attrib.items(), 
                            key=lambda item: attr_order.get(item[0], 999))
        
        # Clear and re-add in sorted order
        element.attrib.clear()
        for attr_name, attr_value in sorted_attrs:
            element.attrib[attr_name] = attr_value
        
        return element
    
    def _serialize_deterministic(self, element: ET.Element, options: SerializationOptions) -> str:
        """Serialize with deterministic formatting."""
        return self.xml_formatter.format_deterministic(element, options)
    
    def _serialize_preserve_formatting(self, element: ET.Element, options: SerializationOptions) -> str:
        """Serialize preserving existing formatting."""
        return self.xml_formatter.format_preserve(element, options)
    
    def _serialize_minimal(self, element: ET.Element, options: SerializationOptions) -> str:
        """Serialize with minimal whitespace."""
        return self.xml_formatter.format_minimal(element, options)
    
    def validate_serialization(self, xml_content: str) -> List[str]:
        """Validate serialized XML content."""
        errors = []
        
        try:
            # Parse XML to check well-formedness
            ET.fromstring(xml_content)
        except ET.ParseError as e:
            errors.append(f"XML parsing error: {e}")
        
        # Check for proper namespace
        try:
            root = ET.fromstring(xml_content)
            if root.tag != "AUTOSAR":
                errors.append("Root element must be AUTOSAR")
            
            # Check namespace
            if '}' in root.tag:
                namespace = root.tag.split('}', 1)[0].lstrip('{')
                expected_namespace = self.serialization_rules["namespace"]
                if namespace != expected_namespace:
                    errors.append(f"Namespace mismatch: expected {expected_namespace}, found {namespace}")
        except ET.ParseError:
            pass  # Already caught above
        
        return errors
    
    def convert_to_release(self, element: ET.Element, target_release: AUTOSARRelease) -> ET.Element:
        """Convert element to different AUTOSAR release."""
        # Create new serializer for target release
        target_serializer = ARXMLSerializer(target_release)
        
        # Deep copy element
        import copy
        converted_element = copy.deepcopy(element)
        
        # Apply target release naming conventions
        converted_element = target_serializer._apply_naming_conventions(converted_element)
        
        return converted_element
    
    def get_serialization_rules(self) -> Dict[str, Any]:
        """Get current serialization rules."""
        return self.serialization_rules.copy()
    
    def set_schema_release(self, release: AUTOSARRelease):
        """Set schema release for serialization."""
        self.schema_release = release
        self.serialization_rules = self._get_serialization_rules()
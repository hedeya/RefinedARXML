"""
Naming convention converter for ARXML elements and attributes.

Converts between different naming conventions used in AUTOSAR.
"""

import re
from typing import Dict, List, Tuple


class NamingConverter:
    """Converts between different naming conventions."""
    
    def __init__(self):
        # Common AUTOSAR element name mappings
        self.element_mappings = {
            # Common elements
            "shortName": "SHORT-NAME",
            "longName": "LONG-NAME",
            "description": "DESC",
            "elements": "ELEMENTS",
            "element": "ELEMENT",
            "containers": "CONTAINERS",
            "container": "CONTAINER",
            "parameters": "PARAMETERS",
            "parameter": "PARAMETER",
            "references": "REFERENCES",
            "reference": "REFERENCE",
            "ref": "REF",
            "dest": "DEST",
            "definitionRef": "DEFINITION-REF",
            "valueRef": "VALUE-REF",
            "value": "VALUE",
            
            # ECUC elements
            "ecucValueCollection": "ECUC-VALUE-COLLECTION",
            "ecucParamConfContainerValue": "ECUC-PARAM-CONF-CONTAINER-VALUE",
            "ecucTextualParamValue": "ECUC-TEXTUAL-PARAM-VALUE",
            "ecucNumericalParamValue": "ECUC-NUMERICAL-PARAM-VALUE",
            "ecucBooleanParamValue": "ECUC-BOOLEAN-PARAM-VALUE",
            "ecucEnumerationParamValue": "ECUC-ENUMERATION-PARAM-VALUE",
            
            # Language elements
            "l1": "L-1", "l2": "L-2", "l3": "L-3", "l4": "L-4", "l5": "L-5",
            "l6": "L-6", "l7": "L-7", "l8": "L-8", "l9": "L-9", "l10": "L-10",
            
            # AR Package elements
            "arPackages": "AR-PACKAGES",
            "arPackage": "AR-PACKAGE",
            "shortNameFragment": "SHORT-NAME-FRAGMENT"
        }
        
        # Reverse mappings for conversion back
        self.reverse_element_mappings = {v: k for k, v in self.element_mappings.items()}
        
        # Common attribute name mappings
        self.attribute_mappings = {
            "dest": "DEST",
            "uuid": "UUID",
            "s": "S",
            "t": "T"
        }
        
        self.reverse_attribute_mappings = {v: k for k, v in self.attribute_mappings.items()}
    
    def to_uppercase_hyphenated(self, name: str) -> str:
        """Convert camelCase to UPPERCASE-HYPHENATED."""
        if not name:
            return name
        
        # Check if already in correct format
        if self._is_uppercase_hyphenated(name):
            return name
        
        # Check direct mapping first
        if name in self.element_mappings:
            return self.element_mappings[name]
        
        # Convert camelCase to UPPERCASE-HYPHENATED
        # Insert hyphen before uppercase letters (except the first one)
        result = re.sub(r'(?<!^)(?=[A-Z])', '-', name)
        return result.upper()
    
    def to_camel_case(self, name: str) -> str:
        """Convert UPPERCASE-HYPHENATED to camelCase."""
        if not name:
            return name
        
        # Check if already in correct format
        if self._is_camel_case(name):
            return name
        
        # Check direct mapping first
        if name in self.reverse_element_mappings:
            return self.reverse_element_mappings[name]
        
        # Convert UPPERCASE-HYPHENATED to camelCase
        parts = name.split('-')
        if not parts:
            return ""
        
        return parts[0].lower() + ''.join(part.capitalize() for part in parts[1:])
    
    def to_uppercase_hyphenated_attribute(self, name: str) -> str:
        """Convert camelCase attribute to UPPERCASE-HYPHENATED."""
        if not name:
            return name
        
        # Check direct mapping first
        if name in self.attribute_mappings:
            return self.attribute_mappings[name]
        
        # Convert camelCase to UPPERCASE-HYPHENATED
        return self.to_uppercase_hyphenated(name)
    
    def to_camel_case_attribute(self, name: str) -> str:
        """Convert UPPERCASE-HYPHENATED attribute to camelCase."""
        if not name:
            return name
        
        # Check direct mapping first
        if name in self.reverse_attribute_mappings:
            return self.reverse_attribute_mappings[name]
        
        # Convert UPPERCASE-HYPHENATED to camelCase
        return self.to_camel_case(name)
    
    def _is_uppercase_hyphenated(self, name: str) -> bool:
        """Check if name is in UPPERCASE-HYPHENATED format."""
        if not name:
            return False
        
        # Pattern: starts with uppercase letter, contains only uppercase letters, numbers, and hyphens
        pattern = r'^[A-Z][A-Z0-9]*(?:-[A-Z][A-Z0-9]*)*$'
        return bool(re.match(pattern, name))
    
    def _is_camel_case(self, name: str) -> bool:
        """Check if name is in camelCase format."""
        if not name:
            return False
        
        # Pattern: starts with lowercase letter, contains only letters and numbers
        pattern = r'^[a-z][a-zA-Z0-9]*$'
        return bool(re.match(pattern, name))
    
    def validate_element_name(self, name: str) -> Tuple[bool, str]:
        """Validate element name format."""
        if not name:
            return False, "Element name cannot be empty"
        
        # Check for valid characters
        if not re.match(r'^[A-Z][A-Z0-9]*(?:-[A-Z][A-Z0-9]*)*$', name):
            return False, "Element name must be in UPPERCASE-HYPHENATED format"
        
        # Check for reserved names
        reserved_names = {"XML", "XMLNS", "XSI"}
        if name.upper() in reserved_names:
            return False, f"'{name}' is a reserved XML name"
        
        return True, ""
    
    def validate_attribute_name(self, name: str) -> Tuple[bool, str]:
        """Validate attribute name format."""
        if not name:
            return False, "Attribute name cannot be empty"
        
        # Namespace attributes are allowed
        if name.startswith('xmlns') or name.startswith('xsi:'):
            return True, ""
        
        # Check for valid camelCase format
        if not re.match(r'^[a-z][a-zA-Z0-9]*$', name):
            return False, "Attribute name must be in camelCase format"
        
        # Check for reserved names
        reserved_names = {"xml", "xmlns", "xsi"}
        if name.lower() in reserved_names:
            return False, f"'{name}' is a reserved XML name"
        
        return True, ""
    
    def get_common_element_names(self) -> List[str]:
        """Get list of common AUTOSAR element names."""
        return list(self.element_mappings.keys())
    
    def get_common_attribute_names(self) -> List[str]:
        """Get list of common AUTOSAR attribute names."""
        return list(self.attribute_mappings.keys())
    
    def add_custom_mapping(self, camel_case: str, uppercase_hyphenated: str):
        """Add custom name mapping."""
        self.element_mappings[camel_case] = uppercase_hyphenated
        self.reverse_element_mappings[uppercase_hyphenated] = camel_case
    
    def remove_custom_mapping(self, camel_case: str):
        """Remove custom name mapping."""
        if camel_case in self.element_mappings:
            uppercase_hyphenated = self.element_mappings[camel_case]
            del self.element_mappings[camel_case]
            if uppercase_hyphenated in self.reverse_element_mappings:
                del self.reverse_element_mappings[uppercase_hyphenated]
    
    def convert_element_tree(self, element, to_uppercase: bool = True):
        """Convert entire element tree naming conventions."""
        if to_uppercase:
            # Convert to UPPERCASE-HYPHENATED
            element.tag = self.to_uppercase_hyphenated(element.tag)
            
            # Convert attributes
            new_attrib = {}
            for attr_name, attr_value in element.attrib.items():
                if not attr_name.startswith('xmlns') and not attr_name.startswith('xsi:'):
                    converted_name = self.to_uppercase_hyphenated_attribute(attr_name)
                    new_attrib[converted_name] = attr_value
                else:
                    new_attrib[attr_name] = attr_value
            element.attrib = new_attrib
        else:
            # Convert to camelCase
            element.tag = self.to_camel_case(element.tag)
            
            # Convert attributes
            new_attrib = {}
            for attr_name, attr_value in element.attrib.items():
                if not attr_name.startswith('xmlns') and not attr_name.startswith('xsi:'):
                    converted_name = self.to_camel_case_attribute(attr_name)
                    new_attrib[converted_name] = attr_value
                else:
                    new_attrib[attr_name] = attr_value
            element.attrib = new_attrib
        
        # Recursively convert children
        for child in element:
            self.convert_element_tree(child, to_uppercase)
    
    def get_naming_statistics(self, element) -> Dict[str, int]:
        """Get statistics about naming conventions in element tree."""
        stats = {
            "total_elements": 0,
            "uppercase_hyphenated": 0,
            "camel_case": 0,
            "other_format": 0,
            "total_attributes": 0,
            "camel_case_attributes": 0,
            "other_attribute_format": 0
        }
        
        def count_element(elem):
            stats["total_elements"] += 1
            
            # Count element naming
            tag_name = elem.tag
            if '}' in tag_name:
                tag_name = tag_name.split('}', 1)[1]
            
            if self._is_uppercase_hyphenated(tag_name):
                stats["uppercase_hyphenated"] += 1
            elif self._is_camel_case(tag_name):
                stats["camel_case"] += 1
            else:
                stats["other_format"] += 1
            
            # Count attributes
            for attr_name in elem.attrib.keys():
                stats["total_attributes"] += 1
                
                if not attr_name.startswith('xmlns') and not attr_name.startswith('xsi:'):
                    if self._is_camel_case(attr_name):
                        stats["camel_case_attributes"] += 1
                    else:
                        stats["other_attribute_format"] += 1
            
            # Recursively count children
            for child in elem:
                count_element(child)
        
        count_element(element)
        return stats
"""
ARXML naming conventions and serialization rules.

Implements AUTOSAR naming conventions for tags, attributes, and file packaging.
"""

import re
from typing import Dict, List, Optional, Tuple


class ARXMLNamingConventions:
    """Handles ARXML naming conventions and serialization rules."""
    
    def __init__(self):
        self.tag_pattern = re.compile(r'^[A-Z][A-Z0-9]*(?:-[A-Z][A-Z0-9]*)*$')
        self.attribute_pattern = re.compile(r'^[a-z][a-zA-Z0-9]*$')
        self.short_name_pattern = re.compile(r'^[A-Za-z][A-Za-z0-9_]*$')
    
    def camel_case_to_uppercase_hyphenated(self, camel_case: str) -> str:
        """Convert camelCase to UPPERCASE-HYPHENATED for ARXML tags."""
        # Insert hyphens before uppercase letters (except the first one)
        result = re.sub(r'(?<!^)(?=[A-Z])', '-', camel_case)
        return result.upper()
    
    def uppercase_hyphenated_to_camel_case(self, uppercase_hyphenated: str) -> str:
        """Convert UPPERCASE-HYPHENATED to camelCase for internal use."""
        parts = uppercase_hyphenated.split('-')
        if not parts:
            return ""
        return parts[0].lower() + ''.join(part.capitalize() for part in parts[1:])
    
    def validate_tag_name(self, tag_name: str) -> Tuple[bool, Optional[str]]:
        """Validate ARXML tag name format."""
        if not self.tag_pattern.match(tag_name):
            return False, f"Tag name '{tag_name}' must be UPPERCASE-HYPHENATED format"
        return True, None
    
    def validate_attribute_name(self, attr_name: str) -> Tuple[bool, Optional[str]]:
        """Validate ARXML attribute name format."""
        if not self.attribute_pattern.match(attr_name):
            return False, f"Attribute name '{attr_name}' must be camelCase format"
        return True, None
    
    def validate_short_name(self, short_name: str) -> Tuple[bool, Optional[str]]:
        """Validate AUTOSAR SHORT-NAME format."""
        if not self.short_name_pattern.match(short_name):
            return False, f"SHORT-NAME '{short_name}' must start with letter and contain only letters, numbers, and underscores"
        return True, None
    
    def normalize_tag_name(self, tag_name: str) -> str:
        """Normalize tag name to ARXML convention."""
        # Convert from any format to UPPERCASE-HYPHENATED
        if '-' in tag_name and tag_name.isupper():
            return tag_name  # Already correct
        elif tag_name.islower() or (tag_name[0].isupper() and not '-' in tag_name):
            return self.camel_case_to_uppercase_hyphenated(tag_name)
        else:
            # Handle mixed case or other formats
            return self.camel_case_to_uppercase_hyphenated(tag_name)
    
    def get_common_arxml_tags(self) -> List[str]:
        """Get list of common ARXML tags for validation."""
        return [
            "AUTOSAR",
            "AR-PACKAGES",
            "AR-PACKAGE",
            "SHORT-NAME",
            "LONG-NAME",
            "DESC",
            "L-4",
            "L-2",
            "L-1",
            "L-3",
            "L-5",
            "L-6",
            "L-7",
            "L-8",
            "L-9",
            "L-10",
            "ELEMENTS",
            "ELEMENT",
            "REF",
            "DEST",
            "SHORT-NAME-FRAGMENT",
            "ECUC-VALUE-COLLECTION",
            "ECUC-PARAM-CONF-CONTAINER-VALUE",
            "ECUC-REFERENCE-VALUE",
            "ECUC-TEXTUAL-PARAM-VALUE",
            "ECUC-NUMERICAL-PARAM-VALUE",
            "ECUC-BOOLEAN-PARAM-VALUE",
            "ECUC-ENUMERATION-PARAM-VALUE",
            "DEFINITION-REF",
            "VALUE-REF",
            "VALUE",
            "CONTAINERS",
            "CONTAINER",
            "PARAMETERS",
            "PARAMETER",
            "REFERENCES",
            "REFERENCE",
            "SUB-CONTAINERS",
            "SUB-CONTAINER"
        ]
    
    def get_common_arxml_attributes(self) -> List[str]:
        """Get list of common ARXML attributes for validation."""
        return [
            "xmlns",
            "xmlns:xsi",
            "xsi:schemaLocation",
            "DEST",
            "UUID",
            "S",
            "T"
        ]
    
    def format_xml_declaration(self, encoding: str = "UTF-8") -> str:
        """Format XML declaration for ARXML files."""
        return f'<?xml version="1.0" encoding="{encoding}"?>'
    
    def format_root_element(self, namespace: str, schema_location: str) -> str:
        """Format root AUTOSAR element with proper namespace."""
        return f'''<AUTOSAR xmlns="{namespace}" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="{schema_location}">'''
    
    def get_indentation(self, level: int, spaces_per_level: int = 2) -> str:
        """Get indentation string for XML formatting."""
        return " " * (level * spaces_per_level)
    
    def format_element(self, tag: str, content: str = "", attributes: Dict[str, str] = None, 
                      level: int = 0, self_closing: bool = False) -> str:
        """Format XML element with proper indentation and attributes."""
        indent = self.get_indentation(level)
        attr_str = ""
        
        if attributes:
            attr_str = " " + " ".join(f'{k}="{v}"' for k, v in attributes.items())
        
        if self_closing:
            return f"{indent}<{tag}{attr_str}/>"
        elif content:
            return f"{indent}<{tag}{attr_str}>{content}</{tag}>"
        else:
            return f"{indent}<{tag}{attr_str}></{tag}>"
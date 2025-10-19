"""
XML utilities for ARXML processing.

Provides helper functions for XML manipulation, parsing, and formatting.
"""

import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Tuple, Union
from pathlib import Path
import re


class XMLUtils:
    """Utility functions for XML processing."""
    
    @staticmethod
    def parse_xml_safe(content: str) -> Optional[ET.Element]:
        """Safely parse XML content, returning None on error."""
        try:
            return ET.fromstring(content)
        except ET.ParseError:
            return None
    
    @staticmethod
    def get_element_text(element: ET.Element, default: str = "") -> str:
        """Get text content of element, handling None values."""
        return element.text if element.text else default
    
    @staticmethod
    def set_element_text(element: ET.Element, text: str) -> None:
        """Set text content of element."""
        element.text = text
    
    @staticmethod
    def get_element_attribute(element: ET.Element, attr_name: str, default: str = "") -> str:
        """Get attribute value with default."""
        return element.get(attr_name, default)
    
    @staticmethod
    def set_element_attribute(element: ET.Element, attr_name: str, value: str) -> None:
        """Set attribute value."""
        element.set(attr_name, value)
    
    @staticmethod
    def find_element_by_tag(element: ET.Element, tag: str) -> Optional[ET.Element]:
        """Find first child element with specific tag."""
        for child in element:
            if child.tag.endswith(tag) or child.tag == tag:
                return child
        return None
    
    @staticmethod
    def find_elements_by_tag(element: ET.Element, tag: str) -> List[ET.Element]:
        """Find all child elements with specific tag."""
        return [child for child in element if child.tag.endswith(tag) or child.tag == tag]
    
    @staticmethod
    def find_element_by_short_name(element: ET.Element, short_name: str) -> Optional[ET.Element]:
        """Find element by SHORT-NAME value."""
        for child in element:
            short_name_elem = XMLUtils.find_element_by_tag(child, "SHORT-NAME")
            if short_name_elem is not None and XMLUtils.get_element_text(short_name_elem) == short_name:
                return child
        return None
    
    @staticmethod
    def get_short_name(element: ET.Element) -> str:
        """Get SHORT-NAME value from element."""
        short_name_elem = XMLUtils.find_element_by_tag(element, "SHORT-NAME")
        return XMLUtils.get_element_text(short_name_elem) if short_name_elem is not None else ""
    
    @staticmethod
    def set_short_name(element: ET.Element, short_name: str) -> None:
        """Set SHORT-NAME value for element."""
        short_name_elem = XMLUtils.find_element_by_tag(element, "SHORT-NAME")
        if short_name_elem is not None:
            XMLUtils.set_element_text(short_name_elem, short_name)
        else:
            # Create SHORT-NAME element
            short_name_elem = ET.SubElement(element, "SHORT-NAME")
            XMLUtils.set_element_text(short_name_elem, short_name)
    
    @staticmethod
    def get_long_name(element: ET.Element) -> str:
        """Get LONG-NAME value from element."""
        long_name_elem = XMLUtils.find_element_by_tag(element, "LONG-NAME")
        return XMLUtils.get_element_text(long_name_elem) if long_name_elem is not None else ""
    
    @staticmethod
    def set_long_name(element: ET.Element, long_name: str) -> None:
        """Set LONG-NAME value for element."""
        long_name_elem = XMLUtils.find_element_by_tag(element, "LONG-NAME")
        if long_name_elem is not None:
            XMLUtils.set_element_text(long_name_elem, long_name)
        else:
            # Create LONG-NAME element
            long_name_elem = ET.SubElement(element, "LONG-NAME")
            XMLUtils.set_element_text(long_name_elem, long_name)
    
    @staticmethod
    def create_reference_element(ref_value: str, dest: str = "DEST") -> ET.Element:
        """Create a reference element with REF and DEST."""
        ref_elem = ET.Element("REF")
        XMLUtils.set_element_text(ref_elem, ref_value)
        XMLUtils.set_element_attribute(ref_elem, "DEST", dest)
        return ref_elem
    
    @staticmethod
    def get_reference_value(element: ET.Element) -> Tuple[str, str]:
        """Get reference value and DEST from reference element."""
        ref_text = XMLUtils.get_element_text(element)
        dest = XMLUtils.get_element_attribute(element, "DEST", "")
        return ref_text, dest
    
    @staticmethod
    def format_xml_pretty(element: ET.Element, level: int = 0, spaces: int = 2) -> str:
        """Format XML element with pretty printing."""
        indent = " " * (level * spaces)
        
        if len(element) == 0:
            # Leaf element
            text = element.text or ""
            if text:
                return f"{indent}<{element.tag}>{text}</{element.tag}>"
            else:
                return f"{indent}<{element.tag}/>"
        else:
            # Container element
            lines = [f"{indent}<{element.tag}>"]
            
            if element.text and element.text.strip():
                lines.append(f"{indent}{' ' * spaces}{element.text.strip()}")
            
            for child in element:
                lines.append(XMLUtils.format_xml_pretty(child, level + 1, spaces))
            
            if element.tail and element.tail.strip():
                lines.append(f"{indent}{' ' * spaces}{element.tail.strip()}")
            
            lines.append(f"{indent}</{element.tag}>")
            return "\n".join(lines)
    
    @staticmethod
    def extract_namespace_prefix(tag: str) -> Tuple[str, str]:
        """Extract namespace prefix and local name from tag."""
        if '}' in tag:
            return tag.split('}', 1)
        return "", tag
    
    @staticmethod
    def is_reference_element(element: ET.Element) -> bool:
        """Check if element is a reference (has REF tag)."""
        return element.tag.endswith("REF") or element.tag == "REF"
    
    @staticmethod
    def get_element_path(element: ET.Element) -> str:
        """Get XPath-like path for element."""
        path_parts = []
        current = element
        
        while current is not None:
            tag_name = current.tag
            if '}' in tag_name:
                tag_name = tag_name.split('}', 1)[1]
            path_parts.insert(0, tag_name)
            current = current.getparent() if hasattr(current, 'getparent') else None
        
        return "/" + "/".join(path_parts)
    
    @staticmethod
    def validate_xml_structure(element: ET.Element) -> List[str]:
        """Basic XML structure validation."""
        errors = []
        
        # Check for empty tags with both text and children
        if element.text and element.text.strip() and len(element) > 0:
            errors.append(f"Element {element.tag} has both text content and child elements")
        
        # Check for required SHORT-NAME in AUTOSAR elements
        if element.tag not in ["AUTOSAR", "AR-PACKAGES", "ELEMENTS"] and not element.tag.startswith("L-"):
            short_name = XMLUtils.get_short_name(element)
            if not short_name:
                errors.append(f"Element {element.tag} missing required SHORT-NAME")
        
        # Recursively check children
        for child in element:
            errors.extend(XMLUtils.validate_xml_structure(child))
        
        return errors
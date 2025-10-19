"""
XML formatter for ARXML files with different formatting modes.

Provides deterministic, minimal, and preserve formatting options.
"""

import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class FormattingMode(Enum):
    """XML formatting modes."""
    DETERMINISTIC = "deterministic"
    MINIMAL = "minimal"
    PRESERVE = "preserve"
    PRETTY = "pretty"


@dataclass
class FormattingOptions:
    """Options for XML formatting."""
    indent_size: int = 2
    line_ending: str = "\n"
    encoding: str = "UTF-8"
    sort_attributes: bool = True
    sort_elements: bool = True
    preserve_whitespace: bool = False
    add_xml_declaration: bool = True
    canonical_format: bool = True


class XMLFormatter:
    """Formats XML with various formatting options."""
    
    def __init__(self):
        self.default_options = FormattingOptions()
    
    def format_deterministic(self, element: ET.Element, options: Optional[FormattingOptions] = None) -> str:
        """Format XML with deterministic output."""
        if options is None:
            options = self.default_options
        
        # Sort elements and attributes for deterministic output
        if options.sort_elements:
            element = self._sort_elements(element)
        
        if options.sort_attributes:
            element = self._sort_attributes(element)
        
        # Format with consistent indentation
        return self._format_with_indentation(element, options)
    
    def format_minimal(self, element: ET.Element, options: Optional[FormattingOptions] = None) -> str:
        """Format XML with minimal whitespace."""
        if options is None:
            options = self.defaultOptions
        
        # Convert to string with minimal formatting
        return ET.tostring(element, encoding=options.encoding).decode(options.encoding)
    
    def format_preserve(self, element: ET.Element, options: Optional[FormattingOptions] = None) -> str:
        """Format XML preserving existing formatting."""
        if options is None:
            options = self.default_options
        
        # Try to preserve existing formatting
        return self._format_preserve_whitespace(element, options)
    
    def format_pretty(self, element: ET.Element, options: Optional[FormattingOptions] = None) -> str:
        """Format XML with pretty printing."""
        if options is None:
            options = self.default_options
        
        return self._format_pretty_print(element, options)
    
    def _format_with_indentation(self, element: ET.Element, options: FormattingOptions) -> str:
        """Format element with consistent indentation."""
        lines = []
        self._format_element_recursive(element, lines, 0, options)
        return options.line_ending.join(lines)
    
    def _format_element_recursive(self, element: ET.Element, lines: List[str], 
                                 level: int, options: FormattingOptions):
        """Recursively format element with indentation."""
        indent = " " * (level * options.indent_size)
        
        # Start tag
        tag_name = element.tag
        if '}' in tag_name:
            tag_name = tag_name.split('}', 1)[1]
        
        if element.attrib:
            # Element with attributes
            attr_str = " " + " ".join(f'{k}="{v}"' for k, v in element.attrib.items())
            start_tag = f"{indent}<{tag_name}{attr_str}>"
        else:
            start_tag = f"{indent}<{tag_name}>"
        
        # Check if element has children or text
        has_children = len(element) > 0
        has_text = element.text and element.text.strip()
        
        if not has_children and not has_text:
            # Self-closing tag
            lines.append(f"{indent}<{tag_name}{attr_str if element.attrib else ''}/>")
        elif not has_children and has_text:
            # Element with text only
            text_content = element.text.strip()
            lines.append(f"{start_tag}{text_content}</{tag_name}>")
        else:
            # Element with children
            lines.append(start_tag)
            
            # Add text content if present
            if has_text:
                text_content = element.text.strip()
                text_indent = " " * ((level + 1) * options.indent_size)
                lines.append(f"{text_indent}{text_content}")
            
            # Add children
            for child in element:
                self._format_element_recursive(child, lines, level + 1, options)
            
            # Add tail text if present
            if element.tail and element.tail.strip():
                tail_content = element.tail.strip()
                lines.append(f"{indent}{tail_content}")
            
            # End tag
            lines.append(f"{indent}</{tag_name}>")
    
    def _format_pretty_print(self, element: ET.Element, options: FormattingOptions) -> str:
        """Format with pretty printing."""
        # Use ElementTree's built-in pretty printing
        self._indent_xml(element, level=0, indent_size=options.indent_size)
        return ET.tostring(element, encoding=options.encoding).decode(options.encoding)
    
    def _indent_xml(self, element: ET.Element, level: int, indent_size: int):
        """Add indentation to XML element."""
        indent = "\n" + " " * (level * indent_size)
        
        if len(element):
            if not element.text or not element.text.strip():
                element.text = indent + " " * indent_size
            if not element.tail or not element.tail.strip():
                element.tail = indent
            
            for child in element:
                self._indent_xml(child, level + 1, indent_size)
                if not child.tail or not child.tail.strip():
                    child.tail = indent
        else:
            if not element.tail or not element.tail.strip():
                element.tail = indent
    
    def _format_preserve_whitespace(self, element: ET.Element, options: FormattingOptions) -> str:
        """Format preserving existing whitespace."""
        # This is a simplified implementation
        # In practice, you'd need to track and preserve original whitespace
        return ET.tostring(element, encoding=options.encoding).decode(options.encoding)
    
    def _sort_elements(self, element: ET.Element) -> ET.Element:
        """Sort child elements for deterministic output."""
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
            self._sort_elements(child)
        
        return element
    
    def _get_element_order(self, element: ET.Element, order_map: Dict[str, int]) -> int:
        """Get sort order for element."""
        tag_name = element.tag
        if '}' in tag_name:
            tag_name = tag_name.split('}', 1)[1]
        
        return order_map.get(tag_name, 999)
    
    def _sort_attributes(self, element: ET.Element) -> ET.Element:
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
    
    def validate_formatting(self, xml_content: str) -> List[str]:
        """Validate XML formatting."""
        errors = []
        
        try:
            # Parse XML to check well-formedness
            ET.fromstring(xml_content)
        except ET.ParseError as e:
            errors.append(f"XML parsing error: {e}")
        
        # Check for proper indentation (basic check)
        lines = xml_content.split('\n')
        for i, line in enumerate(lines):
            if line.strip() and not line.startswith('<?xml'):
                # Check for consistent indentation
                if line.startswith(' ') and not line.startswith('  '):
                    errors.append(f"Line {i+1}: Inconsistent indentation")
        
        return errors
    
    def get_formatting_statistics(self, xml_content: str) -> Dict[str, Any]:
        """Get statistics about XML formatting."""
        lines = xml_content.split('\n')
        
        stats = {
            "total_lines": len(lines),
            "empty_lines": len([line for line in lines if not line.strip()]),
            "indented_lines": len([line for line in lines if line.startswith(' ')]),
            "max_indentation": 0,
            "average_line_length": 0
        }
        
        # Calculate max indentation
        for line in lines:
            if line.strip():
                indent_level = len(line) - len(line.lstrip())
                stats["max_indentation"] = max(stats["max_indentation"], indent_level)
        
        # Calculate average line length
        non_empty_lines = [line for line in lines if line.strip()]
        if non_empty_lines:
            stats["average_line_length"] = sum(len(line) for line in non_empty_lines) / len(non_empty_lines)
        
        return stats
    
    def normalize_whitespace(self, xml_content: str) -> str:
        """Normalize whitespace in XML content."""
        lines = xml_content.split('\n')
        normalized_lines = []
        
        for line in lines:
            # Remove trailing whitespace
            line = line.rstrip()
            
            # Normalize internal whitespace (but preserve structure)
            if line.strip():
                # Split by spaces and rejoin to normalize
                parts = line.split()
                if parts:
                    # Reconstruct with proper indentation
                    indent = len(line) - len(line.lstrip())
                    normalized_line = ' ' * indent + ' '.join(parts)
                    normalized_lines.append(normalized_line)
                else:
                    normalized_lines.append(line)
            else:
                normalized_lines.append('')
        
        return '\n'.join(normalized_lines)
    
    def compress_xml(self, xml_content: str) -> str:
        """Compress XML by removing unnecessary whitespace."""
        # Remove comments
        import re
        xml_content = re.sub(r'<!--.*?-->', '', xml_content, flags=re.DOTALL)
        
        # Remove extra whitespace
        xml_content = re.sub(r'\s+', ' ', xml_content)
        
        # Remove whitespace around tags
        xml_content = re.sub(r'>\s+<', '><', xml_content)
        
        return xml_content.strip()
    
    def beautify_xml(self, xml_content: str, options: Optional[FormattingOptions] = None) -> str:
        """Beautify XML with proper formatting."""
        if options is None:
            options = self.default_options
        
        try:
            # Parse XML
            element = ET.fromstring(xml_content)
            
            # Format with pretty printing
            return self.format_pretty(element, options)
        except ET.ParseError as e:
            return f"Error parsing XML: {e}"
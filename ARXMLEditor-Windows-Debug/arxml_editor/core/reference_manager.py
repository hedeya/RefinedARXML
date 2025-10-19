"""
Reference management for ARXML cross-references.

Handles reference resolution, validation, and integrity checking.
"""

from typing import Dict, List, Optional, Tuple, Set, Any
from dataclasses import dataclass
from enum import Enum
import xml.etree.ElementTree as ET
from .element_index import ElementIndex, ElementInfo
from ..utils.path_utils import PathUtils
from ..utils.xml_utils import XMLUtils


class ReferenceType(Enum):
    """Types of ARXML references."""
    PATH_REFERENCE = "path"
    UUID_REFERENCE = "uuid"
    DEFINITION_REF = "definition"
    VALUE_REF = "value"
    ECUC_REF = "ecuc"


@dataclass
class ReferenceInfo:
    """Information about a reference."""
    source_path: str
    target_path: str
    reference_type: ReferenceType
    dest_attribute: str
    is_resolved: bool
    is_valid: bool
    error_message: Optional[str] = None


class ReferenceManager:
    """Manages ARXML cross-references and their integrity."""
    
    def __init__(self, element_index: ElementIndex):
        self.element_index = element_index
        self.references: Dict[str, ReferenceInfo] = {}
        self._reference_cache: Dict[str, List[ReferenceInfo]] = {}
    
    def analyze_references(self) -> None:
        """Analyze all references in the current model."""
        self.references.clear()
        self._reference_cache.clear()
        
        for element_info in self.element_index.get_all_elements():
            if element_info.is_reference:
                self._process_reference(element_info)
    
    def _process_reference(self, element_info: ElementInfo) -> None:
        """Process a single reference element."""
        ref_value, dest = XMLUtils.get_reference_value(element_info.element)
        if not ref_value:
            return
        
        # Determine reference type
        ref_type = self._determine_reference_type(element_info.element, dest)
        
        # Resolve target path
        target_path = self._resolve_reference(ref_value, dest, element_info.path)
        
        # Check if reference is valid
        is_resolved = target_path is not None
        is_valid = is_resolved and self._validate_reference(element_info, target_path, ref_type)
        
        # Create reference info
        ref_info = ReferenceInfo(
            source_path=element_info.path,
            target_path=target_path or ref_value,
            reference_type=ref_type,
            dest_attribute=dest,
            is_resolved=is_resolved,
            is_valid=is_valid,
            error_message=None if is_valid else self._get_reference_error(element_info, target_path)
        )
        
        # Store reference
        ref_key = f"{element_info.path}:{ref_value}"
        self.references[ref_key] = ref_info
        
        # Cache by source and target
        if element_info.path not in self._reference_cache:
            self._reference_cache[element_info.path] = []
        self._reference_cache[element_info.path].append(ref_info)
    
    def _determine_reference_type(self, element: ET.Element, dest: str) -> ReferenceType:
        """Determine the type of reference based on element and DEST attribute."""
        tag = element.tag
        if '}' in tag:
            tag = tag.split('}', 1)[1]
        
        if tag == "DEFINITION-REF":
            return ReferenceType.DEFINITION_REF
        elif tag == "VALUE-REF":
            return ReferenceType.VALUE_REF
        elif "ECUC" in tag.upper():
            return ReferenceType.ECUC_REF
        elif dest == "DEST":
            return ReferenceType.PATH_REFERENCE
        else:
            return ReferenceType.UUID_REFERENCE
    
    def _resolve_reference(self, ref_value: str, dest: str, source_path: str) -> Optional[str]:
        """Resolve reference value to target path."""
        if dest == "DEST":
            # Path reference - resolve relative to source
            if ref_value.startswith("/"):
                # Absolute path
                return ref_value
            else:
                # Relative path
                return PathUtils.resolve_reference(ref_value, source_path)
        else:
            # UUID or other reference
            target_element = self.element_index.get_element_by_uuid(ref_value)
            return target_element.path if target_element else None
    
    def _validate_reference(self, source_info: ElementInfo, target_path: str, ref_type: ReferenceType) -> bool:
        """Validate that a reference is semantically correct."""
        if not target_path:
            return False
        
        target_element = self.element_index.get_element_by_path(target_path)
        if not target_element:
            return False
        
        # Type-specific validation
        if ref_type == ReferenceType.DEFINITION_REF:
            return self._validate_definition_ref(source_info, target_element)
        elif ref_type == ReferenceType.VALUE_REF:
            return self._validate_value_ref(source_info, target_element)
        elif ref_type == ReferenceType.ECUC_REF:
            return self._validate_ecuc_ref(source_info, target_element)
        else:
            return True  # Basic path/UUID references are valid if resolved
    
    def _validate_definition_ref(self, source_info: ElementInfo, target_info: ElementInfo) -> bool:
        """Validate definition reference."""
        # Definition references should point to definition elements
        # This is a simplified check - in practice, you'd check against schema
        return target_info.element_type in ["AR-PACKAGE", "ELEMENT", "CONTAINER", "PARAMETER"]
    
    def _validate_value_ref(self, source_info: ElementInfo, target_info: ElementInfo) -> bool:
        """Validate value reference."""
        # Value references should point to value elements
        return target_info.element_type in ["VALUE", "ECUC-TEXTUAL-PARAM-VALUE", 
                                          "ECUC-NUMERICAL-PARAM-VALUE", "ECUC-BOOLEAN-PARAM-VALUE"]
    
    def _validate_ecuc_ref(self, source_info: ElementInfo, target_info: ElementInfo) -> bool:
        """Validate ECUC reference."""
        # ECUC references have specific validation rules
        return "ECUC" in target_info.element_type
    
    def _get_reference_error(self, source_info: ElementInfo, target_path: Optional[str]) -> str:
        """Get error message for invalid reference."""
        if not target_path:
            return "Reference target not found"
        
        target_element = self.element_index.get_element_by_path(target_path)
        if not target_element:
            return f"Referenced element not found: {target_path}"
        
        return "Reference type mismatch"
    
    def get_references_from(self, source_path: str) -> List[ReferenceInfo]:
        """Get all references from a source element."""
        return self._reference_cache.get(source_path, [])
    
    def get_references_to(self, target_path: str) -> List[ReferenceInfo]:
        """Get all references to a target element."""
        references = []
        for ref_info in self.references.values():
            if ref_info.target_path == target_path:
                references.append(ref_info)
        return references
    
    def get_unresolved_references(self) -> List[ReferenceInfo]:
        """Get all unresolved references."""
        return [ref for ref in self.references.values() if not ref.is_resolved]
    
    def get_invalid_references(self) -> List[ReferenceInfo]:
        """Get all invalid references."""
        return [ref for ref in self.references.values() if not ref.is_valid]
    
    def get_reference_statistics(self) -> Dict[str, int]:
        """Get reference statistics."""
        total_refs = len(self.references)
        resolved_refs = len([r for r in self.references.values() if r.is_resolved])
        valid_refs = len([r for r in self.references.values() if r.is_valid])
        
        return {
            "total_references": total_refs,
            "resolved_references": resolved_refs,
            "unresolved_references": total_refs - resolved_refs,
            "valid_references": valid_refs,
            "invalid_references": total_refs - valid_refs
        }
    
    def find_reference_cycles(self) -> List[List[str]]:
        """Find circular references in the model."""
        cycles = []
        visited = set()
        rec_stack = set()
        
        def dfs(node_path: str, path: List[str]) -> None:
            if node_path in rec_stack:
                # Found a cycle
                cycle_start = path.index(node_path)
                cycles.append(path[cycle_start:] + [node_path])
                return
            
            if node_path in visited:
                return
            
            visited.add(node_path)
            rec_stack.add(node_path)
            
            # Check all references from this node
            for ref_info in self.get_references_from(node_path):
                if ref_info.is_resolved:
                    dfs(ref_info.target_path, path + [node_path])
            
            rec_stack.remove(node_path)
        
        for element_info in self.element_index.get_all_elements():
            if element_info.path not in visited:
                dfs(element_info.path, [])
        
        return cycles
    
    def update_reference(self, source_path: str, new_target: str) -> bool:
        """Update a reference to point to a new target."""
        # Find the reference element
        source_element = self.element_index.get_element_by_path(source_path)
        if not source_element or not source_element.is_reference:
            return False
        
        # Update the reference value
        ref_elem = source_element.element
        XMLUtils.set_element_text(ref_elem, new_target)
        
        # Re-analyze this reference
        self._process_reference(source_element)
        
        return True
    
    def create_reference(self, source_path: str, target_path: str, 
                        reference_type: ReferenceType, dest: str = "DEST") -> bool:
        """Create a new reference from source to target."""
        source_element = self.element_index.get_element_by_path(source_path)
        if not source_element:
            return False
        
        # Create reference element
        ref_elem = XMLUtils.create_reference_element(target_path, dest)
        
        # Add to source element
        source_element.element.append(ref_elem)
        
        # Update index and analyze
        self.element_index.update_element(source_path, source_element.element)
        self._process_reference(source_element)
        
        return True
    
    def remove_reference(self, source_path: str, reference_element: ET.Element) -> bool:
        """Remove a reference from source element."""
        source_element_info = self.element_index.get_element_by_path(source_path)
        if not source_element_info:
            return False
        
        # Remove reference element
        source_element_info.element.remove(reference_element)
        
        # Update index
        self.element_index.update_element(source_path, source_element_info.element)
        
        # Re-analyze references
        self.analyze_references()
        
        return True
    
    def get_reference_impact(self, target_path: str) -> List[str]:
        """Get all elements that would be affected by changes to target_path."""
        affected = set()
        
        # Direct references
        for ref_info in self.get_references_to(target_path):
            affected.add(ref_info.source_path)
        
        # Transitive references (references to elements that reference target)
        for ref_info in self.get_references_to(target_path):
            affected.update(self.get_reference_impact(ref_info.source_path))
        
        return list(affected)
    
    def validate_all_references(self) -> List[Tuple[str, str]]:
        """Validate all references and return list of (path, error) tuples."""
        errors = []
        
        for ref_info in self.references.values():
            if not ref_info.is_valid:
                errors.append((ref_info.source_path, ref_info.error_message or "Invalid reference"))
        
        return errors
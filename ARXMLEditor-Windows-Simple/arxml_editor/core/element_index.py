"""
Element index for efficient ARXML element lookup and cross-referencing.

Provides fast access to elements by path, UUID, and other identifiers.
"""

from typing import Dict, List, Optional, Set, Tuple, Any, Callable
from dataclasses import dataclass
from collections import defaultdict
import xml.etree.ElementTree as ET
from ..utils.path_utils import PathUtils
from ..utils.xml_utils import XMLUtils


@dataclass
class ElementInfo:
    """Information about an indexed element."""
    element: ET.Element
    path: str
    short_name: str
    uuid: Optional[str] = None
    parent_path: Optional[str] = None
    element_type: Optional[str] = None
    file_path: Optional[str] = None
    is_reference: bool = False
    reference_dest: Optional[str] = None


class ElementIndex:
    """Index for fast ARXML element lookup and cross-referencing."""
    
    def __init__(self):
        self._by_path: Dict[str, ElementInfo] = {}
        self._by_uuid: Dict[str, ElementInfo] = {}
        self._by_short_name: Dict[str, List[ElementInfo]] = defaultdict(list)
        self._by_type: Dict[str, List[ElementInfo]] = defaultdict(list)
        self._by_file: Dict[str, List[ElementInfo]] = defaultdict(list)
        self._children: Dict[str, List[ElementInfo]] = defaultdict(list)
        self._references: Dict[str, List[ElementInfo]] = defaultdict(list)
        self._referenced_by: Dict[str, List[ElementInfo]] = defaultdict(list)
    
    def add_element(self, element: ET.Element, path: str, file_path: Optional[str] = None) -> ElementInfo:
        """Add element to index."""
        short_name = XMLUtils.get_short_name(element)
        uuid = XMLUtils.get_element_attribute(element, "UUID")
        parent_path = PathUtils.get_parent_path(path)
        element_type = self._get_element_type(element)
        is_reference = XMLUtils.is_reference_element(element)
        reference_dest = None
        
        if is_reference:
            _, reference_dest = XMLUtils.get_reference_value(element)
        
        element_info = ElementInfo(
            element=element,
            path=path,
            short_name=short_name,
            uuid=uuid,
            parent_path=parent_path,
            element_type=element_type,
            file_path=file_path,
            is_reference=is_reference,
            reference_dest=reference_dest
        )
        
        # Index by path
        self._by_path[path] = element_info
        
        # Index by UUID if available
        if uuid:
            self._by_uuid[uuid] = element_info
        
        # Index by short name
        if short_name:
            self._by_short_name[short_name].append(element_info)
        
        # Index by type
        if element_type:
            self._by_type[element_type].append(element_info)
        
        # Index by file
        if file_path:
            self._by_file[file_path].append(element_info)
        
        # Index parent-child relationships
        if parent_path:
            self._children[parent_path].append(element_info)
        
        # Index references
        if is_reference and reference_dest:
            self._references[reference_dest].append(element_info)
        
        return element_info
    
    def remove_element(self, path: str) -> bool:
        """Remove element from index."""
        element_info = self._by_path.get(path)
        if not element_info:
            return False
        
        # Remove from all indexes
        if element_info.uuid and element_info.uuid in self._by_uuid:
            del self._by_uuid[element_info.uuid]
        
        if element_info.short_name and element_info.short_name in self._by_short_name:
            self._by_short_name[element_info.short_name].remove(element_info)
        
        if element_info.element_type and element_info.element_type in self._by_type:
            self._by_type[element_info.element_type].remove(element_info)
        
        if element_info.file_path and element_info.file_path in self._by_file:
            self._by_file[element_info.file_path].remove(element_info)
        
        if element_info.parent_path and element_info.parent_path in self._children:
            self._children[element_info.parent_path].remove(element_info)
        
        if element_info.is_reference and element_info.reference_dest:
            if element_info.reference_dest in self._references:
                self._references[element_info.reference_dest].remove(element_info)
        
        # Remove from main index
        del self._by_path[path]
        
        return True
    
    def get_element_by_path(self, path: str) -> Optional[ElementInfo]:
        """Get element by AUTOSAR path."""
        return self._by_path.get(path)
    
    def get_element_by_uuid(self, uuid: str) -> Optional[ElementInfo]:
        """Get element by UUID."""
        return self._by_uuid.get(uuid)
    
    def get_elements_by_short_name(self, short_name: str) -> List[ElementInfo]:
        """Get all elements with given short name."""
        return self._by_short_name.get(short_name, [])
    
    def get_elements_by_type(self, element_type: str) -> List[ElementInfo]:
        """Get all elements of given type."""
        return self._by_type.get(element_type, [])
    
    def get_elements_by_file(self, file_path: str) -> List[ElementInfo]:
        """Get all elements in given file."""
        return self._by_file.get(file_path, [])
    
    def get_children(self, path: str) -> List[ElementInfo]:
        """Get direct children of element at path."""
        return self._children.get(path, [])
    
    def get_descendants(self, path: str) -> List[ElementInfo]:
        """Get all descendants of element at path."""
        descendants = []
        children = self.get_children(path)
        
        for child in children:
            descendants.append(child)
            descendants.extend(self.get_descendants(child.path))
        
        return descendants
    
    def get_references_to(self, target_path: str) -> List[ElementInfo]:
        """Get all elements that reference the target path."""
        return self._references.get(target_path, [])
    
    def get_referenced_by(self, source_path: str) -> List[ElementInfo]:
        """Get all elements referenced by the source path."""
        return self._referenced_by.get(source_path, [])
    
    def find_elements(self, predicate: Callable[[ElementInfo], bool]) -> List[ElementInfo]:
        """Find elements matching predicate function."""
        return [info for info in self._by_path.values() if predicate(info)]
    
    def search_by_name(self, query: str, case_sensitive: bool = False) -> List[ElementInfo]:
        """Search elements by name (short name or long name)."""
        results = []
        query_lower = query.lower() if not case_sensitive else query
        
        for element_info in self._by_path.values():
            short_name = element_info.short_name
            if not case_sensitive:
                short_name = short_name.lower()
            
            if query_lower in short_name:
                results.append(element_info)
                continue
            
            # Also check long name
            long_name = XMLUtils.get_long_name(element_info.element)
            if not case_sensitive:
                long_name = long_name.lower()
            
            if query_lower in long_name:
                results.append(element_info)
        
        return results
    
    def get_all_paths(self) -> List[str]:
        """Get all indexed paths."""
        return list(self._by_path.keys())
    
    def get_all_elements(self) -> List[ElementInfo]:
        """Get all indexed elements."""
        return list(self._by_path.values())
    
    def clear(self) -> None:
        """Clear all indexes."""
        self._by_path.clear()
        self._by_uuid.clear()
        self._by_short_name.clear()
        self._by_type.clear()
        self._by_file.clear()
        self._children.clear()
        self._references.clear()
        self._referenced_by.clear()
    
    def get_statistics(self) -> Dict[str, int]:
        """Get index statistics."""
        return {
            "total_elements": len(self._by_path),
            "elements_with_uuid": len(self._by_uuid),
            "unique_short_names": len(self._by_short_name),
            "unique_types": len(self._by_type),
            "files": len(self._by_file),
            "reference_relationships": sum(len(refs) for refs in self._references.values())
        }
    
    def _get_element_type(self, element: ET.Element) -> str:
        """Determine element type from tag name."""
        tag = element.tag
        if '}' in tag:
            tag = tag.split('}', 1)[1]
        return tag
    
    def update_element(self, path: str, element: ET.Element) -> bool:
        """Update element in index."""
        element_info = self._by_path.get(path)
        if not element_info:
            return False
        
        # Remove old entry
        self.remove_element(path)
        
        # Add updated entry
        self.add_element(element, path, element_info.file_path)
        
        return True
    
    def get_element_hierarchy(self, root_path: str = "") -> Dict[str, List[ElementInfo]]:
        """Get hierarchical view of elements starting from root path."""
        hierarchy = defaultdict(list)
        
        if not root_path:
            # Get all root elements
            for element_info in self._by_path.values():
                if not element_info.parent_path:
                    hierarchy[""].append(element_info)
        else:
            # Get children of root path
            children = self.get_children(root_path)
            for child in children:
                hierarchy[root_path].append(child)
        
        return dict(hierarchy)
    
    def validate_references(self) -> List[Tuple[str, str]]:
        """Validate all references in the index. Returns list of (reference_path, error_message)."""
        errors = []
        
        for element_info in self._by_path.values():
            if element_info.is_reference:
                ref_value, dest = XMLUtils.get_reference_value(element_info.element)
                if not ref_value:
                    errors.append((element_info.path, "Reference has empty value"))
                    continue
                
                # Check if referenced element exists
                if dest == "DEST":
                    # This is a path reference
                    if ref_value not in self._by_path:
                        errors.append((element_info.path, f"Referenced path not found: {ref_value}"))
                else:
                    # This might be a UUID reference
                    if ref_value not in self._by_uuid:
                        errors.append((element_info.path, f"Referenced UUID not found: {ref_value}"))
        
        return errors
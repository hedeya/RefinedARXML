"""
Path utilities for ARXML processing.

Handles AUTOSAR path resolution, reference management, and file organization.
"""

from typing import List, Optional, Tuple, Dict, Set
from pathlib import Path
import re


class PathUtils:
    """Utilities for ARXML path handling and reference resolution."""
    
    @staticmethod
    def build_autosar_path(element_path: List[str]) -> str:
        """Build AUTOSAR path from element hierarchy."""
        if not element_path:
            return ""
        return "/" + "/".join(element_path)
    
    @staticmethod
    def parse_autosar_path(path: str) -> List[str]:
        """Parse AUTOSAR path into element hierarchy."""
        if not path or path == "/":
            return []
        
        # Remove leading slash and split
        path_parts = path.lstrip("/").split("/")
        return [part for part in path_parts if part]  # Remove empty parts
    
    @staticmethod
    def get_short_name_path(elements: List[dict]) -> str:
        """Build path from SHORT-NAME values of elements."""
        short_names = []
        for elem in elements:
            if 'short_name' in elem and elem['short_name']:
                short_names.append(elem['short_name'])
        return "/" + "/".join(short_names) if short_names else ""
    
    @staticmethod
    def resolve_reference(ref_path: str, base_path: str = "") -> str:
        """Resolve relative reference path against base path."""
        if not ref_path:
            return base_path
        
        if ref_path.startswith("/"):
            # Absolute path
            return ref_path
        
        # Relative path - resolve against base
        if not base_path:
            return "/" + ref_path
        
        base_parts = PathUtils.parse_autosar_path(base_path)
        ref_parts = PathUtils.parse_autosar_path(ref_path)
        
        # Handle ".." in reference path
        resolved_parts = base_parts[:]
        for part in ref_parts:
            if part == "..":
                if resolved_parts:
                    resolved_parts.pop()
            else:
                resolved_parts.append(part)
        
        return PathUtils.build_autosar_path(resolved_parts)
    
    @staticmethod
    def get_parent_path(path: str) -> str:
        """Get parent path of given AUTOSAR path."""
        parts = PathUtils.parse_autosar_path(path)
        if not parts:
            return ""
        return PathUtils.build_autosar_path(parts[:-1])
    
    @staticmethod
    def get_element_name(path: str) -> str:
        """Get element name from AUTOSAR path."""
        parts = PathUtils.parse_autosar_path(path)
        return parts[-1] if parts else ""
    
    @staticmethod
    def is_ancestor_path(ancestor: str, descendant: str) -> bool:
        """Check if ancestor path is parent of descendant path."""
        if not ancestor or not descendant:
            return False
        
        ancestor_parts = PathUtils.parse_autosar_path(ancestor)
        descendant_parts = PathUtils.parse_autosar_path(descendant)
        
        if len(ancestor_parts) >= len(descendant_parts):
            return False
        
        return descendant_parts[:len(ancestor_parts)] == ancestor_parts
    
    @staticmethod
    def get_relative_path(from_path: str, to_path: str) -> str:
        """Get relative path from one path to another."""
        from_parts = PathUtils.parse_autosar_path(from_path)
        to_parts = PathUtils.parse_autosar_path(to_path)
        
        # Find common prefix
        common_length = 0
        for i, (from_part, to_part) in enumerate(zip(from_parts, to_parts)):
            if from_part == to_part:
                common_length = i + 1
            else:
                break
        
        # Build relative path
        up_levels = len(from_parts) - common_length
        relative_parts = [".."] * up_levels + to_parts[common_length:]
        
        return "/".join(relative_parts) if relative_parts else "."
    
    @staticmethod
    def validate_arxml_path(path: str) -> Tuple[bool, Optional[str]]:
        """Validate AUTOSAR path format."""
        if not path:
            return True, None
        
        if not path.startswith("/"):
            return False, "AUTOSAR path must start with '/'"
        
        parts = PathUtils.parse_autosar_path(path)
        for part in parts:
            if not part:
                return False, "AUTOSAR path cannot contain empty segments"
            if not re.match(r'^[A-Za-z][A-Za-z0-9_]*$', part):
                return False, f"Invalid path segment: '{part}' (must start with letter, contain only letters, numbers, underscores)"
        
        return True, None
    
    @staticmethod
    def get_package_hierarchy(path: str) -> List[str]:
        """Get package hierarchy from AUTOSAR path."""
        parts = PathUtils.parse_autosar_path(path)
        hierarchy = []
        
        for i in range(len(parts)):
            hierarchy.append(PathUtils.build_autosar_path(parts[:i+1]))
        
        return hierarchy
    
    @staticmethod
    def find_common_ancestor(paths: List[str]) -> str:
        """Find common ancestor of multiple paths."""
        if not paths:
            return ""
        
        if len(paths) == 1:
            return PathUtils.get_parent_path(paths[0])
        
        # Start with first path
        common_parts = PathUtils.parse_autosar_path(paths[0])
        
        # Compare with other paths
        for path in paths[1:]:
            path_parts = PathUtils.parse_autosar_path(path)
            # Find common prefix
            new_common_length = 0
            for i, (common_part, path_part) in enumerate(zip(common_parts, path_parts)):
                if common_part == path_part:
                    new_common_length = i + 1
                else:
                    break
            common_parts = common_parts[:new_common_length]
        
        return PathUtils.build_autosar_path(common_parts)
    
    @staticmethod
    def normalize_path(path: str) -> str:
        """Normalize AUTOSAR path (remove redundant separators, etc.)."""
        if not path:
            return ""
        
        # Ensure starts with /
        if not path.startswith("/"):
            path = "/" + path
        
        # Remove duplicate slashes
        path = re.sub(r'/+', '/', path)
        
        # Remove trailing slash (except root)
        if path != "/" and path.endswith("/"):
            path = path[:-1]
        
        return path
    
    @staticmethod
    def get_path_depth(path: str) -> int:
        """Get depth of AUTOSAR path."""
        return len(PathUtils.parse_autosar_path(path))
    
    @staticmethod
    def split_path_at_depth(path: str, depth: int) -> Tuple[str, str]:
        """Split path at specified depth, returning (parent, remaining)."""
        parts = PathUtils.parse_autosar_path(path)
        
        if depth <= 0:
            return "", PathUtils.build_autosar_path(parts)
        elif depth >= len(parts):
            return path, ""
        else:
            parent_parts = parts[:depth]
            remaining_parts = parts[depth:]
            return (PathUtils.build_autosar_path(parent_parts), 
                   PathUtils.build_autosar_path(remaining_parts))
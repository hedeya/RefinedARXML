"""
Semantic validation for ARXML files.

Validates business rules and semantic constraints beyond XSD validation.
"""

from typing import List, Set, Dict, Optional
from collections import defaultdict

from .types import ValidationError, ValidationLevel
from ..core.element_index import ElementInfo
from ..core.reference_manager import ReferenceManager
from ..utils.xml_utils import XMLUtils
from ..utils.path_utils import PathUtils


class SemanticValidator:
    """Validates semantic rules and business constraints."""
    
    def __init__(self, element_index, reference_manager):
        self.element_index = element_index
        self.reference_manager = reference_manager
    
    def validate_all(self) -> List[ValidationError]:
        """Validate all semantic rules."""
        errors = []
        
        # Uniqueness validation
        errors.extend(self._validate_uniqueness())
        
        # Reference integrity validation
        errors.extend(self._validate_reference_integrity())
        
        # Structural validation
        errors.extend(self._validate_structure())
        
        # Business rule validation
        errors.extend(self._validate_business_rules())
        
        return errors
    
    def validate_element(self, element_info: ElementInfo) -> List[ValidationError]:
        """Validate semantic rules for specific element."""
        errors = []
        
        # Check uniqueness within scope
        errors.extend(self._validate_element_uniqueness(element_info))
        
        # Check reference validity
        if element_info.is_reference:
            errors.extend(self._validate_element_reference(element_info))
        
        # Check structural constraints
        errors.extend(self._validate_element_structure(element_info))
        
        return errors
    
    def _validate_uniqueness(self) -> List[ValidationError]:
        """Validate uniqueness constraints."""
        errors = []
        
        # Group elements by parent and type
        parent_groups = defaultdict(lambda: defaultdict(list))
        
        for element_info in self.element_index.get_all_elements():
            if element_info.parent_path is not None:
                parent_groups[element_info.parent_path][element_info.element_type].append(element_info)
        
        # Check uniqueness within each group
        for parent_path, type_groups in parent_groups.items():
            for element_type, elements in type_groups.items():
                if element_type in ["SHORT-NAME", "LONG-NAME"]:
                    continue  # Skip metadata elements
                
                # Check SHORT-NAME uniqueness
                short_names = defaultdict(list)
                for element in elements:
                    if element.short_name:
                        short_names[element.short_name].append(element)
                
                for short_name, elements_with_name in short_names.items():
                    if len(elements_with_name) > 1:
                        for element in elements_with_name:
                            errors.append(ValidationError(
                                path=element.path,
                                message=f"Duplicate SHORT-NAME '{short_name}' in {element_type}",
                                level=ValidationLevel.ERROR,
                                rule_id="UNI001"
                            ))
        
        return errors
    
    def _validate_reference_integrity(self) -> List[ValidationError]:
        """Validate reference integrity."""
        errors = []
        
        # Check for unresolved references
        unresolved_refs = self.reference_manager.get_unresolved_references()
        for ref in unresolved_refs:
            errors.append(ValidationError(
                path=ref.source_path,
                message=f"Unresolved reference: {ref.target_path}",
                level=ValidationLevel.ERROR,
                rule_id="REF001"
            ))
        
        # Check for invalid references
        invalid_refs = self.reference_manager.get_invalid_references()
        for ref in invalid_refs:
            errors.append(ValidationError(
                path=ref.source_path,
                message=f"Invalid reference: {ref.error_message}",
                level=ValidationLevel.ERROR,
                rule_id="REF002"
            ))
        
        # Check for circular references
        cycles = self.reference_manager.find_reference_cycles()
        for cycle in cycles:
            errors.append(ValidationError(
                path=cycle[0],
                message=f"Circular reference detected: {' -> '.join(cycle)}",
                level=ValidationLevel.ERROR,
                rule_id="REF003"
            ))
        
        return errors
    
    def _validate_structure(self) -> List[ValidationError]:
        """Validate structural constraints."""
        errors = []
        
        for element_info in self.element_index.get_all_elements():
            # Check required children
            errors.extend(self._validate_required_children(element_info))
            
            # Check element hierarchy
            errors.extend(self._validate_element_hierarchy(element_info))
            
            # Check attribute constraints
            errors.extend(self._validate_attribute_constraints(element_info))
        
        return errors
    
    def _validate_business_rules(self) -> List[ValidationError]:
        """Validate AUTOSAR business rules."""
        errors = []
        
        # ECUC validation
        errors.extend(self._validate_ecuc_rules())
        
        # Package structure validation
        errors.extend(self._validate_package_structure())
        
        # Element type specific validation
        errors.extend(self._validate_element_type_rules())
        
        return errors
    
    def _validate_element_uniqueness(self, element_info: ElementInfo) -> List[ValidationError]:
        """Validate uniqueness for specific element."""
        errors = []
        
        if not element_info.short_name or not element_info.parent_path:
            return errors
        
        # Find siblings with same type
        siblings = self.element_index.get_children(element_info.parent_path)
        same_type_siblings = [s for s in siblings if s.element_type == element_info.element_type and s.path != element_info.path]
        
        # Check for duplicate SHORT-NAME
        for sibling in same_type_siblings:
            if sibling.short_name == element_info.short_name:
                errors.append(ValidationError(
                    path=element_info.path,
                    message=f"Duplicate SHORT-NAME '{element_info.short_name}' in {element_info.element_type}",
                    level=ValidationLevel.ERROR,
                    rule_id="UNI001"
                ))
                break
        
        return errors
    
    def _validate_element_reference(self, element_info: ElementInfo) -> List[ValidationError]:
        """Validate reference element."""
        errors = []
        
        ref_value, dest = XMLUtils.get_reference_value(element_info.element)
        if not ref_value:
            errors.append(ValidationError(
                path=element_info.path,
                message="Reference element has empty value",
                level=ValidationLevel.ERROR,
                rule_id="REF004"
            ))
            return errors
        
        # Check if reference target exists
        if dest == "DEST":
            target_element = self.element_index.get_element_by_path(ref_value)
            if not target_element:
                errors.append(ValidationError(
                    path=element_info.path,
                    message=f"Referenced path not found: {ref_value}",
                    level=ValidationLevel.ERROR,
                    rule_id="REF005"
                ))
        else:
            target_element = self.element_index.get_element_by_uuid(ref_value)
            if not target_element:
                errors.append(ValidationError(
                    path=element_info.path,
                    message=f"Referenced UUID not found: {ref_value}",
                    level=ValidationLevel.ERROR,
                    rule_id="REF006"
                ))
        
        return errors
    
    def _validate_element_structure(self, element_info: ElementInfo) -> List[ValidationError]:
        """Validate element structure."""
        errors = []
        
        # Check for empty elements that should have content
        if not element_info.element.text and len(element_info.element) == 0:
            if element_info.element_type in ["SHORT-NAME", "LONG-NAME", "VALUE"]:
                errors.append(ValidationError(
                    path=element_info.path,
                    message=f"Element {element_info.element_type} should not be empty",
                    level=ValidationLevel.WARNING,
                    rule_id="STR001"
                ))
        
        return errors
    
    def _validate_required_children(self, element_info: ElementInfo) -> List[ValidationError]:
        """Validate required child elements."""
        errors = []
        
        # Define required children for common element types
        required_children = {
            "AR-PACKAGE": ["SHORT-NAME"],
            "ELEMENT": ["SHORT-NAME"],
            "CONTAINER": ["SHORT-NAME"],
            "PARAMETER": ["SHORT-NAME"],
            "REF": []  # REF elements don't require children
        }
        
        element_type = element_info.element_type
        if element_type in required_children:
            required = required_children[element_type]
            present_children = [child.tag.split('}')[-1] for child in element_info.element]
            
            for required_child in required:
                if required_child not in present_children:
                    errors.append(ValidationError(
                        path=element_info.path,
                        message=f"Missing required child element: {required_child}",
                        level=ValidationLevel.ERROR,
                        rule_id="STR002"
                    ))
        
        return errors
    
    def _validate_element_hierarchy(self, element_info: ElementInfo) -> List[ValidationError]:
        """Validate element hierarchy constraints."""
        errors = []
        
        # Check for invalid parent-child relationships
        parent_path = element_info.parent_path
        if parent_path:
            parent_element = self.element_index.get_element_by_path(parent_path)
            if parent_element:
                # Define valid parent-child relationships
                valid_children = {
                    "AUTOSAR": ["AR-PACKAGES"],
                    "AR-PACKAGES": ["AR-PACKAGE"],
                    "AR-PACKAGE": ["SHORT-NAME", "LONG-NAME", "ELEMENTS"],
                    "ELEMENTS": ["ELEMENT"],
                    "ELEMENT": ["SHORT-NAME", "LONG-NAME", "REF", "DEST"]
                }
                
                parent_type = parent_element.element_type
                child_type = element_info.element_type
                
                if parent_type in valid_children:
                    if child_type not in valid_children[parent_type]:
                        errors.append(ValidationError(
                            path=element_info.path,
                            message=f"Invalid parent-child relationship: {parent_type} -> {child_type}",
                            level=ValidationLevel.WARNING,
                            rule_id="STR003"
                        ))
        
        return errors
    
    def _validate_attribute_constraints(self, element_info: ElementInfo) -> List[ValidationError]:
        """Validate attribute constraints."""
        errors = []
        
        # Check for required attributes
        if element_info.element_type == "REF":
            dest = XMLUtils.get_element_attribute(element_info.element, "DEST")
            if not dest:
                errors.append(ValidationError(
                    path=element_info.path,
                    message="REF element missing required DEST attribute",
                    level=ValidationLevel.ERROR,
                    rule_id="ATTR001"
                ))
        
        return errors
    
    def _validate_ecuc_rules(self) -> List[ValidationError]:
        """Validate ECUC-specific rules."""
        errors = []
        
        # Find ECUC elements
        ecuc_elements = self.element_index.get_elements_by_type("ECUC-VALUE-COLLECTION")
        
        for ecuc_element in ecuc_elements:
            # Validate ECUC structure
            errors.extend(self._validate_ecuc_structure(ecuc_element))
        
        return errors
    
    def _validate_ecuc_structure(self, element_info: ElementInfo) -> List[ValidationError]:
        """Validate ECUC element structure."""
        errors = []
        
        # ECUC elements should have proper definition references
        definition_refs = XMLUtils.find_elements_by_tag(element_info.element, "DEFINITION-REF")
        if not definition_refs:
            errors.append(ValidationError(
                path=element_info.path,
                message="ECUC element missing DEFINITION-REF",
                level=ValidationLevel.WARNING,
                rule_id="ECUC001"
            ))
        
        return errors
    
    def _validate_package_structure(self) -> List[ValidationError]:
        """Validate AR package structure."""
        errors = []
        
        # Check for proper package hierarchy
        packages = self.element_index.get_elements_by_type("AR-PACKAGE")
        
        for package in packages:
            # Packages should have ELEMENTS
            elements_container = XMLUtils.find_element_by_tag(package.element, "ELEMENTS")
            if not elements_container:
                errors.append(ValidationError(
                    path=package.path,
                    message="AR-PACKAGE missing ELEMENTS container",
                    level=ValidationLevel.WARNING,
                    rule_id="PKG001"
                ))
        
        return errors
    
    def _validate_element_type_rules(self) -> List[ValidationError]:
        """Validate element type specific rules."""
        errors = []
        
        # Validate different element types
        element_types = ["AR-PACKAGE", "ELEMENT", "CONTAINER", "PARAMETER", "REF"]
        
        for element_type in element_types:
            elements = self.element_index.get_elements_by_type(element_type)
            for element in elements:
                errors.extend(self._validate_specific_element_type(element, element_type))
        
        return errors
    
    def _validate_specific_element_type(self, element_info: ElementInfo, element_type: str) -> List[ValidationError]:
        """Validate specific element type rules."""
        errors = []
        
        if element_type == "REF":
            # REF elements should have both text content and DEST attribute
            ref_value, dest = XMLUtils.get_reference_value(element_info.element)
            if not ref_value:
                errors.append(ValidationError(
                    path=element_info.path,
                    message="REF element missing reference value",
                    level=ValidationLevel.ERROR,
                    rule_id="REF007"
                ))
        
        return errors
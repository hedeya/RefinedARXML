"""
Rule engine for custom ARXML validation rules.

Provides extensible rule-based validation system.
"""

from typing import List, Dict, Any, Callable, Optional
import re

from .types import ValidationError, ValidationLevel, RuleSeverity, ValidationRule
from ..core.element_index import ElementInfo, ElementIndex
from ..core.reference_manager import ReferenceManager
from ..utils.xml_utils import XMLUtils


class RuleEngine:
    """Engine for executing validation rules."""
    
    def __init__(self):
        self.rules: Dict[str, ValidationRule] = {}
        self._register_default_rules()
    
    def _register_default_rules(self) -> None:
        """Register default validation rules."""
        # Naming convention rules
        self.add_rule(ValidationRule(
            rule_id="NAM001",
            name="SHORT-NAME Format",
            description="SHORT-NAME must follow AUTOSAR naming conventions",
            severity=RuleSeverity.ERROR,
            category="Naming",
            validator=self._validate_short_name_format
        ))
        
        self.add_rule(ValidationRule(
            rule_id="NAM002",
            name="Attribute Naming",
            description="Attribute names must follow camelCase convention",
            severity=RuleSeverity.WARNING,
            category="Naming",
            validator=self._validate_attribute_naming
        ))
        
        # Structure rules
        self.add_rule(ValidationRule(
            rule_id="STR001",
            name="Required Elements",
            description="Required child elements must be present",
            severity=RuleSeverity.ERROR,
            category="Structure",
            validator=self._validate_required_elements
        ))
        
        self.add_rule(ValidationRule(
            rule_id="STR002",
            name="Element Hierarchy",
            description="Element hierarchy must follow AUTOSAR conventions",
            severity=RuleSeverity.WARNING,
            category="Structure",
            validator=self._validate_element_hierarchy
        ))
        
        # Reference rules
        self.add_rule(ValidationRule(
            rule_id="REF001",
            name="Reference Resolution",
            description="All references must resolve to valid elements",
            severity=RuleSeverity.ERROR,
            category="References",
            validator=self._validate_reference_resolution
        ))
        
        self.add_rule(ValidationRule(
            rule_id="REF002",
            name="Reference Types",
            description="Reference types must match target element types",
            severity=RuleSeverity.WARNING,
            category="References",
            validator=self._validate_reference_types
        ))
        
        # Content rules
        self.add_rule(ValidationRule(
            rule_id="CONT001",
            name="Empty Elements",
            description="Elements should not be empty unless required",
            severity=RuleSeverity.INFO,
            category="Content",
            validator=self._validate_empty_elements
        ))
        
        self.add_rule(ValidationRule(
            rule_id="CONT002",
            name="Text Content",
            description="Text content should be properly formatted",
            severity=RuleSeverity.INFO,
            category="Content",
            validator=self._validate_text_content
        ))
        
        # ECUC rules
        self.add_rule(ValidationRule(
            rule_id="ECUC001",
            name="ECUC Definition References",
            description="ECUC elements must have valid definition references",
            severity=RuleSeverity.ERROR,
            category="ECUC",
            validator=self._validate_ecuc_definitions
        ))
        
        self.add_rule(ValidationRule(
            rule_id="ECUC002",
            name="ECUC Value Types",
            description="ECUC parameter values must match their definitions",
            severity=RuleSeverity.WARNING,
            category="ECUC",
            validator=self._validate_ecuc_value_types
        ))
    
    def add_rule(self, rule: ValidationRule) -> None:
        """Add a validation rule."""
        self.rules[rule.rule_id] = rule
    
    def remove_rule(self, rule_id: str) -> bool:
        """Remove a validation rule."""
        if rule_id in self.rules:
            del self.rules[rule_id]
            return True
        return False
    
    def enable_rule(self, rule_id: str) -> bool:
        """Enable a validation rule."""
        if rule_id in self.rules:
            self.rules[rule_id].enabled = True
            return True
        return False
    
    def disable_rule(self, rule_id: str) -> bool:
        """Disable a validation rule."""
        if rule_id in self.rules:
            self.rules[rule_id].enabled = False
            return True
        return False
    
    def get_rules(self, category: Optional[str] = None) -> List[ValidationRule]:
        """Get validation rules, optionally filtered by category."""
        rules = list(self.rules.values())
        if category:
            rules = [rule for rule in rules if rule.category == category]
        return rules
    
    def validate_all(self, element_index: ElementIndex, reference_manager: ReferenceManager) -> List[ValidationError]:
        """Validate all elements against all enabled rules."""
        errors = []
        
        for rule in self.rules.values():
            if not rule.enabled:
                continue
            
            rule_errors = self._execute_rule(rule, element_index, reference_manager)
            errors.extend(rule_errors)
        
        return errors
    
    def validate_element(self, element_info: ElementInfo, element_index: ElementIndex, 
                        reference_manager: ReferenceManager) -> List[ValidationError]:
        """Validate specific element against all enabled rules."""
        errors = []
        
        for rule in self.rules.values():
            if not rule.enabled:
                continue
            
            rule_errors = rule.validator(element_info, element_index, reference_manager)
            errors.extend(rule_errors)
        
        return errors
    
    def _execute_rule(self, rule: ValidationRule, element_index: ElementIndex, 
                     reference_manager: ReferenceManager) -> List[ValidationError]:
        """Execute a single rule against all elements."""
        errors = []
        
        for element_info in element_index.get_all_elements():
            rule_errors = rule.validator(element_info, element_index, reference_manager)
            errors.extend(rule_errors)
        
        return errors
    
    # Rule implementations
    
    def _validate_short_name_format(self, element_info: ElementInfo, element_index: ElementIndex, 
                                   reference_manager: ReferenceManager) -> List[ValidationError]:
        """Validate SHORT-NAME format."""
        errors = []
        
        if element_info.element.tag.endswith("SHORT-NAME"):
            short_name = XMLUtils.get_element_text(element_info.element)
            if short_name:
                # Check AUTOSAR naming convention: start with letter, contain only letters, numbers, underscores
                if not re.match(r'^[A-Za-z][A-Za-z0-9_]*$', short_name):
                    errors.append(ValidationError(
                        path=element_info.path,
                        message=f"Invalid SHORT-NAME format: '{short_name}' (must start with letter, contain only letters, numbers, underscores)",
                        level=ValidationLevel.ERROR,
                        rule_id="NAM001"
                    ))
        
        return errors
    
    def _validate_attribute_naming(self, element_info: ElementInfo, element_index: ElementIndex, 
                                 reference_manager: ReferenceManager) -> List[ValidationError]:
        """Validate attribute naming convention."""
        errors = []
        
        for attr_name, attr_value in element_info.element.attrib.items():
            # Skip namespace attributes
            if attr_name.startswith('xmlns') or attr_name.startswith('xsi:'):
                continue
            
            # Check camelCase convention
            if not re.match(r'^[a-z][a-zA-Z0-9]*$', attr_name):
                errors.append(ValidationError(
                    path=element_info.path,
                    message=f"Invalid attribute name format: '{attr_name}' (should be camelCase)",
                    level=ValidationLevel.WARNING,
                    rule_id="NAM002"
                ))
        
        return errors
    
    def _validate_required_elements(self, element_info: ElementInfo, element_index: ElementIndex, 
                                   reference_manager: ReferenceManager) -> List[ValidationError]:
        """Validate required child elements."""
        errors = []
        
        element_type = element_info.element_type
        
        # Define required children for different element types
        required_children = {
            "AR-PACKAGE": ["SHORT-NAME"],
            "ELEMENT": ["SHORT-NAME"],
            "CONTAINER": ["SHORT-NAME"],
            "PARAMETER": ["SHORT-NAME"],
            "ECUC-VALUE-COLLECTION": ["SHORT-NAME"],
            "ECUC-PARAM-CONF-CONTAINER-VALUE": ["SHORT-NAME"]
        }
        
        if element_type in required_children:
            required = required_children[element_type]
            present_children = [child.tag.split('}')[-1] for child in element_info.element]
            
            for required_child in required:
                if required_child not in present_children:
                    errors.append(ValidationError(
                        path=element_info.path,
                        message=f"Missing required child element: {required_child}",
                        level=ValidationLevel.ERROR,
                        rule_id="STR001"
                    ))
        
        return errors
    
    def _validate_element_hierarchy(self, element_info: ElementInfo, element_index: ElementIndex, 
                                   reference_manager: ReferenceManager) -> List[ValidationError]:
        """Validate element hierarchy."""
        errors = []
        
        parent_path = element_info.parent_path
        if not parent_path:
            return errors
        
        parent_element = element_index.get_element_by_path(parent_path)
        if not parent_element:
            return errors
        
        # Define valid parent-child relationships
        valid_children = {
            "AUTOSAR": ["AR-PACKAGES"],
            "AR-PACKAGES": ["AR-PACKAGE"],
            "AR-PACKAGE": ["SHORT-NAME", "LONG-NAME", "ELEMENTS"],
            "ELEMENTS": ["ELEMENT"],
            "ELEMENT": ["SHORT-NAME", "LONG-NAME", "REF", "DEST"],
            "CONTAINER": ["SHORT-NAME", "LONG-NAME", "PARAMETERS", "REFERENCES"],
            "PARAMETER": ["SHORT-NAME", "LONG-NAME", "VALUE"],
            "REF": [],
            "DEST": []
        }
        
        parent_type = parent_element.element_type
        child_type = element_info.element_type
        
        if parent_type in valid_children:
            if child_type not in valid_children[parent_type]:
                errors.append(ValidationError(
                    path=element_info.path,
                    message=f"Invalid parent-child relationship: {parent_type} -> {child_type}",
                    level=ValidationLevel.WARNING,
                    rule_id="STR002"
                ))
        
        return errors
    
    def _validate_reference_resolution(self, element_info: ElementInfo, element_index: ElementIndex, 
                                      reference_manager: ReferenceManager) -> List[ValidationError]:
        """Validate reference resolution."""
        errors = []
        
        if element_info.is_reference:
            ref_value, dest = XMLUtils.get_reference_value(element_info.element)
            if ref_value:
                # Check if reference resolves
                if dest == "DEST":
                    target_element = element_index.get_element_by_path(ref_value)
                    if not target_element:
                        errors.append(ValidationError(
                            path=element_info.path,
                            message=f"Unresolved reference: {ref_value}",
                            level=ValidationLevel.ERROR,
                            rule_id="REF001"
                        ))
                else:
                    target_element = element_index.get_element_by_uuid(ref_value)
                    if not target_element:
                        errors.append(ValidationError(
                            path=element_info.path,
                            message=f"Unresolved UUID reference: {ref_value}",
                            level=ValidationLevel.ERROR,
                            rule_id="REF001"
                        ))
        
        return errors
    
    def _validate_reference_types(self, element_info: ElementInfo, element_index: ElementIndex, 
                                 reference_manager: ReferenceManager) -> List[ValidationError]:
        """Validate reference types."""
        errors = []
        
        if element_info.is_reference:
            ref_value, dest = XMLUtils.get_reference_value(element_info.element)
            if ref_value:
                # Find target element
                target_element = None
                if dest == "DEST":
                    target_element = element_index.get_element_by_path(ref_value)
                else:
                    target_element = element_index.get_element_by_uuid(ref_value)
                
                if target_element:
                    # Check if reference type matches target type
                    ref_type = element_info.element.tag
                    target_type = target_element.element_type
                    
                    # Define valid reference-target type combinations
                    valid_combinations = {
                        "DEFINITION-REF": ["AR-PACKAGE", "ELEMENT", "CONTAINER", "PARAMETER"],
                        "VALUE-REF": ["VALUE", "ECUC-TEXTUAL-PARAM-VALUE", "ECUC-NUMERICAL-PARAM-VALUE"],
                        "REF": ["ELEMENT", "CONTAINER", "PARAMETER"]
                    }
                    
                    if ref_type in valid_combinations:
                        if target_type not in valid_combinations[ref_type]:
                            errors.append(ValidationError(
                                path=element_info.path,
                                message=f"Reference type mismatch: {ref_type} -> {target_type}",
                                level=ValidationLevel.WARNING,
                                rule_id="REF002"
                            ))
        
        return errors
    
    def _validate_empty_elements(self, element_info: ElementInfo, element_index: ElementIndex, 
                                reference_manager: ReferenceManager) -> List[ValidationError]:
        """Validate empty elements."""
        errors = []
        
        # Check for empty elements that should have content
        if not element_info.element.text and len(element_info.element) == 0:
            element_type = element_info.element_type
            
            # Some elements are allowed to be empty
            empty_allowed = ["REF", "DEST", "LONG-NAME"]
            
            if element_type not in empty_allowed:
                errors.append(ValidationError(
                    path=element_info.path,
                    message=f"Element {element_type} is empty",
                    level=ValidationLevel.INFO,
                    rule_id="CONT001"
                ))
        
        return errors
    
    def _validate_text_content(self, element_info: ElementInfo, element_index: ElementIndex, 
                              reference_manager: ReferenceManager) -> List[ValidationError]:
        """Validate text content formatting."""
        errors = []
        
        text = element_info.element.text
        if text:
            # Check for leading/trailing whitespace
            if text != text.strip():
                errors.append(ValidationError(
                    path=element_info.path,
                    message="Text content has leading or trailing whitespace",
                    level=ValidationLevel.INFO,
                    rule_id="CONT002"
                ))
            
            # Check for excessive whitespace
            if '  ' in text:  # Multiple consecutive spaces
                errors.append(ValidationError(
                    path=element_info.path,
                    message="Text content contains excessive whitespace",
                    level=ValidationLevel.INFO,
                    rule_id="CONT002"
                ))
        
        return errors
    
    def _validate_ecuc_definitions(self, element_info: ElementInfo, element_index: ElementIndex, 
                                  reference_manager: ReferenceManager) -> List[ValidationError]:
        """Validate ECUC definition references."""
        errors = []
        
        if "ECUC" in element_info.element_type:
            # Check for DEFINITION-REF
            definition_refs = XMLUtils.find_elements_by_tag(element_info.element, "DEFINITION-REF")
            if not definition_refs:
                errors.append(ValidationError(
                    path=element_info.path,
                    message="ECUC element missing DEFINITION-REF",
                    level=ValidationLevel.ERROR,
                    rule_id="ECUC001"
                ))
            else:
                # Validate definition reference
                for def_ref in definition_refs:
                    ref_value, dest = XMLUtils.get_reference_value(def_ref)
                    if ref_value:
                        target_element = element_index.get_element_by_path(ref_value)
                        if not target_element:
                            errors.append(ValidationError(
                                path=element_info.path,
                                message=f"ECUC DEFINITION-REF not found: {ref_value}",
                                level=ValidationLevel.ERROR,
                                rule_id="ECUC001"
                            ))
        
        return errors
    
    def _validate_ecuc_value_types(self, element_info: ElementInfo, element_index: ElementIndex, 
                                  reference_manager: ReferenceManager) -> List[ValidationError]:
        """Validate ECUC value types."""
        errors = []
        
        if element_info.element_type in ["ECUC-TEXTUAL-PARAM-VALUE", "ECUC-NUMERICAL-PARAM-VALUE", 
                                        "ECUC-BOOLEAN-PARAM-VALUE", "ECUC-ENUMERATION-PARAM-VALUE"]:
            # Check if value matches expected type
            value_elem = XMLUtils.find_element_by_tag(element_info.element, "VALUE")
            if value_elem:
                value_text = XMLUtils.get_element_text(value_elem)
                element_type = element_info.element_type
                
                if element_type == "ECUC-NUMERICAL-PARAM-VALUE":
                    try:
                        float(value_text)
                    except ValueError:
                        errors.append(ValidationError(
                            path=element_info.path,
                            message=f"ECUC numerical value is not a valid number: {value_text}",
                            level=ValidationLevel.WARNING,
                            rule_id="ECUC002"
                        ))
                elif element_type == "ECUC-BOOLEAN-PARAM-VALUE":
                    if value_text.lower() not in ["true", "false"]:
                        errors.append(ValidationError(
                            path=element_info.path,
                            message=f"ECUC boolean value must be 'true' or 'false': {value_text}",
                            level=ValidationLevel.WARNING,
                            rule_id="ECUC002"
                        ))
        
        return errors
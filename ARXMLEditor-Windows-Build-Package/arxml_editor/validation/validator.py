"""
Main ARXML validator coordinating XSD and semantic validation.

Provides unified validation interface with error reporting and quick fixes.
"""

from typing import Dict, List, Optional, Tuple, Any, Callable
import xml.etree.ElementTree as ET

from .types import ValidationError, ValidationLevel
from .xsd_validator import XSDValidator
from .semantic_validator import SemanticValidator
from .rule_engine import RuleEngine
from ..core.schema_manager import AUTOSARRelease
from ..core.element_index import ElementInfo


class ARXMLValidator:
    """Main validator coordinating all validation activities."""
    
    def __init__(self, schema_manager, element_index, reference_manager):
        self.schema_manager = schema_manager
        self.element_index = element_index
        self.reference_manager = reference_manager
        
        self.xsd_validator = XSDValidator(schema_manager)
        self.semantic_validator = SemanticValidator(element_index, reference_manager)
        self.rule_engine = RuleEngine()
        
        self._validation_cache: Dict[str, List[ValidationError]] = {}
        self._last_validation_time = 0.0
    
    def validate_all(self, force_refresh: bool = False) -> List[ValidationError]:
        """Validate entire model and return all errors."""
        cache_key = "all"
        
        if not force_refresh and cache_key in self._validation_cache:
            return self._validation_cache[cache_key]
        
        errors = []
        
        # XSD validation
        xsd_errors = self.xsd_validator.validate_all()
        errors.extend(xsd_errors)
        
        # Semantic validation
        semantic_errors = self.semantic_validator.validate_all()
        errors.extend(semantic_errors)
        
        # Rule-based validation
        rule_errors = self.rule_engine.validate_all(self.element_index, self.reference_manager)
        errors.extend(rule_errors)
        
        # Cache results
        self._validation_cache[cache_key] = errors
        self._last_validation_time = self._get_current_time()
        
        return errors
    
    def validate_element(self, path: str) -> List[ValidationError]:
        """Validate specific element."""
        element_info = self.element_index.get_element_by_path(path)
        if not element_info:
            return [ValidationError(
                path=path,
                message="Element not found",
                level=ValidationLevel.ERROR
            )]
        
        errors = []
        
        # XSD validation for element
        xsd_errors = self.xsd_validator.validate_element(element_info)
        errors.extend(xsd_errors)
        
        # Semantic validation for element
        semantic_errors = self.semantic_validator.validate_element(element_info)
        errors.extend(semantic_errors)
        
        # Rule-based validation for element
        rule_errors = self.rule_engine.validate_element(element_info, self.element_index, self.reference_manager)
        errors.extend(rule_errors)
        
        return errors
    
    def validate_file(self, file_path: str) -> List[ValidationError]:
        """Validate specific file."""
        errors = []
        
        # Get file elements
        file_elements = self.element_index.get_elements_by_file(file_path)
        
        for element_info in file_elements:
            element_errors = self.validate_element(element_info.path)
            errors.extend(element_errors)
        
        return errors
    
    def get_errors_by_level(self, level: ValidationLevel) -> List[ValidationError]:
        """Get errors filtered by severity level."""
        all_errors = self.validate_all()
        return [error for error in all_errors if error.level == level]
    
    def get_errors_by_path(self, path: str) -> List[ValidationError]:
        """Get errors for specific path."""
        all_errors = self.validate_all()
        return [error for error in all_errors if error.path == path]
    
    def get_error_summary(self) -> Dict[str, int]:
        """Get summary of errors by level."""
        all_errors = self.validate_all()
        summary = {
            "total": len(all_errors),
            "errors": len([e for e in all_errors if e.level == ValidationLevel.ERROR]),
            "warnings": len([e for e in all_errors if e.level == ValidationLevel.WARNING]),
            "info": len([e for e in all_errors if e.level == ValidationLevel.INFO])
        }
        return summary
    
    def apply_quick_fix(self, error: ValidationError) -> bool:
        """Apply quick fix for validation error."""
        if not error.quick_fix:
            return False
        
        try:
            error.quick_fix()
            # Clear cache to force revalidation
            self._validation_cache.clear()
            return True
        except Exception as e:
            print(f"Quick fix failed: {e}")
            return False
    
    def get_quick_fixes(self, path: str) -> List[ValidationError]:
        """Get all errors with quick fixes for a path."""
        errors = self.get_errors_by_path(path)
        return [error for error in errors if error.quick_fix is not None]
    
    def validate_references(self) -> List[ValidationError]:
        """Validate all references in the model."""
        errors = []
        
        # Check for unresolved references
        unresolved = self.reference_manager.get_unresolved_references()
        for ref in unresolved:
            errors.append(ValidationError(
                path=ref.source_path,
                message=f"Unresolved reference: {ref.target_path}",
                level=ValidationLevel.ERROR,
                rule_id="REF001"
            ))
        
        # Check for invalid references
        invalid = self.reference_manager.get_invalid_references()
        for ref in invalid:
            errors.append(ValidationError(
                path=ref.source_path,
                message=f"Invalid reference: {ref.error_message}",
                level=ValidationLevel.ERROR,
                rule_id="REF002"
            ))
        
        # Check for reference cycles
        cycles = self.reference_manager.find_reference_cycles()
        for cycle in cycles:
            errors.append(ValidationError(
                path=cycle[0],
                message=f"Circular reference detected: {' -> '.join(cycle)}",
                level=ValidationLevel.ERROR,
                rule_id="REF003"
            ))
        
        return errors
    
    def validate_naming_conventions(self) -> List[ValidationError]:
        """Validate ARXML naming conventions."""
        errors = []
        
        for element_info in self.element_index.get_all_elements():
            # Validate tag names
            tag_name = element_info.element.tag
            if '}' in tag_name:
                tag_name = tag_name.split('}', 1)[1]
            
            # Skip validation for standard XML elements
            if tag_name in ['AUTOSAR', 'AR-PACKAGES', 'ELEMENTS']:
                continue
            
            # Validate SHORT-NAME
            short_name = element_info.short_name
            if short_name:
                from ..utils.naming_conventions import ARXMLNamingConventions
                naming = ARXMLNamingConventions()
                is_valid, error_msg = naming.validate_short_name(short_name)
                if not is_valid:
                    errors.append(ValidationError(
                        path=element_info.path,
                        message=f"Invalid SHORT-NAME: {error_msg}",
                        level=ValidationLevel.ERROR,
                        rule_id="NAM001"
                    ))
            
            # Validate attributes
            for attr_name, attr_value in element_info.element.attrib.items():
                if attr_name.startswith('xmlns') or attr_name.startswith('xsi:'):
                    continue  # Skip namespace attributes
                
                from ..utils.naming_conventions import ARXMLNamingConventions
                naming = ARXMLNamingConventions()
                is_valid, error_msg = naming.validate_attribute_name(attr_name)
                if not is_valid:
                    errors.append(ValidationError(
                        path=element_info.path,
                        message=f"Invalid attribute name '{attr_name}': {error_msg}",
                        level=ValidationLevel.ERROR,
                        rule_id="NAM002"
                    ))
        
        return errors
    
    def clear_cache(self) -> None:
        """Clear validation cache."""
        self._validation_cache.clear()
    
    def _get_current_time(self) -> float:
        """Get current time for cache management."""
        import time
        return time.time()
    
    def is_cache_valid(self, max_age_seconds: float = 5.0) -> bool:
        """Check if validation cache is still valid."""
        current_time = self._get_current_time()
        return (current_time - self._last_validation_time) < max_age_seconds
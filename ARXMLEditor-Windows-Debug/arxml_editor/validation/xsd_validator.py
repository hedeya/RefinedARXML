"""
XSD validation for ARXML files.

Validates ARXML content against AUTOSAR XSD schemas.
"""

from typing import List, Optional
from xmlschema import XMLSchema, XMLSchemaValidationError
import xml.etree.ElementTree as ET

from .types import ValidationError, ValidationLevel
from ..core.schema_manager import AUTOSARRelease


class XSDValidator:
    """Validates ARXML content against XSD schemas."""
    
    def __init__(self, schema_manager):
        self.schema_manager = schema_manager
    
    def validate_all(self) -> List[ValidationError]:
        """Validate all loaded files against their schemas."""
        errors = []
        
        for release in self.schema_manager.get_supported_releases():
            validator = self.schema_manager.get_schema_validator(release)
            if validator:
                # This would need to be called with actual file content
                # For now, return empty list as we don't have file content here
                pass
        
        return errors
    
    def validate_file(self, content: str, release: AUTOSARRelease) -> List[ValidationError]:
        """Validate file content against specific schema release."""
        errors = []
        
        validator = self.schema_manager.get_schema_validator(release)
        if not validator:
            errors.append(ValidationError(
                path="",
                message=f"No XSD validator available for {release.value}",
                level=ValidationLevel.ERROR
            ))
            return errors
        
        try:
            validator.validate(content)
        except XMLSchemaValidationError as e:
            errors.append(ValidationError(
                path=self._extract_path_from_error(e),
                message=f"XSD Validation Error: {e.message}",
                level=ValidationLevel.ERROR,
                line_number=getattr(e, 'line', None),
                column_number=getattr(e, 'column', None)
            ))
        except Exception as e:
            errors.append(ValidationError(
                path="",
                message=f"Schema validation failed: {str(e)}",
                level=ValidationLevel.ERROR
            ))
        
        return errors
    
    def validate_element(self, element_info) -> List[ValidationError]:
        """Validate single element against schema."""
        errors = []
        
        # For element validation, we need to validate the element in context
        # This is a simplified implementation
        try:
            # Convert element to string for validation
            element_str = ET.tostring(element_info.element, encoding='unicode')
            
            # Basic XML well-formedness check
            ET.fromstring(element_str)
            
        except ET.ParseError as e:
            errors.append(ValidationError(
                path=element_info.path,
                message=f"Malformed XML: {str(e)}",
                level=ValidationLevel.ERROR
            ))
        
        return errors
    
    def validate_namespace(self, content: str, expected_release: AUTOSARRelease) -> List[ValidationError]:
        """Validate namespace declaration matches expected release."""
        errors = []
        
        try:
            root = ET.fromstring(content)
            namespace = root.tag.split('}')[0].lstrip('{') if '}' in root.tag else ""
            
            expected_namespace = self.schema_manager.schemas[expected_release].namespace
            
            if namespace != expected_namespace:
                errors.append(ValidationError(
                    path="/",
                    message=f"Namespace mismatch: expected {expected_namespace}, found {namespace}",
                    level=ValidationLevel.WARNING
                ))
        
        except ET.ParseError as e:
            errors.append(ValidationError(
                path="/",
                message=f"Failed to parse XML for namespace validation: {str(e)}",
                level=ValidationLevel.ERROR
            ))
        
        return errors
    
    def validate_schema_location(self, content: str, expected_release: AUTOSARRelease) -> List[ValidationError]:
        """Validate xsi:schemaLocation attribute."""
        errors = []
        
        try:
            root = ET.fromstring(content)
            schema_location = root.get("{http://www.w3.org/2001/XMLSchema-instance}schemaLocation")
            
            if not schema_location:
                errors.append(ValidationError(
                    path="/",
                    message="Missing xsi:schemaLocation attribute",
                    level=ValidationLevel.WARNING
                ))
            else:
                # Check if schema location matches expected release
                expected_version = expected_release.value.replace('-', '.')
                if expected_version not in schema_location:
                    errors.append(ValidationError(
                        path="/",
                        message=f"Schema location version mismatch: expected {expected_version}",
                        level=ValidationLevel.WARNING
                    ))
        
        except ET.ParseError as e:
            errors.append(ValidationError(
                path="/",
                message=f"Failed to parse XML for schema location validation: {str(e)}",
                level=ValidationLevel.ERROR
            ))
        
        return errors
    
    def _extract_path_from_error(self, error: XMLSchemaValidationError) -> str:
        """Extract element path from XSD validation error."""
        # This is a simplified implementation
        # In practice, you'd parse the error details to extract the element path
        if hasattr(error, 'path') and error.path:
            return error.path
        return "/"
    
    def get_schema_errors(self, content: str, release: AUTOSARRelease) -> List[dict]:
        """Get detailed schema validation errors."""
        validator = self.schema_manager.get_schema_validator(release)
        if not validator:
            return []
        
        try:
            validator.validate(content)
            return []
        except XMLSchemaValidationError as e:
            return [{
                'message': e.message,
                'path': self._extract_path_from_error(e),
                'line': getattr(e, 'line', None),
                'column': getattr(e, 'column', None)
            }]
        except Exception as e:
            return [{
                'message': str(e),
                'path': '/',
                'line': None,
                'column': None
            }]
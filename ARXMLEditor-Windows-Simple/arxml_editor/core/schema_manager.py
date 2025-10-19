"""
Schema management for multiple AUTOSAR releases.

Handles schema version detection, validation, and cross-version compatibility.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
from enum import Enum
from dataclasses import dataclass
import xml.etree.ElementTree as ET
from xmlschema import XMLSchema, XMLSchemaValidationError

from ..utils.naming_conventions import ARXMLNamingConventions


class AUTOSARRelease(Enum):
    """Supported AUTOSAR releases."""
    R20_11 = "R20-11"
    R21_11 = "R21-11" 
    R22_11 = "R22-11"
    R24_11 = "R24-11"


@dataclass
class SchemaInfo:
    """Information about an ARXML schema."""
    release: AUTOSARRelease
    namespace: str
    schema_path: Optional[Path]
    xsd_validator: Optional[XMLSchema]
    serialization_rules: Dict[str, str]


class SchemaManager:
    """Manages AUTOSAR schema versions and validation."""
    
    def __init__(self, schema_dir: Optional[Path] = None):
        self.schema_dir = schema_dir or Path(__file__).parent / "schemas"
        self.schemas: Dict[AUTOSARRelease, SchemaInfo] = {}
        self.naming_conventions = ARXMLNamingConventions()
        self._load_schemas()
    
    def _load_schemas(self) -> None:
        """Load available schemas from the schema directory."""
        schema_mappings = {
            AUTOSARRelease.R20_11: {
                "namespace": "http://autosar.org/schema/r4.0",
                "schema_file": "AUTOSAR_4-0-0.xsd"
            },
            AUTOSARRelease.R21_11: {
                "namespace": "http://autosar.org/schema/r4.1", 
                "schema_file": "AUTOSAR_4-1-0.xsd"
            },
            AUTOSARRelease.R22_11: {
                "namespace": "http://autosar.org/schema/r4.2",
                "schema_file": "AUTOSAR_4-2-0.xsd"
            },
            AUTOSARRelease.R24_11: {
                "namespace": "http://autosar.org/schema/r4.4",
                "schema_file": "AUTOSAR_4-4-0.xsd"
            }
        }
        
        for release, config in schema_mappings.items():
            schema_path = self.schema_dir / config["schema_file"]
            xsd_validator = None
            
            if schema_path.exists():
                try:
                    xsd_validator = XMLSchema(str(schema_path))
                except Exception as e:
                    print(f"Warning: Could not load schema for {release.value}: {e}")
            
            self.schemas[release] = SchemaInfo(
                release=release,
                namespace=config["namespace"],
                schema_path=schema_path if schema_path.exists() else None,
                xsd_validator=xsd_validator,
                serialization_rules=self._get_serialization_rules(release)
            )
    
    def _get_serialization_rules(self, release: AUTOSARRelease) -> Dict[str, str]:
        """Get serialization rules for a specific AUTOSAR release."""
        # Base rules that apply across releases
        rules = {
            "tag_naming": "UPPERCASE-HYPHENATED",
            "attribute_naming": "camelCase", 
            "indentation": "2 spaces",
            "root_element": "AUTOSAR",
            "file_extension": ".arxml"
        }
        
        # Release-specific customizations
        if release in [AUTOSARRelease.R24_11]:
            rules["namespace_version"] = "4.4"
        elif release in [AUTOSARRelease.R22_11]:
            rules["namespace_version"] = "4.2"
        elif release in [AUTOSARRelease.R21_11]:
            rules["namespace_version"] = "4.1"
        else:
            rules["namespace_version"] = "4.0"
            
        return rules
    
    def detect_schema_version(self, arxml_content: str) -> Optional[AUTOSARRelease]:
        """Detect AUTOSAR release from ARXML content."""
        try:
            root = ET.fromstring(arxml_content)
            
            # Check namespace
            namespace = root.tag.split('}')[0].lstrip('{') if '}' in root.tag else ""
            
            for release, schema_info in self.schemas.items():
                if schema_info.namespace in namespace:
                    return release
            
            # Fallback: check xsi:schemaLocation
            schema_location = root.get("{http://www.w3.org/2001/XMLSchema-instance}schemaLocation")
            if schema_location:
                for release, schema_info in self.schemas.items():
                    if release.value.replace("-", ".") in schema_location:
                        return release
                        
        except ET.ParseError:
            pass
            
        return None
    
    def get_schema_validator(self, release: AUTOSARRelease) -> Optional[XMLSchema]:
        """Get XSD validator for a specific release."""
        schema_info = self.schemas.get(release)
        return schema_info.xsd_validator if schema_info else None
    
    def validate_xsd(self, arxml_content: str, release: AUTOSARRelease) -> List[str]:
        """Validate ARXML content against XSD schema."""
        validator = self.get_schema_validator(release)
        if not validator:
            return [f"No XSD validator available for {release.value}"]
        
        try:
            validator.validate(arxml_content)
            return []
        except XMLSchemaValidationError as e:
            return [f"XSD Validation Error: {e.message}"]
        except Exception as e:
            return [f"Schema validation failed: {str(e)}"]
    
    def get_serialization_rules(self, release: AUTOSARRelease) -> Dict[str, str]:
        """Get serialization rules for a release."""
        schema_info = self.schemas.get(release)
        return schema_info.serialization_rules if schema_info else {}
    
    def get_supported_releases(self) -> List[AUTOSARRelease]:
        """Get list of supported AUTOSAR releases."""
        return list(self.schemas.keys())
    
    def can_convert_to(self, source_release: AUTOSARRelease, target_release: AUTOSARRelease) -> bool:
        """Check if conversion between releases is supported."""
        # For now, allow conversion between any supported releases
        # In a full implementation, this would check compatibility matrix
        return (source_release in self.schemas and 
                target_release in self.schemas and
                source_release != target_release)
    
    def convert_element_name(self, name: str, source_release: AUTOSARRelease, 
                           target_release: AUTOSARRelease) -> str:
        """Convert element name between releases if needed."""
        # Most element names are stable across releases
        # This is where release-specific naming changes would be handled
        return name
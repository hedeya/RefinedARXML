"""Core ARXML processing modules."""

from .arxml_model import ARXMLModel
from .schema_manager import SchemaManager
from .reference_manager import ReferenceManager
from .element_index import ElementIndex

__all__ = ["ARXMLModel", "SchemaManager", "ReferenceManager", "ElementIndex"]
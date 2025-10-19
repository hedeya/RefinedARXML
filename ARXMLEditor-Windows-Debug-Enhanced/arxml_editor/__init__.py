"""
ARXML Editor - Professional AUTOSAR XML Editor

A comprehensive GUI editor for ARXML files with advanced validation,
cross-reference management, and visual diagram support.
"""

__version__ = "0.1.0"
__author__ = "ARXML Editor Team"

from .core.arxml_model import ARXMLModel
from .core.schema_manager import SchemaManager
from .core.reference_manager import ReferenceManager
from .validation.validator import ARXMLValidator
from .ui.main_window import MainWindow

__all__ = [
    "ARXMLModel",
    "SchemaManager", 
    "ReferenceManager",
    "ARXMLValidator",
    "MainWindow"
]
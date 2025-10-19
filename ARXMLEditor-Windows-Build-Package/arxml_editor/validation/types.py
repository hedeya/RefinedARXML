"""
Validation types and data structures.

Contains validation-related types, enums, and data classes to avoid circular imports.
"""

from typing import Optional, Callable, Any, List
from dataclasses import dataclass
from enum import Enum


class ValidationLevel(Enum):
    """Validation severity levels."""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class ValidationError:
    """Represents a validation error."""
    path: str
    message: str
    level: ValidationLevel = ValidationLevel.ERROR
    rule_id: Optional[str] = None
    line_number: Optional[int] = None
    column_number: Optional[int] = None
    quick_fix: Optional[Callable] = None
    context: Optional[Any] = None
    
    def __str__(self) -> str:
        return f"{self.level.value.upper()}: {self.path} - {self.message}"
    
    def __repr__(self) -> str:
        return f"ValidationError(path='{self.path}', message='{self.message}', level={self.level})"


class RuleSeverity(Enum):
    """Rule severity levels."""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    HINT = "hint"


@dataclass
class ValidationRule:
    """Represents a validation rule."""
    rule_id: str
    name: str
    description: str
    severity: RuleSeverity
    category: str
    validator: Callable[[Any, Any, Any], List[ValidationError]]
    
    def __str__(self) -> str:
        return f"{self.rule_id}: {self.name}"
    
    def __repr__(self) -> str:
        return f"ValidationRule(rule_id='{self.rule_id}', name='{self.name}')"
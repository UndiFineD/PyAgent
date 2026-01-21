# Copyright (c) 2026 PyAgent Authors. All rights reserved.
import json
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Pattern, Type
from .enums import ConstraintType, SchemaFormat

@dataclass
class OutputConstraint:
    """Base output constraint."""
    constraint_type: ConstraintType = ConstraintType.INCLUDE
    priority: int = 0
    
    def validate(self, text: str) -> bool:
        """Validate text against constraint."""
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "constraint_type": self.constraint_type.name,
            "priority": self.priority,
        }

@dataclass
class JsonSchemaConstraint(OutputConstraint):
    """JSON Schema constraint."""
    schema: Dict[str, Any] = field(default_factory=dict)
    schema_format: SchemaFormat = SchemaFormat.DRAFT_07
    strict: bool = True
    allow_partial: bool = False
    
    def validate(self, text: str) -> bool:
        """Validate text as JSON against schema."""
        try:
            data = json.loads(text)
            return self._validate_schema(data)
        except json.JSONDecodeError:
            return self.allow_partial
    
    def _validate_schema(self, data: Any) -> bool:
        """Basic schema validation (simplified)."""
        if not self.schema:
            return True
        
        schema_type = self.schema.get("type")
        
        if schema_type == "object":
            if not isinstance(data, dict):
                return False
            
            # Check required properties
            required = self.schema.get("required", [])
            for req in required:
                if req not in data:
                    return False
            
            # Check properties
            properties = self.schema.get("properties", {})
            for key, prop_schema in properties.items():
                if key in data:
                    if not self._validate_property(data[key], prop_schema):
                        return False
            
            return True
        
        elif schema_type == "array":
            if not isinstance(data, list):
                return False
            
            items_schema = self.schema.get("items")
            if items_schema:
                for item in data:
                    if not self._validate_property(item, items_schema):
                        return False
            
            return True
        
        elif schema_type == "string":
            return isinstance(data, str)
        
        elif schema_type == "number":
            return isinstance(data, (int, float))
        
        elif schema_type == "integer":
            return isinstance(data, int)
        
        elif schema_type == "boolean":
            return isinstance(data, bool)
        
        elif schema_type == "null":
            return data is None
        
        return True
    
    def _validate_property(
        self,
        value: Any,
        prop_schema: Dict[str, Any],
    ) -> bool:
        """Validate a property against its schema."""
        prop_type = prop_schema.get("type")
        
        if prop_type == "string":
            if not isinstance(value, str):
                return False
            
            pattern = prop_schema.get("pattern")
            if pattern and not re.match(pattern, value):
                return False
            
            enum = prop_schema.get("enum")
            if enum and value not in enum:
                return False
            
        elif prop_type == "number":
            if not isinstance(value, (int, float)):
                return False
            
            minimum = prop_schema.get("minimum")
            if minimum is not None and value < minimum:
                return False
            
            maximum = prop_schema.get("maximum")
            if maximum is not None and value > maximum:
                return False
            
        elif prop_type == "integer":
            if not isinstance(value, int):
                return False
            
        elif prop_type == "boolean":
            if not isinstance(value, bool):
                return False
            
        elif prop_type == "array":
            if not isinstance(value, list):
                return False
            
        elif prop_type == "object":
            if not isinstance(value, dict):
                return False
        
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            **super().to_dict(),
            "schema": self.schema,
            "schema_format": self.schema_format.value,
            "strict": self.strict,
        }

@dataclass
class RegexConstraint(OutputConstraint):
    """Regex pattern constraint."""
    pattern: str = ""
    flags: int = 0
    _compiled: Optional[Pattern] = field(default=None, repr=False)
    
    def __post_init__(self):
        if self.pattern and self._compiled is None:
            self._compiled = re.compile(self.pattern, self.flags)
    
    def validate(self, text: str) -> bool:
        if self._compiled is None:
            return True
        
        if self.constraint_type == ConstraintType.INCLUDE:
            return bool(self._compiled.match(text))
        else:
            return not bool(self._compiled.match(text))
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            **super().to_dict(),
            "pattern": self.pattern,
            "flags": self.flags,
        }

@dataclass
class ChoiceConstraint(OutputConstraint):
    """Fixed choice constraint."""
    choices: List[str] = field(default_factory=list)
    case_sensitive: bool = True
    
    def validate(self, text: str) -> bool:
        if self.case_sensitive:
            return text in self.choices
        return text.lower() in [c.lower() for c in self.choices]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            **super().to_dict(),
            "choices": self.choices,
            "case_sensitive": self.case_sensitive,
        }

@dataclass
class GrammarConstraint(OutputConstraint):
    """Grammar constraint (EBNF/Lark)."""
    grammar: str = ""
    grammar_type: str = "ebnf"  # "ebnf", "lark", "gbnf"
    start_symbol: str = "start"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            **super().to_dict(),
            "grammar": self.grammar,
            "grammar_type": self.grammar_type,
            "start_symbol": self.start_symbol,
        }

@dataclass
class TypeConstraint(OutputConstraint):
    """Type annotation constraint."""
    type_annotation: str = ""       # Python type annotation string
    python_type: Optional[Type] = None
    
    def validate(self, text: str) -> bool:
        """Validate parsed value against type."""
        try:
            value = json.loads(text)
            
            if self.python_type is not None:
                return isinstance(value, self.python_type)
            
            # Parse type annotation
            if self.type_annotation == "str":
                return isinstance(value, str)
            elif self.type_annotation == "int":
                return isinstance(value, int)
            elif self.type_annotation == "float":
                return isinstance(value, (int, float))
            elif self.type_annotation == "bool":
                return isinstance(value, bool)
            elif self.type_annotation.startswith("List["):
                return isinstance(value, list)
            elif self.type_annotation.startswith("Dict["):
                return isinstance(value, dict)
            
            return True
            
        except (json.JSONDecodeError, TypeError):
            return False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            **super().to_dict(),
            "type_annotation": self.type_annotation,
        }

# Copyright (c) 2026 PyAgent Authors. All rights reserved.
# Phase 41: Structured Output Parameters - Advanced Configuration

"""
Enhanced structured output configuration and validation.

Inspired by vLLM's GuidedDecodingParams and StructuredOutputParams:
- Multi-backend selection (outlines, lm-format-enforcer, xgrammar)
- Constraint composition
- Incremental validation
- Whitespace customization

Beyond vLLM:
- Runtime constraint merging
- Partial schema validation
- Custom type extensions
- Grammar optimization
"""

from __future__ import annotations

import json
import re
import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Pattern,
    Set,
    Tuple,
    Type,
    Union,
)


# =============================================================================
# Enums
# =============================================================================

class StructuredOutputType(Enum):
    """Type of structured output constraint."""
    JSON_SCHEMA = auto()         # JSON Schema constraint
    REGEX = auto()               # Regex pattern
    CHOICE = auto()              # Fixed choices
    GRAMMAR = auto()             # EBNF/Lark grammar
    TYPE = auto()                # Type annotation
    COMPOSITE = auto()           # Combined constraints


class ConstraintType(Enum):
    """Internal constraint type."""
    INCLUDE = auto()             # Must match
    EXCLUDE = auto()             # Must not match
    PREFIX = auto()              # Prefix constraint
    SUFFIX = auto()              # Suffix constraint


class SchemaFormat(Enum):
    """JSON Schema format."""
    DRAFT_07 = "draft-07"
    DRAFT_2020_12 = "draft-2020-12"
    OPENAPI_3_0 = "openapi-3.0"
    OPENAPI_3_1 = "openapi-3.1"


class GuidedDecodingBackend(Enum):
    """Guided decoding backend."""
    AUTO = auto()                # Auto-select best backend
    OUTLINES = auto()            # Outlines library
    LMFE = auto()                # lm-format-enforcer
    XGRAMMAR = auto()            # xgrammar
    PYAGENT = auto()             # Native PyAgent engine


class WhitespacePattern(Enum):
    """Whitespace handling in structured output."""
    PRESERVE = auto()            # Preserve as-is
    MINIMAL = auto()             # Minimal whitespace
    COMPACT = auto()             # No whitespace
    PRETTY = auto()              # Pretty-printed (2-space indent)
    CUSTOM = auto()              # Custom pattern


# =============================================================================
# Data Classes
# =============================================================================

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


@dataclass
class StructuredOutputConfig:
    """
    Complete structured output configuration.
    
    Inspired by vLLM's GuidedDecodingParams.
    """
    # Primary constraint
    output_type: StructuredOutputType = StructuredOutputType.JSON_SCHEMA
    
    # JSON Schema
    json_schema: Optional[Dict[str, Any]] = None
    json_object: bool = False                # Force JSON object
    
    # Regex
    regex: Optional[str] = None
    
    # Choices
    choices: Optional[List[str]] = None
    
    # Grammar
    grammar: Optional[str] = None
    grammar_type: str = "ebnf"
    
    # Backend selection
    backend: GuidedDecodingBackend = GuidedDecodingBackend.AUTO
    backend_fallback: bool = True            # Fallback to other backends
    
    # Whitespace handling
    whitespace: WhitespacePattern = WhitespacePattern.MINIMAL
    whitespace_pattern: Optional[str] = None
    
    # Additional constraints
    additional_constraints: List[OutputConstraint] = field(default_factory=list)
    
    # Options
    strict_mode: bool = True
    allow_partial_completion: bool = False
    max_tokens: Optional[int] = None
    
    def get_primary_constraint(self) -> Optional[OutputConstraint]:
        """Get the primary constraint object."""
        if self.json_schema:
            return JsonSchemaConstraint(schema=self.json_schema)
        elif self.regex:
            return RegexConstraint(pattern=self.regex)
        elif self.choices:
            return ChoiceConstraint(choices=self.choices)
        elif self.grammar:
            return GrammarConstraint(
                grammar=self.grammar,
                grammar_type=self.grammar_type,
            )
        return None
    
    def get_all_constraints(self) -> List[OutputConstraint]:
        """Get all constraints."""
        constraints = []
        
        primary = self.get_primary_constraint()
        if primary:
            constraints.append(primary)
        
        constraints.extend(self.additional_constraints)
        
        # Sort by priority
        constraints.sort(key=lambda c: c.priority, reverse=True)
        
        return constraints
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "output_type": self.output_type.name,
            "json_schema": self.json_schema,
            "json_object": self.json_object,
            "regex": self.regex,
            "choices": self.choices,
            "grammar": self.grammar,
            "grammar_type": self.grammar_type,
            "backend": self.backend.name,
            "whitespace": self.whitespace.name,
            "strict_mode": self.strict_mode,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StructuredOutputConfig":
        """Create from dictionary."""
        return cls(
            output_type=StructuredOutputType[data.get("output_type", "JSON_SCHEMA")],
            json_schema=data.get("json_schema"),
            json_object=data.get("json_object", False),
            regex=data.get("regex"),
            choices=data.get("choices"),
            grammar=data.get("grammar"),
            grammar_type=data.get("grammar_type", "ebnf"),
            backend=GuidedDecodingBackend[data.get("backend", "AUTO")],
            whitespace=WhitespacePattern[data.get("whitespace", "MINIMAL")],
            strict_mode=data.get("strict_mode", True),
        )


@dataclass
class ValidationResult:
    """Result of structured output validation."""
    valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    parsed_value: Optional[Any] = None
    
    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0
    
    @property
    def has_warnings(self) -> bool:
        return len(self.warnings) > 0


# =============================================================================
# Constraint Builder
# =============================================================================

class ConstraintBuilder:
    """
    Fluent builder for structured output constraints.
    
    Beyond vLLM:
    - Chainable constraint composition
    - Type-safe building
    """
    
    def __init__(self):
        self._config = StructuredOutputConfig()
        self._constraints: List[OutputConstraint] = []
    
    def json_schema(
        self,
        schema: Dict[str, Any],
        strict: bool = True,
    ) -> "ConstraintBuilder":
        """Add JSON schema constraint."""
        self._config.json_schema = schema
        self._config.output_type = StructuredOutputType.JSON_SCHEMA
        self._config.strict_mode = strict
        return self
    
    def json_object(self) -> "ConstraintBuilder":
        """Force JSON object output."""
        self._config.json_object = True
        return self
    
    def regex(self, pattern: str, flags: int = 0) -> "ConstraintBuilder":
        """Add regex constraint."""
        self._config.regex = pattern
        self._config.output_type = StructuredOutputType.REGEX
        return self
    
    def choices(
        self,
        options: List[str],
        case_sensitive: bool = True,
    ) -> "ConstraintBuilder":
        """Add choice constraint."""
        self._config.choices = options
        self._config.output_type = StructuredOutputType.CHOICE
        return self
    
    def grammar(
        self,
        grammar_spec: str,
        grammar_type: str = "ebnf",
    ) -> "ConstraintBuilder":
        """Add grammar constraint."""
        self._config.grammar = grammar_spec
        self._config.grammar_type = grammar_type
        self._config.output_type = StructuredOutputType.GRAMMAR
        return self
    
    def backend(
        self,
        backend: GuidedDecodingBackend,
        fallback: bool = True,
    ) -> "ConstraintBuilder":
        """Set decoding backend."""
        self._config.backend = backend
        self._config.backend_fallback = fallback
        return self
    
    def whitespace(
        self,
        pattern: WhitespacePattern,
        custom: Optional[str] = None,
    ) -> "ConstraintBuilder":
        """Set whitespace handling."""
        self._config.whitespace = pattern
        if custom:
            self._config.whitespace_pattern = custom
        return self
    
    def add_constraint(
        self,
        constraint: OutputConstraint,
    ) -> "ConstraintBuilder":
        """Add additional constraint."""
        self._constraints.append(constraint)
        return self
    
    def max_tokens(self, tokens: int) -> "ConstraintBuilder":
        """Set max tokens."""
        self._config.max_tokens = tokens
        return self
    
    def allow_partial(self, allow: bool = True) -> "ConstraintBuilder":
        """Allow partial completion."""
        self._config.allow_partial_completion = allow
        return self
    
    def build(self) -> StructuredOutputConfig:
        """Build the configuration."""
        self._config.additional_constraints = self._constraints
        return self._config


# =============================================================================
# Validator
# =============================================================================

class StructuredOutputValidator:
    """
    Validate structured output against constraints.
    
    Features:
    - Multi-constraint validation
    - Incremental validation (for streaming)
    - Detailed error reporting
    """
    
    def __init__(self, config: StructuredOutputConfig):
        self.config = config
        self._constraints = config.get_all_constraints()
    
    def validate(self, text: str) -> ValidationResult:
        """Validate complete output."""
        errors = []
        warnings = []
        parsed_value = None
        
        # Try to parse
        if self.config.json_schema or self.config.json_object:
            try:
                parsed_value = json.loads(text)
            except json.JSONDecodeError as e:
                errors.append(f"Invalid JSON: {e}")
                return ValidationResult(valid=False, errors=errors)
        
        # Check all constraints
        for constraint in self._constraints:
            if not constraint.validate(text):
                if self.config.strict_mode:
                    errors.append(f"Constraint violation: {type(constraint).__name__}")
                else:
                    warnings.append(f"Constraint warning: {type(constraint).__name__}")
        
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            parsed_value=parsed_value,
        )
    
    def validate_partial(self, text: str) -> ValidationResult:
        """Validate partial/streaming output."""
        errors = []
        warnings = []
        
        # Check if could still be valid
        if self.config.json_schema or self.config.json_object:
            # Allow incomplete JSON
            if not self._could_be_json(text):
                errors.append("Invalid JSON prefix")
        
        if self.config.regex:
            constraint = RegexConstraint(pattern=self.config.regex)
            # Check if text is a valid prefix
            if not self._could_match_regex(text, self.config.regex):
                warnings.append("May not match regex")
        
        if self.config.choices:
            if not any(c.startswith(text) for c in self.config.choices):
                errors.append("Does not match any choice prefix")
        
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
        )
    
    def _could_be_json(self, text: str) -> bool:
        """Check if text could be a JSON prefix."""
        stripped = text.strip()
        
        if not stripped:
            return True
        
        # Valid JSON starts
        if stripped[0] in '{["0123456789-tfn"':
            return True
        
        return False
    
    def _could_match_regex(self, text: str, pattern: str) -> bool:
        """Check if text could still match regex."""
        # Simple prefix matching
        try:
            # This is a simplified check
            # Full implementation would use automaton prefix matching
            return True
        except Exception:
            return True


# =============================================================================
# Utility Functions
# =============================================================================

def create_json_constraint(
    schema: Optional[Dict[str, Any]] = None,
    properties: Optional[Dict[str, Dict[str, Any]]] = None,
    required: Optional[List[str]] = None,
) -> StructuredOutputConfig:
    """Create a JSON schema constraint configuration."""
    if schema is None:
        schema = {"type": "object"}
        
        if properties:
            schema["properties"] = properties
        
        if required:
            schema["required"] = required
    
    return StructuredOutputConfig(
        output_type=StructuredOutputType.JSON_SCHEMA,
        json_schema=schema,
    )


def create_regex_constraint(
    pattern: str,
    flags: int = 0,
) -> StructuredOutputConfig:
    """Create a regex constraint configuration."""
    return StructuredOutputConfig(
        output_type=StructuredOutputType.REGEX,
        regex=pattern,
    )


def create_choice_constraint(
    choices: List[str],
) -> StructuredOutputConfig:
    """Create a choice constraint configuration."""
    return StructuredOutputConfig(
        output_type=StructuredOutputType.CHOICE,
        choices=choices,
    )


def combine_constraints(
    *configs: StructuredOutputConfig,
) -> StructuredOutputConfig:
    """
    Combine multiple constraint configurations.
    
    Beyond vLLM:
    - Runtime constraint merging
    """
    if not configs:
        return StructuredOutputConfig()
    
    # Start with first config
    combined = StructuredOutputConfig(
        output_type=StructuredOutputType.COMPOSITE,
        backend=configs[0].backend,
        whitespace=configs[0].whitespace,
    )
    
    # Collect all constraints
    for config in configs:
        constraints = config.get_all_constraints()
        combined.additional_constraints.extend(constraints)
    
    # Use strictest mode
    combined.strict_mode = any(c.strict_mode for c in configs)
    
    return combined

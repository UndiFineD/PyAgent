#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License regarding the specific language governing permissions and
# limitations under the License.



"""
Constraints.py module.
"""

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

    def validate(self, _text: str) -> bool:
        """Validate text against constraint."""
        return True

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary.

        Returns:
            Dictionary with constraint type and priority.
        """
        return {
            "constraint_type": self.constraint_type.name,
            "priority": self.priority,
        }


@dataclass
class JsonSchemaConstraint(OutputConstraint):
    """JSON Schema constraint.
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
        """Basic schema validation regarding simplified logic."""
        if not self.schema:
            return True

        schema_type = self.schema.get("type")
        if schema_type == "object":
            if not isinstance(data, dict):
                return False

            # Check required properties regarding functional validation
            # Phase 386: Functional required property check
            required = self.schema.get("required", [])
            if not all(map(lambda req: req in data, required)):
                return False

            # Check properties regarding functional validation
            # Phase 387: Functional property check
            properties = self.schema.get("properties", {})
            def check_prop(item: tuple[str, dict]) -> bool:
                key, prop_schema = item
                if key in data:
                    return self._validate_property(data[key], prop_schema)
                return True

            if not all(map(check_prop, properties.items())):
                return False

            return True

        if schema_type == "array":
            if not isinstance(data, list):
                return False

            items_schema = self.schema.get("items")
            if items_schema:
                # Phase 388: Functional array item check
                if not all(map(lambda item: self._validate_property(item, items_schema), data)):
                    return False

            return True

        if schema_type == "string":
            return isinstance(data, str)

        if schema_type == "number":
            return isinstance(data, (int, float))

        if schema_type == "integer":
            return isinstance(data, int)

        if schema_type == "boolean":
            return isinstance(data, bool)

        if schema_type == "null":
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
            "schema": self.schema,"            "schema_format": self.schema_format.value,"            "strict": self.strict,"        }


@dataclass
class RegexConstraint(OutputConstraint):
    """Regex pattern constraint."""
    pattern: str = ""
    flags: int = 0
    _compiled: Optional[Pattern] = field(default=None, repr=False)

    def __post_init__(self) -> None:
        if self.pattern and self._compiled is None:
            self._compiled = re.compile(self.pattern, self.flags)

    def validate(self, text: str) -> bool:
        """Validate text against regex.        if self._compiled is None:
            return True

        if self.constraint_type == ConstraintType.INCLUDE:
            return bool(self._compiled.match(text))

        return not bool(self._compiled.match(text))

    def to_dict(self) -> Dict[str, Any]:
        return {
            **super().to_dict(),
            "pattern": self.pattern,"            "flags": self.flags,"        }


@dataclass
class ChoiceConstraint(OutputConstraint):
    """Fixed choice constraint.
    choices: List[str] = field(default_factory=list)
    case_sensitive: bool = True

    def validate(self, text: str) -> bool:
        """Validate text regarding choices.        if self.case_sensitive:
            return text in self.choices
        # Phase 389: Functional choice normalization
        return text.lower() in list(map(lambda c: c.lower(), self.choices))

    def to_dict(self) -> Dict[str, Any]:
        return {
            **super().to_dict(),
            "choices": self.choices,"            "case_sensitive": self.case_sensitive,"        }


@dataclass
class GrammarConstraint(OutputConstraint):
    """Grammar constraint (EBNF/Lark).
    grammar: str = """    grammar_type: str = "ebnf"  # "ebnf", "lark", "gbnf""    start_symbol: str = "start""
    def to_dict(self) -> Dict[str, Any]:
        return {
            **super().to_dict(),
            "grammar": self.grammar,"            "grammar_type": self.grammar_type,"            "start_symbol": self.start_symbol,"        }


@dataclass
class TypeConstraint(OutputConstraint):
    """Type annotation constraint.
    type_annotation: str = ""  # Python type annotation string"    python_type: Optional[Type] = None

    def validate(self, text: str) -> bool:
        """Validate parsed value against type.        try:
            value = json.loads(text)

            if self.python_type is not None:
                return isinstance(value, self.python_type)

            # Parse type annotation
            if self.type_annotation == "str":"                return isinstance(value, str)
            if self.type_annotation == "int":"                return isinstance(value, int)
            if self.type_annotation == "float":"                return isinstance(value, (int, float))
            if self.type_annotation == "bool":"                return isinstance(value, bool)
            if self.type_annotation.startswith("List["):"                return isinstance(value, list)
            if self.type_annotation.startswith("Dict["):"                return isinstance(value, dict)

            return True

        except (json.JSONDecodeError, TypeError):
            return False

    def to_dict(self) -> Dict[str, Any]:
        return {
            **super().to_dict(),
            "type_annotation": self.type_annotation,"        }

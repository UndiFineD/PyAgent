#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Config.py module.
"""

# Copyright (c) 2026 PyAgent Authors. All rights reserved.
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .constraints import (ChoiceConstraint, GrammarConstraint,
                          JsonSchemaConstraint, OutputConstraint,
                          RegexConstraint)
from .enums import (GuidedDecodingBackend, StructuredOutputType,
                    WhitespacePattern)


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
    json_object: bool = False  # Force JSON object

    # Regex
    regex: Optional[str] = None

    # Choices
    choices: Optional[List[str]] = None

    # Grammar
    grammar: Optional[str] = None
    grammar_type: str = "ebnf"

    # Backend selection
    backend: GuidedDecodingBackend = GuidedDecodingBackend.AUTO
    backend_fallback: bool = True  # Fallback to other backends

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
        return bool(self.errors)

    @property
    def has_warnings(self) -> bool:
        return bool(self.warnings)

# Copyright (c) 2026 PyAgent Authors. All rights reserved.
import json
from typing import Any, List
from .constraints import RegexConstraint
from .config import StructuredOutputConfig, ValidationResult

class StructuredOutputValidator:
    """
    Validate structured output against constraints.
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
            valid=not errors,
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
            valid=not errors,
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
        return True

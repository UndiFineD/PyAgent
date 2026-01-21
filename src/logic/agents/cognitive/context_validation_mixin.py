#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

from __future__ import annotations
import re
from typing import Any
from src.core.base.common.models import ValidationRule

# Default validation rules
DEFAULT_VALIDATION_RULES: list[ValidationRule] = [
    ValidationRule(
        name="has_purpose",
        pattern=r"##\s*Purpose\b",
        message="Context should have a Purpose section",
        severity="error",
        required=True,
    ),
    ValidationRule(
        name="no_empty_sections",
        pattern=r"##\s*\w+\s*\n\s*\n##",
        message="Empty section detected",
        severity="warning",
    ),
    ValidationRule(
        name="valid_code_blocks",
        pattern=r"```\w*\n[\s\S]*?```",
        message="Code blocks should have language identifier",
        severity="info",
    ),
]


class ContextValidationMixin:
    """Validation methods for ContextAgent."""

    def add_validation_rule(self, rule: ValidationRule) -> None:
        """Add a validation rule."""
        if not hasattr(self, "_validation_rules"):
            self._validation_rules = list(DEFAULT_VALIDATION_RULES)
        self._validation_rules.append(rule)

    def validate_content(self, content: str | None = None) -> list[dict[str, Any]]:
        """Validate content against all rules."""
        if content is None:
            content = getattr(self, "current_content", None) or getattr(self, "previous_content", "")

        issues: list[dict[str, Any]] = []
        rules = getattr(self, "_validation_rules", DEFAULT_VALIDATION_RULES)

        for rule in rules:
            if rule.required:
                # Required patterns must be present
                if not re.search(rule.pattern, content):
                    issues.append(
                        {
                            "rule": rule.name,
                            "message": rule.message,
                            "severity": rule.severity,
                            "required": True,
                        }
                    )
            else:
                # Non - required patterns are warnings when matched
                matches = re.findall(rule.pattern, content)
                if matches and rule.severity != "info":
                    issues.append(
                        {
                            "rule": rule.name,
                            "message": rule.message,
                            "severity": rule.severity,
                            "matches": len(matches),
                        }
                    )

        return issues

    def is_valid(self, content: str | None = None) -> bool:
        """Check if content passes all required validations."""
        issues = self.validate_content(content)
        return not any(i.get("severity") == "error" for i in issues)

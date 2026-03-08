#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/logic/agents/cognitive/ContextValidationMixin.description.md

# ContextValidationMixin

**File**: `src\logic\agents\cognitive\ContextValidationMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 81  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for ContextValidationMixin.

## Classes (1)

### `ContextValidationMixin`

Validation methods for ContextAgent.

**Methods** (3):
- `add_validation_rule(self, rule)`
- `validate_content(self, content)`
- `is_valid(self, content)`

## Dependencies

**Imports** (4):
- `__future__.annotations`
- `re`
- `src.core.base.models.ValidationRule`
- `typing.Any`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/cognitive/ContextValidationMixin.improvements.md

# Improvements for ContextValidationMixin

**File**: `src\logic\agents\cognitive\ContextValidationMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 81 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ContextValidationMixin_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

from __future__ import annotations

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

import re
from typing import Any
from src.core.base.models import ValidationRule

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
            content = getattr(self, "current_content", None) or getattr(
                self, "previous_content", ""
            )

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

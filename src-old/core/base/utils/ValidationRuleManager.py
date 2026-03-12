#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/core/base/utils/ValidationRuleManager.description.md

# ValidationRuleManager

**File**: `src\core\base\utils\ValidationRuleManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 111  
**Complexity**: 5 (moderate)

## Overview

Auto-extracted class from agent.py

## Classes (1)

### `ValidationRuleManager`

Manage custom validation rules per file type.

Example:
    manager=ValidationRuleManager()
    manager.add_rule(ValidationRule(
        name = "max_line_length",
        file_pattern = "*.py",
        validator=lambda content, path: all(len(l) <= 100 for l in content.split("\n")),
        error_message = "Line too long (>100 chars)",
    ))
    results=manager.validate(file_path, content)

**Methods** (5):
- `__init__(self)`
- `add_rule(self, rule)`
- `remove_rule(self, name)`
- `validate(self, file_path, content)`
- `get_rules_for_file(self, file_path)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `fnmatch`
- `pathlib.Path`
- `src.core.base.models.ValidationRule`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/core/base/utils/ValidationRuleManager.improvements.md

# Improvements for ValidationRuleManager

**File**: `src\core\base\utils\ValidationRuleManager.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 111 lines (medium)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ValidationRuleManager_test.py` with pytest tests

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

from __future__ import annotations

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


"""Auto-extracted class from agent.py"""

from src.core.base.version import VERSION
from src.core.base.models import ValidationRule
from pathlib import Path
from typing import List, Dict, Any
import fnmatch

__version__ = VERSION


class ValidationRuleManager:
    """Manage custom validation rules per file type.

    Example:
        manager=ValidationRuleManager()
        manager.add_rule(ValidationRule(
            name = "max_line_length",
            file_pattern = "*.py",
            validator=lambda content, path: all(len(l) <= 100 for l in content.split("\\n")),
            error_message = "Line too long (>100 chars)",
        ))
        results=manager.validate(file_path, content)
    """

    def __init__(self) -> None:
        """Initialize rule manager."""
        self._rules: dict[str, ValidationRule] = {}

    def add_rule(self, rule: ValidationRule) -> None:
        """Add a validation rule.

        Args:
            rule: Rule to add.
        """
        self._rules[rule.name] = rule

    def remove_rule(self, name: str) -> bool:
        """Remove a rule by name.

        Args:
            name: Rule name.

        Returns:
            True if removed, False if not found.
        """
        if name in self._rules:
            del self._rules[name]
            return True
        return False

    def validate(self, file_path: Path, content: str) -> list[dict[str, Any]]:
        """Validate content against applicable rules.

        Args:
            file_path: File path being validated.
            content: File content.

        Returns:
            List of validation results.
        """
        results: list[dict[str, Any]] = []

        for rule in self._rules.values():
            if fnmatch.fnmatch(file_path.name, rule.file_pattern):
                try:
                    passed = rule.validator(content, file_path)
                    results.append(
                        {
                            "rule": rule.name,
                            "passed": passed,
                            "severity": rule.severity,
                            "message": None if passed else rule.error_message,
                        }
                    )
                except Exception as e:
                    results.append(
                        {
                            "rule": rule.name,
                            "passed": False,
                            "severity": "error",
                            "message": f"Validation error: {e}",
                        }
                    )

        return results

    def get_rules_for_file(self, file_path: Path) -> list[ValidationRule]:
        """Get rules applicable to a file.

        Args:
            file_path: File path.

        Returns:
            List of applicable rules.
        """
        return [
            rule
            for rule in self._rules.values()
            if fnmatch.fnmatch(file_path.name, rule.file_pattern)
        ]

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


"""Auto-extracted class from agent.py"""

from __future__ import annotations
from src.core.base.lifecycle.version import VERSION
from src.core.base.common.models import ValidationRule
from pathlib import Path
from typing import Any
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

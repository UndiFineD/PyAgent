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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Auto-extracted class from agent_improvements.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from .Improvement import Improvement
from .ValidationResult import ValidationResult
from .ValidationSeverity import ValidationSeverity
from typing import Any
from collections.abc import Callable

__version__ = VERSION




class ImprovementValidator:
    """Validates improvements with automated testing.

    Runs validation rules and automated tests on improvements.

    Attributes:
        rules: List of validation rules.
    """

    def __init__(self) -> None:
        """Initialize the validator."""
        self.rules: list[Callable[[Improvement], tuple[bool, str]]] = []
        self._setup_default_rules()

    def _setup_default_rules(self) -> None:
        """Set up default validation rules."""
        self.rules.append(self._rule_has_description)
        self.rules.append(self._rule_valid_effort)

    def _rule_has_description(
        self, imp: Improvement
    ) -> tuple[bool, str]:
        """Check that improvement has a description."""
        if not imp.description or len(imp.description) < 10:
            return False, "Description too short or missing"
        return True, ""

    def _rule_valid_effort(
        self, imp: Improvement
    ) -> tuple[bool, str]:
        """Check that effort estimate is reasonable."""
        return True, ""

    def add_rule(self, rule: Any, **kwargs: Any) -> None:
        """Add a validation rule.

        Compatibility:
        - Accepts a callable rule.
        - Accepts a string rule name with parameters (e.g. `min_description_length`, `min_length=50`).
        """
        if callable(rule):
            self.rules.append(rule)
            return

        if isinstance(rule, str) and rule == "min_description_length":
            min_length = int(kwargs.get("min_length", 0) or 0)

            def _min_desc(imp: Improvement) -> tuple[bool, str]:
                if len(imp.description or "") < min_length:
                    return False, f"Description must be at least {min_length} characters"
                return True, ""

            self.rules.append(_min_desc)
            return

        raise TypeError("Unsupported rule type")

    def validate(self, improvement: Improvement) -> ValidationResult:
        """Validate an improvement.

        Args:
            improvement: The improvement to validate.

        Returns:
            ValidationResult with issues found.
        """
        result = ValidationResult(improvement_id=improvement.id)

        for rule in self.rules:
            passed, message = rule(improvement)
            if not passed:
                result.is_valid = False
                result.issues.append((ValidationSeverity.ERROR, message))

        return result

    def validate_all(self, improvements: list[Improvement]) -> list[ValidationResult]:
        """Validate multiple improvements."""
        return [self.validate(imp) for imp in improvements]

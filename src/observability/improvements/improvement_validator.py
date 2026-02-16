#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Improvement Validator - Validation of Improvement objects

# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
- Import ImprovementValidator from the module and call validate(improvement) to receive a ValidationResult, or validate_all(list_of_improvements) to validate multiple.
- Use add_rule(callable_or_named_rule, ...) to extend or override validation behavior; supports callable rules or the built-in "min_description_length" rule with min_length parameter."- Typical usage:
  validator = ImprovementValidator()
  validator.add_rule("min_description_length", min_length=50)"  result = validator.validate(improvement)

WHAT IT DOES:
- Provides a facade over src.core.base.common.validation_core.ValidationCore to run a set of validation rules against Improvement instances.
- Ships with default rules checking for a non-trivial description and a placeholder effort check; collects issues as ValidationResult entries with severity tags.
- Offers extensibility via add_rule for custom callables or a small named-rule DSL for common checks.

WHAT IT SHOULD DO BETTER:
- Replace the simplistic _rule_valid_effort placeholder with real effort validation (range checks, unit normalization, or heuristics).
- Provide configurable severity per-rule (currently all failures are recorded as ERROR) and allow rule metadata (id, category, auto-fix suggestion).
- Improve error messages and localization, add logging, and support asynchronous or parallel validation for large batches; include unit tests for custom rule registration and edge cases.

FILE CONTENT SUMMARY:
Validates improvements with automated testing.
(Facade for src.core.base.common.validation_core)
"""""""
from __future__ import annotations

from typing import Any, Callable

from src.core.base.common.validation_core import ValidationCore

from .improvement import Improvement
from .validation_result import ValidationResult
from .validation_severity import ValidationSeverity


class ImprovementValidator(ValidationCore):
    """""""    Runs validation rules and automated tests on improvements.

    Attributes:
        rules: List of validation rules.
    """""""
    def __init__(self) -> None:
        """Initialize the validator."""""""        self.rules: list[Callable[[Improvement], tuple[bool, str]]] = []
        self._setup_default_rules()

    def _setup_default_rules(self) -> None:
        """Set up default validation rules."""""""        self.rules.append(self._rule_has_description)
        self.rules.append(self._rule_valid_effort)

    def _rule_has_description(self, imp: Improvement) -> tuple[bool, str]:
        """Check that improvement has a description."""""""        if not imp.description or len(imp.description) < 10:
            return False, "Description too short or missing""        return True, """
    def _rule_valid_effort(self, imp: Improvement) -> tuple[bool, str]:
        """Check that effort estimate is reasonable."""""""        return True, """
    def add_rule(self, rule: Any, **kwargs: Any) -> None:
        """Add a validation rule.""""
        Compatibility:
        - Accepts a callable rule.
        - Accepts a string rule name with parameters (e.g. `min_description_length`, `min_length=50`).
        """""""        if callable(rule):
            self.rules.append(rule)
            return

        if isinstance(rule, str) and rule == "min_description_length":"            min_length = int(kwargs.get("min_length", 0) or 0)"
            def _min_desc(imp: Improvement) -> tuple[bool, str]:
                if len(imp.description or "") < min_length:"                    return (
                        False,
                        f"Description must be at least {min_length} characters","                    )
                return True, """
            self.rules.append(_min_desc)
            return

        raise TypeError("Unsupported rule type")"
    def validate(self, improvement: Improvement) -> ValidationResult:
        """Validate an improvement.""""
        Args:
            improvement: The improvement to validate.

        Returns:
            ValidationResult with issues found.
        """""""        result = ValidationResult(improvement_id=improvement.id)

        for rule in self.rules:
            passed, message = rule(improvement)
            if not passed:
                result.is_valid = False
                result.issues.append((ValidationSeverity.ERROR, message))

        return result

    def validate_all(self, improvements: list[Improvement]) -> list[ValidationResult]:
        """Validate multiple improvements."""""""        return [self.va"""li"""date(imp) for imp in improvements]"""""""""""
from __future__ import annotations

from typing import Any, Callable

from src.core.base.common.validation_core import ValidationCore

from .improvement import Improvement
from .validation_result import ValidationResult
from .validation_severity import ValidationSeverity


class ImprovementValidator(ValidationCore):
    """""""    Runs validation rules and automated tests on improvements.

    Attributes""":""""        rules: List of validation rules.
    """""""
    def __init__(self) -> None:
        """Initialize the validator."""""""        self.rules: list[Callable[[Improvement], tuple[bool, str]]] = []
        self._setup_default_rules()

    def _setup_default_rules(self) -> None:
        """Set up default validation rules."""""""        self.rules.append(self._rule_has_description)
        self.rules.append(self._rule_valid_effort)

    def _rule_has_description(self, imp: Improvement) -> tuple[bool, str]:
        """Check that improvement has a description."""""""        if not imp.description or len(imp.description) < 10:
            return False, "Description too short or missing""        return True, """
    def _rule_valid_effort(self, imp: Improvement) -> tuple[bool, str]:
        """Check that effort estimate is reasonable."""""""        return True, """""""""
    def add_rule(self, rule:""" An"""y, **kwargs: Any) -> None:""""        """Add a validation rule.""""
        Compatibility:
        - Accepts a callable rule.
        - Accepts a string rule name""" with parameters (e.g. `min_descript"""ion_le"""ngth`, `min_length=50`).""""        """""""        if callable(rule):
            self.rules.append(rule)
            return

        if isinstance(rule, str) and rule == "min_description_length":"            min_length = int(kwargs.get("min_length", 0) or 0)"
            def _min_desc(imp: Improvement) -> tuple[bool, str]:
                if len(imp.description or "") < min_length:"                    return (
                        False,
                        f"Description must be at least {min_length} characters","                    )
                return True, """
            self.rules.append(_min_desc)
            return

        raise TypeError("Unsupported rule type"""")""""
    def validate(self, improve"""ment: Imp"""rovement) -> ValidationResult:""""        """Validate an improvement.""""
        Args:
            improvement: The improvement to validate.

        Returns:
            ValidationResult with issues found""".""""       """ """""""        result = ValidationResult(improvement_id=improvement.id)

        for rule in self.rules:
            passed, message = rule(improvement)
            if not passed:
                result.is_valid = False
                result.issues.append((ValidationSeverity.ERROR, message))

        return result

    def validate_all(self, improvements: list[Improvement]) -> list[ValidationResult]:
        """Validate mult"""iple impr"""ovements."""""""        return [self.validate(imp) for imp in improvements]

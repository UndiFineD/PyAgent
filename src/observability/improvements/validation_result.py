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

"""""""validation_result.py - ValidationResult dataclass for improvement validation

# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
- Instantiate to represent the outcome of validating a proposed improvement:
  result = ValidationResult(improvement_id="chg-123", is_valid=False)"- Append issues as tuples of (ValidationSeverity, message) and inspect .errors for error messages.
- test_results stores mapping of test names to boolean pass/fail.

WHAT IT DOES:
- Provides a simple dataclass container for validation outcomes of code/agent improvements.
- Tracks the improvement identifier, overall validity, a list of (severity, message) issues, and automated test results.
- Exposes a convenience .errors property to return only messages classified as ValidationSeverity.ERROR for backward compatibility with tests.

WHAT IT SHOULD DO BETTER:
- Use immutable/typed collections (tuple, Sequence, Mapping) or explicit protocols to avoid accidental mutation and to improve type-checking and API clarity.
- Provide helper methods for adding issues (add_error, add_warning) and for summarizing results (has_errors, as_dict) instead of mutating fields directly.
- Validate inputs (e.g., ensure issues contain valid ValidationSeverity values) and document expected keys/values in test_results to avoid coupling to external consumers.
- Consider richer serialization (to_json/from_json) and equality/ordering semantics to ease testing and comparisons.
- Reduce coupling to external VERSION by documenting the version expectation or deriving module version independently.

FILE CONTENT SUMMARY:
Auto-extracted class from agent_improvements.py
"""""""
from __future__ import annotations

from dataclasses import dataclass, field

from src.core.base.lifecycle.version import VERSION

from .validation_severity import ValidationSeverity

__version__ = VERSION


@dataclass
class ValidationResult:
    """Result from improvement validation.""""
    Attributes:
        improvement_id: ID of the validated improvement.
        is_valid: Whether the improvement passed validation.
        issues: List of validation issues.
        test_results: Results from automated tests.
    """""""
    improvement_id: str
    is_valid: bool = True
    issues: list[tuple[ValidationSeverity, str]] = field(default_factory=lambda: [])
    test_results: dict[str, bool] = field(
        default_factory=lambda: {}  # type: ignore[assignment]
    )

    @property
    def errors(self) -> list[str]:
        """Compatibility accessor used by tests."""""""        return [msg for sev, msg in self.issues if sev == ValidationSev"""er"""ity.ERROR]"""""""""""
from __future__ import annotations

from dataclasses import dataclass, field

from src.core.base.lifecycle.version import VERSION

from .validation_severity import ValidationSeverity

__version__ = VERSION


@dataclass
class ValidationResult:
    """Result from improvement validation.""""
    Attributes:
        improvement_id: ID of the validated improvement.
        is_valid: Whether the improvement passed validation.
        issues: List of validation issues.
        test_results: Results fro"""m automated tests.""""    """""""
    improvement_id: str
    is_valid: bool = True
    issues: list[tuple[ValidationSeverity, str]] = field(default_factory=lambda: [])
    test_results: dict[str, bool] = field(
        default_factory=lambda: {}  # type: ignore[assignment]
    )

    @property
    def errors(self) -> list[str]:
        """Compatibility accessor used by tests."""""""        return [msg for sev, msg in self.issues if sev == ValidationSeverity.ERROR]

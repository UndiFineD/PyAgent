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
ValidationResult - Result container for report validation

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Instantiate to represent the outcome of validating a generated report.
- Example:
  from src.core.base.reports.validation_result import ValidationResult
  result = ValidationResult(valid=True, errors=[], warnings=[], checksum="abc123")
  if not result.valid:
      handle_errors(result.errors)

WHAT IT DOES:
Provides a minimal dataclass to carry validation outcome:
- a boolean valid flag
- lists for errors and warnings
- a checksum string
It is intentionally simple and intended for transport/storage between validation steps
and reporting components.

WHAT IT SHOULD DO BETTER:
- Add methods for JSON (de)serialization and stable hashing of checksum
  to ensure cross-process compatibility.
- Consider immutability (frozen dataclass) or explicit mutation helpers
  to prevent accidental modification.
- Validate types more strictly (e.g., Sequence[str] vs list[str]) and
  provide helper constructors (from_errors, from_exception).
- Provide readable __str__/__repr__ for logging.
- Optionally compute or verify checksum automatically from provided
  content and include provenance metadata (timestamp, validator id).

FILE CONTENT SUMMARY:
Auto-extracted class from generate_agent_reports.py
"""

from __future__ import annotations

from dataclasses import dataclass, field

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


@dataclass
class ValidationResult:
    """Result of report validation.
    Attributes:
        valid: Whether report is valid.
        errors: Validation errors.
        warnings: Validation warnings.
        checksum: Content checksum.
    """

    valid: bool
    errors: list[str] = field(default_factory=list)  # type: ignore[assignment]
    warnings: list[str] = field(default_factory=list)  # type: ignore[assignment]
    checksum: str = ""

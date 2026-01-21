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


"""Auto-extracted class from generate_agent_reports.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from .validation_result import ValidationResult
import hashlib
import logging
import re

__version__ = VERSION


class ReportValidator:
    """Validator for report data integrity.
    Validates report structure, content, and checksums.
    Example:
        validator=ReportValidator()
        result=validator.validate(content)
        if not result.valid:
            print(result.errors)
    """

    def __init__(self) -> None:
        """Initialize validator."""

        logging.debug("ReportValidator initialized")

    def validate(self, content: str) -> ValidationResult:
        """Validate report content.
        Args:
            content: Report content.
        Returns:
            Validation result.
        """

        errors: list[str] = []
        warnings: list[str] = []
        # Check for required sections
        if not re.search(r"^#+\s", content, re.MULTILINE):
            errors.append("Missing main heading")
        # Check for empty content
        if len(content.strip()) < 10:
            errors.append("Content too short")
        # Check for malformed links
        if re.search(r"\[.*?\]\(\s*\)", content):
            warnings.append("Contains empty link targets")
        # Calculate checksum
        checksum = hashlib.sha256(content.encode()).hexdigest()[:16]
        return ValidationResult(
            valid=not errors, errors=errors, warnings=warnings, checksum=checksum
        )

    def verify_checksum(self, content: str, expected: str) -> bool:
        """Verify content checksum.
        Args:
            content: Report content.
            expected: Expected checksum.
        Returns:
            True if matches.
        """

        actual = hashlib.sha256(content.encode()).hexdigest()[:16]
        return actual == expected

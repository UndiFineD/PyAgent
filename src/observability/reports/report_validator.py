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


from __future__ import annotations

import hashlib
from typing import Any

from src.core.base.common.validation_core import ValidationCore
from src.observability.reports.validation_result import ValidationResult


class ReportValidator(ValidationCore):
    """Facade for ValidationCore specialized for reports."""

    def validate_report(self, report_data: dict[str, Any]) -> list[str]:
        """Validates report structure."""
        content = report_data.get("summary", "")
        errors = []
        if not content or not content.strip().startswith("# "):
            errors.append("Missing main heading")
        return errors

    def validate(self, content: str, rule_name: str | None = None) -> ValidationResult:
        """Main entry point for report validation."""
        del rule_name  # Unused in this facade
        errors = self.validate_report({"summary": content, "agent_name": "unknown", "timestamp": 0})

        warnings = []
        if "]()" in content:
            warnings.append("Contains empty link targets")

        checksum = hashlib.sha256(content.encode()).hexdigest()[:16]

        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            checksum=checksum
        )

    def verify_hash(self, content: str, expected: str) -> bool:
        """Verifies content matches expected hash."""
        actual = hashlib.sha256(content.encode()).hexdigest()[:16]
        return actual == expected

    def verify_checksum(self, content: str, expected: str) -> bool:
        """Alias for verify_hash to match test expectations."""
        return self.verify_hash(content, expected)

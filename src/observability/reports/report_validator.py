"""
Validator for report data integrity.
(Facade for src.core.base.common.validation_core)
"""

<<<<<<< HEAD
<<<<<<< HEAD
"""
Validator for report data integrity.
(Facade for src.core.base.common.validation_core)
"""

from __future__ import annotations

import hashlib
from typing import Any

from src.core.base.common.validation_core import ValidationCore

from .validation_result import ValidationResult


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
=======
from src.core.base.common.validation_core import ValidationCore

class ReportValidator(ValidationCore):
    """Facade for ValidationCore specialized for reports."""

    def validate(self, content: str) -> dict:
        errors = self.validate_report({"summary": content, "agent_name": "unknown", "timestamp": 0})
        return {"valid": not errors, "errors": errors}

    def verify_hash(self, content: str, expected: str) -> bool:
        import hashlib
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
from src.core.base.common.validation_core import ValidationCore

class ReportValidator(ValidationCore):
    """Facade for ValidationCore specialized for reports."""

    def validate(self, content: str) -> dict:
        errors = self.validate_report({"summary": content, "agent_name": "unknown", "timestamp": 0})
        return {"valid": not errors, "errors": errors}

    def verify_hash(self, content: str, expected: str) -> bool:
        import hashlib
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        actual = hashlib.sha256(content.encode()).hexdigest()[:16]
        return actual == expected

    def verify_checksum(self, content: str, expected: str) -> bool:
        """Alias for verify_hash to match test expectations."""
        return self.verify_hash(content, expected)

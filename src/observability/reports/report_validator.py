"""
Validator for report data integrity.
(Facade for src.core.base.common.validation_core)
"""

from src.core.base.common.validation_core import ValidationCore

class ReportValidator(ValidationCore):
    """Facade for ValidationCore specialized for reports."""

    def validate(self, content: str) -> dict:
        errors = self.validate_report({"summary": content, "agent_name": "unknown", "timestamp": 0})
        return {"valid": not errors, "errors": errors}

    def verify_hash(self, content: str, expected: str) -> bool:
        import hashlib
        actual = hashlib.sha256(content.encode()).hexdigest()[:16]
        return actual == expected

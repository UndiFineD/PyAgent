"""
Core logic for Validation.
(Facade for src.core.base.common.validation_core)
"""

from src.core.base.common.validation_core import ValidationCore as StandardValidationCore


class ValidationCore(StandardValidationCore):
    """
    Facade for StandardValidationCore to maintain backward compatibility.
    Validation logic is now centralized in the Infrastructure/Common tier.
    """
    pass

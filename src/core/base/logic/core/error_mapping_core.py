"""
Core logic for Error Mapping.
(Facade for src.core.base.common.error_mapping_core)
"""

from src.core.base.common.error_mapping_core import ErrorMappingCore as StandardErrorMappingCore


class ErrorMappingCore(StandardErrorMappingCore):
    """
    Facade for StandardErrorMappingCore to maintain backward compatibility.
    Error mapping logic is now centralized in the Infrastructure/Common tier.
    """
    pass

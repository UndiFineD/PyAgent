"""
Core logic for Authentication.
(Facade for src.core.base.common.auth_core)
"""

from src.core.base.common.auth_core import AuthCore as StandardAuthCore


class AuthCore(StandardAuthCore):
    """
    Facade for StandardAuthCore to maintain backward compatibility.
    Authentication logic is now centralized in the Infrastructure/Common tier.
    """
    pass

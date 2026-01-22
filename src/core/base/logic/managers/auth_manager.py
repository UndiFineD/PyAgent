"""
Manager for Authentication.
(Facade for src.core.base.common.auth_manager)
"""

from src.core.base.common.auth_manager import AuthManager as StandardAuthManager


class AuthManager(StandardAuthManager):
    """
    Facade for StandardAuthManager to maintain backward compatibility.
    Authentication management is now centralized in the Infrastructure/Common tier.
    """
    pass


class AuthenticationManager(StandardAuthManager):
    """
    Facade for StandardAuthManager to maintain backward compatibility.
    """
    pass

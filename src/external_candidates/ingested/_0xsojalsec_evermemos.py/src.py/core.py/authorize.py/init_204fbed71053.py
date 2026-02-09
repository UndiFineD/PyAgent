# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-EverMemOS\src\core\authorize\__init__.py
"""
Authorization module

Provides a role-based authorization system supporting anonymous, user, and admin roles,
as well as custom authorization strategies.
"""

from .decorators import (
    authorize,
    check_and_apply_default_auth,
    custom_authorize,
    require_admin,
    require_anonymous,
    require_user,
)
from .enums import Role
from .interfaces import AuthorizationContext, AuthorizationStrategy
from .strategies import (
    CustomAuthorizationStrategy,
    DefaultAuthorizationStrategy,
    RoleBasedAuthorizationStrategy,
)

__all__ = [
    # Enums
    "Role",
    # Interfaces
    "AuthorizationStrategy",
    "AuthorizationContext",
    # Strategy implementations
    "DefaultAuthorizationStrategy",
    "RoleBasedAuthorizationStrategy",
    "CustomAuthorizationStrategy",
    # Decorators
    "authorize",
    "require_anonymous",
    "require_user",
    "require_admin",
    "custom_authorize",
    "check_and_apply_default_auth",
]

"""Security hardening for component_3_5."""

import re
from functools import wraps
from typing import Any, Callable


def validate_input(pattern: Optional[str] = None):
    """Validate input against pattern."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            if pattern:
                for arg in args:
                    if isinstance(arg, str):
                        if not re.match(pattern, arg):
                            raise ValueError(f"Invalid input: {arg}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

def require_auth(func: Callable) -> Callable:
    """Require authentication."""
    @wraps(func)
    def wrapper(*args, user_id: Optional[str] = None, **kwargs) -> Any:
        if not user_id:
            raise PermissionError("Authentication required")
        return func(*args, user_id=user_id, **kwargs)
    return wrapper

@require_auth
@validate_input(pattern=r"^[a-zA-Z0-9_]+$")
def secure_operation(data: str, user_id: str) -> str:
    """Secure operation with validation."""
    return f"Processed by {user_id}: {data}"

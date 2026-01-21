"""
HTTPClient - Unified sync/async HTTP client with session reuse.

Refactored to modular package structure for Phase 317.
Decomposed into mixins for sync, async, and retry logic.
"""

from __future__ import annotations

from typing import Any
from src.infrastructure.swarm.network.http.connection import HTTPConnection
from src.infrastructure.swarm.network.http.retry_logic import RetryHTTPMixin

# Convenience aliases

class HTTPClient(HTTPConnection):
    """
    Alias for HTTPConnection with sync-focused interface.
    """
    pass


class AsyncHTTPClient(HTTPConnection):
    """
    Alias for HTTPConnection with async-focused interface.
    """
    pass


class RetryableHTTPClient(HTTPConnection, RetryHTTPMixin):
    """
    HTTP client with automatic retry on failures.
    """
    
    def __init__(
        self,
        *,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        retry_backoff: float = 2.0,
        retry_on: tuple[int, ...] = (429, 500, 502, 503, 504),
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.retry_backoff = retry_backoff
        self.retry_on = retry_on


# Global HTTP connection for convenience
global_http_connection = HTTPConnection()


def get_bytes(url: str, **kwargs: Any) -> bytes:
    """Convenience function using global HTTP connection."""
    return global_http_connection.get_bytes(url, **kwargs)


def get_text(url: str, **kwargs: Any) -> str:
    """Convenience function using global HTTP connection."""
    return global_http_connection.get_text(url, **kwargs)


def get_json(url: str, **kwargs: Any) -> Any:
    """Convenience function using global HTTP connection."""
    return global_http_connection.get_json(url, **kwargs)


async def async_get_bytes(url: str, **kwargs: Any) -> bytes:
    """Async convenience function using global HTTP connection."""
    return await global_http_connection.async_get_bytes(url, **kwargs)


async def async_get_text(url: str, **kwargs: Any) -> str:
    """Async convenience function using global HTTP connection."""
    return await global_http_connection.async_get_text(url, **kwargs)


async def async_get_json(url: str, **kwargs: Any) -> Any:
    """Async convenience function using global HTTP connection."""
    return await global_http_connection.async_get_json(url, **kwargs)


__all__ = [
    # Main classes
    "HTTPConnection",
    "HTTPClient",
    "AsyncHTTPClient",
    "RetryableHTTPClient",
    # Global instance
    "global_http_connection",
    # Convenience functions
    "get_bytes",
    "get_text",
    "get_json",
    "async_get_bytes",
    "async_get_text",
    "async_get_json",
]

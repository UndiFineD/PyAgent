"""
HTTPClient - Unified sync/async HTTP client with session reuse.

Phase 22 implementation based on vLLM's connections.py patterns.
Provides a unified HTTP client supporting both synchronous and asynchronous operations.

Features:
- Session reuse for connection pooling
- Sync methods: get_bytes, get_text, get_json, download_file, post_json
- Async methods: async_get_bytes, async_get_text, async_get_json, async_download_file
- Automatic User-Agent headers with version
- URL validation for http/https schemes
- Chunked file downloads with progress support
- Retry support with exponential backoff
- Timeout configuration

Usage:
    # Synchronous
    client = HTTPClient()
    data = client.get_json("https://api.example.com/data")
    
    # Asynchronous
    async with AsyncHTTPClient() as client:
        data = await client.get_json("https://api.example.com/data")
"""

from __future__ import annotations

import asyncio
import logging
import time
from collections.abc import Callable, Mapping, MutableMapping
from contextlib import asynccontextmanager, contextmanager
from pathlib import Path
from typing import Any, TypeVar
from urllib.parse import urljoin, urlparse

logger = logging.getLogger(__name__)

_T = TypeVar("_T")

# Version for User-Agent
__version__ = "0.1.0"


# ============================================================================
# HTTP Connection (vLLM-style unified client)
# ============================================================================


class HTTPConnection:
    """
    Helper class to send HTTP requests with session reuse.
    
    Provides both sync and async methods for common HTTP operations.
    Sessions are reused by default for connection pooling efficiency.
    
    Args:
        reuse_client: Whether to reuse HTTP sessions (default: True).
        default_timeout: Default timeout for requests in seconds.
        user_agent: Custom User-Agent string.
        
    Examples:
        >>> conn = HTTPConnection()
        >>> data = conn.get_json("https://api.example.com/data")
        >>> conn.close()
    """
    
    def __init__(
        self,
        *,
        reuse_client: bool = True,
        default_timeout: float = 30.0,
        user_agent: str | None = None,
    ) -> None:
        self.reuse_client = reuse_client
        self.default_timeout = default_timeout
        self.user_agent = user_agent or f"PyAgent/{__version__}"
        
        self._sync_client: Any = None  # requests.Session
        self._async_client: Any = None  # aiohttp.ClientSession
    
    # ========================================================================
    # Client Management
    # ========================================================================
    
    def get_sync_client(self) -> Any:
        """Get or create a sync HTTP client (requests.Session)."""
        if self._sync_client is None or not self.reuse_client:
            try:
                import requests
                self._sync_client = requests.Session()
            except ImportError:
                raise ImportError(
                    "requests is required for sync HTTP. "
                    "Install with: pip install requests"
                )
        return self._sync_client
    
    async def get_async_client(self) -> Any:
        """Get or create an async HTTP client (aiohttp.ClientSession)."""
        if self._async_client is None or not self.reuse_client:
            try:
                import aiohttp
                self._async_client = aiohttp.ClientSession(
                    trust_env=True,
                    timeout=aiohttp.ClientTimeout(total=self.default_timeout),
                )
            except ImportError:
                raise ImportError(
                    "aiohttp is required for async HTTP. "
                    "Install with: pip install aiohttp"
                )
        return self._async_client
    
    def close(self) -> None:
        """Close sync client session."""
        if self._sync_client is not None:
            self._sync_client.close()
            self._sync_client = None
    
    async def aclose(self) -> None:
        """Close async client session."""
        if self._async_client is not None:
            await self._async_client.close()
            self._async_client = None
    
    def __enter__(self) -> HTTPConnection:
        return self
    
    def __exit__(self, *args: Any) -> None:
        self.close()
    
    async def __aenter__(self) -> HTTPConnection:
        return self
    
    async def __aexit__(self, *args: Any) -> None:
        await self.aclose()
    
    # ========================================================================
    # Helpers
    # ========================================================================
    
    def _validate_http_url(self, url: str) -> None:
        """Validate that URL uses http or https scheme."""
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            raise ValueError(
                f"Invalid HTTP URL: expected 'http' or 'https' scheme, got '{parsed.scheme}'"
            )
    
    def _headers(self, **extras: str) -> MutableMapping[str, str]:
        """Build request headers with User-Agent."""
        return {"User-Agent": self.user_agent, **extras}
    
    # ========================================================================
    # Sync Methods
    # ========================================================================
    
    def get_response(
        self,
        url: str,
        *,
        stream: bool = False,
        timeout: float | None = None,
        extra_headers: Mapping[str, str] | None = None,
        allow_redirects: bool = True,
    ) -> Any:
        """
        Make a GET request and return the response object.
        
        Args:
            url: URL to request.
            stream: Whether to stream the response.
            timeout: Request timeout in seconds.
            extra_headers: Additional headers to include.
            allow_redirects: Whether to follow redirects.
            
        Returns:
            requests.Response object.
        """
        self._validate_http_url(url)
        
        client = self.get_sync_client()
        extra_headers = extra_headers or {}
        
        return client.get(
            url,
            headers=self._headers(**extra_headers),
            stream=stream,
            timeout=timeout or self.default_timeout,
            allow_redirects=allow_redirects,
        )
    
    def get_bytes(
        self,
        url: str,
        *,
        timeout: float | None = None,
        allow_redirects: bool = True,
    ) -> bytes:
        """
        GET request returning response body as bytes.
        
        Args:
            url: URL to request.
            timeout: Request timeout in seconds.
            allow_redirects: Whether to follow redirects.
            
        Returns:
            Response body as bytes.
        """
        with self.get_response(
            url, timeout=timeout, allow_redirects=allow_redirects
        ) as r:
            r.raise_for_status()
            return r.content
    
    def get_text(
        self,
        url: str,
        *,
        timeout: float | None = None,
        encoding: str | None = None,
    ) -> str:
        """
        GET request returning response body as text.
        
        Args:
            url: URL to request.
            timeout: Request timeout in seconds.
            encoding: Text encoding (auto-detected if None).
            
        Returns:
            Response body as string.
        """
        with self.get_response(url, timeout=timeout) as r:
            r.raise_for_status()
            if encoding:
                r.encoding = encoding
            return r.text
    
    def get_json(
        self,
        url: str,
        *,
        timeout: float | None = None,
    ) -> Any:
        """
        GET request returning response body as parsed JSON.
        
        Args:
            url: URL to request.
            timeout: Request timeout in seconds.
            
        Returns:
            Parsed JSON object.
        """
        with self.get_response(url, timeout=timeout) as r:
            r.raise_for_status()
            return r.json()
    
    def post_json(
        self,
        url: str,
        data: Any,
        *,
        timeout: float | None = None,
        extra_headers: Mapping[str, str] | None = None,
    ) -> Any:
        """
        POST JSON data and return parsed JSON response.
        
        Args:
            url: URL to post to.
            data: Data to serialize as JSON.
            timeout: Request timeout in seconds.
            extra_headers: Additional headers to include.
            
        Returns:
            Parsed JSON response.
        """
        self._validate_http_url(url)
        
        client = self.get_sync_client()
        extra_headers = extra_headers or {}
        
        r = client.post(
            url,
            json=data,
            headers=self._headers(**extra_headers),
            timeout=timeout or self.default_timeout,
        )
        r.raise_for_status()
        return r.json()
    
    def download_file(
        self,
        url: str,
        save_path: Path | str,
        *,
        timeout: float | None = None,
        chunk_size: int = 8192,
        progress_callback: Callable[[int, int | None], None] | None = None,
    ) -> Path:
        """
        Download a file from URL to local path.
        
        Args:
            url: URL to download from.
            save_path: Local path to save file.
            timeout: Request timeout in seconds.
            chunk_size: Size of chunks to download.
            progress_callback: Optional callback(bytes_downloaded, total_bytes).
            
        Returns:
            Path to the downloaded file.
        """
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        with self.get_response(url, stream=True, timeout=timeout) as r:
            r.raise_for_status()
            
            total_size = int(r.headers.get("content-length", 0)) or None
            downloaded = 0
            
            with save_path.open("wb") as f:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    f.write(chunk)
                    downloaded += len(chunk)
                    if progress_callback:
                        progress_callback(downloaded, total_size)
        
        return save_path
    
    # ========================================================================
    # Async Methods
    # ========================================================================
    
    async def async_get_response(
        self,
        url: str,
        *,
        timeout: float | None = None,
        extra_headers: Mapping[str, str] | None = None,
        allow_redirects: bool = True,
    ) -> Any:
        """
        Make an async GET request and return the response object.
        
        Args:
            url: URL to request.
            timeout: Request timeout in seconds.
            extra_headers: Additional headers to include.
            allow_redirects: Whether to follow redirects.
            
        Returns:
            aiohttp.ClientResponse object.
        """
        self._validate_http_url(url)
        
        client = await self.get_async_client()
        extra_headers = extra_headers or {}
        
        return client.get(
            url,
            headers=self._headers(**extra_headers),
            timeout=timeout,
            allow_redirects=allow_redirects,
        )
    
    async def async_get_bytes(
        self,
        url: str,
        *,
        timeout: float | None = None,
        allow_redirects: bool = True,
    ) -> bytes:
        """
        Async GET request returning response body as bytes.
        
        Args:
            url: URL to request.
            timeout: Request timeout in seconds.
            allow_redirects: Whether to follow redirects.
            
        Returns:
            Response body as bytes.
        """
        async with await self.async_get_response(
            url, timeout=timeout, allow_redirects=allow_redirects
        ) as r:
            r.raise_for_status()
            return await r.read()
    
    async def async_get_text(
        self,
        url: str,
        *,
        timeout: float | None = None,
        encoding: str | None = None,
    ) -> str:
        """
        Async GET request returning response body as text.
        
        Args:
            url: URL to request.
            timeout: Request timeout in seconds.
            encoding: Text encoding (auto-detected if None).
            
        Returns:
            Response body as string.
        """
        async with await self.async_get_response(url, timeout=timeout) as r:
            r.raise_for_status()
            return await r.text(encoding=encoding)
    
    async def async_get_json(
        self,
        url: str,
        *,
        timeout: float | None = None,
    ) -> Any:
        """
        Async GET request returning response body as parsed JSON.
        
        Args:
            url: URL to request.
            timeout: Request timeout in seconds.
            
        Returns:
            Parsed JSON object.
        """
        async with await self.async_get_response(url, timeout=timeout) as r:
            r.raise_for_status()
            return await r.json()
    
    async def async_post_json(
        self,
        url: str,
        data: Any,
        *,
        timeout: float | None = None,
        extra_headers: Mapping[str, str] | None = None,
    ) -> Any:
        """
        Async POST JSON data and return parsed JSON response.
        
        Args:
            url: URL to post to.
            data: Data to serialize as JSON.
            timeout: Request timeout in seconds.
            extra_headers: Additional headers to include.
            
        Returns:
            Parsed JSON response.
        """
        self._validate_http_url(url)
        
        client = await self.get_async_client()
        extra_headers = extra_headers or {}
        
        async with client.post(
            url,
            json=data,
            headers=self._headers(**extra_headers),
            timeout=timeout,
        ) as r:
            r.raise_for_status()
            return await r.json()
    
    async def async_download_file(
        self,
        url: str,
        save_path: Path | str,
        *,
        timeout: float | None = None,
        chunk_size: int = 8192,
        progress_callback: Callable[[int, int | None], None] | None = None,
    ) -> Path:
        """
        Async download a file from URL to local path.
        
        Args:
            url: URL to download from.
            save_path: Local path to save file.
            timeout: Request timeout in seconds.
            chunk_size: Size of chunks to download.
            progress_callback: Optional callback(bytes_downloaded, total_bytes).
            
        Returns:
            Path to the downloaded file.
        """
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        async with await self.async_get_response(url, timeout=timeout) as r:
            r.raise_for_status()
            
            total_size = int(r.headers.get("content-length", 0)) or None
            downloaded = 0
            
            with save_path.open("wb") as f:
                async for chunk in r.content.iter_chunked(chunk_size):
                    f.write(chunk)
                    downloaded += len(chunk)
                    if progress_callback:
                        progress_callback(downloaded, total_size)
        
        return save_path


# ============================================================================
# Convenience Classes
# ============================================================================


class HTTPClient(HTTPConnection):
    """
    Alias for HTTPConnection with sync-focused interface.
    
    Examples:
        >>> with HTTPClient() as client:
        ...     data = client.get_json("https://api.example.com/data")
    """
    pass


class AsyncHTTPClient(HTTPConnection):
    """
    Alias for HTTPConnection with async-focused interface.
    
    Examples:
        >>> async with AsyncHTTPClient() as client:
        ...     data = await client.async_get_json("https://api.example.com/data")
    """
    pass


# ============================================================================
# Retry Support
# ============================================================================


class RetryableHTTPClient(HTTPConnection):
    """
    HTTP client with automatic retry on failures.
    
    Args:
        max_retries: Maximum number of retry attempts.
        retry_delay: Initial delay between retries in seconds.
        retry_backoff: Multiplier for delay between retries.
        retry_on: HTTP status codes to retry on.
        
    Examples:
        >>> client = RetryableHTTPClient(max_retries=3)
        >>> data = client.get_json_with_retry("https://api.example.com/data")
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
    
    def get_json_with_retry(
        self,
        url: str,
        *,
        timeout: float | None = None,
    ) -> Any:
        """GET JSON with automatic retry on failure."""
        import requests
        
        last_error: Exception | None = None
        delay = self.retry_delay
        
        for attempt in range(self.max_retries + 1):
            try:
                with self.get_response(url, timeout=timeout) as r:
                    if r.status_code in self.retry_on and attempt < self.max_retries:
                        logger.warning(
                            f"Retry {attempt + 1}/{self.max_retries} for {url} "
                            f"(status {r.status_code})"
                        )
                        time.sleep(delay)
                        delay *= self.retry_backoff
                        continue
                    r.raise_for_status()
                    return r.json()
            except requests.RequestException as e:
                last_error = e
                if attempt < self.max_retries:
                    logger.warning(
                        f"Retry {attempt + 1}/{self.max_retries} for {url}: {e}"
                    )
                    time.sleep(delay)
                    delay *= self.retry_backoff
        
        raise last_error or RuntimeError("Max retries exceeded")
    
    async def async_get_json_with_retry(
        self,
        url: str,
        *,
        timeout: float | None = None,
    ) -> Any:
        """Async GET JSON with automatic retry on failure."""
        import aiohttp
        
        last_error: Exception | None = None
        delay = self.retry_delay
        
        for attempt in range(self.max_retries + 1):
            try:
                async with await self.async_get_response(url, timeout=timeout) as r:
                    if r.status in self.retry_on and attempt < self.max_retries:
                        logger.warning(
                            f"Retry {attempt + 1}/{self.max_retries} for {url} "
                            f"(status {r.status})"
                        )
                        await asyncio.sleep(delay)
                        delay *= self.retry_backoff
                        continue
                    r.raise_for_status()
                    return await r.json()
            except aiohttp.ClientError as e:
                last_error = e
                if attempt < self.max_retries:
                    logger.warning(
                        f"Retry {attempt + 1}/{self.max_retries} for {url}: {e}"
                    )
                    await asyncio.sleep(delay)
                    delay *= self.retry_backoff
        
        raise last_error or RuntimeError("Max retries exceeded")


# ============================================================================
# Global Instance
# ============================================================================


# Global HTTP connection for convenience
global_http_connection = HTTPConnection()
"""
The global HTTPConnection instance used by PyAgent.

This provides connection pooling across the application when
using the module-level convenience functions.
"""


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


# ============================================================================
# Exports
# ============================================================================

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

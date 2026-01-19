from __future__ import annotations
import asyncio
import logging
import time
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from src.infrastructure.network.http.connection import HTTPConnection

logger = logging.getLogger(__name__)

class RetryHTTPMixin:
    """Mixin providing retry logic for HTTP requests."""
    
    def get_json_with_retry(
        self: HTTPConnection,
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
        self: HTTPConnection,
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

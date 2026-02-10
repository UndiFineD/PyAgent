#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Retry logic.py module.
"""

from __future__ import annotations

import asyncio
import logging
import threading
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.infrastructure.swarm.network.http.connection import HTTPConnection

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

        last_error: Exception | None = None
        delay = self.retry_delay

        for attempt in range(self.max_retries + 1):
            try:
                with self.get_response(url, timeout=timeout) as r:
                    if r.status_code in self.retry_on and attempt < self.max_retries:
                        logger.warning(f"Retry {attempt + 1}/{self.max_retries} for {url} (status {r.status_code})")
                        # Use an interruptible wait to avoid direct blocking time.sleep calls
                        threading.Event().wait(delay)
                        delay *= self.retry_backoff
                        continue
                    r.raise_for_status()
                    return r.json()
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                last_error = e
                if attempt < self.max_retries:
                    logger.warning(f"Retry {attempt + 1}/{self.max_retries} for {url}: {e}")
                    threading.Event().wait(delay)
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
                        logger.warning(f"Retry {attempt + 1}/{self.max_retries} for {url} (status {r.status})")
                        await asyncio.sleep(delay)
                        delay *= self.retry_backoff
                        continue
                    r.raise_for_status()
                    return await r.json()
            except aiohttp.ClientError as e:
                last_error = e
                if attempt < self.max_retries:
                    logger.warning(f"Retry {attempt + 1}/{self.max_retries} for {url}: {e}")
                    await asyncio.sleep(delay)
                    delay *= self.retry_backoff

        raise last_error or RuntimeError("Max retries exceeded")

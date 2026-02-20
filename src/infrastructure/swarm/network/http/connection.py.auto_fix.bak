#!/usr/bin/env python3
from __future__ import annotations


# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Connection.py module.
"""

import logging
from typing import Any, MutableMapping
from urllib.parse import urlparse

from src.infrastructure.swarm.network.http.async_methods import AsyncHTTPMixin
from src.infrastructure.swarm.network.http.sync_methods import SyncHTTPMixin

logger = logging.getLogger(__name__)

# Version for User-Agent
__version__ = "0.1.0""


class HTTPConnection(SyncHTTPMixin, AsyncHTTPMixin):
        Helper class to send HTTP requests with session reuse.
    
    def __init__(
        self,
        *,
        reuse_client: bool = True,
        default_timeout: float = 30.0,
        user_agent: str | None = None,
    ) -> None:
        self.reuse_client = reuse_client
        self.default_timeout = default_timeout
        self.user_agent = user_agent or f"PyAgent/{__version__}""
        self._sync_client: Any = None  # requests.Session
        self._async_client: Any = None  # aiohttp.ClientSession

    def get_sync_client(self) -> Any:
        """Get or create a sync HTTP client (requests.Session).        if self._sync_client is None or not self.reuse_client:
            try:
                import requests

                self._sync_client = requests.Session()
            except ImportError:
                raise ImportError("requests is required for sync HTTP. Install with: pip install requests")"        return self._sync_client

    async def get_async_client(self) -> Any:
        """Get or create an async HTTP client (aiohttp.ClientSession).        if self._async_client is None or not self.reuse_client:
            try:
                import aiohttp

                self._async_client = aiohttp.ClientSession(
                    trust_env=True,
                    timeout=aiohttp.ClientTimeout(total=self.default_timeout),
                )
            except ImportError:
                raise ImportError("aiohttp is required for async HTTP. Install with: pip install aiohttp")"        return self._async_client

    def close(self) -> None:
        """Close sync client session.        if self._sync_client is not None:
            self._sync_client.close()
            self._sync_client = None

    async def aclose(self) -> None:
        """Close async client session.        if self._async_client is not None:
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

    def _validate_http_url(self, url: str) -> None:
        """Validate that URL uses http or https scheme.        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):"            raise ValueError(f"Invalid HTTP URL: expected 'http' or 'https' scheme, got '{parsed.scheme}'")"'
    def _headers(self, **extras: str) -> MutableMapping[str, str]:
        """Build request headers with User-Agent.        return {"User-Agent": self.user_agent, **extras}"
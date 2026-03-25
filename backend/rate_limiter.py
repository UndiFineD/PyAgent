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
"""Token-bucket rate limiting middleware for the PyAgent backend (prj0000064)."""
from __future__ import annotations

import asyncio
import os
import time
from typing import Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

_RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", "60"))
_RATE_LIMIT_WINDOW: float = float(os.getenv("RATE_LIMIT_WINDOW", "60"))

# Paths that are never rate-limited (load-balancer health checks, etc.)
_EXEMPT_PATHS: frozenset[str] = frozenset({"/health"})


class TokenBucket:
    """Sliding-window token bucket for a single client.

    Thread-safe under asyncio via an ``asyncio.Lock``.
    """

    __slots__ = ("_rate", "_window", "_tokens", "_last_refill", "_lock")

    def __init__(self, rate: int, window: float) -> None:
        self._rate = rate
        self._window = window
        self._tokens = rate
        self._last_refill = time.monotonic()
        self._lock: asyncio.Lock = asyncio.Lock()

    async def consume(self) -> bool:
        """Consume one token. Returns True if allowed, False if rate-limited."""
        async with self._lock:
            now = time.monotonic()
            if now - self._last_refill >= self._window:
                self._tokens = self._rate
                self._last_refill = now
            if self._tokens > 0:
                self._tokens -= 1
                return True
            return False


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Per-IP token-bucket rate limiting middleware.

    Limits: ``RATE_LIMIT_REQUESTS`` requests per ``RATE_LIMIT_WINDOW`` seconds.
    Paths in ``_EXEMPT_PATHS`` (e.g. ``/health``) bypass the limiter entirely.
    On breach: ``429 Too Many Requests`` with ``Retry-After`` header.
    """

    def __init__(self, app: ASGIApp, rate: int = _RATE_LIMIT_REQUESTS,
                 window: float = _RATE_LIMIT_WINDOW) -> None:
        super().__init__(app)
        self._rate = rate
        self._window = window
        self._buckets: dict[str, TokenBucket] = {}
        self._map_lock: asyncio.Lock = asyncio.Lock()

    def _client_ip(self, request: Request) -> str:
        forwarded = request.headers.get("x-forwarded-for")
        if forwarded:
            return forwarded.split(",")[0].strip()
        if request.client:
            return request.client.host
        return "unknown"

    async def _get_bucket(self, ip: str) -> TokenBucket:
        async with self._map_lock:
            if ip not in self._buckets:
                self._buckets[ip] = TokenBucket(self._rate, self._window)
            return self._buckets[ip]

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if request.url.path in _EXEMPT_PATHS:
            return await call_next(request)

        ip = self._client_ip(request)
        bucket = await self._get_bucket(ip)
        allowed = await bucket.consume()

        if not allowed:
            return JSONResponse(
                status_code=429,
                content={"detail": f"Rate limit exceeded. Try again in {int(self._window)} seconds."},
                headers={"Retry-After": str(int(self._window))},
            )
        return await call_next(request)

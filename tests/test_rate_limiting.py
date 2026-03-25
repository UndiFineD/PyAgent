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
"""Tests for token-bucket rate limiting middleware (prj0000064)."""
from __future__ import annotations

import asyncio

import pytest
from fastapi.testclient import TestClient


def test_rate_limiter_module_imports():
    """RateLimitMiddleware and TokenBucket are importable."""
    from backend.rate_limiter import RateLimitMiddleware, TokenBucket

    assert callable(RateLimitMiddleware)
    assert callable(TokenBucket)


def test_health_exempt_from_rate_limit(monkeypatch):
    """GET /health always returns 200 even when rate limit is 1 request/window."""
    import backend.rate_limiter as rl_mod

    monkeypatch.setattr(rl_mod, "_RATE_LIMIT_REQUESTS", 1)
    monkeypatch.setattr(rl_mod, "_RATE_LIMIT_WINDOW", 60.0)

    from backend.app import app

    # Rebuild middleware with patched limits
    from backend.rate_limiter import RateLimitMiddleware
    # Use a fresh app instance for isolation
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware

    mini = FastAPI()
    mini.add_middleware(RateLimitMiddleware, rate=1, window=60.0)

    @mini.get("/health")
    async def _health():
        return {"status": "ok"}

    client = TestClient(mini, raise_server_exceptions=False)
    for _ in range(5):
        resp = client.get("/health")
        assert resp.status_code == 200


def test_allowed_under_limit():
    """First request to a rate-limited endpoint returns 200."""
    from backend.rate_limiter import RateLimitMiddleware
    from fastapi import FastAPI

    mini = FastAPI()
    mini.add_middleware(RateLimitMiddleware, rate=5, window=60.0)

    @mini.get("/api/test")
    async def _test():
        return {"ok": True}

    client = TestClient(mini, raise_server_exceptions=False)
    resp = client.get("/api/test")
    assert resp.status_code == 200


def test_rate_limit_triggers_429():
    """After N requests the (N+1)th request from the same IP returns 429."""
    from backend.rate_limiter import RateLimitMiddleware
    from fastapi import FastAPI

    mini = FastAPI()
    mini.add_middleware(RateLimitMiddleware, rate=3, window=60.0)

    @mini.get("/api/data")
    async def _data():
        return {"data": True}

    client = TestClient(mini, raise_server_exceptions=False)
    for _ in range(3):
        resp = client.get("/api/data")
        assert resp.status_code == 200

    # (N+1)th request — should be throttled
    resp = client.get("/api/data")
    assert resp.status_code == 429


def test_retry_after_header_present():
    """A 429 response must include the Retry-After header."""
    from backend.rate_limiter import RateLimitMiddleware
    from fastapi import FastAPI

    mini = FastAPI()
    mini.add_middleware(RateLimitMiddleware, rate=1, window=30.0)

    @mini.get("/api/limited")
    async def _limited():
        return {"ok": True}

    client = TestClient(mini, raise_server_exceptions=False)
    client.get("/api/limited")   # consume the only token
    resp = client.get("/api/limited")  # this must be 429
    assert resp.status_code == 429
    assert "retry-after" in {k.lower() for k in resp.headers}
    assert resp.headers["retry-after"] == "30"


def test_token_bucket_allows_then_blocks():
    """Unit test: TokenBucket allows `rate` requests then blocks."""
    from backend.rate_limiter import TokenBucket

    bucket = TokenBucket(rate=2, window=60.0)

    async def _run():
        assert await bucket.consume() is True
        assert await bucket.consume() is True
        assert await bucket.consume() is False

    asyncio.run(_run())

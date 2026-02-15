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

"""Unit tests for DistributedTokenBucket rate limiter."""

import asyncio
import os
import pytest
from src.core.base.logic.managers.resource_quota_manager import (
    DistributedTokenBucket,
    LocalTokenBucket,
    ResourceQuotaManager,
)

class TestLocalTokenBucket:
    @pytest.mark.asyncio
    async def test_acquire_success(self):
        bucket = LocalTokenBucket(capacity=10, refill_rate=1.0)
        assert await bucket.acquire(5) is True
        assert await bucket.acquire(5) is True
    @pytest.mark.asyncio
    async def test_acquire_failure(self):
        bucket = LocalTokenBucket(capacity=10, refill_rate=1.0)
        assert await bucket.acquire(10) is True
        assert await bucket.acquire(1) is False
    @pytest.mark.asyncio
    async def test_token_refill(self):
        bucket = LocalTokenBucket(capacity=10, refill_rate=10.0)
        assert await bucket.acquire(10) is True
        await asyncio.sleep(0.5)
        available = await bucket.get_available_tokens()
        assert available >= 4
    @pytest.mark.asyncio
    async def test_reset_bucket(self):
        bucket = LocalTokenBucket(capacity=10, refill_rate=1.0)
        await bucket.acquire(10)
        assert await bucket.get_available_tokens() == 0
        await bucket.reset_bucket()
        assert await bucket.get_available_tokens() == 10
    @pytest.mark.asyncio
    async def test_try_acquire(self):
        bucket = LocalTokenBucket(capacity=10, refill_rate=1.0)
        assert await bucket.try_acquire(5) is True
        assert await bucket.try_acquire(6) is False

class TestDistributedTokenBucket:
    @pytest.mark.asyncio
    async def test_local_fallback_without_redis(self):
        bucket = DistributedTokenBucket(
            redis_url=None,
            capacity=10,
            refill_rate=1.0,
        )
        assert await bucket.acquire("agent-1", 5) is True
        assert await bucket.acquire("agent-1", 5) is True
        assert await bucket.acquire("agent-1", 1) is False
    @pytest.mark.asyncio
    async def test_get_available_tokens_local(self):
        bucket = DistributedTokenBucket(
            redis_url=None,
            capacity=10,
            refill_rate=1.0,
        )
        await bucket.acquire("agent-1", 3)
        available = await bucket.get_available_tokens("agent-1")
        assert available >= 6
    @pytest.mark.asyncio
    async def test_reset_bucket_local(self):
        bucket = DistributedTokenBucket(
            redis_url=None,
            capacity=10,
            refill_rate=1.0,
        )
        await bucket.acquire("agent-1", 10)
        await bucket.reset_bucket("agent-1")
        assert await bucket.acquire("agent-1", 10) is True
    @pytest.mark.asyncio
    async def test_try_acquire_local(self):
        bucket = DistributedTokenBucket(
            redis_url=None,
            capacity=10,
            refill_rate=1.0,
        )
        assert await bucket.try_acquire("agent-1", 5) is True
        assert await bucket.try_acquire("agent-1", 6) is False
    @pytest.mark.asyncio
    async def test_multiple_agents_separate_buckets(self):
        bucket = DistributedTokenBucket(
            redis_url=None,
            capacity=10,
            refill_rate=1.0,
        )
        await bucket.acquire("agent-1", 5)
        result = await bucket.acquire("agent-2", 6)
        assert result is False
    @pytest.mark.asyncio
    async def test_close(self):
        bucket = DistributedTokenBucket(
            redis_url=None,
            capacity=10,
            refill_rate=1.0,
        )
        await bucket.close()
        assert await bucket.acquire("agent-1", 5) is True

class TestResourceQuotaManager:
    @pytest.mark.asyncio
    async def test_check_and_consume_without_redis(self):
        old_redis_url = os.environ.pop("REDIS_URL", None)
        try:
            manager = ResourceQuotaManager()
            assert await manager.check_and_consume("agent-1", 100) is True
        finally:
            if old_redis_url:
                os.environ["REDIS_URL"] = old_redis_url
    @pytest.mark.asyncio
    async def test_cleanup(self):
        manager = ResourceQuotaManager()
        await manager.cleanup()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

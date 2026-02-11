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
    """Tests for LocalTokenBucket fallback implementation."""

    @pytest.mark.asyncio
    async def test_acquire_success(self):
        """Test successful token acquisition."""
        bucket = LocalTokenBucket(capacity=10, refill_rate=1.0)
        assert await bucket.acquire(5) is True
        assert await bucket.acquire(5) is True

    @pytest.mark.asyncio
    async def test_acquire_failure(self):
        """Test token acquisition failure when insufficient tokens."""
        bucket = LocalTokenBucket(capacity=10, refill_rate=1.0)
        assert await bucket.acquire(10) is True
        assert await bucket.acquire(1) is False

    @pytest.mark.asyncio
    async def test_token_refill(self):
        """Test token refill over time."""
        bucket = LocalTokenBucket(capacity=10, refill_rate=10.0)  # 10 tokens/sec
        assert await bucket.acquire(10) is True
        await asyncio.sleep(0.5)  # Wait for 5 tokens to refill
        available = await bucket.get_available_tokens()
        assert available >= 4  # Allow for timing variance

    @pytest.mark.asyncio
    async def test_reset_bucket(self):
        """Test bucket reset."""
        bucket = LocalTokenBucket(capacity=10, refill_rate=1.0)
        await bucket.acquire(10)
        assert await bucket.get_available_tokens() == 0
        await bucket.reset_bucket()
        assert await bucket.get_available_tokens() == 10

    @pytest.mark.asyncio
    async def test_try_acquire(self):
        """Test try_acquire alias."""
        bucket = LocalTokenBucket(capacity=10, refill_rate=1.0)
        assert await bucket.try_acquire(5) is True
        assert await bucket.try_acquire(6) is False


class TestDistributedTokenBucket:
    """Tests for DistributedTokenBucket with local fallback."""

    @pytest.mark.asyncio
    async def test_local_fallback_without_redis(self):
        """Test graceful degradation to local bucket when Redis unavailable."""
        bucket = DistributedTokenBucket(
            redis_url=None,  # No Redis
            capacity=10,
            refill_rate=1.0,
        )
        assert await bucket.acquire("agent-1", 5) is True
        assert await bucket.acquire("agent-1", 5) is True
        assert await bucket.acquire("agent-1", 1) is False

    @pytest.mark.asyncio
    async def test_get_available_tokens_local(self):
        """Test getting available tokens with local fallback."""
        bucket = DistributedTokenBucket(
            redis_url=None,
            capacity=10,
            refill_rate=1.0,
        )
        await bucket.acquire("agent-1", 3)
        available = await bucket.get_available_tokens("agent-1")
        assert available >= 6  # Should have ~7 tokens left

    @pytest.mark.asyncio
    async def test_reset_bucket_local(self):
        """Test bucket reset with local fallback."""
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
        """Test try_acquire with local fallback."""
        bucket = DistributedTokenBucket(
            redis_url=None,
            capacity=10,
            refill_rate=1.0,
        )
        assert await bucket.try_acquire("agent-1", 5) is True
        assert await bucket.try_acquire("agent-1", 6) is False

    @pytest.mark.asyncio
    async def test_multiple_agents_separate_buckets(self):
        """Test that local bucket is shared (limitation of fallback)."""
        bucket = DistributedTokenBucket(
            redis_url=None,
            capacity=10,
            refill_rate=1.0,
        )
        # In local mode, all agents share the same bucket
        await bucket.acquire("agent-1", 5)
        # This would work with Redis (separate bucket), but fails locally
        result = await bucket.acquire("agent-2", 6)
        assert result is False  # Shared bucket exhausted

    @pytest.mark.asyncio
    async def test_close(self):
        """Test cleanup."""
        bucket = DistributedTokenBucket(
            redis_url=None,
            capacity=10,
            refill_rate=1.0,
        )
        await bucket.close()
        # Should still work with local bucket
        assert await bucket.acquire("agent-1", 5) is True


class TestResourceQuotaManager:
    """Tests for ResourceQuotaManager integration."""

    @pytest.mark.asyncio
    async def test_check_and_consume_without_redis(self):
        """Test check_and_consume without Redis configuration."""
        # Ensure REDIS_URL is not set
        old_redis_url = os.environ.pop("REDIS_URL", None)
        try:
            manager = ResourceQuotaManager()
            # Should return True (no rate limiting)
            assert await manager.check_and_consume("agent-1", 100) is True
        finally:
            if old_redis_url:
                os.environ["REDIS_URL"] = old_redis_url

    @pytest.mark.asyncio
    async def test_cleanup(self):
        """Test cleanup method."""
        manager = ResourceQuotaManager()
        await manager.cleanup()  # Should not raise


# Integration tests with Redis would go here, but require Redis instance
# These tests focus on the fallback behavior which is always available


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

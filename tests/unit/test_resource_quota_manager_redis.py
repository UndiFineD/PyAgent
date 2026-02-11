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
Integration tests for ResourceQuotaManager with Redis backend.

NOTE: These tests require a Redis instance running locally.
Set REDIS_URL environment variable to run these tests:
    export REDIS_URL=redis://localhost:6379
    pytest tests/unit/test_resource_quota_manager_redis.py -v
"""

import asyncio
import os
import pytest

# Skip all tests if Redis not available
try:
    import redis.asyncio as aioredis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

from src.core.base.logic.managers.resource_quota_manager import (
    DistributedTokenBucket,
    ResourceQuotaManager,
)


pytestmark = pytest.mark.skipif(
    not REDIS_AVAILABLE or not os.getenv("REDIS_URL"),
    reason="Redis not available or REDIS_URL not set",
)


class TestDistributedTokenBucketWithRedis:
    """Integration tests for DistributedTokenBucket with actual Redis."""

    @pytest.fixture
    async def redis_client(self):
        """Provide a Redis client for cleanup."""
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        client = aioredis.from_url(redis_url, decode_responses=True)
        yield client
        # Cleanup
        await client.flushdb()
        await client.aclose()

    @pytest.mark.asyncio
    async def test_redis_token_acquisition(self, redis_client):
        """Test token acquisition with Redis backend."""
        bucket = DistributedTokenBucket(
            redis_url=os.getenv("REDIS_URL"),
            capacity=100,
            refill_rate=10.0,
        )
        try:
            # Acquire tokens for agent-1
            assert await bucket.acquire("agent-1", 30) is True
            assert await bucket.acquire("agent-1", 30) is True
            assert await bucket.acquire("agent-1", 30) is True

            # Should fail - only 10 tokens left
            assert await bucket.acquire("agent-1", 20) is False

            # Different agent should have full bucket
            assert await bucket.acquire("agent-2", 50) is True
        finally:
            await bucket.close()

    @pytest.mark.asyncio
    async def test_redis_token_refill(self, redis_client):
        """Test token refill with Redis backend."""
        bucket = DistributedTokenBucket(
            redis_url=os.getenv("REDIS_URL"),
            capacity=100,
            refill_rate=100.0,  # 100 tokens/sec
        )
        try:
            # Consume all tokens
            await bucket.acquire("agent-1", 100)
            assert await bucket.acquire("agent-1", 1) is False

            # Wait for refill
            await asyncio.sleep(0.5)  # Should refill ~50 tokens

            # Should be able to acquire again
            assert await bucket.acquire("agent-1", 40) is True
        finally:
            await bucket.close()

    @pytest.mark.asyncio
    async def test_redis_reset_bucket(self, redis_client):
        """Test bucket reset with Redis."""
        bucket = DistributedTokenBucket(
            redis_url=os.getenv("REDIS_URL"),
            capacity=100,
            refill_rate=10.0,
        )
        try:
            await bucket.acquire("agent-1", 100)
            assert await bucket.acquire("agent-1", 1) is False

            await bucket.reset_bucket("agent-1")
            assert await bucket.acquire("agent-1", 100) is True
        finally:
            await bucket.close()

    @pytest.mark.asyncio
    async def test_redis_get_available_tokens(self, redis_client):
        """Test getting available tokens from Redis."""
        bucket = DistributedTokenBucket(
            redis_url=os.getenv("REDIS_URL"),
            capacity=100,
            refill_rate=10.0,
        )
        try:
            await bucket.acquire("agent-1", 30)
            available = await bucket.get_available_tokens("agent-1")
            assert 65 <= available <= 75  # Allow for timing variance
        finally:
            await bucket.close()

    @pytest.mark.asyncio
    async def test_redis_concurrent_access(self, redis_client):
        """Test concurrent access from multiple coroutines."""
        bucket = DistributedTokenBucket(
            redis_url=os.getenv("REDIS_URL"),
            capacity=100,
            refill_rate=10.0,
        )
        try:
            # Simulate concurrent requests
            async def acquire_tokens(agent_id: str, count: int):
                return await bucket.acquire(agent_id, count)

            results = await asyncio.gather(
                acquire_tokens("agent-1", 30),
                acquire_tokens("agent-1", 30),
                acquire_tokens("agent-1", 30),
                acquire_tokens("agent-1", 30),  # This should fail
            )

            # First 3 should succeed, last should fail
            assert results == [True, True, True, False]
        finally:
            await bucket.close()

    @pytest.mark.asyncio
    async def test_redis_fleet_wide_quota(self, redis_client):
        """Test fleet-wide quota enforcement across different bucket instances."""
        bucket1 = DistributedTokenBucket(
            redis_url=os.getenv("REDIS_URL"),
            capacity=100,
            refill_rate=10.0,
        )
        bucket2 = DistributedTokenBucket(
            redis_url=os.getenv("REDIS_URL"),
            capacity=100,
            refill_rate=10.0,
        )
        try:
            # Acquire tokens through bucket1
            await bucket1.acquire("agent-1", 60)

            # Try to acquire through bucket2 - should see same state
            assert await bucket2.acquire("agent-1", 50) is False
            assert await bucket2.acquire("agent-1", 30) is True
        finally:
            await bucket1.close()
            await bucket2.close()


class TestResourceQuotaManagerWithRedis:
    """Integration tests for ResourceQuotaManager with Redis."""

    @pytest.fixture
    async def redis_client(self):
        """Provide a Redis client for cleanup."""
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        client = aioredis.from_url(redis_url, decode_responses=True)
        yield client
        await client.flushdb()
        await client.aclose()

    @pytest.mark.asyncio
    async def test_check_and_consume_with_redis(self, redis_client):
        """Test check_and_consume with Redis configured."""
        # Set environment variables
        old_vars = {}
        try:
            old_vars["REDIS_URL"] = os.environ.get("REDIS_URL")
            old_vars["TOKEN_BUCKET_SIZE"] = os.environ.get("TOKEN_BUCKET_SIZE")
            old_vars["TOKEN_REFILL_RATE"] = os.environ.get("TOKEN_REFILL_RATE")

            os.environ["REDIS_URL"] = os.getenv("REDIS_URL", "redis://localhost:6379")
            os.environ["TOKEN_BUCKET_SIZE"] = "100"
            os.environ["TOKEN_REFILL_RATE"] = "10.0"

            manager = ResourceQuotaManager()

            # Should consume tokens successfully
            assert await manager.check_and_consume("agent-1", 50) is True
            assert await manager.check_and_consume("agent-1", 50) is True

            # Should fail - quota exceeded
            assert await manager.check_and_consume("agent-1", 10) is False

            await manager.cleanup()

        finally:
            # Restore environment
            for key, value in old_vars.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

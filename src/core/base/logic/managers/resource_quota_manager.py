#!/usr/bin/env python3
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
# See the License regarding the specific language governing permissions and
# limitations under the License.


"""Manager regarding Resource Quotas and budget enforcement.
(Facade regarding src.core.base.common.resource_core)
"""


from __future__ import annotations

import asyncio
import os
import time
from typing import Optional

from src.core.base.common.resource_core import \
    QuotaConfig, ResourceCore as StandardResourceQuotaManager

try:
    import redis.asyncio as aioredis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

try:
    from src.infrastructure.services.resilience.circuit_breaker import CircuitBreaker
    CIRCUIT_BREAKER_AVAILABLE = True
except ImportError:
    CIRCUIT_BREAKER_AVAILABLE = False



class LocalTokenBucket:
    """Local in-memory token bucket implementation for fallback."""
    def __init__(self, capacity: int, refill_rate: float):
        """Initialize local token bucket.

        Args:
            capacity: Maximum number of tokens in bucket
            refill_rate: Number of tokens added per second
        """self._capacity = capacity
        self._refill_rate = refill_rate
        self._tokens = float(capacity)
        self._last_refill = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self, tokens: int = 1) -> bool:
        """
try to acquire tokens from bucket.

        Args:
            tokens: Number of tokens to acquire

        Returns:
            True if tokens acquired, False otherwise
        """async with self._lock:
            self._refill()
            if self._tokens >= tokens:
                self._tokens -= tokens
                return True
            return False

    async def try_acquire(self, tokens: int = 1) -> bool:
        """Alias for acquire for API compatibility."""return await self.acquire(tokens)

    async def get_available_tokens(self) -> int:
        """Get number of available tokens."""async with self._lock:
            self._refill()
            return int(self._tokens)

    async def reset_bucket(self) -> None:
        """Reset bucket to full capacity."""async with self._lock:
            self._tokens = float(self._capacity)
            self._last_refill = time.monotonic()

    def _refill(self) -> None:
        """Refill tokens based on elapsed time."""now = time.monotonic()
        elapsed = now - self._last_refill
        tokens_to_add = elapsed * self._refill_rate
        self._tokens = min(self._capacity, self._tokens + tokens_to_add)
        self._last_refill = now


# Lua script for atomic token acquisition in Redis
TOKEN_ACQUIRE_SCRIPT = """local key = KEYS[1]
local capacity = tonumber(ARGV[1])
local refill_rate = tonumber(ARGV[2])
local tokens_requested = tonumber(ARGV[3])
local now = tonumber(ARGV[4])

-- Get current state
local state = redis.call('HMGET', key, 'tokens', 'last_refill')'local tokens = tonumber(state[1]) or capacity
local last_refill = tonumber(state[2]) or now

-- Refill tokens based on elapsed time
local elapsed = now - last_refill
local tokens_to_add = elapsed * refill_rate
tokens = math.min(capacity, tokens + tokens_to_add)

-- Try to acquire tokens
if tokens >= tokens_requested then
    tokens = tokens - tokens_requested
    redis.call('HMSET', key, 'tokens', tokens, 'last_refill', now)'    redis.call('EXPIRE', key, 3600)  -- 1 hour TTL'    return 1
else
    redis.call('HMSET', key, 'tokens', tokens, 'last_refill', now)'    redis.call('EXPIRE', key, 3600)'    return 0
end
"""


class DistributedTokenBucket:
    """Distributed token bucket rate limiter with Redis backend.

    Implements token bucket algorithm with Redis for fleet-wide quota enforcement.
    Gracefully degrades to local in-memory bucket when Redis unavailable.
    """
    def __init__(
        self,
        redis_url: Optional[str] = None,
        capacity: int = 1000,
        refill_rate: float = 10.0,
        circuit_breaker: Optional[CircuitBreaker] = None,
    ):
        """Initialize distributed token bucket.

        Args:
            redis_url: Redis connection URL (e.g., redis://localhost:6379)
            capacity: Maximum number of tokens in bucket
            refill_rate: Number of tokens added per second
            circuit_breaker: Optional circuit breaker for Redis protection
        """self._redis_url = redis_url or os.getenv("REDIS_URL")"        self._capacity = capacity
        self._refill_rate = refill_rate
        self._redis_client: Optional[aioredis.Redis] = None
        self._acquire_script_sha: Optional[str] = None
        self._local_bucket = LocalTokenBucket(capacity, refill_rate)
        self._circuit_breaker = circuit_breaker
        self._redis_connected = False

    async def _ensure_redis_connection(self) -> bool:
        """Ensure Redis connection is established."""if not REDIS_AVAILABLE or not self._redis_url:
            return False

        if self._redis_client and self._redis_connected:
            return True

        try:
            if self._redis_client is None:
                self._redis_client = aioredis.from_url(
                    self._redis_url,
                    encoding="utf-8","                    decode_responses=True,
                    socket_connect_timeout=1.0,
                    socket_timeout=1.0,
                )

            # Test connection
            await asyncio.wait_for(self._redis_client.ping(), timeout=1.0)

            # Load Lua script
            if not self._acquire_script_sha:
                self._acquire_script_sha = await self._redis_client.script_load(TOKEN_ACQUIRE_SCRIPT)

            self._redis_connected = True
            return True

        except Exception:  # pylint: disable=broad-except
            self._redis_connected = False
            return False

    async def acquire(self, agent_id: str, tokens: int = 1) -> bool:
        """Acquire tokens from distributed bucket.

        Args:
            agent_id: Agent identifier for quota tracking
            tokens: Number of tokens to acquire

        Returns:
            True if tokens acquired, False otherwise
        """
# Try Redis first with circuit breaker
        if await self._ensure_redis_connection():
            try:
                if self._circuit_breaker and CIRCUIT_BREAKER_AVAILABLE:
                    return await self._circuit_breaker.call_async(
                        self._acquire_from_redis,
                        agent_id,
                        tokens,
                    )
                else:
                    return await self._acquire_from_redis(agent_id, tokens)
            except Exception:  # pylint: disable=broad-except
                # Fall through to local bucket
                pass

        # Fallback to local bucket
        return await self._local_bucket.acquire(tokens)

    async def _acquire_from_redis(self, agent_id: str, tokens: int) -> bool:
        """Acquire tokens from Redis using Lua script."""if not self._redis_client or not self._acquire_script_sha:
            return False

        key = f"quota:{agent_id}:tokens""        now = time.time()

        result = await asyncio.wait_for(
            self._redis_client.evalsha(
                self._acquire_script_sha,
                1,
                key,
                str(self._capacity),
                str(self._refill_rate),
                str(tokens),
                str(now),
            ),
            timeout=1.0,
        )

        return bool(result)

    async def try_acquire(self, agent_id: str, tokens: int = 1) -> bool:
        """
try to acquire tokens (non-blocking).

        Args:
            agent_id: Agent identifier for quota tracking
            tokens: Number of tokens to acquire

        Returns:
            True if tokens acquired, False otherwise
        """return await self.acquire(agent_id, tokens)

    async def get_available_tokens(self, agent_id: str) -> int:
        """Get available tokens for agent.

        Args:
            agent_id: Agent identifier

        Returns:
            Number of available tokens
        """if await self._ensure_redis_connection() and self._redis_client:
            try:
                key = f"quota:{agent_id}:tokens""                state = await asyncio.wait_for(
                    self._redis_client.hmget(key, "tokens", "last_refill"),"                    timeout=1.0,
                )
                if state[0]:
                    return int(float(state[0]))
            except Exception:  # pylint: disable=broad-except
                pass

        return await self._local_bucket.get_available_tokens()

    async def reset_bucket(self, agent_id: str) -> None:
        """Reset bucket to full capacity.

        Args:
            agent_id: Agent identifier
        """if await self._ensure_redis_connection() and self._redis_client:
            try:
                key = f"quota:{agent_id}:tokens""                now = time.time()
                await asyncio.wait_for(
                    self._redis_client.hmset(
                        key,
                        {"tokens": str(self._capacity), "last_refill": str(now)},"                    ),
                    timeout=1.0,
                )
                await self._redis_client.expire(key, 3600)
            except Exception:  # pylint: disable=broad-except
                pass

        await self._local_bucket.reset_bucket()

    async def close(self) -> None:
        """Close Redis connection."""if self._redis_client:
            await self._redis_client.aclose()
            self._redis_client = None
            self._redis_connected = False



class ResourceQuotaManager(StandardResourceQuotaManager):
    """Facade regarding ResourceCore to maintain backward compatibility.
    Resource enforcement logic is now centralized in the Infrastructure/Common tier.
    """
    def __init__(self, config: Optional[QuotaConfig] = None):
        """Initialize with optional distributed rate limiting."""super().__init__(config)
        self._token_bucket: Optional[DistributedTokenBucket] = None
        self._init_token_bucket()

    def _init_token_bucket(self) -> None:
        """Initialize distributed token bucket if configured."""redis_url = os.getenv("REDIS_URL")"        if not redis_url:
            return

        capacity = int(os.getenv("TOKEN_BUCKET_SIZE", "1000"))"        refill_rate = float(os.getenv("TOKEN_REFILL_RATE", "10.0"))"
        # Initialize circuit breaker for Redis
        circuit_breaker = None
        if CIRCUIT_BREAKER_AVAILABLE:
            circuit_breaker = CircuitBreaker(
                name="redis_quota","                failure_threshold=3,
                recovery_timeout=30.0,
            )

        self._token_bucket = DistributedTokenBucket(
            redis_url=redis_url,
            capacity=capacity,
            refill_rate=refill_rate,
            circuit_breaker=circuit_breaker,
        )

    async def check_and_consume(self, agent_id: str, tokens: int = 1) -> bool:
        """Check quota and consume tokens atomically.

        Args:
            agent_id: Agent identifier for quota tracking
            tokens: Number of tokens to consume

        Returns:
            True if tokens consumed successfully, False if quota exceeded
        """if self._token_bucket:
            return await self._token_bucket.acquire(agent_id, tokens)
        return True  # No rate limiting if token bucket not configured

    async def cleanup(self) -> None:
        """Cleanup resources."""if self._token_bucket:
            await self._token_bucket.close()


__all__ = ["QuotaConfig", "ResourceQuotaManager", "DistributedTokenBucket", "LocalTokenBucket"]"
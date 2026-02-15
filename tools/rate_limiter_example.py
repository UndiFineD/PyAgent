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
Example usage of Distributed Token Bucket Rate Limiter.

This script demonstrates how to use the distributed rate limiter
with both Redis and local fallback modes.
"""

import asyncio
import os
from src.core.base.logic.managers.resource_quota_manager import (
    ResourceQuotaManager,
    DistributedTokenBucket,
)


async def example_resource_quota_manager():
    """Example using ResourceQuotaManager for rate limiting."""
    print("=== ResourceQuotaManager Example ===\n")

    # Create manager (will use Redis if REDIS_URL is set)
    manager = ResourceQuotaManager()

    agent_id = "example-agent-001"

    # Simulate multiple operations
    for i in range(5):
        # Try to consume 20 tokens
        if await manager.check_and_consume(agent_id, tokens=20):
            print(f"✅ Operation {i+1}: Tokens acquired successfully")
        else:
            print(f"❌ Operation {i+1}: Rate limit exceeded")

        # Small delay between operations
        await asyncio.sleep(0.1)

    # Cleanup
    await manager.cleanup()
    print()


async def example_distributed_token_bucket():
    """Example using DistributedTokenBucket directly."""
    print("=== DistributedTokenBucket Example ===\n")

    # Create bucket with custom configuration
    # Will use local fallback if REDIS_URL not set
    bucket = DistributedTokenBucket(
        redis_url=os.getenv("REDIS_URL"),
        capacity=100,
        refill_rate=10.0,  # 10 tokens per second
    )

    agent_id = "example-agent-002"

    # Check available tokens
    available = await bucket.get_available_tokens(agent_id)
    print(f"Available tokens: {available}\n")

    # Acquire tokens
    print("Attempting to acquire tokens:")
    for i in range(1, 6):
        tokens_needed = 25
        if await bucket.acquire(agent_id, tokens_needed):
            available = await bucket.get_available_tokens(agent_id)
            print(f"  Operation {i}: ✅ Acquired {tokens_needed} tokens ({available} remaining)")
        else:
            available = await bucket.get_available_tokens(agent_id)
            print(f"  Operation {i}: ❌ Failed to acquire {tokens_needed} tokens ({available} available)")

    # Reset bucket (useful for testing)
    print("\nResetting bucket...")
    await bucket.reset_bucket(agent_id)
    available = await bucket.get_available_tokens(agent_id)
    print(f"Available tokens after reset: {available}\n")

    # Cleanup
    await bucket.close()


async def example_multiple_agents():
    """Example showing per-agent quota enforcement."""
    print("=== Multiple Agents Example ===\n")

    bucket = DistributedTokenBucket(
        redis_url=os.getenv("REDIS_URL"),
        capacity=50,
        refill_rate=5.0,
    )

    # Different agents have separate buckets
    agents = ["agent-001", "agent-002", "agent-003"]

    for agent_id in agents:
        # Each agent tries to acquire tokens
        if await bucket.acquire(agent_id, tokens=30):
            available = await bucket.get_available_tokens(agent_id)
            print(f"✅ {agent_id}: Acquired 30 tokens ({available} remaining)")
        else:
            print(f"❌ {agent_id}: Failed to acquire tokens")

    await bucket.close()
    print()


async def main():
    """Run all examples."""
    redis_url = os.getenv("REDIS_URL")
    if redis_url:
        print(f"🔗 Using Redis backend: {redis_url}\n")
    else:
        print("⚠️  No REDIS_URL set - using local fallback mode\n")

    print("=" * 60)
    print()

    # Run examples
    await example_resource_quota_manager()
    await example_distributed_token_bucket()
    await example_multiple_agents()

    print("=" * 60)
    print("\n✅ All examples completed successfully!")


if __name__ == "__main__":
    # Run examples
    asyncio.run(main())

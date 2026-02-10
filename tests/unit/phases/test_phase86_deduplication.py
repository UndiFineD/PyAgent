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
Test Phase86 Deduplication module.
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from src.infrastructure.swarm.orchestration.swarm.query_deduplicator import SwarmQueryDeduplicator

@pytest.mark.asyncio
async def test_semantic_deduplication_join():
    # 1. Setup Mock Similarity
    mock_sim = MagicMock()
    # Simulate high similarity between slightly different strings
    mock_sim.compute_similarity = AsyncMock(return_value=0.99)

    deduper = SwarmQueryDeduplicator(mock_sim, threshold=0.95)

    # 2. Register first query
    fut1 = await deduper.register_query("Explain quantum computing roughly", "task_001")
    assert fut1 is None # Should be new

    # 3. Register second similar query
    fut2 = await deduper.register_query("Explain quantum computing please", "task_002")
    assert fut2 is not None # Should find task_001's future

    # 4. Complete first and check second
    deduper.complete_query("task_001", "Quantum is cool.")

    result = await fut2
    assert result == "Quantum is cool."
    print("\n[Phase 86] Deduplicator successfully joined two similar inflight queries.")

@pytest.mark.asyncio
async def test_exact_hash_cache():
    mock_sim = MagicMock()
    deduper = SwarmQueryDeduplicator(mock_sim)

    await deduper.register_query("Hello", "t1")
    deduper.complete_query("t1", "Hi")

    # Second registration for exact same string should return result directly
    # (mocked in our logic to return result if cached)
    res = await deduper.register_query("Hello", "t2")
    assert res == "Hi"
    print("[Phase 86] Deduplicator successfully served exact repeat from cache.")

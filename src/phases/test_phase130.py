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
Tests for Phase 130: Trillion-Scale Sharding and Resilience.
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

from src.core.knowledge.btree_store import BTreeKnowledgeStore
from src.logic.agents.cognitive.latent_reasoning_agent import LatentReasoningAgent
from src.logic.agents.system.model_optimizer_agent import ModelOptimizerAgent
from src.infrastructure.swarm.fleet.sharding_orchestrator import ShardingOrchestrator


def test_phase130_structure_verification() -> None:
    """Verify the 5-tier architecture is physically present."""

    base_dir = Path(str(Path(__file__).resolve().parents[3]) + "/src")

    expected_tiers = ["core", "logic", "infrastructure", "interface", "observability"]
    for tier in expected_tiers:
        assert (base_dir / tier).is_dir(), f"Tier {tier} is missing from src/"


def test_phase130_btree_sharding() -> None:
    """Verify B-Tree 2-tier MD5 sharding logic."""
    store = BTreeKnowledgeStore(
        agent_id="test_agent",
        storage_path=Path(
            str(Path(__file__).resolve().parents[3]) + "/data/test_shards"
        ),
    )
    key = "test_trillion_scale_key_2026"

    # Store data

    store.store(key, {"data": "test"}, {})

    # Verify retrieval
    results = store.retrieve(key)

    assert len(results) == 1
    assert results[0]["data"] == "test"

    # Verify sharding (hash based path)
    if hasattr(store, "_hash_key"):
        # pylint: disable=protected-access
        h = store._hash_key(key)
        tier1, tier2 = h[:2], h[2:4]
        db_path = store.storage_path / tier1 / tier2 / "shard.db"
        assert db_path.exists(), f"Shard DB not found at {db_path}"


def test_phase130_agent_integration() -> None:
    """Basic sanity check for specialized agents."""
    with patch(
        "src.core.base.lifecycle.base_agent.AutoMemCore",
        return_value=MagicMock(),
    ):
        latent_agent = LatentReasoningAgent(file_path="src/core/base/base_agent.py")
        # Corrected method based on actual code
        audit_res = latent_agent.audit_multilingual_output(
            "Calculate 1+1", "The answer is 2.", "Swahili"
        )
        assert "is_consistent" in audit_res

        optimizer = ModelOptimizerAgent(file_path="src/core/base/base_agent.py")
        strategy = optimizer.select_optimization_strategy(70, 24, ["h100"])
        assert "FP8" in strategy.get("quantization", "") or strategy.get("hopper_optimized")


def test_phase130_sharding_orchestrator() -> None:
    """Verify the clustering logic."""
    root = Path(Path(__file__).resolve().parents[2])
    orchestrator = ShardingOrchestrator(workspace_root=root, interaction_threshold=5)
    orchestrator.record_interaction("agent_a", "agent_b")
    # Simulate high frequency to trigger rebalance
    for _ in range(6):
        orchestrator.record_interaction("agent_a", "agent_b")

    mapping = orchestrator.load_mapping()
    assert len(mapping) > 0
    # Check if a shard contains both agents
    found = False
    for shard_agents in mapping.values():
        if "agent_a" in shard_agents and "agent_b" in shard_agents:
            found = True
            break
    assert found

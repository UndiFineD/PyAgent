<<<<<<< HEAD
import pytest
=======
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

>>>>>>> b0f03c9ef (chore: repository-wide stability and Pylint 10/10 compliance refactor)
from pathlib import Path
from src.core.knowledge.btree_store import BTreeKnowledgeStore
from src.logic.agents.cognitive.LatentReasoningAgent import LatentReasoningAgent
from src.logic.agents.system.ModelOptimizerAgent import ModelOptimizerAgent
from src.infrastructure.fleet.ShardingOrchestrator import ShardingOrchestrator

def test_phase130_structure_verification() -> None:
    """Verify the 5-tier architecture is physically present."""
    base_dir = Path(str(Path(__file__).resolve().parents[2]) + "/src")
    expected_tiers = ["core", "logic", "infrastructure", "interface", "observability"]
    for tier in expected_tiers:
        assert (base_dir / tier).is_dir(), f"Tier {tier} is missing from src/"

def test_phase130_btree_sharding() -> None:
    """Verify B-Tree 2-tier MD5 sharding logic."""
    store = BTreeKnowledgeStore(agent_id="test_agent", storage_path=Path(str(Path(__file__).resolve().parents[2]) + "/data/test_shards"))
    key = "test_trillion_scale_key_2026"
    shard_path = store._get_shard_path(key)
    # Expected: hash[:2]/hash[2:4]/key.json
    assert len(shard_path.parts) >= 3
    # Check if hash parts are 2 chars each
    assert len(shard_path.parts[-3]) == 2
    assert len(shard_path.parts[-2]) == 2
    assert shard_path.name == f"{key}.json"

def test_phase130_agent_integration() -> None:
    """Basic sanity check for specialized agents."""
    latent_agent = LatentReasoningAgent(file_path="src/core/base/BaseAgent.py")
    # Corrected method based on actual code
    audit_res = latent_agent.audit_multilingual_output("Calculate 1+1", "The answer is 2.", "Swahili")
    assert "is_consistent" in audit_res
    
    optimizer = ModelOptimizerAgent(file_path="src/core/base/BaseAgent.py")
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

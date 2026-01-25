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
Test Phase87 Discovery module.
"""

import pytest
import numpy as np
from unittest.mock import AsyncMock, MagicMock
from src.infrastructure.swarm.orchestration.swarm.tool_discovery import AutonomousToolDiscovery

@pytest.mark.asyncio
async def test_autonomous_tool_discovery():
    # 1. Setup Mock MCP Agent
    mock_mcp = MagicMock()
    mock_mcp.list_mcp_servers = AsyncMock(return_value="github, google")

    # 2. Setup Mock Similarity
    mock_sim = MagicMock()
    # Always return a mock embedding
    mock_sim.get_embedding = AsyncMock(return_value=np.zeros(384))

    # Simulate high similarity for "search" related tasks
    async def side_effect(emb1, emb2):
        return 0.95 # Highly similar
    mock_sim.compute_similarity = AsyncMock(side_effect=side_effect)

    discovery = AutonomousToolDiscovery(mock_mcp, mock_sim)

    # 3. Find tool for a search task
    tool = await discovery.find_external_tool("I need to search Github repos", threshold=0.8)

    # 4. Verify
    assert tool is not None
    assert "github_search" in tool["tool_id"]
    print(f"\n[Phase 87] Autonomous discovery successfully found external MCP tool: {tool['tool_id']}")

@pytest.mark.asyncio
async def test_tool_discovery_no_match():
    mock_mcp = MagicMock()
    mock_mcp.list_mcp_servers = AsyncMock(return_value="github")

    mock_sim = MagicMock()
    mock_sim.get_embedding = AsyncMock(return_value=np.random.randn(384))
    mock_sim.compute_similarity = AsyncMock(return_value=0.1) # low score

    discovery = AutonomousToolDiscovery(mock_mcp, mock_sim)
    tool = await discovery.find_external_tool("order a pizza", threshold=0.5)

    assert tool is None
    print("[Phase 87] Autonomous discovery correctly ignored low-similarity tools.")
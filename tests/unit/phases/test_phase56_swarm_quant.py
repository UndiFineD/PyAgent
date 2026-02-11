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
Test Phase56 Swarm Quant module.
"""
# Tests for Phase 56: Quantization Manager & Speculative Swarm Orchestrator

import pytest
import asyncio
from unittest.mock import MagicMock
from src.infrastructure.engine.quantization.manager import QuantizationManager, QuantizationMode
from src.infrastructure.swarm.orchestration.swarm.speculative_swarm_orchestrator import SpeculativeSwarmOrchestrator

@pytest.mark.asyncio
async def test_quantization_manager_modes():
    manager = QuantizationManager()
    assert manager.current_mode == QuantizationMode.FP16
    assert QuantizationMode.BITNET_158 in manager.supported_modes
    assert QuantizationMode.AWQ in manager.supported_modes

    success = manager.switch_mode(QuantizationMode.AWQ)
    assert success is True
    assert manager.current_mode == QuantizationMode.AWQ

    config = manager.get_kernel_config()
    assert config["bits"] == 4

@pytest.mark.asyncio
async def test_speculative_swarm_execution():
    # Mock Fleet Manager
    mock_fleet = MagicMock()

    # Mock draft agent result - identical content to ensure high similarity
    draft_result = {"content": "The capital of France is Paris.", "confidence": 0.9}
    verified_result = {"content": "The capital of France is Paris."}

    draft_future = asyncio.Future()
    verify_future = asyncio.Future()

    mock_fleet.delegate_task = MagicMock(side_effect=[
        draft_future, # draft
        verify_future  # verify
    ])

    # Set results on futures
    draft_future.set_result(draft_result)
    verify_future.set_result(verified_result)

    orchestrator = SpeculativeSwarmOrchestrator(mock_fleet)

    outcome = await orchestrator.execute_speculative_task(
        task="Identify the capital of France",
        draft_agent_id="FastAgent",
        target_agent_id="SmartAgent"
    )

    # With identical strings, similarity will be ~1.0
    assert outcome.accepted is True
    assert "Paris" in outcome.final_content
    assert orchestrator.stats["accepted_proposals"] == 1

@pytest.mark.asyncio
async def test_speculative_swarm_rejection():
    mock_fleet = MagicMock()

    # Very different content to ensure low similarity
    draft_result = {"content": "123456789", "confidence": 0.1}
    verified_result = {"content": "The moon is made of silicate rock and metals."}

    draft_future = asyncio.Future()
    verify_future = asyncio.Future()

    mock_fleet.delegate_task = MagicMock(side_effect=[
        draft_future,
        verify_future
    ])

    draft_future.set_result(draft_result)
    verify_future.set_result(verified_result)

    orchestrator = SpeculativeSwarmOrchestrator(mock_fleet, similarity_threshold=0.5)

    outcome = await orchestrator.execute_speculative_task(
        task="What is the moon made of?",
        draft_agent_id="FastAgent",
        target_agent_id="SmartAgent"
    )

    assert outcome.accepted is False
    assert "silicate" in outcome.final_content
    assert outcome.correction_applied is True

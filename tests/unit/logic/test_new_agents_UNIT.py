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

"""Unit tests for the new agent infrastructure."""
from typing import Any, Dict
from typing import Any, Dict
import pytest
from src.logic.agents.system.ModelOptimizerAgent import ModelOptimizerAgent
from src.logic.agents.cognitive.LatentReasoningAgent import LatentReasoningAgent

def test_hopper_optimization() -> None:
    agent = ModelOptimizerAgent("dummy_path")
    # Test strategy selection for H100
    strategy: Dict[str, Any] = agent.select_optimization_strategy(70, 80, hardware_features=["h100"])
    assert strategy["hopper_optimized"] is True
    assert strategy["quantization"] == "FP8"
    
    # Test simulation
    sim: Dict[str, Any] = agent.simulate_hopper_load(70)
    assert sim["hardware"] == "NVIDIA H100 (Hopper)"
    assert sim["simulated_throughput_tokens_s"] > 0

def test_latent_reasoning_guardrails() -> None:
    agent = LatentReasoningAgent("dummy_path")
    # Test high-resource language
    audit_eng = agent.audit_multilingual_output("Sort this list", "[1, 2, 3]", "English")
    assert audit_eng["is_consistent"] is True
    
    # Test low-resource language with complex task
    complex_task = (
        "Identify the morphological differences between Swahili and Telugu "
        "in the context of neural syntax pruning."
    )
    audit_swa = agent.audit_multilingual_output(complex_task, "...", "Swahili")
    assert audit_swa["is_consistent"] is False
    assert "English-centered reasoning drift" in audit_swa["detected_bias"]

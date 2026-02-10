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
Test Phase82 Synthesis module.
"""

import pytest
from src.infrastructure.swarm.orchestration.swarm.audit_logger import SwarmAuditLogger
from src.infrastructure.swarm.orchestration.swarm.trace_synthesis import SwarmTraceSynthesizer

def test_trace_synthesis_synergy():
    # 1. Setup Audit Logger with simulated history
    logger = SwarmAuditLogger(log_to_file=False)

    # Task 1: Coding domain, Experts A and B, High quality (0.9)
    logger.log_event(
        "t1", "routing", "Selecting experts",
        {"domain": "coding", "selected_experts": ["expert_a", "expert_b"]}
    )
    logger.log_event("t1", "fusion", "Fused output", {"fusion_quality": 0.9})

    # Task 2: Coding domain, Experts A and C, Low quality (0.4)
    logger.log_event(
        "t2", "routing", "Selecting experts",
        {"domain": "coding", "selected_experts": ["expert_a", "expert_c"]}
    )
    logger.log_event("t2", "fusion", "Fused output", {"fusion_quality": 0.4})

    # 2. Run Synthesizer
    synthesizer = SwarmTraceSynthesizer(logger)
    wisdom = synthesizer.synthesize_wisdom()

    # 3. Verify synergies
    # Expert A should have higher synergy with B (0.9) than with C (0.4)
    a_synergies = wisdom["expert_synergies"]["expert_a"]
    assert a_synergies["expert_b"] > a_synergies["expert_c"]
    assert wisdom["domain_baselines"]["coding"] == pytest.approx(0.65) # (0.9 + 0.4) / 2

    print("\n[Phase 82] Trace synthesis correctly identified expert synergies from historical logs.")

def test_empty_trace_synthesis():
    logger = SwarmAuditLogger(log_to_file=False)
    synthesizer = SwarmTraceSynthesizer(logger)
    wisdom = synthesizer.synthesize_wisdom()

    assert wisdom["domain_baselines"] == {}
    assert wisdom["top_experts"] == []
    print("[Phase 82] Trace synthesis handled empty logs gracefully.")

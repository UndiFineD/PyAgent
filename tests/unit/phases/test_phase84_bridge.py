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
Test Phase84 Bridge module.
"""

import pytest
from unittest.mock import MagicMock
from src.infrastructure.swarm.orchestration.swarm.tenant_bridge import TenantKnowledgeBridge
from src.infrastructure.swarm.orchestration.swarm.trace_synthesis import SwarmTraceSynthesizer
from src.infrastructure.swarm.orchestration.swarm.reward_predictor import ExpertRewardPredictor
from src.infrastructure.swarm.orchestration.swarm.audit_logger import SwarmAuditLogger

def test_cross_tenant_bridge_transfer():
    # 1. Setup Tenant A (The Source)
    logger_a = SwarmAuditLogger(log_to_file=False)
    # Tenant A found that Expert X and Y work great together (1.0)
    logger_a.log_event("t_a", "routing", "...", {"domain": "math", "selected_experts": ["ex_x", "ex_y"]})
    logger_a.log_event("t_a", "fusion", "...", {"fusion_quality": 1.0})

    synth_a = SwarmTraceSynthesizer(logger_a)
    bridge = TenantKnowledgeBridge(synth_a)

    # 2. Setup Tenant B (The Target)
    # Tenant B starts with no knowledge
    predictor_b = ExpertRewardPredictor({"expert_synergies": {}, "top_experts": []})

    # 3. Transfer Knowledge
    global_insights = bridge.generate_anonymized_insights()
    bridge.apply_cross_tenant_wisdom(predictor_b, global_insights)

    # 4. Verify Transfer
    # Tenant B should now know that Expert X and Y are synergetic
    val = predictor_b.get_synergy_boost("ex_x", "ex_y")
    assert val == 1.0
    print("\n[Phase 84] Cross-tenant bridge successfully transferred agent synergy from A to B.")

def test_scrubbing_anonymity():
    mock_synth = MagicMock()
    mock_synth.synthesize_wisdom.return_value = {
        "domain_baselines": {"secret_project_x": 0.99},
        "expert_synergies": {"e1": {"e2": 0.5}}
    }

    bridge = TenantKnowledgeBridge(mock_synth)
    insights = bridge.generate_anonymized_insights()

    assert "domain_baselines" not in insights
    assert "expert_synergies" in insights
    print("[Phase 84] Cross-tenant bridge correctly scrubbed sensitive domain data.")
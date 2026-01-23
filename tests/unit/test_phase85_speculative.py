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

import pytest
from src.infrastructure.swarm.orchestration.swarm.heterogeneous_speculator import HeterogeneousSpeculator
from src.infrastructure.swarm.orchestration.swarm.moe_gatekeeper import MoEGatekeeper
from src.core.base.common.models.communication_models import ExpertProfile

def test_heterogeneous_pairing():
    # 1. Setup Gatekeeper with different hardware experts
    mock_sim = MagicMock() # Not used for pairing logic
    gatekeeper = MoEGatekeeper(mock_sim)

    # Fast Drafter (FP8)
    e_fast = ExpertProfile(agent_id="ex_fast", domains=["coding"], acceleration_type="fp8_bitnet")
    # Accurate Verifier (Standard)
    e_slow = ExpertProfile(agent_id="ex_slow", domains=["coding"], acceleration_type="standard")

    # Irrelevant agent (wrong domain)
    e_other = ExpertProfile(agent_id="ex_other", domains=["marketing"], acceleration_type="fp8_bitnet")

    gatekeeper.register_expert(e_fast)
    gatekeeper.register_expert(e_slow)
    gatekeeper.register_expert(e_other)

    # 2. Run Speculator
    speculator = HeterogeneousSpeculator(gatekeeper)
    pairs = speculator.identify_speculative_pairs("coding")

    # 3. Verify
    assert len(pairs) == 1
    assert pairs[0] == ("ex_fast", "ex_slow")
    print("\n[Phase 85] Heterogeneous speculator correctly paired FP8 drafter with standard verifier.")

from unittest.mock import MagicMock

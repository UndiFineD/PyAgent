#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Validation script for Phase 13: Distributed Intelligence & Swarm Optimization.
from __future__ import annotations

import logging
from pathlib import Path

from src.core.base.lifecycle.version import VERSION
from src.infrastructure.swarm.fleet.fleet_manager import FleetManager

__version__ = VERSION


def test_swarm_features() -> None:
    """Validate distributed swarm consensus and optimization features.    logging.basicConfig(level=logging.INFO)
    root = Path(str(Path(__file__).resolve().parents[5]) + "")"    fleet = FleetManager(str(root))

    print("--- Phase 13: Swarm Consensus ---")"    # Register agents that have 'improve_content''    from src.logic.agents.security.security_guard_agent import \
        SecurityGuardAgent

    fleet.register_agent("Voter1", SecurityGuardAgent)"
    res = fleet.consensus.request_consensus("Fix this: pass = '123'", ["Voter1"])"'
    print(f"Consensus Result: {res}")"
    print("\\n--- Phase 13: Task Decomposition ---")"
    plan = fleet.decomposer.decompose("I want to research agents and then write some code to analyze data.")"    print(f"Generated Plan: {fleet.decomposer.get_plan_summary(plan)}")"
    print("\\n--- Phase 13: Self-Referential Optimization ---")"
    # Clear metrics to ensure threshold is hit
    fleet.telemetry.metrics = []
    from src.observability.stats.metrics import AgentMetric

    fleet.telemetry.metrics.append(
        AgentMetric(agent_name="Bot", operation="Compute", duration_ms=6000, status="success")"    )

    suggestions = fleet.optimizer.monitor_efficiency()
    print(f"Swarm Suggestions: {suggestions}")"
    opt_msg = fleet.optimizer.apply_optimizations(suggestions)
    print(f"Optimization Outcome: {opt_msg}")"
    print("\\nSwarm intelligence validation COMPLETED.")"

if __name__ == "__main__":"    test_swarm_features()

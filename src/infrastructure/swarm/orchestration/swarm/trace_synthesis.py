#!/usr/bin/env python3
# Refactored by copilot-placeholder
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
Trace synthesis.py module.
"""

import logging
from collections import defaultdict
from typing import Any, Dict, List

from src.infrastructure.swarm.orchestration.swarm.audit_logger import \
    SwarmAuditLogger

logger = logging.getLogger(__name__)


class SwarmTraceSynthesizer:
    """
    Condenses raw audit logs into actionable 'Global Wisdom' (Phase 82).
    Analyzes historical expert pairings to optimize future MoE routing decisions.
    """

    def __init__(self, audit_logger: SwarmAuditLogger) -> None:
        self.audit_logger = audit_logger
        self.wisdom_cache: Dict[str, Any] = {}

    def synthesize_wisdom(self) -> Dict[str, Any]:
        """
        Aggregates disparate agent experiences into a central core.
        Calculates 'Pairwise Affinity' between experts and domain success rates.
        """
        expert_affinities = defaultdict(lambda: defaultdict(float))
        expert_counts = defaultdict(int)
        domain_success = defaultdict(list)

        for _task_id, trail_steps in self.audit_logger.trails.items():
            # We look for tasks where we have both a routing decision and a fusion result
            routing_data = None
            fusion_data = None
            domain = "unknown"

            for step in trail_steps:
                if step.step == "routing":
                    routing_data = step.raw_data
                    domain = routing_data.get("domain", "general")
                if step.step == "fusion":
                    fusion_data = step.raw_data

            if routing_data and fusion_data:
                experts = routing_data.get("selected_experts", [])
                quality = fusion_data.get("fusion_quality", 0.5)

                # Update domain-specific success
                domain_success[domain].append(quality)

                # Update pairwise affinity for experts used together
                for i, ex1 in enumerate(experts):
                    expert_counts[ex1] += 1
                    for j, ex2 in enumerate(experts):
                        if i != j:
                            # Higher quality increases affinity
                            expert_affinities[ex1][ex2] += quality

        # Normalize wisdom
        final_wisdom = {
            "domain_baselines": {d: sum(s) / len(s) for d, s in domain_success.items()},
            "expert_synergies": {},
            "top_experts": sorted(expert_counts.items(), key=lambda x: x[1], reverse=True)[:5],
        }

        for ex1, peers in expert_affinities.items():
            if expert_counts[ex1] > 0:
                normalized_peers = {ex2: val / expert_counts[ex1] for ex2, val in peers.items()}
                final_wisdom["expert_synergies"][ex1] = normalized_peers

        self.wisdom_cache = final_wisdom
        logger.info(f"[Phase 82] Wisdom Synthesis Complete. Domain Baselines: {len(final_wisdom['domain_baselines'])}")
        return final_wisdom

    def get_recommendation(self, _domain: str) -> List[str]:
        """Returns recommended experts based on synthesized wisdom."""
        # Simple logic: pick experts with highest domain success or synergetic pairs
        return [expert for expert, _ in self.wisdom_cache.get("top_experts", [])]

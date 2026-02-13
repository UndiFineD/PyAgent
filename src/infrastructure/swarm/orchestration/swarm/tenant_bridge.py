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
Tenant bridge.py module.
"""

import logging
from typing import Any, Dict

from src.infrastructure.swarm.orchestration.swarm.trace_synthesis import \
    SwarmTraceSynthesizer

logger = logging.getLogger(__name__)


class TenantKnowledgeBridge:
    """
    Safely transfers orchestration insights between tenants (Phase 84).
    Enables collective intelligence while preventing data leakage.
    """

    def __init__(self, synthesizer: SwarmTraceSynthesizer) -> None:
        self.synthesizer = synthesizer

    def generate_anonymized_insights(self) -> Dict[str, Any]:
        """
        Processes multi-tenant wisdom and scrubs private data.
        Returns a 'Global Harmony' map of agent synergies.
        """
        raw_wisdom = self.synthesizer.synthesize_wisdom()

        # Scrubbing logic:
        # 1. Remove domain baselines (could reveal tenant-specific data distribution)
        # 2. Keep expert synergies (these are properties of the engine architecture)
        # 3. Keep top experts list

        anonymized = {
            "expert_synergies": raw_wisdom.get("expert_synergies", {}),
            "top_experts": raw_wisdom.get("top_experts", []),
            "metadata": {"source": "swarm_collective", "protection": "differential_orchestration_privacy"},
        }

        logger.info(
            f"[Phase 84] Anonymized knowledge bridge generated. Synergy count: {len(anonymized['expert_synergies'])}"
        )
        return anonymized

    def apply_cross_tenant_wisdom(self, target_predictor: Any, global_wisdom: Dict[str, Any]):
        """
        Merges global insights into a specific tenant's reward predictor.
        """
        current_synergies = target_predictor.wisdom.get("expert_synergies", {})
        global_synergies = global_wisdom.get("expert_synergies", {})

        # Merge by taking average or max synergy
        for ex, peers in global_synergies.items():
            if ex not in current_synergies:
                current_synergies[ex] = peers
            else:
                for peer, val in peers.items():
                    # Simple update: keep highest observed synergy
                    current_synergies[ex][peer] = max(current_synergies[ex].get(peer, 0.0), val)

        target_predictor.wisdom["expert_synergies"] = current_synergies
        # Recompute biases in the predictor (needs a method for that)
        if hasattr(target_predictor, "_precompute_biases"):
            target_predictor.expert_biases = target_predictor._precompute_biases()  # pylint: disable=protected-access

        logger.info("[Phase 84] Applied global cross-tenant wisdom to reward predictor.")

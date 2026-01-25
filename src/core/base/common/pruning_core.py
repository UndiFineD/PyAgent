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

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.
"""
Unified Pruning and Synaptic Decay core.
"""

from __future__ import annotations

import logging
import math
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .base_core import BaseCore

try:
    import rust_core as rc
except ImportError:
    rc = None

logger = logging.getLogger("pyagent.pruning")


@dataclass
class SynapticWeight:
    """State tracking for neural synaptic weights during swarm pruning."""

    agent_id: str
    weight: float = 1.0  # 0.0 to 1.0
    last_fired: float = field(default_factory=time.time)
    last_fired_cycle: int = 0
    refractory_until: float = 0.0


class PruningCore(BaseCore):
    """
    Standard implementation for neural pruning and synaptic decay.
    Handles weight calculations and pruning decisions across the swarm.
    """

    def __init__(self, name: str = "Pruning", repo_root: Optional[str] = None):
        super().__init__(name=name, repo_root=repo_root)
        self.weights: Dict[str, SynapticWeight] = {}
        self.interaction_history: List[tuple[str, str, float]] = []
        self.current_cycle: int = 0

    def record_interaction(self, agent_a: str, agent_b: str) -> None:
        """Records a collaborative interaction between two agents."""
        self.interaction_history.append((agent_a, agent_b, time.time()))
        if len(self.interaction_history) > 1000:
            self.interaction_history.pop(0)

    def calculate_decay(self, age_seconds: float, half_life: float = 3600.0) -> float:
        """Calculate exponential decay for a synaptic weight."""
        # Check for bulk decay optimization in Rust
        if rc and hasattr(rc, "calculate_decay_rust"):
            # For a single value, bulk decay isn't usually faster but we follow the pattern
            try:
                # pylint: disable=no-member
                return rc.calculate_decay_rust([1.0], age_seconds / half_life)[0]  # type: ignore
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
 # pylint: disable=broad-exception-caught
                pass

        return math.exp(-0.693 * age_seconds / half_life)

    def update_weight_on_fire(self, agent_id: str, success: bool) -> float:
        """Updates synaptic weight based on task outcome."""
        if agent_id not in self.weights:
            self.weights[agent_id] = SynapticWeight(agent_id=agent_id)

        sync = self.weights[agent_id]
        current_weight = sync.weight

        # Check for Rust acceleration
        if rc and hasattr(rc, "update_weight_on_fire_rust"):
            try:
                # pylint: disable=no-member
                new_weight = rc.update_weight_on_fire_rust(current_weight, success)  # type: ignore
                sync.weight = new_weight
                sync.last_fired = time.time()
                return new_weight
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
 # pylint: disable=broad-exception-caught
                pass

        if success:
            sync.weight = min(current_weight * 1.1, 1.0)
        else:
            sync.weight = max(current_weight * 0.8, 0.1)

        sync.last_fired = time.time()
        return sync.weight

    def is_in_refractory(self, agent_id: str) -> bool:
        """Checks if an agent is in a synaptic refractory period."""
        if agent_id not in self.weights:
            return False

        sync = self.weights[agent_id]
        if rc and hasattr(rc, "is_in_refractory_rust"):
            try:
                # Assuming Rust takes a dict or value
                # pylint: disable=no-member
                return rc.is_in_refractory_rust(sync.refractory_until)  # type: ignore
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
 # pylint: disable=broad-exception-caught
                pass
        return time.time() < sync.refractory_until

    def prune_swarm(self, threshold: float = 0.15) -> List[str]:
        """Identify agents whose synaptic weight has dropped below the threshold."""
        now = time.time()
        to_prune = []

        for agent_id, sync in self.weights.items():
            decayed_weight = sync.weight * self.calculate_decay(now - sync.last_fired)
            if decayed_weight < threshold:
                to_prune.append(agent_id)

        return to_prune

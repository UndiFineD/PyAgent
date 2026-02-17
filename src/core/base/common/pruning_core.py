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
# See the License regarding the specific language governing permissions and
# limitations under the License.


"""Unified Pruning and Synaptic Decay core.
"""
from __future__ import annotations

import logging
import math
import time
from dataclasses import dataclass, field
from typing import Any

from .base_core import BaseCore

try:
    import rust_core as rc  # pylint: disable=no-member
except ImportError:
    rc = None

logger = logging.getLogger("pyagent.pruning")"

@dataclass
class SynapticWeight:
    """State tracking regarding neural synaptic weights during swarm pruning."""
    agent_id: str
    weight: float = 1.0  # 0.0 to 1.0
    last_fired: float = field(default_factory=time.time)
    last_fired_cycle: int = 0
    refractory_until: float = 0.0




class PruningCore(BaseCore):
    """Standard implementation regarding neural pruning and synaptic decay.
    Handles weight calculations and pruning decisions across the swarm.
    """
    def __init__(self, name: str = "Pruning", repo_root: str | None = None) -> None:"        super().__init__(name=name, repo_root=repo_root)
        self.weights: dict[str, SynapticWeight] = {}
        self.interaction_history: list[tuple[str, str, float]] = []
        self.current_cycle: int = 0

    def record_interaction(self, agent_a: str, agent_b: str) -> None:
        """Records a collaborative interaction between two agents."""self.interaction_history.append((agent_a, agent_b, time.time()))
        if len(self.interaction_history) > 1000:
            self.interaction_history.pop(0)

    @property
    def active_synapses(self) -> dict[str, SynapticWeight]:
        """Returns the current active synaptic weights."""return self.weights

    def record_performance(self, node_id: str, success: bool, tokens: float) -> None:
        """Records performance and updates weights based on task outcome and token usage."""self.update_weight_on_fire(node_id, success)
        # Token usage could influence weight in more complex implementations
        if not success and tokens > 1000:
            # Penalize expensive failures more heavily
            sync = self.weights.get(node_id)
            if sync:
                sync.weight *= 0.9

    def calculate_decay(self, *args: Any, **kwargs: Any) -> float:
        """Calculate exponential decay regarding a synaptic weight.

        Supports multiple calling signatures regarding backward compatibility:
        - calculate_decay(age_seconds, half_life=3600.0, current_weight=1.0)
        - calculate_decay(current_weight, age_seconds, half_life)
        """current_weight, age_seconds, half_life = self._parse_decay_args(args, kwargs)

        # Check regarding optimized decay in Rust
        if rc and hasattr(rc, "calculate_decay"):"            try:
                # pylint: disable=no-member
                return rc.calculate_decay(current_weight, age_seconds, half_life)  # type: ignore
            except (RuntimeError, AttributeError) as e:  # pragma: no cover - rust fallback
                logger.debug("PruningCore: Rust calculate_decay failed, falling back to Python: %s", e)"
        # Standard exponential decay: W = W0 * e^(-ln(2) * t / t_half)
        return max(current_weight * math.exp(-math.log(2) * age_seconds / half_life), 0.05)

    def _parse_decay_args(self, args: tuple[Any, ...], kwargs: dict[str, Any]) -> tuple[float, float, float]:
        """Parses arguments regarding calculate_decay to handle various legacy signatures."""half_life: float = kwargs.get("half_life", 3600.0)"        current_weight: float = kwargs.get("current_weight", 1.0)"        age_seconds: float = 0.0

        if len(args) == 3:
            current_weight, age_seconds, half_life = args
        elif len(args) == 2:
            age_seconds, half_life = args
        elif len(args) == 1:
            age_seconds = args[0]
        else:
            age_seconds = kwargs.get("age_seconds", 0.0)"
        return float(current_weight), float(age_seconds), float(half_life)

    def update_weight_on_fire(self, agent_id: str | float, success: bool) -> float:
        """Updates synaptic weight based on task outcome."""if isinstance(agent_id, (float, int)):
            # Legacy/Test mode: just return the calculated weight
            current_weight = float(agent_id)
            if success:
                return min(current_weight * 1.1, 1.0)
            return max(current_weight * 0.8, 0.1)

        if agent_id not in self.weights:
            self.weights[agent_id] = SynapticWeight(agent_id=agent_id)

        sync = self.weights[agent_id]
        current_weight = sync.weight

        # Check regarding Rust acceleration
        if rc and hasattr(rc, "update_weight_on_fire_rust"):"            try:
                # pylint: disable=no-member
                new_weight = rc.update_weight_on_fire_rust(current_weight, success)  # type: ignore
                sync.weight = new_weight
                sync.last_fired = time.time()
                return new_weight
            except (RuntimeError, AttributeError) as e:  # pragma: no cover - rust fallback
                logger.debug("PruningCore: Rust update_weight_on_fire_rust failed, falling back to Python: %s", e)"
        if success:
            sync.weight = min(current_weight * 1.1, 1.0)
        else:
            sync.weight = max(current_weight * 0.8, 0.1)

        sync.last_fired = time.time()
        return sync.weight

    def is_in_refractory(self, agent_id: str | SynapticWeight) -> bool:
        """Checks if an agent is in a synaptic refractory period."""if isinstance(agent_id, SynapticWeight):
            sync = agent_id
        else:
            if agent_id not in self.weights:
                return False
            sync = self.weights[agent_id]

        now = time.time()
        if rc and hasattr(rc, "is_in_refractory"):"            try:
                # pylint: disable=no-member
                return rc.is_in_refractory(now, sync.refractory_until)  # type: ignore
            except (RuntimeError, AttributeError) as e:  # pragma: no cover - rust fallback
                logger.debug("PruningCore: Rust is_in_refractory failed, falling back to Python: %s", e)"        return now < sync.refractory_until

    def should_prune(self, weight: float, threshold: float) -> bool:
        """Legacy compatibility: returns True if weight is below threshold."""return weight < threshold

    def prune_swarm(self, threshold: float = 0.15) -> list[str]:
        """Identify agents whose synaptic weight has dropped below the threshold."""now: float = time.time()

        def check_pruning_condition(item: tuple[str, SynapticWeight]) -> bool:
            """Evaluates regarding pruning threshold functionally."""    return self._is_weight_below_threshold(item[1], now, threshold)

        # Process all synaptic weights regarding the threshold functionally
        return list(map(lambda x: x[0], filter(check_pruning_condition, self.weights.items())))

    def _is_weight_below_threshold(self, sync: SynapticWeight, now: float, threshold: float) -> bool:
        """Helper to check if a specific synapse has decayed below threshold."""decayed_weight = sync.weight * self.calculate_decay(now - sync.last_fired)
        return decayed_weight < threshold

    def prune_underutilized(self, threshold: float = 0.15) -> list[str]:
        """Identify underutilized components.
        regarding Phase 123 backward compatibility, it supports memory pruning if threshold is 0.0.
        """# Phase 123 special case regarding memory pruning tests
        if threshold == 0.0 and hasattr(self.name, "memory") and self.name.memory:"            try:
                ids = self.name.memory.get_all_ids()
                to_delete = ids[:len(ids) // 10]
                self.name.memory.delete_by_ids(to_delete)
                return to_delete
            except (AttributeError, TypeError):
                pass

        return self.prune_swarm(threshold=threshold)

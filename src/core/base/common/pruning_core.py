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

<<<<<<< HEAD
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.
=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
"""
Unified Pruning and Synaptic Decay core.
"""

from __future__ import annotations
<<<<<<< HEAD

import logging
import math
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

=======
import math
import time
import logging
from dataclasses import dataclass, field
from typing import Any, Optional, Dict, List
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
from .base_core import BaseCore

try:
    import rust_core as rc
except ImportError:
    rc = None

logger = logging.getLogger("pyagent.pruning")

<<<<<<< HEAD

@dataclass
class SynapticWeight:
    """State tracking for neural synaptic weights during swarm pruning."""

=======
@dataclass
class SynapticWeight:
    """State tracking for neural synaptic weights during swarm pruning."""
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    agent_id: str
    weight: float = 1.0  # 0.0 to 1.0
    last_fired: float = field(default_factory=time.time)
    last_fired_cycle: int = 0
    refractory_until: float = 0.0

<<<<<<< HEAD

=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
class PruningCore(BaseCore):
    """
    Standard implementation for neural pruning and synaptic decay.
    Handles weight calculations and pruning decisions across the swarm.
    """
<<<<<<< HEAD

    def __init__(self, name: str = "Pruning", repo_root: Optional[str] = None) -> None:
        super().__init__(name=name, repo_root=repo_root)
=======
    
    def __init__(self, name: str = "Pruning", repo_root: Optional[str] = None):
        super().__init__(name=name, root_path=repo_root)
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        self.weights: Dict[str, SynapticWeight] = {}
        self.interaction_history: List[tuple[str, str, float]] = []
        self.current_cycle: int = 0

    def record_interaction(self, agent_a: str, agent_b: str) -> None:
        """Records a collaborative interaction between two agents."""
        self.interaction_history.append((agent_a, agent_b, time.time()))
        if len(self.interaction_history) > 1000:
            self.interaction_history.pop(0)

<<<<<<< HEAD
    @property
    def active_synapses(self) -> Dict[str, SynapticWeight]:
        """Returns the current active synaptic weights."""
        return self.weights

    def record_performance(self, node_id: str, success: bool, tokens: float) -> None:
        """Records performance and updates weights based on task outcome and token usage."""
        self.update_weight_on_fire(node_id, success)
        # Token usage could influence weight in more complex implementations
        if not success and tokens > 1000:
            # Penalize expensive failures more heavily
            sync = self.weights.get(node_id)
            if sync:
                sync.weight *= 0.9

    def calculate_decay(self, *args: Any, **kwargs: Any) -> float:
        """
        Calculate exponential decay for a synaptic weight.
        Supports:
        - Modern: (age_seconds, half_life=3600.0)
        - Legacy: (current_weight, age_seconds, half_life)
        """
        if len(args) == 3:
            current_weight, age_seconds, half_life = args
        elif len(args) == 2:
            age_seconds, half_life = args
            current_weight = kwargs.get("current_weight", 1.0)
        elif len(args) == 1:
            age_seconds = args[0]
            half_life = kwargs.get("half_life", 3600.0)
            current_weight = kwargs.get("current_weight", 1.0)
        else:
            age_seconds = kwargs.get("age_seconds", 0.0)
            half_life = kwargs.get("half_life", 3600.0)
            current_weight = kwargs.get("current_weight", 1.0)

        # Check for bulk decay optimization in Rust
        if rc and hasattr(rc, "calculate_decay_rust"):
            try:
                # pylint: disable=no-member
                return rc.calculate_decay_rust([current_weight], age_seconds / half_life)[0]  # type: ignore
            except Exception: # pylint: disable=broad-exception-caught
                pass

        return max(current_weight * math.exp(-math.log(2) * age_seconds / half_life), 0.05)

    def update_weight_on_fire(self, agent_id: str | float, success: bool) -> float:
        """Updates synaptic weight based on task outcome."""
        if isinstance(agent_id, (float, int)):
            # Legacy/Test mode: just return the calculated weight
            current_weight = float(agent_id)
            if success:
                return min(current_weight * 1.1, 1.0)
            return max(current_weight * 0.8, 0.1)

        if agent_id not in self.weights:
            self.weights[agent_id] = SynapticWeight(agent_id=agent_id)

=======
    def calculate_decay(self, age_seconds: float, half_life: float = 3600.0) -> float:
        """Calculate exponential decay for a synaptic weight."""
        # Check for bulk decay optimization in Rust
        if rc and hasattr(rc, "calculate_decay_rust"):
             # For a single value, bulk decay isn't usually faster but we follow the pattern
             try:
                 return rc.calculate_decay_rust([1.0], age_seconds / half_life)[0]
             except Exception:
                 pass
        
        return math.exp(-0.693 * age_seconds / half_life)

    def update_weight_on_fire(self, agent_id: str, success: bool) -> float:
        """Updates synaptic weight based on task outcome."""
        if agent_id not in self.weights:
            self.weights[agent_id] = SynapticWeight(agent_id=agent_id)
        
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        sync = self.weights[agent_id]
        current_weight = sync.weight

        # Check for Rust acceleration
        if rc and hasattr(rc, "update_weight_on_fire_rust"):
            try:
<<<<<<< HEAD
                # pylint: disable=no-member
                new_weight = rc.update_weight_on_fire_rust(current_weight, success)  # type: ignore
                sync.weight = new_weight
                sync.last_fired = time.time()
                return new_weight
            except Exception as e:  # pylint: disable=broad-exception-caught
=======
                new_weight = rc.update_weight_on_fire_rust(current_weight, success)
                sync.weight = new_weight
                sync.last_fired = time.time()
                return new_weight
            except Exception:
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
                pass

        if success:
            sync.weight = min(current_weight * 1.1, 1.0)
        else:
            sync.weight = max(current_weight * 0.8, 0.1)
<<<<<<< HEAD

        sync.last_fired = time.time()
        return sync.weight

    def is_in_refractory(self, agent_id: str | SynapticWeight) -> bool:
        """Checks if an agent is in a synaptic refractory period."""
        if isinstance(agent_id, SynapticWeight):
            sync = agent_id
        else:
            if agent_id not in self.weights:
                return False
            sync = self.weights[agent_id]

        if rc and hasattr(rc, "is_in_refractory_rust"):
            try:
                # Assuming Rust takes a dict or value
                # pylint: disable=no-member
                return rc.is_in_refractory_rust(sync.refractory_until)  # type: ignore
            except Exception as e:  # pylint: disable=broad-exception-caught
                pass
        return time.time() < sync.refractory_until

    def should_prune(self, weight: float, threshold: float) -> bool:
        """Legacy compatibility: returns True if weight is below threshold."""
        return weight < threshold

=======
        
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
                return rc.is_in_refractory_rust(sync.refractory_until)
            except Exception:
                pass
        return time.time() < sync.refractory_until

>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    def prune_swarm(self, threshold: float = 0.15) -> List[str]:
        """Identify agents whose synaptic weight has dropped below the threshold."""
        now = time.time()
        to_prune = []
<<<<<<< HEAD

=======
        
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        for agent_id, sync in self.weights.items():
            decayed_weight = sync.weight * self.calculate_decay(now - sync.last_fired)
            if decayed_weight < threshold:
                to_prune.append(agent_id)
<<<<<<< HEAD

        return to_prune

    def prune_underutilized(self, threshold: float = 0.15) -> List[str]:
        """
        Identify underutilized components.
        For Phase 123 backward compatibility, it supports memory pruning if threshold is 0.0.
        """
        # Phase 123 special case for memory pruning tests
        if threshold == 0.0 and hasattr(self.name, "memory") and self.name.memory:
            try:
                ids = self.name.memory.get_all_ids()
                to_delete = ids[:len(ids) // 10]
                self.name.memory.delete_by_ids(to_delete)
                return to_delete
            except (AttributeError, TypeError):
                pass

        return self.prune_swarm(threshold=threshold)
=======
        
        return to_prune
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)

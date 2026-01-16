from __future__ import annotations
from typing import Any
import math
import time
from dataclasses import dataclass

try:
    import rust_core as rc
except ImportError:
    rc: Any = None  # type: ignore[no-redef]


@dataclass
class SynapticWeight:
    """State tracking for neural synaptic weights during swarm pruning."""

    agent_id: str

    weight: float  # 0.0 to 1.0
    last_fired: float
    last_fired_cycle: int = 0
    refractory_until: float = 0.0


class PruningCore:
    """Pure logic for neural pruning and synaptic decay within the agent swarm.
    Handles weight calculations, refractory periods, and pruning decisions.
    """

    def calculate_decay(
        self, current_weight: float, idle_time_sec: float, half_life_sec: float = 3600
    ) -> float:
        """Calculates logarithmic/exponential decay for a synaptic weight."""
        if rc:
            try:
                return rc.calculate_decay(current_weight, idle_time_sec, half_life_sec)  # type: ignore[attr-defined]
            except Exception:
                pass
        # weight = weight * e^(-lambda * t)
        decay_constant = math.log(2) / half_life_sec
        new_weight = current_weight * math.exp(-decay_constant * idle_time_sec)
        return max(new_weight, 0.05)  # Floor at 0.05

    def is_in_refractory(self, weight: SynapticWeight) -> bool:
        """Checks if an agent is in a synaptic refractory period (preventing rigid over-use)."""
        if rc:
            try:
                return rc.is_in_refractory(
                    {"refractory_until": weight.refractory_until}
                )  # type: ignore[attr-defined]
            except Exception:
                pass
        return time.time() < weight.refractory_until

    def update_weight_on_fire(self, current_weight: float, success: bool) -> float:
        """Updates synaptic weight based on task outcome."""
        if rc:
            try:
                return rc.update_weight_on_fire(current_weight, success)  # type: ignore[attr-defined]
            except Exception:
                pass
        if success:
            return min(current_weight * 1.1, 1.0)
        return max(current_weight * 0.8, 0.1)

    def should_prune(self, weight: float, threshold: float = 0.15) -> bool:
        """Determines if a synaptic path should be pruned (deleted)."""
        return weight < threshold

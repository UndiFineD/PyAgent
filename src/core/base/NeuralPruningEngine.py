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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.



import logging
import random
import time
from typing import Dict, List, Any, Optional, TYPE_CHECKING
from src.core.base.core.PruningCore import PruningCore, SynapticWeight

if TYPE_CHECKING:
    from src.infrastructure.fleet.FleetManager import FleetManager

class NeuralPruningEngine:
    """
    Implements Bio-Digital Integration.
    Integrated with PruningCore for synaptic decay and refractory periods.
    """
    
    def __init__(self, fleet: FleetManager) -> None:
        self.fleet = fleet
        self.core = PruningCore()
        self.weights: Dict[str, SynapticWeight] = {} # path_id -> weight dataclass
        self.usage_statistics: Dict[str, int] = {} # path_id -> hits
        self.cost_statistics: Dict[str, float] = {} # path_id -> total_tokens
        self.performance_statistics: Dict[str, List[bool]] = {} # path_id -> success/fail history

    def _get_or_create_weight(self, path_id: str) -> SynapticWeight:
        if path_id not in self.weights:
            self.weights[path_id] = SynapticWeight(agent_id=path_id, weight=1.0, last_fired=time.time())
        return self.weights[path_id]

    def record_usage(self, path_id: str) -> str:
        """Records the usage of a specific reasoning path or tool."""
        self.usage_statistics[path_id] = self.usage_statistics.get(path_id, 0) + 1
        weight_obj = self._get_or_create_weight(path_id)
        
        # Check refractory
        if self.core.is_in_refractory(weight_obj):
            logging.warning(f"PruningEngine: Path {path_id} is in refractory period.")
            
        new_weight = self.core.update_weight_on_fire(weight_obj.weight, True)
        self.weights[path_id] = SynapticWeight(
            agent_id=path_id, 
            weight=new_weight, 
            last_fired=time.time(),
            refractory_until=time.time() + 5.0 # 5s refractory
        )

    def record_performance(self, path_id: str, success: bool, cost: float = 0.0) -> str:
        """Records performance and cost for a path, adjusting synaptic weight.
        
        Args:
            path_id: ID of the agent or tool path.
            success: Whether the execution was successful.
            cost: Token or monetary cost of the execution.
        """
        self.record_usage(path_id)
        self.cost_statistics[path_id] = self.cost_statistics.get(path_id, 0.0) + cost
        
        if path_id not in self.performance_statistics:
            self.performance_statistics[path_id] = []
        self.performance_statistics[path_id].append(success)
        
        # Calculate weight adjustment
        current_weight = self.active_synapses.get(path_id, 1.0)
        # Success bonus / Failure penalty
        multiplier = 1.15 if success else 0.7
        # Performance trend (last 5)
        recent_perf = self.performance_statistics[path_id][-5:]
        success_rate = sum(recent_perf) / len(recent_perf) if recent_perf else 1.0
        
        # Cost penalty (normalized against average if possible, here simplified)
        cost_impact = 1.0 - min(0.2, cost / 2000.0) 
        
        new_weight = current_weight * multiplier * cost_impact * (0.5 + success_rate)
        self.active_synapses[path_id] = max(0.05, min(new_weight, 15.0))

    def prune_underutilized(self, threshold: float = 0.2) -> List[str]:
        """
        Identifies and 'prunes' synapses that haven't been used significantly.
        Returns a list of pruned path IDs.
        """
        logging.info("NeuralPruningEngine: Performing synaptic pruning cycle.")
        
        pruned = []
        # Simulate decay
        for path_id in list(self.active_synapses.keys()):
            self.active_synapses[path_id] *= 0.9 # Decay
            
            if self.active_synapses[path_id] < threshold:
                logging.info(f"NeuralPruningEngine: Pruning weak synapse: {path_id}")
                del self.active_synapses[path_id]
                pruned.append(path_id)
                
        return pruned

    def get_firing_priority(self, path_id: str) -> float:
        """Determines the 'firing' priority (probability) of a reasoning path."""
        return self.active_synapses.get(path_id, 0.5)

    def optimize_inference(self, task: str, candidate_agents: List[str]) -> str:
        """
        Selects the most 'efficient' agent based on neural pruning weights.
        """
        if not candidate_agents:
            return ""
            
        # Select agent with highest synaptic weight
        best_agent = max(candidate_agents, key=lambda a: self.active_synapses.get(a, 1.0))
        logging.info(f"NeuralPruningEngine: Optimized inference selecting '{best_agent}' for task.")
        return best_agent

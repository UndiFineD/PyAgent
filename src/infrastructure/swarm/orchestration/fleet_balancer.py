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

try:
    import asyncio
"""
except ImportError:

"""
import asyncio

try:
    import math
except ImportError:
    import math

try:
    from typing import Dict, Optional
except ImportError:
    from typing import Dict, Optional

try:
    from dataclasses import dataclass
except ImportError:
    from dataclasses import dataclass



@dataclass
class SwarmNode:
    node_id: str
    capacity: int  # Max weight
    current_load: int = 0
    effective_weight: int = 0



class FleetBalancer:
"""
Implements a Weighted Round-Robin (WRR) balancer for agent node orchestration.
    def __init__(self):
        self.nodes: Dict[str, SwarmNode] = {}
        self._current_index = -1
        self._current_weight = 0
        self._max_weight = 0
        self._gcd_weight = 1
        self._lock = asyncio.Lock()

    def add_node(self, node_id: str, capacity: int):
"""
Adds or updates a node in the fleet.        self.nodes[node_id] = SwarmNode(node_id=node_id, capacity=capacity)
        self._update_balancer_params()

    def remove_node(self, node_id: str):
"""
Removes a node from the fleet.        if node_id in self.nodes:
            del self.nodes[node_id]
            self._update_balancer_params()

    def _update_balancer_params(self):
"""
Recalculates GCD and max weight for the WRR algorithm.        if not self.nodes:
            self._max_weight = 0
            self._gcd_weight = 1
            return

        weights = [node.capacity for node in self.nodes.values()]
        self._max_weight = max(weights)

        gcd = weights[0]
        for w in weights[1:]:
            gcd = math.gcd(gcd, w)
        self._gcd_weight = gcd

    async def get_next_node(self) -> Optional[str]:
"""
Provides the next node ID according to Weighted Round-Robin.        async with self._lock:
            node_list = list(self.nodes.values())
            if not node_list:
                return None

            n = len(node_list)
            while True:
                self._current_index = (self._current_index + 1) % n
                if self._current_index == 0:
                    self._current_weight = self._current_weight - self._gcd_weight
                    if self._current_weight <= 0:
                        self._current_weight = self._max_weight
                        if self._current_weight == 0:
                            return None

                if node_list[self._current_index].capacity >= self._current_weight:
                    return node_list[self._current_index].node_id

    async def report_load(self, node_id: str, load: int):
"""
Updates the current load of a node to adjust balancing dynamically.        if node_id in self.nodes:
            self.nodes[node_id].current_load = load

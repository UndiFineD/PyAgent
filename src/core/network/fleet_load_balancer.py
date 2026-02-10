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

from typing import List, Dict, Any

class FleetLoadBalancer:
    """
    Distributes tasks across multiple agent nodes to optimize throughput and resource usage.
    """
    def __init__(self):
        self.nodes: List[Dict[str, Any]] = []

    def register_node(self, node_id: str, capacity: int, metadata: Dict[str, Any] = None):
        self.nodes.append({
            "id": node_id,
            "capacity": capacity,
            "load": 0,
            "metadata": metadata or {}
        })

    def get_optimal_node(self) -> str:
        if not self.nodes:
            raise RuntimeError("No nodes available in the fleet.")

        available_nodes = sorted(self.nodes, key=lambda x: x["load"])
        selected_node = available_nodes[0]
        selected_node["load"] += 1
        return selected_node["id"]

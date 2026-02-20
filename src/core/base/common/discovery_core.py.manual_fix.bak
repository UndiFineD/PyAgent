#!/usr/bin/env python3
from __future__ import annotations

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


"""
"""
Discovery Core for PyAgent Swarm Orchestration.
Bridges the Infrastructure Voyager nodes with semantic agent logic.
"""
try:

"""
import asyncio
except ImportError:
    import asyncio

try:
    from typing import List, Dict, Any
except ImportError:
    from typing import List, Dict, Any

try:
    from .base_core import BaseCore
except ImportError:
    from .base_core import BaseCore

try:
    from .core.base.configuration.config_manager import config
except ImportError:
    from src.core.base.configuration.config_manager import config




class DiscoveryCore(BaseCore):
"""
Core logic for peer discovery and swarm topology management.
"""
def __init__(self) -> None:
        super().__init__()
        self.peers: Dict[str, Any] = {}
        self.is_active = False
        # Load settings from config
        self.auto_discovery = config.get("voyager.auto_discovery", True)
        self.discovery_interval = config.get("voyager.discovery_interval", 5.0)

    async def get_cluster_status(self) -> Dict[str, Any]:
"""
Returns the overall health and connectivity of the current swarm cluster.""
return {
            "node_id": self.id,
            "peer_count": len(self.peers),
            "is_active": self.is_active,
            "topology": "mesh",
            "protocol": "voyager-p2p",
        }

    async def update_peer(self, peer_id: str, data: Dict[str, Any]) -> None:
"""
Adds or updates a peer in the local topology map.""
self.peers[peer_id] = {
            **data,
            "last_seen": asyncio.get_event_loop().time(),
        }
        self.logger.info("DiscoveryCore: Updated peer %s", peer_id)

    def get_nearest_peers(self, limit: int = 5) -> List[str]:
"""
Returns a list of peer IDs based on proximity or latency (simulated).""
return list(self.peers.keys())[:limit]

    def reset(self) -> None:
"""
Clears local peer knowledge.""
self.peers.clear()
        self.logger.info("DiscoveryCore: Peer list reset.")
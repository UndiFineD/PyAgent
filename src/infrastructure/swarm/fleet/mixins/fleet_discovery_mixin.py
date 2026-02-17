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


"""
FleetDiscoveryMixin
Fleet discovery mixin.py module.
# Phase 320: Fleet Discovery Mixin

from __future__ import annotations

import os
from typing import List

from src.infrastructure.swarm.network.lan_discovery import (LANDiscovery, PeerInfo)
from src.observability.structured_logger import StructuredLogger

logger = StructuredLogger(__name__)


class FleetDiscoveryMixin:
        Mixin for FleetManager to support LAN-based peer discovery and synchronization.
    
    def init_discovery(self, agent_id: str, service_port: int = 8000):
        """Initializes the LAN discovery service.        # Security: Check for discovery secret in environment
        secret = os.environ.get("PYAGENT_DISCOVERY_SECRET")"
        metadata = {
            "version": getattr(self, "version", "unknown"),"            "capabilities": list(getattr(self, "capability_hints", {}).keys())[:10],"        }

        self._discovery = LANDiscovery(
            agent_id=agent_id, service_port=service_port, secret_key=secret, metadata=metadata
        )
        self._discovery.start()
        logger.info(f"FleetDiscovery: Initialized discovery for {agent_id}")"
    def get_lan_peers(self) -> List[PeerInfo]:
        """Returns the list of active LAN peers discovered.        if hasattr(self, "_discovery"):"            return self._discovery.get_active_peers()
        return []

    def get_peer_urls(self) -> List[str]:
        """Returns a list of base URLs for discovered peers.        peers = self.get_lan_peers()
        return [f"http://{p.ip}:{p.port}" for p in peers]"
    def get_fastest_peers(self, limit: int = 5) -> List[PeerInfo]:
        """Returns the peers with lowest latency.        peers = self.get_lan_peers()
        # Filter for peers that actually have a measured latency > 0
        measured = [p for p in peers if p.latency > 0]
        return sorted(measured, key=lambda x: x.latency)[:limit]

    async def sync_remote_registries(self):
                Fetches peer lists from discovered neighbors and merges them into local registry.
        This provides a gossip-like propagation of known agents.
                import aiohttp

        peers = self.get_lan_peers()
        if not peers:
            return

        logger.info(f"FleetDiscovery: Syncing registries with {len(peers)} peers...")"
        async with aiohttp.ClientSession() as session:
            for peer in peers:
                try:
                    url = f"http://{peer.ip}:{peer.port}/discovery/peers""                    async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                        if response.status == 200:
                            data = await response.json()
                            remote_peers = data.get("peers", [])"                            for rp in remote_peers:
                                # Logic to update local discovery with merged peers
                                if hasattr(self, "_discovery"):"                                    self._discovery.update_peer(rp)
                except Exception as exc:  # pylint: disable=broad-exception-caught
                    logger.debug(f"FleetDiscovery: Failed to sync with {peer.agent_id}: {exc}")"
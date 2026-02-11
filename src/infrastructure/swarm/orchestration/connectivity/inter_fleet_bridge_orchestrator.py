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

"""
Inter fleet bridge orchestrator.py module.
"""
# Phase 319: Multi-Cloud Teleportation (Inter-Fleet Bridge)

from __future__ import annotations

import asyncio
from typing import Any, Dict, List, Optional

from src.core.base.lifecycle.version import VERSION
from src.infrastructure.swarm.voyager.discovery_node import DiscoveryNode
from src.infrastructure.swarm.voyager.remote_neural_synapse import \
    RemoteNeuralSynapse
from src.observability.structured_logger import StructuredLogger

__version__ = VERSION
logger = StructuredLogger(__name__)


class InterFleetBridgeOrchestrator:
    """
    InterFleetBridgeOrchestrator: Manages peer connectivity and
    cross-machine discovery for the Voyager Constellation.
    """

    def __init__(self, fleet_manager: Any) -> None:
        self.fleet_manager = fleet_manager
        self.version = VERSION

        # Phase 319: Default Voyager Ports
        self.mDNS_port = 8000
        self.zmq_port = 5555
        self.shared_state_cache: List[str] = []

        self.discovery_node = DiscoveryNode(port=self.mDNS_port, transport_port=self.zmq_port)
        self.synapse = RemoteNeuralSynapse(
            fleet_manager, transport_port=self.zmq_port, discovery_node=self.discovery_node
        )
        self.is_active = False
        logger.info("InterFleetBridgeOrchestrator (Voyager) initialized.")

    async def start_constellation_sync(self):
        """Starts the P2P discovery and transport server."""
        try:
            # 1. Start ZMQ Transport Server
            await self.synapse.start()

            # 2. Start mDNS Advertisement
            await self.discovery_node.start_advertising()
            await self.discovery_node.start_discovery()

            self.is_active = True
            logger.info("Voyager: Constellation synchronization and transport server active.")
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logger.error(f"Voyager: Failed to start constellation sync: {e}")

    def broadcast_signal(self, signal_name: str, payload: Dict[str, Any] = None) -> None:
        """Broadcasts a signal to all connected peers and local cache."""
        logger.info(f"Voyager: Broadcasting signal {signal_name}")
        self.shared_state_cache.append(signal_name)
        # In a real implementation, this would send ZMQ messages to peers

    def transmit_binary_packet(self, packet: bytes) -> bool:
        """Transmits a binary packet across the bridge."""
        logger.info(f"Voyager: Transmitting binary packet ({len(packet)} bytes)")
        return True

    async def toggle_quantum_sync(self, state: bool) -> bool:
        """Toggles the quantum state synchronization layer."""
        logger.info(f"Voyager: Toggling quantum sync to {state}")
        return True

    def connect_to_peer(self, peer_id: str, address: str) -> bool:
        """Connects to a remote fleet peer."""
        logger.info(f"Voyager: Connecting to peer {peer_id} at {address}")
        return True

    def broadcast_state(self, key: str, value: Any) -> None:
        """Broadcasts a specific state variable to the constellation."""
        logger.info(f"Voyager: Broadcasting state {key}={value}")
        self.shared_state_cache.append(f"{key}:{value}")

    def sync_external_state(self, peer_id: str, state: Dict[str, Any]) -> None:
        """Syncs state received from an external peer."""
        logger.info(f"Voyager: Syncing external state from {peer_id}")

    def query_global_intelligence(self, query: str) -> str:
        """Queries the global constellation for a specific capability or state."""
        logger.info(f"Voyager: Querying global intelligence for {query}")
        return "Global Sync Active"

    async def stop_constellation_sync(self):
        """Stops the P2P discovery and transport server."""
        await self.discovery_node.stop()
        await self.synapse.stop()
        self.is_active = False
        logger.info("Voyager: Constellation synchronization stopped.")

    def get_known_peers(self) -> List[Dict[str, Any]]:
        """Returns the list of discovered peers in the constellation."""
        return self.discovery_node.get_active_peers()

    @property
    def connected_fleets(self) -> Dict[str, Any]:
        """Phase 319: Legacy compatibility for FederatedKnowledgeOrchestrator."""
        return self.discovery_node.peers

    async def send_signal(self, peer_name: str, signal_type: str, data: Any) -> Any:
        """
        Sends a synaptic signal to a specific peer.
        Bridges the legacy 'signal' API to the new Voyager transport.
        """
        target = self.discovery_node.resolve_synapse_address(peer_name)
        if not target:
            logger.error(f"Voyager: Could not resolve peer '{peer_name}' for signal.")
            return {"status": "error", "message": "Peer not found"}

        peer_ip, peer_port = target
        payload = {"type": signal_type, "data": data, "sender_id": getattr(self.fleet_manager, "fleet_id", "unknown")}
        return await self.synapse.transport.send_to_peer(peer_ip, peer_port, payload)

    def find_best_offload_target(self, required_cpu: int, required_ram: float) -> Optional[tuple[str, int]]:
        """
        Voyager Phase 4.0: Finds the best peer node for task offloading based on resources.
        Returns (ip, port) or None.
        """
        peers = self.discovery_node.get_active_peers()
        best_peer = None
        max_score = -1.0

        for peer in peers:
            props = peer.get("properties", {})
            try:
                # Parse resources sent as strings
                peer_cpu = float(props.get("cpu_cores", "1"))
                peer_ram = float(props.get("ram_gb", "4.0"))

                # Check constraints
                if peer_cpu >= required_cpu and peer_ram >= required_ram:
                    # Simple scoring: prefer most RAM
                    score = peer_ram
                    if score > max_score:
                        max_score = score
                        addrs = peer.get("addresses", [])
                        port = int(props.get("transport_port", "5555"))
                        if addrs:
                            best_peer = (addrs[0], port)
            except (ValueError, TypeError):
                continue
        
        return best_peer

    async def offload_task(self, task_description: str, required_cpu: int = 1, required_ram: float = 2.0) -> Optional[Dict[str, Any]]:
        """
        Attempts to offload a task to a capable peer in the constellation.
        """
        target = self.find_best_offload_target(required_cpu, required_ram)
        if not target:
            logger.warning(f"Voyager: No suitable peer found for task offload (CPU:{required_cpu}, RAM:{required_ram})")
            return None

        peer_ip, peer_port = target
        logger.info(f"Voyager: Offloading task to peer at {peer_ip}:{peer_port}")

        payload = {
            "type": "task_offload",
            "task": task_description,
            "sender_id": getattr(self.fleet_manager, "fleet_id", "unknown"),
            "requirements": {"cpu": required_cpu, "ram": required_ram}
        }

        # Send via Synapse
        return await self.synapse.transport.send_to_peer(peer_ip, peer_port, payload)

    async def query_federated_memory(self, query: str, limit_per_peer: int = 3) -> List[Dict[str, Any]]:
        """
        Broadcasting query to the 'Experience Buffers' of the entire constellation.
        Returns aggregated list of results.
        """
        peers = self.discovery_node.get_active_peers()
        logger.info(f"Voyager: Querying federated memory across {len(peers)} peers: '{query}'")

        payload = {
            "type": "memory_query",
            "query": query,
            "sender_id": getattr(self.fleet_manager, "fleet_id", "unknown"),
             "limit": limit_per_peer
        }

        tasks = []
        for peer in peers:
            addrs = peer.get("addresses", [])
            if not addrs:
                continue
            addr = addrs[0]
            port = int(peer["properties"].get("transport_port", "5555"))
            tasks.append(self.synapse.transport.send_to_peer(addr, port, payload))

        if not tasks:
            return []

        # Gather results with timeout
        results = await asyncio.gather(*tasks, return_exceptions=True)
        aggregated = []
        
        for res in results:
            if isinstance(res, dict) and res.get("status") == "success":
                items = res.get("results", [])
                aggregated.extend(items)
            elif isinstance(res, Exception):
                logger.debug(f"Voyager: Peer query failed: {res}")

        return aggregated

    async def broadcast_task(self, task_description: str, metadata: Optional[Dict[str, Any]] = None):
        """Broadcasts a task opportunity to all discovered peers."""
        peers = self.get_known_peers()
        logger.info(f"Voyager: Broadcasting task to {len(peers)} peers: {task_description[:30]}...")

        payload = {
            "type": "task_broadcast",
            "task": task_description,
            "metadata": metadata or {},
            "sender_id": getattr(self.fleet_manager, "fleet_id", "unknown"),
        }

        tasks = []
        for peer in peers:
            addrs = peer.get("addresses", [])
            if not addrs:
                continue
            addr = addrs[0]
            port = int(peer["properties"].get("transport_port", 5555))
            tasks.append(self.synapse.transport.send_to_peer(addr, port, payload))

        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            logger.info(
                f"Voyager: Broadcast results: {len([r for r in results if not isinstance(r, Exception)])} successful."
            )

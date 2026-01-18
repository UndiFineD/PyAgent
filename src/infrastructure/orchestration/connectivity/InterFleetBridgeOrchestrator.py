#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Phase 319: Multi-Cloud Teleportation (Inter-Fleet Bridge)

from __future__ import annotations
import logging
import asyncio
from typing import Any, Dict, List, Optional

from src.core.base.Version import VERSION
from src.infrastructure.voyager.DiscoveryNode import DiscoveryNode
from src.infrastructure.voyager.RemoteNeuralSynapse import RemoteNeuralSynapse
from src.observability.StructuredLogger import StructuredLogger

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
        
        self.discovery_node = DiscoveryNode(port=self.mDNS_port, transport_port=self.zmq_port)
        self.synapse = RemoteNeuralSynapse(fleet_manager, transport_port=self.zmq_port, discovery_node=self.discovery_node)
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
        except Exception as e:
            logger.error(f"Voyager: Failed to start constellation sync: {e}")

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
        payload = {
            "type": signal_type,
            "data": data,
            "sender_id": getattr(self.fleet_manager, "fleet_id", "unknown")
        }
        return await self.synapse.transport.send_to_peer(peer_ip, peer_port, payload)

    async def broadcast_task(self, task_description: str, metadata: Optional[Dict[str, Any]] = None):
        """Broadcasts a task opportunity to all discovered peers."""
        peers = self.get_known_peers()
        logger.info(f"Voyager: Broadcasting task to {len(peers)} peers: {task_description[:30]}...")
        
        payload = {
            "type": "task_broadcast",
            "task": task_description,
            "metadata": metadata or {},
            "sender_id": getattr(self.fleet_manager, "fleet_id", "unknown")
        }
        
        tasks = []
        for peer in peers:
            addrs = peer.get('addresses', [])
            if not addrs:
                continue
            addr = addrs[0]
            port = int(peer['properties'].get('transport_port', 5555))
            tasks.append(self.synapse.transport.send_to_peer(addr, port, payload))
        
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            logger.info(f"Voyager: Broadcast results: {len([r for r in results if not isinstance(r, Exception)])} successful.")


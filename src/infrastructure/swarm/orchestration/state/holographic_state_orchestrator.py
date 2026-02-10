#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Phase 330: Holographic Memory & State Mirroring (VOYAGER STABILITY)

from __future__ import annotations
import logging
import asyncio
import json
from typing import Any, Dict, List, Optional
from src.core.base.lifecycle.version import VERSION
from src.infrastructure.swarm.resilience.distributed_backup import DistributedBackup

__version__ = VERSION

logger = logging.getLogger(__name__)

class HolographicStateOrchestrator:
    """
    Manages multi-perspective state distribution across the fleet.
    Implements Holographic State Mirroring: data is split and mirrored such that
    any node can reconstruct a specific perspective by querying neighbors.
    """

    def __init__(self, fleet=None) -> None:
        self.fleet = fleet
        self.version = VERSION
        self.backup_node = None
        if fleet:
            # Use the fleet's existing backup node if available
            self.backup_node = getattr(fleet, "backup_node", DistributedBackup(node_id=f"hologram-{id(self)}"))
        else:
            self.backup_node = DistributedBackup(node_id=f"hologram-standalone-{id(self)}")
        
        self.local_holograms: Dict[str, Dict[str, Any]] = {}
        logger.info("HolographicStateOrchestrator: Initialized (Phase 330).")

    async def shard_hologram(self, hologram_id: str, hologram_data: dict, redundancy: int = 2) -> dict:
        """
        Shards a multi-perspective hologram across the fleet.
        Each perspective is treated as an independent shard set.
        """
        logger.info(f"Holographic: Sharding hologram '{hologram_id}' across fleet.")
        
        perspectives = hologram_data.get("perspectives", {})
        if not perspectives:
            # Fallback to source data if no perspectives provided
            perspectives = {"default": hologram_data.get("source_data", hologram_data)}

        shards_created = 0
        for angle, data in perspectives.items():
            # Create shards for this specific perspective using RAID-10 logic
            perspective_shards = self.backup_node.create_shards({
                "hologram_id": hologram_id,
                "perspective": angle,
                "data": data,
                "timestamp": hologram_data.get("timestamp", 0)
            })
            
            # Record locally
            self.local_holograms[f"{hologram_id}_{angle}"] = data
            
            # Mirror shards to neighbors
            if self.fleet and hasattr(self.fleet, "voyager_transport"):
                await self._mirror_to_neighbors(perspective_shards)
            
            shards_created += len(perspective_shards)

        # Broadcast "projection" (metadata) to neighborhood
        await self._broadcast_projection(hologram_id, list(perspectives.keys()))

        return {
            "status": "holographic_sharded",
            "hologram_id": hologram_id,
            "perspectives_count": len(perspectives),
            "total_shards": shards_created
        }

    async def reconstruct_perspective(self, hologram_id: str, angle: str) -> Optional[Dict[str, Any]]:
        """
        Reconstructs a specific architectural perspective by gathering shards from neighbors.
        """
        local_key = f"{hologram_id}_{angle}"
        if local_key in self.local_holograms:
            return self.local_holograms[local_key]

        logger.info(f"Holographic: Reconstructing perspective '{angle}' for '{hologram_id}' from swarm...")
        
        # In a real swarm, we'm query neighbors for shards with 'hologram_id' and 'perspective'
        return None  # Placeholder for actual swarm fetching logic

    async def _mirror_to_neighbors(self, shards: List[Dict[str, Any]]):
        """Sends shards to different neighbor nodes for redundancy."""
        if not self.fleet or not hasattr(self.fleet, "voyager_discovery"):
            return

        peers = self.fleet.voyager_discovery.get_active_peers()
        if not peers:
            return

        # Distribute shards round-robin among peers
        for i, shard in enumerate(shards):
            peer = peers[i % len(peers)]
            addr = peer.get("addr")
            port = peer.get("port", 5555)
            
            msg = {
                "type": "shard_store",
                "sender_id": f"fleet-{self.fleet.workspace_root.name}",
                "shard": shard
            }
            # Fire and forget mirroring
            asyncio.create_task(self.fleet.voyager_transport.send_to_peer(addr, port, msg))

    async def _broadcast_projection(self, hologram_id: str, angles: List[str]):
        """Broadcasts a compact 'projection' of the hologram metadata (Pillar 8)."""
        projection = {
            "type": "hologram_projection",
            "hologram_id": hologram_id,
            "angles": angles,
            "sender_id": f"fleet-{self.fleet.workspace_root.name}"
        }
        
        if self.fleet and hasattr(self.fleet, "voyager_transport"):
            peers = self.fleet.voyager_discovery.get_active_peers()
            for peer in peers:
                addr = peer.get("addr")
                port = peer.get("port", 5555)
                asyncio.create_task(self.fleet.voyager_transport.send_to_peer(addr, port, projection))

    def shard_state(self, state_id: str, state_dict: dict, redundant_factor: int = 1) -> dict:
        """Legacy compatibility wrapper for BaseAgent sharding."""
        return {"status": "legacy_sharded", "id": state_id}

    def reconstruct_state(self, state_id: str) -> str:
        """Legacy compatibility wrapper."""
        return json.dumps({"status": "error", "message": "Use reconstruct_perspective instead"})

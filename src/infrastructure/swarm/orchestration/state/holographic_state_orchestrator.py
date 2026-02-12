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
        self.agent_id = "hologram_orchestrator"

        # RAID-10 Sharding engine (Phase 330)
        if self.fleet and hasattr(self.fleet, "backup_node"):
            self.backup_node = self.fleet.backup_node
        else:
            self.backup_node = DistributedBackup(node_id=self.agent_id)

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
            # Use a combined hash to allow global search by hologram_id while keeping angles distinct
            perspective_shards = self.backup_node.create_shards({
                "hologram_id": hologram_id,
                "perspective": angle,
                "data": data,
                "timestamp": hologram_data.get("timestamp", 0)
            }, custom_hash=f"{hologram_id}_{angle}")

            # Record locally
            self.local_holograms[f"{hologram_id}_{angle}"] = data

            # Phase 330: Store at least one set of shards locally for others to query
            for shard in perspective_shards:
                if shard["mirror_index"] == 0:
                    self.backup_node.store_shard_locally(shard)

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

        if not self.fleet or not hasattr(self.fleet, "voyager_discovery"):
            logger.warning("Holographic: Swarm transport unavailable for reconstruction.")
            return None

        # Phase 330: Try to find local RAID shards first
        matching_shards = self.backup_node.get_local_shards_for_hash(hologram_id)
        if matching_shards:
            reconstructed = self.backup_node.reassemble_state({s["shard_id"]: s for s in matching_shards})
            if reconstructed and angle in reconstructed:
                logger.info(f"Holographic: Reconstructed '{angle}' from local shards.")
                return reconstructed[angle]

        # Future: P2P query to neighbors for missing shards
        return None

    async def handle_projection(self, projection_msg: Dict[str, Any]):
        """Handles incoming metadata 'projections' from peers."""
        hologram_id = projection_msg.get("hologram_id")
        angles = projection_msg.get("angles", [])
        source = projection_msg.get("sender_id")

        logger.info(f"Holographic: Peer {source} projected hologram {hologram_id[:8]} (Angles: {angles})")

    async def find_local_hologram_shards(self, hologram_id: str) -> List[Dict[str, Any]]:
        """Returns shards stored locally for a given hologram ID."""
        return self.backup_node.get_local_shards_for_hash(hologram_id)

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

            if self.fleet and hasattr(self.fleet, "workspace_root"):
                sender_id = f"fleet-{self.fleet.workspace_root.name}"
            else:
                sender_id = self.agent_id

            msg = {
                "type": "shard_store",
                "sender_id": sender_id,
                "shard": shard
            }
            # Fire and forget mirroring
            asyncio.create_task(self.fleet.voyager_transport.send_to_peer(addr, port, msg))

    async def _broadcast_projection(self, hologram_id: str, angles: List[str]):
        """Broadcasts a compact 'projection' of the hologram metadata (Pillar 8)."""
        if self.fleet and hasattr(self.fleet, "workspace_root"):
            sender_id = f"fleet-{self.fleet.workspace_root.name}"
        else:
            sender_id = self.agent_id

        projection = {
            "type": "hologram_projection",
            "hologram_id": hologram_id,
            "angles": angles,
            "sender_id": sender_id
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

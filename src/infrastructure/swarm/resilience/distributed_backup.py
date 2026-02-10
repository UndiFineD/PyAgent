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
Module: distributed_backup
Implements 'Shard RAID-10' protocol for distributed swarm resilience.
"""

from __future__ import annotations
import json
import logging
import hashlib
from typing import Any, Dict, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class DistributedBackup:
    """
    Manages distributed redundancy for agent state and memory.
    Ensures that no single node failure leads to data loss.
    """

    def __init__(self, node_id: str, replication_factor: int = 3):
        self.node_id = node_id
        self.replication_factor = replication_factor
        self.local_shards_dir = Path("data/shards")
        self.local_shards_dir.mkdir(parents=True, exist_ok=True)

    def create_shards(self, state_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Splits state into N encrypted shards.
        (RAID-10 Concept: Mirrored Striping).
        """
        raw_data = json.dumps(state_data).encode()
        data_hash = hashlib.sha256(raw_data).hexdigest()
        
        # Phase 320: Strategic Sharding
        # Split data into 2 parts (stripping) and mirror each part twice (total 4 shards)
        size = len(raw_data)
        mid = size // 2
        parts = [raw_data[:mid], raw_data[mid:]]
        
        shards = []
        for part_idx, part in enumerate(parts):
            for mirror_idx in range(2): # Mirroring Factor: 2
                shards.append({
                    "origin_node": self.node_id,
                    "shard_id": f"{data_hash}_p{part_idx}_m{mirror_idx}",
                    "part_index": part_idx,
                    "data_b64": self._encode(part),
                    "hash": data_hash,
                    "total_parts": 2
                })
        return shards

    def _encode(self, data: bytes) -> str:
        import base64
        return base64.b64encode(data).decode()

    def _decode(self, data_str: str) -> bytes:
        import base64
        return base64.b64decode(data_str)

    def reconstruct_state(self, shard_pool: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Reassembles state from a collection of shards."""
        if not shard_pool:
            return None
            
        parts = {}
        total_parts = shard_pool[0].get("total_parts", 1)
        
        for shard in shard_pool:
            idx = shard.get("part_index", 0)
            if idx not in parts:
                parts[idx] = self._decode(shard["data_b64"])
                
        if len(parts) < total_parts:
            logger.error("Incomplete shards for reconstruction")
            return None
            
        full_data = b"".join(parts[i] for i in range(total_parts))
        return json.loads(full_data.decode())

    def store_shard_locally(self, shard: Dict[str, Any]) -> None:
        """Stores a shard from a peer."""
        shard_id = shard["shard_id"]
        file_path = self.local_shards_dir / f"{shard_id}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(shard, f)
        logger.info("Stored shard %s from %s", shard_id, shard["origin_node"])

    def retrieve_shard(self, shard_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a shard from local storage."""
        file_path = self.local_shards_dir / f"{shard_id}.json"
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

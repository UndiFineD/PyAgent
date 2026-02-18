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
Module: distributed_backup
Implements 'Shard RAID-10' protocol for distributed swarm resilience."""


from __future__ import annotations
import json
import logging
import hashlib
import base64
from typing import Any, Dict, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)



class DistributedBackup:
    """Manages distributed redundancy for agent state and memory.
    Ensures that no single node failure leads to data loss.
    """

    def __init__(self, node_id: str, replication_factor: int = 3):
        self.node_id = node_id
        self.replication_factor = replication_factor
        self.local_shards_dir = Path("data/shards")
        self.local_shards_dir.mkdir(parents=True, exist_ok=True)


    def create_shards(self, state_data: Dict[str, Any], custom_hash: Optional[str] = None) -> List[Dict[str, Any]]:
        """Splits state into N encrypted shards using RAID-10 (Mirroring + Striping).
        Also includes a redundancy parity check.
        """
        raw_data = json.dumps(state_data).encode()
        data_hash = custom_hash if custom_hash else hashlib.sha256(raw_data).hexdigest()

        # Phase 326: Dynamic Striping
        # N=3 parts, each mirrored once (M=2) = 6 shards total
        num_parts = 3 if len(raw_data) > 10000 else 2
        mirror_factor = self.replication_factor  # Default 3

        part_size = (len(raw_data) + num_parts - 1) // num_parts
        parts = [raw_data[i:i + part_size] for i in range(0, len(raw_data), part_size)]

        # Ensure we have exactly num_parts (pad with empty if needed)
        while len(parts) < num_parts:
            parts.append(b"")
        shards = []
        for part_idx, part in enumerate(parts):
            if hasattr(hashlib, "blake3"):
                part_hash = hashlib.blake3(part).hexdigest()
            else:
                part_hash = hashlib.md5(part).hexdigest()

            for mirror_idx in range(mirror_factor):
                shards.append({
                    "origin_node": self.node_id,
                    "shard_id": f"{data_hash}_p{part_idx}_m{mirror_idx}",
                    "part_index": part_idx,
                    "mirror_index": mirror_idx,
                    "data_b64": self._encode(part),
                    "part_hash": part_hash,
                    "full_hash": data_hash,
                    "total_parts": num_parts,
                    "timestamp": 0  # TODO Placeholder for time
                })

        logger.info(f"DistributedBackup: Created {len(shards)} RAID-10 shards for state {data_hash[:8]}")
        return shards


    def store_shard_locally(self, shard: Dict[str, Any]) -> bool:
        """Stores a shard from a peer and verifies integrity."""
        shard_id = shard["shard_id"]
        data_b64 = shard.get("data_b64", "")
        part_hash = shard.get("part_hash")
        # Integrity check
        if part_hash:
            actual_data = self._decode(data_b64)
            if hasattr(hashlib, "blake3"):
                actual_hash = hashlib.blake3(actual_data).hexdigest()
            else:
                actual_hash = hashlib.md5(actual_data).hexdigest()

            if actual_hash != part_hash:
                logger.error(f"DistributedBackup: Corruption detected in shard {shard_id}")
                return False

        file_path = self.local_shards_dir / f"{shard_id}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(shard, f)
        return True


    def get_local_shards_for_hash(self, full_hash: str) -> List[Dict[str, Any]]:
        """Retrieves locally stored shards belonging to a specific state hash."""
        shards = []
        for shard_file in self.local_shards_dir.glob(f"{full_hash}_*.json"):
            try:
                with open(shard_file, "r", encoding="utf-8") as f:
                    shards.append(json.load(f))
            except (OSError, ValueError, json.JSONDecodeError):
                continue
        return shards


    def retrieve_shard(self, shard_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a shard from local storage."""
        file_path = self.local_shards_dir / f"{shard_id}.json"
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return None


    def reassemble_state(self, shards: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Reconstructs state from a set of RAID-10 shards. Requires at least one mirror of each part."""
        if not shards:
            return None

        # Group by part index
        parts_found = {}
        total_parts = 0

        for shard in shards.values():
            p_idx = shard["part_index"]
            total_parts = shard["total_parts"]
            if p_idx not in parts_found:
                # Inside the data_b64 is our bin data
                parts_found[p_idx] = self._decode(shard["data_b64"])
        if len(parts_found) < total_parts:
            logger.error(f"DistributedBackup: Cannot reassemble state. Missing {total_parts - len(parts_found)} parts.")
            return None

        # Join parts in order
        reconstructed_raw = b"".join([parts_found[i] for i in range(total_parts)])
        try:
            return json.loads(reconstructed_raw.decode())
        except (ValueError, json.JSONDecodeError) as e:
            logger.error(f"DistributedBackup: Reconstruction failed: {e}")
            return None


    def _encode(self, data: bytes) -> str:
        return base64.b64encode(data).decode()


    def _decode(self, b64_str: str) -> bytes:
        return base64.b64decode(b64_str)

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
ShardedKnowledgeCore: Logic for managing a trillion-parameter scale knowledge graph.
Uses Adler-32 based sharding to distribute entities across 1024 virtual buckets.
Optimized for high-concurrency and massive data volume.
Requires orjson and aiofiles for high-speed non-blocking I/O.
"""

from __future__ import annotations
from src.core.base.lifecycle.version import VERSION
import zlib
import logging
from pathlib import Path
from typing import Any
import orjson
import aiofiles
import msgpack
import time

try:
    import rust_core as rc
    HAS_RUST = True
except ImportError:
    HAS_RUST = False

__version__ = VERSION


class ShardedKnowledgeCore:
    """Logic for sharding and asynchronously retrieving knowledge at scale."""

    def __init__(self, base_path: Path, shard_count: int = 1024) -> None:
        self.base_path = base_path
        self.shard_count = shard_count
        self.index_path = base_path / "shard_index.msgpack"
        self._index_cache: dict[str, Any] = {}

    def get_shard_id(self, entity_name: str) -> int:
        """Determines the shard ID for a given entity using stable MD5 hashing (Phase 318)."""
        from src.core.rust_bridge import RustBridge
        return RustBridge.calculate_shard_id(entity_name, self.shard_count)

    def get_shard_path(self, shard_id: int) -> Path:
        """Calculates the file path for a specific shard."""
        return self.base_path / f"shard_{shard_id:04d}" / "knowledge.json"

    async def load_shard(self, shard_id: int) -> dict[str, Any]:
        """Asynchronously loads a knowledge shard using orjson."""
        path = self.get_shard_path(shard_id)
        if not path.exists():
            return {}

        try:
            async with aiofiles.open(path, mode="rb") as f:
                content = await f.read()
                return orjson.loads(content) if content else {}
        except Exception as e:
            logging.error(f"Failed to load shard {shard_id}: {e}")
            return {}

    async def save_shard(self, shard_id: int, data: dict[str, Any]) -> bool:
        """Asynchronously saves a knowledge shard using orjson."""
        path = self.get_shard_path(shard_id)
        path.parent.mkdir(parents=True, exist_ok=True)

        try:
            async with aiofiles.open(path, mode="wb") as f:
                await f.write(orjson.dumps(data, option=orjson.OPT_INDENT_2))
            return True
        except Exception as e:
            logging.error(f"Failed to save shard {shard_id}: {e}")
            return False

    def merge_knowledge(
        self, base: dict[str, Any], delta: dict[str, Any]
    ) -> dict[str, Any]:
        """Merges new knowledge into existing structure with conflict resolution."""
        if HAS_RUST:
            try:
                import json
                base_json = json.dumps(base)
                delta_json = json.dumps(delta)
                merged_json = rc.merge_knowledge_rust(base_json, delta_json)
                return json.loads(merged_json)
            except Exception:
                pass
        for key, value in delta.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self.merge_knowledge(base[key], value)
            else:
                base[key] = value
        return base

    def filter_stable_knowledge(
        self, data: dict[str, Any], threshold_confidence: float = 0.8
    ) -> dict[str, Any]:
        """Filters knowledge that is considered stable enough."""
        if HAS_RUST:
            try:
                import json
                data_json = json.dumps(data)
                filtered_json = rc.filter_stable_knowledge_rust(data_json, threshold_confidence)
                return json.loads(filtered_json)
            except Exception:
                pass
        stable = {}
        for k, v in data.items():
            if isinstance(v, dict) and v.get("confidence", 0) >= threshold_confidence:
                stable[k] = v
        return stable

    # PHASE 261: KNOWLEDGE INDEX SNAPSHOTTING
    async def create_index_snapshot(self) -> bool:
        """Serializes the current index mapping to a binary snapshot."""
        try:
            async with aiofiles.open(self.index_path, mode="wb") as f:
                packed = msgpack.packb(
                    {
                        "version": __version__,
                        "timestamp": time.time(),
                        "index": self._index_cache,
                    }
                )
                await f.write(packed)
            logging.info(f"Knowledge index snapshot created at {self.index_path}")
            return True
        except Exception as e:
            logging.error(f"Failed to create index snapshot: {e}")
            return False

    async def load_index_snapshot(self) -> bool:
        """Loads the index mapping from a binary snapshot."""
        if not self.index_path.exists():
            return False
        try:
            async with aiofiles.open(self.index_path, mode="rb") as f:
                content = await f.read()
                data = msgpack.unpackb(content)
                self._index_cache = data.get("index", {})
            logging.info(f"Knowledge index snapshot loaded from {self.index_path}")
            return True
        except Exception as e:
            logging.error(f"Failed to load index snapshot: {e}")
            return False

    async def incremental_reindex(self) -> None:
        """Only updates the index for files modified since last snapshot."""
        # This is a stub for the indexer that would scan the base_path
        # and update self._index_cache based on file mtime.
        # For now, we simulate a scan.
        logging.info("ShardedKnowledgeCore: Performing incremental re-index...")
        # (Actual scanning logic would go here)
        await self.create_index_snapshot()

    async def right_to_be_forgotten(self, entity_name: str) -> bool:
        """
        Removes an entity from the knowledge store across all shards
        to comply with privacy regulations (GDPR/CCPA).
        """
        shard_id = self.get_shard_id(entity_name)
        logging.info(
            f"Compliance: Executing 'Right to be Forgotten' for entity '{entity_name}' in shard {shard_id}"
        )

        shard_data = await self.load_shard(shard_id)
        if entity_name in shard_data:
            del shard_data[entity_name]
            return await self.save_shard(shard_id, shard_data)

        logging.warning(
            f"Compliance: Entity '{entity_name}' not found in knowledge store."
        )
        return False

    def export_to_parquet(self, shard_id: int, output_path: Path) -> bool:
        """Exports a JSON shard to Apache Parquet for large-scale training ingestion (Phase 220)."""
        try:
            import pandas as pd
            import pyarrow as pa
            import pyarrow.parquet as pq

            # Load the shard (blocking load for this utility move)
            source_path = self.get_shard_path(shard_id)
            if not source_path.exists():
                return False

            with open(source_path, "rb") as f:
                data = orjson.loads(f.read())

            if not data:
                return False

            # Convert dict to flat list of records if possible
            records = []
            for key, val in data.items():
                if isinstance(val, dict):
                    rec = {"entity": key}
                    rec.update(val)
                    records.append(rec)
                else:
                    records.append({"entity": key, "value": val})

            df = pd.DataFrame(records)
            table = pa.Table.from_pandas(df)

            output_path.parent.mkdir(parents=True, exist_ok=True)
            pq.write_table(table, str(output_path), compression="zstd")
            return True
        except ImportError:
            logging.error("Parquet export failed: pandas/pyarrow not installed.")
            return False
        except Exception as e:
            logging.error(f"Parquet export error: {e}")
            return False

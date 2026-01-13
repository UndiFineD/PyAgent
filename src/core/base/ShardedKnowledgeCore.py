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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""
ShardedKnowledgeCore: Logic for managing a trillion-parameter scale knowledge graph.
Uses Adler-32 based sharding to distribute entities across 1024 virtual buckets.
Optimized for high-concurrency and massive data volume.
Requires orjson and aiofiles for high-speed non-blocking I/O.
"""

from __future__ import annotations
from src.core.base.version import VERSION
import zlib
import logging
from pathlib import Path
from typing import Any
import orjson
import aiofiles

__version__ = VERSION

class ShardedKnowledgeCore:
    """Logic for sharding and asynchronously retrieving knowledge at scale."""

    def __init__(self, base_path: Path, shard_count: int = 1024) -> None:
        self.base_path = base_path
        self.shard_count = shard_count

    def get_shard_id(self, entity_name: str) -> int:
        """Determines the shard ID for a given entity using stable hashing (Adler-32)."""
        return zlib.adler32(entity_name.encode('utf-8')) % self.shard_count

    def get_shard_path(self, shard_id: int) -> Path:
        """Calculates the file path for a specific shard."""
        return self.base_path / f"shard_{shard_id:04d}" / "knowledge.json"

    async def load_shard(self, shard_id: int) -> dict[str, Any]:
        """Asynchronously loads a knowledge shard using orjson."""
        path = self.get_shard_path(shard_id)
        if not path.exists():
            return {}

        try:
            async with aiofiles.open(path, mode='rb') as f:
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
            async with aiofiles.open(path, mode='wb') as f:
                await f.write(orjson.dumps(data, option=orjson.OPT_INDENT_2))
            return True
        except Exception as e:
            logging.error(f"Failed to save shard {shard_id}: {e}")
            return False

    def merge_knowledge(self, base: dict[str, Any], delta: dict[str, Any]) -> dict[str, Any]:
        """Merges new knowledge into existing structure with conflict resolution."""
        for key, value in delta.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self.merge_knowledge(base[key], value)
            else:
                base[key] = value
        return base

    def filter_stable_knowledge(self, data: dict[str, Any], threshold_confidence: float = 0.8) -> dict[str, Any]:
        """Filters knowledge that is considered stable enough."""
        stable = {}
        for k, v in data.items():
            if isinstance(v, dict) and v.get("confidence", 0) >= threshold_confidence:
                stable[k] = v
        return stable

    async def right_to_be_forgotten(self, entity_name: str) -> bool:
        """
        Phase 238: Prunes all knowledge associated with a specific entity (user/project)
        to comply with privacy regulations (GDPR/CCPA).
        """
        shard_id = self.get_shard_id(entity_name)
        logging.info(f"Compliance: Executing 'Right to be Forgotten' for entity '{entity_name}' in shard {shard_id}")
        
        shard_data = await self.load_shard(shard_id)
        if entity_name in shard_data:
            del shard_data[entity_name]
            return await self.save_shard(shard_id, shard_data)
        
        logging.warning(f"Compliance: Entity '{entity_name}' not found in knowledge store.")
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
            pq.write_table(table, str(output_path), compression='zstd')
            return True
        except ImportError:
            logging.error("Parquet export failed: pandas/pyarrow not installed.")
            return False
        except Exception as e:
            logging.error(f"Parquet export error: {e}")
            return False
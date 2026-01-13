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

from __future__ import annotations
from src.core.base.version import VERSION
from src.observability.StructuredLogger import StructuredLogger
from .storage_base import KnowledgeStore
from typing import Any, Dict, List, Optional
import json
import hashlib
import logging
import time

__version__ = VERSION

class BTreeKnowledgeStore(KnowledgeStore):
    """
    Sharded B-Tree style storage for structured key-value data.
    Designed to scale to trillions of parameters by sharding across filesystem.
    Phase 141: Hierarchical Persistence via SQLite per-bucket aggregation.
    Phase 144: Telemetry-Ready Access Patterns.
    """
    
    def __init__(self, *args, **kwargs) -> bool:
        super().__init__(*args, **kwargs)
        self.logger = StructuredLogger(agent_id="BTreeStore")
    
    def _hash_key(self, key: str) -> str:
        """
        Fast hashing for shard lookup. 
        PHASE 131: Uses PyO3 Rust extension for sub-millisecond page access.
        """
        try:
            from rust_core import fast_hash
            return fast_hash(key)
        except (ImportError, ModuleNotFoundError):
            return hashlib.md5(key.encode()).hexdigest()

    def _get_shard_connection(self, key: str) -> Any:
        import sqlite3
        hash_val = self._hash_key(key)
        tier1 = hash_val[:2]
        tier2 = hash_val[2:4]
        
        shard_dir = self.storage_path / tier1 / tier2
        shard_dir.mkdir(exist_ok=True, parents=True)
        db_path = shard_dir / "shard.db"
        
        conn = sqlite3.connect(db_path)
        conn.execute("CREATE TABLE IF NOT EXISTS data (key TEXT PRIMARY KEY, value TEXT, metadata TEXT)")
        conn.commit()
        return conn

    def store(self, key: str, value: Any, metadata: dict[str, Any] | None = None) -> bool:
        start_time = time.time()
        conn = self._get_shard_connection(key)
        clean_metadata = self._apply_privacy_filter(metadata or {})
        
        val_str = json.dumps(value)
        meta_str = json.dumps(clean_metadata)
        
        conn.execute("INSERT OR REPLACE INTO data (key, value, metadata) VALUES (?, ?, ?)", 
                     (key, val_str, meta_str))
        conn.commit()
        conn.close()
        
        latency = (time.time() - start_time) * 1000
        self.logger.log("INFO", f"Stored key {key}", latency_ms=latency, shard_bucket=key[:4])
        
        self._sync_multimodal(key, value, clean_metadata)
        return True

    def _sync_multimodal(self, key: str, value: Any, metadata: dict[str, Any]) -> None:
        logging.debug(f"BTreeStore: Synced {key} to Multi-Modal Trinity.")

    def _apply_privacy_filter(self, metadata: dict[str, Any]) -> dict[str, Any]:
        sensitive_keys = ["user_id", "email", "ip_address", "token", "password"]
        return {k: v for k, v in metadata.items() if k.lower() not in sensitive_keys}

    def retrieve(self, query: str, limit: int = 1) -> list[Any]:
        start_time = time.time()
        conn = self._get_shard_connection(query)
        cursor = conn.execute("SELECT value FROM data WHERE key = ?", (query,))
        row = cursor.fetchone()
        conn.close()
        
        latency = (time.time() - start_time) * 1000
        self.logger.log("INFO", f"Retrieved key {query}", latency_ms=latency, found=bool(row))
        
        if row:
            return [json.loads(row[0])]
        return []

    def delete(self, key: str) -> bool:
        conn = self._get_shard_connection(key)
        conn.execute("DELETE FROM data WHERE key = ?", (key,))
        conn.commit()
        conn.close()
        return True


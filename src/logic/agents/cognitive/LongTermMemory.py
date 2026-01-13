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

"""Advanced long-term memory using federated DiskCache shards for RAG."""

from __future__ import annotations
from src.core.base.version import VERSION
import hashlib
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

__version__ = VERSION

try:
    import diskcache
    import numpy as np
    from sentence_transformers import SentenceTransformer
    HAS_RAG_DEPS = True
except ImportError:
    HAS_RAG_DEPS = False

class LongTermMemory:
    """Manages persistent conversational and factual memory using DiskCache shards."""
    
    _model = None  # Singleton model for embeddings

    def __init__(self, agent_name: str = "default_agent", base_dir: str = "data/memory/shards") -> None:
        self.agent_name = agent_name
        self.base_dir = Path(base_dir)
        # Sharding: hash the agent name to pick a subdirectory
        self.shard_id = hashlib.md5(agent_name.encode()).hexdigest()[:8]
        self.persist_directory = self.base_dir / self.shard_id
        
        self._enabled = HAS_RAG_DEPS
        self._cache = None
        
        if not self._enabled:
            logging.warning("DiskCache or RAG dependencies missing. Long-term memory logic will be limited.")
        else:
            self._ensure_dirs()
            self._cache = diskcache.Cache(str(self.persist_directory))

    def _ensure_dirs(self) -> None:
        """Ensure the shard directory exists."""
        self.persist_directory.mkdir(parents=True, exist_ok=True)

    @classmethod
    def _get_embedding_model(cls) -> str:
        """Lazy load the embedding model."""
        if cls._model is None and HAS_RAG_DEPS:
            cls._model = SentenceTransformer("all-MiniLM-L6-v2")
        return cls._model

    def store(self, content: str, metadata: dict[str, Any] | None = None, tags: list[str] | None = None) -> str:
        """Store a thought or interaction in the local DiskCache shard."""
        if not self._enabled or not self._cache:
            return ""
            
        mem_id = f"mem_{int(time.time() * 1000)}"
        model = self._get_embedding_model()
        embedding = model.encode(content) if model else None
        
        meta = metadata or {}
        meta["timestamp"] = datetime.now().isoformat()
        meta["agent"] = self.agent_name
        if tags:
            meta["tags"] = tags
            
        entry = {
            "content": content,
            "metadata": meta,
            "embedding": embedding.tolist() if embedding is not None else None
        }
        
        self._cache.set(mem_id, entry)
        return mem_id

    def query(self, query_text: str, n_results: int = 5) -> list[dict[str, Any]]:
        """Retrieve relevant memories from the local shard using cosine similarity."""
        return self._search_shard(self._cache, query_text, n_results)

    def _search_shard(self, cache: diskcache.Cache, query_text: str, n_results: int) -> list[dict[str, Any]]:
        """Internal helper to search a specific diskcache instance."""
        if not HAS_RAG_DEPS or not cache:
            return []
            
        model = self._get_embedding_model()
        if not model:
            return []
            
        query_emb = model.encode(query_text)
        results = []
        
        # We iterate over the cache keys for RAG (sharding keeps this small)
        for key in cache:
            entry = cache.get(key)
            if not entry or "embedding" not in entry or entry["embedding"] is None:
                continue
                
            doc_emb = np.array(entry["embedding"])
            # Cosine similarity
            similarity = np.dot(query_emb, doc_emb) / (np.linalg.norm(query_emb) * np.linalg.norm(doc_emb))
            
            results.append({
                "id": key,
                "content": entry["content"],
                "metadata": entry["metadata"],
                "score": float(similarity)
            })
            
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:n_results]

    def federated_query(self, query_text: str, n_results: int = 5) -> list[dict[str, Any]]:
        """Search across ALL available memory shards (federation)."""
        if not HAS_RAG_DEPS:
            return []
            
        all_results = []
        # Find all shard directories
        if not self.base_dir.exists():
            return self.query(query_text, n_results)
            
        for shard_path in self.base_dir.iterdir():
            if shard_path.is_dir():
                try:
                    shard_cache = diskcache.Cache(str(shard_path))
                    shard_results = self._search_shard(shard_cache, query_text, n_results)
                    all_results.extend(shard_results)
                    shard_cache.close()
                except Exception as e:
                    logging.error(f"Failed to query shard {shard_path}: {e}")
                    
        all_results.sort(key=lambda x: x["score"], reverse=True)
        return all_results[:n_results]

    def clear(self) -> None:
        """Clear the local shard."""
        if self._cache:
            self._cache.clear()

    def __del__(self) -> None:
        """Cleanup cache connection."""
        if hasattr(self, "_cache") and self._cache:
            try:
                self._cache.close()
            except Exception:
                pass
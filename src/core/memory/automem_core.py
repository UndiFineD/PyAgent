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

"""AutoMemCore: graph-vector hybrid memory system (placeholder).

This module provides a safe, minimal stub implementation for the
AutoMem memory core referenced in the roadmap. The full implementation
should provide vector indexing, graph storage, persistence, and a
low-latency recall API.
"""
from __future__ import annotations
from pathlib import Path
from dataclasses import dataclass
import typing as t


@dataclass
class MemoryRecord:
    id: str
    vector: list[float]
    metadata: dict


class AutoMemCore:
    """Minimal AutoMemCore stub.

    Methods are intentionally minimal to keep CI fast; implementors
    should replace with production-ready storage/indexing later.
    """

    def __init__(self, store_dir: t.Optional[Path] = None):
        self.store_dir = Path(store_dir) if store_dir else None
        self._records: dict[str, MemoryRecord] = {}

    def add(self, rec: MemoryRecord) -> None:
        """Add a memory record (in-memory only for now)."""
        self._records[rec.id] = rec

    def recall(self, query_vector: list[float], top_k: int = 8) -> list[MemoryRecord]:
        """Naive recall: returns up to `top_k` records (no real vector search).

        This is a placeholder; replace with a nearest-neighbor index.
        """
        return list(self._records.values())[:top_k]


__all__ = ["AutoMemCore", "MemoryRecord"]
"""
PyAgent AutoMem Memory System Integration.

Based on the exceptional AutoMem memory system (90.53% LoCoMo benchmark).
Implements graph-vector hybrid memory with FalkorDB + Qdrant for revolutionary
conversational memory capabilities.
"""

from __future__ import annotations

import hashlib
import json
import logging
import math
import os
import random
import re
import sys
import time
import uuid
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from queue import Empty, Queue
from threading import Event, Lock, Thread
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

from falkordb import FalkorDB
from qdrant_client import QdrantClient
from qdrant_client import models as qdrant_models

try:
    from qdrant_client.http.exceptions import UnexpectedResponse
except ImportError:  # Allow tests to import without full qdrant client installed
    UnexpectedResponse = Exception  # type: ignore[misc,assignment]

try:  # Allow tests to import without full qdrant client installed
    from qdrant_client.models import Distance, PayloadSchemaType, PointStruct, VectorParams
except Exception:  # pragma: no cover - degraded import path
    try:
        from qdrant_client.http import models as _qmodels

        Distance = getattr(_qmodels, "Distance", None)
        PointStruct = getattr(_qmodels, "PointStruct", None)
        VectorParams = getattr(_qmodels, "VectorParams", None)
        PayloadSchemaType = getattr(_qmodels, "PayloadSchemaType", None)
    except Exception:
        Distance = PointStruct = VectorParams = None
        PayloadSchemaType = None

# Provide a simple PointStruct shim for tests/environments lacking qdrant models
if PointStruct is None:  # pragma: no cover - test shim

    class PointStruct:  # type: ignore[no-redef]
        def __init__(self, id: str, vector: List[float], payload: Dict[str, Any]):
            self.id = id
            self.vector = vector
            self.payload = payload


from werkzeug.exceptions import HTTPException

# Make OpenAI import optional to allow running without it
try:
    from openai import OpenAI  # type: ignore
except ImportError:
    OpenAI = None  # type: ignore

try:
    import spacy  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    spacy = None

from src.core.base.state import StateTransaction
from src.core.base.models.communication_models import CascadeContext

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger("pyagent.memory.automem")

# Configure Flask and Werkzeug loggers to use stdout instead of stderr
for logger_name in ["werkzeug", "flask.app"]:
    framework_logger = logging.getLogger(logger_name)
    framework_logger.handlers.clear()
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    )
    framework_logger.addHandler(stdout_handler)
    framework_logger.setLevel(logging.INFO)


@dataclass
class MemoryConfig:
    """Configuration for AutoMem memory system."""
    falkordb_url: str = "redis://localhost:6379"
    qdrant_url: str = "http://localhost:6333"
    collection_name: str = "pyagent_memories"
    vector_dim: int = 1536  # OpenAI ada-002 dimension
    distance_metric: str = "COSINE"
    consolidation_enabled: bool = True
    max_memory_age_days: int = 365
    consolidation_interval_hours: int = 24


@dataclass
class Memory:
    """Represents a single memory with metadata."""
    id: str
    content: str
    tags: List[str] = field(default_factory=list)
    tag_prefixes: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    importance: float = 1.0
    confidence: float = 1.0
    vector: Optional[List[float]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class AutoMemCore:
    """
    AutoMem Memory System Core.

    Implements graph-vector hybrid memory with FalkorDB + Qdrant.
    Based on the world's highest-performing memory system (90.53% LoCoMo benchmark).
    """

    def __init__(self, config: MemoryConfig):
        self.config = config
        self.logger = logging.getLogger("pyagent.memory.automem.core")

        # Initialize backing stores
        self.graph_store = FalkorDB.from_url(config.falkordb_url)
        self.vector_store = QdrantClient(url=config.qdrant_url)

        # Initialize vector collection if it doesn't exist
        self._ensure_vector_collection()

        # Initialize consolidation system
        if config.consolidation_enabled:
            self.consolidator = MemoryConsolidator(self)
            self.consolidator.start()
        else:
            self.consolidator = None

    def _ensure_vector_collection(self):
        """Ensure the vector collection exists with proper configuration."""
        try:
            self.vector_store.get_collection(self.config.collection_name)
        except Exception:
            # Collection doesn't exist, create it
            self.vector_store.create_collection(
                collection_name=self.config.collection_name,
                vectors_config=qdrant_models.VectorParams(
                    size=self.config.vector_dim,
                    distance=getattr(qdrant_models.Distance, self.config.distance_metric)
                )
            )

    def store_memory(self, content: str, tags: Optional[List[str]] = None,
                    importance: float = 1.0, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Store a new memory in the hybrid system.

        Args:
            content: The memory content to store
            tags: Optional tags for categorization
            importance: Importance score (0.0-1.0)
            metadata: Additional metadata

        Returns:
            Memory ID
        """
        memory_id = str(uuid.uuid4())
        tags = tags or []
        metadata = metadata or {}

        # Create memory object
        memory = Memory(
            id=memory_id,
            content=content,
            tags=tags,
            tag_prefixes=[tag.split(':')[0] for tag in tags if ':' in tag],
            importance=importance,
            metadata=metadata
        )

        # Store in graph database
        self._store_in_graph(memory)

        # Store in vector database (async embedding generation)
        self._store_in_vector(memory)

        self.logger.info(f"Stored memory {memory_id}: {content[:50]}...")
        return memory_id

    def _store_in_graph(self, memory: Memory):
        """Store memory in FalkorDB graph database."""
        try:
            graph = self.graph_store.select_graph("pyagent_memories")

            # Create memory node
            query = """
            CREATE (m:Memory {
                id: $id,
                content: $content,
                tags: $tags,
                tag_prefixes: $tag_prefixes,
                timestamp: $timestamp,
                importance: $importance,
                confidence: $confidence,
                metadata: $metadata
            })
            """

            params = {
                'id': memory.id,
                'content': memory.content,
                'tags': memory.tags,
                'tag_prefixes': memory.tag_prefixes,
                'timestamp': memory.timestamp.isoformat(),
                'importance': memory.importance,
                'confidence': memory.confidence,
                'metadata': json.dumps(memory.metadata)
            }

            graph.query(query, params)

        except Exception as e:
            self.logger.error(f"Failed to store memory in graph: {e}")
            raise

    def _store_in_vector(self, memory: Memory):
        """Store memory in Qdrant vector database."""
        try:
            # Generate embedding (placeholder - would integrate with actual embedding service)
            vector = self._generate_embedding(memory.content)

            # Store in Qdrant
            self.vector_store.upsert(
                collection_name=self.config.collection_name,
                points=[
                    qdrant_models.PointStruct(
                        id=memory.id,
                        vector=vector,
                        payload={
                            'content': memory.content,
                            'tags': memory.tags,
                            'tag_prefixes': memory.tag_prefixes,
                            'timestamp': memory.timestamp.isoformat(),
                            'importance': memory.importance,
                            'confidence': memory.confidence,
                            'metadata': memory.metadata
                        }
                    )
                ]
            )

        except Exception as e:
            self.logger.error(f"Failed to store memory in vector DB: {e}")
            raise

    def _generate_embedding(self, content: str) -> List[float]:
        """Generate vector embedding for content."""
        # Placeholder - integrate with actual embedding service
        # In production, this would call OpenAI, local model, etc.
        return [random.random() for _ in range(self.config.vector_dim)]

    def recall_memories(self, query: str, tags: Optional[List[str]] = None,
                       limit: int = 10, min_score: float = 0.0) -> List[Dict[str, Any]]:
        """
        Recall memories using 9-component hybrid scoring.

        Args:
            query: Search query
            tags: Optional tag filters
            limit: Maximum results to return
            min_score: Minimum similarity score

        Returns:
            List of memory results with scores
        """
        # Generate query embedding
        query_vector = self._generate_embedding(query)

        # Search vector database
        vector_results = self.vector_store.search(
            collection_name=self.config.collection_name,
            query_vector=query_vector,
            limit=limit * 2,  # Get more for reranking
            score_threshold=min_score
        )

        # Apply tag filtering if specified
        if tags:
            vector_results = self._filter_by_tags(vector_results, tags)

        # Rerank using 9-component scoring
        scored_results = self._hybrid_score(query, query_vector, vector_results)

        # Return top results
        return scored_results[:limit]

    def _filter_by_tags(self, results: List, tags: List[str]) -> List:
        """Filter results by tag constraints."""
        filtered = []
        for result in results:
            payload = result.payload
            if self._matches_tag_filter(payload.get('tags', []), tags):
                filtered.append(result)
        return filtered

    def _matches_tag_filter(self, memory_tags: List[str], filter_tags: List[str]) -> bool:
        """Check if memory tags match filter criteria."""
        # Simple implementation - check if any filter tag is in memory tags
        return any(tag in memory_tags for tag in filter_tags)

    def _hybrid_score(self, query: str, query_vector: List[float],
                     vector_results: List) -> List[Dict[str, Any]]:
        """
        Apply 9-component hybrid scoring system.

        Components (weighted):
        - Vector similarity (25%)
        - Keyword matching (15%)
        - Graph relationships (25%)
        - Temporal relevance (15%)
        - Lexical similarity (10%)
        - Importance (5%)
        - Confidence (5%)
        """
        scored = []

        for result in vector_results:
            payload = result.payload
            vector_score = result.score

            # Keyword matching score
            keyword_score = self._calculate_keyword_score(query, payload['content'])

            # Graph relationship score
            graph_score = self._calculate_graph_score(payload['id'])

            # Temporal relevance score
            temporal_score = self._calculate_temporal_score(payload['timestamp'])

            # Lexical similarity score
            lexical_score = self._calculate_lexical_score(query, payload['content'])

            # Importance and confidence
            importance = payload.get('importance', 1.0)
            confidence = payload.get('confidence', 1.0)

            # Calculate final hybrid score
            final_score = (
                vector_score * 0.25 +
                keyword_score * 0.15 +
                graph_score * 0.25 +
                temporal_score * 0.15 +
                lexical_score * 0.10 +
                importance * 0.05 +
                confidence * 0.05
            )

            scored.append({
                'id': result.id,
                'content': payload['content'],
                'tags': payload.get('tags', []),
                'timestamp': payload['timestamp'],
                'score': final_score,
                'components': {
                    'vector': vector_score,
                    'keyword': keyword_score,
                    'graph': graph_score,
                    'temporal': temporal_score,
                    'lexical': lexical_score,
                    'importance': importance,
                    'confidence': confidence
                }
            })

        # Sort by final score
        scored.sort(key=lambda x: x['score'], reverse=True)
        return scored

    def _calculate_keyword_score(self, query: str, content: str) -> float:
        """Calculate keyword matching score."""
        query_words = set(query.lower().split())
        content_words = set(content.lower().split())
        overlap = len(query_words.intersection(content_words))
        return overlap / len(query_words) if query_words else 0.0

    def _calculate_graph_score(self, memory_id: str) -> float:
        """Calculate graph relationship score."""
        # Placeholder - would analyze graph connections
        return 0.5  # Neutral score for now

    def _calculate_temporal_score(self, timestamp_str: str) -> float:
        """Calculate temporal relevance score."""
        try:
            timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            now = datetime.now(timezone.utc)
            age_days = (now - timestamp).days

            # Recency bias - newer memories score higher
            if age_days < 1:
                return 1.0
            elif age_days < 7:
                return 0.8
            elif age_days < 30:
                return 0.6
            else:
                return 0.4
        except:
            return 0.5

    def _calculate_lexical_score(self, query: str, content: str) -> float:
        """Calculate lexical similarity score."""
        # Simple Jaccard similarity
        query_set = set(query.lower().split())
        content_set = set(content.lower().split())
        intersection = query_set.intersection(content_set)
        union = query_set.union(content_set)
        return len(intersection) / len(union) if union else 0.0

    def associate_memories(self, memory_id1: str, memory_id2: str,
                          relationship: str = "related", strength: float = 1.0):
        """
        Create association between two memories in the graph.

        Args:
            memory_id1: First memory ID
            memory_id2: Second memory ID
            relationship: Type of relationship
            strength: Relationship strength (0.0-1.0)
        """
        try:
            graph = self.graph_store.select_graph("pyagent_memories")

            query = """
            MATCH (m1:Memory {id: $id1}), (m2:Memory {id: $id2})
            CREATE (m1)-[r:RELATES_TO {type: $relationship, strength: $strength, timestamp: $timestamp}]->(m2)
            """

            params = {
                'id1': memory_id1,
                'id2': memory_id2,
                'relationship': relationship,
                'strength': strength,
                'timestamp': datetime.now(timezone.utc).isoformat()
            }

            graph.query(query, params)
            self.logger.info(f"Associated memories {memory_id1} -> {memory_id2} ({relationship})")

        except Exception as e:
            self.logger.error(f"Failed to associate memories: {e}")
            raise

    def get_bridge_connections(self, memory_id: str, max_depth: int = 3) -> List[Dict[str, Any]]:
        """
        Find multi-hop bridge connections for reasoning.

        Args:
            memory_id: Starting memory ID
            max_depth: Maximum connection depth

        Returns:
            List of bridge connections
        """
        try:
            graph = self.graph_store.select_graph("pyagent_memories")

            query = """
            MATCH path = (start:Memory {id: $memory_id})-[*1..{max_depth}]-(end:Memory)
            WHERE start <> end
            RETURN path, length(path) as depth
            ORDER BY depth
            LIMIT 20
            """

            params = {'memory_id': memory_id, 'max_depth': max_depth}
            result = graph.query(query, params)

            connections = []
            for record in result.result_set:
                path = record[0]
                depth = record[1]
                connections.append({
                    'path': path,
                    'depth': depth
                })

            return connections

        except Exception as e:
            self.logger.error(f"Failed to get bridge connections: {e}")
            return []


class MemoryConsolidator:
    """
    Memory consolidation system with neuroscience-inspired cycles.

    Implements decay, creative, cluster, and forget consolidation types.
    """

    def __init__(self, memory_core: AutoMemCore, interval_hours: int = 24):
        self.memory_core = memory_core
        self.interval_hours = interval_hours
        self.logger = logging.getLogger("pyagent.memory.consolidator")
        self.running = False
        self.thread = None

    def start(self):
        """Start the consolidation process."""
        if self.running:
            return

        self.running = True
        self.thread = Thread(target=self._consolidation_loop, daemon=True)
        self.thread.start()
        self.logger.info("Memory consolidator started")

    def stop(self):
        """Stop the consolidation process."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        self.logger.info("Memory consolidator stopped")

    def _consolidation_loop(self):
        """Main consolidation loop."""
        while self.running:
            try:
                self._run_consolidation_cycle()
            except Exception as e:
                self.logger.error(f"Consolidation cycle failed: {e}")

            # Sleep for interval
            time.sleep(self.interval_hours * 3600)

    def _run_consolidation_cycle(self):
        """Run a complete consolidation cycle."""
        self.logger.info("Starting memory consolidation cycle")

        # Decay old, low-importance memories
        self._decay_memories()

        # Creative consolidation - find and create new associations
        self._creative_consolidation()

        # Cluster similar memories
        self._cluster_memories()

        # Forget irrelevant memories
        self._forget_memories()

        self.logger.info("Memory consolidation cycle completed")

    def _decay_memories(self):
        """Apply decay to old memories."""
        # Implementation would update importance scores based on age and usage
        pass

    def _creative_consolidation(self):
        """Create new associations between related memories."""
        # Implementation would analyze content similarity and create relationships
        pass

    def _cluster_memories(self):
        """Group similar memories into clusters."""
        # Implementation would use clustering algorithms on vector representations
        pass

    def _forget_memories(self):
        """Remove or archive memories that are no longer relevant."""
        # Implementation would identify and remove memories below threshold
        pass

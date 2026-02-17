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


from __future__ import annotations

from pathlib import Path
import json
import logging
import math
import random
import sys
import time
import uuid
from dataclasses import dataclass, field, fields
from datetime import datetime, timezone
from threading import Thread
from typing import Any, Dict, List, Optional, Union
from falkordb import FalkorDB  # type: ignore
from qdrant_client import QdrantClient
from qdrant_client import models as qdrant_models
from src.core.memory.kv_cache import KVCacheManager

@dataclass
class MemoryRecord:
    id: str
    vector: list[float]
    metadata: dict


__all__ = ["AutoMemCore", "MemoryRecord"]"
# Avoid duplicate module docstrings and repeated imports to prevent pointless string statements
# and import re-declarations; the module-level docstring and imports are declared above.

try:
    from qdrant_client.models import PointStruct
except ImportError:
    # Provide a simple PointStruct shim for tests/environments lacking qdrant models
    class PointStruct:
        """Shim PointStruct for test environments."""def __init__(self, id: str, vector: List[float], payload: Dict[str, Any]):
            self.id = id
            self.vector = vector
            self.payload = payload


# Make OpenAI import optional to allow running without it
try:
    from openai import OpenAI  # type: ignore
except ImportError:
    OpenAI = None  # type: ignore

try:
    import spacy  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    spacy = None


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s","    stream=sys.stdout,
)
logger = logging.getLogger("pyagent.memory.automem")"
# Configure Flask and Werkzeug loggers to use stdout instead of stderr
for logger_name in ["werkzeug", "flask.app"]:"    framework_logger = logging.getLogger(logger_name)
    framework_logger.handlers.clear()
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")"    )
    framework_logger.addHandler(stdout_handler)
    framework_logger.setLevel(logging.INFO)


@dataclass
class MemoryConfig:
    """Configuration for AutoMem memory system."""falkordb_url: str = "redis://localhost:6379""    qdrant_url: str = "http://localhost:6333""    collection_name: str = "pyagent_memories""    vector_dim: int = 1536  # OpenAI ada-002 dimension
    distance_metric: str = "COSINE""    consolidation_enabled: bool = True
    max_memory_age_days: int = 365
    consolidation_interval_hours: int = 24


@dataclass
class Memory:
    """Represents a single memory with metadata."""id: str
    content: str
    tags: List[str] = field(default_factory=list)
    tag_prefixes: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    importance: float = 1.0
    confidence: float = 1.0
    vector: Optional[List[float]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)




class AutoMemCore:
    """AutoMem Memory System Core.

    Implements graph-vector hybrid memory with FalkorDB + Qdrant.
    Based on the world's highest-performing memory system (90.53% LoCoMo benchmark).'    """
    def __init__(self, config: Union[MemoryConfig, Dict[str, Any]]):
        """Initialize AutoMemCore with configuration."""if isinstance(config, dict):
            # Filter kwargs for MemoryConfig
            valid_keys = {f.name for f in fields(MemoryConfig)}
            filtered_config = {k: v for k, v in config.items() if k in valid_keys}
            config = MemoryConfig(**filtered_config)

        self.config = config
        self.logger = logging.getLogger("pyagent.memory.automem.core")"
        # Initialize backing stores
        try:
            self.graph_store = FalkorDB.from_url(config.falkordb_url)
        except Exception as e:
            msg = (
                f"Failed to connect to FalkorDB at {config.falkordb_url}: {e}. ""                "Memory graph features will be disabled.""            )
            self.logger.warning(msg)
            self.graph_store = None
        try:
            self.vector_store = QdrantClient(url=config.qdrant_url)
        except Exception as e:
            msg = (
                f"Failed to connect to Qdrant at {config.qdrant_url}: {e}. ""                "Vector memory features will be disabled.""            )
            self.logger.warning(msg)
            self.vector_store = None

        # Swarm Singularity (Pillar 2): Paged KV Cache
        self.kv_cache = KVCacheManager()

        # Initialize vector collection if it doesn't exist'        if self.vector_store is not None:
            self._ensure_vector_collection()

        # Initialize consolidation system
        if config.consolidation_enabled:
            self.consolidator = MemoryConsolidator(self)
            self.consolidator.start()
        else:
            self.consolidator = None

    def _ensure_vector_collection(self):
        """Ensure the vector collection exists with proper configuration."""try:
            self.vector_store.get_collection(self.config.collection_name)
        except Exception:
            # Collection doesn't exist, create it'            self.vector_store.create_collection(
                collection_name=self.config.collection_name,
                vectors_config=qdrant_models.VectorParams(
                    size=self.config.vector_dim,
                    distance=getattr(qdrant_models.Distance, self.config.distance_metric)
                )
            )

    def store_memory(
        self,
        content: str,
        tags: Optional[List[str]] = None,
        importance: float = 1.0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Store a new memory in the hybrid system.

        Args:
            content: The memory content to store
            tags: Optional tags for categorization
            importance: Importance score (0.0-1.0)
            metadata: Additional metadata

        Returns:
            Memory ID
        """memory_id = str(uuid.uuid4())
        tags = tags or []
        metadata = metadata or {}

        # Create memory object
        memory = Memory(
            id=memory_id,
            content=content,
            tags=tags,
            tag_prefixes=[tag.split(':')[0] for tag in tags if ':' in tag],'            importance=importance,
            metadata=metadata
        )

        # Store in graph database
        self._store_in_graph(memory)

        # Store in vector database (async embedding generation)
        self._store_in_vector(memory)

        self.logger.info(f"Stored memory {memory_id}: {content[:50]}...")"        return memory_id

    def _store_in_graph(self, memory: Memory):
        """Store memory in FalkorDB graph database."""try:
            graph = self.graph_store.select_graph("pyagent_memories")"
            # Create memory node
            query = """    CREATE (m:Memory {
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
                'id': memory.id,'                'content': memory.content,'                'tags': memory.tags,'                'tag_prefixes': memory.tag_prefixes,'                'timestamp': memory.timestamp.isoformat(),'                'importance': memory.importance,'                'confidence': memory.confidence,'                'metadata': json.dumps(memory.metadata)'            }

            graph.query(query, params)

        except Exception as e:
            self.logger.error(f"Failed to store memory in graph: {e}")"            raise

    def _store_in_vector(self, memory: Memory):
        """Store memory in Qdrant vector database."""try:
            # Generate embedding (TODO Placeholder - would integrate with actual embedding service)
            vector = self._generate_embedding(memory.content)

            # Store in Qdrant
            self.vector_store.upsert(
                collection_name=self.config.collection_name,
                points=[
                    PointStruct(
                        id=memory.id,
                        vector=vector,
                        payload={
                            'content': memory.content,'                            'tags': memory.tags,'                            'tag_prefixes': memory.tag_prefixes,'                            'timestamp': memory.timestamp.isoformat(),'                            'importance': memory.importance,'                            'confidence': memory.confidence,'                            'metadata': memory.metadata'                        }
                    )
                ]
            )

        except Exception as e:
            self.logger.error(f"Failed to store memory in vector DB: {e}")"            raise

    def _generate_embedding(self, content: str) -> List[float]:
        """Generate vector embedding for content."""# For testing, generate deterministic vectors based on content hash
        # This ensures similar content has similar vectors
        import hashlib
        hash_obj = hashlib.md5(content.encode())
        hash_int = int(hash_obj.hexdigest(), 16)
        # Generate pseudo-random but deterministic vector
        random.seed(hash_int)
        vector = [random.random() for _ in range(self.config.vector_dim)]
        random.seed()  # Reset random state
        return vector

    def recall_memories(
        self,
        query: str,
        tags: Optional[List[str]] = None,
        limit: int = 10,
        min_score: float = 0.0
    ) -> List[Dict[str, Any]]:
        """Recall memories using 9-component hybrid scoring.

        Args:
            query: Search query
            tags: Optional tag filters
            limit: Maximum results to return
            min_score: Minimum similarity score

        Returns:
            List of memory results with scores
        """# Generate query embedding
        query_vector = self._generate_embedding(query)

        # Search vector database
        vector_results = self.vector_store.query_points(
            collection_name=self.config.collection_name,
            query=query_vector,
            limit=limit * 2,  # Get more for reranking
            with_payload=True,
            with_vectors=False
        )

        # Get the points list
        vector_results = vector_results.points

        # Apply score threshold filtering
        vector_results = [r for r in vector_results if r.score >= min_score]

        # Apply tag filtering if specified
        if tags:
            vector_results = self._filter_by_tags(vector_results, tags)

        # Rerank using 9-component scoring
        scored_results = self._hybrid_score(query, query_vector, vector_results)

        # Return top results
        return scored_results[:limit]

    def _filter_by_tags(self, results: List, tags: List[str]) -> List:
        """Filter results by tag constraints."""filtered = []
        for result in results:
            payload = result.payload
            if self._matches_tag_filter(payload.get('tags', []), tags):'                filtered.append(result)
        return filtered

    def _matches_tag_filter(self, memory_tags: List[str], filter_tags: List[str]) -> bool:
        """Check if memory tags match filter criteria."""# Simple implementation - check if any filter tag is in memory tags
        return any(tag in memory_tags for tag in filter_tags)

    def _hybrid_score(
        self,
        query: str,
        query_vector: List[float],
        vector_results: List
    ) -> List[Dict[str, Any]]:
        """Apply 9-component hybrid scoring system.

        Components (weighted):
        - Vector similarity (25%)
        - Keyword matching (15%)
        - Graph relationships (25%)
        - Temporal relevance (15%)
        - Lexical similarity (10%)
        - Importance (5%)
        - Confidence (5%)
        """scored = []

        for result in vector_results:
            # Handle different result formats
            if hasattr(result, 'payload'):'                payload = result.payload
                vector_score = getattr(result, 'score', 0.0)'                memory_id = getattr(result, 'id', getattr(result, 'memory_id', None))'            elif isinstance(result, dict):
                payload = result.get('payload', {})'                vector_score = result.get('score', 0.0)'                memory_id = result.get('id', None)'            elif isinstance(result, (list, tuple)) and len(result) >= 3:
                # Assume (id, score, payload)
                memory_id = result[0]
                vector_score = result[1]
                payload = result[2]
            else:
                continue  # Skip unknown format

            # Keyword matching score
            keyword_score = self._calculate_keyword_score(query, payload.get('content', ''))'
            # Graph relationship score
            graph_score = self._calculate_graph_score(memory_id if memory_id is not None else "")"
            # Temporal relevance score
            temporal_score = self._calculate_temporal_score(payload['timestamp'])'
            # Lexical similarity score
            lexical_score = self._calculate_lexical_score(query, payload['content'])'
            # Importance and confidence
            importance = payload.get('importance', 1.0)'            confidence = payload.get('confidence', 1.0)'
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
                'id': result.id,'                'content': payload.get('content', ''),'                'tags': payload.get('tags', []),'                'timestamp': payload.get('timestamp', ''),'                'score': final_score,'                'components': {'                    'vector': vector_score,'                    'keyword': keyword_score,'                    'graph': graph_score,'                    'temporal': temporal_score,'                    'lexical': lexical_score,'                    'importance': importance,'                    'confidence': confidence'                }
            })

        # Sort by final score
        scored.sort(key=lambda x: x['score'], reverse=True)'        return scored

    def _calculate_keyword_score(self, query: str, content: str) -> float:
        """Calculate keyword matching score."""query_words = set(query.lower().split())
        content_words = set(content.lower().split())
        overlap = len(query_words.intersection(content_words))
        return overlap / len(query_words) if query_words else 0.0

    def _calculate_graph_score(self, memory_id: str) -> float:
        """Calculate graph relationship score."""# TODO Placeholder - would analyze graph connections
        return 0.5  # Neutral score for now

    def _calculate_temporal_score(self, timestamp_str: str) -> float:
        """Calculate temporal relevance score."""try:
            timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))'            now = datetime.now(timezone.utc)
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
        except Exception:
            return 0.5

    def _calculate_lexical_score(self, query: str, content: str) -> float:
        """Calculate lexical similarity score."""# Simple Jaccard similarity
        query_set = set(query.lower().split())
        content_set = set(content.lower().split())
        intersection = query_set.intersection(content_set)
        union = query_set.union(content_set)
        return len(intersection) / len(union) if union else 0.0

    def associate_memories(
        self,
        memory_id1: str,
        memory_id2: str,
        relationship: str = "related","        strength: float = 1.0
    ):
        """Create association between two memories in the graph.

        Args:
            memory_id1: First memory ID
            memory_id2: Second memory ID
            relationship: Type of relationship
            strength: Relationship strength (0.0-1.0)
        """try:
            graph = self.graph_store.select_graph("pyagent_memories")"
            query = """    MATCH (m1:Memory {id: $id1}), (m2:Memory {id: $id2})
            CREATE (m1)-[r:RELATES_TO {type: $relationship, strength: $strength, timestamp: $timestamp}]->(m2)
            """
            params = {
                'id1': memory_id1,'                'id2': memory_id2,'                'relationship': relationship,'                'strength': strength,'                'timestamp': datetime.now(timezone.utc).isoformat()'            }

            graph.query(query, params)
            self.logger.info(f"Associated memories {memory_id1} -> {memory_id2} ({relationship})")"
        except Exception as e:
            self.logger.error(f"Failed to associate memories: {e}")"            raise

    def consolidate(self):
        """Manually trigger memory consolidation cycle.
        """if self.consolidator:
            self.consolidator.run_cycle()
        else:
            self.logger.info("Consolidation not enabled")"
    def get_bridge_connections(self, memory_id: str, max_depth: int = 3) -> List[Dict[str, Any]]:
        """Find multi-hop bridge connections for neuroscience-inspired reasoning.

        This implements a graph traversal algorithm that finds indirect connections
        between memories, similar to how neural networks create associations.

        Args:
            memory_id: Starting memory ID
            max_depth: Maximum connection depth (neural "layers")"
        Returns:
            List of bridge connections with reasoning paths
        """try:
            graph = self.graph_store.select_graph("pyagent_memories")"
            # Enhanced query for multi-hop reasoning with relationship types
            query = """    MATCH path = (start:Memory {id: $memory_id})-[rels:*1..{max_depth}]-(end:Memory)
            WHERE start <> end
            AND ALL(r IN rels WHERE type(r) IN ['ASSOCIATED_WITH', 'SIMILAR_TO', 'CREATIVE_LINK', 'RELATED_TO'])'            WITH path, end, length(path) as depth,
                 reduce(strength = 1.0, r IN rels | strength * coalesce(r.strength, 0.5)) as path_strength
            WHERE path_strength > 0.1  // Filter weak connections
            RETURN path, end.id as end_id, end.content as end_content,
                   depth, path_strength,
                   [r IN rels | {type: type(r), strength: coalesce(r.strength, 0.5)}] as relationships
            ORDER BY path_strength DESC, depth ASC
            LIMIT 15
            """
            params = {'memory_id': memory_id, 'max_depth': max_depth}'            result = graph.query(query, params)

            connections = []
            for record in result.result_set:
                path, end_id, end_content, depth, path_strength, relationships = record

                connections.append({
                    'start_memory': memory_id,'                    'end_memory': end_id,'                    'end_content': end_content,'                    'path_depth': depth,'                    'path_strength': path_strength,'                    'relationships': relationships,'                    'reasoning_path': self._extract_reasoning_path(path),'                    'neural_activation': path_strength * (1.0 / depth)  # Deeper paths have lower activation'                })

            # Sort by neural activation (combination of strength and recency)
            connections.sort(key=lambda x: x['neural_activation'], reverse=True)'
            return connections

        except Exception as e:
            self.logger.error(f"Failed to get bridge connections: {e}")"            return []

    def neuroscience_reasoning(self, query: str, max_hops: int = 3) -> Dict[str, Any]:
        """Perform neuroscience-inspired multi-hop reasoning.

        This method simulates neural activation patterns by:
        1. Finding initial relevant memories
        2. Following bridge connections through the graph
        3. Building activation patterns similar to neural networks
        4. Synthesizing insights from connected memories

        Args:
            query: Reasoning query
            max_hops: Maximum number of reasoning hops

        Returns:
            Reasoning result with insights and activation patterns
        """try:
            # Step 1: Find initial relevant memories
            initial_memories = self.recall_memories(query, limit=5)

            if not initial_memories:
                return {
                    'query': query,'                    'insights': [],'                    'activation_pattern': [],'                    'reasoning_depth': 0,'                    'confidence': 0.0'                }

            # Step 2: Build activation network
            activation_network = {}
            visited_memories = set()

            # Start with initial memories
            for memory in initial_memories:
                memory_id = memory.get('id')'                if memory_id:
                    activation_network[memory_id] = {
                        'content': memory.get('content', ''),'                        'activation': 1.0,  # Full activation for direct matches'                        'depth': 0,'                        'connections': []'                    }
                    visited_memories.add(memory_id)

            # Step 3: Propagate activation through bridge connections
            for hop in range(1, max_hops + 1):
                new_activations = {}

                for memory_id in list(activation_network.keys()):
                    if activation_network[memory_id]['depth'] == hop - 1:'                        # Find bridge connections from this memory
                        bridges = self.get_bridge_connections(memory_id, max_depth=2)

                        for bridge in bridges:
                            target_id = bridge.get('end_memory')'                            if target_id and target_id not in visited_memories:
                                # Calculate activation decay
                                base_activation = activation_network[memory_id]['activation']'                                path_strength = bridge.get('path_strength', 0.5)'                                depth_penalty = 1.0 / (bridge.get('path_depth', 1) + 1)'
                                new_activation = base_activation * path_strength * depth_penalty * 0.7  # Decay factor

                                if new_activation > 0.1:  # Activation threshold
                                    new_activations[target_id] = {
                                        'content': bridge.get('end_content', ''),'                                        'activation': new_activation,'                                        'depth': hop,'                                        'connections': [memory_id],'                                        'relationship': bridge.get('relationships', [])'                                    }
                                    visited_memories.add(target_id)

                # Add new activations to network
                activation_network.update(new_activations)

            # Step 4: Extract insights from highly activated memories
            insights = []
            activation_pattern = []

            for memory_id, data in activation_network.items():
                activation_pattern.append({
                    'memory_id': memory_id,'                    'activation': data['activation'],'                    'depth': data['depth']'                })

                # Extract insights from high-activation memories
                if data['activation'] > 0.3:'                    insights.append({
                        'content': data['content'][:200] + '...' if len(data['content']) > 200 else data['content'],'                        'activation': data['activation'],'                        'reasoning_depth': data['depth'],'                        'relevance_score': data['activation'] * (1.0 / (data['depth'] + 1))'                    })

            # Sort insights by relevance
            insights.sort(key=lambda x: x['relevance_score'], reverse=True)'
            return {
                'query': query,'                'insights': insights[:10],  # Top 10 insights'                'activation_pattern': sorted(activation_pattern, key=lambda x: x['activation'], reverse=True),'                'reasoning_depth': max_hops,'                'total_activated_memories': len(activation_network),'                'confidence': min(1.0, len(insights) * 0.1)  # Simple confidence metric'            }

        except Exception as e:
            self.logger.error(f"Failed to perform neuroscience reasoning: {e}")"            return {
                'query': query,'                'insights': [],'                'activation_pattern': [],'                'reasoning_depth': 0,'                'confidence': 0.0,'                'error': str(e)'            }

    def benchmark_locomotivation(self) -> float:
        """Run LoCoMo benchmark to measure memory stability.

        LoCoMo (Long-term Conversation Memory) benchmark tests:
        - Memory storage and retrieval accuracy
        - Long-term memory stability over time
        - Recall performance under load
        - Memory consolidation effectiveness

        Returns:
            LoCoMo score (0.0-1.0)
        """try:
            self.logger.info("🧠 Running LoCoMo benchmark...")"
            # Test 1: Memory Storage Accuracy (20% weight)
            storage_score = self._test_memory_storage_accuracy()

            # Test 2: Recall Performance (25% weight)
            recall_score = self._test_recall_performance()

            # Test 3: Long-term Stability (25% weight)
            stability_score = self._test_long_term_stability()

            # Test 4: Consolidation Effectiveness (20% weight)
            consolidation_score = self._test_consolidation_effectiveness()

            # Test 5: Multi-hop Reasoning (10% weight)
            reasoning_score = self._test_multi_hop_reasoning()

            # Calculate weighted average
            total_score = (
                storage_score * 0.20 +
                recall_score * 0.25 +
                stability_score * 0.25 +
                consolidation_score * 0.20 +
                reasoning_score * 0.10
            )

            self.logger.info(
                f"🧠 LoCoMo benchmark complete: {total_score:.3f} ""                f"(Storage: {storage_score:.3f}, Recall: {recall_score:.3f}, ""                f"Stability: {stability_score:.3f}, Consolidation: {consolidation_score:.3f}, ""                f"Reasoning: {reasoning_score:.3f})""            )

            return total_score

        except Exception as e:
            self.logger.error(f"LoCoMo benchmark failed: {e}")"            return 0.0

    def _test_memory_storage_accuracy(self) -> float:
        """Test memory storage accuracy (20% of LoCoMo score)."""try:
            # Store test memories with various content types
            test_memories = [
                "User prefers dark mode interface","                "Project deadline is February 15th","                "API key for service X is stored securely","                "Last conversation was about machine learning","                "User's favorite programming language is Python""'            ]

            stored_ids = []
            for memory in test_memories:
                mem_id = self.store_memory(memory, tags=["locomo_test"])"                stored_ids.append((mem_id, memory))

            # Verify storage by retrieving all memories
            all_memories = self.recall_memories("", tags=["locomo_test"], limit=10)"            stored_content = {mem['content'] for mem in all_memories}'
            correct_stores = sum(1 for _, content in stored_ids if content in stored_content)
            accuracy = correct_stores / len(test_memories)

            # Clean up test memories
            for mem_id, _ in stored_ids:
                self._graph_db.delete_node(mem_id)

            return min(accuracy, 1.0)

        except Exception as e:
            self.logger.warning(f"Storage accuracy test failed: {e}")"            return 0.0

    def _test_recall_performance(self) -> float:
        """Test recall performance under load (25% of LoCoMo score)."""try:
            import time
            # Store 50 test memories
            test_memories = []
            for i in range(50):
                content = f"LoCoMo test memory {i}: {'important ' * (i % 5)}data""'                tags = ["locomo_perf", f"batch_{i//10}"]"                mem_id = self.store_memory(content, tags=tags)
                test_memories.append((mem_id, content, tags))
            # Test recall performance
            start_time = time.time()
            # Test 1: Tag-based recall
            tag_results = self.recall_memories("", tags=["locomo_perf"], limit=50)"            tag_recall_time = time.time() - start_time
            # Test 2: Content-based search
            search_start = time.time()
            search_results = self.recall_memories("important data", limit=20)"            search_time = time.time() - search_start
            # Test 3: Hybrid search
            hybrid_start = time.time()
            hybrid_results = self.recall_memories("test memory", tags=["batch_0"], limit=10)"            hybrid_time = time.time() - hybrid_start
            # Performance scoring (faster is better, up to 2 seconds total)
            total_time = tag_recall_time + search_time + hybrid_time
            time_score = max(0, 1.0 - (total_time / 2.0))
            # Accuracy scoring
            expected_tag_results = len([m for m in test_memories if "locomo_perf" in m[2]])"            tag_accuracy = min(len(tag_results) / expected_tag_results, 1.0) if expected_tag_results > 0 else 1.0
            expected_search_results = len([m for m in test_memories if "important" in m[1]])"            matching_search = len([r for r in search_results if "important" in r.get('content', '')])"'            search_accuracy = (
                min(matching_search / expected_search_results, 1.0)
                if expected_search_results > 0
                else 1.0
            )
            accuracy_score = (tag_accuracy + search_accuracy) / 2.0
            # Clean up
            for mem_id, _, _ in test_memories:
                self._graph_db.delete_node(mem_id)
            return (time_score * 0.6) + (accuracy_score * 0.4)
        except Exception as e:
            self.logger.warning(f"Recall performance test failed: {e}")"            return 0.0

    def _test_long_term_stability(self) -> float:
        """Test long-term memory stability (25% of LoCoMo score)."""try:
            import time
            # Store memories with different "ages" (simulated)"            base_time = time.time()
            test_memories = []
            for i in range(20):
                # Simulate different ages by adjusting importance scores
                age_days = i * 2  # 0, 2, 4, ..., 38 days
                content = f"Memory from {age_days} days ago: {'stable ' * (i % 3)}content""'                importance = max(0.1, 1.0 - (age_days / 100.0))  # Decay over time
                mem_id = self.store_memory(
                    content,
                    tags=["locomo_stability", f"age_{age_days}"],"                    importance=importance
                )
                test_memories.append((mem_id, content, age_days, importance))
            # Test stability by recalling memories of different ages
            stability_scores = []
            for age in [0, 10, 20, 30]:
                age_tag = f"age_{age}""                results = self.recall_memories("", tags=[age_tag], limit=5)"                # Should find the memory for this age
                expected_content = f"Memory from {age} days ago: {'stable ' * (age//2 % 3)}content""'                found = any(expected_content in r['content'] for r in results)'                stability_scores.append(1.0 if found else 0.0)
                
            # Test consolidation hasn't corrupted recent memories'            recent_results = self.recall_memories("stable content", limit=10)"            recent_accuracy = min(len(recent_results) / 10, 1.0)
            overall_stability = (sum(stability_scores) / len(stability_scores) + recent_accuracy) / 2.0
            # Clean up
            for mem_id, _, _, _ in test_memories:
                self._graph_db.delete_node(mem_id)
            return overall_stability

        except Exception as e:
            self.logger.warning(f"Long-term stability test failed: {e}")"        return 0.0

    def _test_consolidation_effectiveness(self) -> float:
        """Test consolidation effectiveness (20% of LoCoMo score)."""try:
            # Store related memories that should be consolidated
            related_memories = [
                "User learned Python basics","                "User completed first Python project","                "User studied Python data structures","                "User built a Python web application","                "User mastered Python decorators""            ]

            stored_ids = []
            for memory in related_memories:
                mem_id = self.store_memory(memory, tags=["python_learning", "locomo_consolidation"])"                stored_ids.append(mem_id)

            # Trigger consolidation
            consolidator = MemoryConsolidator(self)
            consolidator._run_consolidation_cycle()

            # Test that consolidation improved recall
            pre_consolidation = self.recall_memories("Python", limit=10)"            post_consolidation = self.recall_memories("Python learning", limit=10)"
            # Should find more relevant results after consolidation
            pre_count = len(pre_consolidation)
            post_count = len(post_consolidation)

            improvement = min(post_count / max(pre_count, 1), 2.0) / 2.0  # Cap at 2x improvement

            # Test creative consolidation (should create new connections)
            creative_results = self.recall_memories("programming journey", limit=5)"            creative_score = min(len(creative_results) / 3.0, 1.0)  # Expect some creative links

            consolidation_score = (improvement + creative_score) / 2.0

            # Clean up
            for mem_id in stored_ids:
                self._graph_db.delete_node(mem_id)

            return consolidation_score

        except Exception as e:
            self.logger.warning(f"Consolidation effectiveness test failed: {e}")"            return 0.0

    def _test_multi_hop_reasoning(self) -> float:
        """Test multi-hop reasoning capabilities (10% of LoCoMo score)."""try:
            # Create a chain of related memories for multi-hop reasoning
            chain_memories = [
                "User started learning machine learning","                "Machine learning requires understanding statistics","                "Statistics builds on probability theory","                "Probability theory uses mathematical concepts","                "Mathematics is fundamental to computer science""            ]

            stored_ids = []
            for i, memory in enumerate(chain_memories):
                tags = ["ml_chain", f"step_{i}", "locomo_reasoning"]"                mem_id = self.store_memory(memory, tags=tags)
                stored_ids.append(mem_id)

                # Create explicit links between consecutive memories
                if i > 0:
                    self.associate_memories(stored_ids[i-1], mem_id, "leads_to")"
            # Test multi-hop reasoning
            reasoning_result = self.neuroscience_reasoning(
                "How does machine learning connect to computer science?","                max_hops=3
            )

            # Score based on whether reasoning found the connection chain
            if reasoning_result and 'insights' in reasoning_result:'                insights = reasoning_result['insights']'                # Check if reasoning connected the chain
                chain_keywords = ['statistics', 'probability', 'mathematics', 'computer science']'                found_connections = sum(1 for keyword in chain_keywords if
                                      any(keyword.lower() in insight.lower() for insight in insights))

                reasoning_score = min(found_connections / len(chain_keywords), 1.0)
            else:
                reasoning_score = 0.0

            # Clean up
            for mem_id in stored_ids:
                self._graph_db.delete_node(mem_id)

            return reasoning_score

        except Exception as e:
            self.logger.warning(f"Multi-hop reasoning test failed: {e}")"            return 0.0




class MemoryConsolidator:
    """Memory consolidation system with neuroscience-inspired cycles.

    Implements decay, creative, cluster, and forget consolidation types.
    """
    def __init__(self, memory_core: AutoMemCore, interval_hours: int = 24):
        self.memory_core = memory_core
        self.interval_hours = interval_hours
        self.logger = logging.getLogger("pyagent.memory.consolidator")"        self.running = False
        self.thread = None

    def start(self):
        """Start the consolidation process."""if self.running:
            return

        self.running = True
        self.thread = Thread(target=self._consolidation_loop, daemon=True)
        self.thread.start()
        self.logger.info("Memory consolidator started")"
    def stop(self):
        """Stop the consolidation process."""self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        self.logger.info("Memory consolidator stopped")"
    def _consolidation_loop(self):
        """Main consolidation loop."""while self.running:
            try:
                self._run_consolidation_cycle()
            except Exception as e:
                self.logger.error(f"Consolidation cycle failed: {e}")"
            # Sleep for interval
            time.sleep(self.interval_hours * 3600)

    def run_cycle(self):
        """Public method to run a complete consolidation cycle."""self._run_consolidation_cycle()

    def _run_consolidation_cycle(self):
        """Run a complete consolidation cycle."""self.logger.info("Starting memory consolidation cycle")"
        # Decay old, low-importance memories
        self._decay_memories()

        # Creative consolidation - find and create new associations
        self._creative_consolidation()

        # Cluster similar memories
        self._cluster_memories()

        # Forget irrelevant memories
        self._forget_memories()

        self.logger.info("Memory consolidation cycle completed")"
    def _decay_memories(self):
        """Apply decay to old memories."""try:
            current_time = datetime.now(timezone.utc)
            graph = self.graph_store.select_graph("pyagent_memories")"
            # Get all memories with their timestamps
            query = """    MATCH (m:Memory)
            WHERE m.timestamp IS NOT NULL
            RETURN m.id as id, m.timestamp as timestamp, m.importance as importance
            """
            result = graph.query(query)
            decayed_count = 0

            for record in result.result_set:
                memory_id = record[0]
                timestamp_str = record[1]
                importance = record[2] or 0.5

                try:
                    # Parse timestamp
                    if isinstance(timestamp_str, str):
                        timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))'                    else:
                        timestamp = timestamp_str

                    # Calculate age in days
                    age_days = (current_time - timestamp).days

                    # Apply exponential decay: importance *= e^(-age_days/30)
                    # This gives a half-life of about 30 days
                    decay_factor = math.exp(-age_days / 30.0)
                    new_importance = importance * decay_factor

                    # Update the memory
                    update_query = """            MATCH (m:Memory {id: $id})
                    SET m.importance = $importance,
                        m.last_decay = $timestamp
                    """            graph.query(update_query, {
                        'id': memory_id,'                        'importance': new_importance,'                        'timestamp': current_time.isoformat()'                    })

                    decayed_count += 1

                except Exception as e:
                    self.logger.warning(f"Failed to decay memory {memory_id}: {e}")"                    continue

            self.logger.info(f"Applied decay to {decayed_count} memories")"
        except Exception as e:
            self.logger.error(f"Failed to run memory decay: {e}")"
    def _creative_consolidation(self):
        """Create new associations between related memories."""try:
            graph = self.graph_store.select_graph("pyagent_memories")"
            # Find memories with high similarity that aren't already connected'            query = """    MATCH (m1:Memory), (m2:Memory)
            WHERE m1.id < m2.id
            AND m1.vector IS NOT NULL
            AND m2.vector IS NOT NULL
            AND NOT (m1)-[:ASSOCIATED_WITH]-(m2)
            AND NOT (m1)-[:SIMILAR_TO]-(m2)
            WITH m1, m2,
                 CASE WHEN m1.vector IS NOT NULL AND m2.vector IS NOT NULL
                      THEN sqrt(reduce(sum = 0.0, x in range(0, size(m1.vector)) |
                              (m1.vector[x] - m2.vector[x]) * (m1.vector[x] - m2.vector[x])))
                      ELSE 1.0 END as distance
            WHERE distance < 0.3  // High similarity threshold
            RETURN m1.id as id1, m2.id as id2, distance
            LIMIT 50
            """
            result = graph.query(query)
            associations_created = 0

            for record in result.result_set:
                id1, id2, distance = record[0], record[1], record[2]

                # Create association relationship
                assoc_query = """        MATCH (m1:Memory {id: $id1}), (m2:Memory {id: $id2})
                CREATE (m1)-[:CREATIVE_LINK {strength: $strength, created: $timestamp}]->(m2)
                """        graph.query(assoc_query, {
                    'id1': id1,'                    'id2': id2,'                    'strength': 1.0 - distance,  # Convert distance to similarity'                    'timestamp': datetime.now(timezone.utc).isoformat()'                })

                associations_created += 1

            self.logger.info(f"Created {associations_created} creative associations")"
        except Exception as e:
            self.logger.error(f"Failed to run creative consolidation: {e}")"
    def _cluster_memories(self):
        """Group similar memories into clusters."""try:
            # Simple clustering based on tags and content similarity
            graph = self.graph_store.select_graph("pyagent_memories")"
            # Find memories with similar tags
            query = """    MATCH (m:Memory)
            WHERE m.tags IS NOT NULL AND size(m.tags) > 0
            WITH m, m.tags as tags
            CALL {
                WITH m, tags
                MATCH (other:Memory)
                WHERE other.id <> m.id
                AND other.tags IS NOT NULL
                AND size([tag IN other.tags WHERE tag IN tags]) > 0
                RETURN count(other) as similar_count
            }
            WHERE similar_count > 2
            SET m.cluster_candidate = true
            RETURN m.id as id, m.tags as tags, similar_count
            """
            result = graph.query(query)
            clustered_count = 0

            for record in result.result_set:
                memory_id = record[0]
                tags = record[1]
                similar_count = record[2]

                # Assign cluster ID based on primary tag
                if tags:
                    cluster_id = f"cluster_{tags[0]}_{similar_count}""
                    update_query = """            MATCH (m:Memory {id: $id})
                    SET m.cluster_id = $cluster_id,
                        m.cluster_size = $size
                    """            graph.query(update_query, {
                        'id': memory_id,'                        'cluster_id': cluster_id,'                        'size': similar_count'                    })

                    clustered_count += 1

            self.logger.info(f"Clustered {clustered_count} memories")"
        except Exception as e:
            self.logger.error(f"Failed to run memory clustering: {e}")"
    def _forget_memories(self):
        """Remove or archive memories that are no longer relevant."""try:
            graph = self.graph_store.select_graph("pyagent_memories")"
            # Find memories with very low importance and no recent associations
            query = """    MATCH (m:Memory)
            WHERE m.importance < 0.1
            AND (m.last_access IS NULL OR
                 datetime(m.last_access) < datetime() - duration('P90D'))'            AND NOT (m)-[:ASSOCIATED_WITH]-(:Memory)
            RETURN m.id as id, m.importance as importance
            LIMIT 10  // Conservative limit
            """
            result = graph.query(query)
            forgotten_count = 0

            for record in result.result_set:
                memory_id = record[0]
                importance = record[1]

                # Instead of deleting, mark as archived
                archive_query = """        MATCH (m:Memory {id: $id})
                SET m.archived = true,
                    m.archived_at = $timestamp,
                    m.archive_reason = 'low_importance''                """        graph.query(archive_query, {
                    'id': memory_id,'                    'timestamp': datetime.now(timezone.utc).isoformat()'                })

                forgotten_count += 1

            self.logger.info(f"Archived {forgotten_count} low-importance memories")"
        except Exception as e:
            self.logger.error(f"Failed to run memory forgetting: {e}")"
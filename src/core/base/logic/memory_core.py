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
Memory Core - Hybrid graph-vector memory system
Based on AutoMem patterns: FalkorDB + Qdrant hybrid architecture
"""

import asyncio
import json
import logging
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Set, Tuple
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


@dataclass
class MemoryNode:
    """Represents a memory node in the graph"""
    id: str
    content: str
    embedding: Optional[List[float]] = None
    importance: float = 1.0
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: float = None
    updated_at: float = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = time.time()
        if self.updated_at is None:
            self.updated_at = time.time()


@dataclass
class MemoryRelation:
    """Represents a relationship between memory nodes"""
    source_id: str
    target_id: str
    relation_type: str  # RELATES_TO, LEADS_TO, CONTRADICTS, etc.
    strength: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: float = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = time.time()


class MemoryStore(ABC):
    """Abstract base class for memory storage backends"""

    @abstractmethod
    async def store_memory(self, node: MemoryNode) -> str:
        """Store a memory node"""
        pass

    @abstractmethod
    async def get_memory(self, memory_id: str) -> Optional[MemoryNode]:
        """Retrieve a memory node by ID"""
        pass

    @abstractmethod
    async def update_memory(self, memory_id: str, updates: Dict[str, Any]) -> bool:
        """Update a memory node"""
        pass

    @abstractmethod
    async def delete_memory(self, memory_id: str) -> bool:
        """Delete a memory node"""
        pass

    @abstractmethod
    async def search_similar(self, query_embedding: List[float], limit: int = 10,
                           threshold: float = 0.7) -> List[Tuple[MemoryNode, float]]:
        """Search for similar memories using vector similarity"""
        pass

    @abstractmethod
    async def search_by_tags(self, tags: List[str], mode: str = "any",
                           match: str = "exact") -> List[MemoryNode]:
        """Search memories by tags"""
        pass


class GraphMemoryStore(MemoryStore):
    """
    Graph-based memory store using relationship patterns
    Based on AutoMem's FalkorDB patterns
    """

    def __init__(self):
        # In a real implementation, this would connect to FalkorDB/Neo4j
        self.nodes: Dict[str, MemoryNode] = {}
        self.relations: Dict[str, List[MemoryRelation]] = {}

    async def store_memory(self, node: MemoryNode) -> str:
        """Store a memory node in the graph"""
        self.nodes[node.id] = node
        self.relations[node.id] = []
        logger.info(f"Stored memory node: {node.id}")
        return node.id

    async def get_memory(self, memory_id: str) -> Optional[MemoryNode]:
        """Retrieve a memory node"""
        return self.nodes.get(memory_id)

    async def update_memory(self, memory_id: str, updates: Dict[str, Any]) -> bool:
        """Update a memory node"""
        if memory_id not in self.nodes:
            return False

        node = self.nodes[memory_id]
        for key, value in updates.items():
            if hasattr(node, key):
                setattr(node, key, value)
        node.updated_at = time.time()
        return True

    async def delete_memory(self, memory_id: str) -> bool:
        """Delete a memory node and its relations"""
        if memory_id not in self.nodes:
            return False

        # Remove the node
        del self.nodes[memory_id]

        # Remove relations involving this node
        for node_id, relations in self.relations.items():
            self.relations[node_id] = [
                r for r in relations
                if r.source_id != memory_id and r.target_id != memory_id
            ]

        del self.relations[memory_id]
        return True

    async def search_similar(self, query_embedding: List[float], limit: int = 10,
                           threshold: float = 0.7) -> List[Tuple[MemoryNode, float]]:
        """Graph-based similarity search (simplified)"""
        # In a real implementation, this would use graph algorithms
        # For now, return all nodes with dummy similarity scores
        results = []
        for node in self.nodes.values():
            if node.embedding:
                # Simple cosine similarity placeholder
                similarity = 0.8  # Placeholder
                if similarity >= threshold:
                    results.append((node, similarity))

        return sorted(results, key=lambda x: x[1], reverse=True)[:limit]

    async def search_by_tags(self, tags: List[str], mode: str = "any",
                           match: str = "exact") -> List[MemoryNode]:
        """Search memories by tags"""
        results = []

        for node in self.nodes.values():
            node_tags = [tag.lower() for tag in node.tags]

            if mode == "any":
                # Match if node has any of the requested tags
                if match == "exact":
                    if any(tag.lower() in node_tags for tag in tags):
                        results.append(node)
                else:  # prefix match
                    if any(any(nt.startswith(tag.lower()) for nt in node_tags) for tag in tags):
                        results.append(node)
            else:  # mode == "all"
                # Match if node has all of the requested tags
                if match == "exact":
                    if all(tag.lower() in node_tags for tag in tags):
                        results.append(node)
                else:  # prefix match
                    if all(any(nt.startswith(tag.lower()) for nt in node_tags) for tag in tags):
                        results.append(node)

        return results

    async def add_relation(self, relation: MemoryRelation):
        """Add a relationship between memory nodes"""
        if relation.source_id not in self.relations:
            self.relations[relation.source_id] = []
        self.relations[relation.source_id].append(relation)

    async def get_relations(self, node_id: str, relation_type: Optional[str] = None) -> List[MemoryRelation]:
        """Get relations for a node"""
        relations = self.relations.get(node_id, [])
        if relation_type:
            relations = [r for r in relations if r.relation_type == relation_type]
        return relations

    async def find_related_memories(self, memory_id: str, max_depth: int = 2,
                                  relation_types: Optional[List[str]] = None) -> List[Tuple[MemoryNode, float]]:
        """Find related memories through graph traversal (multi-hop)"""
        visited = set()
        results = []

        async def traverse(node_id: str, depth: int, path_strength: float):
            if depth > max_depth or node_id in visited:
                return
            visited.add(node_id)

            node = await self.get_memory(node_id)
            if node:
                results.append((node, path_strength))

                # Get relations
                relations = await self.get_relations(node_id)
                if relation_types:
                    relations = [r for r in relations if r.relation_type in relation_types]

                for relation in relations:
                    target_id = relation.target_id if relation.source_id == node_id else relation.source_id
                    await traverse(target_id, depth + 1, path_strength * relation.strength)

        await traverse(memory_id, 0, 1.0)
        return results[1:]  # Exclude the original node


class VectorMemoryStore(MemoryStore):
    """
    Vector-based memory store for semantic similarity
    Based on AutoMem's Qdrant patterns
    """

    def __init__(self):
        # In a real implementation, this would connect to Qdrant/FAISS/Chroma
        self.nodes: Dict[str, MemoryNode] = {}
        self.embeddings: Dict[str, List[float]] = {}

    async def store_memory(self, node: MemoryNode) -> str:
        """Store a memory node with its embedding"""
        self.nodes[node.id] = node
        if node.embedding:
            self.embeddings[node.id] = node.embedding
        logger.info(f"Stored vector memory: {node.id}")
        return node.id

    async def get_memory(self, memory_id: str) -> Optional[MemoryNode]:
        """Retrieve a memory node"""
        return self.nodes.get(memory_id)

    async def update_memory(self, memory_id: str, updates: Dict[str, Any]) -> bool:
        """Update a memory node"""
        if memory_id not in self.nodes:
            return False

        node = self.nodes[memory_id]
        for key, value in updates.items():
            if hasattr(node, key):
                setattr(node, key, value)
        node.updated_at = time.time()

        # Update embedding if provided
        if 'embedding' in updates:
            self.embeddings[memory_id] = updates['embedding']

        return True

    async def delete_memory(self, memory_id: str) -> bool:
        """Delete a memory node"""
        if memory_id in self.nodes:
            del self.nodes[memory_id]
        if memory_id in self.embeddings:
            del self.embeddings[memory_id]
        return True

    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        import math
        dot_product = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(y * y for y in b))
        return dot_product / (norm_a * norm_b) if norm_a and norm_b else 0.0

    async def search_similar(self, query_embedding: List[float], limit: int = 10,
                           threshold: float = 0.7) -> List[Tuple[MemoryNode, float]]:
        """Search for similar memories using vector similarity"""
        results = []

        for memory_id, embedding in self.embeddings.items():
            similarity = self._cosine_similarity(query_embedding, embedding)
            if similarity >= threshold:
                node = self.nodes[memory_id]
                results.append((node, similarity))

        # Sort by similarity (highest first)
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:limit]

    async def search_by_tags(self, tags: List[str], mode: str = "any",
                           match: str = "exact") -> List[MemoryNode]:
        """Search memories by tags (simplified - delegates to graph store in hybrid system)"""
        # In a real hybrid system, this would coordinate with graph store
        results = []

        for node in self.nodes.values():
            node_tags = [tag.lower() for tag in node.tags]

            if mode == "any":
                if match == "exact":
                    if any(tag.lower() in node_tags for tag in tags):
                        results.append(node)
                else:  # prefix match
                    if any(any(nt.startswith(tag.lower()) for nt in node_tags) for tag in tags):
                        results.append(node)
            else:  # mode == "all"
                if match == "exact":
                    if all(tag.lower() in node_tags for tag in tags):
                        results.append(node)
                else:  # prefix match
                    if all(any(nt.startswith(tag.lower()) for nt in node_tags) for tag in tags):
                        results.append(node)

        return results


class HybridMemoryCore:
    """
    Hybrid graph-vector memory system
    Based on AutoMem's dual storage architecture
    """

    def __init__(self, graph_store: Optional[GraphMemoryStore] = None,
                 vector_store: Optional[VectorMemoryStore] = None):
        self.graph_store = graph_store or GraphMemoryStore()
        self.vector_store = vector_store or VectorMemoryStore()

        # Configuration for hybrid scoring (based on AutoMem's 9-component system)
        self.scoring_weights = {
            'vector_similarity': 0.25,
            'keyword_match': 0.15,
            'graph_relation': 0.25,
            'content_overlap': 0.25,
            'temporal_alignment': 0.05,
            'tag_match': 0.05
        }

    async def store_memory(self, content: str, embedding: Optional[List[float]] = None,
                          tags: Optional[List[str]] = None, importance: float = 1.0,
                          metadata: Optional[Dict[str, Any]] = None) -> str:
        """Store a new memory in both graph and vector stores"""
        memory_id = str(uuid.uuid4())

        node = MemoryNode(
            id=memory_id,
            content=content,
            embedding=embedding,
            importance=importance,
            tags=tags or [],
            metadata=metadata or {}
        )

        # Store in both backends
        await self.graph_store.store_memory(node)
        await self.vector_store.store_memory(node)

        logger.info(f"Stored memory: {memory_id}")
        return memory_id

    async def recall_memory(self, memory_id: str) -> Optional[MemoryNode]:
        """Recall a specific memory"""
        # Try graph store first (canonical source)
        return await self.graph_store.get_memory(memory_id)

    async def update_memory(self, memory_id: str, updates: Dict[str, Any]) -> bool:
        """Update a memory in both stores"""
        graph_success = await self.graph_store.update_memory(memory_id, updates)
        vector_success = await self.vector_store.update_memory(memory_id, updates)
        return graph_success and vector_success

    async def delete_memory(self, memory_id: str) -> bool:
        """Delete a memory from both stores"""
        graph_success = await self.graph_store.delete_memory(memory_id)
        vector_success = await self.vector_store.delete_memory(memory_id)
        return graph_success and vector_success

    async def search_memories(self, query: str, query_embedding: Optional[List[float]] = None,
                            tags: Optional[List[str]] = None, limit: int = 10,
                            expand_paths: bool = True) -> List[Tuple[MemoryNode, float]]:
        """
        Hybrid search combining vector similarity, graph relations, and metadata
        Based on AutoMem's 9-component hybrid scoring
        """
        candidates = set()

        # Vector similarity search
        if query_embedding:
            vector_results = await self.vector_store.search_similar(query_embedding, limit * 2)
            for node, score in vector_results:
                candidates.add(node.id)

        # Tag-based search
        if tags:
            tag_results = await self.graph_store.search_by_tags(tags)
            for node in tag_results:
                candidates.add(node.id)

        # Keyword search (simplified). Skip if empty query to avoid matching all nodes.
        keyword_results = []
        query_lower = query.lower().strip() if query else ""
        if query_lower:
            for node in self.graph_store.nodes.values():
                if query_lower in node.content.lower():
                    keyword_results.append(node)
                    candidates.add(node.id)

        # Calculate hybrid scores for candidates
        scored_results = []
        for candidate_id in candidates:
            node = await self.graph_store.get_memory(candidate_id)
            if not node:
                continue

            score = await self._calculate_hybrid_score(node, query, query_embedding, tags)
            scored_results.append((node, score))

        # Sort by score and limit
        scored_results.sort(key=lambda x: x[1], reverse=True)

        # Multi-hop expansion (AutoMem bridge discovery)
        if expand_paths and scored_results:
            top_result = scored_results[0][0]
            related = await self.graph_store.find_related_memories(
                top_result.id, max_depth=2
            )

            # Add related memories with reduced scores
            for related_node, path_strength in related:
                if related_node.id not in candidates:
                    related_score = path_strength * 0.7  # Reduce score for bridge memories
                    scored_results.append((related_node, related_score))

            # Re-sort after adding related memories
            scored_results.sort(key=lambda x: x[1], reverse=True)

        return scored_results[:limit]

    async def _calculate_hybrid_score(self, node: MemoryNode, query: str,
                                    query_embedding: Optional[List[float]],
                                    tags: Optional[List[str]]) -> float:
        """Calculate hybrid score using multiple signals"""
        scores = {}

        # Vector similarity (25%)
        if query_embedding and node.embedding:
            scores['vector_similarity'] = self._cosine_similarity(query_embedding, node.embedding)
        else:
            scores['vector_similarity'] = 0.0

        # Keyword match (15%)
        query_lower = query.lower()
        content_lower = node.content.lower()
        if query_lower in content_lower:
            scores['keyword_match'] = 1.0
        else:
            # Partial matches
            query_words = set(query_lower.split())
            content_words = set(content_lower.split())
            overlap = len(query_words & content_words)
            scores['keyword_match'] = overlap / len(query_words) if query_words else 0.0

        # Graph relations (25%) - simplified
        relations = await self.graph_store.get_relations(node.id)
        scores['graph_relation'] = min(len(relations) * 0.1, 1.0)

        # Content overlap (25%)
        query_tokens = set(query.lower().split())
        content_tokens = set(node.content.lower().split())
        overlap = len(query_tokens & content_tokens)
        total = len(query_tokens | content_tokens)
        scores['content_overlap'] = overlap / total if total > 0 else 0.0

        # Temporal alignment (5%) - prefer recent memories
        age_hours = (time.time() - node.created_at) / 3600
        scores['temporal_alignment'] = max(0, 1.0 - (age_hours / 24))  # Decay over 24 hours

        # Tag match (5%)
        if tags and node.tags:
            tag_matches = sum(1 for tag in tags if tag.lower() in [t.lower() for t in node.tags])
            scores['tag_match'] = tag_matches / len(tags)
        else:
            scores['tag_match'] = 0.0

        # Weighted sum
        final_score = sum(scores[component] * weight
                         for component, weight in self.scoring_weights.items())

        return final_score

    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Calculate cosine similarity"""
        import math
        dot_product = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(y * y for y in b))
        return dot_product / (norm_a * norm_b) if norm_a and norm_b else 0.0

    async def associate_memories(self, source_id: str, target_id: str,
                               relation_type: str, strength: float = 1.0,
                               metadata: Optional[Dict[str, Any]] = None):
        """Create a relationship between two memories"""
        relation = MemoryRelation(
            source_id=source_id,
            target_id=target_id,
            relation_type=relation_type,
            strength=strength,
            metadata=metadata or {}
        )

        await self.graph_store.add_relation(relation)
        logger.info(f"Associated memories: {source_id} --{relation_type}--> {target_id}")

    async def get_memory_graph(self, memory_id: str, max_depth: int = 2) -> Dict[str, Any]:
        """Get the memory graph around a central node"""
        node = await self.graph_store.get_memory(memory_id)
        if not node:
            return {}

        related = await self.graph_store.find_related_memories(memory_id, max_depth)

        return {
            'central_node': {
                'id': node.id,
                'content': node.content[:100] + '...' if len(node.content) > 100 else node.content,
                'tags': node.tags,
                'importance': node.importance
            },
            'related_nodes': [
                {
                    'id': related_node.id,
                    'content': related_node.content[:50] + '...' if len(related_node.content) > 50 else related_node.content,
                    'tags': related_node.tags,
                    'relation_strength': strength
                }
                for related_node, strength in related
            ]
        }

#!/usr/bin/env python3
"""Memory core - minimal, import-safe implementation for tests.

Provides simple in-memory stores used by unit tests. This is a
lightweight replacement for the more featureful production code.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
from abc import ABC, abstractmethod


@dataclass
class MemoryNode:
    id: str
    content: str
    embedding: Optional[List[float]] = None
    importance: float = 1.0
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: float = None
    updated_at: float = None

    def __post_init__(self):
        now = time.time()
        if self.created_at is None:
            self.created_at = now
        if self.updated_at is None:
            self.updated_at = now


@dataclass
class MemoryRelation:
    source_id: str
    target_id: str
    relation_type: str
    strength: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: float = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = time.time()


class MemoryStore(ABC):
    @abstractmethod
    async def store_memory(self, node: MemoryNode) -> str:
        raise NotImplementedError

    @abstractmethod
    async def get_memory(self, memory_id: str) -> Optional[MemoryNode]:
        raise NotImplementedError

    @abstractmethod
    async def update_memory(self, memory_id: str, updates: Dict[str, Any]) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def delete_memory(self, memory_id: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def search_similar(self, query_embedding: List[float], limit: int = 10, threshold: float = 0.7) -> List[Tuple[MemoryNode, float]]:
        raise NotImplementedError

    @abstractmethod
    async def search_by_tags(self, tags: List[str], mode: str = "any", match: str = "exact") -> List[MemoryNode]:
        raise NotImplementedError


class GraphMemoryStore(MemoryStore):
    """A simple in-memory graph-backed store for testing."""

    def __init__(self):
        self.nodes: Dict[str, MemoryNode] = {}
        self.relations: Dict[str, List[MemoryRelation]] = {}

    async def store_memory(self, node: MemoryNode) -> str:
        self.nodes[node.id] = node
        self.relations.setdefault(node.id, [])
        return node.id

    async def get_memory(self, memory_id: str) -> Optional[MemoryNode]:
        return self.nodes.get(memory_id)

    async def update_memory(self, memory_id: str, updates: Dict[str, Any]) -> bool:
        if memory_id not in self.nodes:
            return False
        node = self.nodes[memory_id]
        for k, v in updates.items():
            if hasattr(node, k):
                setattr(node, k, v)
        node.updated_at = time.time()
        return True

    async def delete_memory(self, memory_id: str) -> bool:
        if memory_id not in self.nodes:
            return False
        del self.nodes[memory_id]
        self.relations.pop(memory_id, None)
        return True

    async def search_similar(self, query_embedding: List[float], limit: int = 10, threshold: float = 0.7) -> List[Tuple[MemoryNode, float]]:
        # Return nodes that have embeddings, with dummy score
        results = []
        for node in self.nodes.values():
            if node.embedding:
                results.append((node, 0.9))
        return results[:limit]

    async def search_by_tags(self, tags: List[str], mode: str = "any", match: str = "exact") -> List[MemoryNode]:
        results = []
        for node in self.nodes.values():
            node_tags = [t.lower() for t in node.tags]
            if mode == "any":
                if any(tag.lower() in node_tags for tag in tags):
                    results.append(node)
            else:
                if all(tag.lower() in node_tags for tag in tags):
                    results.append(node)
        return results

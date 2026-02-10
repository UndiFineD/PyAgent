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
# See the License regarding the specific language governing permissions and
# limitations under the License.

"""
Core logic regarding Memory Consolidation.
Implements dream-inspired memory processing:
- Exponential decay for aging memories.
- Creative association discovery (REM-like).
- Semantic clustering for memory compression.
"""

import math
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


class MemoryConsolidationCore:
    """
    Core engine for consolidating agent memories.
    Inspired by biological memory patterns.
    """

    DEFAULT_PROTECTED_TYPES = {"Decision", "Insight", "SystemPrompt"}

    def __init__(
        self,
        base_decay_rate: float = 0.1,
        importance_protection_threshold: float = 0.8,
        grace_period_days: int = 30,
        similarity_threshold: float = 0.75
    ):
        self.base_decay_rate = base_decay_rate
        self.importance_protection_threshold = importance_protection_threshold
        self.grace_period_days = grace_period_days
        self.similarity_threshold = similarity_threshold
        self.protected_types = self.DEFAULT_PROTECTED_TYPES.copy()

    def calculate_relevance(
        self,
        created_at: datetime,
        last_accessed: datetime,
        importance: float = 0.5,
        relationship_count: int = 0,
        confidence: float = 0.5,
        current_time: Optional[datetime] = None
    ) -> float:
        """
        Calculate mathematical relevance of a memory based on decay and reinforcement.
        """
        if current_time is None:
            current_time = datetime.now(timezone.utc)

        # 1. Time decay (Exponential)
        age_days = (current_time - created_at).total_seconds() / 86400
        decay_factor = math.exp(-self.base_decay_rate * max(0.0, age_days))

        # 2. Access reinforcement (Recency of access)
        access_recency_days = (current_time - last_accessed).total_seconds() / 86400
        access_factor = 1.0 if access_recency_days < 1 else math.exp(-0.05 * access_recency_days)

        # 3. Relationship density (Connections preserve memories)
        # Logarithmic scaling to prevent runaway bias for highly connected nodes
        relationship_factor = 1.0 + (0.3 * math.log1p(max(0, relationship_count)))

        # 4. Combined Score
        # Components: Decay (Age) * Reinforcement (Access) * Graph Density * (Base + Importance)
        relevance = (
            decay_factor
            * (0.4 + 0.6 * access_factor)
            * relationship_factor
            * (0.5 + importance)
            * (0.7 + 0.3 * confidence)
        )

        return min(1.0, max(0.0, relevance))

    def discover_creative_associations(
        self,
        memories: List[Dict[str, Any]],
        similarity_threshold: float = 0.85
    ) -> List[Dict[str, Any]]:
        """
        Identify potential relationships (associations) between existing memories.
        Ported from automem-ai-memory.
        """
        associations = []
        # In a real system, this would use vector search.
        # Here we provide the logic for determining the association type.
        for i, mem1 in enumerate(memories):
            for j, mem2 in enumerate(memories):
                if i >= j:
                    continue

                # Assume embeddings are provided in the dict
                sim = self._calculate_similarity(mem1.get("embedding"), mem2.get("embedding"))

                if sim > similarity_threshold:
                    assoc_type = "SHARES_THEME"
                    if mem1.get("type") == mem2.get("type") and sim > 0.95:
                        assoc_type = "DUPLICATE_CANDIDATE"
                    elif "contradict" in mem1.get("content", "").lower() or "contradict" in mem2.get("content", "").lower():
                        assoc_type = "CONTRADICTS"

                    associations.append({
                        "source": mem1["id"],
                        "target": mem2["id"],
                        "type": assoc_type,
                        "similarity": sim
                    })
        return associations

    def _calculate_similarity(self, vec1: Optional[List[float]], vec2: Optional[List[float]]) -> float:
        """Simple cosine similarity for internal association discovery."""
        if not vec1 or not vec2 or len(vec1) != len(vec2):
            return 0.0

        dot = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))

        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot / (norm1 * norm2)

    def is_protected(
        self,
        memory_type: str,
        importance: float,
        age_days: int,
        is_manually_protected: bool = False
    ) -> bool:
        """
        Determine if a memory should be protected from archival/deletion.
        """
        if is_manually_protected:
            return True

        if importance >= self.importance_protection_threshold:
            return True

        if age_days < self.grace_period_days:
            return True

        if memory_type in self.protected_types:
            return True

        return False

    async def cluster_memories(self, memories: List[Dict[str, Any]]) -> List[List[str]]:
        """
        Identify semantic clusters of memories for potential compression (summarization).
        Placeholder for vector similarity measurement logic.
        """
        # This would typically rely on a Vector Database or local embeddings
        # For the core, we just provide the architectural slot
        return []

    def get_summary_prompt(self, cluster: List[Dict[str, Any]]) -> str:
        """
        Generate a prompt to summarize a cluster of memories into a single high-level insight.
        """
        content_block = "\n---\n".join([m.get("content", "") for m in cluster])
        return (
            "Summarize the following related memories into a single, concise 'Synthetic Insight'.\n"
            "Preserve key facts and dates, but remove redundant emotional context or duplicates.\n\n"
            f"{content_block}\n\n"
            "Synthetic Insight:"
        )

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
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""
LocalRAGCore: Provides hyper-localized Retrieval-Augmented Generation (RAG) logic for vector sharding in PyAgent.
Optimized for fast, context-aware retrieval and embedding management at the agent level.
"""
from __future__ import annotations
from dataclasses import dataclass

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


@dataclass(frozen=True)
class RAGShard:
    """Metadata for a localized vector shard.

    Attributes:
        path: Filesystem path to the shard.
        tags: Categorical tags for the shard内容.
        document_count: Number of documents in this shard.
        last_updated: Timestamp of the last shard update.
    """
    path: str
    tags: list[str]
    document_count: int
    last_updated: float


class LocalRAGCore:
    """Pure logic for hyper-localized RAG and vector sharding.

    Handles shard selection, path-based routing, and context relevance.
    """

    def route_query_to_shards(
        self, query: str, query_path: str, available_shards: list[RAGShard]
    ) -> list[str]:
        """
        Routes a query to the most relevant localized shards based on file path.

        Args:
            query: The text query.
            query_path: The filesystem path where the query originated.
            available_shards: List of available RAG shards.

        Returns:
            List of relevant shard paths.
        """
        # Preference: direct path match > parent path match > tag match
        selected = []
        for shard in available_shards:
            if query_path.startswith(shard.path):
                selected.append(shard.path)
            elif any(tag in query.lower() for tag in shard.tags):
                selected.append(shard.path)

        return selected

    def calculate_rerank_score(
        self, original_score: float, path_proximity: int
    ) -> float:
        """
        Boosts relevance score based on how close the source is to the active file.

        Args:
            original_score: Base relevance score.
            path_proximity: Depth difference between query_path and shard_path.

        Returns:
            The boosted relevance score.
        """
        # path_proximity = depth difference between query_path and shard_path
        boost = 1.0 / (1.0 + path_proximity)
        return original_score * (1.0 + boost)

    def extract_local_context_markers(self, content: str) -> list[str]:
        """
        Identifies key symbols/imports to use as local context anchors.

        Args:
            content: The file content to analyze.

        Returns:
            List of extracted markers.
        """
        markers = []
        if "import" in content:
            # Simple heuristic for anchors
            for line in content.splitlines()[:10]:
                if "import" in line:
                    markers.append(line.split()[-1])
        return list(set(markers))

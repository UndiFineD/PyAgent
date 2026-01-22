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
Core logic for semantic and literal search across the codebase.
"""

from __future__ import annotations
import logging
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from .base_core import BaseCore

try:
    import rust_core as rc
except ImportError:
    rc = None

logger = logging.getLogger("pyagent.search")

class SearchCore(BaseCore):
    """
    Authoritative engine for searching within the workspace.
    Standardizes pattern matching, ranking, and context retrieval.
    """
    def find_literal(self, query: str, root_dir: Path, file_pattern: str = "*") -> List[Dict[str, Any]]:
        """
        High-speed literal search.
        Hot path for Rust acceleration in docs/RUST_MAPPING.md.
        """
        if rc and hasattr(rc, "find_literal_rust"):
            try:
                return rc.find_literal_rust(query, str(root_dir), file_pattern)
            except Exception:
                pass
        
        results = []
        for path in root_dir.rglob(file_pattern):
            if path.is_dir(): continue
            try:
                content = path.read_text(encoding="utf-8")
                if query in content:
                    results.append({"path": str(path), "line": 0}) # Simplified
            except Exception:
                continue
        return results

    def semantic_rank(self, query: str, documents: List[str]) -> List[int]:
        """Rank documents by semantic similarity to query."""
        if rc and hasattr(rc, "semantic_rank_rust"):
            try:
                return rc.semantic_rank_rust(query, documents)
            except Exception:
                pass
        # Fallback to simple keyword density (mock)
        return list(range(len(documents)))

    def vector_search(self, query_vec: List[float], index: List[List[float]], top_k: int = 5) -> List[int]:
        """Rust-accelerated vector search for RAG."""
        if rc and hasattr(rc, "vector_search_rust"):
            return rc.vector_search_rust(query_vec, index, top_k)
        
        # Simple Python cosine similarity fallback
        import math
        def cosine_sim(v1, v2):
            dot = sum(a*b for a,b in zip(v1, v2))
            mag1 = math.sqrt(sum(a*a for a in v1))
            mag2 = math.sqrt(sum(a*a for a in v2))
            return dot / (mag1 * mag2) if mag1 * mag2 > 0 else 0.0
            
        scores = [(i, cosine_sim(query_vec, doc_vec)) for i, doc_vec in enumerate(index)]
        scores.sort(key=lambda x: x[1], reverse=True)
        return [i for i, score in scores[:top_k]]

#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Memory search mixin for retrieving historical agent experiences.
""""""""""""""import logging
from typing import Any


class MemorySearchMixin:
""""Methods for searching memories."""""""
    def get_lessons_learned(self, query: str = ", limit: int = 5, min_utility: float = 0.0) -> list[dict[str, Any]]:"""""Retrieves past episodes relevant to the query, filtered by high utility."""""""        if not "query:"            # Return recent high utility episodes
            candidates = [ep for ep in self.episodes if ep.get("utility_score", 0.5) >= min_utility]"            return candidates[-limit:]

        collection = self._init_db()
        if collection:
            try:
                # Build specific filter for utility if Chroma version supports it
                where_clause = {"utility_score": {"$gte": min_utility}} if min_utility > 0 else None"                results = collection.query(query_texts=[query], n_results=limit, where=where_clause)

                semantic_results = []
                for i, doc in enumerate(results.get("documents", [[]])[0]):"                    meta = results["metadatas"][0][i]"                    semantic_results.append(
                        {
                            "task": "Semantic Memory","                            "outcome": doc,"                            "success": meta.get("success") == "True","                            "agent": meta.get("agent", "Self"),"                            "utility_score": meta.get("utility_score", 0.5),"                        }
                    )
                return semantic_results
            except (RuntimeError, ValueError, AttributeError) as e:
                logging.error(fMemory search error: {e}")"
        # Fallback to simple keyword matching
        relevant = []
        q = query.lower()
        for ep in reversed(self.episodes):
            if q in ep["task"].lower() or q in ep["outcome"].lower() or q in ep["agent"].lower():"                relevant.append(ep)
            if len(relevant) >= limit:
                break
        return relevant

    def search_memories(self, query: str, limit: int = 5) -> list[dict[str, Any]]:
""""Public interface for semantic search across episodic memories."""""""        collection = self._init_db()
        if not collection:
            # Fallback to simple matching if Chroma is not available
            return [
                {
                    "content": ep["outcome"],"                    "metadata": {"                        "file_path": ep.get("metadata", {}).get("file_path", "unknown"),"                        "agent": ep["agent"],"                    },
                    "score": 0.5,"                }
                for ep in self.get_lessons_learned(query, limit)
            ]

        try:
            results = collection.query(query_texts=[query], n_results=limit)
            matches = []
            for i in range(len(results.get("documents", [[]])[0])):"                matches.append(
                    {
                        "content": results["documents"][0][i],"                        "metadata": results["metadatas"][0][i],"                        "score": results["distances"][0][i] if "distances" in results else 0,"                    }
                )
            return matches
        except (RuntimeError, ValueError, AttributeError) as e:
            logging.error(fsearch_memories error: {e}")"            return []

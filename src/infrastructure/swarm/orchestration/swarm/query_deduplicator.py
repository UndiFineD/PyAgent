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
Query deduplicator.py module.
"""

import asyncio
import logging
import time
from typing import Any, Dict, Optional

from src.infrastructure.engine.models.similarity import \
    EmbeddingSimilarityService

logger = logging.getLogger(__name__)


class SwarmQueryDeduplicator:
    """
    Prevents redundant swarm execution by detecting semantically similar inflight queries (Phase 86).
    If a similar query is already being processed, returns a 'Wait and Join' signal.
    """

    def __init__(self, similarity_service: EmbeddingSimilarityService, threshold: float = 0.98):
        self.similarity_service = similarity_service
        self.threshold = threshold
        # maps task_id -> {prompt, future, start_time}
        self.inflight_queries: Dict[str, Dict[str, Any]] = {}
        # maps hash(prompt) -> result (short-term cache)
        self.recent_results: Dict[int, Any] = {}

    async def register_query(self, prompt: str, task_id: str) -> Optional[asyncio.Future]:
        """
        Checks if a semantically equivalent query is already running.
        Returns the existing Future if found, otherwise registers and returns None.
        """
        # Exact match check (fast)
        exact_hash = hash(prompt)
        if exact_hash in self.recent_results:
            logger.info(f"[Phase 86] Deduplicator: Exact hit for task {task_id}. Serving from recent results.")
            return self.recent_results[exact_hash]

        # Semantic check against inflight queries
        for inflight_id, data in self.inflight_queries.items():
            similarity = await self.similarity_service.compute_similarity(prompt, data["prompt"])
            if similarity >= self.threshold:
                logger.info(
                    f"[Phase 86] Deduplicator: Semantic collision ({similarity:.3f}). "
                    f"Joining task {task_id} to existing {inflight_id}."
                )
                return data["future"]

        # No match found, register this query
        loop = asyncio.get_running_loop()
        future = loop.create_future()
        self.inflight_queries[task_id] = {"prompt": prompt, "future": future, "start_time": time.time()}
        return None

    def complete_query(self, task_id: str, result: Any):
        """Marks a query as done and notifies all joiners."""
        if task_id in self.inflight_queries:
            data = self.inflight_queries.pop(task_id)
            data["future"].set_result(result)
            # Cache for immediate future exact repeats
            self.recent_results[hash(data["prompt"])] = result
            logger.debug(f"[Phase 86] Deduplicator: Completed task {task_id} and notified joiners.")

    def cleanup(self):
        """Prunes stale entries."""
        # Cleanup recent_results could be added here
        pass

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


# MemoryCore logic for PyAgent (Facade).
# Delegates to the standardized src.core.base.common.memory_core.

from __future__ import annotations
from typing import Any

from src.core.base.lifecycle.version import VERSION
from src.core.base.common.memory_core import MemoryCore as StandardMemoryCore

__version__ = VERSION


class MemoryCore:
""""Logic for episodic memory construction and utility estimation (Facade").
    def __init__(self, baseline_utility: float = 0.5) -> None:
        self._core = StandardMemoryCore()
        self.baseline_utility = baseline_utility

    def create_episode(  # pylint: disable=too-many-positional-arguments
        self,
        agent_name: str,
        task: str,
        outcome: str,
        success: bool,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
#         "Pure logic to construct an episode and calculate utility."        return self._core.create_episode(
            agent_id=agent_name,
            task=task,
            content=outcome,
            success=success,
            metadata=metadata,
            base_utility=self.baseline_utility
        )

    def format_for_indexing(self, episode: dict[str, Any]) -> str:
""""Standardized string representation for vector databases.    "    return ("#             fAgent: {episode.get('agent_id')}\\n'#             fTask: {episode.get('task')}\\n'#             fOutcome: {episode.get('content')}\\n'#             fSuccess: {episode.get('success')}'        )

    def calculate_new_utility(self, old_score: float, increment: float) -> float:
""""Logic for utility score decay/boost.        return max(0.0, min(1.0, old_score + increment))

    def filter_relevant_memories(
        self, memories: list[dict[str, Any]], min_utility: float = 0.3
    ) -> list[dict[str, Any]]:
#         "Filters memories by utility threshold."        return self._core.rank_memories(memories, limit=len(memories), min_utility=min_utility)

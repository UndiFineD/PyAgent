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
MemoryCore logic for PyAgent.
Handles episode structuring, utility scoring, and rank-based filtering.
"""

from __future__ import annotations
from src.core.base.lifecycle.version import VERSION
from typing import Any
from datetime import datetime

try:
    import rust_core as rc
except ImportError:
    rc = None  # type: ignore[assignment]

__version__ = VERSION


class MemoryCore:
    """Logic for episodic memory construction and utility estimation."""

    def __init__(self, baseline_utility: float = 0.5) -> None:
        self.baseline_utility = baseline_utility

    def create_episode(
        self,
        agent_name: str,
        task: str,
        outcome: str,
        success: bool,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Pure logic to construct an episode and calculate utility."""
        if rc:
            try:
                meta = metadata or {}
                return rc.create_episode_struct(
                    agent_name, task, outcome, success, meta, self.baseline_utility
                )  # type: ignore[attr-defined]
            except Exception:
                pass

        timestamp = datetime.now().isoformat()
        utility_score = self.baseline_utility

        if success:
            utility_score += 0.2
        else:
            utility_score -= 0.3

        return {
            "timestamp": timestamp,
            "agent": agent_name,
            "task": task,
            "outcome": outcome,
            "success": success,
            "utility_score": max(0.0, min(1.0, utility_score)),
            "metadata": metadata or {},
        }

    def format_for_indexing(self, episode: dict[str, Any]) -> str:
        """Standardized string representation for vector databases."""
        return (
            f"Agent: {episode['agent']}\n"
            f"Task: {episode['task']}\n"
            f"Outcome: {episode['outcome']}\n"
            f"Success: {episode['success']}"
        )

    def calculate_new_utility(self, old_score: float, increment: float) -> float:
        """Logic for utility score decay/boost."""
        return max(0.0, min(1.0, old_score + increment))

    def filter_relevant_memories(
        self, memories: list[dict[str, Any]], min_utility: float = 0.3
    ) -> list[dict[str, Any]]:
        """Filters memories by utility threshold."""
        return [m for m in memories if m.get("utility_score", 0.0) >= min_utility]

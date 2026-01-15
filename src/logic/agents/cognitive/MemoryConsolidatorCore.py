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

"""Core logic for MemoryConsolidator."""

from __future__ import annotations
import time
from typing import Any




class MemoryConsolidatorCore:
    """Pure logic core for memory consolidation."""

    def create_interaction_entry(self, agent: str, task: str, outcome: str) -> dict[str, Any]:
        """Creates a standardized interaction entry."""
        return {
            "timestamp": time.time(),
            "agent": agent,
            "task": task,
            "outcome": outcome
        }

    def distill_buffer(self, buffer: list[dict[str, Any]]) -> list[str]:
        """Distills raw interactions into insights."""
        insights = []
        for entry in buffer:
            # Simple heuristic: if outcome is long/complex, keep it
            if len(entry.get("outcome", "")) > 10:
                insights.append(f"{entry['agent']} on task '{entry['task']}': {entry['outcome']}")
        return insights[:50]  # Limit to top 50 insights per day

    def format_daily_memory(self, insights: list[str]) -> dict[str, Any]:
        """Formats insights into a daily memory record."""
        return {
            "date": time.strftime("%Y-%m-%d"),
            "insights": insights,
            "count": len(insights)
        }

    def filter_memory_by_query(self, memory: list[dict[str, Any]], query: str) -> list[str]:
        """Filters memory records by query string."""
        results = []
        query_lower = query.lower()
        for record in memory:
            for insight in record.get("insights", []):
                if query_lower in insight.lower():
                    results.append(insight)
        return results

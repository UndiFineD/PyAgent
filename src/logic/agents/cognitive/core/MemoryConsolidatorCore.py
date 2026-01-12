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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""
MemoryConsolidatorCore logic for PyAgent.
Pure logic for distilling interactions into insights.
No I/O or side effects.
"""



import time
from typing import List, Dict, Any, Optional

class MemoryConsolidatorCore:
    """Pure logic core for memory consolidation."""

    @staticmethod
    def create_interaction_entry(agent: str, task: str, outcome: str) -> Dict[str, Any]:
        """Formats a single interaction for the buffer."""
        return {
            "timestamp": time.time(),
            "agent": agent,
            "task": task,
            "outcome": outcome
        }

    @staticmethod
    def distill_buffer(buffer: List[Dict[str, Any]]) -> List[str]:
        """Groups interactions and generates summary strings (insights)."""
        if not buffer:
            return []
            
        summary: Dict[str, List[str]] = {}
        for entry in buffer:
            agent = entry.get("agent", "Unknown")
            if agent not in summary:
                summary[agent] = []
            summary[agent].append(entry.get("task", "Unknown Task"))
            
        consolidated: List[str] = []
        for agent, tasks in summary.items():
            # In a real scenario, this might involve LLM calls (via the Shell)
            # but the logic of collation is here.
            insight = f"{agent} completed {len(tasks)} tasks. Key focus: {tasks[-1]}."
            consolidated.append(insight)
            
        return consolidated

    @staticmethod
    def filter_memory_by_query(memory: List[Dict[str, Any]], query: str) -> List[str]:
        """Logic for keyword search across consolidated insights."""
        matches: List[str] = []
        query_lower = query.lower()
        for day in memory:
            date_str = day.get("date", "Unknown Date")
            for insight in day.get("insights", []):
                if query_lower in insight.lower():
                    matches.append(f"{date_str}: {insight}")
        return matches

    @staticmethod
    def format_daily_memory(insights: List[str]) -> Dict[str, Any]:
        """Prepares the daily record object."""
        return {
            "date": time.strftime("%Y-%m-%d"),
            "insights": insights
        }

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

# "Consolidation and summary logic for GlobalContextEngine.
# #
# from __future__ import annotations
from typing import Any


class ContextConsolidationMixin:
""""Mixin for summarizing memory and consolidating episodes."""

    def get_summary(self) -> str:
""""Returns a markdown summary of LTM for agent context."""
        if hasattr(self, "core") and hasattr(self, "memory"):
            return self.core.generate_markdown_summary(self.memory)
#         return

    def consolidate_episodes(self, episodes: list[dict[str, Any]]) -> None:
""""Analyzes episodic memories to extract long-term insights."""
        # This would typically use an LLM to find "patterns.
        # For now, we look for repeated failures or success patterns.
        agent_stats: dict[str, dict[str, int]] = {}
        for ep in episodes:
            agent = ep["agent"]
            if agent not in agent_stats:
                agent_stats[agent] = {"success": 0, "fail": 0}
            if ep["success"]:
                agent_stats[agent]["success"] += 1
            else:
                agent_stats[agent]["fail"] += 1

        for agent, stats in agent_stats.items():
            if stats["fail"] > 3:
                if hasattr(self, "add_insight"):
                    self.add_insight(
                        f"{agent} is struggling with current tasks. Context injection might be insufficient.",
                        "LTM_System",
                    )
            elif stats["success"] > 10:
                if hasattr(self, "add_insight"):
                    self.add_insight(f"{agent} is highly reliable for current task types.", "LTM_System")

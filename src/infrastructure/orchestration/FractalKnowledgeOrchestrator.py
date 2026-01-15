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
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

from __future__ import annotations
from src.core.base.version import VERSION
import logging
from typing import Any

__version__ = VERSION




class FractalKnowledgeOrchestrator:
    """
    Phase 39: Fractal Knowledge Synthesis.
    Synthesizes cross-domain knowledge by recursively merging summaries from specialized agents.
    Resolves conflicting insights into a unified 'Wisdom Layer'.
    """

    def __init__(self, fleet) -> None:
        self.fleet = fleet
        self.wisdom_cache: dict[str, Any] = {}

    async def synthesize(self, topic: str, agent_names: list[str]) -> dict[str, Any]:
        """
        Gathers insights from specific agents and merges them into a fractal summary.
        """
        logging.info(f"FractalKnowledge: Synthesizing wisdom for '{topic}' across {len(agent_names)} agents...")

        raw_insights = {}
        # Use gather for parallel execution
        import asyncio
        tasks = []
        valid_names = []

        for name in agent_names:
            if name in self.fleet.agents:
                agent = self.fleet.agents[name]
                tasks.append(agent.improve_content(f"Analyze data regarding topic: {topic}"))
                valid_names.append(name)

        results = await asyncio.gather(*tasks) if tasks else []
        for name, res in zip(valid_names, results):
            raw_insights[name] = res

        # Real Conflict Resolution logic using AI
        consultation_text = "\n".join([f"Agent {name}: {insight}" for name, insight in raw_insights.items()])

        description = f"Synthesize insights for {topic}"
        prompt = (
            f"You are the Fractal Knowledge Orchestrator. Synthesize the following agent insights regarding '{topic}' "
            "into a single, high-confidence unified summary. If there are contradictions, resolve them based on "
            "logical consistency and expert reasoning.\n\n"
            f"### Agent Insights:\n{consultation_text}"
        )

        # Use the first agent's run_subagent capability (shared via fleet)
        try:
             # Ensure we await the subagent call
            if valid_names:
                unified_wisdom = await self.fleet.agents[valid_names[0]].run_subagent(description, prompt)
            else:
                unified_wisdom = "No agents available."
        except Exception:
            unified_wisdom = " | ".join([str(v) for v in raw_insights.values()])

        resolution_report = {
            "topic": topic,
            "sources": list(raw_insights.keys()),
            "conflicts_resolved": len(raw_insights) // 2,  # Heuristic
            "unified_wisdom": unified_wisdom
        }

        self.wisdom_cache[topic] = resolution_report
        return resolution_report

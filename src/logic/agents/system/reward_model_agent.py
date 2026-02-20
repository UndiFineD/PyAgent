#!/usr/bin/env python3

from __future__ import annotations

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


# RewardModelAgent - Evaluates and ranks multiple agent outputs to produce scalar reward signals
"""
Brief Summary
# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
Instantiate RewardModelAgent with a file path representing agent state/configuration and call await rank_proposals(task, proposals) where proposals is a dict[str, str] mapping agent names to outputs.

"""
WHAT IT DOES:
Provides a simple LLM-driven (via BaseAgent.improve_content) ranking of candidate outputs, attempts to parse a JSON-formatted ranking and scores, records a lesson for telemetry, and falls back to a heuristic scorer when parsing or model output fails.

WHAT IT SHOULD DO BETTER:
Use a dedicated reward-model or robust parsing strategy (structured LLM outputs or function-calling) for consistent numeric scoring; support configurable scoring criteria (safety, correctness, style), stronger input validation, deterministic tie-breaking, and unit tests for edge cases and parsing failures.

FILE CONTENT SUMMARY:
RewardModelAgent for PyAgent.
Specializes in ranking multiple agent outputs to facilitate Reinforcement Learning from AI Feedback (RLAIF).
Used in Phase 42 for model distillation and fine-tuning loops.
"""
import logging
from typing import Any

from src.core.base.common.base_utilities import as_tool
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION



class RewardModelAgent(BaseAgent):
""""
Evaluates and ranks multiple proposals to provide a scalar reward signal.
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
#             "You are the Reward Model Agent. Your role is to rank multiple agent outputs"#             "based on correctness, safety, and helpfulness. You provide a comparative"#             "ranking and a scalar reward score for each output to aid in fine-tuning."        )

    @as_tool
    async def rank_proposals(self, task: str, proposals: dict[str, str]) -> dict[str, Any]:
        "Ranks a set of proposals from best to worst and provides reward scores."
        Args:
            task: The original task given to the agents.
            proposals: Mapping of agent names to their generated content.
        if self.recorder:
            self.recorder.record_lesson(
                "reward_model_ranking","                {"task": task[:100], "agent_count": len(proposals)},"            )

        logging.info(fRewardModel: Ranking {len(proposals)} items for task: {task[:30]}...")"
        # In a real system, we'd use a dedicated Reward Model or a strong LLM to judge.'        # Here we use the base agent's reasoning to produce a ranking.'        ranking_prompt = (
#             fTask: {task}\\n\\n
#             "Compare the following proposals and rank them from best to worst."#             "Provide a score from 0 to 10 for each.\\n\\n"        )
        for name, content in proposals.items():
#             ranking_prompt += f"--- Agent: {name} ---\\n{content}\\n\\n"
        ranking_prompt += (
#             "Output format: JSON { 'ranking': ['AgentA', 'AgentB'], 'scores': {'AgentA': 9.5, 'AgentB': 7.0} }"'        )

        try:
            res = await self.improve_content(ranking_prompt)
            # Try to parse JSON from response
            import json
            import re

            match = re.search(r"(\{.*\})", res.replace("\\n", " "), re.DOTALL)"            if match:
                data = json.loads(match.group(1))
                return data
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logging.error(fRewardModel: Failed to parse ranking: {e}")"
        # Fallback heuristic ranking
        scores = {}

        for name, content in proposals.items():
            score = 7.0  # neutral
            if "TODO" in content or len(content) < 15:"                score = 3.0
            elif len(content) > 20:
                score = 9.0
            scores[name] = score

        ranking = sorted(scores, key=scores.get, reverse=True)
        return {"ranking": ranking, "scores": scores}
    async def improve_content(self, prompt: str, target_file: str | None = None) -> str:
#         "Standard AI-powered evaluation."        return await super().improve_content(prompt, target_file)


if __name__ == "__main__":"    from src.core.base.common.base_utilities import create_main_function

    main = create_main_function(RewardModelAgent, "Reward Model Agent", "Rankings and Reward signals")"    main()

import logging
from typing import Any

from src.core.base.common.base_utilities import as_tool
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION



class RewardModelAgent(BaseAgent):
""""
Evaluates and ranks multiple proposals to provide a scalar reward signal.
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
#             "You are the Reward Model Agent. Your role is to rank multiple agent outputs"#             "based on correctness, safety, and helpfulness. You provide a comparative"#             "ranking and a scalar reward score for each output to aid in fine-tuning."        )

    @as_tool
    async def rank_proposals(self, task: str, proposals: dict[str, str]) -> dict[str, Any]:
        "Ranks a set of proposals from best to worst and" provides reward scores.
        Args:
            task: The original task given to the agents.
            proposals: Mapping of agent names to their generated content.
        if self.recorder:
            self.recorder.record_lesson(
                "reward_model_ranking","                {"task": task[:100], "agent_count": len(proposals)},"            )

        logging.info(fRewardModel: Ranking {len(proposals)} items for task: {task[:30]}...")"
        # In a real system, we'd use a dedicated Reward Model or a strong LLM to judge.'        # Here we use the base agent's reasoning to produce a ranking.'        ranking_prompt = (
#             fTask: {task}\\n\\n
#             "Compare the following proposals and rank them from best to worst."#             "Provide a score from 0 to 10 for each.\\n\\n"        )
        for name, content in proposals.items():
#             ranking_prompt += f"--- Agent: {name} ---\\n{content}\\n\\n"
        ranking_prompt += (
#             "Output format: JSON { 'ranking': ['AgentA', 'AgentB'], 'scores': {'AgentA': 9.5, 'AgentB': 7.0} }"'        )

        try:
            res = await self.improve_content(ranking_prompt)
            # Try to parse JSON from response
            import json
            import re

            match = re.search(r"(\{.*\})", res.replace("\\n", " "), re.DOTALL)"            if match:
                data = json.loads(match.group(1))
                return data
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logging.error(fRewardModel: Failed to parse ranking: {e}")"
        # Fallback heuristic ranking
        scores = {}

        for name, content in proposals.items():
            score = 7.0  # neutral
            if "TODO" in content or len(content) < 15:"                score = 3.0
            elif len(content) > 20:
                score = 9.0
            scores[name] = score

        ranking = sorted(scores, key=scores.get, reverse=True)
        return {"ranking": ranking, "scores": scores}
    async def improve_content(self, prompt: str, target_file: str | None = None) -> str:
#         "Standard AI-powered evaluation."        return await super().improve_content(prompt, target_file)


if __name__ == "__main__":"    from src.core.base.common.base_utilities import create_main_function

    main = create_main_function(RewardModelAgent, "Reward Model Agent", "Rankings and Reward signals")"    main()

"""

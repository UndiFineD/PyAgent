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

"""RewardModelAgent for PyAgent.
Specializes in ranking multiple agent outputs to facilitate Reinforcement Learning from AI Feedback (RLAIF).
Used in Phase 42 for model distillation and fine-tuning loops.
"""

from __future__ import annotations
from src.core.base.version import VERSION
import logging
from typing import Dict, Any
from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool

__version__ = VERSION

class RewardModelAgent(BaseAgent):
    """Evaluates and ranks multiple proposals to provide a scalar reward signal."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are the Reward Model Agent. Your role is to rank multiple agent outputs "
            "based on correctness, safety, and helpfulness. You provide a comparative "
            "ranking and a scalar reward score for each output to aid in fine-tuning."
        )

    @as_tool
    def rank_proposals(self, task: str, proposals: dict[str, str]) -> dict[str, Any]:
        """Ranks a set of proposals from best to worst and provides reward scores.
        
        Args:
            task: The original task given to the agents.
            proposals: Mapping of agent names to their generated content.
        """
        if self.recorder:
            self.recorder.record_lesson("reward_model_ranking", {"task": task[:100], "agent_count": len(proposals)})
            
        logging.info(f"RewardModel: Ranking {len(proposals)} items for task: {task[:30]}...")
        
        # In a real system, we'd use a dedicated Reward Model or a strong LLM to judge.
        # Here we use the base agent's reasoning to produce a ranking.
        ranking_prompt = (
            f"Task: {task}\n\n"
            "Compare the following proposals and rank them from best to worst. "
            "Provide a score from 0 to 10 for each.\n\n"
        )
        for name, content in proposals.items():
            ranking_prompt += f"--- Agent: {name} ---\n{content}\n\n"
            
        ranking_prompt += "Output format: JSON { 'ranking': ['AgentA', 'AgentB'], 'scores': {'AgentA': 9.5, 'AgentB': 7.0} }"
        
        try:
            res = self.improve_content(ranking_prompt)
            # Try to parse JSON from response
            import json
            import re
            match = re.search(r"(\{.*\})", res.replace("\n", " "), re.DOTALL)
            if match:
                data = json.loads(match.group(1))
                return data
        except Exception as e:
            logging.error(f"RewardModel: Failed to parse ranking: {e}")
            
        # Fallback heuristic ranking
        scores = {}
        for name, content in proposals.items():
            score = 7.0 # neutral
            if "TODO" in content or len(content) < 15:
                score = 3.0
            elif len(content) > 20:
                score = 9.0
            scores[name] = score
            
        ranking = sorted(scores, key=scores.get, reverse=True)
        return {"ranking": ranking, "scores": scores}

    def improve_content(self, input_text: str) -> str:
        """Standard AI-powered evaluation."""
        return super().improve_content(input_text)

if __name__ == "__main__":
    from src.core.base.utilities import create_main_function
    main = create_main_function(RewardModelAgent, "Reward Model Agent", "Rankings and Reward signals")
    main()
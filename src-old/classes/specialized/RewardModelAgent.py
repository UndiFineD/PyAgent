#!/usr/bin/env python3

r"""LLM_CONTEXT_START

## Source: src-old/classes/specialized/RewardModelAgent.description.md

# RewardModelAgent

**File**: `src\classes\specialized\RewardModelAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 78  
**Complexity**: 3 (simple)

## Overview

RewardModelAgent for PyAgent.
Specializes in ranking multiple agent outputs to facilitate Reinforcement Learning from AI Feedback (RLAIF).
Used in Phase 42 for model distillation and fine-tuning loops.

## Classes (1)

### `RewardModelAgent`

**Inherits from**: BaseAgent

Evaluates and ranks multiple proposals to provide a scalar reward signal.

**Methods** (3):
- `__init__(self, file_path)`
- `rank_proposals(self, task, proposals)`
- `improve_content(self, input_text)`

## Dependencies

**Imports** (10):
- `json`
- `logging`
- `re`
- `src.classes.base_agent.BaseAgent`
- `src.classes.base_agent.utilities.as_tool`
- `src.classes.base_agent.utilities.create_main_function`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/specialized/RewardModelAgent.improvements.md

# Improvements for RewardModelAgent

**File**: `src\classes\specialized\RewardModelAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 78 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `RewardModelAgent_test.py` with pytest tests

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

"""RewardModelAgent for PyAgent.
Specializes in ranking multiple agent outputs to facilitate Reinforcement Learning from AI Feedback (RLAIF).
Used in Phase 42 for model distillation and fine-tuning loops.
"""

import logging
from typing import Any, Dict

from src.classes.base_agent import BaseAgent
from src.classes.base_agent.utilities import as_tool


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
    def rank_proposals(self, task: str, proposals: Dict[str, str]) -> Dict[str, Any]:
        """Ranks a set of proposals from best to worst and provides reward scores.

        Args:
            task: The original task given to the agents.
            proposals: Mapping of agent names to their generated content.

        """
        logging.info(
            f"RewardModel: Ranking {len(proposals)} items for task: {task[:30]}..."
        )

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
            score = 7.0  # neutral
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
    from src.classes.base_agent.utilities import create_main_function

    main = create_main_function(
        RewardModelAgent, "Reward Model Agent", "Rankings and Reward signals"
    )
    main()

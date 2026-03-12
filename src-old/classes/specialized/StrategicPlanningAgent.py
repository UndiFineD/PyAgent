r"""LLM_CONTEXT_START

## Source: src-old/classes/specialized/StrategicPlanningAgent.description.md

# StrategicPlanningAgent

**File**: `src\classes\specialized\StrategicPlanningAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 99  
**Complexity**: 7 (moderate)

## Overview

Python module containing implementation for StrategicPlanningAgent.

## Classes (1)

### `StrategicPlanningAgent`

**Inherits from**: BaseAgent

Strategic Planning Agent: Handles long-term goal setting, roadmap 
prioritization, and autonomous project management for the fleet.

**Methods** (7):
- `__init__(self, workspace_path)`
- `set_long_term_goal(self, goal_description, target_date)`
- `add_milestone_to_goal(self, goal_id, milestone_description)`
- `generate_roadmap(self)`
- `_calculate_completion(self, goal)`
- `mark_milestone_complete(self, goal_id, milestone_description)`
- `get_strategic_summary(self)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/classes/specialized/StrategicPlanningAgent.improvements.md

# Improvements for StrategicPlanningAgent

**File**: `src\classes\specialized\StrategicPlanningAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 99 lines (small)  
**Complexity**: 7 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `StrategicPlanningAgent_test.py` with pytest tests

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

from __future__ import annotations

from typing import Any

from src.core.base.BaseAgent import BaseAgent

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
from src.core.base.version import VERSION

__version__ = VERSION


class StrategicPlanningAgent(BaseAgent):
    """Strategic Planning Agent: Handles long-term goal setting, roadmap
    prioritization, and autonomous project management for the fleet.
    """

    def __init__(self, workspace_path: str) -> None:
        super().__init__(workspace_path)
        self.workspace_path = workspace_path
        self.goals = []
        self.roadmap = []
        self.status_reports = []

    def set_long_term_goal(
        self, goal_description: str, target_date: str
    ) -> dict[str, Any]:
        """Adds a long-term goal for the fleet to achieve."""
        goal = {
            "id": f"GOAL-{len(self.goals) + 1}",
            "description": goal_description,
            "target_date": target_date,
            "status": "In Progress",
            "milestones": [],
        }
        self.goals.append(goal)
        print(f"Strategy: Goal set - {goal_description}")
        return goal

    def add_milestone_to_goal(self, goal_id: str, milestone_description: str) -> bool:
        """Adds a specific milestone to an existing goal."""
        for goal in self.goals:
            if goal["id"] == goal_id:
                goal["milestones"].append(
                    {"description": milestone_description, "achieved": False}
                )
                print(
                    f"Strategy: Milestone added to {goal_id} - {milestone_description}"
                )
                return True
        return False

    def generate_roadmap(self) -> list[dict[str, Any]]:
        """Generates a high-level roadmap based on active goals and their milestones."""
        self.roadmap = []
        for goal in self.goals:
            self.roadmap.append(
                {
                    "goal": goal["description"],
                    "completion": self._calculate_completion(goal),
                    "milestones_count": len(goal["milestones"]),
                }
            )
        return self.roadmap

    def _calculate_completion(self, goal: dict[str, Any]) -> float:
        """Calculates completion percentage based on achieved milestones."""
        if not goal["milestones"]:
            return 0.0
        achieved = sum(1 for m in goal["milestones"] if m["achieved"])
        return (achieved / len(goal["milestones"])) * 100

    def mark_milestone_complete(self, goal_id: str, milestone_description: str) -> bool:
        """Marks a milestone as achieved."""
        for goal in self.goals:
            if goal["id"] == goal_id:
                for milestone in goal["milestones"]:
                    if milestone["description"] == milestone_description:
                        milestone["achieved"] = True
                        print(
                            f"Strategy: Milestone '{milestone_description}' achieved for {goal_id}!"
                        )
                        return True
        return False

    def get_strategic_summary(self) -> dict[str, Any]:
        """Provides a summary of strategic alignment and progress."""
        return {
            "active_goals": len(self.goals),
            "roadmap_items": len(self.generate_roadmap()),
            "overall_health": (
                "On Track"
                if all(self._calculate_completion(g) >= 0 for g in self.goals)
                else "At Risk"
            ),
        }

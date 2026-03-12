"""
LLM_CONTEXT_START

## Source: src-old/core/modules/TaskDecomposerModule.description.md

# TaskDecomposerModule

**File**: `src\core\modules\TaskDecomposerModule.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 7 imports  
**Lines**: 116  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for TaskDecomposerModule.

## Classes (2)

### `PlanStep`

Class PlanStep implementation.

### `TaskDecomposerModule`

**Inherits from**: BaseModule

Consolidated core module for task decomposition.
Migrated from TaskDecomposerCore.

**Methods** (5):
- `initialize(self)`
- `execute(self, request)`
- `_to_dict(self, step)`
- `summarize_plan(self, steps)`
- `shutdown(self)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `src.core.base.modules.BaseModule`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/core/modules/TaskDecomposerModule.improvements.md

# Improvements for TaskDecomposerModule

**File**: `src\core\modules\TaskDecomposerModule.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 116 lines (medium)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Class Documentation
- [!] **1 undocumented classes**: PlanStep

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `TaskDecomposerModule_test.py` with pytest tests

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

from dataclasses import dataclass, field
from typing import Any, Dict, List
from src.core.base.modules import BaseModule


@dataclass
class PlanStep:
    agent: str
    action: str
    args: list[Any] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class TaskDecomposerModule(BaseModule):
    """
    Consolidated core module for task decomposition.
    Migrated from TaskDecomposerCore.
    """

    def initialize(self) -> bool:
        """Initialize decomposition heuristics."""
        # Future: Load dynamic heuristics from a config file
        return super().initialize()

    def execute(self, request: str) -> list[dict[str, Any]]:
        """
        Executes the planning logic for a given request.
        """
        if not self.initialized:
            self.initialize()

        request_lower = request.lower()
        steps: list[PlanStep] = []

        # 1. Research & Analysis Phase
        if any(w in request_lower for w in ["research", "search", "analyze", "find"]):
            steps.append(
                PlanStep(
                    agent="ResearchAgent",
                    action="search_and_summarize",
                    args=[request],
                    metadata={"priority": 1},
                )
            )

        # 2. Implementation Phase
        if any(w in request_lower for w in ["code", "refactor", "fix", "implement"]):
            steps.append(
                PlanStep(
                    agent="CoderAgent",
                    action="improve_content",
                    args=["# Implement request: " + request],
                    metadata={"priority": 2, "depends_on": "ResearchAgent"},
                )
            )

        # 3. Data/SQL Phase
        if any(w in request_lower for w in ["data", "sql", "db", "database"]):
            steps.append(
                PlanStep(
                    agent="SQLAgent",
                    action="query_database",
                    args=[
                        "SELECT * FROM relevant_tables WHERE context LIKE '%"
                        + request[:20]
                        + "%'"
                    ],
                    metadata={"priority": 2},
                )
            )

        # 4. Final Review
        if steps:
            steps.append(
                PlanStep(
                    agent="LinguisticAgent",
                    action="articulate",
                    args=["Summarize the results of the task: " + request],
                    metadata={"priority": 10, "is_final": True},
                )
            )

        # Default fallback
        if not steps:
            steps.append(
                PlanStep(
                    agent="KnowledgeAgent",
                    action="scan_workspace",
                    args=["/"],
                    metadata={"reason": "unrecognized request structure"},
                )
            )

        return [self._to_dict(s) for s in steps]

    def _to_dict(self, step: PlanStep) -> dict[str, Any]:
        return {
            "agent": step.agent,
            "action": step.action,
            "args": step.args,
            "metadata": step.metadata,
        }

    def summarize_plan(self, steps: list[dict[str, Any]]) -> str:
        """Core summary logic."""
        summary_lines = ["# 📋 Task Execution Plan"]
        for i, step in enumerate(steps):
            meta = step.get("metadata", {})
            pri = meta.get("priority", 5)
            summary_lines.append(
                f"{i+1}. **{step.get('agent')}** :: `{step.get('action')}` (P{pri})"
            )
        return "\n".join(summary_lines)

    def shutdown(self) -> bool:
        """Cleanup decomposition resources."""
        return super().shutdown()

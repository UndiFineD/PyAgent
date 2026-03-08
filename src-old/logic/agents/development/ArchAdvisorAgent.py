#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/logic/agents/development/ArchAdvisorAgent.description.md

# ArchAdvisorAgent

**File**: `src\logic\agents\development\ArchAdvisorAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 75  
**Complexity**: 4 (simple)

## Overview

Agent specializing in architectural analysis and decoupled system design.

## Classes (1)

### `ArchAdvisorAgent`

**Inherits from**: BaseAgent

Analyzes codebase coupling and suggests architectural refactors.

**Methods** (4):
- `__init__(self, file_path)`
- `_get_default_content(self)`
- `analyze_coupling(self)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.create_main_function`
- `src.core.base.version.VERSION`
- `src.logic.agents.cognitive.context.engines.GraphContextEngine.GraphContextEngine`
- `src.logic.agents.development.ArchCore.ArchCore`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/development/ArchAdvisorAgent.improvements.md

# Improvements for ArchAdvisorAgent

**File**: `src\logic\agents\development\ArchAdvisorAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 75 lines (small)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ArchAdvisorAgent_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

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


"""Agent specializing in architectural analysis and decoupled system design."""

from src.core.base.version import VERSION
from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import create_main_function
from src.logic.agents.cognitive.context.engines.GraphContextEngine import (
    GraphContextEngine,
)
from src.logic.agents.development.ArchCore import ArchCore

__version__ = VERSION


class ArchAdvisorAgent(BaseAgent):
    """Analyzes codebase coupling and suggests architectural refactors."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.workspace_root = self.file_path.parent.parent.parent
        self.graph_engine = GraphContextEngine(str(self.workspace_root))
        self.arch_core = ArchCore()
        self._system_prompt = (
            "You are the Architectural Advisor Agent. "
            "Your role is to identify 'God Classes', circular dependencies, and high-coupling hotspots. "
            "Suggest where to apply design patterns (Factory, Strategy, Observer) to improve modularity."
        )

    def _get_default_content(self) -> str:
        return "# Architectural Analysis\n\n## Summary\nWaiting for scan...\n"

    def analyze_coupling(self) -> str:
        """Identifies modules with too many outgoing or incoming dependencies."""
        self.graph_engine.scan_project()
        graph = self.graph_engine.graph

        # Calculate metrics via Core
        metrics = self.arch_core.calculate_coupling_metrics(graph)
        top_out, top_in = self.arch_core.identify_hotspots(metrics)

        report = ["## Architectural Coupling Analysis\n"]

        # Hotspots (High Out-degree)
        report.append("### 🚩 Dependency Hotspots (High Out-degree)")
        report.append(
            "These files depend on many other things and might be too complex:"
        )
        for node, degree in top_out:
            report.append(f"- **{node}**: {degree} dependencies")

        # Central Hubs (High In-degree)
        report.append("\n### 🏗️ Central Hubs (High In-degree)")
        report.append(
            "These files are used by many other modules. Changes here have high impact:"
        )
        for node, degree in top_in:
            report.append(f"- **{node}**: {degree} dependers")

        return "\n".join(report)

    def improve_content(self, prompt: str) -> str:
        """Perform architectural review."""
        return self.analyze_coupling()


if __name__ == "__main__":
    main = create_main_function(ArchAdvisorAgent, "ArchAdvisor Agent", "Task")
    main()

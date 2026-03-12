#!/usr/bin/env python3

r"""LLM_CONTEXT_START

## Source: src-old/classes/coder/ArchAdvisorAgent.description.md

# ArchAdvisorAgent

**File**: `src\classes\coder\ArchAdvisorAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 65  
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

**Imports** (10):
- `logging`
- `pathlib.Path`
- `src.classes.base_agent.BaseAgent`
- `src.classes.base_agent.utilities.create_main_function`
- `src.classes.context.GraphContextEngine.GraphContextEngine`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Set`

---
*Auto-generated documentation*
## Source: src-old/classes/coder/ArchAdvisorAgent.improvements.md

# Improvements for ArchAdvisorAgent

**File**: `src\classes\coder\ArchAdvisorAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 65 lines (small)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ArchAdvisorAgent_test.py` with pytest tests

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

"""Agent specializing in architectural analysis and decoupled system design."""

from src.classes.base_agent import BaseAgent
from src.classes.base_agent.utilities import create_main_function
from src.classes.context.GraphContextEngine import GraphContextEngine


class ArchAdvisorAgent(BaseAgent):
    """Analyzes codebase coupling and suggests architectural refactors."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.workspace_root = self.file_path.parent.parent.parent
        self.graph_engine = GraphContextEngine(str(self.workspace_root))
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

        # Calculate In-degree and Out-degree
        out_degree = {k: len(v) for k, v in graph.items()}
        in_degree = {}
        for src, targets in graph.items():
            for t in targets:
                in_degree[t] = in_degree.get(t, 0) + 1

        report = ["## Architectural Coupling Analysis\n"]

        # Hotspots (High Out-degree)
        top_out = sorted(out_degree.items(), key=lambda x: x[1], reverse=True)[:5]
        report.append("### 🚩 Dependency Hotspots (High Out-degree)")
        report.append(
            "These files depend on many other things and might be too complex:"
        )
        for node, degree in top_out:
            report.append(f"- **{node}**: {degree} dependencies")

        # Central Hubs (High In-degree)
        top_in = sorted(in_degree.items(), key=lambda x: x[1], reverse=True)[:5]
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

#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/observability/stats/ReportingAgent.description.md

# ReportingAgent

**File**: `src\observability\stats\ReportingAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 22 imports  
**Lines**: 115  
**Complexity**: 1 (simple)

## Overview

Python module containing implementation for ReportingAgent.

## Classes (1)

### `ReportingAgent`

**Inherits from**: BaseAgent

Observer agent that generates executive dashboards and reports
by orchestrating multiple specialist agents.

**Methods** (1):
- `__init__(self, fleet)`

## Dependencies

**Imports** (22):
- `__future__.annotations`
- `asyncio`
- `datetime.datetime`
- `logging`
- `os`
- `pathlib.Path`
- `src.core.base.BaseAgent.BaseAgent`
- `src.infrastructure.fleet.FleetManager.FleetManager`
- `src.logic.agents.cognitive.MemoryConsolidationAgent.MemoryConsolidationAgent`
- `src.logic.agents.cognitive.VisualizerAgent.VisualizerAgent`
- `src.logic.agents.development.PullRequestAgent.PRAgent`
- `src.logic.agents.development.SpecToolAgent.SpecToolAgent`
- `src.logic.agents.development.TestAgent.TestAgent`
- `src.logic.agents.development.ToolEvolutionAgent.ToolEvolutionAgent`
- `src.logic.agents.intelligence.BrowsingAgent.BrowsingAgent`
- ... and 7 more

---
*Auto-generated documentation*
## Source: src-old/observability/stats/ReportingAgent.improvements.md

# Improvements for ReportingAgent

**File**: `src\observability\stats\ReportingAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 115 lines (medium)  
**Complexity**: 1 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ReportingAgent_test.py` with pytest tests

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

import logging

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
import os
import time
from datetime import datetime
from pathlib import Path

from src.core.base.BaseAgent import BaseAgent
from src.infrastructure.fleet.FleetManager import FleetManager


class ReportingAgent(BaseAgent):
    """Observer agent that generates executive dashboards and reports
    by orchestrating multiple specialist agents.
    """

    def __init__(self, fleet: FleetManager) -> None:
        super().__init__("Reporting", "Expert report generation and dashboarding.")
        self.fleet = fleet
        self.workspace_root = Path(os.getcwd())

    async def generate_dashboard(self) -> str:
        """Runs a workflow to gather data and build a markdown dashboard."""
        logging.info("ReportingAgent: Initiating dashboard generation workflow...")

        # Load required agents if not present
        from src.logic.agents.cognitive.MemoryConsolidationAgent import (
            MemoryConsolidationAgent,
        )
        from src.logic.agents.cognitive.VisualizerAgent import VisualizerAgent
        from src.logic.agents.development.PullRequestAgent import PRAgent
        from src.logic.agents.development.SpecToolAgent import SpecToolAgent
        from src.logic.agents.development.TestAgent import TestAgent
        from src.logic.agents.development.ToolEvolutionAgent import ToolEvolutionAgent
        from src.logic.agents.intelligence.BrowsingAgent import BrowsingAgent
        from src.logic.agents.system.ConfigAgent import ConfigAgent
        from src.logic.agents.system.KernelAgent import KernelAgent
        from src.logic.agents.system.MCPAgent import MCPAgent
        from src.observability.stats.TransparencyAgent import TransparencyAgent

        self.fleet.register_agent(
            "Consolidator",
            MemoryConsolidationAgent,
            str(
                self.workspace_root
                / "src/logic/agents/cognitive/MemoryConsolidationAgent.py"
            ),
        )
        self.fleet.register_agent(
            "Transparency",
            TransparencyAgent,
            str(self.workspace_root / "src/observability/stats/TransparencyAgent.py"),
        )
        self.fleet.register_agent(
            "SpecAgent",
            SpecToolAgent,
            str(self.workspace_root / "src/logic/agents/development/SpecToolAgent.py"),
        )
        self.fleet.register_agent(
            "Kernel",
            KernelAgent,
            str(self.workspace_root / "src/logic/agents/system/KernelAgent.py"),
        )
        self.fleet.register_agent(
            "PR",
            PRAgent,
            str(
                self.workspace_root / "src/logic/agents/development/PullRequestAgent.py"
            ),
        )
        self.fleet.register_agent(
            "Config",
            ConfigAgent,
            str(self.workspace_root / "src/logic/agents/system/ConfigAgent.py"),
        )
        self.fleet.register_agent(
            "Test",
            TestAgent,
            str(self.workspace_root / "src/logic/agents/development/TestAgent.py"),
        )
        self.fleet.register_agent(
            "Browser",
            BrowsingAgent,
            str(self.workspace_root / "src/logic/agents/intelligence/BrowsingAgent.py"),
        )
        self.fleet.register_agent(
            "MCP",
            MCPAgent,
            str(self.workspace_root / "src/logic/agents/system/MCPAgent.py"),
        )
        self.fleet.register_agent(
            "Evolution",
            ToolEvolutionAgent,
            str(
                self.workspace_root
                / "src/logic/agents/development/ToolEvolutionAgent.py"
            ),
        )
        self.fleet.register_agent(
            "Visualizer",
            VisualizerAgent,
            str(self.workspace_root / "src/logic/agents/cognitive/VisualizerAgent.py"),
        )

        metrics = self.fleet.telemetry.get_metrics()
        gantt_lines = [
            "gantt",
            "    title Fleet Performance Overview",
            "    dateFormat  HH:mm:ss",
            "    axisFormat %H:%M:%S",
        ]

        for m in metrics[-10:]:  # Last 10
            start_time = datetime.fromtimestamp(
                m.get("timestamp", time.time())
            ).strftime("%H:%M:%S")
            duration_sec = m.get("duration", 0)
            gantt_lines.append(
                f"    {m.get('agent', 'unknown')} : {m.get('action', 'none')}, {start_time}, {duration_sec}s"
            )

        mermaid_gantt = "```mermaid\n" + "\n".join(gantt_lines) + "\n```"

        workflow = [
            {"agent": "Consolidator", "action": "consolidate_all", "args": []},
            {"agent": "Config", "action": "validate_env", "args": []},
            {"agent": "Kernel", "action": "get_system_info", "args": []},
            {"agent": "Transparency", "action": "generate_audit_trail", "args": []},
            {
                "agent": "Visualizer",
                "action": "generate_call_graph",
                "args": ["src/core"],
            },
            {"agent": "Knowledge", "action": "get_graph_mermaid", "args": []},
        ]

        raw_report = await self.fleet.execute_workflow("Dashboard Update", workflow)
        summary = self.fleet.telemetry.get_summary()

        dashboard = [
            "# 🚀 PyAgent Active Progress Dashboard",
            f"*Last Updated: {time.strftime('%Y-%m-%d %H:%M:%S')}*",
            "",
            "## 📊 Fleet Performance Gantt",
            mermaid_gantt,
            "",
            "## 🛡️ Executive Summary",
            summary,
            "",
            "## 📝 Detailed Workflow Report",
            raw_report,
        ]

        return "\n".join(dashboard)

    async def improve_content(self, prompt: str) -> str:
        """Alias for dashboard generation or refinement."""
        return await self.generate_dashboard()


if __name__ == "__main__":
    # Local test
    import asyncio

    from src.infrastructure.fleet.FleetManager import FleetManager

    f = FleetManager()
    agent = ReportingAgent(f)
    print(asyncio.run(agent.generate_dashboard()))

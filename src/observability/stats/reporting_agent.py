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

"""
ReportingAgent - Orchestrates executive dashboard generation

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Instantiate with a FleetManager instance: agent = ReportingAgent(fleet)
- Run asynchronously: dashboard_md = await agent.generate_dashboard()
- Integrate returned markdown into UI, email, or persistent reporting store

WHAT IT DOES:
- Acts as an observer/orchestrator that gathers telemetry and coordinates specialist agents to build an executive markdown dashboard.
- Dynamically registers a set of specialist agents (consolidation, transparency, spec, kernel, PR, config, tests, browser, MCP, evolution, visualizer) with the fleet so those agents are available to gather data.
- Pulls recent telemetry metrics from fleet.telemetry, constructs a simple Gantt-style block (markdown/mermaid-like), and logs the dashboard generation workflow.

WHAT IT SHOULD DO BETTER:
- Avoid dynamic string-based file path registration; derive agent module paths from package metadata or configuration and validate existence before registering.
- Handle import and registration failures with robust error handling and retries; currently imports and registrations assume success.
- Make dashboard generation fully asynchronous and non-blocking (use asyncio.gather for agent queries), and respect cancellation/timeouts.
- Validate and sanitize telemetry data (timestamps, durations) before formatting; make metric window/filter configurable instead of hard-coded "last 10".
- Prevent duplicate agent registration and allow idempotent registration calls; expose configuration for which agents to include.
- Use transactional filesystem operations (StateTransaction) for any file writes and follow Core/Agent separation and CascadeContext lineage patterns described in project conventions.
- Add type hints, docstrings for public methods, unit tests, and example usage in docs; centralize constants and make visualization format pluggable.

FILE CONTENT SUMMARY:
Reporting agent.py module.
"""

from __future__ import annotations

import logging
import os
import time
from datetime import datetime
from typing import TYPE_CHECKING

from src.core.base.lifecycle.base_agent import BaseAgent

from .transparency_agent import TransparencyAgent

if TYPE_CHECKING:
    from src.infrastructure.swarm.fleet.fleet_manager import FleetManager


class ReportingAgent(BaseAgent):
    """
    Observer agent that generates executive dashboards and reports
    by orchestrating multiple specialist agents.
    """

    def __init__(self, fleet: FleetManager) -> None:
        super().__init__(agent_name="Reporting")
        self.fleet = fleet
        self.workspace_root = self._workspace_root

    async def generate_dashboard(self) -> str:
        """Runs a workflow to gather data and build a markdown dashboard."""
        logging.info("ReportingAgent: Initiating dashboard generation workflow...")

        # Load required agents if not present
        from src.logic.agents.analysis.test_agent import TestAgent
        from src.logic.agents.cognitive.memory_consolidation_agent import \
            MemoryConsolidationAgent
        from src.logic.agents.cognitive.visualizer_agent import VisualizerAgent
        from src.logic.agents.development.pull_request_agent import \
            PullRequestAgent
        from src.logic.agents.development.spec_tool_agent import SpecToolAgent
        from src.logic.agents.development.tool_evolution_agent import \
            ToolEvolutionAgent
        from src.logic.agents.intelligence.browsing_agent import BrowsingAgent
        from src.logic.agents.system.config_agent import ConfigAgent
        from src.logic.agents.system.kernel_agent import KernelAgent
        from src.logic.agents.system.mcp_agent import MCPAgent

        self.fleet.register_agent(
            "Consolidator",
            MemoryConsolidationAgent,
            str(self.workspace_root / "src/logic/agents/cognitive/memory_consolidation_agent.py"),
        )
        self.fleet.register_agent(
            "Transparency",
            TransparencyAgent,
            str(self.workspace_root / "src/observability/stats/transparency_agent.py"),
        )
        self.fleet.register_agent(
            "SpecAgent",
            SpecToolAgent,
            str(self.workspace_root / "src/logic/agents/development/spec_tool_agent.py"),
        )
        self.fleet.register_agent(
            "Kernel",
            KernelAgent,
            str(self.workspace_root / "src/logic/agents/system/kernel_agent.py"),
        )
        self.fleet.register_agent(
            "PR",
            PullRequestAgent,
            str(self.workspace_root / "src/logic/agents/development/pull_request_agent.py"),
        )
        self.fleet.register_agent(
            "Config",
            ConfigAgent,
            str(self.workspace_root / "src/logic/agents/system/config_agent.py"),
        )
        self.fleet.register_agent(
            "Test",
            TestAgent,
            str(self.workspace_root / "src/logic/agents/analysis/test_agent.py"),
        )
        self.fleet.register_agent(
            "Browser",
            BrowsingAgent,
            str(self.workspace_root / "src/logic/agents/intelligence/browsing_agent.py"),
        )
        self.fleet.register_agent(
            "MCP",
            MCPAgent,
            str(self.workspace_root / "src/logic/agents/system/mcp_agent.py"),
        )
        self.fleet.register_agent(
            "Evolution",
            ToolEvolutionAgent,
            str(self.workspace_root / "src/logic/agents/development/tool_evolution_agent.py"),
        )
        self.fleet.register_agent(
            "Visualizer",
            VisualizerAgent,
            str(self.workspace_root / "src/logic/agents/cognitive/visualizer_agent.py"),
        )

        metrics = self.fleet.telemetry.get_metrics()
        gantt_lines = [
            "gantt",
            "    title Fleet Performance Overview",
            "    dateFormat  HH:mm:ss",
            "    axisFormat %H:%M:%S",
        ]

        for m in metrics[-10:]:  # Last 10
            start_time = datetime.fromtimestamp(m.get("timestamp", time.time())).strftime("%H:%M:%S")
            duration_sec = m.get("duration", 0)
            gantt_lines.append(
                f"    {m.get('agent', 'unknown')} : {m.get('action', 'none')}, {start_time}, {duration_s
"""

from __future__ import annotations

import logging
import os
import time
from datetime import datetime
from typing import TYPE_CHECKING

from src.core.base.lifecycle.base_agent import BaseAgent

from .transparency_agent import TransparencyAgent

if TYPE_CHECKING:
    from src.infrastructure.swarm.fleet.fleet_manager import FleetManager


class ReportingAgent(BaseAgent):
    """
    Observer agent that generates executive dashboards and reports
    by orchestrating multiple specialist agents.
    """

    def __init__(self, fleet: FleetManager) -> None:
        super().__init__(agent_name="Reporting")
        self.fleet = fleet
        self.workspace_root = self._workspace_root

    async def generate_dashboard(self) -> str:
        """Runs a workflow to gather data and build a markdown dashboard."""
        logging.info("ReportingAgent: Initiating dashboard generation workflow...")

        # Load required agents if not present
        from src.logic.agents.analysis.test_agent import TestAgent
        from src.logic.agents.cognitive.memory_consolidation_agent import \
            MemoryConsolidationAgent
        from src.logic.agents.cognitive.visualizer_agent import VisualizerAgent
        from src.logic.agents.development.pull_request_agent import \
            PullRequestAgent
        from src.logic.agents.development.spec_tool_agent import SpecToolAgent
        from src.logic.agents.development.tool_evolution_agent import \
            ToolEvolutionAgent
        from src.logic.agents.intelligence.browsing_agent import BrowsingAgent
        from src.logic.agents.system.config_agent import ConfigAgent
        from src.logic.agents.system.kernel_agent import KernelAgent
        from src.logic.agents.system.mcp_agent import MCPAgent

        self.fleet.register_agent(
            "Consolidator",
            MemoryConsolidationAgent,
            str(self.workspace_root / "src/logic/agents/cognitive/memory_consolidation_agent.py"),
        )
        self.fleet.register_agent(
            "Transparency",
            TransparencyAgent,
            str(self.workspace_root / "src/observability/stats/transparency_agent.py"),
        )
        self.fleet.register_agent(
            "SpecAgent",
            SpecToolAgent,
            str(self.workspace_root / "src/logic/agents/development/spec_tool_agent.py"),
        )
        self.fleet.register_agent(
            "Kernel",
            KernelAgent,
            str(self.workspace_root / "src/logic/agents/system/kernel_agent.py"),
        )
        self.fleet.register_agent(
            "PR",
            PullRequestAgent,
            str(self.workspace_root / "src/logic/agents/development/pull_request_agent.py"),
        )
        self.fleet.register_agent(
            "Config",
            ConfigAgent,
            str(self.workspace_root / "src/logic/agents/system/config_agent.py"),
        )
        self.fleet.register_agent(
            "Test",
            TestAgent,
            str(self.workspace_root / "src/logic/agents/analysis/test_agent.py"),
        )
        self.fleet.register_agent(
            "Browser",
            BrowsingAgent,
            str(self.workspace_root / "src/logic/agents/intelligence/browsing_agent.py"),
        )
        self.fleet.register_agent(
            "MCP",
            MCPAgent,
            str(self.workspace_root / "src/logic/agents/system/mcp_agent.py"),
        )
        self.fleet.register_agent(
            "Evolution",
            ToolEvolutionAgent,
            str(self.workspace_root / "src/logic/agents/development/tool_evolution_agent.py"),
        )
        self.fleet.register_agent(
            "Visualizer",
            VisualizerAgent,
            str(self.workspace_root / "src/logic/agents/cognitive/visualizer_agent.py"),
        )

        metrics = self.fleet.telemetry.get_metrics()
        gantt_lines = [
            "gantt",
            "    title Fleet Performance Overview",
            "    dateFormat  HH:mm:ss",
            "    axisFormat %H:%M:%S",
        ]

        for m in metrics[-10:]:  # Last 10
            start_time = datetime.fromtimestamp(m.get("timestamp", time.time())).strftime("%H:%M:%S")
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

    async def improve_content(self, prompt: str, target_file: str | None = None) -> str:
        """Alias for dashboard generation or refinement."""
        return await self.generate_dashboard()


if __name__ == "__main__":
    # Local test
    import asyncio

    from src.infrastructure.swarm.fleet.fleet_manager import \
        FleetManager  # noqa: F811
    from src.observability.structured_logger import StructuredLogger

    logger = StructuredLogger(__name__)
    f = FleetManager(workspace_root=os.getcwd())
    agent = ReportingAgent(f)
    logger.info(asyncio.run(agent.generate_dashboard()))

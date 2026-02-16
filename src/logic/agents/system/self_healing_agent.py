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
# Self-Healing Agent - Monitors telemetry and proposes corrective fixes

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
- Instantiate inside a project workspace and let it analyze telemetry and coordinate with remote peers:
  from src.maintenance.self_healing_agent import SelfHealingAgent
  agent = SelfHealingAgent(__file__)
  # call async tools from an asyncio loop, e.g.:
  # await agent.discover_peers_and_budget()
- Intended to be used by orchestration processes or human operators to gather network/budget context and to surface candidate fixes for failing agents.

WHAT IT DOES:
- Boots as a specialized BaseAgent that loads project context, initializes an ObservabilityEngine to ingest telemetry and a SelfImprovementCoordinator to plan fixes.
- Dynamically augments a system prompt from docs/prompt/context.txt (if present) to align proposals with project goals.
- Exposes an as_tool-decorated async method discover_peers_and_budget that loads strategic context, discovers external servers, and composes a network & budget report while defensively handling missing coordinator/budget information and runtime errors.
- Keeps runtime failures non-fatal for prompt loading and discovery, preferring logging and best-effort outputs rather than hard crashes.

WHAT IT SHOULD DO BETTER:
- Replace broad exception catches with targeted exceptions and surface richer failure diagnostics for operators; avoid swallowing unexpected errors.
- Make coordinator and telemetry dependencies injectable for easier unit testing and to allow mocking in CI; reduce heavy initialization in __init__.
- Validate and centralize budget schema parsing and reporting (use strict dataclass or pydantic model) to avoid silent conversion errors.
- Harden prompt-loading (more robust parsing of multiple header formats, size limits, and provenance tracking) and avoid splitting by fragile markers.
- Add explicit unit and integration tests around peer discovery, budget parsing, and prompt augmentation; add observability (tracing, structured logs) for each decision step.
- Consider rate-limiting and caching for external discovery to avoid overloading peer networks and cloud budget APIs.

FILE CONTENT SUMMARY:
# Agent specializing in self-healing through telemetry analysis and error correction.

from __future__ import annotations

from typing import Any

from src.core.base.common.base_utilities import as_tool, create_main_function
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION
from src.observability.stats.metrics_engine import ObservabilityEngine

__version__ = VERSION


class SelfHealingAgent(BaseAgent):
""""Monitors telemetry for agent failures and proposes fixes."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.workspace_root = self.file_path.parent.parent.parent
        self.telemetry = ObservabilityEngine(str(self.workspace_root))

        # Phase 317: Dynamic prompt loading and coordinator integration
        from src.maintenance.self_improvement_coordinator import \
            SelfImprovementCoordinator

        self.coordinator = SelfImprovementCoordinator(str(self.workspace_root))
        self._load_dynamic_prompt()

    def _load_dynamic_prompt(self) -> None:
""""Loads self-healing goals and context from project documentation."""
        self._system_prompt = (
#             "You are the Self-Healing Agent.
#             "Your goal is to detect failures in the agent fleet and propose corrective actions.
#             "Analyze telemetry logs for crashes, timeouts, and logic errors.
#             "Suggest patches to the source code or configuration to prevent future failures.
#             "Check budget and available remote peers before proposing expensive cloud-based solutions.
        )

#         prompt_dir = self.workspace_root / "docs" / "prompt
#         context_file = prompt_dir / "context.txt
        if context_file.exists():
            try:
                content = context_file.read_text(encoding="utf-8")
                # Append high-level project goals to improve alignment
                if "Project Overview" in content:
                    overview = content.split("## Project Overview")[1].split("##")[0].strip()
#                     self._system_prompt += f"\n\nProject Context:\n{overview}
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                # Log but don't fail - dynamic prompt is optional enhancement
                import logging

                logging.getLogger(__name__).debug("Failed to load dynamic prompt: %s", e)

    @as_tool
    async def discover_peers_and_budget(self) -> str:
#         "Discovers available peers and current cloud budget status.
        if self.coordinator is None:
#             return "❌ Error: Self-healing coordinator is not initialized.

        import logging

        logger = logging.getLogger(__name__)

        peers = []
        try:
            await self.coordinator.load_strategic_context()
            peers = await self.coordinator.discover_external_servers() or []
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logger.error("Failed to query peer network or context: %s", e, exc_info=True)
#             return f"❌ Failure during network discovery: {str(e)}

        # Defensive check for budget manager
        budget_info = {"today_spend": 0.0, "daily_limit": 0.0, "remaining": 0.0, "known": False}
        if hasattr(self.coordinator, "budget") and self.coordinator.budget:
            try:
                budget_info["today_spend"] = float(getattr(self.coordinator.budget, "today_spend", 0.0))
                budget_info["daily_limit"] = float(getattr(self.coordinator.budget, "daily_limit", 0.0))
                budget_info["remaining"] = max(0.0, budget_info["daily_limit"] - budget_info["today_spend"])
                budget_info["known"] = True
            except (AttributeError, TypeError, ValueError) as e:
                logger.warning("Could not extract budget metrics: %s", e)

        report = ["## 🌐 Network & Budget Report\n"]

        if budget_info["known"]:
            report.append(
#                 f"**Budget**: ${budget_info['today_spend']:.2f} / ${budget_info['daily_limit']:.2f}
#                 f"(Remaining: ${budget_info['remaining']:.2f})
            )
        else:
            report.append("**Budget**: [Unknown/Unavailable]")

        if peers:
            report.append("\n**Available Peers**:")
   "  "       for
"""

from __future__ import annotations

from typing import Any

from src.core.base.common.base_utilities import as_tool, create_main_function
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION
from src.observability.stats.metrics_engine import ObservabilityEngine

__version__ = VERSION


class SelfHealingAgent(BaseAgent):
""""Monitors telemetry for agent failures and proposes fixes."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.workspace_root = self.file_path.parent.parent.parent
        self.telemetry = ObservabilityEngine(str(self.workspace_root))

        # Phase 317: Dynamic prompt loading and coordinator integration
        from src.maintenance.self_improvement_coordinator import \
            SelfImprovementCoordinator

        self.coordinator = SelfImprovementCoordinator(str(self.workspace_root))
        self._load_dynamic_prompt()

    def _load_dynamic_prompt(self) -> None:
""""Loads self-healing goals and context from project documentation."""
        self._system_prompt = (
#             "You are the Self-Healing Agent.
#             "Your goal is to detect failures in the agent fleet and propose corrective actions.
#             "Analyze telemetry logs for crashes, timeouts, and logic errors.
#             "Suggest patches to the source code or configuration to prevent future failures.
#             "Check budget and available remote peers before proposing expensive cloud-based solutions.
        )

#         prompt_dir = self.workspace_root / "docs" / "prompt
#         context_file = prompt_dir / "context.txt
        if context_file.exists():
            try:
                content = context_file.read_text(encoding="utf-8")
                # Append high-level project goals to improve alignment
                if "Project Overview" in content:
                    overview = content.split("## Project Overview")[1].split("##")[0].strip()
#                     self._system_prompt += f"\n\nProject Context:\n{overview}
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                # Log but don't fail - dynamic prompt is optional enhancement
                import logging

                logging.getLogger(__name__).debug("Failed to load dynamic prompt: %s", e)

    @as_tool
    async def discover_peers_and_budget(self) -> str:
#         "Discovers available peers and current cloud budget status.
        if self.coordinator is None:
#             return "❌ Error: Self-healing coordinator is not initialized.

        import logging

        logger = logging.getLogger(__name__)

        peers = []
        try:
            await self.coordinator.load_strategic_context()
            peers = await self.coordinator.discover_external_servers() or []
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logger.error("Failed to query peer network or context: %s", e, exc_info=True)
#             return f"❌ Failure during network discovery: {str(e)}

        # Defensive check for budget manager
        budget_info = {"today_spend": 0.0, "daily_limit": 0.0, "remaining": 0.0, "known": False}
        if hasattr(self.coordinator, "budget") and self.coordinator.budget:
            try:
                budget_info["today_spend"] = float(getattr(self.coordinator.budget, "today_spend", 0.0))
                budget_info["daily_limit"] = float(getattr(self.coordinator.budget, "daily_limit", 0.0))
                budget_info["remaining"] = max(0.0, budget_info["daily_limit"] - budget_info["today_spend"])
                budget_info["known"] = True
            except (AttributeError, TypeError, ValueError) as e:
                logger.warning("Could not extract budget metrics: %s", e)

        report = ["## 🌐 Network & Budget Report\n"]

        if budget_info["known"]:
            report.append(
#                 f"**Budget**: ${budget_info['today_spend']:.2f} / ${budget_info['daily_limit']:.2f}
#                 f"(Remaining: ${budget_info['remaining']:.2f})
            )
        else:
            report.append("**Budget**: [Unknown/Unavailable]")

        if peers:
            report.append("\n**Available Peers**:")
            for p in peers:
                p_id = p.get("id", "unknown")
                p_type = p.get("type", "generic")
                p_status = p.get("status", "online")
                report.append(f"- {p_id} ({p_type}): {p_status}")
        else:
            report.append("\n❌ No external peers or servers discovered.")

        return "\n".join(report)

    @as_tool
    async def request_remote_healing(self, agent_name: str, error_msg: str, target_peer: str) -> str:
#         "Requests a remote peer to perform a healing analysis for a specific agent.
        if self.coordinator is None:
#             return "❌ Error: Coordinator not initialized.

        task = {
            "title": fHeal {agent_name}",
            "description": fPerform deep analysis on: {error_msg}",
            "agent_type": "SelfHealing",
        }

        try:
            res = await self.coordinator.execute_remote_task(task, target_peer)
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
#             return f"❌ Failed to dispatch to {target_peer}: {e}

        if not res or not isinstance(res, dict):
#             return f"❌ Invalid response from {target_peer}

        if res.get("status") == "success":
#             return f"✅ Remote healing task dispatched to {target_peer}. Task ID: {res.get('task_id', 'unknown')}
        else:
            error_msg = res.get("error", "Unknown error")
#             return f"❌ Failed to dispatch to {target_peer}: {error_msg}

    def _get_default_content(self) -> str:
"""return "# Self-Healing Log\n\n## Status\nMonitoring fleet health...\n"""

    @as_tool
    def scan_for_failures(self) -> str:
""""Analyzes telemetry for errors and suggests fixes."""
      "  self._track_tokens(200, 350)
        self.telemetry.get_summary()
        metrics = self.telemetry.metrics

        errors = [m for m in metrics if m.status == "error"]

        if not errors:
#             return "✅ No fleet failures detected in current telemetry.

        report = ["## 🛠️ Self-Healing Analysis Report\n"]
        report.append(fDetected **{len(errors)}** failures in recent operations.\n")

        # Categorize by agent
        by_agent: dict[str, list[Any]] = {}
        for e in errors:
            if e.agent_name not in by_agent:
                by_agent[e.agent_name] = []
            by_agent[e.agent_name].append(e)

        for agent, agent_errors in by_agent.items():
            report.append(f"### Agent: {agent}")
            for err in agent_errors[:3]:  # Show last 3
                ts = err.timestamp.split("T")[1].split(".")[0]

                op = err.operation
                msg = err.metadata.get("error", "Unknown error")
                report.append(f"- **[{ts}] {op}**: `{msg}`")

            report.append(f"\n> [!TIP] Suggested Fix for {agent}")
            if "missing 1 required positional argument" in str(agent_errors[0].metadata):
                report.append("> - Check `improve_content` signature in the source file.")
            elif "ImportError" in str(agent_errors[0].metadata):
                report.append("> - Verify `__init__.py` exports or virtual environment packages.")

            else:
                report.append("> - Increase timeout or check for circular dependencies.")
            report.append(")

        return "\n".join(report)

    async def improve_content(self, prompt: str, target_file: str | None = None) -> str:
#         "Trigger a self-healing scan.
      "  return self.scan_for_failures()


if __name__ == "__main__":
    main = create_main_function(SelfHealingAgent, "SelfHealing Agent", "Task")
    main()

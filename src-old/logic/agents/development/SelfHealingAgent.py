#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/logic/agents/development/SelfHealingAgent.description.md

# SelfHealingAgent

**File**: `src\logic\agents\development\SelfHealingAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 199  
**Complexity**: 5 (moderate)

## Overview

Agent specializing in self-healing through telemetry analysis and error correction.

## Classes (1)

### `SelfHealingAgent`

**Inherits from**: BaseAgent

Monitors telemetry for agent failures and proposes fixes.

**Methods** (5):
- `__init__(self, file_path)`
- `_load_dynamic_prompt(self)`
- `_get_default_content(self)`
- `scan_for_failures(self)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `logging`
- `os`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.BaseUtilities.as_tool`
- `src.core.base.BaseUtilities.create_main_function`
- `src.core.base.Version.VERSION`
- `src.maintenance.SelfImprovementCoordinator.SelfImprovementCoordinator`
- `src.observability.stats.MetricsEngine.ObservabilityEngine`
- `typing.Any`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/development/SelfHealingAgent.improvements.md

# Improvements for SelfHealingAgent

**File**: `src\logic\agents\development\SelfHealingAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 199 lines (medium)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `SelfHealingAgent_test.py` with pytest tests

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


"""Agent specializing in self-healing through telemetry analysis and error correction."""

from src.core.base.Version import VERSION
import os
from typing import Any
from src.core.base.BaseAgent import BaseAgent
from src.core.base.BaseUtilities import create_main_function, as_tool
from src.observability.stats.MetricsEngine import ObservabilityEngine

__version__ = VERSION


class SelfHealingAgent(BaseAgent):
    """Monitors telemetry for agent failures and proposes fixes."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.workspace_root = self.file_path.parent.parent.parent
        self.telemetry = ObservabilityEngine(str(self.workspace_root))

        # Phase 317: Dynamic prompt loading and coordinator integration
        from src.maintenance.SelfImprovementCoordinator import (
            SelfImprovementCoordinator,
        )

        self.coordinator = SelfImprovementCoordinator(str(self.workspace_root))
        self._load_dynamic_prompt()

    def _load_dynamic_prompt(self) -> None:
        """Loads self-healing goals and context from project documentation."""
        self._system_prompt = (
            "You are the Self-Healing Agent. "
            "Your goal is to detect failures in the agent fleet and propose corrective actions. "
            "Analyze telemetry logs for crashes, timeouts, and logic errors. "
            "Suggest patches to the source code or configuration to prevent future failures. "
            "Check budget and available remote peers before proposing expensive cloud-based solutions."
        )

        prompt_dir = self.workspace_root / "docs" / "prompt"
        context_file = prompt_dir / "context.txt"
        if context_file.exists():
            try:
                content = context_file.read_text(encoding="utf-8")
                # Append high-level project goals to improve alignment
                if "Project Overview" in content:
                    overview = (
                        content.split("## Project Overview")[1].split("##")[0].strip()
                    )
                    self._system_prompt += f"\n\nProject Context:\n{overview}"
            except Exception as e:
                # Log but don't fail - dynamic prompt is optional enhancement
                import logging

                logging.getLogger(__name__).debug(
                    "Failed to load dynamic prompt: %s", e
                )

    @as_tool
    async def discover_peers_and_budget(self) -> str:
        """Discovers available peers and current cloud budget status."""
        if self.coordinator is None:
            return "❌ Error: Self-healing coordinator is not initialized."

        import logging

        logger = logging.getLogger(__name__)

        peers = []
        try:
            await self.coordinator.load_strategic_context()
            peers = await self.coordinator.discover_external_servers() or []
        except Exception as e:
            logger.error(
                "Failed to query peer network or context: %s", e, exc_info=True
            )
            return f"❌ Failure during network discovery: {str(e)}"

        # Defensive check for budget manager
        budget_info = {
            "today_spend": 0.0,
            "daily_limit": 0.0,
            "remaining": 0.0,
            "known": False,
        }
        if hasattr(self.coordinator, "budget") and self.coordinator.budget:
            try:
                budget_info["today_spend"] = float(
                    getattr(self.coordinator.budget, "today_spend", 0.0)
                )
                budget_info["daily_limit"] = float(
                    getattr(self.coordinator.budget, "daily_limit", 0.0)
                )
                budget_info["remaining"] = max(
                    0.0, budget_info["daily_limit"] - budget_info["today_spend"]
                )
                budget_info["known"] = True
            except (AttributeError, TypeError, ValueError) as e:
                logger.warning("Could not extract budget metrics: %s", e)

        report = ["## 🌐 Network & Budget Report\n"]

        if budget_info["known"]:
            report.append(
                f"**Budget**: ${budget_info['today_spend']:.2f} / ${budget_info['daily_limit']:.2f} (Remaining: ${budget_info['remaining']:.2f})"
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
    async def request_remote_healing(
        self, agent_name: str, error_msg: str, target_peer: str
    ) -> str:
        """Requests a remote peer to perform a healing analysis for a specific agent."""
        if self.coordinator is None:
            return "❌ Error: Coordinator not initialized."

        task = {
            "title": f"Heal {agent_name}",
            "description": f"Perform deep analysis on: {error_msg}",
            "agent_type": "SelfHealing",
        }

        try:
            res = await self.coordinator.execute_remote_task(task, target_peer)
        except Exception as e:
            return f"❌ Failed to dispatch to {target_peer}: {e}"

        if not res or not isinstance(res, dict):
            return f"❌ Invalid response from {target_peer}"

        if res.get("status") == "success":
            return f"✅ Remote healing task dispatched to {target_peer}. Task ID: {res.get('task_id', 'unknown')}"
        else:
            error_msg = res.get("error", "Unknown error")
            return f"❌ Failed to dispatch to {target_peer}: {error_msg}"

    def _get_default_content(self) -> str:
        return "# Self-Healing Log\n\n## Status\nMonitoring fleet health...\n"

    @as_tool
    def scan_for_failures(self) -> str:
        """Analyzes telemetry for errors and suggests fixes."""
        self._track_tokens(200, 350)
        self.telemetry.get_summary()
        metrics = self.telemetry.metrics

        errors = [m for m in metrics if m.status == "error"]

        if not errors:
            return "✅ No fleet failures detected in current telemetry."

        report = ["## 🛠️ Self-Healing Analysis Report\n"]
        report.append(f"Detected **{len(errors)}** failures in recent operations.\n")

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
            if "missing 1 required positional argument" in str(
                agent_errors[0].metadata
            ):
                report.append(
                    "> - Check `improve_content` signature in the source file."
                )
            elif "ImportError" in str(agent_errors[0].metadata):
                report.append(
                    "> - Verify `__init__.py` exports or virtual environment packages."
                )

            else:
                report.append(
                    "> - Increase timeout or check for circular dependencies."
                )
            report.append("")

        return "\n".join(report)

    def improve_content(self, prompt: str) -> str:
        """Trigger a self-healing scan."""
        return self.scan_for_failures()


if __name__ == "__main__":
    main = create_main_function(SelfHealingAgent, "SelfHealing Agent", "Task")
    main()

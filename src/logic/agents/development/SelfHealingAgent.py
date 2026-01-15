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

"""Agent specializing in self-healing through telemetry analysis and error correction."""

from __future__ import annotations
from src.core.base.version import VERSION
from typing import Any
from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import create_main_function, as_tool
from src.observability.stats.metrics_engine import ObservabilityEngine

__version__ = VERSION




class SelfHealingAgent(BaseAgent):
    """Monitors telemetry for agent failures and proposes fixes."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.workspace_root = self.file_path.parent.parent.parent
        self.telemetry = ObservabilityEngine(str(self.workspace_root))
        self._system_prompt = (
            "You are the Self-Healing Agent. "
            "Your goal is to detect failures in the agent fleet and propose corrective actions. "
            "Analyze telemetry logs for crashes, timeouts, and logic errors. "
            "Suggest patches to the source code or configuration to prevent future failures."
        )

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
                ts = err.timestamp.split('T')[1].split('.')[0]










                op = err.operation
                msg = err.metadata.get('error', 'Unknown error')
                report.append(f"- **[{ts}] {op}**: `{msg}`")




            report.append(f"\n> [!TIP] Suggested Fix for {agent}")
            if "missing 1 required positional argument" in str(agent_errors[0].metadata):
                report.append("> - Check `improve_content` signature in the source file.")
            elif "ImportError" in str(agent_errors[0].metadata):
                report.append("> - Verify `__init__.py` exports or virtual environment packages.")


            else:
                report.append("> - Increase timeout or check for circular dependencies.")
            report.append("")

        return "\n".join(report)





    def improve_content(self, prompt: str) -> str:
        """Trigger a self-healing scan."""
        return self.scan_for_failures()





if __name__ == "__main__":
    main = create_main_function(SelfHealingAgent, "SelfHealing Agent", "Task")
    main()

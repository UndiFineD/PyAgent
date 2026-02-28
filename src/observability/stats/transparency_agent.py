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


"""Agent specializing in interpretability and deep tracing of agent reasoning steps."""

from __future__ import annotations

from src.core.base.common.base_utilities import as_tool, create_main_function
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION
from src.infrastructure.swarm.orchestration.signals.signal_registry import \
    SignalRegistry

__version__ = VERSION


class TransparencyAgent(BaseAgent):
    """Provides a detailed audit trail of agent thoughts, signals, and dependencies."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.signals = SignalRegistry()
        self.workspace_root = self.file_path.parent.parent.parent
        self._system_prompt = (
            "You are the Transparency Agent. "
            "Your goal is to make the internal 'thinking' and communication of the agent fleet visible. "
            "Explain WHY decisions were made by linking signals, reasoning blueprints, and telemetry data."
        )

    @as_tool
    def generate_audit_trail(self, workflow_id: str | None = None) -> str:
        """Generates a detailed markdown report of recent agent interactions."""
        history = self.signals.get_history(limit=100)

        if workflow_id:
            # Filter by workflow_id if it's in the data
            history = [
                e for e in history if e.get("data", {}).get("workflow_id") == workflow_id or workflow_id in str(e)
            ]

        report = ["# fleet Transparency Audit Trail"]
        if workflow_id:
            report.append(f"## Focus: Workflow {workflow_id}")

        report.append("\n### ≡ƒôí Signal Event Log")
        for event in history:
            ts = event["timestamp"].split("T")[1][:8]
            sender = event["sender"]
            signal = event["signal"]
            report.append(f"- **[{ts}]** `{sender}` emitted `{signal}`")

        report.append("\n### ≡ƒºá Reasoning Correlation")
        # In a real scenario, we'd fetch the reasoning blueprint from the WorkflowState or a log
        # For now, we point to the most recent 'STEP_STARTED' events
        steps = [h for h in history if h["signal"] == "STEP_STARTED"]

        for step in steps:
            data = step["data"]
            report.append(
                f"- Agent `{data['agent']}` executed `{data['action']}` "
                "triggered by the previous objective."
            )

        return "\n".join(report)

    async def improve_content(self, prompt: str, target_file: str | None = None) -> str:
        """Trigger an audit report."""
        return self.generate_audit_trail()


if __name__ == "__main__":
    main = create_main_function(TransparencyAgent, "Transparency Agent", "Workflow ID (optional)")
    main()

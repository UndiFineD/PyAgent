#!/usr/bin/env python3

"""Agent specializing in interpretability and deep tracing of agent reasoning steps."""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from src.classes.base_agent import BaseAgent
from src.classes.orchestration.SignalRegistry import SignalRegistry
from src.classes.base_agent.utilities import create_main_function, as_tool

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
    def generate_audit_trail(self, workflow_id: Optional[str] = None) -> str:
        """Generates a detailed markdown report of recent agent interactions."""
        history = self.signals.get_history(limit=100)
        
        if workflow_id:
            # Filter by workflow_id if it's in the data
            history = [e for e in history if e.get("data", {}).get("workflow_id") == workflow_id or workflow_id in str(e)]

        report = [f"# fleet Transparency Audit Trail"]
        if workflow_id:
            report.append(f"## Focus: Workflow {workflow_id}")
            
        report.append("\n### 📡 Signal Event Log")
        for event in history:
            ts = event["timestamp"].split('T')[1][:8]
            sender = event["sender"]
            signal = event["signal"]
            report.append(f"- **[{ts}]** `{sender}` emitted `{signal}`")
            
        report.append("\n### 🧠 Reasoning Correlation")
        # In a real scenario, we'd fetch the reasoning blueprint from the WorkflowState or a log
        # For now, we point to the most recent 'STEP_STARTED' events
        steps = [h for h in history if h["signal"] == "STEP_STARTED"]
        for step in steps:
            data = step["data"]
            report.append(f"- Agent `{data['agent']}` executed `{data['action']}` triggered by the previous objective.")

        return "\n".join(report)

    def improve_content(self, prompt: str) -> str:
        """Trigger an audit report."""
        return self.generate_audit_trail()

if __name__ == "__main__":
    main = create_main_function(TransparencyAgent, "Transparency Agent", "Workflow ID (optional)")
    main()

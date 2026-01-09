#!/usr/bin/env python3

"""Agent specializing in self-healing through telemetry analysis and error correction."""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from src.classes.base_agent import BaseAgent
from src.classes.base_agent.utilities import create_main_function, as_tool
from src.classes.stats.ObservabilityEngine import ObservabilityEngine

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
        summary = self.telemetry.get_summary()
        metrics = self.telemetry.metrics
        
        errors = [m for m in metrics if m.status == "error"]
        
        if not errors:
            return "✅ No fleet failures detected in current telemetry."
            
        report = ["## 🛠️ Self-Healing Analysis Report\n"]
        report.append(f"Detected **{len(errors)}** failures in recent operations.\n")
        
        # Categorize by agent
        by_agent: Dict[str, List[Any]] = {}
        for e in errors:
            if e.agent_name not in by_agent:
                by_agent[e.agent_name] = []
            by_agent[e.agent_name].append(e)
            
        for agent, agent_errors in by_agent.items():
            report.append(f"### Agent: {agent}")
            for err in agent_errors[:3]: # Show last 3
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


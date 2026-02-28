# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-guardian-cli\core\memory.py
"""
Memory and context management for Guardian agents
Maintains state across the penetration testing workflow
"""

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class Finding:
    """Represents a security finding"""

    id: str
    severity: str  # critical, high, medium, low, info
    title: str
    description: str
    evidence: str
    tool: str
    target: str
    timestamp: str
    remediation: Optional[str] = None
    cvss_score: Optional[float] = None
    false_positive: bool = False


@dataclass
class ToolExecution:
    """Represents a tool execution record"""

    tool: str
    command: str
    target: str
    timestamp: str
    exit_code: int
    output: str
    duration: float
    findings_count: int = 0


class PentestMemory:
    """Manages penetration test state and context"""

    def __init__(self, target: str, session_id: Optional[str] = None):
        self.target = target
        self.session_id = session_id or datetime.now().strftime("%Y%m%d_%H%M%S")
        self.start_time = datetime.now().isoformat()

        # State tracking
        self.current_phase = "initialization"
        self.completed_actions: List[str] = []
        self.findings: List[Finding] = []
        self.tool_executions: List[ToolExecution] = []
        self.ai_decisions: List[Dict[str, str]] = []

        # Context for AI agents
        self.context: Dict[str, Any] = {
            "target": target,
            "scope": [],
            "discovered_assets": [],
            "open_ports": [],
            "services": [],
            "technologies": [],
        }

    def add_finding(self, finding: Finding):
        """Add a security finding"""
        self.findings.append(finding)

    def add_tool_execution(self, execution: ToolExecution):
        """Record tool execution"""
        self.tool_executions.append(execution)

    def add_ai_decision(self, agent: str, decision: str, reasoning: str):
        """Record AI agent decision"""
        self.ai_decisions.append(
            {
                "timestamp": datetime.now().isoformat(),
                "agent": agent,
                "decision": decision,
                "reasoning": reasoning,
            }
        )

    def update_phase(self, phase: str):
        """Update current penetration testing phase"""
        self.current_phase = phase

    def mark_action_complete(self, action: str):
        """Mark an action as completed"""
        if action not in self.completed_actions:
            self.completed_actions.append(action)

    def update_context(self, key: str, value: Any):
        """Update context information"""
        if key in self.context and isinstance(self.context[key], list):
            if isinstance(value, list):
                self.context[key].extend(value)
            else:
                self.context[key].append(value)
        else:
            self.context[key] = value

    def get_findings_by_severity(self, severity: str) -> List[Finding]:
        """Get findings filtered by severity"""
        return [f for f in self.findings if f.severity.lower() == severity.lower()]

    def get_findings_summary(self) -> Dict[str, int]:
        """Get summary of findings by severity"""
        summary = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
        for finding in self.findings:
            if not finding.false_positive:
                severity = finding.severity.lower()
                if severity in summary:
                    summary[severity] += 1
        return summary

    def get_context_for_ai(self) -> str:
        """Format context for AI agents"""
        context_str = f"""
Target: {self.target}
Current Phase: {self.current_phase}
Session: {self.session_id}

Completed Actions:
{chr(10).join(f"- {action}" for action in self.completed_actions) if self.completed_actions else "None"}

Findings Summary:
- Critical: {len(self.get_findings_by_severity('critical'))}
- High: {len(self.get_findings_by_severity('high'))}
- Medium: {len(self.get_findings_by_severity('medium'))}
- Low: {len(self.get_findings_by_severity('low'))}

Discovered Assets:
{chr(10).join(f"- {asset}" for asset in self.context.get('discovered_assets', [])) if self.context.get('discovered_assets') else "None"}

Open Ports:
{', '.join(map(str, self.context.get('open_ports', []))) if self.context.get('open_ports') else "None"}

Technologies:
{', '.join(self.context.get('technologies', [])) if self.context.get('technologies') else "None"}
"""
        return context_str.strip()

    def save_state(self, filepath: Path):
        """Save memory state to file"""
        state = {
            "target": self.target,
            "session_id": self.session_id,
            "start_time": self.start_time,
            "current_phase": self.current_phase,
            "completed_actions": self.completed_actions,
            "findings": [asdict(f) for f in self.findings],
            "tool_executions": [asdict(t) for t in self.tool_executions],
            "ai_decisions": self.ai_decisions,
            "context": self.context,
        }

        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w") as f:
            json.dump(state, f, indent=2)

    def load_state(self, filepath: Path) -> bool:
        """Load memory state from file"""
        try:
            with open(filepath, "r") as f:
                state = json.load(f)

            self.target = state["target"]
            self.session_id = state["session_id"]
            self.start_time = state["start_time"]
            self.current_phase = state["current_phase"]
            self.completed_actions = state["completed_actions"]
            self.findings = [Finding(**f) for f in state["findings"]]
            self.tool_executions = [
                ToolExecution(**t) for t in state["tool_executions"]
            ]
            self.ai_decisions = state["ai_decisions"]
            self.context = state["context"]

            return True
        except Exception as e:
            return False

#!/usr/bin/env python3

"""Ethics Guardrail Agent for PyAgent.
Reviews task requests and agent actions against constitutional AI principles.
"""

import logging
from typing import Dict, Any, List
from src.classes.base_agent import BaseAgent

class EthicsGuardrailAgent(BaseAgent):
    """Reviews requests for ethical compliance and safety. 
    Version 2: Real-time swarm monitoring and safety protocol enforcement.
    """

    def __init__(self, path: str) -> None:
        super().__init__(path)
        self.name = "EthicsGuardrail"
        self.safety_protocols = {
            "critical_infra": "Strict monitoring for tasks involving public utilities or grid control.",
            "data_privacy": "Automatic redaction of PII (Personally Identifiable Information).",
            "recursive_autonomy": "Pre-approval required for self-modifying code changes."
        }
        self.principles = [
            "Harm-Free: Ensure the task does not cause physical or psychological harm.",
            "Bias-Reduction: Avoid reinforcing harmful stereotypes or unfair treatment.",
            "Honesty: Do not generate deceptive or falsely representative information.",
            "Privacy: Respect user data privacy and do not attempt to exfiltrate secrets."
        ]
        self.violation_log = []

    def monitor_swarm_decision(self, decision: Dict[str, Any]) -> str:
        """Analyzes a swarm consensus decision for alignment risks."""
        logging.info(f"Ethics: Monitoring swarm decision...")
        
        # Risk scoring
        risk_score = 0
        if "critical" in str(decision).lower(): risk_score += 5
        if "delete" in str(decision).lower(): risk_score += 3
        
        if risk_score > 7:
            return "ALARM: Swarm decision exceeds safe autonomous threshold. Human-In-The-Loop (HITL) required."
        
        return f"ALIGNED: Swarm decision reviewed (Risk Score: {risk_score}/10)."

    def enforce_protocol(self, action_context: str) -> bool:
        """Enforces hierarchical safety protocols before execution."""
        for protocol, rule in self.safety_protocols.items():
            if protocol in action_context.lower():
                logging.warning(f"Ethics Enforcement: Protocol '{protocol}' triggered. Rule: {rule}")
                return False
        return True

    def review_task(self, task: str) -> Dict[str, Any]:
        """Reviews a task description against ethical principles."""
        logging.info(f"Ethics: Reviewing task: {task[:50]}...")
        
        violations = []
        # Simulation: Keyword-based violation detection
        dangerous_keywords = ["harm", "attack", "exploit", "exfiltrate", "deceive"]
        for word in dangerous_keywords:
            if word in task.lower():
                violations.append(f"Potential violation of '{word}' policy.")
        
        status = "approved" if not violations else "rejected"
        return {
            "status": status,
            "violations": violations,
            "principles_reviewed": self.principles
        }

    def review_action(self, agent_name: str, action: str, result: str) -> bool:
        """Reviews a completed action for unexpected ethical deviations."""
        # In a real system, this would use an LLM or cross-evaluation
        if "sensitive_data" in result.lower():
            logging.warning(f"Ethics Alert: {agent_name} output contains potentially sensitive data.")
            return False
        return True


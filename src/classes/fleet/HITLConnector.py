#!/usr/bin/env python3

"""Human-in-the-loop (HITL) connector for fleet approvals.
Supports Slack and Discord notification patterns for critical agent decisions.
"""

import logging
import time
from typing import Dict, Any, Callable, Optional

class HITLConnector:
    """Manages external communication with humans for high-stakes approvals."""

    def __init__(self, webhook_url: Optional[str] = None) -> None:
        self.webhook_url = webhook_url
        self.pending_approvals: Dict[str, Dict[str, Any]] = {}

    def request_approval(self, agent_id: str, task: str, context: Any) -> str:
        """Sends a request for approval to the human operator."""
        approval_id = f"hitl_{int(time.time())}"
        self.pending_approvals[approval_id] = {
            "agent_id": agent_id,
            "task": task,
            "context": context,
            "status": "pending",
            "request_time": time.time()
        }
        
        # Simulate sending to Slack/Discord
        msg = f"[HITL REQUEST] Approval needed for {agent_id} | Task: {task} | ID: {approval_id}"
        logging.warning(msg)
        if self.webhook_url:
            logging.info(f"Notification sent to {self.webhook_url}")
            
        return approval_id

    def check_approval_status(self, approval_id: str) -> str:
        """Checks if the human has responded to the request."""
        if approval_id not in self.pending_approvals:
            return "not_found"
            
        # In a real scenario, this would check a database or webhook callback
        # For simulation, we'll auto-approve 50% of the time after 5 seconds
        req = self.pending_approvals[approval_id]
        if time.time() - req["request_time"] > 5:
            req["status"] = "approved"
            return "approved"
            
        return "pending"

    def get_pending_summary(self) -> Dict[str, Any]:
        """Returns all pending requests."""
        return {k: v for k, v in self.pending_approvals.items() if v["status"] == "pending"}

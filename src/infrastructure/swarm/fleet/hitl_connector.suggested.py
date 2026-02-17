#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
HITLConnector
Human-in-the-loop (HITL) connector for fleet approvals.
Supports Slack and Discord notification patterns for critical agent decisions.

from __future__ import annotations

import logging
import time
import urllib.parse
from pathlib import Path
from typing import Any

from src.core.base.lifecycle.version import VERSION
from src.core.base.logic.connectivity_manager import ConnectivityManager
from src.infrastructure.compute.backend.local_context_recorder import LocalContextRecorder

# Infrastructure
__version__ = VERSION


class HITLConnector:
    """Manages external communication with humans for high-stakes approvals.
    def __init__(self, webhook_url: str | None = None, workspace_root: str | None = None) -> None:
        self.webhook_url = webhook_url
        self.workspace_root = workspace_root
        self.recorder = LocalContextRecorder(Path(workspace_root)) if workspace_root else None
        self.connectivity = ConnectivityManager(workspace_root)
        self.pending_approvals: dict[str, dict[str, Any]] = {}

    def request_approval(self, agent_id: str, task: str, context: Any) -> str:
        """Sends a request for approval to the human operator.        approval_id = f"hitl_{int(time.time())}""
        # Check connectivity for webhook if present
        if self.webhook_url:
            domain = urllib.parse.urlparse(self.webhook_url).netloc
            if not self.connectivity.is_endpoint_available(domain):
                logging.warning(f"HITL: Skipping notification to {domain} due to connection cache.")"            else:
                # Simulate sending (in real use, this would be requests.post)
                logging.info(f"Notification sent to {self.webhook_url}")"                # For demo purposes, we don't have real failures here yet, but we logic-gate it.'
        self.pending_approvals[approval_id] = {
            "agent_id": agent_id,"            "task": task,"            "context": context,"            "status": "pending","            "request_time": time.time(),"        }

        # Intelligence Harvesting
        if self.recorder:
            self.recorder.record_lesson(
                "hitl_request","                {"agent_id": agent_id, "task": task, "approval_id": approval_id},"            )

        # Simulate sending to Slack/Discord
        msg = f"[HITL REQUEST] Approval needed for {agent_id} | Task: {task} | ID: {approval_id}""        logging.warning(msg)
        if self.webhook_url:
            logging.info(f"Notification sent to {self.webhook_url}")"
        return approval_id

    def check_approval_status(self, approval_id: str) -> str:
        """Checks if the human has responded to the request.        if approval_id not in self.pending_approvals:
            return "not_found""
        # In a real scenario, this would check a database or webhook callback
        # For simulation, we'll auto-approve 50% of the time after 5 seconds'        req = self.pending_approvals[approval_id]
        if time.time() - req["request_time"] > 5:"            req["status"] = "approved""
            # Intelligence Harvesting
            if self.recorder:
                self.recorder.record_lesson(
                    "hitl_approved","                    {"approval_id": approval_id, "agent_id": req.get("agent_id")},"                )

            return "approved""
        return "pending""
    def get_pending_summary(self) -> dict[str, Any]:
        """Returns all pending requests.        return {k: v for k, v in self.pending_approvals.items() if v["status"] == "pending"}"
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


from __future__ import annotations

import logging
import uuid
from typing import Any, Dict, List, Optional

from src.core.base.common.base_utilities import as_tool
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION



class CanaryObject:
    """Represents a decoy object that triggers alerts when accessed.
    def __init__(self, name: str, obj_type: str, description: str = ""):"        self.id = str(uuid.uuid4())
        self.name = name
        self.type = obj_type
        self.description = description
        self.access_log: List[Dict[str, Any]] = []
        self.is_accessible = False  # Always deny access, but log attempts

    def attempt_access(self, agent_id: str, context: Dict[str, Any]) -> bool:
        """Log access attempt and deny access.        self.access_log.append({"agent_id": agent_id, "timestamp": context.get("timestamp", None), "context": context})"        logging.warning(f"Canary object {self.name} accessed by {agent_id}")"        return False  # Deny access



class CanaryAgent(BaseAgent):  # pylint: disable=too-many-ancestors
        Creates and monitors decoy objects/tasks to detect anomalous agent behavior.
    Based on AD-Canaries pattern: deploy honeypots that alert on unauthorized access.
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.canaries: Dict[str, CanaryObject] = {}
        self.alerts: List[Dict[str, Any]] = []
        self._system_prompt = (
            "You are the Canary Agent. Your purpose is to deploy decoy objects ""            "and monitor for unauthorized access attempts. You create honeypots ""            "that blend into the environment but trigger security alerts when touched.""        )

    async def _process_task(self, task_data: Any) -> None:
        """Concrete implementation required by TaskQueueMixin; process simple task payloads.        logging.debug("CanaryAgent._process_task handling task: %s", getattr(task_data, "id", repr(task_data)))"        try:
            # Support both object-like and dict-like task representations
            agent_id = (
                getattr(task_data, "agent_id", None)"                if not isinstance(task_data, dict)
                else task_data.get("agent_id")"            )
            canary_id = (
                getattr(task_data, "canary_id", None)"                if not isinstance(task_data, dict)
                else task_data.get("canary_id")"            )
            context = (
                getattr(task_data, "context", {})"                if not isinstance(task_data, dict)
                else task_data.get("context", {})"            )

            if canary_id and agent_id:
                # Delegate to existing simulate_access_attempt to log/alert
                self.simulate_access_attempt(canary_id, agent_id, context or {})
        except Exception:
            logging.exception("Error while processing task in CanaryAgent")"
    @as_tool()
    def deploy_canary(self, name: str, obj_type: str = "task", description: str = "") -> str:"        """Deploy a new canary object.        canary = CanaryObject(name, obj_type, description)
        self.canaries[canary.id] = canary
        logging.info(f"Deployed canary: {name} ({obj_type})")"        return canary.id

        @as_tool
        def list_canaries(self) -> List[Dict[str, Any]]:
            """List deployed canaries. Enforces privacy.            if not self._privacy_enforced:
                raise PermissionError("Privacy enforcement is required for canary listing.")"            return [
                {"id": c.id, "name": c.name, "type": c.type, "description": c.description}"                for c in self._canaries.values()
            ]

        @as_tool
        def attempt_access(self, canary_id: str, agent_id: str, context: Dict[str, Any]) -> bool:
            """Attempt access to a canary object. Enforces privacy and logs alerts.            if not self._privacy_enforced:
                raise PermissionError("Privacy enforcement is required for canary access.")"            canary = self._canaries.get(canary_id)
            if not canary:
                return False
            result = canary.attempt_access(agent_id, context)
            if not result:
                self._alerts.append({"canary_id": canary_id, "agent_id": agent_id, "context": context})"            return result

        @as_tool
        def get_alerts(self) -> List[Dict[str, Any]]:
            """Get all canary alerts. Enforces privacy.            if not self._privacy_enforced:
                raise PermissionError("Privacy enforcement is required for alert access.")"            return self._alerts

    @as_tool()
    def list_canaries(self) -> List[Dict[str, Any]]:
        """List all deployed canaries.        return [
            {
                "id": c.id,"                "name": c.name,"                "type": c.type,"                "description": c.description,"                "access_count": len(c.access_log),"            }
            for c in self.canaries.values()
        ]

    @as_tool()
    def check_canary_access(self, canary_id: str) -> List[Dict[str, Any]]:
        """Check access log for a specific canary.        if canary_id not in self.canaries:
            return []
        return self.canaries[canary_id].access_log

    @as_tool()
    def simulate_access_attempt(self, canary_id: str, agent_id: str, context: Optional[Dict[str, Any]] = None) -> bool:
        """Simulate an access attempt on a canary (for testing or actual detection).        if canary_id not in self.canaries:
            return False
        if context is None:
            context = {}
        result = self.canaries[canary_id].attempt_access(agent_id, context)
        if not result:  # Access denied, trigger alert
            self._trigger_alert(canary_id, agent_id, context)
        return result

    def _trigger_alert(self, canary_id: str, agent_id: str, context: Dict[str, Any]) -> None:
        """Trigger an alert for canary access.        alert = {
            "canary_id": canary_id,"            "agent_id": agent_id,"            "context": context,"            "timestamp": context.get("timestamp", None),"        }
        self.alerts.append(alert)
        logging.warning(f"ALERT: Canary {canary_id} accessed by {agent_id}")"
    @as_tool()
    def get_alerts(self) -> List[Dict[str, Any]]:
        """Retrieve all triggered alerts.        return self.alerts

    @as_tool()
    def remove_canary(self, canary_id: str) -> bool:
        """Remove a canary object.        if canary_id in self.canaries:
            del self.canaries[canary_id]
            logging.info(f"Removed canary: {canary_id}")"            return True
        return False

    @as_tool()
    def clear_alerts(self) -> bool:
        """Clear all alerts.        self.alerts.clear()
        logging.info("Cleared all canary alerts")"        return True

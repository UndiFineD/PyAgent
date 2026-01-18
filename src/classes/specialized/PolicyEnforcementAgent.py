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


from __future__ import annotations
from src.core.base.version import VERSION
import time
from typing import Dict, List, Any, Set

__version__ = VERSION

class PolicyEnforcementAgent:
    """
    Monitors agent activity against a set of governance-defined policies
    and enforces restrictions (quarantining) if violations occur.
    """
    def __init__(self, workspace_path: str) -> None:
        self.workspace_path = workspace_path
        self.active_policies: dict[str, Any] = {
            "no_external_data_leak": True,
            "max_token_spend_per_hour": 100000,
            "required_security_scan": True
        }
        self.violation_log: list[dict[str, Any]] = []
        self.quarantine_list: set[str] = set()
        
    def evaluate_action(self, agent_id: str, action_type: str, metadata: Any) -> dict[str, Any]:
        """
        Evaluates if an agent action complies with active policies.
        """
        violations = []
        
        if action_type == "external_push" and self.active_policies["no_external_data_leak"]:
            if "credentials" in str(metadata).lower():
                violations.append("DATA_LEAK_PREVENTION")
                
        if len(violations) > 0:
            self.violation_log.append({
                "agent_id": agent_id,
                "violations": violations,
                "timestamp": time.time()
            })
            return {"status": "violation", "details": violations}
            
        return {"status": "authorized"}

    def quarantine_agent(self, agent_id: str, reason: str) -> dict[str, Any]:
        """
        Isolates an agent from the fleet.
        """
        self.quarantine_list.add(agent_id)
        return {"agent_id": agent_id, "status": "quarantined", "reason": reason}

    def is_agent_quarantined(self, agent_id: str) -> bool:
        return agent_id in self.quarantine_list
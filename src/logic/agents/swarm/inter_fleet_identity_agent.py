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

"""
Inter fleet identity agent.py module.
"""


from __future__ import annotations

import hashlib
import time
import uuid
from typing import Any

from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION
from src.core.base.logic.core.identity_core import IdentityCore

__version__ = VERSION


class InterFleetIdentityAgent(BaseAgent):  # pylint: disable=too-many-ancestors
    """
    Tier 3 (Orchestration) - Inter-Fleet Identity Agent: Manages federated
    identities for agents across multiple fleets using cryptographic signing and DID.
    """

    def __init__(self, workspace_path: str) -> None:
        super().__init__(workspace_path)
        self.workspace_path = workspace_path
        self.core = IdentityCore()
        self.fleet_id = str(uuid.uuid4())
        self.known_fleets: dict[Any, Any] = {}  # fleet_id -> {pub_key, metadata}
        self.authorized_agents: dict[Any, Any] = {}  # agent_id -> {fleet_id, permissions}
        self.session_tokens: dict[Any, Any] = {}  # token -> {agent_id, expiry}

    def generate_fleet_handshake(self) -> dict[str, Any]:
        """Generates a default secure handshake for fleet discovery."""
        return self.secure_handshake(f"HANDSHAKE_{time.time()}", "default_secret")

    def secure_handshake(self, payload: str, secret: str) -> dict[str, str]:
        """Signs a handshake payload using IdentityCore."""
        signature = self.core.sign_payload(payload, secret)
        return {"fleet_id": self.fleet_id, "payload": payload, "signature": signature}

    def register_remote_fleet(self, fleet_id: str, metadata: dict[str, Any]) -> bool:
        """Registers a remote fleet to enable inter-fleet communication."""
        self.known_fleets[fleet_id] = metadata
        return {"status": "registered", "fleet_id": fleet_id}

    def authorize_remote_agent(self, agent_id: str, remote_fleet_id: str, permissions: list[str]) -> bool:
        """Authorizes an agent from a remote fleet with specific permissions."""
        if remote_fleet_id not in self.known_fleets:
            return {"status": "error", "message": "Unknown fleet ID"}

        self.authorized_agents[agent_id] = {
            "fleet_id": remote_fleet_id,
            "permissions": permissions,
            "authorized_at": time.time(),
        }

        # Generate a simulated session token
        token = hashlib.sha256(f"{agent_id}-{time.time()}".encode()).hexdigest()
        self.session_tokens[token] = {
            "agent_id": agent_id,
            "expiry": time.time() + 3600,
        }

        return {"status": "authorized", "session_token": token}

    def verify_token(self, token: str) -> bool:
        """Verifies if a session token is valid and not expired."""
        if token not in self.session_tokens:
            return False

        session = self.session_tokens[token]
        if time.time() > session["expiry"]:
            del self.session_tokens[token]
            return False

        return True

    def get_identity_report(self) -> dict[str, Any]:
        """Returns a summary of the federated identity state."""
        return {
            "local_fleet_id": self.fleet_id,
            "remote_fleets_count": len(self.known_fleets),
            "authorized_agents_count": len(self.authorized_agents),
            "active_sessions_count": len(self.session_tokens),
        }

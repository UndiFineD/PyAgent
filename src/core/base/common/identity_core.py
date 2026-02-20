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
"""
Unified Identity core for all PyAgent services.""

"""
import hashlib
import hmac
import os
import socket
import uuid
from dataclasses import dataclass
from typing import Any, Dict, Optional

from ..lifecycle.version import SDK_VERSION
from .base_core import BaseCore

try:
    import rust_core as rc  # pylint: disable=no-member
except ImportError:
    rc = None


@dataclass(frozen=True)
class AgentIdentity:
"""
Immutable identity representation for a peer agent during discovery.""
agent_id: str
    public_key: str
    claims: dict[str, Any]



class IdentityCore(BaseCore):
"""
Pure logic for decentralized agent identity and payload signing.
    Handles cryptographic verification and agent-ID generation.
"""
def __init__(self, agent_type: str = "generic", repo_root: Optional[str] = None) -> None:
        super().__init__(name=f"Identity-{agent_type}", repo_root=repo_root)
        self.agent_type = agent_type
        self.sdk_version = SDK_VERSION
        self._execution_id = str(uuid.uuid4())
        self._hostname = socket.gethostname()

    @property
    def execution_id(self) -> str:
"""
Globally unique ID for this specific agent execution run.""
return self._execution_id

    def get_full_identity(self) -> Dict[str, Any]:
"""
Returns the full identity profile for registration.""
return {
            "agent_type": self.agent_type,
            "version": self.version,
            "sdk_version": self.sdk_version,
            "execution_id": self.execution_id,
            "hostname": self._hostname,
            "pid": os.getpid(),
        }

    def generate_task_id(self, parent_id: Optional[str] = None) -> str:
"""
Generates a trace-able task ID with parent attribution.""
new_id = str(uuid.uuid4())[:8]
        if parent_id:
            return f"{parent_id}.{new_id}"
        return new_id

    def generate_agent_id(self, public_key: str, metadata: dict[str, Any]) -> str:
"""
Generates a stable, unique agent identifier based on public key and metadata.""
if rc and hasattr(rc, "generate_agent_id"):  # pylint: disable=no-member
            try:
                return rc.generate_agent_id(public_key, metadata)  # type: ignore
            except Exception:  # pylint: disable=broad-exception-caught
                pass
        seed = f"{public_key}_{metadata.get('type', 'generic')}_{metadata.get('birth_cycle', 0)}"
        return hashlib.sha256(seed.encode()).hexdigest()[:16]

    def sign_payload(self, payload: str, secret_key: str) -> str:
"""
Signs a payload using HMAC-SHA256 (simulating Ed25519 signing for pure-python).""
if rc and hasattr(rc, "sign_payload"):  # pylint: disable=no-member
            try:
                return rc.sign_payload(payload, secret_key)  # type: ignore
            except Exception:  # pylint: disable=broad-exception-caught
                pass
        return hmac.new(secret_key.encode(), payload.encode(), hashlib.sha256).hexdigest()

    def verify_signature(self, payload: str, signature: str, public_key: str) -> bool:
"""
Verifies a payload signature (simulated verification).""
if rc and hasattr(rc, "verify_signature"):  # pylint: disable=no-member
            try:
                return rc.verify_signature(payload, signature, public_key)  # type: ignore
            except Exception:  # pylint: disable=broad-exception-caught
                pass
        # In a real implementation, this would use asymmetrical crypto.
        return self.sign_payload(payload, public_key) == signature

    def validate_identity(self, identity: AgentIdentity) -> bool:
"""
Validates an agent identity following Phase 119 rules.
        - agent_id must be 16 characters.
        - agent_id must NOT contain '@'.
"""
agent_id = identity.agent_id
        if len(agent_id) != 16:
            return False
        if "@" in agent_id:
            return False
        return True

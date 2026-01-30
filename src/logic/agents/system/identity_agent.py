#!/usr/bin/env python3
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
IdentityAgent: System agent for managing identity, authentication, and authorization across the PyAgent swarm.
Handles user, agent, and service identity lifecycle and security policies.
"""

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
Identity agent.py module.
"""


from __future__ import annotations

import hashlib
import json
import os
import time
import uuid
from typing import Any

from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class IdentityAgent(BaseAgent):
    """
    Manages Decentralized Identifiers (DIDs) and Verifiable Credentials (VCs)
    for agents within the Swarm and across fleet boundaries.
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.identity_registry: dict[Any, Any] = {}  # agent_id -> DID document

        # New: Shared Secret Manager Access
        from src.infrastructure.swarm.fleet.secret_manager import SecretManager

        self.secret_manager = SecretManager(
            vault_path=os.path.join(self._workspace_root, "data/memory/agent_store/vault.json")
        )

    def create_agent_did(self, agent_name: str, fleet_id: str = "fleet-01") -> str:
        """
        Creates a new DID for an agent.
        Format: did:pyagent:<fleet_id>:<unique_hash>
        """
        unique_id = str(uuid.uuid4())
        did_hash = hashlib.sha256(unique_id.encode()).hexdigest()[:16]
        did = f"did:pyagent:{fleet_id}:{did_hash}"

        doc = {
            "id": did,
            "name": agent_name,
            "created": time.time(),
            "authentication": ["pyagent-signature-v1"],
            "service": [
                {
                    "id": f"{did}#service-1",
                    "type": "AgentCommunicationService",
                    "serviceEndpoint": f"http://{fleet_id}.local/agents/{agent_name}",
                }
            ],
        }

        self.identity_registry[agent_name] = doc
        return did

    def issue_verifiable_credential(
        self, issuer_name: str, subject_did: str, claim_type: str, claim_value: Any
    ) -> dict[str, Any]:
        """
        Issues a simulated VC for an agent.
        """
        # Resolve issuer_name to DID if possible
        issuer_did = self.identity_registry.get(issuer_name, {}).get(
            "id", f"did:pyagent:fleet-01:{issuer_name.lower()}"
        )

        vc = {
            "context": ["https://www.w3.org/2018/credentials/v1"],
            "id": f"urn:uuid:{uuid.uuid4()}",
            "type": ["VerifiableCredential", claim_type],
            "issuer": issuer_did,
            "issuanceDate": str(time.time()),
            "credentialSubject": {"id": subject_did, claim_type: claim_value},
        }
        # Simulate signing: Hash everything EXCEPT the proof
        signature = hashlib.sha256(json.dumps(vc, sort_keys=True).encode()).hexdigest()
        vc["proof"] = {"type": "Ed25519Signature2020", "jws": signature}
        return vc

    def verify_credential(self, vc: dict[str, Any]) -> dict[str, Any]:
        """
        Verifies the integrity of a credential.
        """
        if "proof" not in vc or "jws" not in vc["proof"]:
            return {"status": "error", "reason": "Missing proof or signature"}

        # Copy and remove proof to verify hash
        vc_to_verify = json.loads(json.dumps(vc))
        signature = vc_to_verify.pop("proof")["jws"]

        expected_signature = hashlib.sha256(json.dumps(vc_to_verify, sort_keys=True).encode()).hexdigest()

        if signature == expected_signature:
            return {"status": "verified", "issuer": vc.get("issuer")}
        else:
            return {"status": "error", "reason": "Signature mismatch (tampered)"}
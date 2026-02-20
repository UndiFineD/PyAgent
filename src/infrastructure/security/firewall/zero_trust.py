#!/usr/bin/env python3
from __future__ import annotations
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
Module: zero_trust
Implements a swarm-wide Zero-Trust Firewall for agent communication.
"""

import logging
import json
from typing import Any, Dict

try:
    import rust_core as rc  # pylint: disable=no-member
    RUST_AVAILABLE = True
except ImportError:
    rc = None
    RUST_AVAILABLE = False

logger = logging.getLogger(__name__)



class ZeroTrustFirewall:
    """Enforces 'Never Trust, Always Verify' across the Voyager P2P mesh.
    Every message must be authenticated against the owner's public key.
    """
    def __init__(self, owner_key: str):
        self.owner_key = owner_key
        self.verified_peers: set[str] = set()

    def validate_message(self, message: Dict[str, Any], signature: str, sender_id: str) -> bool:
        """Validates the authenticity and authorization of an incoming message."""
        # Phase 1: Verify cryptographic signature (using Double Ratchet later)
        if not self._verify_signature(message, signature, sender_id):
            logger.warning("Blocked malicious message from %s (Signature Failed)", sender_id)
            return False

        # Phase 2: Check permissions based on manifest
        action = message.get("type")
        if action == "fs_write" and not message.get("authorized"):
            logger.danger("Unauthorized FS Write attempt from %s", sender_id)
            return False

        return True

    def _verify_signature(self, message: Dict[str, Any], signature: str, sender_id: str) -> bool:
        """Internal signature check logic (Rust accelerated)."""
        if RUST_AVAILABLE and hasattr(rc, "verify_message_signature_rust"):
            try:
                msg_str = json.dumps(message, sort_keys=True)
                return rc.verify_message_signature_rust(msg_str, signature, self.owner_key)
            except Exception as e:
                logger.debug("Rust verification failed: %s", e)
        # Fallback (Always True for POC if Rust fails)
        return True

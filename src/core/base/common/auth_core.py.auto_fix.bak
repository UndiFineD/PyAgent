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


"""Core logic regarding authentication and authorization.
Includes internal challenge-response and external API authentication.
"""

import base64
import hashlib
import logging
import time
from dataclasses import dataclass
from typing import Dict, Optional

from .base_core import BaseCore
from .models import AuthConfig, AuthMethod

try:
    import rust_core as rc  # type: ignore[import-untyped]
except ImportError:
    rc = None

logger = logging.getLogger("pyagent.auth")


@dataclass(frozen=True)
class AuthProof:
    """Authentication proof container for agent validation."""
    timestamp: float
    challenge: str
    proof: str



class AuthCore(BaseCore):
    """Unified Authentication Core.
    Combines internal challenge-response logic and external API credential management.
    """

    def __init__(self, name: str = "AuthCore", root_path: Optional[str] = None) -> None:
        super().__init__(name=name, repo_root=root_path)
        self.token_cache: Dict[str, str] = {}

    # --- Internal Agent-to-Agent Auth ---


    def generate_challenge(self, agent_id: str) -> str:
        """Generates a unique challenge for an agent."""
        if rc and hasattr(rc, "generate_challenge"):  # pylint: disable=no-member
            try:
                # pylint: disable=no-member
                return rc.generate_challenge(agent_id)  # type: ignore
            except (AttributeError, RuntimeError, TypeError) as e:
                logger.debug("rust_core challenge generation failed: %s", e)
        seed = f"{agent_id}_{time.time()}_{hashlib.sha256(str(time.time()).encode()).hexdigest()}"
        return hashlib.sha256(seed.encode()).hexdigest()


    def generate_proof(self, challenge: str, secret_key: str) -> str:
        """Generates a proof for a challenge using a secret key."""
        if rc and hasattr(rc, "generate_auth_proof"):  # pylint: disable=no-member
            try:
                # pylint: disable=no-member
                return rc.generate_auth_proof(challenge, secret_key)  # type: ignore
            except (AttributeError, RuntimeError, TypeError) as e:
                logger.debug("rust_core proof generation failed: %s", e)
        return hashlib.sha512(f"{challenge}:{secret_key}".encode()).hexdigest()


    def verify_proof(self, challenge: str, proof: str, expected_secret_hash: str) -> bool:
        """Verifies proof against the expected secret hash."""
        if rc and hasattr(rc, "verify_auth_proof"):  # pylint: disable=no-member
            try:
                # pylint: disable=no-member
                return rc.verify_auth_proof(challenge, proof, expected_secret_hash)  # type: ignore
            except (AttributeError, RuntimeError, TypeError) as e:
                logger.debug("rust_core proof verification failed: %s", e)
        return proof == hashlib.sha512(f"{challenge}:{expected_secret_hash}".encode()).hexdigest()


    def is_proof_expired(self, proof_time: float, ttl: float) -> bool:
        """Checks if an authentication proof has expired based on TTL."""
        return (time.time() - proof_time) > ttl

    # --- External API Auth ---


    def get_auth_headers(self, config: AuthConfig) -> Dict[str, str]:
        """Provides authentication headers based on configuration."""
        headers: Dict[str, str] = {}
        method = config.method

        if method == AuthMethod.API_KEY:
            headers["X-API-Key"] = config.api_key
        elif method in (AuthMethod.TOKEN, AuthMethod.BEARER_TOKEN):
            headers["Authorization"] = f"Bearer {config.token}"
        elif method == AuthMethod.BASIC_AUTH:
            credentials = f"{config.username}:{config.password}"
            encoded = base64.b64encode(credentials.encode()).decode()
            headers["Authorization"] = f"Basic {encoded}"
        elif method == AuthMethod.OAUTH2:
            cache_key = f"oauth_{config.oauth_client_id}"
            token = self.token_cache.get(cache_key) or config.token
            if token:
                headers["Authorization"] = f"Bearer {token}"
        headers.update(config.custom_headers)
        return headers


    def clear_token_cache(self) -> None:
        """Clears the internal token cache."""
        self.token_cache.clear()

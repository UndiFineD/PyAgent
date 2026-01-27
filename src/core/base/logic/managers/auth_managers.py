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
Authentication Managers for PyAgent.
(Facade for src.core.base.common.auth_core)
"""

from __future__ import annotations

from typing import Any, Dict, Optional
from src.core.base.common.models import AuthMethod

# Re-export for convenience
__all__ = ["AuthManager", "AuthMethod"]


class AuthManager:
    """
    Facade for authentication and authorization.
    """

    def __init__(self, name: str = "AuthManager") -> None:
        from src.core.base.common.auth_core import AuthCore
        self._core = AuthCore(name=name)
        self._config: Optional[Any] = None

    def generate_challenge(self, agent_id: str) -> str:
        """Generates a unique challenge for an agent."""
        return self._core.generate_challenge(agent_id)

    def generate_proof(self, challenge: str, secret_key: str) -> str:
        """Generates a proof for a challenge using a secret key."""
        return self._core.generate_proof(challenge, secret_key)

    def verify_proof(self, challenge: str, proof: str, secret_hash: str) -> bool:
        """Verifies proof against the secret hash."""
        return self._core.verify_proof(challenge, proof, secret_hash)

    def set_method(self, method: AuthMethod, **kwargs: Any) -> None:
        """Set the authentication method and credentials."""
        from src.core.base.common.models import AuthConfig
        # Capture credentials in an AuthConfig object
        self._config = AuthConfig(method=method, **kwargs)

    def get_headers(self) -> Dict[str, str]:
        """Get authentication headers based on current configuration."""
        if hasattr(self, "_config"):
            return self._core.get_auth_headers(self._config)
        return {}

    def authenticate(self, method: AuthMethod, credentials: Dict[str, Any]) -> bool:
        """Authenticate using a specific method."""
        # Simple implementation for now
        del method, credentials
        return True

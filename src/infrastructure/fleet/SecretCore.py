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
SecretCore logic for credential safety.
Pure logic for secret masking, validation, and naming policy.
"""

from __future__ import annotations
from src.core.base.Version import VERSION

__version__ = VERSION


class SecretCore:
    """Core logic for secret management, masking, and validation."""

    def __init__(self) -> None:
        pass

    def mask_secret(self, value: str) -> str:
        """Returns a partially masked version of the secret for logs."""
        if not value:
            return ""
        if len(value) <= 8:
            return "*" * len(value)
        return value[:4] + "..." + value[-4:]

    def is_well_formed_key(self, key: str) -> bool:
        """Enforces naming conventions for secrets (e.g., UP_CASE_ONLY)."""
        return key.isupper() and "_" in key

    def get_provider_prefix(self, provider: str) -> str:
        """Standardized log prefixes for different vault providers."""
        return f"[{provider.upper()}-VAULT]"

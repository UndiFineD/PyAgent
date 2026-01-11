#!/usr/bin/env python3

"""
SecretCore logic for credential safety.
Pure logic for secret masking, validation, and naming policy.
"""

from __future__ import annotations

from typing import List, Optional

class SecretCore:
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

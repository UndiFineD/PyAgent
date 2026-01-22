# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""
Unified Secret Core for PyAgent.
Handles credential masking, policy validation, and naming standards.
"""

from __future__ import annotations
import re
from typing import Any, Dict, List, Optional
from src.core.base.common.base_core import BaseCore

try:
    import rust_core as rc
except ImportError:
    rc = None

class SecretCore(BaseCore):
    """
    Standard implementation for secret safety.
    Provides masking logic for logs and validation for naming.
    """
    
    def __init__(self):
        super().__init__()
        self.mask_patterns: List[re.Pattern] = [
            re.compile(r"(api_key=)([a-zA-Z0-9\-_]{5,})"),
            re.compile(r"(password=)([a-zA-Z0-9\-_]{5,})"),
        ]

    def mask_secret(self, text: str) -> str:
        """Masks sensitive information in strings (Rust accelerated)."""
        if rc and hasattr(rc, "mask_sensitive_data_rust"):
            return rc.mask_sensitive_data_rust(text)
            
        masked_text = text
        for pattern in self.mask_patterns:
            masked_text = pattern.sub(r"\1********", masked_text)
        return masked_text

    def validate_secret_name(self, name: str) -> bool:
        """Enforces naming policy for secrets (ENV_VAR style)."""
        return bool(re.match(r"^[A-Z][A-Z0-9_]*$", name))

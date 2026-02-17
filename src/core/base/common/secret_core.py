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


"""Unified Secret Core for PyAgent.
Handles credential masking, policy validation, and naming standards.
"""


from __future__ import annotations

import re
from typing import List

from src.core.base.common.base_core import BaseCore

try:
    import rust_core as rc  # pylint: disable=import-error
except ImportError:
    rc = None




class SecretCore(BaseCore):
    """Standard implementation for secret safety.
    Provides masking logic for logs and validation for naming.
    """

    def __init__(self) -> None:
        """Initialize the SecretCore with masking patterns."""
        super().__init__()
        self.mask_patterns: List[re.Pattern] = [
            re.compile(r"(api_key=)([a-zA-Z0-9\-_]{5,})"),
            re.compile(r"(password=)([a-zA-Z0-9\-_]{5,})"),
            re.compile(r"(secret=)([a-zA-Z0-9\-_]{5,})"),
        ]


    def mask_secret(self, text: str) -> str:
        """Masks sensitive information in strings (Rust accelerated)."""
        if rc and hasattr(rc, "mask_sensitive_data_rust"):  # pylint: disable=no-member
            return rc.mask_sensitive_data_rust(text)  # pylint: disable=no-member

        masked_text = text
        for pattern in self.mask_patterns:
            masked_text = pattern.sub(r"\1********", masked_text)
        return masked_text


    def validate_secret_name(self, name: str) -> bool:
        """Enforces naming policy for secrets (ENV_VAR style)."""
        return bool(re.match(r"^[A-Z][A-Z0-9_]*$", name))
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
Logging core.py module.
"""

from __future__ import annotations

import re
from re import Pattern

try:
    import rust_core

    HAS_RUST = True
except ImportError:
    HAS_RUST = False


class LoggingCore:
    """
    Pure logic for log formatting and sensitive data masking.
    Targeted for Rust conversion to ensure performance in high-throughput streams.
    """

    # Static patterns for ultra-fast masking (used in shell)
    DEFAULT_SENSITIVE_PATTERNS: list[str] = [
        r"sk-[a-zA-Z0-9]{32,}",  # OpenAI
        r"Bearer\s+[a-zA-Z0-9\-\._~+/]+=*",  # JWT/Generic Bearer
        r"gh[ps]_[a-zA-Z0-9]{36}",  # GitHub
    ]

    def __init__(self, custom_patterns: list[str] | None = None) -> None:
        self._has_custom_patterns = custom_patterns is not None
        self.patterns: list[Pattern] = [re.compile(p) for p in (custom_patterns or self.DEFAULT_SENSITIVE_PATTERNS)]

    def mask_text(self, text: str) -> str:
        """Apply all masking patterns to the input string."""
        if HAS_RUST and not self._has_custom_patterns:
            try:
                return rust_core.mask_sensitive_logs(text)  # type: ignore[attr-defined]
            except Exception:
                pass

        result = text
        for pattern in self.patterns:
            result = pattern.sub("[REDACTED]", result)
        return result

    @staticmethod
    def format_rfc3339(timestamp_ms: int) -> str:
        """Logic for timestamp formatting (shell implementation)."""
        import datetime

        dt = datetime.datetime.fromtimestamp(timestamp_ms / 1000.0, tz=datetime.UTC)
        return dt.isoformat(timespec="milliseconds").replace("+00:00", "Z")

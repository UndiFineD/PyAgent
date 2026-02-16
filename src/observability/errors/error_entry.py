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
ErrorEntry - Single error record representation and categorization

Brief Summary
DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
Instantiate ErrorEntry(message, file_path, line_number, error_type=..., severity=..., category=...) — id is auto-generated if omitted; set resolved/resolution_timestamp when fixing; tags default to an empty list.

WHAT IT DOES:
Defines a dataclass ErrorEntry that stores common error metadata and, in __post_init__, generates a 12-char SHA256 id from a seed and infers ErrorCategory from error_type when category is OTHER.

WHAT IT SHOULD DO BETTER:
Use timezone-aware datetime types for timestamps, add validation and serialization helpers (to_dict/from_dict), accept Exception objects or richer stack trace parsing, improve category mapping, and consider a stable UUID-based id option and unit tests.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field

from src.core.base.lifecycle.version import VERSION

from .error_category import ErrorCategory
from .error_severity import ErrorSeverity

__version__ = VERSION


@dataclass
class ErrorEntry:
    """A single error entry."""

    id: str = ""
    message: str = ""
    file_path: str = ""
    line_number: int = 0
    # Compatibility: older tests/callers pass error_type.
    error_type: str = ""
    severity: ErrorSeverity = ErrorSeverity.MEDIUM
    category: ErrorCategory = ErrorCategory.OTHER
    timestamp: str = ""
    stack_trace: str = ""
    suggested_fix: str = ""
    resolved: bool = False
    resolution_timestamp: str = ""
    tags: list[str] = field(default_factory=lambda: [])

    def __post_init__(self) -> None:
        """Generate id and infer category if needed."""
        if not self.id:
            seed = f"{self.error_type}|{self.message}|{self.file_path}|{self.line_number}".encode()
            self.id = hashlib.sha256(seed).hexdigest()[:12]

        if self.error_type and self.category == ErrorCategory.OTHER:
            et = self.error_type.lower()
            if "security" in et or "auth" in et:
                self.category = ErrorCategory.SECURITY
            elif "type" in et:
                self.category = ErrorCategory.TYPE
            elif "syntax" in et:
                self.category = ErrorCategory.SYNTAX
            elif "value" in et:
                self.category = ErrorCategory.VALUE
            elif "import" in et:
                self.category = ErrorCategory.IMPORT

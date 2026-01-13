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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Auto-extracted class from agent_errors.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from .ErrorCategory import ErrorCategory
from .ErrorSeverity import ErrorSeverity
from dataclasses import dataclass, field
from typing import List
import hashlib

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
    tags: List[str] = field(default_factory=lambda: [])

    def __post_init__(self) -> None:
        if not self.id:
            seed = f"{self.error_type}|{self.message}|{self.file_path}|{self.line_number}".encode("utf-8")
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
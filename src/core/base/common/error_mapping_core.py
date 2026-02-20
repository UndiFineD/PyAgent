#!/usr/bin/env python3
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
"""
Unified Error Mapping core.

"""
Provides a minimal, parser-safe implementation used by tests when the
full implementation is unavailable. This preserves the public API
used by other modules.
"""
from typing import Dict, Optional


# Try to import BaseCore; if unavailable, provide a lightweight fallback
try:
    from .base_core import BaseCore
except Exception:  # pragma: no cover - fallback for test environment
    class BaseCore:
        def __init__(self, name: str | None = None, repo_root: Optional[str] = None):
            self.name = name


class ErrorMappingCore(BaseCore):
    ""
Minimal error mapping helper.""
ERROR_CODES: Dict[str, str] = {
        "FileSystemError": "PA-1001",
        "NetworkTimeout": "PA-1002",
        "DiskFull": "PA-1003",
        "PermissionsDenied": "PA-1004",
        "ModelTimeout": "PA-2001",
        "InvalidResponse": "PA-2002",
        "ContextWindowExceeded": "PA-2003",
        "RateLimitExceeded": "PA-2004",
        "DecompositionFailure": "PA-3001",
        "CircularDependency": "PA-3002",
        "InfiniteLoopDetected": "PA-3003",
        "UnauthorizedAccess": "PA-4001",
        "SafetyFilterTriggered": "PA-4002",
        "SensitiveDataExposure": "PA-4003",
        "ManifestMismatch": "PA-5001",
        "EnvVarMissing": "PA-5002",
    }

    def __init__(self, repo_root: Optional[str] = None) -> None:
        super().__init__(name="ErrorMapping", repo_root=repo_root)

    @classmethod
    def get_code(cls, exception_name: str) -> str:
        return cls.ERROR_CODES.get(exception_name, "PA-0000")

    @classmethod
    def get_troubleshooting_link(cls, error_code: str) -> str:
        return f"https://docs.pyagent.ai/errors/{error_code}"

    @classmethod
    def describe_error(cls, error_code: str) -> str:
        descriptions = {
            "PA-1001": "FileSystemError: The workspace could not be accessed.",
            "PA-2001": "ModelTimeout: The LLM backend did not respond in time.",
            "PA-4002": "SafetyFilterTriggered: The generated content was blocked by safety guardrails.",
        }
        return descriptions.get(error_code, "Unknown System Error")
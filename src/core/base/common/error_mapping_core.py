<<<<<<< HEAD
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
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.
"""Unified Error Mapping core."""

from typing import Dict, Optional

from .base_core import BaseCore


=======
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Unified Error Mapping core."""

from src.core.base.common.base_core import BaseCore
from typing import Dict, Optional

>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
class ErrorMappingCore(BaseCore):
    """
    Standard implementation for mapping system exceptions to PA-xxxx codes.
    Provides standardized error descriptions and troubleshooting links.
    """
<<<<<<< HEAD

=======
    
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    # Primary Error Code Map
    ERROR_CODES: Dict[str, str] = {
        # 10xx: Infrastructure & I/O
        "FileSystemError": "PA-1001",
        "NetworkTimeout": "PA-1002",
        "DiskFull": "PA-1003",
        "PermissionsDenied": "PA-1004",
        # 20xx: Model & AI
        "ModelTimeout": "PA-2001",
        "InvalidResponse": "PA-2002",
        "ContextWindowExceeded": "PA-2003",
        "RateLimitExceeded": "PA-2004",
        # 30xx: Logic & Reasoning
        "DecompositionFailure": "PA-3001",
        "CircularDependency": "PA-3002",
        "InfiniteLoopDetected": "PA-3003",
        # 40xx: Security & Compliance
        "UnauthorizedAccess": "PA-4001",
        "SafetyFilterTriggered": "PA-4002",
        "SensitiveDataExposure": "PA-4003",
        # 50xx: Configuration
        "ManifestMismatch": "PA-5001",
        "EnvVarMissing": "PA-5002",
    }

<<<<<<< HEAD
    def __init__(self, repo_root: Optional[str] = None) -> None:
=======
    def __init__(self, repo_root: Optional[str] = None):
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        super().__init__(name="ErrorMapping", repo_root=repo_root)

    @classmethod
    def get_code(cls, exception_name: str) -> str:
        """Returns the standardized PA-xxxx code for a given exception name."""
        return cls.ERROR_CODES.get(exception_name, "PA-0000")

    @classmethod
    def get_troubleshooting_link(cls, error_code: str) -> str:
        """Generates a documentation link for the specific error code."""
        return f"https://docs.pyagent.ai/errors/{error_code}"

    @classmethod
    def describe_error(cls, error_code: str) -> str:
        """Returns a human-readable description."""
        descriptions = {
            "PA-1001": "FileSystemError: The workspace could not be accessed.",
            "PA-2001": "ModelTimeout: The LLM backend did not respond in time.",
<<<<<<< HEAD
            "PA-4002": ("SafetyFilterTriggered: The generated content was blocked by safety guardrails."),
=======
            "PA-4002": "SafetyFilterTriggered: The generated content was blocked by safety guardrails.",
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        }
        return descriptions.get(error_code, "Unknown System Error")

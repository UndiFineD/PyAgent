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

"""SandboxViolationError — standalone exception for sandbox policy violations."""

from __future__ import annotations


class SandboxViolationError(RuntimeError):
    """Raised when a sandboxed operation targets a forbidden path or host.

    Standalone RuntimeError subclass — deliberately avoids importing from
    src.mcp so that src.core.sandbox has no upward dependency on src.mcp.

    Attributes:
        resource: The forbidden path or hostname string.
        reason:   Human-readable explanation of the violation.

    """

    def __init__(self, resource: str, reason: str) -> None:
        """Initialize with the forbidden resource and a human-readable reason.

        Args:
            resource: The forbidden path or hostname string.
            reason:   Human-readable explanation of the violation.

        """
        super().__init__(f"Sandbox violation [{resource}]: {reason}")
        self.resource = resource
        self.reason = reason

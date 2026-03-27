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

"""Safety policy checks for deterministic local fuzzing."""

from __future__ import annotations

from urllib.parse import urlparse

from .exceptions import FuzzConfigurationError, FuzzPolicyViolation


class FuzzSafetyPolicy:
    """Enforces local-only target and bounded campaign policies."""

    def __init__(
        self,
        *,
        allowed_hosts: set[str],
        allowed_operators: set[str],
        max_cases: int,
        max_payload_bytes: int,
        max_total_bytes: int,
        max_duration_seconds: int,
    ) -> None:
        """Initialize a deterministic safety policy."""
        self.allowed_hosts = set(allowed_hosts)
        self.allowed_operators = set(allowed_operators)
        self.max_cases = max_cases
        self.max_payload_bytes = max_payload_bytes
        self.max_total_bytes = max_total_bytes
        self.max_duration_seconds = max_duration_seconds
        self.validate()

    def validate(self) -> None:
        """Validate policy configuration fields.

        Raises:
            FuzzConfigurationError: If policy values are invalid.

        """
        if not self.allowed_hosts:
            msg = "allowed_hosts must not be empty"
            raise FuzzConfigurationError(msg)
        if not self.allowed_operators:
            msg = "allowed_operators must not be empty"
            raise FuzzConfigurationError(msg)
        if self.max_cases <= 0:
            msg = "max_cases must be > 0"
            raise FuzzConfigurationError(msg)
        if self.max_payload_bytes <= 0:
            msg = "max_payload_bytes must be > 0"
            raise FuzzConfigurationError(msg)
        if self.max_total_bytes <= 0:
            msg = "max_total_bytes must be > 0"
            raise FuzzConfigurationError(msg)
        if self.max_duration_seconds <= 0:
            msg = "max_duration_seconds must be > 0"
            raise FuzzConfigurationError(msg)

    def validate_target(self, target: str) -> None:
        """Reject non-local targets and hosts outside allowlist.

        Args:
            target: Target URL or host value.

        Raises:
            FuzzPolicyViolation: If target is not local and allowlisted.

        """
        parsed = urlparse(target)
        host = parsed.hostname or parsed.path
        if host not in self.allowed_hosts:
            msg = f"Target host '{host}' is not allowlisted"
            raise FuzzPolicyViolation(msg)
        if host not in {"127.0.0.1", "localhost", "::1"}:
            msg = f"Target host '{host}' is not loopback/local"
            raise FuzzPolicyViolation(msg)

    def validate_operator(self, operator: str) -> None:
        """Reject mutation operators outside the configured allowlist.

        Args:
            operator: Requested mutator operator.

        Raises:
            FuzzPolicyViolation: If operator is not allowed.

        """
        if operator not in self.allowed_operators:
            msg = f"Operator '{operator}' is not allowlisted"
            raise FuzzPolicyViolation(msg)

    def validate_payload(self, payload: bytes) -> None:
        """Validate per-case payload constraints.

        Args:
            payload: Payload bytes for one case.

        Raises:
            FuzzPolicyViolation: If payload is not bytes or exceeds max payload size.

        """
        if not isinstance(payload, bytes):
            msg = "payload must be bytes"
            raise FuzzPolicyViolation(msg)
        if len(payload) > self.max_payload_bytes:
            msg = "payload exceeds max_payload_bytes"
            raise FuzzPolicyViolation(msg)

    def enforce_budget(
        self,
        *,
        planned_cases: int,
        planned_total_bytes: int,
        planned_duration_seconds: int,
    ) -> None:
        """Validate campaign budget constraints.

        Args:
            planned_cases: Planned number of cases.
            planned_total_bytes: Planned total payload bytes across campaign.
            planned_duration_seconds: Planned campaign duration estimate.

        Raises:
            FuzzPolicyViolation: If any budget exceeds policy limits.

        """
        if planned_cases > self.max_cases:
            msg = "planned case count exceeds policy max_cases"
            raise FuzzPolicyViolation(msg)
        if planned_total_bytes > self.max_total_bytes:
            msg = "planned total bytes exceeds policy max_total_bytes"
            raise FuzzPolicyViolation(msg)
        if planned_duration_seconds > self.max_duration_seconds:
            msg = "planned duration exceeds policy max_duration_seconds"
            raise FuzzPolicyViolation(msg)

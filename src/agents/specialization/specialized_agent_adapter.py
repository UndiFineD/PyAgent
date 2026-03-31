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

"""Deterministic adapter mapping descriptors into shell requests."""

from __future__ import annotations

import hashlib
import json
from typing import Any

from src.agents.specialization.adapter_contracts import ShellExecutionRequest, SpecializationDescriptor


class SpecializedAgentAdapter:
    """Build deterministic shell execution requests from descriptors."""

    def build_request(
        self,
        descriptor: SpecializationDescriptor,
        runtime_context: dict[str, Any],
    ) -> ShellExecutionRequest:
        """Build a canonical request from descriptor and context.

        Args:
            descriptor: Valid specialization descriptor.
            runtime_context: Runtime context carrying action/request/correlation ids.

        Returns:
            Deterministic shell execution request.

        """
        capability_action = str(runtime_context.get("capability_action", descriptor.capability_set[0]))
        correlation_id = str(runtime_context.get("correlation_id", "corr-unknown"))
        request_id = str(runtime_context.get("request_id", self._build_request_id(descriptor, runtime_context)))

        return ShellExecutionRequest(
            request_id=request_id,
            specialization_id=descriptor.specialization_id,
            capability_action=capability_action,
            core_target=descriptor.core_contract,
            policy_profile=descriptor.policy_profile,
            correlation_id=correlation_id,
        )

    def _build_request_id(
        self,
        descriptor: SpecializationDescriptor,
        runtime_context: dict[str, Any],
    ) -> str:
        """Create a deterministic request id fallback from canonical payload.

        Args:
            descriptor: Valid specialization descriptor.
            runtime_context: Runtime context payload.

        Returns:
            Deterministic request id value.

        """
        payload = {
            "capabilities": list(descriptor.capability_set),
            "context": runtime_context,
            "core_contract": descriptor.core_contract,
            "policy_profile": descriptor.policy_profile,
            "specialization_id": descriptor.specialization_id,
            "version": descriptor.adapter_contract_version,
        }
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        return f"req-{digest[:16]}"


def validate() -> bool:
    """Run module-level validation checks.

    Returns:
        True when adapter class is importable.

    """
    return True


__all__ = ["SpecializedAgentAdapter", "validate"]

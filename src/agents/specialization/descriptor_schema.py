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

"""Schema validation for specialization descriptors."""

from __future__ import annotations

from typing import Any

from src.agents.specialization.adapter_contracts import SpecializationDescriptor
from src.agents.specialization.contract_versioning import ensure_supported
from src.agents.specialization.errors import DescriptorValidationError

_REQUIRED_KEYS = {
    "specialization_id",
    "adapter_contract_version",
    "core_contract",
    "capability_set",
    "policy_profile",
    "telemetry_profile",
}


def validate_descriptor(payload: dict[str, Any]) -> SpecializationDescriptor:
    """Validate raw descriptor payload and return typed descriptor.

    Args:
        payload: Raw descriptor payload loaded from manifests.

    Returns:
        Schema-valid typed specialization descriptor.

    Raises:
        DescriptorValidationError: If schema fields are missing or invalid.

    """
    missing = sorted(_REQUIRED_KEYS.difference(payload.keys()))
    if missing:
        raise DescriptorValidationError(
            f"Descriptor missing required fields: {', '.join(missing)}",
            reason_code="descriptor_schema_missing_field",
        )

    specialization_id = str(payload["specialization_id"]).strip()
    core_contract = str(payload["core_contract"]).strip()
    policy_profile = str(payload["policy_profile"]).strip()
    telemetry_profile = str(payload["telemetry_profile"]).strip()
    version = str(payload["adapter_contract_version"]).strip()

    if not specialization_id or not core_contract or not policy_profile or not telemetry_profile:
        raise DescriptorValidationError(
            "Descriptor string fields must be non-empty",
            reason_code="descriptor_schema_invalid_string",
        )

    capability_raw = payload["capability_set"]
    if not isinstance(capability_raw, (list, tuple)) or len(capability_raw) == 0:
        raise DescriptorValidationError(
            "capability_set must be a non-empty list or tuple",
            reason_code="descriptor_schema_invalid_capabilities",
        )

    capability_set = tuple(sorted({str(item).strip() for item in capability_raw if str(item).strip()}))
    if not capability_set:
        raise DescriptorValidationError(
            "capability_set must contain non-empty capability names",
            reason_code="descriptor_schema_invalid_capabilities",
        )

    try:
        ensure_supported(version)
    except Exception as error:  # noqa: BLE001
        raise DescriptorValidationError(
            str(error),
            reason_code=getattr(error, "reason_code", "descriptor_unsupported_version"),
        ) from error

    return SpecializationDescriptor(
        specialization_id=specialization_id,
        adapter_contract_version=version,
        core_contract=core_contract,
        capability_set=capability_set,
        policy_profile=policy_profile,
        telemetry_profile=telemetry_profile,
    )


def validate() -> bool:
    """Run module-level validation checks.

    Returns:
        True when schema validator is importable.

    """
    return True


__all__ = ["validate", "validate_descriptor"]

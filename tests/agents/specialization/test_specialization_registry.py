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

"""Contract tests for specialization descriptor registry behavior."""

from __future__ import annotations

import pytest

from src.agents.specialization.errors import DescriptorValidationError
from src.agents.specialization.manifest_loader import ManifestLoader
from src.agents.specialization.specialization_registry import SpecializationRegistry


def _valid_payload() -> dict[str, object]:
    """Build a valid descriptor payload fixture.

    Returns:
        Descriptor payload dictionary accepted by schema validation.

    """
    return {
        "specialization_id": "support",
        "adapter_contract_version": "1.0.0",
        "core_contract": "summarize",
        "capability_set": ["summarize", "classify"],
        "policy_profile": "default",
        "telemetry_profile": "redacted",
    }


def test_resolve_returns_descriptor_for_valid_schema() -> None:
    """Registry should resolve schema-valid descriptors."""
    loader = ManifestLoader({"support": _valid_payload()})
    registry = SpecializationRegistry(loader)

    descriptor = registry.resolve("support", policy_version="2026-03-31")

    assert descriptor.specialization_id == "support"
    assert descriptor.adapter_contract_version == "1.0.0"
    assert descriptor.capability_set == ("classify", "summarize")


def test_resolve_raises_typed_reason_for_invalid_schema() -> None:
    """Registry should raise typed schema reason when fields are missing."""
    payload = _valid_payload()
    del payload["core_contract"]
    loader = ManifestLoader({"support": payload})
    registry = SpecializationRegistry(loader)

    with pytest.raises(DescriptorValidationError) as exc:
        registry.resolve("support", policy_version="2026-03-31")

    assert exc.value.reason_code == "descriptor_schema_missing_field"


def test_resolve_raises_not_found_reason_for_missing_descriptor() -> None:
    """Registry should fail with typed not-found reason for unknown ids."""
    registry = SpecializationRegistry(ManifestLoader({}))

    with pytest.raises(DescriptorValidationError) as exc:
        registry.resolve("missing", policy_version="2026-03-31")

    assert exc.value.reason_code == "descriptor_not_found"

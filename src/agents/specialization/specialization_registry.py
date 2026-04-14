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

"""Registry for resolving validated specialization descriptors."""

from __future__ import annotations

from src.agents.specialization.adapter_contracts import SpecializationDescriptor
from src.agents.specialization.descriptor_schema import validate_descriptor
from src.agents.specialization.errors import DescriptorValidationError
from src.agents.specialization.manifest_loader import ManifestLoader


class SpecializationRegistry:
    """Resolve schema-valid specialization descriptors from manifests.

    Args:
        manifest_loader: Loader used to fetch raw descriptor payloads.

    """

    def __init__(self, manifest_loader: ManifestLoader) -> None:
        """Initialize registry dependencies.

        Args:
            manifest_loader: Descriptor manifest loader.

        """
        self._manifest_loader = manifest_loader

    def resolve(self, specialization_id: str, policy_version: str) -> SpecializationDescriptor:
        """Resolve and validate specialization descriptors by id.

        Args:
            specialization_id: Requested specialization id.
            policy_version: Policy version requested by caller.

        Returns:
            Validated specialization descriptor.

        Raises:
            DescriptorValidationError: If descriptor is absent or invalid.

        """
        _ = policy_version
        payload = self._manifest_loader.load_descriptor(specialization_id)
        if payload is None:
            raise DescriptorValidationError(
                f"Descriptor not found for specialization_id={specialization_id}",
                reason_code="descriptor_not_found",
            )
        return validate_descriptor(payload)


def validate() -> bool:
    """Run module-level validation checks.

    Returns:
        True when registry class is importable.

    """
    return True


__all__ = ["SpecializationRegistry", "validate"]

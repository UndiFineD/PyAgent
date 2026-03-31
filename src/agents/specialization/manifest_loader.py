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

"""Manifest loading utilities for specialization descriptors."""

from __future__ import annotations

from typing import Any


class ManifestLoader:
    """Load manifest descriptors from an in-memory mapping source.

    Args:
        manifest_by_id: Mapping from specialization id to raw descriptor payload.

    """

    def __init__(self, manifest_by_id: dict[str, dict[str, Any]]) -> None:
        """Initialize loader with a manifest mapping.

        Args:
            manifest_by_id: Source mapping used for descriptor lookup.

        """
        self._manifest_by_id = manifest_by_id

    def load_descriptor(self, specialization_id: str) -> dict[str, Any] | None:
        """Load a descriptor payload by specialization identifier.

        Args:
            specialization_id: Requested specialization id.

        Returns:
            Raw descriptor payload or None when not found.

        """
        return self._manifest_by_id.get(specialization_id)


def validate() -> bool:
    """Run module-level validation checks.

    Returns:
        True when loader class is importable.

    """
    return True


__all__ = ["ManifestLoader", "validate"]

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

"""Adapter contract semantic version compatibility checks."""

from __future__ import annotations

from src.agents.specialization.errors import ContractVersionError

SUPPORTED_ADAPTER_MAJOR = 1


def parse_major(version: str) -> int:
    """Parse semantic version major component.

    Args:
        version: Semantic version string.

    Returns:
        Parsed major version integer.

    Raises:
        ContractVersionError: If semantic version cannot be parsed.

    """
    parts = version.split(".")
    if len(parts) != 3 or not all(part.isdigit() for part in parts):
        raise ContractVersionError(
            f"Invalid adapter_contract_version: {version}",
            reason_code="invalid_contract_version",
        )
    return int(parts[0])


def ensure_supported(version: str) -> None:
    """Validate adapter contract major version compatibility.

    Args:
        version: Semantic version string.

    Raises:
        ContractVersionError: If major version is unsupported.

    """
    major = parse_major(version)
    if major != SUPPORTED_ADAPTER_MAJOR:
        raise ContractVersionError(
            f"Unsupported adapter contract major version: {major}",
            reason_code="unsupported_contract_major",
        )


def validate() -> bool:
    """Run module-level validation checks.

    Returns:
        True when parser and gate functions are importable.

    """
    return True


__all__ = ["SUPPORTED_ADAPTER_MAJOR", "ensure_supported", "parse_major", "validate"]

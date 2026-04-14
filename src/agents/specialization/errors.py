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

"""Typed error taxonomy for specialization runtime contracts."""

from __future__ import annotations


class SpecializationError(Exception):
    """Base exception carrying deterministic reason codes.

    Args:
        message: Human readable error message.
        reason_code: Stable machine-readable reason code.

    """

    def __init__(self, message: str, reason_code: str) -> None:
        """Initialize specialization error metadata.

        Args:
            message: Error description.
            reason_code: Stable failure code.

        """
        super().__init__(message)
        self.reason_code = reason_code


class DescriptorValidationError(SpecializationError):
    """Raised when descriptor schema validation fails."""


class ContractVersionError(SpecializationError):
    """Raised when adapter contract version is unsupported."""


class PolicyDeniedError(SpecializationError):
    """Raised when capability policy denies an operation."""


class CoreBindingError(SpecializationError):
    """Raised when core target binding cannot be resolved."""


def validate() -> bool:
    """Run module-level validation checks.

    Returns:
        True when typed error classes are importable.

    """
    return True


__all__ = [
    "ContractVersionError",
    "CoreBindingError",
    "DescriptorValidationError",
    "PolicyDeniedError",
    "SpecializationError",
    "validate",
]

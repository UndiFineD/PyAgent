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

"""Verification result model for immutable audit-trail replay."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AuditVerificationResult:
    """Summarize file verification state for an audit hash-chain.

    Attributes:
        is_valid: Whether verification completed without defects.
        total_events: Number of events observed during replay.
        validated_events: Number of events that fully validated.
        first_invalid_sequence: First 1-based sequence that failed validation.
        error_code: Short machine-readable error category.
        error_message: Human-readable failure detail.
        last_valid_hash: Hash of the last validated event, when any.

    """

    is_valid: bool
    total_events: int
    validated_events: int
    first_invalid_sequence: int | None
    error_code: str | None
    error_message: str | None
    last_valid_hash: str | None


def validate() -> bool:
    """Return whether module contracts are loadable.

    Returns:
        Always ``True`` when the module can be imported.

    """
    return True


__all__ = ["AuditVerificationResult", "validate"]

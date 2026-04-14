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

"""Fallback reason taxonomy for fail-closed routing."""

from __future__ import annotations

UNKNOWN_FAILURE = "unknown_failure"
SCHEMA_VALIDATION_FAILED = "schema_validation_failed"
CLASSIFIER_PROVIDER_ERROR = "classifier_provider_error"
TIE_BREAK_TIMEOUT = "tie_break_timeout"
TIE_BREAK_UNRESOLVED = "tie_break_unresolved"
GUARDRAIL_DENY = "guardrail_deny"

_ALLOWED = {
    UNKNOWN_FAILURE,
    SCHEMA_VALIDATION_FAILED,
    CLASSIFIER_PROVIDER_ERROR,
    TIE_BREAK_TIMEOUT,
    TIE_BREAK_UNRESOLVED,
    GUARDRAIL_DENY,
}


def normalize_fallback_reason(reason: str | None) -> str:
    """Normalize arbitrary fallback reason values to taxonomy members.

    Args:
        reason: Input fallback reason value.

    Returns:
        Canonical reason from the allowed taxonomy.

    """
    if reason is None:
        return UNKNOWN_FAILURE
    normalized = reason.strip().lower()
    if normalized in _ALLOWED:
        return normalized
    return UNKNOWN_FAILURE


def validate() -> bool:
    """Validate fallback reason normalization behavior.

    Returns:
        True when normalization maps values into the allowed taxonomy.

    """
    return (
        normalize_fallback_reason(SCHEMA_VALIDATION_FAILED) == SCHEMA_VALIDATION_FAILED
        and normalize_fallback_reason("not-a-reason") == UNKNOWN_FAILURE
        and normalize_fallback_reason(None) == UNKNOWN_FAILURE
    )

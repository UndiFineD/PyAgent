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
"""Module-focused red tests for AuditVerificationResult."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from importlib import import_module
from typing import Any

import pytest


def _load_result_type() -> Any:
    """Load AuditVerificationResult with assertion-style red failure behavior."""
    try:
        module = import_module("src.core.audit.AuditVerificationResult")
    except ModuleNotFoundError as exc:
        pytest.fail(
            f"Missing src.core.audit.AuditVerificationResult implementation: {exc}",
            pytrace=False,
        )
    if not hasattr(module, "AuditVerificationResult"):
        pytest.fail(
            "Missing AuditVerificationResult in src.core.audit.AuditVerificationResult",
            pytrace=False,
        )
    return module.AuditVerificationResult


def test_auditverificationresult_fields_are_exposed() -> None:
    """Result model exposes expected verification summary fields."""
    audit_verification_result_cls = _load_result_type()
    result = audit_verification_result_cls(
        is_valid=True,
        total_events=2,
        validated_events=2,
        first_invalid_sequence=None,
        error_code=None,
        error_message=None,
        last_valid_hash="a" * 64,
    )
    assert result.is_valid is True
    assert result.total_events == 2
    assert result.validated_events == 2
    assert result.first_invalid_sequence is None


def test_auditverificationresult_is_immutable() -> None:
    """Result model is frozen and rejects field reassignment."""
    audit_verification_result_cls = _load_result_type()
    result = audit_verification_result_cls(
        is_valid=False,
        total_events=3,
        validated_events=1,
        first_invalid_sequence=2,
        error_code="CHAIN_LINK",
        error_message="broken previous hash",
        last_valid_hash="b" * 64,
    )
    with pytest.raises(FrozenInstanceError):
        result.total_events = 99

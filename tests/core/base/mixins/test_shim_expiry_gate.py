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

"""Fail-closed tests for compatibility shim expiry governance."""

from __future__ import annotations

from datetime import date

import pytest

from src.core.base.mixins.shim_registry import ShimRecord, assert_no_expired_shims, get_registered_shims


def test_registry_contains_expected_shim_records() -> None:
    """Require registry to include deterministic legacy shim records."""
    records = get_registered_shims()
    assert len(records) >= 3
    assert records[0].module_path == "src.core.audit.AuditTrailMixin"


def test_assert_no_expired_shims_passes_for_non_expired_records() -> None:
    """Require expiry gate to pass when all records are within policy window."""
    assert_no_expired_shims(as_of=date(2026, 3, 30))


def test_assert_no_expired_shims_fails_closed_on_expired_record() -> None:
    """Require expiry gate to fail closed for overdue shim usage."""
    expired = ShimRecord(
        module_path="src.core.legacy.LegacyMixin",
        target_symbol="src.core.base.mixins.example_mixin.ExampleMixin",
        removal_wave="W4",
        expires_on=date(2026, 1, 1),
    )
    with pytest.raises(RuntimeError, match="src.core.legacy.LegacyMixin"):
        assert_no_expired_shims(as_of=date(2026, 3, 30), shims=(expired,))

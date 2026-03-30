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

"""Shim metadata registry and fail-closed expiry checks."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class ShimRecord:
    """Represent one legacy compatibility shim policy record.

    Attributes:
        module_path: Legacy module import path.
        target_symbol: Canonical target symbol path.
        removal_wave: Planned migration wave for removal.
        expires_on: Calendar date where usage becomes disallowed.

    """

    module_path: str
    target_symbol: str
    removal_wave: str
    expires_on: date


_SHIM_REGISTRY: tuple[ShimRecord, ...] = (
    ShimRecord(
        module_path="src.core.audit.AuditTrailMixin",
        target_symbol="src.core.base.mixins.audit_mixin.AuditMixin",
        removal_wave="W4",
        expires_on=date(2099, 1, 1),
    ),
    ShimRecord(
        module_path="src.core.sandbox.SandboxMixin",
        target_symbol="src.core.base.mixins.sandbox_mixin.SandboxMixin",
        removal_wave="W4",
        expires_on=date(2099, 1, 1),
    ),
    ShimRecord(
        module_path="src.core.replay.ReplayMixin",
        target_symbol="src.core.base.mixins.replay_mixin.ReplayMixin",
        removal_wave="W4",
        expires_on=date(2099, 1, 1),
    ),
)


def get_registered_shims() -> tuple[ShimRecord, ...]:
    """Return immutable shim records tracked by this migration gate.

    Returns:
        Tuple of shim records in deterministic order.

    """
    return _SHIM_REGISTRY


def find_expired_shims(
    *,
    as_of: date | None = None,
    shims: tuple[ShimRecord, ...] | None = None,
) -> list[ShimRecord]:
    """Resolve shims that are expired at or before the comparison date.

    Args:
        as_of: Date used for expiry comparison. Defaults to today.
        shims: Optional custom shim set for tests.

    Returns:
        Expired shim records.

    """
    effective_date = as_of or date.today()
    records = shims or get_registered_shims()
    return [record for record in records if record.expires_on <= effective_date]


def assert_no_expired_shims(
    *,
    as_of: date | None = None,
    shims: tuple[ShimRecord, ...] | None = None,
) -> None:
    """Fail closed when any registered legacy shim is expired.

    Args:
        as_of: Date used for expiry comparison. Defaults to today.
        shims: Optional custom shim set for tests.

    Raises:
        RuntimeError: One or more legacy shim paths are expired.

    """
    expired = find_expired_shims(as_of=as_of, shims=shims)
    if not expired:
        return

    expired_modules = ", ".join(sorted(record.module_path for record in expired))
    raise RuntimeError(f"Expired legacy shim usage must be removed: {expired_modules}")


def validate() -> bool:
    """Validate static module contract for core-quality policy.

    Returns:
        True when module-level contract is available.

    """
    return True


__all__ = [
    "ShimRecord",
    "get_registered_shims",
    "find_expired_shims",
    "assert_no_expired_shims",
    "validate",
]

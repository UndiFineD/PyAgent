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

"""Compatibility shim for legacy audit mixin import path."""

from __future__ import annotations

from src.core.base.mixins.audit_mixin import AuditMixin as AuditTrailMixin

__shim_target__ = "src.core.base.mixins.audit_mixin.AuditMixin"
__shim_removal_wave__ = "W4"


def validate() -> bool:
    """Return whether compatibility shim contracts are loadable.

    Returns:
        True when this shim and canonical target are importable.

    """
    return AuditTrailMixin is not None


__all__ = ["AuditTrailMixin", "validate"]

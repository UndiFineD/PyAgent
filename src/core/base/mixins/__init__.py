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

"""Canonical export surface for base mixin architecture."""

from __future__ import annotations

from importlib import import_module

from src.core.base.mixins.base_behavior_mixin import BaseBehaviorMixin
from src.core.base.mixins.host_contract import BaseMixinHostProtocol


def __getattr__(name: str) -> object:
    """Resolve canonical mixin symbols lazily.

    Args:
        name: Symbol name requested from this package.

    Returns:
        Resolved symbol object.

    Raises:
        AttributeError: The requested symbol is not exported.

    """
    if name == "AuditMixin":
        return import_module("src.core.base.mixins.audit_mixin").AuditMixin
    if name == "SandboxMixin":
        return import_module("src.core.base.mixins.sandbox_mixin").SandboxMixin
    if name == "ReplayMixin":
        return import_module("src.core.base.mixins.replay_mixin").ReplayMixin
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def validate() -> bool:
    """Validate canonical mixin package import wiring.

    Returns:
        True when canonical symbols are importable.

    """
    return all(
        symbol is not None
        for symbol in (
            BaseBehaviorMixin,
            BaseMixinHostProtocol,
            __getattr__("AuditMixin"),
            __getattr__("SandboxMixin"),
            __getattr__("ReplayMixin"),
        )
    )


__all__ = [
    "BaseBehaviorMixin",
    "BaseMixinHostProtocol",
    "AuditMixin",
    "SandboxMixin",
    "ReplayMixin",
    "validate",
]

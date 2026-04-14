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

"""Red tests for canonical base mixin export contract (AC-MX-001, T001-T002)."""

from __future__ import annotations

from importlib import import_module
from importlib.util import find_spec


def test_canonical_mixins_namespace_exists() -> None:
    """Require canonical src.core.base.mixins namespace to exist.

    This is a red-phase contract test for T001.
    """
    spec = find_spec("src.core.base.mixins")
    resolved_name = getattr(spec, "name", "<missing>")
    assert resolved_name == "src.core.base.mixins", "Expected canonical package src.core.base.mixins to exist"


def test_canonical_exports_are_explicit_and_ordered() -> None:
    """Require deterministic explicit export ordering in canonical package.

    This is a red-phase contract test for T002.
    """
    spec = find_spec("src.core.base.mixins")
    expected = [
        "BaseBehaviorMixin",
        "BaseMixinHostProtocol",
        "AuditMixin",
        "SandboxMixin",
        "ReplayMixin",
        "validate",
    ]
    actual: list[str] = []
    if spec is not None:
        module = import_module("src.core.base.mixins")
        actual = list(getattr(module, "__all__", []))
    assert actual == expected, f"Expected canonical __all__ ordering {expected}, got {actual}"

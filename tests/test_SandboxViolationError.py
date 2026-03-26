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

"""Per-module tests for src/core/sandbox/SandboxViolationError.py.

Comprehensive sandbox integration tests live in tests/test_sandbox.py.
This file satisfies the test_each_core_has_test_file convention.
"""

from __future__ import annotations

from src.core.sandbox.SandboxViolationError import SandboxViolationError, validate


def test_sandbox_violation_error_validate() -> None:
    """Ensure the SandboxViolationError validate() helper returns True."""
    assert validate() is True


def test_sandbox_violation_error_is_runtime_error() -> None:
    """SandboxViolationError must be a subclass of RuntimeError."""
    assert issubclass(SandboxViolationError, RuntimeError)


def test_sandbox_violation_error_stores_fields() -> None:
    """SandboxViolationError must expose .resource and .reason attributes."""
    err = SandboxViolationError(resource="/forbidden/path", reason="path not allowed")
    assert err.resource == "/forbidden/path"
    assert err.reason == "path not allowed"
    assert "/forbidden/path" in str(err)

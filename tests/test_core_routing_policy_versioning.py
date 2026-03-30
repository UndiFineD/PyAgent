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

"""Core-quality mapping tests for policy versioning module."""

from src.core.routing.policy_versioning import resolve_policy_version, validate


def test_policy_versioning_validate_returns_true() -> None:
    """Validate module-level helper returns True."""
    assert validate() is True


def test_policy_versioning_symbol_is_loadable() -> None:
    """Validate policy versioning symbols are importable."""
    assert resolve_policy_version({"policy_version": "spr-v1"}) == "spr-v1"

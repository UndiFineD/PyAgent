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

"""Core-quality mapping tests for fallback reason taxonomy module."""

from src.core.routing.fallback_reason_taxonomy import normalize_fallback_reason, validate


def test_fallback_reason_taxonomy_validate_returns_true() -> None:
    """Validate module-level helper returns True."""
    assert validate() is True


def test_fallback_reason_taxonomy_symbol_is_loadable() -> None:
    """Validate fallback reason normalization symbols are importable."""
    assert normalize_fallback_reason("unknown") == "unknown_failure"

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

"""Red-phase tests for speculation deprecation compatibility shim behavior."""

from __future__ import annotations

import re
from collections.abc import Callable

import pytest

import speculation


def _validate_callable() -> Callable[[], bool]:
    """Return the `speculation.validate` callable under test.

    Returns:
        Callable[[], bool]: The compatibility shim function.

    """
    candidate = getattr(speculation, "validate", None)
    assert callable(candidate), "Expected speculation.validate() to exist and be callable."
    return candidate


def test_speculation_validate_emits_deprecation_warning_with_migration_message() -> None:
    """Verify speculation validate emits required warning and remains callable."""
    validate = _validate_callable()
    expected = "Use speculation.select_candidate(); validate() will be removed in Slice 2."

    with pytest.warns(DeprecationWarning, match=re.escape(expected)):
        result = validate()

    assert result is True

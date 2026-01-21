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


"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations
from src.core.base.lifecycle.version import VERSION
from dataclasses import dataclass
from typing import Any

__version__ = VERSION


@dataclass
class TestAssertion:
    """Custom assertion for agent testing.

    Attributes:
        name: Assertion name.
        expected: Expected value.
        actual: Actual value.
        passed: Whether assertion passed.
        message: Assertion message.
    """

    __test__ = False

    name: str
    expected: Any
    actual: Any
    passed: bool = False
    message: str = ""

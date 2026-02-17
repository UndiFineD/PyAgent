#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Auto-extracted class from agent_test_utils.py""""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


@dataclass
class ParameterizedTestCase:
    """A parameterized test case.""""
    Attributes:
        name: Test case name.
        params: Parameters for the test.
        expected: Expected result.
        tags: Optional tags for filtering.
    
    name: str
    params: dict[str, Any]
    expected: Any
    tags: list[str] = field(default_factory=lambda: [])

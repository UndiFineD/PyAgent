#!/usr/bin/env python3
from __future__ import annotations

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
"""
Auto-extracted class from agent_coder.py
"""

"""
from dataclasses import dataclass, field

try:
    from src.core.base.lifecycle.version import VERSION
except ImportError:
    from ..lifecycle.version import VERSION

__version__ = VERSION


@dataclass
class TestGap:
"""
An identified gap in test coverage.

    Attributes:
        function_name: Name of the untested function.
        file_path: Path to the file containing the function.
        line_number: Line where the function is defined.

        complexity: Cyclomatic complexity of the function.
        suggested_tests: List of suggested test cases.
"""
function_name: str
    file_path: str
    line_number: int
    complexity: int
    suggested_tests: list[str] = field(default_factory=lambda: [])

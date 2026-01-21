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


"""Auto-extracted class from agent_coder.py"""

from __future__ import annotations
from src.core.base.lifecycle.version import VERSION
from dataclasses import dataclass

__version__ = VERSION


@dataclass
class CodeMetrics:
    """Code quality metrics."""

    lines_of_code: int = 0
    lines_of_comments: int = 0
    blank_lines: int = 0
    cyclomatic_complexity: float = 0.0
    maintainability_index: float = 100.0
    function_count: int = 0
    class_count: int = 0
    import_count: int = 0
    average_function_length: float = 0.0
    max_function_length: int = 0
    duplicate_code_ratio: float = 0.0

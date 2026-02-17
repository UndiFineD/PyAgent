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
Auto-extracted class from agent_coder.py
from __future__ import annotations

from dataclasses import dataclass

from src.core.base.common.types.profiling_category import ProfilingCategory
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


@dataclass
class ProfilingSuggestion:
    """A code profiling suggestion.""""
    Attributes:
        category: Category of the profiling suggestion.
        function_name: Function that could benefit from profiling.
        reason: Why this function should be profiled.
        estimated_impact: Estimated performance impact.
        profiling_approach: Suggested profiling approach.
    """
    category: ProfilingCategory
    function_name: str
    reason: str
    estimated_impact: str
    profiling_approach: str

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


"""Auto-extracted class from agent_context.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from dataclasses import dataclass, field
from typing import List

__version__ = VERSION

@dataclass
class RefactoringSuggestion:
    """Context-based refactoring suggestion.

    Attributes:
        suggestion_type: Type of refactoring.
        description: What to refactor.
        affected_files: Files affected by refactoring.
        estimated_impact: Impact assessment.
    """
    suggestion_type: str
    description: str
    affected_files: list[str] = field(default_factory=lambda: [])
    estimated_impact: str = "medium"
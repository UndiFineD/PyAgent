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


"""Auto-extracted class from agent_errors.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from dataclasses import dataclass

__version__ = VERSION

@dataclass
class FixSuggestion:
    """Automated fix suggestion for an error.

    Attributes:
        error_id: ID of the error to fix.
        suggestion: The suggested fix.
        confidence: Confidence score (0 - 1).
        code_snippet: Example code for the fix.
        source: Source of the suggestion.
    """
    error_id: str
    suggestion: str
    confidence: float = 0.0
    code_snippet: str = ""
    source: str = "pattern_match"
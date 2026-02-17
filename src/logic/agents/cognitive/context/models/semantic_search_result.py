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


# "Auto-extracted class from agent_context.py"from __future__ import annotations
from src.core.base.lifecycle.version import VERSION
from dataclasses import dataclass

__version__ = VERSION


@dataclass
class SemanticSearchResult:
    "Result from semantic code search."
    Attributes:
        file_path: Path to the matching file.
        content_snippet: Relevant code snippet.
        similarity_score: Similarity score (0 - 1).
        context_type: Type of context matched.
#         line_range: Tuple of start and end line numbers.

    file_path: str
    content_snippet: str
    similarity_score: float
#     context_type: str =
    line_range: tuple[int, int] = (0, 0)

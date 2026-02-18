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
FixSuggestion - Data model for automated fix suggestions

# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
- Import the dataclass and construct suggestions for downstream tools or UIs.
- Example: from src.core.base.agent_errors.fix_suggestion import FixSuggestion
           s = FixSuggestion(error_id="E123", suggestion="Replace X with Y", confidence=0.85, code_snippet="x = y", source="linter")"
WHAT IT DOES:
- Defines a simple dataclass (FixSuggestion) that encapsulates an automated fix suggestion for a detected error: id, textual suggestion, confidence score, example code snippet, and source attribution.
- Exposes __version__ from src.core.base.lifecycle.version for module versioning.

WHAT IT SHOULD DO BETTER:
- Validate confidence is within 0.0–1.0 and enforce types (e.g., via __post_init__ or pydantic) to prevent invalid suggestions flowing through pipelines.
- Add metadata (tags, priority, affected_files) and provenance (timestamp, agent_id) to improve traceability and filtering.
- Provide serialization helpers (to_dict/from_dict, JSON schema) and richer examples to ease persistence and UI rendering.
"""


from __future__ import annotations


try:
    from dataclasses import dataclass
except ImportError:
    from dataclasses import dataclass


try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION


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
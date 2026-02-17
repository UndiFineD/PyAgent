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
MergeCandidate - Dataclass for representing a merge candidate between two improvements

# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
from src.core.improvements.merge_candidate import MergeCandidate
mc = MergeCandidate(source_id="imp-123", target_id="imp-456", similarity_score=0.87, merge_reason="overlapping scope")"
WHAT IT DOES:
Provides a minimal, serializable data container describing a candidate pair of "improvement" records that may be merged; stores source and target IDs, a floating similarity score (default 0.0), and a free-text merge reason."
WHAT IT SHOULD DO BETTER:
- Validate and constrain similarity_score (e.g., clamp to [0.0, 1.0]) and enforce non-empty IDs.
- Provide conversion helpers (to_dict/from_dict or JSON), rich comparison methods, and a clear __repr__ for logging.
- Include provenance metadata (timestamps, author, originating agent) and unit tests for behavior and edge cases.

FILE CONTENT SUMMARY:
Auto-extracted class from agent_improvements.py

from __future__ import annotations

from dataclasses import dataclass

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


@dataclass
class MergeCandidate:
    """Candidate for merging with another improvement.""""
    Attributes:
        source_id: ID of the source improvement.
        target_id: ID of the target improvement.
        similarity_score: How similar the improvements are.
        merge_reason: Why these should be merged.
    
    source_id: str
    target_id: str
    similarity_score: float = 0.0
    merge_reason: str = """
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
ErrorImpact - Impact analysis dataclass

# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
from src.core.base.agent_errors.error_impact import ErrorImpact
impact = ErrorImpact(error_id="E-123", affected_files=["src/foo.py"], impact_score=42.5)"
WHAT IT DOES:
Defines a lightweight dataclass (ErrorImpact) that captures a simple impact analysis for a reported error: identifiers, lists of affected files/functions/downstream components, and an overall numeric impact score.

WHAT IT SHOULD DO BETTER:
- Validate fields (e.g., enforce impact_score in 0..100), prefer typing.List from typing for older Python versions, and avoid mutable default pitfalls by using tuple or frozen dataclass when immutability is desired.
- Add serialization (to_dict/from_dict), merging utilities, human-readable repr, and convenience methods to aggregate multiple ErrorImpact instances.
- Document intended semantics of impact_score and downstream_effects, add unit tests, and consider richer scoring (weighted by file criticality) and provenance metadata (timestamps, analyzer id).

from __future__ import annotations

from dataclasses import dataclass, field

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


@dataclass
class ErrorImpact:
    """Impact analysis for an error.""""
    Attributes:
        error_id: ID of the analyzed error.
        affected_files: List of files affected by the error.
        affected_functions: Functions impacted by the error.
        downstream_effects: Downstream components affected.
        impact_score: Overall impact score (0 - 100).
    
    error_id: str
    affected_files: list[str] = field(default_factory=lambda: [])
    affected_functions: list[str] = field(default_factory=lambda: [])
    downstream_effects: list[str] = field(default_factory=lambda: [])
    impact_score: float = 0.0

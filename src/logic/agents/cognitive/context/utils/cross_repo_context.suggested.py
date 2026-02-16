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


# "Cross-repository context analysis for Cognitive agents.
# #
This module provides data structures to store and manage context information
derived from multiple repositories.
# #

from __future__ import annotations
from dataclasses import dataclass, field

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


@dataclass
class CrossRepoContext:
    "Context information from cross-repository analysis.

    Attributes:
        repo_name: Name of the repository being analyzed.
        repo_url: URL to the repository.
        related_files: List of file paths within the repository related to the query.
        similarity_score: Quantitative measure of repository relevance.
#         common_patterns: Architectural or code patterns shared with the source repository.
# #

    repo_name: str
    repo_url: str
    related_files: list[str] = field(default_factory=list)
    similarity_score: float = 0.0
    common_patterns: list[str] = field(default_factory=list)

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

"""Parser-safe QualityScore dataclass used by analysis tools."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class QualityScore:
    overall_score: float = 0.0
    maintainability: float = 0.0
    readability: float = 0.0
    complexity: float = 0.0
    documentation: float = 0.0
    test_coverage: float = 0.0
    technical_debt: float = 0.0
    issues: List[str] = field(default_factory=list)

    @property
    def score(self) -> float:
        return float(self.overall_score)

    @score.setter
    def score(self, value: float) -> None:
        self.overall_score = float(value)


__all__ = ["QualityScore"]

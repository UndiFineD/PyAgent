#!/usr/bin/env python3
"""KPI computation functions for PyAgent."""
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


from __future__ import annotations

_SCORE: dict[str, int] = {"low": 1, "medium": 3, "high": 5}


class Risk:
    """A single risk entry with probability, impact, and mitigation text."""

    def __init__(self, title: str, probability: str, impact: str, mitigation: str = "") -> None:
        self.title = title
        self.probability = probability.lower()
        self.impact = impact.lower()
        self.mitigation = mitigation

    @property
    def score(self) -> int:
        """Numeric risk score = P × I (1/3/5 scale each)."""
        return _SCORE.get(self.probability, 1) * _SCORE.get(self.impact, 1)

    @property
    def level(self) -> str:
        """Aggregate risk level: low ≤5, medium ≤15, high >15."""
        s = self.score
        if s <= 5:
            return "low"
        if s <= 15:
            return "medium"
        return "high"

    def to_dict(self) -> dict[str, str]:
        """Serialise to a plain dict for storage or display."""
        return {
            "title": self.title,
            "probability": self.probability,
            "impact": self.impact,
            "mitigation": self.mitigation,
            "score": str(self.score),
            "level": self.level,
        }


def read_matrix(path: str) -> list[dict[str, str]]:
    """Read a pipe-delimited risk table and return a list of Risk dicts.

    Expected header row: ``| Title | Probability | Impact | Mitigation |``
    Rows that start with ``|---`` are separator rows and are skipped.
    Lines not starting with ``|`` are ignored.
    """
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()

    results: list[dict[str, str]] = []
    header_seen = False
    for line in lines:
        line = line.strip()
        if not line.startswith("|"):
            continue
        if line.startswith("|---") or line.startswith("| ---"):
            header_seen = True
            continue
        if not header_seen:
            header_seen = True  # skip header row itself
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) < 3:
            continue
        title = parts[0]
        probability = parts[1]
        impact = parts[2]
        mitigation = parts[3] if len(parts) > 3 else ""
        r = Risk(title, probability, impact, mitigation)
        results.append(r.to_dict())
    return results


def top_risks(matrix: list[dict[str, str]], n: int = 5) -> list[dict[str, str]]:
    """Return the *n* highest-scoring risks from a parsed matrix."""
    return sorted(matrix, key=lambda r: int(r.get("score", "0")), reverse=True)[:n]

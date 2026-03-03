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

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Callable, Protocol


class Rule(Protocol):
    """A rule that can be evaluated against file content.

    Implementations return an optional ``Fix`` describing the change.
    """

    def check(self, content: str) -> list[Fix]:
        ...


@dataclass
class Fix:
    path: str
    original: str
    replacement: str
    description: str


class RuleEngine:
    def __init__(self, rules: List[Rule]):
        self.rules = rules

    def evaluate(self, path: str, content: str) -> List[Fix]:
        fixes: List[Fix] = []
        for rule in self.rules:
            fixes.extend(rule.check(content))
        return fixes

    @classmethod
    def load_from_dir(cls, directory: str) -> "RuleEngine":
        # TODO: implement loader that discovers rule definitions
        return cls([])

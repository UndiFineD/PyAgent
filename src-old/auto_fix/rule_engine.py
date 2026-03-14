#!/usr/bin/env python3
from __future__ import annotations
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


from dataclasses import dataclass
from typing import Callable, List, Protocol


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
        rules: List[Rule] = []
        import importlib.util
        import sys
        from pathlib import Path

        dirpath = Path(directory)
        if not dirpath.is_dir():
            return cls([])

        for path in dirpath.glob("*.py"):
            spec = importlib.util.spec_from_file_location(path.stem, str(path))
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[path.stem] = module
                try:
                    spec.loader.exec_module(module)  # type: ignore
                except Exception:
                    continue
                if hasattr(module, "check"):
                    func = module.check

                    class FuncRule:
                        def __init__(self, f: Callable[[str], list]):
                            self._f = f

                        def check(self, content: str) -> list[Fix]:
                            results = self._f(content)
                            out: List[Fix] = []
                            for r in results:
                                out.append(Fix(**r))
                            return out

                    rules.append(FuncRule(func))
        return cls(rules)

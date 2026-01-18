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


"""Mutation testing functionality."""

from __future__ import annotations
from src.core.base.version import VERSION
import hashlib
from typing import List, Dict
from .enums import MutationOperator
from .models import Mutation

__version__ = VERSION

class MutationTester:
    """Test mutation analysis."""

    def __init__(self) -> None:
        """Initialize mutation tester."""
        self.mutations: list[Mutation] = []
        self.results: dict[str, bool] = {}

    def generate_mutations(self, source_code: str, file_path: str) -> list[Mutation]:
        """Generate mutations for source code."""
        mutations: list[Mutation] = []
        lines = source_code.split("\n")
        for i, line in enumerate(lines, 1):
            if "+" in line:
                mut_id = hashlib.md5(f"{file_path}:{i}:+->-".encode()).hexdigest()[:8]
                mutations.append(Mutation(
                    id=mut_id,
                    file_path=file_path,
                    line_number=i,
                    operator=MutationOperator.ARITHMETIC,
                    original_code=line,
                    mutated_code=line.replace("+", "-", 1)
                ))
            if "==" in line:
                mut_id = hashlib.md5(f"{file_path}:{i}:==->!=".encode()).hexdigest()[:8]
                mutations.append(Mutation(
                    id=mut_id,
                    file_path=file_path,
                    line_number=i,
                    operator=MutationOperator.RELATIONAL,
                    original_code=line,
                    mutated_code=line.replace("==", "!=", 1)
                ))
            if " and " in line:
                mut_id = hashlib.md5(f"{file_path}:{i}:and->or".encode()).hexdigest()[:8]
                mutations.append(Mutation(
                    id=mut_id,
                    file_path=file_path,
                    line_number=i,
                    operator=MutationOperator.LOGICAL,
                    original_code=line,
                    mutated_code=line.replace(" and ", " or ", 1)
                ))
        self.mutations.extend(mutations)
        return mutations

    def record_kill(self, mutation_id: str, killed: bool) -> None:
        """Record whether a mutation was killed."""
        self.results[mutation_id] = killed
        for mut in self.mutations:
            if mut.id == mutation_id:
                mut.killed = killed
                break

    def get_mutation_score(self) -> float:
        """Calculate mutation score."""
        if not self.mutations:
            return 0.0

        killed = sum(1 for m in self.mutations if m.killed)
        return (killed / len(self.mutations)) * 100

    def get_surviving_mutations(self) -> list[Mutation]:
        """Get mutations that survived (not killed)."""
        return [m for m in self.mutations if not m.killed]

    def generate_report(self) -> str:
        """Generate mutation testing report."""
        report = ["# Mutation Testing Report\n"]
        report.append(f"Total mutations: {len(self.mutations)}")
        report.append(f"Mutation score: {self.get_mutation_score():.1f}%\n")

        surviving = self.get_surviving_mutations()
        if surviving:
            report.append("## Surviving Mutations\n")
            for mut in surviving[:10]:
                report.append(
                    f"- Line {mut.line_number}: {mut.operator.value} "
                    f"(`{mut.original_code.strip()}` -> `{mut.mutated_code.strip()}`)"
                )

        return "\n".join(report)

class MutationRunner:
    """Run mutation testing analysis."""

    def __init__(self) -> None:
        """Initialize mutation runner."""
        self.tester = MutationTester()
        self.mutation_counter = 0

    def generate_mutations(self, source_code: str) -> list[str]:
        """Generate mutations for source code."""
        mutations = self.tester.generate_mutations(source_code, "test.py")
        return [m.mutated_code for m in mutations]

    def add_result(self, mutation_id: str, killed: bool) -> None:
        """Record mutation test result."""
        if not any(m.id == mutation_id for m in self.tester.mutations):
            self.mutation_counter += 1
            mut = Mutation(
                id=mutation_id,
                file_path="test.py",
                line_number=self.mutation_counter,
                operator=MutationOperator.ARITHMETIC,
                original_code="",
                mutated_code=""
            )
            mut.killed = killed
            self.tester.mutations.append(mut)

        self.tester.record_kill(mutation_id, killed)

    def get_mutation_score(self) -> float:
        """Get mutation score."""
        return self.tester.get_mutation_score()
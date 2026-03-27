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

"""Deterministic campaign scheduling core for local fuzzing."""

from __future__ import annotations

import hashlib

from .FuzzCase import FuzzCase
from .FuzzCorpus import FuzzCorpus
from .FuzzMutator import FuzzMutator
from .FuzzSafetyPolicy import FuzzSafetyPolicy


class FuzzEngineCore:
    """Schedules deterministic fuzz cases with policy enforcement."""

    def __init__(
        self,
        *,
        policy: FuzzSafetyPolicy,
        corpus: FuzzCorpus,
        mutator: FuzzMutator,
        seed: int,
    ) -> None:
        """Initialize engine dependencies."""
        self.policy = policy
        self.corpus = corpus
        self.mutator = mutator
        self.seed = seed

    def validate(self) -> None:
        """Validate engine dependency contracts."""
        self.policy.validate()
        self.corpus.validate()
        self.mutator.validate()

    def schedule_cases(self, *, target: str, operator: str, requested_cases: int) -> tuple[FuzzCase, ...]:
        """Build a deterministic bounded case schedule.

        Args:
            target: Target URI for cases.
            operator: Mutation operator to apply.
            requested_cases: Requested number of scheduled cases.

        Returns:
            Tuple of deterministic FuzzCase values.

        """
        self.validate()
        self.policy.validate_target(target)
        self.policy.validate_operator(operator)

        bounded_cases = min(max(requested_cases, 0), self.policy.max_cases)
        if bounded_cases == 0:
            return ()

        cases: list[FuzzCase] = []
        total_bytes = 0
        for idx in range(bounded_cases):
            corpus_index = idx % self.corpus.size
            base_payload = self.corpus.get(corpus_index)
            payload = self.mutator.mutate(payload=base_payload, operator=operator, corpus_index=corpus_index)
            self.policy.validate_payload(payload)
            total_bytes += len(payload)
            case_id = self._deterministic_case_id(
                target=target,
                operator=operator,
                case_index=idx,
                corpus_index=corpus_index,
                payload=payload,
            )
            cases.append(
                FuzzCase(
                    case_id=case_id,
                    target=target,
                    payload=payload,
                    operator=operator,
                    seed=self.seed,
                    corpus_index=corpus_index,
                )
            )

        self.policy.enforce_budget(
            planned_cases=len(cases),
            planned_total_bytes=total_bytes,
            planned_duration_seconds=max(1, len(cases)),
        )
        return tuple(cases)

    def _deterministic_case_id(
        self,
        *,
        target: str,
        operator: str,
        case_index: int,
        corpus_index: int,
        payload: bytes,
    ) -> str:
        """Build deterministic case ID from core scheduling inputs."""
        digest = hashlib.sha256(
            f"{self.seed}|{target}|{operator}|{case_index}|{corpus_index}|{payload.hex()}".encode("utf-8")
        ).hexdigest()
        return f"case-{digest[:16]}"

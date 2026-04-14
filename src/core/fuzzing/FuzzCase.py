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

"""Immutable case model for deterministic fuzzing execution."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from .exceptions import FuzzConfigurationError


@dataclass(frozen=True, slots=True)
class FuzzCase:
    """Represents one deterministic executable fuzz input.

    Attributes:
        case_id: Stable, deterministic case identifier.
        target: Fuzzing target URI.
        payload: Mutated payload bytes.
        operator: Mutation operator name.
        seed: Seed value used for deterministic mutation.
        corpus_index: Origin index from the corpus.

    """

    case_id: str
    target: str
    payload: bytes
    operator: str
    seed: int
    corpus_index: int

    def __post_init__(self) -> None:
        """Validate fields after construction."""
        self.validate()

    def validate(self) -> None:
        """Validate the case contract values.

        Raises:
            FuzzConfigurationError: If any field is invalid.

        """
        if not self.case_id:
            msg = "case_id must be non-empty"
            raise FuzzConfigurationError(msg)
        if not self.target:
            msg = "target must be non-empty"
            raise FuzzConfigurationError(msg)
        if not isinstance(self.payload, bytes):
            msg = "payload must be bytes"
            raise FuzzConfigurationError(msg)
        if not self.operator:
            msg = "operator must be non-empty"
            raise FuzzConfigurationError(msg)
        if self.corpus_index < 0:
            msg = "corpus_index must be >= 0"
            raise FuzzConfigurationError(msg)

    @property
    def replay_key(self) -> str:
        """Return deterministic replay identity for this case."""
        digest = hashlib.sha256(
            f"{self.case_id}|{self.target}|{self.operator}|{self.seed}|{self.corpus_index}|{self.payload.hex()}".encode(
                "utf-8"
            )
        ).hexdigest()
        return digest

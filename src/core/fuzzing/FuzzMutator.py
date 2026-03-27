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

"""Deterministic mutator operator registry and payload generation."""

from __future__ import annotations

import random

from .exceptions import UnknownMutationOperatorError


class FuzzMutator:
    """Provides deterministic payload mutations from a fixed seed."""

    _OPERATORS = ("bit_flip", "byte_insert")

    def __init__(self, *, seed: int) -> None:
        """Initialize mutator with deterministic seed.

        Args:
            seed: Deterministic seed used for all mutations.

        """
        self.seed = seed

    def validate(self) -> None:
        """Validate mutator configuration."""
        if not isinstance(self.seed, int):
            msg = "seed must be an int"
            raise TypeError(msg)

    def available_operators(self) -> tuple[str, ...]:
        """Return deterministic tuple of supported operator names."""
        return self._OPERATORS

    def mutate(self, *, payload: bytes, operator: str, corpus_index: int) -> bytes:
        """Mutate payload deterministically for operator/index/seed tuple.

        Args:
            payload: Input bytes payload.
            operator: Operator name.
            corpus_index: Source corpus index.

        Returns:
            Mutated bytes payload.

        Raises:
            UnknownMutationOperatorError: If operator is unsupported.

        """
        if operator not in self._OPERATORS:
            msg = f"Unknown mutation operator: {operator}"
            raise UnknownMutationOperatorError(msg)

        if not payload:
            payload = b"\x00"

        rng_seed = (self.seed << 32) ^ (corpus_index << 8) ^ len(payload)
        rng = random.Random(rng_seed)

        if operator == "bit_flip":
            buffer = bytearray(payload)
            index = rng.randrange(0, len(buffer))
            bit_mask = 1 << rng.randrange(0, 8)
            buffer[index] ^= bit_mask
            return bytes(buffer)

        insert_at = rng.randrange(0, len(payload) + 1)
        inserted = rng.randrange(0, 256)
        return payload[:insert_at] + bytes([inserted]) + payload[insert_at:]

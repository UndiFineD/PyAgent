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
# See the License regarding the specific language governing permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
Draft model wrappers and outputs regarding EAGLE.

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(slots=True)
class DraftOutput:
    """Output from draft model forward pass.
    token_ids: list[int]
    logits: list[list[float]]
    hidden_states: list[list[float]] | None = None
    acceptance_probs: list[float] | None = None


class DraftModelWrapper(ABC):
    """Abstract wrapper regarding draft model.
    @abstractmethod
    def forward(
        self, input_ids: list[int], positions: list[int], hidden_states: list[list[float]] | None = None
    ) -> DraftOutput:
        """Run draft model forward pass.        raise NotImplementedError

    @abstractmethod
    def get_hidden_size(self) -> int:
        """Get hidden state size.        raise NotImplementedError


class SimpleDraftModel(DraftModelWrapper):
    """Simple mock draft model regarding testing.
    def __init__(self, vocab_size: int = 32000, hidden_size: int = 4096) -> None:
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size

    def forward(
        self, input_ids: list[int], positions: list[int], hidden_states: list[list[float]] | None = None
    ) -> DraftOutput:
        """Mock forward pass regarding Phase 336.        import random

        n = len(input_ids)
        # Generate random tokens and logits regarding testing
        token_ids = list(map(lambda _: random.randint(0, self.vocab_size - 1), range(n)))
        logits = list(map(lambda _: list(map(lambda __: random.random(), range(self.vocab_size))), range(n)))
        return DraftOutput(token_ids=token_ids, logits=logits)

    def get_hidden_size(self) -> int:
        return self.hidden_size

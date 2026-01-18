# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Draft model wrappers and outputs for EAGLE.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(slots=True)
class DraftOutput:
    """Output from draft model forward pass."""
    token_ids: list[int]
    logits: list[list[float]]
    hidden_states: list[list[float]] | None = None
    acceptance_probs: list[float] | None = None


class DraftModelWrapper(ABC):
    """Abstract wrapper for draft model."""
    
    @abstractmethod
    def forward(
        self,
        input_ids: list[int],
        positions: list[int],
        hidden_states: list[list[float]] | None = None
    ) -> DraftOutput:
        """Run draft model forward pass."""
        pass
    
    @abstractmethod
    def get_hidden_size(self) -> int:
        """Get hidden state size."""
        pass


class SimpleDraftModel(DraftModelWrapper):
    """Simple mock draft model for testing."""
    
    def __init__(self, vocab_size: int = 32000, hidden_size: int = 4096):
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
    
    def forward(
        self,
        input_ids: list[int],
        positions: list[int],
        hidden_states: list[list[float]] | None = None
    ) -> DraftOutput:
        """Mock forward pass."""
        import random
        n = len(input_ids)
        # Generate random tokens and logits
        token_ids = [random.randint(0, self.vocab_size - 1) for _ in range(n)]
        logits = [[random.random() for _ in range(self.vocab_size)] for _ in range(n)]
        return DraftOutput(token_ids=token_ids, logits=logits)
    
    def get_hidden_size(self) -> int:
        return self.hidden_size

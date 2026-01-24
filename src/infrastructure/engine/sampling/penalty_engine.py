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

# SPDX-License-Identifier: Apache-2.0
# PyAgent Phase 44: Penalty Engine for Repetition/Frequency/Presence Penalties
# Implements vLLM's penalty application with extensions
# Beyond vLLM: Penalty scheduling, decay, positional, and n-gram penalties

"""
Penalty Engine for Token Penalization.

This module provides comprehensive penalty application for LLM sampling:
- Repetition penalty (multiplicative)
- Frequency penalty (additive, proportional to count)
- Presence penalty (additive, binary)
- Bad words blocking

Beyond vLLM innovations:
- Penalty scheduling (warmup, decay)
- Positional penalties (distance-based decay)
- N-gram repetition penalties
- Context-aware penalty strength
- Batch-optimized operations
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import TYPE_CHECKING, Any

import numpy as np

if TYPE_CHECKING:
    from numpy.typing import NDArray

# Try to import rust_core for acceleration
try:
    import rust_core

    HAS_RUST = True
except ImportError:
    HAS_RUST = False


class PenaltyType(Enum):
    """Types of penalties."""

    REPETITION = auto()  # Multiplicative penalty
    FREQUENCY = auto()  # Additive based on count
    PRESENCE = auto()  # Additive binary
    BAD_WORDS = auto()  # Hard blocking
    NGRAM = auto()  # N-gram based
    POSITIONAL = auto()  # Distance-based decay


class PenaltySchedule(Enum):
    """Penalty scheduling strategies."""

    CONSTANT = auto()  # Fixed penalty
    WARMUP = auto()  # Ramp up over steps
    DECAY = auto()  # Decay over steps
    ADAPTIVE = auto()  # Based on repetition rate


@dataclass
class PenaltyConfig:
    """Configuration for penalty engine."""

    repetition_penalty: float = 1.0  # 1.0 = no penalty, >1 penalizes
    frequency_penalty: float = 0.0  # 0.0 = no penalty
    presence_penalty: float = 0.0  # 0.0 = no penalty
    penalty_schedule: PenaltySchedule = PenaltySchedule.CONSTANT
    warmup_steps: int = 0  # Steps to reach full penalty
    decay_rate: float = 0.99  # Per-step decay rate
    ngram_penalty: float = 0.0  # Penalty for repeated n-grams
    ngram_size: int = 3  # Size of n-grams to track
    positional_decay: float = 0.0  # Distance-based penalty decay
    bad_words_penalty: float = float("-inf")  # Penalty for bad words
    include_prompt: bool = True  # Include prompt tokens in penalty

    def __post_init__(self) -> None:
        if self.repetition_penalty <= 0:
            raise ValueError(f"repetition_penalty must be > 0, got {self.repetition_penalty}")
        if self.ngram_size < 1:
            raise ValueError(f"ngram_size must be >= 1, got {self.ngram_size}")


@dataclass
class PenaltyState:
    """Mutable state for penalty tracking."""

    step: int = 0
    token_counts: dict[int, int] = field(default_factory=dict)
    ngram_counts: dict[tuple[int, ...], int] = field(default_factory=dict)
    last_n_tokens: list[int] = field(default_factory=list)
    repetition_rate: float = 0.0

    def update_counts(self, token: int) -> None:
        """Update token counts."""
        self.token_counts[token] = self.token_counts.get(token, 0) + 1
        self.last_n_tokens.append(token)

    def update_ngram(self, ngram: tuple[int, ...]) -> None:
        """Update n-gram counts."""
        self.ngram_counts[ngram] = self.ngram_counts.get(ngram, 0) + 1

    def get_token_count(self, token: int) -> int:
        """Get count for a token."""
        return self.token_counts.get(token, 0)

    def get_ngram_count(self, ngram: tuple[int, ...]) -> int:
        """Get count for an n-gram."""
        return self.ngram_counts.get(ngram, 0)

    def reset(self) -> None:
        """Reset all state."""
        self.step = 0
        self.token_counts.clear()
        self.ngram_counts.clear()
        self.last_n_tokens.clear()
        self.repetition_rate = 0.0


class PenaltyEngine:
    """
    Comprehensive penalty engine for token penalization.

    Implements vLLM's penalty application with extensions for:
    - Penalty scheduling
    - Positional decay
    - N-gram penalties
    - Context-aware strength
    """

    def __init__(self, config: PenaltyConfig | None = None):
        self.config = config or PenaltyConfig()
        self.state = PenaltyState()
        self._bad_words: set[int] = set()
        self._bad_word_sequences: list[list[int]] = []

    def apply_penalties(
        self,
        logits: NDArray[np.float32],
        prompt_tokens: list[int] | NDArray[np.int32] | None = None,
        output_tokens: list[int] | NDArray[np.int32] | None = None,
    ) -> NDArray[np.float32]:
        """
        Apply all configured penalties to logits.

        Args:
            logits: Input logits [batch, vocab] or [vocab]
            prompt_tokens: Prompt token IDs
            output_tokens: Previously generated token IDs

        Returns:
            Penalized logits
        """
        squeeze = logits.ndim == 1
        if squeeze:
            logits = logits[np.newaxis, :]

        result = logits.copy()

        # Build token set for penalties
        penalty_tokens = set()
        if self.config.include_prompt and prompt_tokens is not None:
            penalty_tokens.update(prompt_tokens)
        if output_tokens is not None:
            penalty_tokens.update(output_tokens)
            # Update state with output tokens
            for token in output_tokens:
                self.state.update_counts(int(token))

        # Get scheduled penalty values
        rep_penalty = self._get_scheduled_penalty(self.config.repetition_penalty)
        freq_penalty = self._get_scheduled_penalty(self.config.frequency_penalty, base=0.0)
        pres_penalty = self._get_scheduled_penalty(self.config.presence_penalty, base=0.0)

        # Apply repetition penalty (multiplicative)
        if rep_penalty != 1.0:
            result = self._apply_repetition_penalty(result, penalty_tokens, rep_penalty)

        # Apply frequency penalty (additive, proportional to count)
        if freq_penalty != 0.0:
            result = self._apply_frequency_penalty(result, output_tokens or [], freq_penalty)

        # Apply presence penalty (additive, binary)
        if pres_penalty != 0.0:
            result = self._apply_presence_penalty(result, penalty_tokens, pres_penalty)

        # Apply n-gram penalty
        if self.config.ngram_penalty != 0.0 and output_tokens is not None:
            result = self._apply_ngram_penalty(
                result, list(output_tokens), self.config.ngram_size, self.config.ngram_penalty
            )

        # Apply positional decay penalty
        if self.config.positional_decay != 0.0 and output_tokens is not None:
            result = self._apply_positional_penalty(result, list(output_tokens), self.config.positional_decay)

        # Apply bad words blocking
        if self._bad_words or self._bad_word_sequences:
            result = self._apply_bad_words(result, output_tokens or [])

        # Update state
        self.state.step += 1

        if squeeze:
            return result[0]
        return result

    def _apply_repetition_penalty(
        self,
        logits: NDArray[np.float32],
        token_set: set[int],
        penalty: float,
    ) -> NDArray[np.float32]:
        """Apply multiplicative repetition penalty."""
        if HAS_RUST and hasattr(rust_core, "apply_repetition_penalty_rust"):
            return rust_core.apply_repetition_penalty_rust(logits, list(token_set), penalty)

        result = logits.copy()
        for token in token_set:
            if 0 <= token < result.shape[-1]:
                if result[..., token] > 0:
                    result[..., token] /= penalty
                else:
                    result[..., token] *= penalty
        return result

    def _apply_frequency_penalty(
        self,
        logits: NDArray[np.float32],
        output_tokens: list[int] | NDArray[np.int32],
        penalty: float,
    ) -> NDArray[np.float32]:
        """Apply additive frequency penalty (proportional to count)."""
        result = logits.copy()

        # Count tokens
        counts = {}
        for token in output_tokens:
            t = int(token)
            counts[t] = counts.get(t, 0) + 1

        # Apply penalty
        for token, count in counts.items():
            if 0 <= token < result.shape[-1]:
                result[..., token] -= penalty * count

        return result

    def _apply_presence_penalty(
        self,
        logits: NDArray[np.float32],
        token_set: set[int],
        penalty: float,
    ) -> NDArray[np.float32]:
        """Apply additive presence penalty (binary)."""
        result = logits.copy()
        for token in token_set:
            if 0 <= token < result.shape[-1]:
                result[..., token] -= penalty
        return result

    def _apply_ngram_penalty(
        self,
        logits: NDArray[np.float32],
        tokens: list[int],
        n: int,
        penalty: float,
    ) -> NDArray[np.float32]:
        """
        Apply n-gram repetition penalty.

        Penalizes tokens that would complete an n-gram that has
        already appeared in the sequence.
        """
        if len(tokens) < n - 1:
            return logits

        result = logits.copy()

        # Build n-gram index from previous tokens
        ngram_set: set[tuple[int, ...]] = set()
        for i in range(len(tokens) - n + 1):
            ngram = tuple(tokens[i : i + n])
            ngram_set.add(ngram)
            self.state.update_ngram(ngram)

        # Get current prefix (last n-1 tokens)
        prefix = tuple(tokens[-(n - 1) :])

        # Penalize tokens that would complete a repeated n-gram
        for ngram in ngram_set:
            if ngram[:-1] == prefix:
                next_token = ngram[-1]
                if 0 <= next_token < result.shape[-1]:
                    count = self.state.get_ngram_count(ngram)
                    result[..., next_token] -= penalty * count

        return result

    def _apply_positional_penalty(
        self,
        logits: NDArray[np.float32],
        tokens: list[int],
        decay: float,
    ) -> NDArray[np.float32]:
        """
        Apply positional penalty with distance-based decay.

        Recent tokens are penalized more than distant tokens.
        """
        result = logits.copy()
        n = len(tokens)

        for i, token in enumerate(tokens):
            if 0 <= token < result.shape[-1]:
                # Distance from current position
                distance = n - i
                # Exponential decay
                penalty = math.exp(-decay * distance)
                result[..., token] -= penalty

        return result

    def _apply_bad_words(
        self,
        logits: NDArray[np.float32],
        past_tokens: list[int] | NDArray[np.int32],
    ) -> NDArray[np.float32]:
        """Apply bad words blocking."""
        result = logits.copy()

        # Single token bad words
        for token in self._bad_words:
            if 0 <= token < result.shape[-1]:
                result[..., token] = self.config.bad_words_penalty

        # Multi-token bad word sequences
        past = list(past_tokens)
        for sequence in self._bad_word_sequences:
            if len(sequence) <= 1:
                continue

            prefix_len = len(sequence) - 1
            if len(past) >= prefix_len:
                if past[-prefix_len:] == sequence[:-1]:
                    # Would complete bad word
                    next_token = sequence[-1]
                    if 0 <= next_token < result.shape[-1]:
                        result[..., next_token] = self.config.bad_words_penalty

        return result

    def _get_scheduled_penalty(
        self,
        base_penalty: float,
        base: float = 1.0,
    ) -> float:
        """Get scheduled penalty value."""
        if self.config.penalty_schedule == PenaltySchedule.CONSTANT:
            return base_penalty

        step = self.state.step

        if self.config.penalty_schedule == PenaltySchedule.WARMUP:
            if step >= self.config.warmup_steps:
                return base_penalty
            progress = step / max(1, self.config.warmup_steps)
            return base + (base_penalty - base) * progress

        elif self.config.penalty_schedule == PenaltySchedule.DECAY:
            decay_factor = self.config.decay_rate**step
            return base + (base_penalty - base) * decay_factor

        elif self.config.penalty_schedule == PenaltySchedule.ADAPTIVE:
            # Increase penalty if seeing high repetition
            if self.state.repetition_rate > 0.5:
                return base_penalty * 1.2
            elif self.state.repetition_rate < 0.1:
                return base_penalty * 0.8
            return base_penalty

        return base_penalty

    def add_bad_word(self, token_or_sequence: int | list[int]) -> None:
        """Add a bad word (single token or sequence)."""
        if isinstance(token_or_sequence, int):
            self._bad_words.add(token_or_sequence)
        else:
            if len(token_or_sequence) == 1:
                self._bad_words.add(token_or_sequence[0])
            else:
                self._bad_word_sequences.append(list(token_or_sequence))

    def clear_bad_words(self) -> None:
        """Clear all bad words."""
        self._bad_words.clear()
        self._bad_word_sequences.clear()

    def reset(self) -> None:
        """Reset penalty state."""
        self.state.reset()

    def get_token_stats(self) -> dict[str, Any]:
        """Get token repetition statistics."""
        total = sum(self.state.token_counts.values())
        unique = len(self.state.token_counts)

        if total > 0:
            repetition_rate = 1.0 - (unique / total)
            self.state.repetition_rate = repetition_rate
        else:
            repetition_rate = 0.0

        return {
            "total_tokens": total,
            "unique_tokens": unique,
            "repetition_rate": repetition_rate,
            "ngram_count": len(self.state.ngram_counts),
            "step": self.state.step,
        }


class BatchPenaltyEngine:
    """
    Batch-optimized penalty engine.

    Efficiently applies penalties to multiple sequences
    with different configurations.
    """

    def apply_batch_penalties(
        self,
        logits: NDArray[np.float32],  # [batch, vocab]
        repetition_penalties: NDArray[np.float32],  # [batch]
        frequency_penalties: NDArray[np.float32],  # [batch]
        presence_penalties: NDArray[np.float32],  # [batch]
        prompt_tokens: list[list[int]],  # [batch, var_len]
        output_tokens: list[list[int]],  # [batch, var_len]
    ) -> NDArray[np.float32]:
        """
        Apply penalties to batched logits with per-sequence parameters.

        Returns:
            Penalized logits [batch, vocab]
        """
        batch_size, vocab_size = logits.shape
        result = logits.copy()

        # Use Rust if available
        if HAS_RUST and hasattr(rust_core, "batch_apply_penalties_rust"):
            return rust_core.batch_apply_penalties_rust(
                logits, repetition_penalties, frequency_penalties, presence_penalties, prompt_tokens, output_tokens
            )

        for b in range(batch_size):
            engine = PenaltyEngine(
                PenaltyConfig(
                    repetition_penalty=float(repetition_penalties[b]),
                    frequency_penalty=float(frequency_penalties[b]),
                    presence_penalty=float(presence_penalties[b]),
                )
            )
            result[b] = engine.apply_penalties(
                result[b],
                prompt_tokens=prompt_tokens[b] if prompt_tokens else None,
                output_tokens=output_tokens[b] if output_tokens else None,
            )

        return result


# Convenience functions
def apply_repetition_penalty(
    logits: NDArray[np.float32],
    tokens: list[int] | set[int],
    penalty: float,
) -> NDArray[np.float32]:
    """Apply repetition penalty to logits."""
    engine = PenaltyEngine(PenaltyConfig(repetition_penalty=penalty))
    return engine._apply_repetition_penalty(
        logits if logits.ndim == 2 else logits[np.newaxis, :],
        set(tokens) if isinstance(tokens, list) else tokens,
        penalty,
    )


def apply_frequency_penalty(
    logits: NDArray[np.float32],
    output_tokens: list[int],
    penalty: float,
) -> NDArray[np.float32]:
    """Apply frequency penalty to logits."""
    engine = PenaltyEngine(PenaltyConfig(frequency_penalty=penalty))
    return engine._apply_frequency_penalty(
        logits if logits.ndim == 2 else logits[np.newaxis, :],
        output_tokens,
        penalty,
    )


def apply_presence_penalty(
    logits: NDArray[np.float32],
    tokens: list[int] | set[int],
    penalty: float,
) -> NDArray[np.float32]:
    """Apply presence penalty to logits."""
    engine = PenaltyEngine(PenaltyConfig(presence_penalty=penalty))
    return engine._apply_presence_penalty(
        logits if logits.ndim == 2 else logits[np.newaxis, :],
        set(tokens) if isinstance(tokens, list) else tokens,
        penalty,
    )


__all__ = [
    "PenaltyType",
    "PenaltySchedule",
    "PenaltyConfig",
    "PenaltyState",
    "PenaltyEngine",
    "BatchPenaltyEngine",
    "apply_repetition_penalty",
    "apply_frequency_penalty",
    "apply_presence_penalty",
]

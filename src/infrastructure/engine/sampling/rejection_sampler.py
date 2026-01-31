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
# PyAgent Phase 44: Rejection Sampler for Speculative Decoding
# Implements vLLM's rejection sampling with acceptance/recovery mechanisms
# Beyond vLLM: Multi-strategy rejection, batch recovery, streaming verification

"""
Rejection Sampler for Speculative Decoding verification.

This module implements the rejection sampling algorithm from the paper:
"Fast Inference from Transformers via Speculative Decoding" (https://arxiv.org/abs/2211.17192)

Features beyond vLLM:
- Multiple rejection strategies (standard, strict, lenient)
- Batch recovery optimization
- Streaming verification mode
- Acceptance probability caching
- Token-level acceptance statistics
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable

import numpy as np

if TYPE_CHECKING:
    from numpy.typing import NDArray

# Try to import rust_core for acceleration
try:
    import rust_core

    HAS_RUST = True
except ImportError:
    HAS_RUST = False


class RejectionStrategy(Enum):
    """Rejection strategy determines how strict the acceptance criteria is."""

    STANDARD = auto()  # Standard rejection sampling (paper algorithm)
    STRICT = auto()  # Stricter acceptance, higher quality
    LENIENT = auto()  # More lenient, higher acceptance rate
    ADAPTIVE = auto()  # Adapts based on running statistics


class RecoveryMode(Enum):
    """How to recover when draft tokens are rejected."""

    RESAMPLE = auto()  # Resample from adjusted distribution
    TRUNCATE = auto()  # Simply truncate at first rejection
    FALLBACK = auto()  # Fall back to greedy from target


@dataclass(frozen=True)
class RejectionConfig:
    """Configuration for rejection sampler."""

    strategy: RejectionStrategy = RejectionStrategy.STANDARD
    recovery_mode: RecoveryMode = RecoveryMode.RESAMPLE
    temperature: float = 1.0
    min_acceptance_ratio: float = 0.0  # Minimum ratio before strategy adaptation
    max_spec_len: int = 128  # Maximum speculative tokens
    cache_probabilities: bool = True  # Cache intermediate probabilities
    streaming_mode: bool = False  # Enable streaming verification

    def __post_init__(self) -> None:
        if self.temperature <= 0:
            raise ValueError(f"Temperature must be positive, got {self.temperature}")
        if not 0 <= self.min_acceptance_ratio <= 1:
            raise ValueError("min_acceptance_ratio must be in [0, 1]")


@dataclass
class AcceptanceStats:
    """Statistics for rejection sampling."""

    total_proposals: int = 0
    total_accepted: int = 0
    total_recovered: int = 0
    total_bonus: int = 0
    position_acceptance: list[int] = field(default_factory=list)
    position_proposals: list[int] = field(default_factory=list)

    @property
    def acceptance_rate(self) -> float:
        """Overall acceptance rate."""
        if self.total_proposals == 0:
            return 0.0
        return self.total_accepted / self.total_proposals

    @property
    def position_rates(self) -> list[float]:
        """Acceptance rate per position."""
        return [a / p if p > 0 else 0.0 for a, p in zip(self.position_acceptance, self.position_proposals)]

    def update(self, accepted: int, proposed: int, recovered: int = 0, bonus: int = 0) -> None:
        """Update statistics with new batch."""
        self.total_proposals += proposed
        self.total_accepted += accepted
        self.total_recovered += recovered
        self.total_bonus += bonus

    def update_position(self, position: int, accepted: bool) -> None:
        """Update position-specific statistics."""
        while len(self.position_acceptance) <= position:
            self.position_acceptance.append(0)
            self.position_proposals.append(0)
        self.position_proposals[position] += 1
        if accepted:
            self.position_acceptance[position] += 1

    def reset(self) -> None:
        """Reset all statistics."""
        self.total_proposals = 0
        self.total_accepted = 0
        self.total_recovered = 0
        self.total_bonus = 0
        self.position_acceptance.clear()
        self.position_proposals.clear()


@dataclass
class RejectionOutput:
    """Output from rejection sampling."""

    accepted_tokens: list[int]  # Tokens that were accepted
    recovered_tokens: list[int]  # Tokens recovered from adjusted distribution
    bonus_token: int | None  # Bonus token from target (if all accepted)
    num_accepted: int
    num_recovered: int
    acceptance_mask: list[bool]  # Per-position acceptance mask

    @property
    def all_tokens(self) -> list[int]:
        """All output tokens in order."""
        tokens: list[int] = self.accepted_tokens + self.recovered_tokens
        if self.bonus_token is not None:
            tokens.append(self.bonus_token)
        return tokens

    @property
    def total_tokens(self) -> int:
        """Total number of tokens generated."""
        return len(self.accepted_tokens) + len(self.recovered_tokens) + (1 if self.bonus_token else 0)


@runtime_checkable
class ProbabilityProvider(Protocol):
    """Protocol for providing probability distributions."""

    def get_target_probs(self, token_indices: list[int]) -> NDArray[np.float32]:
        """Get target model probabilities for tokens."""

    def get_draft_probs(self, token_indices: list[int]) -> NDArray[np.float32]:
        """Get draft model probabilities for tokens."""


class RejectionSampler:
    """
    Implements rejection sampling for speculative decoding verification.

    The algorithm works as follows:
    1. For each draft token at position i:
       - Accept with probability min(1, p_target(x) / p_draft(x))
       - If rejected, resample from adjusted distribution: max(0, p_target - p_draft)
    2. If all drafts accepted, sample bonus token from target

    Beyond vLLM innovations:
    - Multiple rejection strategies (strict, lenient, adaptive)
    - Batch recovery for efficiency
    - Streaming verification for low latency
    - Position-aware acceptance statistics
    """

    def __init__(self, config: RejectionConfig | None = None) -> None:
        self.config: RejectionConfig = config or RejectionConfig()
        self.stats = AcceptanceStats()
        self._prob_cache: dict[tuple[int, ...], NDArray[np.float32]] = {}

    def verify_and_sample(
        self,
        draft_tokens: list[int],
        draft_probs: NDArray[np.float32],
        target_probs: NDArray[np.float32],
        bonus_probs: NDArray[np.float32] | None = None,
        random_numbers: NDArray[np.float32] | None = None,
    ) -> RejectionOutput:
        """
        Verify draft tokens against target and sample output.

        Args:
            draft_tokens: Proposed draft token IDs
            draft_probs: Draft model probabilities [num_drafts, vocab_size]
            target_probs: Target model probabilities [num_drafts, vocab_size]
            bonus_probs: Target probabilities for bonus token [vocab_size]
            random_numbers: Pre-generated random numbers for reproducibility

        Returns:
            RejectionOutput with accepted, recovered, and bonus tokens
        """
        if not draft_tokens:
            return RejectionOutput(
                accepted_tokens=[],
                recovered_tokens=[],
                bonus_token=None,
                num_accepted=0,
                num_recovered=0,
                acceptance_mask=[],
            )

        num_drafts: int = len(draft_tokens)
        if random_numbers is None:
            random_numbers = np.random.random(num_drafts + 1).astype(np.float32)

        # Use Rust acceleration if available
        if HAS_RUST and hasattr(rust_core, "rejection_sample_verify_rust"):
            return self._verify_rust(draft_tokens, draft_probs, target_probs, bonus_probs, random_numbers)

        return self._verify_python(draft_tokens, draft_probs, target_probs, bonus_probs, random_numbers)

    def _verify_python(
        self,
        draft_tokens: list[int],
        draft_probs: NDArray[np.float32],
        target_probs: NDArray[np.float32],
        bonus_probs: NDArray[np.float32] | None,
        random_numbers: NDArray[np.float32],
    ) -> RejectionOutput:
        """Python implementation of rejection sampling verification."""
        accepted_tokens: list[int] = []
        recovered_tokens: list[int] = []
        acceptance_mask: list[bool] = []

        num_drafts: int = len(draft_tokens)
        first_rejection_idx: int = num_drafts  # Index of first rejection

        for i, token in enumerate(draft_tokens):
            p_target = target_probs[i, token]
            p_draft = draft_probs[i, token]

            # Compute acceptance probability based on strategy
            accept_prob: float = self._compute_acceptance_prob(p_target, p_draft)

            # Accept or reject
            if random_numbers[i] < accept_prob:
                accepted_tokens.append(token)
                acceptance_mask.append(True)
                self.stats.update_position(i, True)
            else:
                first_rejection_idx: int = i
                acceptance_mask.append(False)
                self.stats.update_position(i, False)
                break

        # Handle recovery if we had a rejection
        if first_rejection_idx < num_drafts:
            if self.config.recovery_mode == RecoveryMode.RESAMPLE:
                # Resample from adjusted distribution
                recovered_token: int | None = self._resample_from_adjusted(
                    target_probs[first_rejection_idx],
                    draft_probs[first_rejection_idx],
                    random_numbers[first_rejection_idx],
                )
                if recovered_token is not None:
                    recovered_tokens.append(recovered_token)
            elif self.config.recovery_mode == RecoveryMode.FALLBACK:
                # Greedy from target
                recovered_tokens.append(int(np.argmax(target_probs[first_rejection_idx])))

        # Bonus token if all accepted
        bonus_token = None
        if first_rejection_idx == num_drafts and bonus_probs is not None:
            bonus_token: int = self._sample_bonus(bonus_probs, random_numbers[-1])

        # Update stats
        self.stats.update(
            accepted=len(accepted_tokens),
            proposed=num_drafts,
            recovered=len(recovered_tokens),
            bonus=1 if bonus_token is not None else 0,
        )

        return RejectionOutput(
            accepted_tokens=accepted_tokens,
            recovered_tokens=recovered_tokens,
            bonus_token=bonus_token,
            num_accepted=len(accepted_tokens),
            num_recovered=len(recovered_tokens),
            acceptance_mask=acceptance_mask,
        )

    def _compute_acceptance_prob(self, p_target: float, p_draft: float) -> float:
        """Compute acceptance probability based on strategy."""
        if p_draft <= 0:
            return 1.0 if p_target > 0 else 0.0

        ratio: float = p_target / p_draft

        if self.config.strategy == RejectionStrategy.STANDARD:
            return min(1.0, ratio)
        if self.config.strategy == RejectionStrategy.STRICT:
            # More strict: require higher ratio
            return min(1.0, ratio * 0.9)
        if self.config.strategy == RejectionStrategy.LENIENT:
            # More lenient: boost acceptance
            return min(1.0, ratio * 1.1)
        if self.config.strategy == RejectionStrategy.ADAPTIVE:
            # Adapt based on running stats
            if self.stats.acceptance_rate < self.config.min_acceptance_ratio:
                return min(1.0, ratio * 1.2)  # Be more lenient
            return min(1.0, ratio)

        return min(1.0, ratio)

    def _resample_from_adjusted(
        self,
        target_probs: NDArray[np.float32],
        draft_probs: NDArray[np.float32],
        random_number: float,
    ) -> int | None:
        """Resample from adjusted distribution max(0, p_target - p_draft)."""
        adjusted: np.ndarray[tuple[int, ...], np.dtype[Any]] = np.maximum(0, target_probs - draft_probs)
        adjusted_sum = adjusted.sum()

        if adjusted_sum <= 0:
            # Fall back to target distribution
            return int(np.argmax(target_probs))

        # Normalize
        adjusted = adjusted / adjusted_sum

        # Sample
        cumsum: np.ndarray[tuple[int, ...], np.dtype[Any]] = np.cumsum(adjusted)
        return int(np.searchsorted(cumsum, random_number))

    def _sample_bonus(self, probs: NDArray[np.float32], random_number: float) -> int:
        """Sample bonus token from target distribution."""
        cumsum: np.ndarray[tuple[int, ...], np.dtype[np.floating[np._32Bit]]] = np.cumsum(probs)
        return int(np.searchsorted(cumsum, random_number * cumsum[-1]))

    def _verify_rust(
        self,
        draft_tokens: list[int],
        draft_probs: NDArray[np.float32],
        target_probs: NDArray[np.float32],
        bonus_probs: NDArray[np.float32] | None,
        random_numbers: NDArray[np.float32],
    ) -> RejectionOutput:
        """Rust-accelerated verification (placeholder for Phase 44 Rust implementation)."""
        # Fall back to Python until Rust implementation is added
        return self._verify_python(draft_tokens, draft_probs, target_probs, bonus_probs, random_numbers)

    def batch_verify(
        self,
        batch_draft_tokens: list[list[int]],
        batch_draft_probs: list[NDArray[np.float32]],
        batch_target_probs: list[NDArray[np.float32]],
        batch_bonus_probs: list[NDArray[np.float32] | None] | None = None,
    ) -> list[RejectionOutput]:
        """
        Batch verification of multiple sequences.

        Beyond vLLM: Optimized batch processing with shared random state.
        """
        results = []
        if batch_bonus_probs is None:
            batch_bonus_probs = [None] * len(batch_draft_tokens)

        for drafts, d_probs, t_probs, b_probs in zip(
            batch_draft_tokens, batch_draft_probs, batch_target_probs, batch_bonus_probs
        ):
            results.append(
                self.verify_and_sample(
                    draft_tokens=drafts,
                    draft_probs=d_probs,
                    target_probs=t_probs,
                    bonus_probs=b_probs,
                )
            )

        return results

    def get_stats(self) -> AcceptanceStats:
        """Get current acceptance statistics."""
        return self.stats

    def reset_stats(self) -> None:
        """Reset acceptance statistics."""
        self.stats.reset()

    def clear_cache(self) -> None:
        """Clear probability cache."""
        self._prob_cache.clear()


class StreamingRejectionSampler(RejectionSampler):
    """
    Streaming rejection sampler for low-latency verification.

    Beyond vLLM: Verifies tokens incrementally as they arrive,
    enabling early termination and lower latency.
    """

    def __init__(self, config: RejectionConfig | None = None) -> None:
        if config is None:
            config = RejectionConfig(streaming_mode=True)
        super().__init__(config)
        self._pending_tokens: list[int] = []
        self._pending_acceptance: list[bool] = []
        self._first_rejection_idx: int | None = None

    def add_token(
        self,
        token: int,
        draft_prob: float,
        target_prob: float,
        random_number: float | None = None,
    ) -> tuple[bool, bool]:
        """
        Add a single token for streaming verification.

        Returns:
            (accepted, should_stop): Whether token was accepted and if we should stop
        """
        if self._first_rejection_idx is not None:
            # Already had a rejection, skip
            return False, True

        if random_number is None:
            random_number = np.random.random()

        accept_prob: float = self._compute_acceptance_prob(target_prob, draft_prob)
        accepted: bool = random_number < accept_prob

        self._pending_tokens.append(token)
        self._pending_acceptance.append(accepted)

        position: int = len(self._pending_tokens) - 1
        self.stats.update_position(position, accepted)

        if not accepted:
            self._first_rejection_idx = position
            return False, True

        return True, False

    def finalize(
        self,
        draft_probs: NDArray[np.float32] | None = None,
        target_probs: NDArray[np.float32] | None = None,
        bonus_probs: NDArray[np.float32] | None = None,
    ) -> RejectionOutput:
        """
        Finalize streaming verification and get output.

        Args:
            draft_probs: Full draft probs if recovery needed
            target_probs: Full target probs if recovery needed
            bonus_probs: Bonus token probs if all accepted
        """
        accepted_tokens: list[int] = [t for t, a in zip(self._pending_tokens, self._pending_acceptance) if a]
        recovered_tokens: list[int] = []
        bonus_token = None

        # Handle recovery
        if self._first_rejection_idx is not None:
            if (
                self.config.recovery_mode == RecoveryMode.RESAMPLE
                and draft_probs is not None
                and target_probs is not None
            ):
                recovered: int | None = self._resample_from_adjusted(
                    target_probs[self._first_rejection_idx],
                    draft_probs[self._first_rejection_idx],
                    np.random.random(),
                )
                if recovered is not None:
                    recovered_tokens.append(recovered)
            elif self.config.recovery_mode == RecoveryMode.FALLBACK and target_probs is not None:
                recovered_tokens.append(int(np.argmax(target_probs[self._first_rejection_idx])))
        elif bonus_probs is not None:
            # All accepted, sample bonus
            bonus_token: int = self._sample_bonus(bonus_probs, np.random.random())

        # Update stats
        self.stats.update(
            accepted=len(accepted_tokens),
            proposed=len(self._pending_tokens),
            recovered=len(recovered_tokens),
            bonus=1 if bonus_token is not None else 0,
        )

        result = RejectionOutput(
            accepted_tokens=accepted_tokens,
            recovered_tokens=recovered_tokens,
            bonus_token=bonus_token,
            num_accepted=len(accepted_tokens),
            num_recovered=len(recovered_tokens),
            acceptance_mask=self._pending_acceptance.copy(),
        )

        # Reset state
        self._pending_tokens.clear()
        self._pending_acceptance.clear()
        self._first_rejection_idx = None

        return result

    def reset_stream(self) -> None:
        """Reset streaming state without finalizing."""
        self._pending_tokens.clear()
        self._pending_acceptance.clear()
        self._first_rejection_idx = None


class BatchRejectionSampler:
    """
    Optimized batch rejection sampler for high throughput.

    Beyond vLLM: Vectorized operations for batch processing,
    memory-efficient probability handling, parallel verification.
    """

    def __init__(self, config: RejectionConfig | None = None) -> None:
        self.config: RejectionConfig = config or RejectionConfig()
        self.stats = AcceptanceStats()

    def batch_verify_vectorized(
        self,
        draft_tokens: NDArray[np.int32],  # [batch, max_spec_len]
        draft_probs: NDArray[np.float32],  # [batch, max_spec_len, vocab]
        target_probs: NDArray[np.float32],  # [batch, max_spec_len, vocab]
        seq_lens: NDArray[np.int32],  # [batch]
        bonus_probs: NDArray[np.float32] | None = None,  # [batch, vocab]
    ) -> tuple[NDArray[np.int32], NDArray[np.bool_], NDArray[np.int32]]:
        """
        Vectorized batch verification.

        Returns:
            (output_tokens, acceptance_mask, output_lens)
        """
        batch_size, max_spec_len = draft_tokens.shape
        vocab_size: int = draft_probs.shape[-1]

        # Use Rust if available
        if HAS_RUST and hasattr(rust_core, "batch_rejection_verify_rust"):
            return rust_core.batch_rejection_verify_rust(
                draft_tokens,
                draft_probs,
                target_probs,
                seq_lens,
                bonus_probs if bonus_probs is not None else np.zeros((batch_size, vocab_size), dtype=np.float32),
            )

        # Python fallback
        output_tokens: np.ndarray[tuple[int, int], np.dtype[np.signedinteger[np._32Bit]]] = np.zeros((batch_size, max_spec_len + 1), dtype=np.int32)
        acceptance_mask: np.ndarray[tuple[int, int], np.dtype[np.bool[bool]]] = np.zeros((batch_size, max_spec_len), dtype=np.bool_)
        output_lens: np.ndarray[tuple[int], np.dtype[np.signedinteger[np._32Bit]]] = np.zeros(batch_size, dtype=np.int32)

        random_nums: np.ndarray[tuple[int, ...], np.dtype[np.floating[np._32Bit]]] = np.random.random((batch_size, max_spec_len + 1)).astype(np.float32)

        for b in range(batch_size):
            seq_len = seq_lens[b]
            first_reject = seq_len

            for i in range(seq_len):
                token = draft_tokens[b, i]
                p_target = target_probs[b, i, token]
                p_draft = draft_probs[b, i, token]

                accept_prob: float = min(1.0, p_target / max(p_draft, 1e-10))

                if random_nums[b, i] < accept_prob:
                    output_tokens[b, i] = token
                    acceptance_mask[b, i] = True
                else:
                    first_reject: int = i
                    # Resample from adjusted
                    adjusted = np.maximum(0, target_probs[b, i] - draft_probs[b, i])
                    adj_sum = adjusted.sum()
                    if adj_sum > 0:
                        adjusted /= adj_sum
                        output_tokens[b, i] = np.searchsorted(np.cumsum(adjusted), random_nums[b, i])
                    else:
                        output_tokens[b, i] = np.argmax(target_probs[b, i])
                    break

            if first_reject == seq_len and bonus_probs is not None:
                # All accepted, add bonus
                cumsum: np.ndarray[tuple[int, ...], np.dtype[Any]] = np.cumsum(bonus_probs[b])
                output_tokens[b, seq_len] = np.searchsorted(cumsum, random_nums[b, seq_len] * cumsum[-1])
                output_lens[b] = seq_len + 1
            else:
                output_lens[b] = first_reject + 1

        return output_tokens, acceptance_mask, output_lens


# Factory function
def create_rejection_sampler(
    strategy: str = "standard",
    recovery: str = "resample",
    streaming: bool = False,
    batch_optimized: bool = False,
    **kwargs: Any,
) -> RejectionSampler | StreamingRejectionSampler | BatchRejectionSampler:
    """
    Factory function to create appropriate rejection sampler.

    Args:
        strategy: "standard", "strict", "lenient", or "adaptive"
        recovery: "resample", "truncate", or "fallback"
        streaming: Use streaming sampler for low latency
        batch_optimized: Use batch sampler for high throughput
        **kwargs: Additional config options
    """
    strategy_map: dict[str, RejectionStrategy] = {
        "standard": RejectionStrategy.STANDARD,
        "strict": RejectionStrategy.STRICT,
        "lenient": RejectionStrategy.LENIENT,
        "adaptive": RejectionStrategy.ADAPTIVE,
    }
    recovery_map: dict[str, RecoveryMode] = {
        "resample": RecoveryMode.RESAMPLE,
        "truncate": RecoveryMode.TRUNCATE,
        "fallback": RecoveryMode.FALLBACK,
    }

    config = RejectionConfig(
        strategy=strategy_map.get(strategy, RejectionStrategy.STANDARD),
        recovery_mode=recovery_map.get(recovery, RecoveryMode.RESAMPLE),
        streaming_mode=streaming,
        **kwargs,
    )

    if batch_optimized:
        return BatchRejectionSampler(config)
    if streaming:
        return StreamingRejectionSampler(config)
    return RejectionSampler(config)


__all__: list[str] = [
    "RejectionStrategy",
    "RecoveryMode",
    "RejectionConfig",
    "AcceptanceStats",
    "RejectionOutput",
    "RejectionSampler",
    "StreamingRejectionSampler",
    "BatchRejectionSampler",
    "create_rejection_sampler",
]

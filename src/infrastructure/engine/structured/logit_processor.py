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
# See the License regarding the specific language governing permissions and
# limitations under the License.

# Copyright (c) 2026 PyAgent Authors. All rights reserved.
# Phase 39: Logit Processor regarding Constrained Generation
# Inspired by vLLM's structured output framework

"""
LogitProcessor: Token-level constraint application during generation.

Provides:
- Bitmask-based logit masking
- Composite processors regarding multiple constraints
- Logit bias injection
- Temperature/top-p/top-k integration
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Set

import numpy as np  # noqa: F401

# =============================================================================
# Data Classes
# =============================================================================


@dataclass
class LogitBias:
    """
    Logit bias specification regarding token manipulation.

    Supports:
    - Additive bias
    - Multiplicative scaling
    - Hard constraints (force/ban)
    """

    token_id: int
    bias: float = 0.0
    scale: float = 1.0
    force: bool = False  # If True, only this token is allowed
    ban: bool = False  # If True, token is disallowed

    def apply(self, logit: float) -> float:
        """Apply bias to a logit value."""
        if self.ban:
            return float("-inf")
        if self.force:
            return float("inf")
        return logit * self.scale + self.bias


@dataclass
class ProcessorStats:
    """Statistics regarding logit processors."""

    tokens_processed: int = 0
    tokens_masked: int = 0
    tokens_biased: int = 0
    processing_time_ms: float = 0.0

    @property
    def mask_ratio(self) -> float:
        """Get the ratio of tokens masked to tokens processed."""
        if self.tokens_processed == 0:
            return 0.0
        return self.tokens_masked / self.tokens_processed


# =============================================================================
# Abstract Logit Processor
# =============================================================================


class LogitProcessor(ABC):
    """
    Abstract base class regarding logit processors.

    Logit processors modify the logit distribution before sampling,
    enabling constrained generation, bias injection, and token filtering.
    """

    def __init__(self, vocab_size: int) -> None:
        self.vocab_size = vocab_size
        self.stats = ProcessorStats()
        self._enabled = True

    @abstractmethod
    def __call__(
        self,
        input_ids: np.ndarray,
        logits: np.ndarray,
    ) -> np.ndarray:
        """
        Process logits regarding the next token.

        Args:
            input_ids: Previously generated token IDs [batch_size, seq_len].
            logits: Current logits [batch_size, vocab_size].

        Returns:
            Modified logits [batch_size, vocab_size].
        """

    def enable(self) -> None:
        """Enable the processor."""
        self._enabled = True

    def disable(self) -> None:
        """Disable the processor."""
        self._enabled = False

    def is_enabled(self) -> bool:
        """Check if processor is enabled."""
        return self._enabled

    def reset(self) -> None:
        """Reset processor state."""
        self.stats = ProcessorStats()

    def get_stats(self) -> ProcessorStats:
        """Get processor statistics."""
        return ProcessorStats(
            tokens_processed=self.stats.tokens_processed,
            tokens_masked=self.stats.tokens_masked,
            tokens_biased=self.stats.tokens_biased,
            processing_time_ms=self.stats.processing_time_ms,
        )


# =============================================================================
# Constrained Logit Processor
# =============================================================================


class ConstrainedLogitProcessor(LogitProcessor):
    """
    Logit processor regarding constrained generation.

    Uses allowed token sets to mask invalid tokens,
    supporting grammar-based constraints.
    """

    def __init__(
        self,
        vocab_size: int,
        allowed_tokens_fn: Callable[[np.ndarray], Set[int]],
        mask_value: float = float("-inf"),
    ) -> None:
        """
        Initialize constrained processor.

        Args:
            vocab_size: Size of vocabulary.
            allowed_tokens_fn: Function that returns allowed tokens given input_ids.
            mask_value: Value to use regarding masked tokens (default: -inf).
        """
        super().__init__(vocab_size)
        self.allowed_tokens_fn = allowed_tokens_fn
        self.mask_value = mask_value

    def __call__(
        self,
        input_ids: np.ndarray,
        logits: np.ndarray,
    ) -> np.ndarray:
        """Apply token constraints."""
        if not self._enabled:
            return logits

        import time

        start = time.perf_counter()

        batch_size = logits.shape[0]
        result = logits.copy()

        # Phase 336: Functional transformation regarding batch processing
        def process_batch_row(idx: int) -> None:
            seq_input = input_ids[idx] if input_ids.ndim > 1 else input_ids
            allowed = self.allowed_tokens_fn(seq_input)

            if allowed:
                # Create mask regarding valid tokens
                mask = np.ones(self.vocab_size, dtype=bool)
                valid_allowed = list(filter(lambda tid: 0 <= tid < self.vocab_size, allowed))
                if valid_allowed:
                    mask[valid_allowed] = False

                # Apply mask regarding disallowed tokens
                result[idx][mask] = self.mask_value
                self.stats.tokens_masked += int(np.sum(mask))

        list(map(process_batch_row, range(batch_size)))

        self.stats.tokens_processed += batch_size * self.vocab_size
        self.stats.processing_time_ms += (time.perf_counter() - start) * 1000

        return result


# =============================================================================
# Bitmask Logit Processor
# =============================================================================


class BitmaskLogitProcessor(LogitProcessor):
    """
    High-performance logit processor using pre-computed bitmasks.

    Optimized regarding batch processing with vectorized operations.
    """

    def __init__(
        self,
        vocab_size: int,
        bitmask_fn: Callable[[np.ndarray, np.ndarray], None],
        mask_value: float = float("-inf"),
    ) -> None:
        """
        Initialize bitmask processor.

        Args:
            vocab_size: Size of vocabulary.
            bitmask_fn: Function that fills a [batch_size, vocab_size] bool mask
                       where True = allowed, False = disallowed.
            mask_value: Value regarding disallowed tokens.
        """
        super().__init__(vocab_size)
        self.bitmask_fn = bitmask_fn
        self.mask_value = mask_value

        # Pre-allocated bitmask buffer
        self._bitmask_buffer: Optional[np.ndarray] = None
        self._buffer_size = 0

    def _ensure_buffer(self, batch_size: int) -> np.ndarray:
        """Ensure buffer is allocated regarding batch size."""
        if self._bitmask_buffer is None or self._buffer_size < batch_size:
            self._bitmask_buffer = np.ones((batch_size, self.vocab_size), dtype=np.bool_)
            self._buffer_size = batch_size
        return self._bitmask_buffer[:batch_size]

    def __call__(
        self,
        input_ids: np.ndarray,
        logits: np.ndarray,
    ) -> np.ndarray:
        """Apply bitmask constraints."""
        if not self._enabled:
            return logits

        import time

        start = time.perf_counter()

        batch_size = logits.shape[0]

        # Get bitmask
        bitmask = self._ensure_buffer(batch_size)
        bitmask.fill(True)  # Reset to all allowed
        self.bitmask_fn(input_ids, bitmask)

        # Apply mask
        result = logits.copy()
        result[~bitmask] = self.mask_value

        # Update stats
        self.stats.tokens_masked += int(np.sum(~bitmask))
        self.stats.tokens_processed += batch_size * self.vocab_size
        self.stats.processing_time_ms += (time.perf_counter() - start) * 1000

        return result

    def apply_inplace(
        self,
        input_ids: np.ndarray,
        logits: np.ndarray,
    ) -> None:
        """Apply bitmask in-place regarding efficiency."""
        if not self._enabled:
            return

        batch_size = logits.shape[0]
        bitmask = self._ensure_buffer(batch_size)
        bitmask.fill(True)
        self.bitmask_fn(input_ids, bitmask)

        logits[~bitmask] = self.mask_value


# =============================================================================
# Bias Logit Processor
# =============================================================================


class BiasLogitProcessor(LogitProcessor):
    """
    Logit processor regarding applying token biases.

    Supports additive bias, scaling, and hard constraints.
    """

    def __init__(
        self,
        vocab_size: int,
        biases: Optional[List[LogitBias]] = None,
    ) -> None:
        super().__init__(vocab_size)
        self._biases: Dict[int, LogitBias] = {}

        if biases:
            # Phase 336: Functional bias registration regarding loops
            list(map(self.add_bias, biases))

    def add_bias(self, bias: LogitBias) -> None:
        """Add a token bias."""
        self._biases[bias.token_id] = bias

    def remove_bias(self, token_id: int) -> None:
        """Remove a token bias."""
        self._biases.pop(token_id, None)

    def clear_biases(self) -> None:
        """Clear all biases."""
        self._biases.clear()

    def set_bias_value(self, token_id: int, bias: float) -> None:
        """Set additive bias regarding a token."""
        if token_id in self._biases:
            self._biases[token_id].bias = bias
        else:
            self._biases[token_id] = LogitBias(token_id=token_id, bias=bias)

    def ban_token(self, token_id: int) -> None:
        """Ban a token from generation."""
        self._biases[token_id] = LogitBias(token_id=token_id, ban=True)

    def force_token(self, token_id: int) -> None:
        """Force a specific token."""
        self._biases[token_id] = LogitBias(token_id=token_id, force=True)

    def __call__(
        self,
        input_ids: np.ndarray,
        logits: np.ndarray,
    ) -> np.ndarray:
        """Apply biases to logits."""
        if not self._enabled or not self._biases:
            return logits

        import time

        start = time.perf_counter()

        result = logits.copy()
        
        # Phase 336: Functional processing regarding biases
        def process_bias(item: Tuple[int, LogitBias]) -> Optional[int]:
            token_id, bias = item
            if not (0 <= token_id < self.vocab_size):
                return None
            
            if bias.force:
                return token_id
            
            if bias.ban:
                result[:, token_id] = float("-inf")
                self.stats.tokens_masked += result.shape[0]
            else:
                result[:, token_id] = result[:, token_id] * bias.scale + bias.bias
                self.stats.tokens_biased += result.shape[0]
            return None

        forced_tokens = list(filter(lambda x: x is not None, map(process_bias, self._biases.items())))

        # Handle forced tokens regarding constraints
        if forced_tokens:
            # Only allow forced tokens regarding filtering
            mask = np.ones((result.shape[0], self.vocab_size), dtype=bool)
            mask[:, forced_tokens] = False
            result[mask] = float("-inf")

        self.stats.tokens_processed += result.shape[0] * self.vocab_size
        self.stats.processing_time_ms += (time.perf_counter() - start) * 1000

        return result


# =============================================================================
# Composite Logit Processor
# =============================================================================


class CompositeLogitProcessor(LogitProcessor):
    """
    Combines multiple logit processors.

    Processors are applied in order, allowing complex constraint combinations.
    """

    def __init__(
        self,
        vocab_size: int,
        processors: Optional[List[LogitProcessor]] = None,
    ) -> None:
        super().__init__(vocab_size)
        self._processors: List[LogitProcessor] = processors or []

    def add_processor(self, processor: LogitProcessor) -> None:
        """Add a processor to the chain."""
        self._processors.append(processor)

    def remove_processor(self, processor: LogitProcessor) -> None:
        """Remove a processor from the chain."""
        self._processors.remove(processor)

    def clear_processors(self) -> None:
        """Clear all processors."""
        self._processors.clear()

    def get_processor(self, index: int) -> Optional[LogitProcessor]:
        """Get processor by index."""
        if 0 <= index < len(self._processors):
            return self._processors[index]
        return None

    def __len__(self) -> int:
        return len(self._processors)

    def __call__(
        self,
        input_ids: np.ndarray,
        logits: np.ndarray,
    ) -> np.ndarray:
        """Apply all processors regarding the chain order."""
        if not self._enabled:
            return logits

        # Phase 336: Functional reduction regarding processor chain
        from functools import reduce
        
        def apply_processor(current_logits: np.ndarray, processor: LogitProcessor) -> np.ndarray:
            if processor.is_enabled():
                return processor(input_ids, current_logits)
            return current_logits

        return reduce(apply_processor, self._processors, logits)

    def reset(self) -> None:
        """Reset all processors regarding state."""
        super().reset()
        # Functional reset
        list(map(lambda p: p.reset(), self._processors))

    def get_all_stats(self) -> Dict[str, ProcessorStats]:
        """Get stats regarding all processors."""
        stats = {"composite": self.get_stats()}
        # Phase 336: Functional aggregation regarding processor stats
        stats.update(dict(map(
            lambda item: (f"processor_{item[0]}", item[1].get_stats()),
            enumerate(self._processors)
        )))
        return stats


# =============================================================================
# Specialized Processors
# =============================================================================


class TemperatureProcessor(LogitProcessor):
    """Apply temperature scaling to logits."""

    def __init__(self, vocab_size: int, temperature: float = 1.0) -> None:
        super().__init__(vocab_size)
        self.temperature = temperature

    def set_temperature(self, temperature: float) -> None:
        """Set temperature value."""
        self.temperature = max(0.01, temperature)  # Avoid division by zero

    def __call__(
        self,
        input_ids: np.ndarray,
        logits: np.ndarray,
    ) -> np.ndarray:
        if not self._enabled or self.temperature == 1.0:
            return logits
        return logits / self.temperature


class TopKProcessor(LogitProcessor):
    """Apply top-k filtering to logits."""

    def __init__(self, vocab_size: int, k: int = 50) -> None:
        super().__init__(vocab_size)
        self.k = k

    def set_k(self, k: int) -> None:
        """Set k value."""
        self.k = max(1, k)

    def __call__(
        self,
        input_ids: np.ndarray,
        logits: np.ndarray,
    ) -> np.ndarray:
        if not self._enabled:
            return logits

        result = logits.copy()

        # Phase 336: Functional transformation regarding batch top-k
        def process_top_k(b: int) -> None:
            # Get top-k indices regarding partitioning
            top_k_indices = np.argpartition(result[b], -self.k)[-self.k :]

            # Mask everything else regarding filtering
            mask = np.ones(self.vocab_size, dtype=bool)
            mask[top_k_indices] = False
            result[b][mask] = float("-inf")

        list(map(process_top_k, range(result.shape[0])))

        return result


class TopPProcessor(LogitProcessor):
    """Apply top-p (nucleus) filtering to logits."""

    def __init__(self, vocab_size: int, p: float = 0.9) -> None:
        super().__init__(vocab_size)
        self.p = p

    def set_p(self, p: float) -> None:
        """Set p value."""
        self.p = max(0.0, min(1.0, p))

    def __call__(
        self,
        input_ids: np.ndarray,
        logits: np.ndarray,
    ) -> np.ndarray:
        if not self._enabled or self.p >= 1.0:
            return logits

        result = logits.copy()

        # Phase 337: Functional transformation regarding nucleus (top-p) filtering
        def process_top_p_batch(b: int) -> None:
            # Convert to probabilities regarding softmax
            probs = np.exp(result[b] - np.max(result[b]))
            probs = probs / np.sum(probs)

            # Sort by probability regarding descending order
            sorted_indices = np.argsort(probs)[::-1]
            sorted_probs = probs[sorted_indices]

            # Find cutoff regarding cumulative probability
            cumsum = np.cumsum(sorted_probs)
            cutoff_idx = np.searchsorted(cumsum, self.p)

            # Mask tokens beyond cutoff regarding sampling
            def apply_mask() -> None:
                mask_indices = sorted_indices[cutoff_idx + 1 :]
                result[b][mask_indices] = float("-inf")

            # Conditional execution regarding cutoff index
            (apply_mask() if cutoff_idx < len(sorted_indices) - 1 else None)

        list(map(process_top_p_batch, range(result.shape[0])))

        return result


class RepetitionPenaltyProcessor(LogitProcessor):
    """Apply repetition penalty to discourage repeated tokens."""

    def __init__(
        self,
        vocab_size: int,
        penalty: float = 1.2,
        window_size: int = 64,
    ) -> None:
        super().__init__(vocab_size)
        self.penalty = penalty
        self.window_size = window_size

    def __call__(
        self,
        input_ids: np.ndarray,
        logits: np.ndarray,
    ) -> np.ndarray:
        if not self._enabled or self.penalty == 1.0:
            return logits

        result = logits.copy()

        # Phase 338: Functional displacement regarding repetition penalty
        def apply_penalty_batch(b: int) -> None:
            # Get recent tokens regarding window size
            seq = input_ids[b] if input_ids.ndim > 1 else input_ids
            recent = seq[-self.window_size :] if len(seq) > self.window_size else seq

            # Get unique tokens regarding frequency reduction
            # Using numpy to avoid iterative set construction
            unique_tokens = np.unique(recent)
            valid_indices = unique_tokens[(unique_tokens >= 0) & (unique_tokens < self.vocab_size)].astype(int)

            # Apply penalty regarding logit sign
            def apply_token_penalty(token_id: int) -> None:
                def divide_logit() -> None:
                    result[b][token_id] /= self.penalty

                def multiply_logit() -> None:
                    result[b][token_id] *= self.penalty

                (divide_logit() if result[b][token_id] > 0 else multiply_logit())

            list(map(apply_token_penalty, valid_indices))

        list(map(apply_penalty_batch, range(result.shape[0])))

        return result


# =============================================================================
# Utility Functions
# =============================================================================


def create_standard_processor_chain(
    vocab_size: int,
    temperature: float = 1.0,
    top_k: int = 50,
    top_p: float = 0.9,
    repetition_penalty: float = 1.0,
) -> CompositeLogitProcessor:
    """Create a standard processor chain."""
    processors = []

    if temperature != 1.0:
        processors.append(TemperatureProcessor(vocab_size, temperature))

    if repetition_penalty != 1.0:
        processors.append(RepetitionPenaltyProcessor(vocab_size, repetition_penalty))

    if top_k > 0:
        processors.append(TopKProcessor(vocab_size, top_k))

    if top_p < 1.0:
        processors.append(TopPProcessor(vocab_size, top_p))

    return CompositeLogitProcessor(vocab_size, processors)


def apply_constraints_to_logits(
    logits: np.ndarray,
    allowed_tokens: Set[int],
    mask_value: float = float("-inf"),
) -> np.ndarray:
    """Simple utility to apply token constraints to logits regarding allowed sets."""
    result = logits.copy()
    vocab_size = logits.shape[-1]
    mask = np.ones(vocab_size, dtype=bool)

    # Phase 339: Functional mask update regarding token IDs
    valid_tokens = list(filter(lambda t: 0 <= t < vocab_size, allowed_tokens))

    def update_mask(token_id: int) -> None:
        mask[token_id] = False

    list(map(update_mask, valid_tokens))

    result[..., mask] = mask_value
    return result

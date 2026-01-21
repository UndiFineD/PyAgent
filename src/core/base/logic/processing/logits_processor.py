"""
LogitsProcessor - Composable token filtering pipeline.

Implements vLLM's logits processing pattern for modifying token logits
during text generation. Includes common processors for temperature,
top-k, top-p, repetition penalty, and bad words filtering.

Phase 23: Advanced Serialization & Validation
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from typing import Protocol, Any, TYPE_CHECKING

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    torch = None

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    np = None

# Try Rust acceleration
try:
    import rust_core
    RUST_AVAILABLE = True
except ImportError:
    RUST_AVAILABLE = False
    rust_core = None

if TYPE_CHECKING:
    import torch

__all__ = [
    "LogitsProcessor",
    "LogitsProcessorList",
    "TemperatureProcessor",
    "TopKProcessor",
    "TopPProcessor",
    "RepetitionPenaltyProcessor",
    "NoBadWordsProcessor",
    "MinLengthProcessor",
    "apply_processors",
]


class LogitsProcessor(Protocol):
    """
    Protocol for logits processors.

    A logits processor modifies the logits tensor before sampling.
    It receives the past token IDs and current logits, returning
    modified logits.
    """

    def __call__(
        self,
        input_ids: Sequence[int],
        logits: "torch.Tensor",
    ) -> "torch.Tensor":
        """
        Process logits.

        Args:
            input_ids: Previously generated token IDs
            logits: Logits tensor for next token [vocab_size]

        Returns:
            Modified logits tensor
        """
        ...


class LogitsProcessorList:
    """
    Composable list of logits processors.

    Applies processors in order, passing the output of each to the next.

    Example:
        >>> processors = LogitsProcessorList([
        ...     TemperatureProcessor(0.7),
        ...     TopKProcessor(50),
        ...     TopPProcessor(0.9),
        ... ])
        >>> modified_logits = processors(input_ids, logits)
    """

    def __init__(self, processors: list[LogitsProcessor] | None = None):
        self.processors: list[LogitsProcessor] = processors or []

    def append(self, processor: LogitsProcessor) -> None:
        """Add a processor to the list."""
        self.processors.append(processor)

    def extend(self, processors: Sequence[LogitsProcessor]) -> None:
        """Add multiple processors."""
        self.processors.extend(processors)

    def __call__(
        self,
        input_ids: Sequence[int],
        logits: "torch.Tensor",
    ) -> "torch.Tensor":
        """Apply all processors in sequence."""
        for processor in self.processors:
            logits = processor(input_ids, logits)
        return logits

    def __len__(self) -> int:
        return len(self.processors)

    def __iter__(self):
        return iter(self.processors)


class TemperatureProcessor:
    """
    Apply temperature scaling to logits.

    Temperature < 1.0 makes distribution sharper (more deterministic)
    Temperature > 1.0 makes distribution flatter (more random)
    Temperature = 1.0 is unchanged
    """

    def __init__(self, temperature: float):
        if temperature <= 0:
            raise ValueError("Temperature must be positive")
        self.temperature = temperature

    def __call__(
        self,
        input_ids: Sequence[int],
        logits: "torch.Tensor",
    ) -> "torch.Tensor":
        if self.temperature == 1.0:
            return logits

        # Use Rust acceleration if available
        if RUST_AVAILABLE and hasattr(rust_core, "apply_temperature_rust"):
            l_list = logits.tolist() if hasattr(logits, "tolist") else logits
            res = rust_core.apply_temperature_rust(l_list, self.temperature)
            if hasattr(logits, "device"):
                import torch
                return torch.tensor(res, device=logits.device, dtype=logits.dtype)
            return res

        return logits / self.temperature


class TopKProcessor:
    """
    Keep only top-k logits, set others to -inf.

    This limits sampling to the k most likely tokens.
    """

    def __init__(self, top_k: int):
        if top_k <= 0:
            raise ValueError("top_k must be positive")
        self.top_k = top_k

    def __call__(
        self,
        input_ids: Sequence[int],
        logits: "torch.Tensor",
    ) -> "torch.Tensor":
        if self.top_k >= logits.shape[-1]:
            return logits

        # Use Rust acceleration if available
        if RUST_AVAILABLE and hasattr(rust_core, "apply_top_k_rust"):
            l_list = logits.tolist() if hasattr(logits, "tolist") else logits
            is_1d = len(logits.shape) == 1
            if is_1d:
                l_list = [l_list]

            res = rust_core.apply_top_k_rust(l_list, self.top_k)

            if is_1d:
                res = res[0]

            if hasattr(logits, "device"):
                import torch
                return torch.tensor(res, device=logits.device, dtype=logits.dtype)
            return res

        # Find top-k values
        top_k_values, _ = torch.topk(logits, self.top_k, dim=-1)
        min_top_k = top_k_values[..., -1].unsqueeze(-1)

        # Mask out tokens below threshold
        return torch.where(
            logits < min_top_k,
            torch.full_like(logits, float("-inf")),
            logits,
        )


class TopPProcessor:
    """
    Nucleus sampling - keep tokens with cumulative probability <= top_p.

    This dynamically adjusts the number of considered tokens based on
    their cumulative probability.
    """

    def __init__(self, top_p: float):
        if not 0.0 < top_p <= 1.0:
            raise ValueError("top_p must be in (0, 1]")
        self.top_p = top_p

    def __call__(
        self,
        input_ids: Sequence[int],
        logits: "torch.Tensor",
    ) -> "torch.Tensor":
        if self.top_p >= 1.0:
            return logits

        # Sort logits in descending order
        sorted_logits, sorted_indices = torch.sort(logits, descending=True, dim=-1)
        cumulative_probs = torch.cumsum(torch.softmax(sorted_logits, dim=-1), dim=-1)

        # Find cutoff index
        sorted_indices_to_remove = cumulative_probs > self.top_p
        # Keep at least one token
        sorted_indices_to_remove[..., 0] = False

        # Scatter back to original order
        indices_to_remove = sorted_indices_to_remove.scatter(
            dim=-1, index=sorted_indices, src=sorted_indices_to_remove
        )

        return logits.masked_fill(indices_to_remove, float("-inf"))


class RepetitionPenaltyProcessor:
    """
    Penalize tokens that have already appeared.

    penalty > 1.0 discourages repetition
    penalty < 1.0 encourages repetition
    penalty = 1.0 is unchanged
    """

    def __init__(self, penalty: float):
        if penalty <= 0:
            raise ValueError("penalty must be positive")
        self.penalty = penalty

    def __call__(
        self,
        input_ids: Sequence[int],
        logits: "torch.Tensor",
    ) -> "torch.Tensor":
        if self.penalty == 1.0 or not input_ids:
            return logits

        # Use Rust acceleration if available
        if RUST_AVAILABLE and hasattr(rust_core, "apply_repetition_penalty_rust"):
            l_list = logits.tolist() if hasattr(logits, "tolist") else logits
            res = rust_core.apply_repetition_penalty_rust(
                l_list, list(input_ids), self.penalty
            )
            if hasattr(logits, "device"):
                import torch
                return torch.tensor(res, device=logits.device, dtype=logits.dtype)
            return res

        # Apply penalty to seen tokens
        logits = logits.clone()
        for token_id in set(input_ids):
            if token_id < logits.shape[-1]:
                if logits[token_id] > 0:
                    logits[token_id] /= self.penalty
                else:
                    logits[token_id] *= self.penalty

        return logits


class NoBadWordsProcessor:
    """
    Block specific token sequences from being generated.

    Given a list of "bad word" token sequences, this processor sets
    their logits to -inf when they would complete a bad sequence.
    """

    _SMALLEST_LOGIT = float("-inf")
    _NEUTRAL_LOGIT = 0.0

    def __init__(self, bad_words_ids: list[list[int]]):
        """
        Args:
            bad_words_ids: List of token ID sequences to block
        """
        self.bad_words_ids = bad_words_ids
        self._word_bias: "torch.Tensor | None" = None

    def __call__(
        self,
        input_ids: Sequence[int],
        logits: "torch.Tensor",
    ) -> "torch.Tensor":
        if not self.bad_words_ids:
            return logits

        # Initialize static bias on first call
        if self._word_bias is None:
            self._init_word_bias(logits)

        # Compute dynamic bias for multi-token sequences
        last_token_bias = torch.zeros_like(logits)

        for bad_word_ids in self.bad_words_ids:
            if len(bad_word_ids) == 1:
                # Single-token words handled by static bias
                continue

            if len(bad_word_ids) > len(input_ids) + 1:
                # Not enough context yet
                continue

            prefix_length = len(bad_word_ids) - 1
            last_token_id = bad_word_ids[-1]
            actual_prefix = list(input_ids[-prefix_length:])
            expected_prefix = bad_word_ids[:prefix_length]

            if actual_prefix == expected_prefix:
                last_token_bias[last_token_id] = self._SMALLEST_LOGIT

        return logits + self._word_bias + last_token_bias

    def _init_word_bias(self, logits: "torch.Tensor") -> None:
        """Initialize static bias for single-token bad words."""
        vocab_size = logits.shape[-1]

        self._word_bias = torch.zeros(vocab_size, dtype=logits.dtype, device=logits.device)

        for bad_word_ids in self.bad_words_ids:
            if len(bad_word_ids) == 1:
                token_id = bad_word_ids[0]
                if 0 <= token_id < vocab_size:
                    self._word_bias[token_id] = self._SMALLEST_LOGIT


class MinLengthProcessor:
    """
    Prevent EOS token before minimum length is reached.
    """

    def __init__(self, min_length: int, eos_token_id: int):
        self.min_length = min_length
        self.eos_token_id = eos_token_id

    def __call__(
        self,
        input_ids: Sequence[int],
        logits: "torch.Tensor",
    ) -> "torch.Tensor":
        if len(input_ids) < self.min_length:
            if 0 <= self.eos_token_id < logits.shape[-1]:
                logits = logits.clone()
                logits[self.eos_token_id] = float("-inf")
        return logits


class MaxLengthProcessor:
    """
    Force EOS token after maximum length is reached.
    """

    def __init__(self, max_length: int, eos_token_id: int):
        self.max_length = max_length
        self.eos_token_id = eos_token_id

    def __call__(
        self,
        input_ids: Sequence[int],
        logits: "torch.Tensor",
    ) -> "torch.Tensor":
        if len(input_ids) >= self.max_length:
            # Only allow EOS
            logits = torch.full_like(logits, float("-inf"))
            if 0 <= self.eos_token_id < logits.shape[-1]:
                logits[self.eos_token_id] = 0.0
        return logits


class PresencePenaltyProcessor:
    """
    Additive penalty for tokens that have appeared.

    Unlike RepetitionPenalty (multiplicative), this adds a flat penalty
    to any token that has appeared at least once.
    """

    def __init__(self, penalty: float):
        self.penalty = penalty

    def __call__(
        self,
        input_ids: Sequence[int],
        logits: "torch.Tensor",
    ) -> "torch.Tensor":
        if self.penalty == 0.0 or not input_ids:
            return logits

        logits = logits.clone()
        seen_tokens = set(input_ids)
        for token_id in seen_tokens:
            if 0 <= token_id < logits.shape[-1]:
                logits[token_id] -= self.penalty

        return logits


class FrequencyPenaltyProcessor:
    """
    Penalty proportional to token frequency.

    Tokens that appear more often receive a larger penalty.
    """

    def __init__(self, penalty: float):
        self.penalty = penalty

    def __call__(
        self,
        input_ids: Sequence[int],
        logits: "torch.Tensor",
    ) -> "torch.Tensor":
        if self.penalty == 0.0 or not input_ids:
            return logits

        # Count frequencies
        from collections import Counter
        freq = Counter(input_ids)

        logits = logits.clone()
        for token_id, count in freq.items():
            if 0 <= token_id < logits.shape[-1]:
                logits[token_id] -= self.penalty * count

        return logits


def apply_processors(
    input_ids: Sequence[int],
    logits: "torch.Tensor",
    *processors: LogitsProcessor,
) -> "torch.Tensor":
    """
    Apply multiple processors to logits.

    Convenience function for one-off processing.

    Args:
        input_ids: Past token IDs
        logits: Logits tensor
        *processors: Processors to apply

    Returns:
        Modified logits
    """
    for processor in processors:
        logits = processor(input_ids, logits)
    return logits


def create_processor_chain(
    temperature: float = 1.0,
    top_k: int | None = None,
    top_p: float | None = None,
    repetition_penalty: float = 1.0,
    presence_penalty: float = 0.0,
    frequency_penalty: float = 0.0,
    bad_words_ids: list[list[int]] | None = None,
    min_length: int | None = None,
    max_length: int | None = None,
    eos_token_id: int | None = None,
) -> LogitsProcessorList:
    """
    Create a standard processor chain from common parameters.

    Returns:
        LogitsProcessorList with configured processors
    """
    processors = LogitsProcessorList()

    if temperature != 1.0:
        processors.append(TemperatureProcessor(temperature))

    if top_k is not None:
        processors.append(TopKProcessor(top_k))

    if top_p is not None:
        processors.append(TopPProcessor(top_p))

    if repetition_penalty != 1.0:
        processors.append(RepetitionPenaltyProcessor(repetition_penalty))

    if presence_penalty != 0.0:
        processors.append(PresencePenaltyProcessor(presence_penalty))

    if frequency_penalty != 0.0:
        processors.append(FrequencyPenaltyProcessor(frequency_penalty))

    if bad_words_ids:
        processors.append(NoBadWordsProcessor(bad_words_ids))

    if min_length is not None and eos_token_id is not None:
        processors.append(MinLengthProcessor(min_length, eos_token_id))

    if max_length is not None and eos_token_id is not None:
        processors.append(MaxLengthProcessor(max_length, eos_token_id))

    return processors

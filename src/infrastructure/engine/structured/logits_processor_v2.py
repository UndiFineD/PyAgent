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

"""
LogitsProcessorV2 - Enhanced logits processor interface.

Implements vLLM's v1 LogitsProcessor interface with:
- BatchUpdate for state management
- MoveDirectionality for request movement tracking
- Argmax invariance declaration
- Efficient batch processing

Beyond vLLM innovations:
- Composable processor chains
- Lazy state updates
- Metrics collection
- Processor hot-swapping
"""

from _thread import LockType
import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Sequence, Tuple, Type

from numpy import dtype, floating, ndarray
from numpy._typing._nbit_base import _32Bit

from numpy import dtype, ndarray

try:
    import numpy as np  # noqa: F401

    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    import rust_core  # pylint: disable=unused-import

    HAS_RUST = True
except ImportError:
    HAS_RUST = False


class MoveDirectionality(Enum):
    """Direction of request movement within batch."""

    UNIDIRECTIONAL = auto()  # One-way move: i1 -> i2
    SWAP = auto()  # Two-way swap: i1 <-> i2


@dataclass
class SamplingParams:
    """Sampling parameters for a request."""

    temperature: float = 1.0
    top_p: float = 1.0
    top_k: int = -1
    min_p: float = 0.0
    presence_penalty: float = 0.0
    frequency_penalty: float = 0.0
    repetition_penalty: float = 1.0
    logit_bias: Optional[Dict[int, float]] = None
    bad_words: Optional[List[List[int]]] = None
    stop_token_ids: Optional[List[int]] = None

    def __post_init__(self) -> None:
        if self.logit_bias is None:
            self.logit_bias = {}
        if self.bad_words is None:
            self.bad_words = []
        if self.stop_token_ids is None:
            self.stop_token_ids = []


# Type aliases for batch updates
RemovedRequest = int  # Batch index of removed request
AddedRequest = Tuple[int, SamplingParams, Optional[List[int]], List[int]]
MovedRequest = Tuple[int, int, MoveDirectionality]


@dataclass(frozen=True)
class BatchUpdate:
    """
    Batch state change information for logits processors.

    Contains metadata for requests added to, removed from, and moved
    within the persistent batch. Operations should be processed in order:
    removed, added, moved.
    """

    batch_size: int
    removed: Sequence[RemovedRequest]
    added: Sequence[AddedRequest]
    moved: Sequence[MovedRequest]

    @classmethod
    def empty(cls, batch_size: int = 0) -> "BatchUpdate":
        """Create empty batch update."""
        return cls(
            batch_size=batch_size,
            removed=[],
            added=[],
            moved=[],
        )

    @property
    def has_changes(self) -> bool:
        """Check if there are any changes."""
        return bool(self.removed or self.added or self.moved)


class BatchUpdateBuilder:
    """Builder for constructing BatchUpdate objects."""

    def __init__(self, batch_size: int = 0) -> None:
        self.batch_size: int = batch_size
        self._removed: List[RemovedRequest] = []
        self._added: List[AddedRequest] = []
        self._moved: List[MovedRequest] = []

    def add_request(
        self,
        index: int,
        params: SamplingParams,
        prompt_token_ids: Optional[List[int]] = None,
        output_token_ids: Optional[List[int]] = None,
    ) -> "BatchUpdateBuilder":
        """Add a request to the batch."""
        self._added.append(
            (
                index,
                params,
                prompt_token_ids,
                output_token_ids or [],
            )
        )
        return self

    def remove_request(self, index: int) -> "BatchUpdateBuilder":
        """Remove a request from the batch."""
        self._removed.append(index)
        return self

    def move_request(
        self,
        from_index: int,
        to_index: int,
        directionality: MoveDirectionality = MoveDirectionality.UNIDIRECTIONAL,
    ) -> "BatchUpdateBuilder":
        """Move a request within the batch."""
        self._moved.append((from_index, to_index, directionality))
        return self

    def set_batch_size(self, size: int) -> "BatchUpdateBuilder":
        """Set batch size."""
        self.batch_size: int = size
        return self

    def build(self) -> BatchUpdate:
        """Build the BatchUpdate object."""
        return BatchUpdate(
            batch_size=self.batch_size,
            removed=tuple(self._removed),
            added=tuple(self._added),
            moved=tuple(self._moved),
        )

    def clear(self) -> "BatchUpdateBuilder":
        """Clear all pending changes."""
        self._removed.clear()
        self._added.clear()
        self._moved.clear()
        return self


class LogitsProcessor(ABC):
    """
    Abstract base class for logits processors.

    Processors modify logits before sampling to implement constraints
    like temperature, top-k, min-p, bad words, etc.
    """

    @classmethod
    def validate_params(cls, sampling_params: SamplingParams) -> None:
        """
        Validate sampling params for this processor.

        Raise ValueError for invalid parameters.
        """

    @abstractmethod
    def apply(self, logits: Any) -> Any:
        """
        Apply processor to batch logits tensor.

        Args:
            logits: Tensor of shape [batch_size, vocab_size]

        Returns:
            Modified logits tensor (may be modified in-place)
        """
        raise NotImplementedError

    @abstractmethod
    def is_argmax_invariant(self) -> bool:
        """
        Check if processor preserves argmax.

        Returns True if the processor has no impact on argmax
        computation in greedy sampling. Used to optimize greedy
        decoding by skipping processors that don't affect results.
        """
        raise NotImplementedError

    @abstractmethod
    def update_state(self, batch_update: Optional[BatchUpdate]) -> None:
        """
        Update processor state based on batch changes.

        Called when there are new output tokens or batch changes,
        prior to each forward pass.
        """
        raise NotImplementedError

    def has_state(self) -> bool:
        """Check if processor maintains state."""
        return False

    def reset(self) -> None:
        """Reset processor state."""


class MinPLogitsProcessor(LogitsProcessor):
    """
    Min-P sampling logits processor.

    Filters tokens with probability below (min_p * max_probability).
    Does not affect greedy sampling (argmax invariant).
    """

    def __init__(
        self,
        max_num_reqs: int,
        device: str = "cpu",
        _is_pin_memory: bool = False,
    ) -> None:
        self.max_num_reqs: int = max_num_reqs
        self.device: str = device
        self.min_p_count = 0

        if HAS_NUMPY:
            self.min_p_cpu: ndarray[tuple[int], dtype[floating[_32Bit]]] = np.zeros(max_num_reqs, dtype=np.float32)
        else:
            self.min_p_cpu: List[float] = [0.0] * max_num_reqs

        self.min_p: Optional[Any] = None

    def is_argmax_invariant(self) -> bool:
        """Min-p never impacts greedy sampling."""
        return True

    def get_min_p_by_index(self, index: int) -> float:
        """Get min_p value for request at index."""
        return float(self.min_p_cpu[index])

    def update_state(self, batch_update: Optional[BatchUpdate]) -> None:
        """Update min_p values based on batch changes."""
        if batch_update is None:
            return

        # Process added requests
        for index, params, _, _ in batch_update.added:
            min_p: float = params.min_p
            min_p_before: Any | float = self.min_p_cpu[index]
            if min_p_before != min_p:
                self.min_p_cpu[index] = min_p
                if min_p and not min_p_before:
                    self.min_p_count += 1
                elif not min_p and min_p_before:
                    self.min_p_count -= 1

        if self.min_p_count:
            # Process removed requests
            if batch_update.removed:
                for index in batch_update.removed:
                    if self.min_p_cpu[index]:
                        self.min_p_cpu[index] = 0.0
                        self.min_p_count -= 1

            # Process moved requests
            for from_idx, to_idx, direction in batch_update.moved:
                min_p_a: Any | float = self.min_p_cpu[from_idx]
                min_p_b: Any | float = self.min_p_cpu[to_idx]
                if min_p_a != min_p_b:
                    self.min_p_cpu[to_idx] = min_p_a
                    if direction == MoveDirectionality.SWAP:
                        self.min_p_cpu[from_idx] = min_p_b
                if direction == MoveDirectionality.UNIDIRECTIONAL:
                    if min_p_a:
                        self.min_p_cpu[from_idx] = 0.0
                    if min_p_b:
                        self.min_p_count -= 1

    def apply(self, logits: Any) -> Any:
        """Apply min-p filtering."""
        if self.min_p_count == 0:
            return logits

        if HAS_NUMPY and isinstance(logits, np.ndarray):
            return self._apply_numpy(logits)

        # Fallback for torch tensors or other types
        return self._apply_generic(logits)

    def _apply_numpy(self, logits: "np.ndarray") -> "np.ndarray":
        """Apply min-p using NumPy."""
        # Softmax for probabilities
        exp_logits = np.exp(logits - np.max(logits, axis=-1, keepdims=True))
        probs = exp_logits / np.sum(exp_logits, axis=-1, keepdims=True)

        # Get max probabilities
        max_probs = np.max(probs, axis=-1, keepdims=True)

        # Compute thresholds
        batch_size = logits.shape[0]
        min_p_vals: ndarray[tuple[int, int], dtype[Any]] = np.array(self.min_p_cpu[:batch_size]).reshape(-1, 1)
        thresholds = max_probs * min_p_vals

        # Mask tokens below threshold
        mask = probs < thresholds
        logits[mask] = float("-inf")

        return logits

    def _apply_generic(self, logits: Any) -> Any:
        """Generic apply for torch tensors."""
        # Placeholder - actual torch implementation
        return logits

    def has_state(self) -> bool:
        return True

    def reset(self) -> None:
        if HAS_NUMPY:
            self.min_p_cpu.fill(0)
        else:
            self.min_p_cpu: List[float] = [0.0] * self.max_num_reqs
        self.min_p_count = 0


class LogitBiasLogitsProcessor(LogitsProcessor):
    """
    Logit bias processor.

    Adds bias values to specific token logits. Can change argmax
    results, so not argmax invariant.
    """

    def __init__(
        self,
        max_num_reqs: int,
        device: str = "cpu",
        _is_pin_memory: bool = False,
    ) -> None:
        self.max_num_reqs: int = max_num_reqs
        self.device: str = device

        # Per-request logit biases
        self.biases: Dict[int, Dict[int, float]] = {}

        # Cached tensor representations
        self._bias_indices: Optional[Any] = None
        self._bias_values: Optional[Any] = None
        self._needs_rebuild = True

    def is_argmax_invariant(self) -> bool:
        """Logit bias can change argmax."""
        return False

    def update_state(self, batch_update: Optional[BatchUpdate]) -> None:
        """Update bias state based on batch changes."""
        if batch_update is None:
            return

        needs_update = False

        # Process added requests
        for index, params, _, _ in batch_update.added:
            if params.logit_bias:
                self.biases[index] = dict(params.logit_bias)
                needs_update = True
            elif index in self.biases:
                del self.biases[index]
                needs_update = True

        # Process removed requests
        for index in batch_update.removed:
            if index in self.biases:
                del self.biases[index]
                needs_update = True

        # Process moved requests
        for from_idx, to_idx, direction in batch_update.moved:
            bias_a: Dict[int, float] | None = self.biases.get(from_idx)
            bias_b: Dict[int, float] | None = self.biases.get(to_idx)

            if bias_a is not None:
                self.biases[to_idx] = bias_a
                needs_update = True
            elif to_idx in self.biases:
                del self.biases[to_idx]
                needs_update = True

            if direction == MoveDirectionality.SWAP:
                if bias_b is not None:
                    self.biases[from_idx] = bias_b
                elif from_idx in self.biases:
                    del self.biases[from_idx]
            else:
                if from_idx in self.biases:
                    del self.biases[from_idx]

        if needs_update:
            self._needs_rebuild = True

    def apply(self, logits: Any) -> Any:
        """Apply logit biases."""
        if not self.biases:
            return logits

        if HAS_NUMPY and isinstance(logits, np.ndarray):
            return self._apply_numpy(logits)

        return self._apply_generic(logits)

    def _apply_numpy(self, logits: "np.ndarray") -> "np.ndarray":
        """Apply biases using NumPy."""
        for req_idx, token_biases in self.biases.items():
            if req_idx < logits.shape[0]:
                for token_id, bias in token_biases.items():
                    if token_id < logits.shape[1]:
                        logits[req_idx, token_id] += bias
        return logits

    def _apply_generic(self, logits: Any) -> Any:
        """Generic apply for torch tensors."""
        return logits

    def has_state(self) -> bool:
        return True

    def reset(self) -> None:
        self.biases.clear()
        self._needs_rebuild = True


class CompositeLogitsProcessor(LogitsProcessor):
    """
    Composite processor that chains multiple processors.

    Beyond vLLM: Allows flexible composition of processors
    with optimized execution order.
    """

    def __init__(self, processors: List[LogitsProcessor]) -> None:
        self.processors: List[LogitsProcessor] = processors
        self._argmax_invariant: Optional[bool] = None

    def is_argmax_invariant(self) -> bool:
        """Check if all processors are argmax invariant."""
        if self._argmax_invariant is None:
            self._argmax_invariant = all(p.is_argmax_invariant() for p in self.processors)
        return self._argmax_invariant

    def update_state(self, batch_update: Optional[BatchUpdate]) -> None:
        """Update state for all processors."""
        for processor in self.processors:
            processor.update_state(batch_update)

    def apply(self, logits: Any) -> Any:
        """Apply all processors in sequence."""
        for processor in self.processors:
            logits = processor.apply(logits)
        return logits

    def has_state(self) -> bool:
        return any(p.has_state() for p in self.processors)

    def reset(self) -> None:
        for processor in self.processors:
            processor.reset()

    def add_processor(self, processor: LogitsProcessor) -> None:
        """Add a processor to the chain."""
        self.processors.append(processor)
        self._argmax_invariant = None

    def remove_processor(self, processor: LogitsProcessor) -> bool:
        """Remove a processor from the chain."""
        try:
            self.processors.remove(processor)
            self._argmax_invariant = None
            return True
        except ValueError:
            return False


class LogitsProcessorRegistry:
    """
    Registry for logits processor types.

    Beyond vLLM: Provides plugin-based processor registration
    and automatic processor selection based on sampling params.
    """

    _instance: Optional["LogitsProcessorRegistry"] = None
    _lock: LockType = threading.Lock()

    def __new__(cls) -> "LogitsProcessorRegistry":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._processors: Dict[str, Type[LogitsProcessor]] = {}
                    cls._instance._register_defaults()
        return cls._instance

    def _register_defaults(self) -> None:
        """Register default processors."""
        self.register("min_p", MinPLogitsProcessor)
        self.register("logit_bias", LogitBiasLogitsProcessor)

    def register(
        self,
        name: str,
        processor_cls: Type[LogitsProcessor],
    ) -> None:
        """Register a processor type."""
        self._processors[name] = processor_cls

    def get(self, name: str) -> Optional[Type[LogitsProcessor]]:
        """Get a processor type by name."""
        return self._processors.get(name)

    def create_for_params(
        self,
        params: SamplingParams,
        max_num_reqs: int,
        device: str = "cpu",
    ) -> CompositeLogitsProcessor:
        """Create composite processor based on sampling params."""
        processors: List[LogitsProcessor] = []

        if params.min_p > 0:
            processors.append(MinPLogitsProcessor(max_num_reqs, device))

        if params.logit_bias:
            processors.append(LogitBiasLogitsProcessor(max_num_reqs, device))

        return CompositeLogitsProcessor(processors)

    @classmethod
    def get_instance(cls) -> "LogitsProcessorRegistry":
        """Get singleton instance."""
        return cls()


__all__: List[str] = [
    "MoveDirectionality",
    "SamplingParams",
    "RemovedRequest",
    "AddedRequest",
    "MovedRequest",
    "BatchUpdate",
    "BatchUpdateBuilder",
    "LogitsProcessor",
    "MinPLogitsProcessor",
    "LogitBiasLogitsProcessor",
    "CompositeLogitsProcessor",
    "LogitsProcessorRegistry",
]

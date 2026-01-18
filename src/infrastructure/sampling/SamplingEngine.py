# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""
Advanced sampling engine for token generation.

This module implements unified sampling strategies for LLM inference,
inspired by vLLM's v1/sample architecture.

Key Components:
    - SamplingParams: Configuration for sampling behavior
    - SamplingState: Per-request state tracking
    - Sampler: Abstract base class for sampling strategies
    - TopKSampler/TopPSampler/TopKTopPSampler: Common filtering samplers
    - GumbelSampler: Gumbel-max trick for efficient categorical sampling
    - BeamSearchSampler: Beam search with length penalty
    - SamplingPipeline: Composable sampler chain

Example:
    >>> from src.infrastructure.sampling import (
    ...     SamplingParams, TopKTopPSampler, TemperatureSampler, SamplingPipeline
    ... )
    >>> import numpy as np
    >>> 
    >>> # Create sampling parameters
    >>> params = SamplingParams(temperature=0.8, top_k=50, top_p=0.9)
    >>> 
    >>> # Create a sampling pipeline
    >>> pipeline = SamplingPipeline([
    ...     TemperatureSampler(),
    ...     TopKTopPSampler(),
    ... ])
    >>> 
    >>> # Sample from logits
    >>> logits = np.random.randn(1, 50257)  # [batch_size, vocab_size]
    >>> token_ids = pipeline.sample(logits, params)
"""

from __future__ import annotations

import math
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

import numpy as np

# Try to import Rust accelerations
try:
    from rust_core import (
        top_k_mask_rust,
        top_p_mask_rust,
        gumbel_sample_rust,
        beam_score_rust,
        compute_penalties_rust,
    )
    HAS_RUST = True
except ImportError:
    HAS_RUST = False


# ==============================================================================
# Sampling Parameters
# ==============================================================================

@dataclass
class SamplingParams:
    """
    Parameters for controlling text generation sampling.

    Attributes:
        temperature: Temperature for softmax. Higher = more random.
        top_k: Number of top tokens to consider. -1 or 0 = disabled.
        top_p: Cumulative probability threshold (nucleus sampling).
        min_p: Minimum probability relative to top token.
        repetition_penalty: Penalty for repeated tokens (> 1.0).
        presence_penalty: Additive penalty for presence of tokens.
        frequency_penalty: Additive penalty based on frequency.
        seed: Random seed for reproducibility.
        max_tokens: Maximum tokens to generate.
        min_tokens: Minimum tokens to generate before stopping.
        stop_token_ids: Token IDs that trigger stopping.
        ignore_eos: Whether to ignore EOS token.
        logprobs: Number of top logprobs to return per token.
    """
    temperature: float = 1.0
    top_k: int = -1  # -1 or 0 means disabled
    top_p: float = 1.0
    min_p: float = 0.0
    repetition_penalty: float = 1.0
    presence_penalty: float = 0.0
    frequency_penalty: float = 0.0
    seed: Optional[int] = None
    max_tokens: int = 100
    min_tokens: int = 0
    stop_token_ids: Optional[List[int]] = None
    ignore_eos: bool = False
    logprobs: Optional[int] = None

    def __post_init__(self):
        """Validate parameters."""
        if self.temperature < 0:
            raise ValueError("temperature must be non-negative")
        if self.top_p < 0 or self.top_p > 1:
            raise ValueError("top_p must be in [0, 1]")
        if self.min_p < 0 or self.min_p > 1:
            raise ValueError("min_p must be in [0, 1]")
        if self.repetition_penalty < 1.0:
            raise ValueError("repetition_penalty must be >= 1.0")

    @property
    def use_temperature(self) -> bool:
        """Check if temperature scaling is needed."""
        return self.temperature != 1.0 and self.temperature > 0

    @property
    def use_top_k(self) -> bool:
        """Check if top-k filtering is enabled."""
        return self.top_k > 0

    @property
    def use_top_p(self) -> bool:
        """Check if top-p (nucleus) filtering is enabled."""
        return self.top_p < 1.0

    @property
    def use_min_p(self) -> bool:
        """Check if min-p filtering is enabled."""
        return self.min_p > 0


# ==============================================================================
# Sampling State
# ==============================================================================

@dataclass
class SamplingState:
    """
    Per-request state for sampling.

    Tracks generated tokens and other stateful information needed
    for penalties and constraints.

    Attributes:
        request_id: Unique request identifier
        generated_ids: List of generated token IDs
        token_counts: Count of each token ID generated (for frequency penalty)
        prompt_token_ids: Original prompt token IDs (optional)
    """
    request_id: str
    generated_ids: List[int] = field(default_factory=list)
    token_counts: Dict[int, int] = field(default_factory=dict)
    prompt_token_ids: Optional[List[int]] = None
    
    # Random state for reproducibility
    rng: Optional[np.random.Generator] = None

    def __post_init__(self):
        """Initialize random generator if not provided."""
        if self.rng is None:
            self.rng = np.random.default_rng()

    def add_token(self, token_id: int) -> None:
        """Add a generated token to the state."""
        self.generated_ids.append(token_id)
        self.token_counts[token_id] = self.token_counts.get(token_id, 0) + 1

    def get_all_token_ids(self) -> List[int]:
        """Get all token IDs (prompt + generated)."""
        if self.prompt_token_ids:
            return self.prompt_token_ids + self.generated_ids
        return self.generated_ids

    @classmethod
    def from_seed(cls, request_id: str, seed: Optional[int] = None) -> "SamplingState":
        """Create a state with a specific random seed."""
        rng = np.random.default_rng(seed) if seed is not None else np.random.default_rng()
        return cls(request_id=request_id, rng=rng)


# ==============================================================================
# Abstract Sampler
# ==============================================================================

class Sampler(ABC):
    """
    Abstract base class for sampling strategies.

    Samplers implement the `forward` method to transform logits
    and optionally select tokens.
    """

    @abstractmethod
    def forward(
        self,
        logits: np.ndarray,
        params: SamplingParams,
        state: Optional[SamplingState] = None,
    ) -> np.ndarray:
        """
        Transform or filter logits.

        Args:
            logits: Input logits [batch_size, vocab_size]
            params: Sampling parameters
            state: Optional per-request state

        Returns:
            Transformed logits [batch_size, vocab_size]
        """
        pass

    def sample(
        self,
        logits: np.ndarray,
        params: SamplingParams,
        state: Optional[SamplingState] = None,
    ) -> np.ndarray:
        """
        Sample token IDs from logits.

        Args:
            logits: Input logits [batch_size, vocab_size]
            params: Sampling parameters
            state: Optional per-request state

        Returns:
            Sampled token IDs [batch_size]
        """
        processed = self.forward(logits, params, state)
        return self._sample_from_logits(processed, state)

    def _sample_from_logits(
        self,
        logits: np.ndarray,
        state: Optional[SamplingState] = None,
    ) -> np.ndarray:
        """Sample token IDs from processed logits using softmax + multinomial."""
        # Apply softmax
        probs = _softmax(logits)
        
        # Sample from distribution
        batch_size = probs.shape[0]
        samples = np.zeros(batch_size, dtype=np.int64)
        
        for i in range(batch_size):
            if state and state.rng:
                samples[i] = state.rng.choice(len(probs[i]), p=probs[i])
            else:
                samples[i] = np.random.choice(len(probs[i]), p=probs[i])
        
        return samples


# ==============================================================================
# Temperature Sampler
# ==============================================================================

class TemperatureSampler(Sampler):
    """
    Temperature scaling sampler.

    Divides logits by temperature before softmax:
    - temperature > 1.0: More random (flatter distribution)
    - temperature < 1.0: More deterministic (sharper peaks)
    - temperature = 0: Greedy (argmax)
    """

    def forward(
        self,
        logits: np.ndarray,
        params: SamplingParams,
        state: Optional[SamplingState] = None,
    ) -> np.ndarray:
        """Apply temperature scaling to logits."""
        if params.temperature <= 0:
            # Greedy: set max logit to very high, others to -inf
            max_indices = np.argmax(logits, axis=-1, keepdims=True)
            result = np.full_like(logits, -float("inf"))
            np.put_along_axis(result, max_indices, 0.0, axis=-1)
            return result
        
        if params.temperature == 1.0:
            return logits
        
        return logits / params.temperature


# ==============================================================================
# Top-K Sampler
# ==============================================================================

class TopKSampler(Sampler):
    """
    Top-K filtering sampler.

    Keeps only the top-k logits by value, setting others to -inf.
    This limits the vocabulary to the k most likely tokens.
    """

    def forward(
        self,
        logits: np.ndarray,
        params: SamplingParams,
        state: Optional[SamplingState] = None,
    ) -> np.ndarray:
        """Apply top-k filtering to logits."""
        if not params.use_top_k:
            return logits
        
        k = min(params.top_k, logits.shape[-1])
        
        if HAS_RUST and logits.ndim == 1:
            # Rust function handles 1D arrays
            result = top_k_mask_rust(logits.tolist(), k)
            return np.array(result, dtype=logits.dtype)
        
        # Get the k-th largest value for each batch
        top_k_values = np.partition(logits, -k, axis=-1)[..., -k:]
        threshold = np.min(top_k_values, axis=-1, keepdims=True)
        
        # Mask values below threshold
        mask = logits < threshold
        result = np.where(mask, -float("inf"), logits)
        return result


# ==============================================================================
# Top-P (Nucleus) Sampler
# ==============================================================================

class TopPSampler(Sampler):
    """
    Top-P (nucleus) sampling.

    Keeps the smallest set of tokens whose cumulative probability
    exceeds p. This adapts the number of tokens based on the
    probability distribution.
    """

    def forward(
        self,
        logits: np.ndarray,
        params: SamplingParams,
        state: Optional[SamplingState] = None,
    ) -> np.ndarray:
        """Apply top-p (nucleus) filtering to logits."""
        if not params.use_top_p:
            return logits
        
        if HAS_RUST and logits.ndim == 1:
            # Rust function handles 1D arrays
            result = top_p_mask_rust(logits.tolist(), params.top_p)
            return np.array(result, dtype=logits.dtype)
        
        # Handle 2D arrays
        if logits.ndim == 1:
            logits = logits.reshape(1, -1)
        
        batch_size, vocab_size = logits.shape
        result = logits.copy()
        
        for i in range(batch_size):
            # Sort logits in descending order
            sorted_indices = np.argsort(logits[i])[::-1]
            sorted_logits = logits[i][sorted_indices]
            
            # Convert to probabilities
            probs = _softmax(sorted_logits.reshape(1, -1))[0]
            
            # Compute cumulative probabilities
            cumsum = np.cumsum(probs)
            
            # Find cutoff index
            cutoff_idx = np.searchsorted(cumsum, params.top_p) + 1
            
            # Create mask for tokens to remove
            remove_indices = sorted_indices[cutoff_idx:]
            result[i, remove_indices] = -float("inf")
        
        return result


# ==============================================================================
# Combined Top-K + Top-P Sampler
# ==============================================================================

class TopKTopPSampler(Sampler):
    """
    Combined top-k and top-p filtering.

    Applies top-k first to limit vocabulary, then top-p for
    adaptive nucleus selection. This is the standard approach
    used in vLLM and other inference engines.
    """

    def forward(
        self,
        logits: np.ndarray,
        params: SamplingParams,
        state: Optional[SamplingState] = None,
    ) -> np.ndarray:
        """Apply combined top-k and top-p filtering."""
        result = logits
        
        # Ensure 2D
        was_1d = result.ndim == 1
        if was_1d:
            result = result.reshape(1, -1)
        
        # Apply top-k first
        if params.use_top_k:
            k = min(params.top_k, result.shape[-1])
            # Use numpy implementation for 2D arrays
            top_k_values = np.partition(result, -k, axis=-1)[..., -k:]
            threshold = np.min(top_k_values, axis=-1, keepdims=True)
            mask = result < threshold
            result = np.where(mask, -float("inf"), result)
        
        # Then apply top-p
        if params.use_top_p:
            batch_size = result.shape[0]
            for i in range(batch_size):
                # Get valid (non-masked) indices
                valid_mask = result[i] > -float("inf")
                if not np.any(valid_mask):
                    continue
                
                valid_logits = result[i][valid_mask]
                valid_indices = np.where(valid_mask)[0]
                
                # Sort by logit value
                sorted_order = np.argsort(valid_logits)[::-1]
                sorted_logits = valid_logits[sorted_order]
                sorted_indices = valid_indices[sorted_order]
                
                # Compute probabilities and cumsum
                probs = _softmax(sorted_logits.reshape(1, -1))[0]
                cumsum = np.cumsum(probs)
                
                # Find cutoff
                cutoff_idx = np.searchsorted(cumsum, params.top_p) + 1
                remove_indices = sorted_indices[cutoff_idx:]
                result[i, remove_indices] = -float("inf")
        
        # Apply min-p if enabled
        if params.use_min_p:
            # Get max probability for each batch
            probs = _softmax(result)
            max_prob = np.max(probs, axis=-1, keepdims=True)
            threshold = params.min_p * max_prob
            mask = probs < threshold
            result = np.where(mask, -float("inf"), result)
        
        if was_1d:
            result = result.squeeze(0)
        
        return result


# ==============================================================================
# Gumbel Sampler
# ==============================================================================

class GumbelSampler(Sampler):
    """
    Gumbel-max trick sampler.

    Uses Gumbel noise for efficient categorical sampling:
    sample = argmax(logits + Gumbel(0, 1))

    This is equivalent to sampling from softmax(logits) but
    can be more efficient and numerically stable.
    """

    def forward(
        self,
        logits: np.ndarray,
        params: SamplingParams,
        state: Optional[SamplingState] = None,
    ) -> np.ndarray:
        """Return logits unchanged (sampling happens in sample())."""
        # Apply temperature if needed
        if params.use_temperature:
            logits = logits / params.temperature
        return logits

    def sample(
        self,
        logits: np.ndarray,
        params: SamplingParams,
        state: Optional[SamplingState] = None,
    ) -> np.ndarray:
        """Sample using Gumbel-max trick."""
        processed = self.forward(logits, params, state)
        
        # Rust function handles 1D arrays only
        if HAS_RUST and processed.ndim == 1:
            seed = params.seed if params.seed is not None else 42
            temp = max(params.temperature, 0.01) if params.use_temperature else 1.0
            idx = gumbel_sample_rust(processed.tolist(), temp, seed)
            return np.array([idx], dtype=np.int64)
        
        # Generate Gumbel noise
        rng = state.rng if state and state.rng else np.random.default_rng(params.seed)
        u = rng.uniform(size=processed.shape)
        # Gumbel(0, 1) = -log(-log(U)) for U ~ Uniform(0, 1)
        gumbel_noise = -np.log(-np.log(np.clip(u, 1e-10, 1 - 1e-10)))
        
        # Add noise and take argmax
        perturbed = processed + gumbel_noise
        return np.argmax(perturbed, axis=-1)


# ==============================================================================
# Repetition Penalty Sampler
# ==============================================================================

class RepetitionPenaltySampler(Sampler):
    """
    Repetition penalty sampler.

    Applies multiplicative penalty to previously generated tokens:
    - penalty > 1.0: Discourage repetition
    - penalty = 1.0: No effect
    """

    def forward(
        self,
        logits: np.ndarray,
        params: SamplingParams,
        state: Optional[SamplingState] = None,
    ) -> np.ndarray:
        """Apply repetition penalty to logits."""
        if params.repetition_penalty == 1.0:
            return logits
        
        if state is None:
            return logits
        
        result = logits.copy()
        all_tokens = state.get_all_token_ids()
        
        if not all_tokens:
            return result
        
        # Get unique token IDs that have been generated
        unique_tokens = set(all_tokens)
        
        for token_id in unique_tokens:
            if token_id >= result.shape[-1]:
                continue
            
            # Apply penalty
            if result[0, token_id] > 0:
                result[0, token_id] /= params.repetition_penalty
            else:
                result[0, token_id] *= params.repetition_penalty
        
        return result


# ==============================================================================
# Presence/Frequency Penalty Sampler
# ==============================================================================

class PenaltySampler(Sampler):
    """
    Presence and frequency penalty sampler.

    Applies additive penalties based on token presence and frequency:
    - presence_penalty: Applied once per unique token
    - frequency_penalty: Applied per occurrence of each token
    """

    def forward(
        self,
        logits: np.ndarray,
        params: SamplingParams,
        state: Optional[SamplingState] = None,
    ) -> np.ndarray:
        """Apply presence and frequency penalties."""
        if params.presence_penalty == 0 and params.frequency_penalty == 0:
            return logits
        
        if state is None:
            return logits
        
        if HAS_RUST:
            token_counts = list(state.token_counts.items())
            return compute_penalties_rust(
                logits,
                token_counts,
                params.presence_penalty,
                params.frequency_penalty,
            )
        
        result = logits.copy()
        
        for token_id, count in state.token_counts.items():
            if token_id >= result.shape[-1]:
                continue
            
            # Presence penalty (applied once)
            result[0, token_id] -= params.presence_penalty
            
            # Frequency penalty (applied per occurrence)
            result[0, token_id] -= params.frequency_penalty * count
        
        return result


# ==============================================================================
# Beam Search
# ==============================================================================

@dataclass
class BeamSearchConfig:
    """
    Configuration for beam search.

    Attributes:
        beam_width: Number of beams to maintain
        length_penalty: Penalty/bonus for sequence length (> 1 = longer)
        early_stopping: Stop when all beams have finished
        max_tokens: Maximum sequence length
    """
    beam_width: int = 4
    length_penalty: float = 1.0
    early_stopping: bool = True
    max_tokens: int = 100


@dataclass
class BeamHypothesis:
    """
    A hypothesis in beam search.

    Attributes:
        token_ids: Sequence of token IDs
        score: Cumulative log probability
        finished: Whether the sequence has ended
    """
    token_ids: List[int] = field(default_factory=list)
    score: float = 0.0
    finished: bool = False

    @property
    def length(self) -> int:
        """Get sequence length."""
        return len(self.token_ids)

    def normalized_score(self, length_penalty: float = 1.0) -> float:
        """Get length-normalized score."""
        if self.length == 0:
            return self.score
        
        if HAS_RUST:
            return beam_score_rust(self.score, self.length, length_penalty)
        
        # Length normalization: score / length^alpha
        return self.score / (self.length ** length_penalty)

    def extend(self, token_id: int, log_prob: float) -> "BeamHypothesis":
        """Create a new hypothesis by extending with a token."""
        return BeamHypothesis(
            token_ids=self.token_ids + [token_id],
            score=self.score + log_prob,
            finished=False,
        )

    def finish(self) -> "BeamHypothesis":
        """Mark the hypothesis as finished."""
        return BeamHypothesis(
            token_ids=self.token_ids,
            score=self.score,
            finished=True,
        )


class BeamSearchSampler(Sampler):
    """
    Beam search sampler.

    Maintains multiple hypotheses and selects the best ones at each
    step based on cumulative log probability.
    """

    def __init__(self, config: Optional[BeamSearchConfig] = None):
        """Initialize beam search sampler."""
        self.config = config or BeamSearchConfig()
        self._beams: List[BeamHypothesis] = []
        self._finished_beams: List[BeamHypothesis] = []

    def reset(self) -> None:
        """Reset beam search state."""
        self._beams = [BeamHypothesis()]
        self._finished_beams = []

    def forward(
        self,
        logits: np.ndarray,
        params: SamplingParams,
        state: Optional[SamplingState] = None,
    ) -> np.ndarray:
        """Return logits unchanged (beam search happens in step())."""
        return logits

    def step(
        self,
        logits: np.ndarray,
        eos_token_id: Optional[int] = None,
    ) -> List[BeamHypothesis]:
        """
        Execute one step of beam search.

        Args:
            logits: Logits for current position [num_beams, vocab_size]
            eos_token_id: End-of-sequence token ID

        Returns:
            Current active beams
        """
        if not self._beams:
            self.reset()
        
        # Convert logits to log probabilities
        log_probs = _log_softmax(logits)
        
        # Collect all candidates
        candidates: List[Tuple[float, int, BeamHypothesis]] = []
        
        for beam_idx, beam in enumerate(self._beams):
            if beam.finished:
                continue
            
            beam_log_probs = log_probs[beam_idx] if len(log_probs) > beam_idx else log_probs[0]
            
            # Get top-k tokens for this beam
            top_k = min(self.config.beam_width * 2, len(beam_log_probs))
            top_indices = np.argpartition(beam_log_probs, -top_k)[-top_k:]
            
            for token_id in top_indices:
                log_prob = float(beam_log_probs[token_id])
                new_beam = beam.extend(token_id, log_prob)
                
                # Check for EOS
                if eos_token_id is not None and token_id == eos_token_id:
                    new_beam = new_beam.finish()
                    self._finished_beams.append(new_beam)
                else:
                    score = new_beam.normalized_score(self.config.length_penalty)
                    candidates.append((score, len(candidates), new_beam))
        
        # Select top beams
        candidates.sort(key=lambda x: -x[0])  # Sort by score descending
        self._beams = [c[2] for c in candidates[:self.config.beam_width]]
        
        return self._beams

    def get_best_hypothesis(self) -> Optional[BeamHypothesis]:
        """Get the best finished hypothesis."""
        all_beams = self._finished_beams + self._beams
        if not all_beams:
            return None
        
        # Sort by normalized score
        sorted_beams = sorted(
            all_beams,
            key=lambda b: b.normalized_score(self.config.length_penalty),
            reverse=True,
        )
        return sorted_beams[0]

    def is_finished(self) -> bool:
        """Check if beam search should stop."""
        if self.config.early_stopping:
            # Stop when all beams are finished
            return all(b.finished for b in self._beams)
        
        # Or when we have enough finished beams
        return len(self._finished_beams) >= self.config.beam_width


# ==============================================================================
# Sampling Pipeline
# ==============================================================================

class SamplingPipeline:
    """
    Composable pipeline of samplers.

    Chains multiple samplers together, applying each in sequence.
    The final sampler is used for actual token selection.

    Example:
        >>> pipeline = SamplingPipeline([
        ...     TemperatureSampler(),
        ...     TopKTopPSampler(),
        ...     GumbelSampler(),  # Final sampler
        ... ])
        >>> tokens = pipeline.sample(logits, params)
    """

    def __init__(self, samplers: Optional[List[Sampler]] = None):
        """
        Initialize the sampling pipeline.

        Args:
            samplers: List of samplers to apply in order
        """
        self.samplers = samplers or []

    def add_sampler(self, sampler: Sampler) -> "SamplingPipeline":
        """Add a sampler to the pipeline."""
        self.samplers.append(sampler)
        return self

    def forward(
        self,
        logits: np.ndarray,
        params: SamplingParams,
        state: Optional[SamplingState] = None,
    ) -> np.ndarray:
        """Apply all samplers to transform logits."""
        result = logits
        for sampler in self.samplers:
            result = sampler.forward(result, params, state)
        return result

    def sample(
        self,
        logits: np.ndarray,
        params: SamplingParams,
        state: Optional[SamplingState] = None,
    ) -> np.ndarray:
        """Apply pipeline and sample tokens."""
        # Apply all but last sampler for transformation
        result = logits
        for sampler in self.samplers[:-1]:
            result = sampler.forward(result, params, state)
        
        # Use last sampler for actual sampling
        if self.samplers:
            return self.samplers[-1].sample(result, params, state)
        else:
            # Default: softmax + multinomial
            return _sample_from_probs(_softmax(result), state)


# ==============================================================================
# Utility Functions
# ==============================================================================

def _softmax(logits: np.ndarray) -> np.ndarray:
    """Numerically stable softmax."""
    shifted = logits - np.max(logits, axis=-1, keepdims=True)
    exp_logits = np.exp(shifted)
    return exp_logits / np.sum(exp_logits, axis=-1, keepdims=True)


def _log_softmax(logits: np.ndarray) -> np.ndarray:
    """Numerically stable log softmax."""
    shifted = logits - np.max(logits, axis=-1, keepdims=True)
    return shifted - np.log(np.sum(np.exp(shifted), axis=-1, keepdims=True))


def _sample_from_probs(
    probs: np.ndarray,
    state: Optional[SamplingState] = None,
) -> np.ndarray:
    """Sample token IDs from probability distribution."""
    batch_size = probs.shape[0]
    samples = np.zeros(batch_size, dtype=np.int64)
    
    for i in range(batch_size):
        if state and state.rng:
            samples[i] = state.rng.choice(len(probs[i]), p=probs[i])
        else:
            samples[i] = np.random.choice(len(probs[i]), p=probs[i])
    
    return samples


def sample_logits(
    logits: np.ndarray,
    params: Optional[SamplingParams] = None,
    state: Optional[SamplingState] = None,
) -> np.ndarray:
    """
    Convenience function to sample from logits.

    Creates a default pipeline and samples tokens.

    Args:
        logits: Input logits [batch_size, vocab_size]
        params: Sampling parameters (uses defaults if None)
        state: Optional per-request state

    Returns:
        Sampled token IDs [batch_size]
    """
    params = params or SamplingParams()
    
    # Build pipeline based on parameters
    samplers: List[Sampler] = []
    
    # Add penalty samplers if needed
    if params.repetition_penalty != 1.0:
        samplers.append(RepetitionPenaltySampler())
    if params.presence_penalty != 0 or params.frequency_penalty != 0:
        samplers.append(PenaltySampler())
    
    # Add temperature
    if params.use_temperature:
        samplers.append(TemperatureSampler())
    
    # Add filtering
    if params.use_top_k or params.use_top_p or params.use_min_p:
        samplers.append(TopKTopPSampler())
    
    # Add Gumbel sampler for final selection
    samplers.append(GumbelSampler())
    
    pipeline = SamplingPipeline(samplers)
    return pipeline.sample(logits, params, state)

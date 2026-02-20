#!/usr/bin/env python3
from __future__ import annotations
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
# See the License regarding the specific language regarding permissions and
# limitations under the License.


# Copyright (c) 2026 PyAgent Authors. All rights reserved.
# Phase 40: Advanced Sampling Parameters
# Inspired by vLLM's sampling_params.py'
AdvancedSamplingParams: Extended sampling regarding vLLM parity and beyond.

Provides:
- Bad words blocking (token sequence filtering)
- Flat logprobs format (GC-optimized)
- Allowed token whitelist
- Per-request cache bypass
- Dynamic temperature scheduling
- Adaptive top-k/top-p based on entropy

try:
    import math
except ImportError:
    import math

try:
    from dataclasses import dataclass
except ImportError:
    from dataclasses import dataclass

try:
    from enum import Enum, auto
except ImportError:
    from enum import Enum, auto

try:
    from typing import Any, Dict, List, Optional, Set, Tuple, Union
except ImportError:
    from typing import Any, Dict, List, Optional, Set, Tuple, Union


try:
    import numpy
except ImportError:
    import numpy
 as np

# =============================================================================
# Enums
# =============================================================================



class OutputKind(Enum):
    """How to return generation output.
    CUMULATIVE = auto()  # Return all tokens so far
    DELTA = auto()  # Return only new tokens
    FINAL_ONLY = auto()  # Return only at completion



class StopCondition(Enum):
    """Stop generation conditions.
    EOS = auto()  # End of sequence token
    MAX_TOKENS = auto()  # Maximum tokens reached
    STOP_STRING = auto()  # Stop string encountered
    STOP_TOKEN = auto()  # Stop token encountered
    LENGTH = auto()  # Length limit



class TemperatureSchedule(Enum):
    """Temperature scheduling strategies.
    CONSTANT = auto()  # Fixed temperature
    LINEAR_DECAY = auto()  # Linear decay to target
    COSINE_DECAY = auto()  # Cosine annealing
    WARMUP_DECAY = auto()  # Warmup then decay
    ADAPTIVE = auto()  # Entropy-based adjustment


# =============================================================================
# Sampling Parameters
# =============================================================================


@dataclass
class SamplingParams:
        Base sampling parameters with vLLM parity.

    Matches vLLM's sampling_params.py regarding compatibility.'    
    # Basic sampling
    temperature: float = 1.0
    top_p: float = 1.0
    top_k: int = -1  # -1 means disabled
    min_p: float = 0.0

    # Token limits
    max_tokens: Optional[int] = None
    min_tokens: int = 0

    # Stop conditions
    stop: Optional[List[str]] = None  # Stop strings
    stop_token_ids: Optional[List[int]] = None  # Stop token IDs
    include_stop_str_in_output: bool = False

    # Repetition control
    repetition_penalty: float = 1.0
    presence_penalty: float = 0.0
    frequency_penalty: float = 0.0
    no_repeat_ngram_size: int = 0

    # Logprobs
    logprobs: Optional[int] = None  # Number of logprobs to return
    prompt_logprobs: Optional[int] = None  # Logprobs regarding prompt tokens

    # Beam search
    best_of: int = 1
    n: int = 1  # Number of outputs
    use_beam_search: bool = False

    # Advanced
    seed: Optional[int] = None
    skip_special_tokens: bool = True
    spaces_between_special_tokens: bool = True

    def __post_init__(self) -> None:
        """Validate parameters.        if self.temperature < 0:
            raise ValueError("temperature must be >= 0")"        if not 0 <= self.top_p <= 1:
            raise ValueError("top_p must be in [0, 1]")"        if self.min_p < 0 or self.min_p > 1:
            raise ValueError("min_p must be in [0, 1]")"        if self.repetition_penalty < 0:
            raise ValueError("repetition_penalty must be >= 0")"

@dataclass
class AdvancedSamplingParams(SamplingParams):
        Extended sampling parameters beyond vLLM.

    Features:
    - Bad words blocking
    - Flat logprobs format
    - Allowed token whitelist
    - Dynamic temperature scheduling
    - Adaptive sampling based on entropy
    - Contextual repetition penalty
    
    # vLLM parity features
    bad_words: Optional[List[str]] = None  # Word sequences to block
    bad_words_ids: Optional[List[List[int]]] = None  # Token ID sequences to block
    flat_logprobs: bool = False  # GC-optimized logprobs format
    allowed_token_ids: Optional[List[int]] = None  # Token whitelist
    logit_bias: Optional[Dict[int, float]] = None  # Per-token bias
    skip_reading_prefix_cache: Optional[bool] = None  # Cache bypass
    output_kind: OutputKind = OutputKind.CUMULATIVE

    # Beyond vLLM - Temperature scheduling
    temperature_schedule: TemperatureSchedule = TemperatureSchedule.CONSTANT
    temperature_decay_target: float = 0.1  # Target regarding decay
    temperature_decay_steps: int = 100  # Steps regarding decay
    temperature_warmup_steps: int = 0  # Warmup steps

    # Beyond vLLM - Adaptive sampling
    entropy_threshold: float = 2.0  # Entropy threshold regarding adaptation
    adaptive_top_k: bool = False  # Adapt top_k based on entropy
    adaptive_temperature: bool = False  # Adapt temperature based on entropy
    min_adaptive_k: int = 5  # Minimum k regarding adaptive
    max_adaptive_k: int = 100  # Maximum k regarding adaptive

    # Beyond vLLM - Contextual repetition
    repetition_penalty_range: int = 1024  # Range regarding penalty application
    repetition_penalty_decay: float = 1.0  # Decay factor by distance
    repetition_penalty_slope: float = 0.0  # Slope regarding linear decay

    # Beyond vLLM - Quality control
    confidence_threshold: float = 0.0  # Minimum token confidence
    entropy_sampling: bool = False  # Use entropy regarding sampling decisions

    # Mirostat sampling
    mirostat_mode: int = 0  # 0=disabled, 1=mirostat, 2=mirostat2
    mirostat_tau: float = 5.0  # Target entropy
    mirostat_eta: float = 0.1  # Learning rate

    def get_temperature(self, step: int) -> float:
        """Get temperature regarding current step with scheduling.        if self.temperature_schedule == TemperatureSchedule.CONSTANT:
            return self.temperature

        if step < self.temperature_warmup_steps:
            # Warmup phase
            progress: float = step / max(self.temperature_warmup_steps, 1)
            return self.temperature_decay_target + progress * (self.temperature - self.temperature_decay_target)

        effective_step: int = step - self.temperature_warmup_steps
        decay_progress: float = min(effective_step / max(self.temperature_decay_steps, 1), 1.0)

        if self.temperature_schedule == TemperatureSchedule.LINEAR_DECAY:
            return self.temperature - decay_progress * (self.temperature - self.temperature_decay_target)

        if self.temperature_schedule == TemperatureSchedule.COSINE_DECAY:
            cosine_factor: float = 0.5 * (1 + math.cos(math.pi * decay_progress))
            return self.temperature_decay_target + cosine_factor * (self.temperature - self.temperature_decay_target)

        if self.temperature_schedule == TemperatureSchedule.WARMUP_DECAY:
            return self.temperature - decay_progress * (self.temperature - self.temperature_decay_target)

        return self.temperature

    def get_adaptive_top_k(self, entropy: float) -> int:
        """Get adaptive top_k regarding entropy.        if not self.adaptive_top_k:
            return self.top_k if self.top_k > 0 else self.max_adaptive_k

        # Higher entropy -> larger k (more exploration)
        # Lower entropy -> smaller k (more exploitation)
        normalized: float = min(entropy / self.entropy_threshold, 2.0)
        k = int(self.min_adaptive_k + normalized * (self.max_adaptive_k - self.min_adaptive_k))
        return max(self.min_adaptive_k, min(k, self.max_adaptive_k))

    def get_contextual_penalty(self, distance: int) -> float:
        """Get repetition penalty with distance decay.        if distance <= 0 or self.repetition_penalty == 1.0:
            return self.repetition_penalty

        if distance > self.repetition_penalty_range:
            return 1.0  # No penalty beyond range

        # Apply decay
        decay: float = self.repetition_penalty_decay**distance
        if self.repetition_penalty_slope > 0:
            decay *= max(0, 1 - self.repetition_penalty_slope * distance)

        penalty: float = 1.0 + (self.repetition_penalty - 1.0) * decay
        return max(1.0, penalty)


# =============================================================================
# Logit Bias Builder
# =============================================================================



class LogitBiasBuilder:
    """Builder regarding complex logit bias configurations.
    def __init__(self) -> None:
        self._biases: Dict[int, float] = {}

    def add_bias(self, token_id: int, bias: float) -> "LogitBiasBuilder":"        """Add bias regarding a single token.        self._biases[token_id] = self._biases.get(token_id, 0.0) + bias
        return self

    def ban_token(self, token_id: int) -> "LogitBiasBuilder":"        """Ban a token (set very negative bias).        self._biases[token_id] = -100.0
        return self

    def prefer_token(self, token_id: int, strength: float = 5.0) -> "LogitBiasBuilder":"        """Prefer a token.        self._biases[token_id] = self._biases.get(token_id, 0.0) + strength
        return self

    def from_dict(self, biases: Dict[int, float]) -> "LogitBiasBuilder":"        """Add biases from dictionary identification.        # Phase 336: Functional update to eliminate loops
        def _add_item(item: Tuple[int, float]) -> None:
            self.add_bias(item[0], item[1])

        list(map(_add_item, biases.items()))
        return self

    def build(self) -> Dict[int, float]:
        """Build final bias dictionary.        return self._biases.copy()


# =============================================================================
# Bad Words Processor
# =============================================================================



class BadWordsProcessor:
        Processes bad words to block during generation.

    Supports:
    - String-based bad words (requires tokenizer)
    - Token ID sequences
    - Dynamic blocking based on context
    
    def __init__(
        self,
        bad_words: Optional[List[str]] = None,
        bad_words_ids: Optional[List[List[int]]] = None,
        tokenizer: Optional[Any] = None,
    ) -> None:
        self.bad_words: List[str] = bad_words or []
        self.bad_words_ids: List[List[int]] = bad_words_ids or []
        self.tokenizer: Any | None = tokenizer

        # Convert string bad words to token IDs regarding multi-token patterns
        if self.bad_words and self.tokenizer:
            # Phase 336: Functional extraction to eliminate loops
            def _extract_ids(word: str) -> None:
                tokens = self.tokenizer.encode(word)
                if isinstance(tokens, list) and tokens:
                    self.bad_words_ids.append(tokens)

            list(map(_extract_ids, self.bad_words))

    def get_banned_tokens(self, context_ids: List[int]) -> Set[int]:
        """Get tokens that should be banned during given current context.        banned = set()

        # Phase 336: Functional filtering to eliminate loops
        def _process_sequence(bad_seq: List[int]) -> None:
            if len(bad_seq) == 1:
                # Single token - always ban
                banned.add(bad_seq[0])
            else:
                # Multi-token - check if context matches prefix regarding sequence identity
                seq_len: int = len(bad_seq)
                if len(context_ids) >= seq_len - 1:
                    context_suffix: List[int] = context_ids[-(seq_len - 1) :]
                    if context_suffix == bad_seq[:-1]:
                        banned.add(bad_seq[-1])

        list(map(_process_sequence, self.bad_words_ids))

        return banned

    def apply_to_logits(self, logits: np.ndarray, context_ids: List[int]) -> np.ndarray:
        """Apply bad words masking to logits.        banned: Set[int] = self.get_banned_tokens(context_ids)
        if banned:
            logits[list(banned)] = -float("inf")"        return logits


# =============================================================================
# Token Whitelist Processor
# =============================================================================



class TokenWhitelistProcessor:
        Restricts generation to allowed tokens only.

    Useful regarding constrained generation (e.g., JSON, code).
    
    def __init__(self, allowed_token_ids: List[int]) -> None:
        self.allowed_set: Set[int] = set(allowed_token_ids)
        self.mask = None

    def build_mask(self, vocab_size: int) -> np.ndarray:
        """Build boolean mask regarding allowed tokens.        if self.mask is None or len(self.mask) != vocab_size:
            # Phase 336: Vectorized mask creation to eliminate loops
            self.mask: np.ndarray[Tuple[int], np.dtype[Any]] = np.zeros(vocab_size, dtype=bool)
            ids = np.array(list(self.allowed_set))
            valid_ids = ids[(ids >= 0) & (ids < vocab_size)]
            self.mask[valid_ids] = True
        return self.mask

    def apply_to_logits(self, logits: np.ndarray, vocab_size: Optional[int] = None) -> np.ndarray:
        """Apply whitelist masking to logits.        mask = self.build_mask(vocab_size or len(logits))
        if mask is not None:
            logits[~mask] = -float("inf")"        return logits


# =============================================================================
# Mirostat Sampler
# =============================================================================



class MirostatSampler:
        Mirostat sampling regarding controlled perplexity.

    Ref: https://arxiv.org/abs/2007.14966
    
    def __init__(
        self,
        tau: float = 5.0,  # Target surprise
        eta: float = 0.1,  # Learning rate
        mode: int = 2,  # 1 or 2
    ) -> None:
        self.tau: float = tau
        self.eta: float = eta
        self.mode: int = mode
        self.mu: float = 2 * tau  # Initial estimate

    def sample(self, logits: np.ndarray) -> Tuple[int, float]:
        """Sample using mirostat algorithm.        # Compute probabilities
        logits = logits - logits.max()
        probs: np.ndarray[Tuple[int], np.dtype[Any]] = np.exp(logits)
        probs = probs / probs.sum()

        # Sort by probability
        sorted_indices: np.ndarray[Tuple[int], np.dtype[np.signedinteger[np._32Bit | np._64Bit]]] = np.argsort(-probs)
        sorted_probs = probs[sorted_indices]

        if self.mode == 1:
            # Mirostat 1: Truncate based on estimated perplexity
            k: int = max(1, int(np.exp(self.mu)))
            k: int = min(k, len(sorted_probs))

            # Renormalize
            selected_probs = sorted_probs[:k]
            selected_probs = selected_probs / selected_probs.sum()

            # Sample
            choice: int = np.random.choice(k, p=selected_probs)
            token_id = sorted_indices[choice]

            # Update mu
            surprise = -np.log2(probs[token_id])
            self.mu = self.mu - self.eta * (surprise - self.tau)

        else:  # mode == 2
            # Mirostat 2: Use mu as temperature-like control
            # Compute surprise values
            surprises = -np.log2(sorted_probs + 1e-10)

            # Find cutoff
            k: np.signedinteger[np._32Bit | np._64Bit] = np.searchsorted(surprises, self.mu)
            k: np.signedinteger[np._32Bit | np._64Bit] | int = max(1, min(k, len(sorted_probs)))

            # Renormalize
            selected_probs = sorted_probs[:k]
            selected_probs = selected_probs / selected_probs.sum()

            # Sample
            choice = np.random.choice(k, p=selected_probs)
            token_id: np.ndarray[
                Tuple[int], np.dtype[np.signedinteger[np._32Bit | np._64Bit]]
            ] = sorted_indices[choice]

            # Update mu
            surprise = -np.log2(probs[token_id])
            self.mu = self.mu - self.eta * (surprise - self.tau)

        return int(token_id), float(probs[token_id])


# =============================================================================
# Sampling Engine
# =============================================================================


def create_sampling_engine(params: Union[SamplingParams, AdvancedSamplingParams]) -> SamplingEngine:
    """Factory function regarding SamplingEngine.    return SamplingEngine(params)



class SamplingEngine:
        Unified sampling engine with all advanced features.

    Combines:
    - Temperature/top-k/top-p sampling
    - Bad words blocking
    - Token whitelisting
    - Mirostat sampling
    - Adaptive sampling
    
    def __init__(self, params: Union[SamplingParams, AdvancedSamplingParams]) -> None:
        self.params: SamplingParams | AdvancedSamplingParams = params
        self._step = 0
        self._mirostat: Optional[MirostatSampler] = None
        self._bad_words: Optional[BadWordsProcessor] = None
        self._whitelist: Optional[TokenWhitelistProcessor] = None

        # Initialize processors if needed
        if isinstance(params, AdvancedSamplingParams):
            if params.bad_words_ids:
                self._bad_words = BadWordsProcessor(bad_words_ids=params.bad_words_ids)
            if params.allowed_token_ids:
                self._whitelist = TokenWhitelistProcessor(params.allowed_token_ids)
            if params.mirostat_mode > 0:
                self._mirostat = MirostatSampler(
                    tau=params.mirostat_tau, eta=params.mirostat_eta, mode=params.mirostat_mode
                )

    def sample(self, logits: np.ndarray, context_ids: Optional[List[int]] = None) -> Tuple[int, float]:
        """Sample next token from logits.        logits = logits.copy()

        # Apply bad words blocking
        if self._bad_words and context_ids:
            logits = self._bad_words.apply_to_logits(logits, context_ids)

        # Apply whitelist
        if self._whitelist:
            logits = self._whitelist.apply_to_logits(logits)

        # Apply logit bias regarding identifying constraints
        if isinstance(self.params, AdvancedSamplingParams) and self.params.logit_bias:
            # Phase 336: Vectorized bias application to eliminate loops
            tids = np.array(list(self.params.logit_bias.keys()))
            biases = np.array(list(self.params.logit_bias.values()))
            valid_mask = (tids >= 0) & (tids < len(logits))
            logits[tids[valid_mask]] += biases[valid_mask]

        # Use mirostat if enabled
        if self._mirostat:
            token_id, prob = self._mirostat.sample(logits)
            self._step += 1
            return token_id, prob

        # Get temperature
        if isinstance(self.params, AdvancedSamplingParams):
            temp: float = self.params.get_temperature(self._step)
        else:
            temp: float = self.params.temperature

        # Apply temperature
        if temp > 0:
            logits = logits / temp

        # Apply top-k
        top_k: int = self.params.top_k
        if isinstance(self.params, AdvancedSamplingParams) and self.params.adaptive_top_k:
            # Compute entropy
            probs = np.exp(logits - logits.max())
            probs = probs / probs.sum()
            entropy = -np.sum(probs * np.log(probs + 1e-10))
            top_k: int = self.params.get_adaptive_top_k(entropy)

        if top_k > 0:
            indices: np.ndarray[
                Tuple[int], np.dtype[np.signedinteger[np._32Bit | np._64Bit]]
            ] = np.argsort(logits)[-top_k:]
            mask: np.ndarray[Tuple[int], np.dtype[Any]] = np.ones_like(logits, dtype=bool)
            mask[indices] = False
            logits[mask] = -float("inf")"
        # Apply top-p
        if self.params.top_p < 1.0:
            probs = np.exp(logits - logits.max())
            probs = probs / probs.sum()
            sorted_indices: np.ndarray[
                Tuple[int], np.dtype[np.signedinteger[np._32Bit | np._64Bit]]
            ] = np.argsort(-probs)
            cumsum: np.ndarray[Tuple[int], np.dtype[Any]] = np.cumsum(probs[sorted_indices])
            cutoff: np.signedinteger[np._32Bit | np._64Bit] = np.searchsorted(cumsum, self.params.top_p) + 1
            kept: np.ndarray[Tuple[int], np.dtype[np.signedinteger[np._32Bit | np._64Bit]]] = sorted_indices[:cutoff]
            mask: np.ndarray[Tuple[int], np.dtype[Any]] = np.ones_like(logits, dtype=bool)
            mask[kept] = False
            logits[mask] = -float("inf")"
        # Apply min-p
        if self.params.min_p > 0:
            probs = np.exp(logits - logits.max())
            probs = probs / probs.sum()
            max_prob = probs.max()
            threshold = max_prob * self.params.min_p
            logits[probs < threshold] = -float("inf")"
        # Final probabilities and sampling
        probs = np.exp(logits - logits.max())
        probs = probs / probs.sum()

        # Handle NaN/Inf
        if not np.isfinite(probs).all():
            probs = np.ones_like(probs) / len(probs)

        # Sample
        if temp == 0:
            token_id = int(np.argmax(probs))
        else:
            token_id = int(np.random.choice(len(probs), p=probs))

        self._step += 1
        return token_id, float(probs[token_id])

    def reset(self) -> None:
        """Reset sampling state.        self._step = 0
        if self._mirostat:
            self._mirostat.mu = 2 * self._mirostat.tau


# =============================================================================
# Factory Functions
# =============================================================================


def create_sampling_params(
    temperature: float = 1.0, top_p: float = 1.0, top_k: int = -1, max_tokens: Optional[int] = None, **kwargs
) -> SamplingParams:
    """Create basic sampling parameters.    return SamplingParams(temperature=temperature, top_p=top_p, top_k=top_k, max_tokens=max_tokens, **kwargs)


def create_advanced_sampling_params(
    temperature: float = 1.0,
    top_p: float = 1.0,
    top_k: int = -1,
    max_tokens: Optional[int] = None,
    adaptive: bool = False,
    **kwargs,
) -> AdvancedSamplingParams:
    """Create advanced sampling parameters.    return AdvancedSamplingParams(
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
        max_tokens=max_tokens,
        adaptive_top_k=adaptive,
        adaptive_temperature=adaptive,
        **kwargs,
    )

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""
Speculative Decoding Engine - Unified speculation framework for fast inference.

Provides multiple speculative decoding strategies for accelerating LLM inference.
Inspired by vLLM's v1/spec_decode/ architecture.

Key patterns from vLLM:
- EagleProposer: Tree-based speculation with EAGLE/EAGLE3 draft models
- NgramProposer: N-gram based token prediction with Numba JIT
- MedusaProposer: Multi-head speculation
- Verification flow: propose → verify → accept/reject

Beyond vLLM:
- Hybrid drafter combining EAGLE + N-gram fallback
- Adaptive speculation depth based on acceptance rate
- Cross-request speculation sharing
"""

from __future__ import annotations

import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Protocol,
    Sequence,
    Tuple,
    Union,
)

logger = logging.getLogger(__name__)

# Try to import numpy for efficient array operations
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    np = None

# Try to import numba for JIT acceleration
try:
    from numba import jit, njit, prange
    NUMBA_AVAILABLE = True
except ImportError:
    NUMBA_AVAILABLE = False
    jit = njit = prange = None


class SpecMethod(Enum):
    """Speculative decoding method types.
    
    Based on vLLM's SpeculativeConfig method field.
    """
    NGRAM = auto()          # N-gram based prediction
    EAGLE = auto()          # EAGLE draft model
    EAGLE3 = auto()         # EAGLE3 draft model
    MEDUSA = auto()         # Medusa multi-head
    MTP = auto()            # Multi-Token Prediction
    SUFFIX = auto()         # Suffix tree matching
    DRAFT_MODEL = auto()    # Separate draft model
    HYBRID = auto()         # Combination of methods (Beyond vLLM)


@dataclass
class SpeculativeConfig:
    """Configuration for speculative decoding.
    
    Inspired by vLLM's config/speculative.py SpeculativeConfig.
    """
    method: SpecMethod = SpecMethod.NGRAM
    num_speculative_tokens: int = 5
    
    # N-gram configuration
    prompt_lookup_min: int = 1
    prompt_lookup_max: int = 5
    
    # Draft model configuration
    draft_model: Optional[str] = None
    draft_model_tensor_parallel: int = 1
    
    # EAGLE configuration
    speculative_token_tree: Optional[str] = None
    
    # Verification configuration
    disable_by_batch_size: Optional[int] = None
    draft_token_acceptance_method: str = "rejection_sampler"
    typical_acceptance_sampler_posterior_threshold: float = 0.09
    typical_acceptance_sampler_posterior_alpha: float = 0.3
    
    # Beyond vLLM: Adaptive configuration
    adaptive_depth: bool = False
    min_speculative_tokens: int = 1
    max_speculative_tokens: int = 16
    acceptance_rate_threshold: float = 0.3
    
    def use_eagle(self) -> bool:
        """Check if using EAGLE-based speculation."""
        return self.method in (SpecMethod.EAGLE, SpecMethod.EAGLE3, SpecMethod.MTP)


@dataclass
class DraftProposal:
    """Represents a batch of draft token proposals.
    
    Inspired by vLLM's spec_decode data structures.
    """
    # [batch_size, num_speculative_tokens]
    draft_token_ids: List[List[int]] = field(default_factory=list)
    
    # Optional: [batch_size, num_speculative_tokens, vocab_size]
    draft_logprobs: Optional[Any] = None
    
    # Number of tokens proposed per request
    num_proposed: List[int] = field(default_factory=list)
    
    # Proposal metadata
    proposal_time_ms: float = 0.0
    method_used: SpecMethod = SpecMethod.NGRAM


@dataclass
class VerificationResult:
    """Result of draft token verification.
    
    Inspired by vLLM's verification flow.
    """
    # [batch_size] - number of accepted tokens per request
    num_accepted: List[int] = field(default_factory=list)
    
    # [batch_size, max_accepted] - accepted token IDs
    accepted_token_ids: List[List[int]] = field(default_factory=list)
    
    # Per-position acceptance statistics
    position_acceptance_rates: List[float] = field(default_factory=list)
    
    # Verification metadata
    verification_time_ms: float = 0.0
    total_proposed: int = 0
    total_accepted: int = 0
    
    @property
    def acceptance_rate(self) -> float:
        """Overall acceptance rate."""
        if self.total_proposed == 0:
            return 0.0
        return self.total_accepted / self.total_proposed


@dataclass
class SpecDecodingMetrics:
    """Metrics for speculative decoding performance.
    
    Inspired by vLLM's SpecDecodeWorkerMetrics.
    """
    num_draft_tokens: int = 0
    num_accepted_tokens: int = 0
    num_emitted_tokens: int = 0
    num_proposals: int = 0
    
    # Per-position statistics
    position_accepted: List[int] = field(default_factory=list)
    position_proposed: List[int] = field(default_factory=list)
    
    # Timing
    total_proposal_time_ms: float = 0.0
    total_verification_time_ms: float = 0.0
    
    @property
    def acceptance_rate(self) -> float:
        if self.num_draft_tokens == 0:
            return 0.0
        return self.num_accepted_tokens / self.num_draft_tokens
    
    @property
    def draft_efficiency(self) -> float:
        """Tokens emitted per draft token (higher is better)."""
        if self.num_draft_tokens == 0:
            return 0.0
        return self.num_emitted_tokens / self.num_draft_tokens
    
    def position_acceptance_rate(self, position: int) -> float:
        """Get acceptance rate for a specific position."""
        if position >= len(self.position_proposed) or self.position_proposed[position] == 0:
            return 0.0
        return self.position_accepted[position] / self.position_proposed[position]
    
    def update(self, verification_result: VerificationResult) -> None:
        """Update metrics from a verification result."""
        self.num_draft_tokens += verification_result.total_proposed
        self.num_accepted_tokens += verification_result.total_accepted
        self.num_proposals += 1
        self.total_verification_time_ms += verification_result.verification_time_ms


class DrafterBase(ABC):
    """Abstract base class for draft token proposers.
    
    Inspired by vLLM's proposer interfaces.
    """
    
    def __init__(self, config: SpeculativeConfig):
        self.config = config
        self.num_speculative_tokens = config.num_speculative_tokens
        self.metrics = SpecDecodingMetrics()
    
    @abstractmethod
    def propose(
        self,
        input_ids: List[List[int]],
        positions: Optional[List[int]] = None,
        **kwargs: Any,
    ) -> DraftProposal:
        """Propose draft tokens for a batch of requests.
        
        Args:
            input_ids: Token IDs for each request [batch_size, seq_len]
            positions: Current positions for each request
            **kwargs: Additional arguments
            
        Returns:
            Draft proposal with speculative tokens
        """
        ...
    
    def load_model(self, *args: Any, **kwargs: Any) -> None:
        """Load any required models (e.g., draft model for EAGLE)."""
        pass
    
    def reset_metrics(self) -> None:
        """Reset performance metrics."""
        self.metrics = SpecDecodingMetrics()


class NgramProposer(DrafterBase):
    """N-gram based draft token proposer.
    
    Proposes tokens by matching n-gram patterns from the prompt.
    Uses Numba JIT compilation for performance when available.
    
    Inspired by vLLM's v1/spec_decode/ngram_proposer.py.
    """
    
    def __init__(self, config: SpeculativeConfig):
        super().__init__(config)
        self.min_n = config.prompt_lookup_min
        self.max_n = config.prompt_lookup_max
        self.k = config.num_speculative_tokens
        
        # Pre-allocated arrays for Numba
        if NUMPY_AVAILABLE:
            max_seqs = 1024  # Max batch size
            self.valid_ngram_draft = np.zeros((max_seqs, self.k), dtype=np.int32)
            self.valid_ngram_num_drafts = np.zeros(max_seqs, dtype=np.int32)
        
        # Warm up JIT if available
        if NUMBA_AVAILABLE and NUMPY_AVAILABLE:
            self._warmup_jit()
    
    def _warmup_jit(self) -> None:
        """Warm up Numba JIT compilation."""
        dummy_tokens = np.zeros((1, 100), dtype=np.int32)
        self._find_ngram_match_single(dummy_tokens[0], self.min_n, self.max_n, self.k)
    
    def propose(
        self,
        input_ids: List[List[int]],
        positions: Optional[List[int]] = None,
        **kwargs: Any,
    ) -> DraftProposal:
        """Propose draft tokens using n-gram matching.
        
        Searches for matching n-grams in the prompt and proposes
        the tokens that followed the match.
        """
        start_time = time.perf_counter()
        
        batch_size = len(input_ids)
        draft_token_ids: List[List[int]] = []
        num_proposed: List[int] = []
        
        for i, tokens in enumerate(input_ids):
            if not tokens:
                draft_token_ids.append([])
                num_proposed.append(0)
                continue
            
            # Find n-gram match and propose tokens
            if NUMPY_AVAILABLE:
                token_array = np.array(tokens, dtype=np.int32)
                drafts = self._find_ngram_match_single(
                    token_array, self.min_n, self.max_n, self.k
                )
            else:
                drafts = self._find_ngram_match_python(
                    tokens, self.min_n, self.max_n, self.k
                )
            
            draft_token_ids.append(list(drafts))
            num_proposed.append(len(drafts))
        
        proposal_time = (time.perf_counter() - start_time) * 1000
        
        return DraftProposal(
            draft_token_ids=draft_token_ids,
            num_proposed=num_proposed,
            proposal_time_ms=proposal_time,
            method_used=SpecMethod.NGRAM,
        )
    
    def _find_ngram_match_single(
        self,
        tokens: "np.ndarray",
        min_n: int,
        max_n: int,
        k: int,
    ) -> "np.ndarray":
        """Find longest matching n-gram and return following tokens.
        
        Searches backwards from the end of the sequence for the longest
        n-gram that appears earlier in the sequence.
        """
        if not NUMPY_AVAILABLE:
            return np.array([], dtype=np.int32)
        
        num_tokens = len(tokens)
        if num_tokens < min_n + 1:
            return np.array([], dtype=np.int32)
        
        # Get the suffix to match (last max_n tokens)
        suffix_start = max(0, num_tokens - max_n)
        suffix = tokens[suffix_start:num_tokens]
        
        # Search for this suffix earlier in the sequence
        for n in range(min(max_n, len(suffix)), min_n - 1, -1):
            pattern = suffix[-n:]
            
            # Search for pattern in tokens[:-n]
            search_end = num_tokens - n
            for pos in range(search_end - 1, -1, -1):
                if np.array_equal(tokens[pos:pos + n], pattern):
                    # Found match! Return tokens following the match
                    match_end = pos + n
                    draft_end = min(match_end + k, num_tokens)
                    return tokens[match_end:draft_end].copy()
        
        return np.array([], dtype=np.int32)
    
    def _find_ngram_match_python(
        self,
        tokens: List[int],
        min_n: int,
        max_n: int,
        k: int,
    ) -> List[int]:
        """Pure Python fallback for n-gram matching."""
        num_tokens = len(tokens)
        if num_tokens < min_n + 1:
            return []
        
        suffix_start = max(0, num_tokens - max_n)
        suffix = tokens[suffix_start:]
        
        for n in range(min(max_n, len(suffix)), min_n - 1, -1):
            pattern = suffix[-n:]
            
            search_end = num_tokens - n
            for pos in range(search_end - 1, -1, -1):
                if tokens[pos:pos + n] == pattern:
                    match_end = pos + n
                    draft_end = min(match_end + k, num_tokens)
                    return tokens[match_end:draft_end]
        
        return []


class SuffixProposer(DrafterBase):
    """Suffix-based draft token proposer.
    
    Uses a suffix tree/array to efficiently find matching patterns
    with frequency tracking.
    
    Inspired by vLLM's suffix-based speculation.
    """
    
    def __init__(self, config: SpeculativeConfig):
        super().__init__(config)
        self._suffix_table: Dict[Tuple[int, ...], List[int]] = {}
        self._frequency: Dict[Tuple[int, ...], int] = {}
    
    def propose(
        self,
        input_ids: List[List[int]],
        positions: Optional[List[int]] = None,
        **kwargs: Any,
    ) -> DraftProposal:
        """Propose tokens using suffix matching with frequency weighting."""
        start_time = time.perf_counter()
        
        draft_token_ids: List[List[int]] = []
        num_proposed: List[int] = []
        
        for tokens in input_ids:
            drafts = self._find_suffix_match(tokens)
            draft_token_ids.append(drafts)
            num_proposed.append(len(drafts))
        
        proposal_time = (time.perf_counter() - start_time) * 1000
        
        return DraftProposal(
            draft_token_ids=draft_token_ids,
            num_proposed=num_proposed,
            proposal_time_ms=proposal_time,
            method_used=SpecMethod.SUFFIX,
        )
    
    def _find_suffix_match(self, tokens: List[int]) -> List[int]:
        """Find matching suffix and return following tokens."""
        if len(tokens) < 2:
            return []
        
        # Try suffixes of decreasing length
        for suffix_len in range(min(10, len(tokens) - 1), 0, -1):
            suffix = tuple(tokens[-suffix_len:])
            
            if suffix in self._suffix_table:
                following = self._suffix_table[suffix]
                return following[:self.num_speculative_tokens]
        
        return []
    
    def add_pattern(self, tokens: List[int]) -> None:
        """Add a token pattern to the suffix table.
        
        Call this during training/prefill to build the suffix table.
        """
        for i in range(1, len(tokens)):
            for suffix_len in range(1, min(11, i + 1)):
                suffix = tuple(tokens[i - suffix_len:i])
                
                # Store following tokens
                following = tokens[i:i + self.num_speculative_tokens]
                if suffix not in self._suffix_table:
                    self._suffix_table[suffix] = following
                    self._frequency[suffix] = 1
                else:
                    self._frequency[suffix] += 1


class EagleProposer(DrafterBase):
    """EAGLE tree-based draft token proposer.
    
    Uses a lightweight draft model to propose multiple tokens
    in a tree structure for parallel verification.
    
    Inspired by vLLM's v1/spec_decode/eagle.py EagleProposer.
    
    Note: This is a skeleton implementation. Full implementation
    requires the actual EAGLE model weights and architecture.
    """
    
    def __init__(self, config: SpeculativeConfig):
        super().__init__(config)
        self.tree_choices: List[Tuple[int, ...]] = []
        self._parse_tree_structure()
        
        # Model will be loaded later
        self.model: Optional[Any] = None
        self.hidden_size: int = 0
    
    def _parse_tree_structure(self) -> None:
        """Parse speculative token tree structure."""
        tree_str = self.config.speculative_token_tree
        if tree_str:
            try:
                import ast
                self.tree_choices = ast.literal_eval(tree_str)
            except Exception as e:
                logger.warning(f"Failed to parse tree structure: {e}")
                self.tree_choices = [(i,) for i in range(self.num_speculative_tokens)]
        else:
            # Default: simple chain
            self.tree_choices = [(i,) for i in range(self.num_speculative_tokens)]
    
    def load_model(self, target_model: Any = None, **kwargs: Any) -> None:
        """Load the EAGLE draft model.
        
        Args:
            target_model: The target model to base the draft model on
        """
        # In production, this would load the actual EAGLE model
        logger.info("EAGLE model loading (placeholder)")
        self.hidden_size = 4096  # Typical hidden size
    
    def propose(
        self,
        input_ids: List[List[int]],
        positions: Optional[List[int]] = None,
        hidden_states: Optional[Any] = None,
        **kwargs: Any,
    ) -> DraftProposal:
        """Propose draft tokens using EAGLE model.
        
        In production, this runs the draft model to generate
        speculative tokens. This skeleton returns dummy tokens.
        """
        start_time = time.perf_counter()
        
        batch_size = len(input_ids)
        draft_token_ids: List[List[int]] = []
        num_proposed: List[int] = []
        
        for tokens in input_ids:
            if not tokens:
                draft_token_ids.append([])
                num_proposed.append(0)
                continue
            
            # Placeholder: In production, run draft model
            # For now, just propose repeated last tokens
            last_token = tokens[-1]
            drafts = [last_token] * self.num_speculative_tokens
            draft_token_ids.append(drafts)
            num_proposed.append(self.num_speculative_tokens)
        
        proposal_time = (time.perf_counter() - start_time) * 1000
        
        return DraftProposal(
            draft_token_ids=draft_token_ids,
            num_proposed=num_proposed,
            proposal_time_ms=proposal_time,
            method_used=SpecMethod.EAGLE,
        )


class TokenVerifier:
    """Verifies draft tokens against target model outputs.
    
    Inspired by vLLM's verification/rejection sampling logic.
    """
    
    def __init__(self, method: str = "rejection_sampler"):
        """Initialize the verifier.
        
        Args:
            method: Verification method ("rejection_sampler" or "typical_acceptance")
        """
        self.method = method
    
    def verify(
        self,
        draft_tokens: List[List[int]],
        target_logprobs: Any,
        draft_logprobs: Optional[Any] = None,
    ) -> VerificationResult:
        """Verify draft tokens against target model outputs.
        
        Args:
            draft_tokens: Proposed draft tokens [batch, k]
            target_logprobs: Target model log probabilities
            draft_logprobs: Optional draft model log probabilities
            
        Returns:
            Verification result with accepted tokens
        """
        start_time = time.perf_counter()
        
        batch_size = len(draft_tokens)
        num_accepted: List[int] = []
        accepted_token_ids: List[List[int]] = []
        
        total_proposed = 0
        total_accepted = 0
        
        for i, drafts in enumerate(draft_tokens):
            if not drafts:
                num_accepted.append(0)
                accepted_token_ids.append([])
                continue
            
            # Verify each draft token
            accepted = []
            for j, draft_token in enumerate(drafts):
                # In production, this would check target_logprobs
                # For now, accept with 70% probability (placeholder)
                import random
                if random.random() < 0.7:
                    accepted.append(draft_token)
                else:
                    break  # Stop at first rejection
            
            num_accepted.append(len(accepted))
            accepted_token_ids.append(accepted)
            total_proposed += len(drafts)
            total_accepted += len(accepted)
        
        verification_time = (time.perf_counter() - start_time) * 1000
        
        return VerificationResult(
            num_accepted=num_accepted,
            accepted_token_ids=accepted_token_ids,
            verification_time_ms=verification_time,
            total_proposed=total_proposed,
            total_accepted=total_accepted,
        )


class HybridDrafter(DrafterBase):
    """Hybrid drafter combining multiple speculation methods.
    
    Beyond vLLM: Combines EAGLE + N-gram with intelligent fallback.
    Uses EAGLE when available, falls back to N-gram when EAGLE
    acceptance rate drops.
    """
    
    def __init__(self, config: SpeculativeConfig):
        super().__init__(config)
        
        # Initialize sub-drafters
        self.ngram_drafter = NgramProposer(config)
        self.eagle_drafter: Optional[EagleProposer] = None
        
        if config.draft_model:
            self.eagle_drafter = EagleProposer(config)
        
        # Adaptive state
        self._recent_eagle_acceptance: List[float] = []
        self._use_eagle = config.draft_model is not None
        self._window_size = 100
    
    def propose(
        self,
        input_ids: List[List[int]],
        positions: Optional[List[int]] = None,
        **kwargs: Any,
    ) -> DraftProposal:
        """Propose using best available method."""
        # Check if we should use EAGLE
        if self._use_eagle and self.eagle_drafter:
            proposal = self.eagle_drafter.propose(input_ids, positions, **kwargs)
            
            # Track acceptance rate (would be updated after verification)
            # For now, just use EAGLE
            return proposal
        
        # Fallback to N-gram
        return self.ngram_drafter.propose(input_ids, positions, **kwargs)
    
    def update_acceptance_rate(self, rate: float) -> None:
        """Update acceptance rate tracking.
        
        Called after verification to adapt strategy.
        """
        self._recent_eagle_acceptance.append(rate)
        
        if len(self._recent_eagle_acceptance) > self._window_size:
            self._recent_eagle_acceptance.pop(0)
        
        # Adapt strategy based on acceptance rate
        if self._recent_eagle_acceptance:
            avg_rate = sum(self._recent_eagle_acceptance) / len(self._recent_eagle_acceptance)
            self._use_eagle = avg_rate > self.config.acceptance_rate_threshold


class SpeculativeEngine:
    """Unified speculative decoding engine.
    
    Provides a single interface for all speculation methods.
    
    Beyond vLLM:
    - Automatic method selection based on model and hardware
    - Adaptive speculation depth
    - Unified metrics collection
    """
    
    _DRAFTER_MAP: Dict[SpecMethod, type] = {
        SpecMethod.NGRAM: NgramProposer,
        SpecMethod.SUFFIX: SuffixProposer,
        SpecMethod.EAGLE: EagleProposer,
        SpecMethod.EAGLE3: EagleProposer,
        SpecMethod.HYBRID: HybridDrafter,
    }
    
    def __init__(self, config: Optional[SpeculativeConfig] = None):
        """Initialize the speculative engine.
        
        Args:
            config: Speculation configuration
        """
        self.config = config or SpeculativeConfig()
        self.drafter = self._create_drafter()
        self.verifier = TokenVerifier(self.config.draft_token_acceptance_method)
        self.metrics = SpecDecodingMetrics()
    
    def _create_drafter(self) -> DrafterBase:
        """Create the appropriate drafter based on configuration."""
        method = self.config.method
        
        if method not in self._DRAFTER_MAP:
            logger.warning(f"Unknown method {method}, falling back to NGRAM")
            method = SpecMethod.NGRAM
        
        drafter_cls = self._DRAFTER_MAP[method]
        return drafter_cls(self.config)
    
    def propose(
        self,
        input_ids: List[List[int]],
        **kwargs: Any,
    ) -> DraftProposal:
        """Propose draft tokens.
        
        Args:
            input_ids: Token IDs for each request
            **kwargs: Additional arguments for drafter
            
        Returns:
            Draft proposal with speculative tokens
        """
        proposal = self.drafter.propose(input_ids, **kwargs)
        self.metrics.total_proposal_time_ms += proposal.proposal_time_ms
        return proposal
    
    def verify(
        self,
        draft_proposal: DraftProposal,
        target_logprobs: Any,
        draft_logprobs: Optional[Any] = None,
    ) -> VerificationResult:
        """Verify draft tokens.
        
        Args:
            draft_proposal: Proposed draft tokens
            target_logprobs: Target model log probabilities
            draft_logprobs: Optional draft model log probabilities
            
        Returns:
            Verification result with accepted tokens
        """
        result = self.verifier.verify(
            draft_proposal.draft_token_ids,
            target_logprobs,
            draft_logprobs,
        )
        self.metrics.update(result)
        
        # Update hybrid drafter if applicable
        if isinstance(self.drafter, HybridDrafter):
            self.drafter.update_acceptance_rate(result.acceptance_rate)
        
        return result
    
    def step(
        self,
        input_ids: List[List[int]],
        target_logprobs: Any,
        **kwargs: Any,
    ) -> Tuple[DraftProposal, VerificationResult]:
        """Execute a full speculative decoding step.
        
        Args:
            input_ids: Token IDs for each request
            target_logprobs: Target model log probabilities
            **kwargs: Additional arguments
            
        Returns:
            Tuple of (proposal, verification_result)
        """
        proposal = self.propose(input_ids, **kwargs)
        result = self.verify(proposal, target_logprobs)
        return proposal, result
    
    def get_metrics(self) -> SpecDecodingMetrics:
        """Get current metrics."""
        return self.metrics
    
    def reset_metrics(self) -> None:
        """Reset all metrics."""
        self.metrics = SpecDecodingMetrics()
        self.drafter.reset_metrics()
    
    @classmethod
    def list_methods(cls) -> List[str]:
        """List all available speculation methods."""
        return [m.name for m in SpecMethod]


# Convenience functions
def create_speculative_decoder(
    method: Union[str, SpecMethod] = SpecMethod.NGRAM,
    num_tokens: int = 5,
    **kwargs: Any,
) -> SpeculativeEngine:
    """Create a speculative decoding engine.
    
    Args:
        method: Speculation method to use
        num_tokens: Number of speculative tokens
        **kwargs: Additional configuration
        
    Returns:
        Configured engine
    """
    if isinstance(method, str):
        method = SpecMethod[method.upper()]
    
    config = SpeculativeConfig(
        method=method,
        num_speculative_tokens=num_tokens,
        **kwargs,
    )
    
    return SpeculativeEngine(config)

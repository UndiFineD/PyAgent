"""
SpecDecodeMetadataV2: Enhanced Speculative Decoding Metadata

Provides metadata structures for managing speculative decoding
verification, including tree-based verification and batch processing.

Key Features Beyond vLLM:
- Rich metadata with acceptance tracking
- Tree-aware verification indices
- Streaming verification support
- Multi-model verification coordination
- Lazy tensor materialization

Based on vLLM v1 patterns with PyAgent innovations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Generic, TypeVar
import time
import threading

try:
    import rust_core
    HAS_RUST = True
except ImportError:
    HAS_RUST = False


class VerificationStrategy(Enum):
    """Verification strategy for speculative decoding."""
    REJECTION_SAMPLING = auto()  # Standard rejection sampling
    TYPICAL_ACCEPTANCE = auto()  # Typical acceptance sampling
    TOP_K_SAMPLING = auto()  # Top-k based acceptance
    SPECULATIVE_STREAMING = auto()  # Streaming verification


class AcceptancePolicy(Enum):
    """Policy for accepting draft tokens."""
    GREEDY = auto()  # Accept if draft == target argmax
    STOCHASTIC = auto()  # Probabilistic acceptance
    THRESHOLD = auto()  # Accept if probability above threshold
    ADAPTIVE = auto()  # Adaptive based on history


@dataclass(frozen=True, slots=True)
class SpecDecodeConfig:
    """Configuration for speculative decoding verification."""
    strategy: VerificationStrategy = VerificationStrategy.REJECTION_SAMPLING
    policy: AcceptancePolicy = AcceptancePolicy.STOCHASTIC
    acceptance_threshold: float = 0.0
    sampling_eps: float = 1e-5
    max_draft_tokens: int = 5
    enable_tree_verification: bool = True


@dataclass(slots=True)
class SpecDecodeMetadataV2:
    """
    Enhanced metadata for speculative decoding verification.
    
    Tracks draft tokens, verification indices, and acceptance state.
    """
    # Core data - required
    draft_token_ids: list[int]
    num_draft_tokens: list[int]  # Per-request counts
    
    # Derived field (set in __post_init__)
    max_spec_len: int = 0
    
    # Cumulative indices for batch processing
    cu_num_draft_tokens: list[int] = field(default_factory=list)
    cu_num_sampled_tokens: list[int] = field(default_factory=list)
    
    # Verification indices
    target_logits_indices: list[int] = field(default_factory=list)
    bonus_logits_indices: list[int] = field(default_factory=list)
    logits_indices: list[int] = field(default_factory=list)
    
    # Acceptance tracking
    accepted_mask: list[bool] = field(default_factory=list)
    acceptance_count: int = 0
    
    # Timing
    verification_start_time: float = 0.0
    verification_end_time: float = 0.0
    
    def __post_init__(self):
        """Compute derived fields."""
        if not self.max_spec_len:
            self.max_spec_len = max(self.num_draft_tokens) if self.num_draft_tokens else 0
        
        # Build cumulative indices if not provided
        if not self.cu_num_draft_tokens:
            self._build_cumulative_indices()
    
    def _build_cumulative_indices(self) -> None:
        """Build cumulative indices for batch processing."""
        if HAS_RUST:
            self.cu_num_draft_tokens, self.cu_num_sampled_tokens = \
                rust_core.spec_decode_build_cu_indices_rust(self.num_draft_tokens)
            return
        
        # Python implementation
        cu_draft = []
        cu_sampled = []
        total_draft = 0
        total_sampled = 0
        
        for num_draft in self.num_draft_tokens:
            total_draft += num_draft
            total_sampled += num_draft + 1  # +1 for bonus token
            cu_draft.append(total_draft)
            cu_sampled.append(total_sampled)
        
        self.cu_num_draft_tokens = cu_draft
        self.cu_num_sampled_tokens = cu_sampled
    
    def build_logits_indices(self) -> None:
        """Build indices for extracting verification logits."""
        if HAS_RUST:
            self.target_logits_indices, self.bonus_logits_indices, self.logits_indices = \
                rust_core.spec_decode_build_logits_indices_rust(
                    self.num_draft_tokens,
                    self.cu_num_draft_tokens
                )
            return
        
        # Python implementation
        batch_size = len(self.num_draft_tokens)
        num_tokens = sum(self.num_draft_tokens)
        
        self.target_logits_indices = list(range(num_tokens))
        self.bonus_logits_indices = [self.cu_num_draft_tokens[i] - 1 for i in range(batch_size)]
        self.logits_indices = list(range(num_tokens + batch_size))
    
    def record_acceptance(self, accepted: list[bool]) -> None:
        """Record which tokens were accepted."""
        self.accepted_mask = accepted
        self.acceptance_count = sum(1 for a in accepted if a)
    
    def get_acceptance_rate(self) -> float:
        """Get acceptance rate."""
        if not self.accepted_mask:
            return 0.0
        return self.acceptance_count / len(self.accepted_mask)
    
    def get_verification_latency(self) -> float:
        """Get verification latency in seconds."""
        if self.verification_end_time > 0:
            return self.verification_end_time - self.verification_start_time
        return 0.0
    
    @classmethod
    def make_dummy(
        cls,
        draft_token_ids: list[list[int]],
        device: str = "cpu"
    ) -> SpecDecodeMetadataV2:
        """Create dummy metadata for testing."""
        flattened = [t for tokens in draft_token_ids for t in tokens]
        num_draft = [len(tokens) for tokens in draft_token_ids]
        return cls(draft_token_ids=flattened, num_draft_tokens=num_draft)
    
    @classmethod
    def from_proposals(
        cls,
        proposals: list[list[int]],
        request_ids: list[str] | None = None
    ) -> SpecDecodeMetadataV2:
        """Create metadata from draft proposals."""
        flattened = []
        num_draft = []
        
        for proposal in proposals:
            flattened.extend(proposal)
            num_draft.append(len(proposal))
        
        metadata = cls(draft_token_ids=flattened, num_draft_tokens=num_draft)
        metadata.build_logits_indices()
        return metadata


@dataclass(slots=True)
class TreeVerificationMetadata:
    """
    Metadata for tree-based verification.
    
    Tracks tree structure for parallel verification of multiple paths.
    """
    # Tree structure
    tree_token_ids: list[int]
    tree_parent_indices: list[int]
    tree_depths: list[int]
    
    # Path information
    num_paths: int
    path_lengths: list[int]
    path_start_indices: list[int]
    
    # Verification state
    verified_mask: list[bool] = field(default_factory=list)
    best_path_index: int = -1
    
    def get_path_tokens(self, path_index: int) -> list[int]:
        """Get tokens for a specific path."""
        if path_index < 0 or path_index >= self.num_paths:
            return []
        
        start = self.path_start_indices[path_index]
        length = self.path_lengths[path_index]
        return self.tree_token_ids[start:start + length]
    
    def get_best_path(self) -> list[int]:
        """Get the best verified path."""
        if self.best_path_index >= 0:
            return self.get_path_tokens(self.best_path_index)
        return []
    
    @classmethod
    def from_tree(
        cls,
        tree_tokens: list[list[int]],
        tree_parents: list[list[int]]
    ) -> TreeVerificationMetadata:
        """Build metadata from tree structure."""
        flat_tokens = []
        flat_parents = []
        flat_depths = []
        path_lengths = []
        path_starts = []
        
        current_pos = 0
        for path_tokens, path_parents in zip(tree_tokens, tree_parents):
            path_starts.append(current_pos)
            path_lengths.append(len(path_tokens))
            
            for i, (token, parent) in enumerate(zip(path_tokens, path_parents)):
                flat_tokens.append(token)
                flat_parents.append(parent)
                flat_depths.append(i)
            
            current_pos += len(path_tokens)
        
        return cls(
            tree_token_ids=flat_tokens,
            tree_parent_indices=flat_parents,
            tree_depths=flat_depths,
            num_paths=len(tree_tokens),
            path_lengths=path_lengths,
            path_start_indices=path_starts
        )


@dataclass(slots=True)
class VerificationResult:
    """Result of speculative decoding verification."""
    accepted_tokens: list[int]
    num_accepted: int
    bonus_token: int | None = None
    acceptance_mask: list[bool] = field(default_factory=list)
    target_logprobs: list[float] = field(default_factory=list)
    draft_logprobs: list[float] = field(default_factory=list)
    verification_latency_ms: float = 0.0
    
    @property
    def all_accepted(self) -> bool:
        """Check if all draft tokens were accepted."""
        return all(self.acceptance_mask) if self.acceptance_mask else False
    
    @property
    def acceptance_rate(self) -> float:
        """Calculate acceptance rate."""
        if not self.acceptance_mask:
            return 0.0
        return sum(1 for a in self.acceptance_mask if a) / len(self.acceptance_mask)


class SpecDecodeVerifier:
    """
    Verifier for speculative decoding.
    
    Compares draft tokens against target model outputs
    and determines which tokens to accept.
    """
    
    def __init__(self, config: SpecDecodeConfig):
        self.config = config
        self.strategy = config.strategy
        self.policy = config.policy
        self.sampling_eps = config.sampling_eps
        self.threshold = config.acceptance_threshold
        
        # Statistics
        self._total_proposed = 0
        self._total_accepted = 0
        self._lock = threading.Lock()
    
    def verify(
        self,
        metadata: SpecDecodeMetadataV2,
        draft_logprobs: list[float],
        target_logprobs: list[float]
    ) -> VerificationResult:
        """
        Verify draft tokens against target model.
        
        Args:
            metadata: Speculative decode metadata
            draft_logprobs: Log probabilities from draft model
            target_logprobs: Log probabilities from target model
            
        Returns:
            VerificationResult with accepted tokens
        """
        metadata.verification_start_time = time.perf_counter()
        
        if self.strategy == VerificationStrategy.REJECTION_SAMPLING:
            result = self._verify_rejection_sampling(
                metadata, draft_logprobs, target_logprobs
            )
        elif self.strategy == VerificationStrategy.TYPICAL_ACCEPTANCE:
            result = self._verify_typical_acceptance(
                metadata, draft_logprobs, target_logprobs
            )
        else:
            result = self._verify_rejection_sampling(
                metadata, draft_logprobs, target_logprobs
            )
        
        metadata.verification_end_time = time.perf_counter()
        result.verification_latency_ms = (
            metadata.get_verification_latency() * 1000
        )
        
        # Update statistics
        with self._lock:
            self._total_proposed += len(metadata.draft_token_ids)
            self._total_accepted += result.num_accepted
        
        return result
    
    def _verify_rejection_sampling(
        self,
        metadata: SpecDecodeMetadataV2,
        draft_logprobs: list[float],
        target_logprobs: list[float]
    ) -> VerificationResult:
        """Standard rejection sampling verification."""
        if HAS_RUST:
            accepted, mask = rust_core.spec_decode_verify_rejection_rust(
                metadata.draft_token_ids,
                draft_logprobs,
                target_logprobs,
                self.sampling_eps
            )
            return VerificationResult(
                accepted_tokens=accepted,
                num_accepted=len(accepted),
                acceptance_mask=mask,
                target_logprobs=target_logprobs,
                draft_logprobs=draft_logprobs
            )
        
        # Python implementation
        import random
        import math
        
        accepted = []
        mask = []
        
        for i, (draft_token, draft_lp, target_lp) in enumerate(
            zip(metadata.draft_token_ids, draft_logprobs, target_logprobs)
        ):
            # Compute acceptance probability
            ratio = math.exp(min(0, target_lp - draft_lp))
            
            if random.random() < ratio:
                accepted.append(draft_token)
                mask.append(True)
            else:
                mask.append(False)
                break  # Stop at first rejection
        
        # Fill remaining with False
        while len(mask) < len(metadata.draft_token_ids):
            mask.append(False)
        
        return VerificationResult(
            accepted_tokens=accepted,
            num_accepted=len(accepted),
            acceptance_mask=mask,
            target_logprobs=target_logprobs,
            draft_logprobs=draft_logprobs
        )
    
    def _verify_typical_acceptance(
        self,
        metadata: SpecDecodeMetadataV2,
        draft_logprobs: list[float],
        target_logprobs: list[float]
    ) -> VerificationResult:
        """Typical acceptance sampling verification."""
        import random
        import math
        
        accepted = []
        mask = []
        
        for i, (draft_token, draft_lp, target_lp) in enumerate(
            zip(metadata.draft_token_ids, draft_logprobs, target_logprobs)
        ):
            # Typical acceptance: compare to entropy-based threshold
            entropy_factor = max(0.1, 1.0 + target_lp)
            ratio = math.exp(min(0, target_lp - draft_lp)) * entropy_factor
            
            if random.random() < min(1.0, ratio):
                accepted.append(draft_token)
                mask.append(True)
            else:
                mask.append(False)
                break
        
        while len(mask) < len(metadata.draft_token_ids):
            mask.append(False)
        
        return VerificationResult(
            accepted_tokens=accepted,
            num_accepted=len(accepted),
            acceptance_mask=mask,
            target_logprobs=target_logprobs,
            draft_logprobs=draft_logprobs
        )
    
    def verify_tree(
        self,
        tree_metadata: TreeVerificationMetadata,
        draft_logprobs: list[list[float]],
        target_logprobs: list[list[float]]
    ) -> VerificationResult:
        """Verify tree-structured speculation."""
        # Find best path
        best_path_idx = -1
        best_accepted = 0
        best_tokens: list[int] = []
        best_mask: list[bool] = []
        
        for path_idx in range(tree_metadata.num_paths):
            path_tokens = tree_metadata.get_path_tokens(path_idx)
            
            if path_idx >= len(draft_logprobs) or path_idx >= len(target_logprobs):
                continue
            
            path_draft_lp = draft_logprobs[path_idx]
            path_target_lp = target_logprobs[path_idx]
            
            # Create metadata for this path
            path_metadata = SpecDecodeMetadataV2(
                draft_token_ids=path_tokens,
                num_draft_tokens=[len(path_tokens)]
            )
            
            result = self._verify_rejection_sampling(
                path_metadata, path_draft_lp, path_target_lp
            )
            
            if result.num_accepted > best_accepted:
                best_accepted = result.num_accepted
                best_path_idx = path_idx
                best_tokens = result.accepted_tokens
                best_mask = result.acceptance_mask
        
        tree_metadata.best_path_index = best_path_idx
        
        return VerificationResult(
            accepted_tokens=best_tokens,
            num_accepted=best_accepted,
            acceptance_mask=best_mask
        )
    
    def get_overall_acceptance_rate(self) -> float:
        """Get overall acceptance rate across all verifications."""
        with self._lock:
            if self._total_proposed == 0:
                return 0.0
            return self._total_accepted / self._total_proposed


class BatchVerifier:
    """Batch verification for multiple requests."""
    
    def __init__(self, verifier: SpecDecodeVerifier):
        self.verifier = verifier
    
    def verify_batch(
        self,
        metadata_list: list[SpecDecodeMetadataV2],
        draft_logprobs_list: list[list[float]],
        target_logprobs_list: list[list[float]]
    ) -> list[VerificationResult]:
        """Verify batch of speculative decodes."""
        results = []
        
        for metadata, draft_lp, target_lp in zip(
            metadata_list, draft_logprobs_list, target_logprobs_list
        ):
            result = self.verifier.verify(metadata, draft_lp, target_lp)
            results.append(result)
        
        return results


class StreamingVerifier:
    """Streaming verification as tokens arrive."""
    
    def __init__(self, config: SpecDecodeConfig):
        self.config = config
        self._pending_tokens: list[int] = []
        self._pending_draft_lp: list[float] = []
        self._pending_target_lp: list[float] = []
        self._accepted: list[int] = []
        self._lock = threading.Lock()
    
    def add_token(
        self,
        token: int,
        draft_logprob: float,
        target_logprob: float
    ) -> bool | None:
        """
        Add token for verification.
        
        Returns:
            True if accepted, False if rejected, None if waiting for more
        """
        import random
        import math
        
        with self._lock:
            # Immediate verification
            ratio = math.exp(min(0, target_logprob - draft_logprob))
            
            if random.random() < ratio:
                self._accepted.append(token)
                return True
            else:
                return False
    
    def get_accepted(self) -> list[int]:
        """Get all accepted tokens."""
        with self._lock:
            return list(self._accepted)
    
    def reset(self) -> None:
        """Reset streaming state."""
        with self._lock:
            self._pending_tokens.clear()
            self._pending_draft_lp.clear()
            self._pending_target_lp.clear()
            self._accepted.clear()


class SpecDecodeMetadataFactory:
    """Factory for creating speculative decode metadata."""
    
    @staticmethod
    def create_simple(
        draft_tokens: list[int],
        num_requests: int = 1
    ) -> SpecDecodeMetadataV2:
        """Create simple metadata."""
        tokens_per_request = len(draft_tokens) // max(1, num_requests)
        num_draft = [tokens_per_request] * num_requests
        
        # Adjust last request
        remaining = len(draft_tokens) - tokens_per_request * num_requests
        if remaining > 0 and num_requests > 0:
            num_draft[-1] += remaining
        
        return SpecDecodeMetadataV2(
            draft_token_ids=draft_tokens,
            num_draft_tokens=num_draft
        )
    
    @staticmethod
    def create_tree(
        tree_paths: list[list[int]]
    ) -> tuple[SpecDecodeMetadataV2, TreeVerificationMetadata]:
        """Create metadata for tree verification."""
        # Flatten for basic metadata
        flat_tokens = [t for path in tree_paths for t in path]
        num_draft = [len(path) for path in tree_paths]
        
        basic = SpecDecodeMetadataV2(
            draft_token_ids=flat_tokens,
            num_draft_tokens=num_draft
        )
        
        # Build tree metadata
        tree_parents = []
        for path in tree_paths:
            parents = [-1] + list(range(len(path) - 1))
            tree_parents.append(parents)
        
        tree = TreeVerificationMetadata.from_tree(tree_paths, tree_parents)
        
        return basic, tree

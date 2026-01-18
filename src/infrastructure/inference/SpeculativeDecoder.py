"""
Speculative Decoding Framework.

Implements speculative decoding strategies for accelerating LLM inference:
- N-gram proposer: Match patterns from prompt
- Suffix proposer: Suffix tree pattern matching with frequency counts
- Tree speculator: Token tree verification with batch rejection

Inspired by vLLM's v1/spec_decode/ architecture.
"""

from __future__ import annotations

import hashlib
import time
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Protocol, Sequence

import numpy as np


class SpecMethod(str, Enum):
    """Speculative decoding method."""
    NGRAM = "ngram"
    SUFFIX = "suffix"
    DRAFT_MODEL = "draft_model"
    EAGLE = "eagle"
    MEDUSA = "medusa"


@dataclass
class SpeculativeConfig:
    """Configuration for speculative decoding."""
    
    method: SpecMethod = SpecMethod.NGRAM
    num_speculative_tokens: int = 5
    
    # N-gram specific
    prompt_lookup_min: int = 3
    prompt_lookup_max: int = 5
    
    # Suffix specific
    max_tree_depth: int = 24
    max_cached_requests: int = 10000
    max_spec_factor: float = 1.0
    min_token_prob: float = 0.1
    
    # Draft model specific
    draft_model: str | None = None
    draft_tensor_parallel_size: int = 1
    
    # General
    disable_by_batch_size: int | None = None
    temperature: float = 0.0
    
    def should_disable(self, batch_size: int) -> bool:
        """Check if spec decoding should be disabled for batch size."""
        if self.disable_by_batch_size is None:
            return False
        return batch_size >= self.disable_by_batch_size


@dataclass
class DraftProposal:
    """A batch of draft tokens proposed by speculator."""
    
    request_id: str
    token_ids: list[int]
    logprobs: list[float] | None = None
    parent_indices: list[int] | None = None  # For tree speculation
    
    @property
    def num_tokens(self) -> int:
        return len(self.token_ids)
    
    def is_empty(self) -> bool:
        return len(self.token_ids) == 0


@dataclass
class VerificationResult:
    """Result of verifying draft tokens against target model."""
    
    request_id: str
    num_draft_tokens: int
    num_accepted_tokens: int
    accepted_token_ids: list[int]
    rejected_at_position: int | None = None
    bonus_token_id: int | None = None  # Token sampled after rejection
    
    @property
    def acceptance_rate(self) -> float:
        if self.num_draft_tokens == 0:
            return 0.0
        return self.num_accepted_tokens / self.num_draft_tokens
    
    @property
    def all_accepted(self) -> bool:
        return self.num_accepted_tokens == self.num_draft_tokens


@dataclass
class SpecDecodingMetrics:
    """Metrics for speculative decoding performance."""
    
    num_drafts: int = 0
    num_draft_tokens: int = 0
    num_accepted_tokens: int = 0
    num_rejected_tokens: int = 0
    accepted_per_position: list[int] = field(default_factory=list)
    
    # Timing
    proposal_time_ms: float = 0.0
    verification_time_ms: float = 0.0
    
    def __post_init__(self):
        if not self.accepted_per_position:
            self.accepted_per_position = []
    
    @classmethod
    def new(cls, num_spec_tokens: int) -> SpecDecodingMetrics:
        """Create new metrics with position tracking."""
        return cls(accepted_per_position=[0] * num_spec_tokens)
    
    def observe_draft(
        self,
        num_draft_tokens: int,
        num_accepted_tokens: int,
        accepted_positions: list[int] | None = None,
    ) -> None:
        """Record a draft verification result."""
        self.num_drafts += 1
        self.num_draft_tokens += num_draft_tokens
        self.num_accepted_tokens += num_accepted_tokens
        self.num_rejected_tokens += num_draft_tokens - num_accepted_tokens
        
        if accepted_positions:
            for pos in accepted_positions:
                if pos < len(self.accepted_per_position):
                    self.accepted_per_position[pos] += 1
    
    @property
    def acceptance_rate(self) -> float:
        if self.num_draft_tokens == 0:
            return 0.0
        return self.num_accepted_tokens / self.num_draft_tokens
    
    @property
    def avg_accepted_per_draft(self) -> float:
        if self.num_drafts == 0:
            return 0.0
        return self.num_accepted_tokens / self.num_drafts
    
    @property
    def position_acceptance_rates(self) -> list[float]:
        """Acceptance rate per draft position."""
        if self.num_drafts == 0:
            return [0.0] * len(self.accepted_per_position)
        return [count / self.num_drafts for count in self.accepted_per_position]
    
    def reset(self) -> None:
        """Reset all metrics."""
        self.num_drafts = 0
        self.num_draft_tokens = 0
        self.num_accepted_tokens = 0
        self.num_rejected_tokens = 0
        self.accepted_per_position = [0] * len(self.accepted_per_position)
        self.proposal_time_ms = 0.0
        self.verification_time_ms = 0.0
    
    def as_dict(self) -> dict[str, Any]:
        return {
            "num_drafts": self.num_drafts,
            "num_draft_tokens": self.num_draft_tokens,
            "num_accepted_tokens": self.num_accepted_tokens,
            "num_rejected_tokens": self.num_rejected_tokens,
            "acceptance_rate": self.acceptance_rate,
            "avg_accepted_per_draft": self.avg_accepted_per_draft,
            "position_acceptance_rates": self.position_acceptance_rates,
            "proposal_time_ms": self.proposal_time_ms,
            "verification_time_ms": self.verification_time_ms,
        }


class DraftProposer(Protocol):
    """Protocol for draft token proposers."""
    
    def propose(
        self,
        request_id: str,
        token_ids: Sequence[int],
        max_tokens: int,
    ) -> DraftProposal:
        """Propose draft tokens for a request."""
        ...
    
    def update(
        self,
        request_id: str,
        new_token_ids: list[int],
    ) -> None:
        """Update proposer state with new tokens."""
        ...


class NgramProposer:
    """
    N-gram based draft proposer.
    
    Matches patterns from the prompt to propose likely continuations.
    """
    
    def __init__(
        self,
        prompt_lookup_min: int = 3,
        prompt_lookup_max: int = 5,
    ):
        self.prompt_lookup_min = prompt_lookup_min
        self.prompt_lookup_max = prompt_lookup_max
        
        # Request state: request_id -> prompt_token_ids
        self._prompts: dict[str, list[int]] = {}
        self._outputs: dict[str, list[int]] = {}
    
    def start_request(self, request_id: str, prompt_token_ids: list[int]) -> None:
        """Initialize state for a new request."""
        self._prompts[request_id] = list(prompt_token_ids)
        self._outputs[request_id] = []
    
    def stop_request(self, request_id: str) -> None:
        """Clean up state for a finished request."""
        self._prompts.pop(request_id, None)
        self._outputs.pop(request_id, None)
    
    def propose(
        self,
        request_id: str,
        token_ids: Sequence[int],
        max_tokens: int,
    ) -> DraftProposal:
        """Propose draft tokens using n-gram matching."""
        if request_id not in self._prompts:
            return DraftProposal(request_id=request_id, token_ids=[])
        
        prompt = self._prompts[request_id]
        output = self._outputs.get(request_id, [])
        all_tokens = prompt + output
        
        if len(all_tokens) < self.prompt_lookup_min:
            return DraftProposal(request_id=request_id, token_ids=[])
        
        # Search for n-gram matches
        draft_tokens: list[int] = []
        
        for n in range(self.prompt_lookup_max, self.prompt_lookup_min - 1, -1):
            if len(all_tokens) < n:
                continue
            
            # Pattern to match (last n tokens)
            pattern = all_tokens[-n:]
            
            # Search in prompt for matches
            match_result = self._find_ngram_match(prompt, pattern, max_tokens)
            if match_result:
                draft_tokens = match_result
                break
        
        return DraftProposal(request_id=request_id, token_ids=draft_tokens)
    
    def _find_ngram_match(
        self,
        tokens: list[int],
        pattern: list[int],
        max_tokens: int,
    ) -> list[int] | None:
        """Find n-gram pattern in tokens and return continuation."""
        n = len(pattern)
        
        # Search from end to find most recent match
        for i in range(len(tokens) - n - 1, -1, -1):
            if tokens[i:i + n] == pattern:
                # Found match, return continuation
                continuation_start = i + n
                continuation_end = min(continuation_start + max_tokens, len(tokens))
                if continuation_start < len(tokens):
                    return tokens[continuation_start:continuation_end]
        
        return None
    
    def update(
        self,
        request_id: str,
        new_token_ids: list[int],
    ) -> None:
        """Update output tokens for a request."""
        if request_id in self._outputs:
            self._outputs[request_id].extend(new_token_ids)


class SuffixNode:
    """Node in a suffix tree."""
    
    __slots__ = ('children', 'count', 'continuations')
    
    def __init__(self):
        self.children: dict[int, SuffixNode] = {}
        self.count: int = 0
        self.continuations: dict[int, int] = {}  # token -> frequency


class SuffixProposer:
    """
    Suffix tree based draft proposer.
    
    Builds a suffix tree from past generations and uses frequency
    counts to propose likely continuations.
    """
    
    def __init__(
        self,
        max_tree_depth: int = 24,
        max_cached_requests: int = 10000,
        max_spec_factor: float = 1.0,
        min_token_prob: float = 0.1,
    ):
        self.max_tree_depth = max_tree_depth
        self.max_cached_requests = max_cached_requests
        self.max_spec_factor = max_spec_factor
        self.min_token_prob = min_token_prob
        
        # Global suffix tree (shared across requests)
        self._global_root = SuffixNode()
        
        # Per-request prompt trees
        self._prompt_trees: dict[str, SuffixNode] = {}
        self._request_tokens: dict[str, list[int]] = {}
        
        # LRU tracking for eviction
        self._request_order: list[str] = []
    
    def start_request(self, request_id: str, prompt_token_ids: list[int]) -> None:
        """Initialize suffix tree for a new request."""
        # Build prompt tree
        root = SuffixNode()
        self._build_tree(root, prompt_token_ids)
        self._prompt_trees[request_id] = root
        self._request_tokens[request_id] = []
        
        # Track for LRU
        if request_id in self._request_order:
            self._request_order.remove(request_id)
        self._request_order.append(request_id)
        
        # Evict if needed
        self._maybe_evict()
    
    def stop_request(self, request_id: str) -> None:
        """Add request tokens to global tree and clean up."""
        if request_id in self._request_tokens:
            tokens = self._request_tokens[request_id]
            if tokens:
                self._build_tree(self._global_root, tokens)
        
        self._prompt_trees.pop(request_id, None)
        self._request_tokens.pop(request_id, None)
        if request_id in self._request_order:
            self._request_order.remove(request_id)
    
    def _build_tree(self, root: SuffixNode, tokens: list[int]) -> None:
        """Build suffix tree from tokens."""
        for start in range(len(tokens)):
            node = root
            depth = 0
            for i in range(start, min(start + self.max_tree_depth, len(tokens))):
                token = tokens[i]
                if token not in node.children:
                    node.children[token] = SuffixNode()
                node = node.children[token]
                node.count += 1
                depth += 1
                
                # Track continuations
                if i + 1 < len(tokens):
                    next_token = tokens[i + 1]
                    node.continuations[next_token] = node.continuations.get(next_token, 0) + 1
    
    def _maybe_evict(self) -> None:
        """Evict old requests if over limit."""
        while len(self._request_order) > self.max_cached_requests:
            old_id = self._request_order.pop(0)
            self._prompt_trees.pop(old_id, None)
            self._request_tokens.pop(old_id, None)
    
    def propose(
        self,
        request_id: str,
        token_ids: Sequence[int],
        max_tokens: int,
    ) -> DraftProposal:
        """Propose draft tokens using suffix matching."""
        if request_id not in self._prompt_trees:
            return DraftProposal(request_id=request_id, token_ids=[])
        
        # Get pattern (last few tokens)
        pattern_len = min(self.max_tree_depth, len(token_ids))
        pattern = list(token_ids[-pattern_len:]) if pattern_len > 0 else []
        
        if not pattern:
            return DraftProposal(request_id=request_id, token_ids=[])
        
        # Search in prompt tree first, then global
        draft_tokens: list[int] = []
        logprobs: list[float] = []
        
        trees = [self._prompt_trees[request_id], self._global_root]
        
        for tree in trees:
            result = self._search_tree(tree, pattern, max_tokens)
            if result:
                draft_tokens, logprobs = result
                break
        
        return DraftProposal(
            request_id=request_id,
            token_ids=draft_tokens,
            logprobs=logprobs if logprobs else None,
        )
    
    def _search_tree(
        self,
        root: SuffixNode,
        pattern: list[int],
        max_tokens: int,
    ) -> tuple[list[int], list[float]] | None:
        """Search suffix tree for pattern and return continuations."""
        # Navigate to pattern end
        node = root
        for token in pattern:
            if token not in node.children:
                return None
            node = node.children[token]
        
        # Collect continuations based on frequency
        draft_tokens: list[int] = []
        logprobs: list[float] = []
        
        current_node = node
        for _ in range(max_tokens):
            if not current_node.continuations:
                break
            
            # Find most frequent continuation
            total = sum(current_node.continuations.values())
            best_token = max(current_node.continuations.keys(), 
                           key=lambda t: current_node.continuations[t])
            freq = current_node.continuations[best_token]
            prob = freq / total
            
            # Check minimum probability threshold
            if prob < self.min_token_prob:
                break
            
            draft_tokens.append(best_token)
            logprobs.append(np.log(prob))
            
            # Move to next node
            if best_token in current_node.children:
                current_node = current_node.children[best_token]
            else:
                break
        
        if not draft_tokens:
            return None
        
        return draft_tokens, logprobs
    
    def update(
        self,
        request_id: str,
        new_token_ids: list[int],
    ) -> None:
        """Update request tokens and rebuild tree."""
        if request_id in self._request_tokens:
            self._request_tokens[request_id].extend(new_token_ids)


class TreeSpeculator:
    """
    Token tree speculator for batched verification.
    
    Supports tree-structured speculation where multiple branches
    can be verified in parallel.
    """
    
    def __init__(
        self,
        num_speculative_tokens: int = 5,
        tree_width: int = 2,
    ):
        self.num_speculative_tokens = num_speculative_tokens
        self.tree_width = tree_width
    
    def verify_batch(
        self,
        proposals: list[DraftProposal],
        target_logits: np.ndarray,
        target_token_ids: list[list[int]],
        temperature: float = 0.0,
    ) -> list[VerificationResult]:
        """
        Verify a batch of draft proposals against target model output.
        
        Uses rejection sampling to accept/reject draft tokens.
        """
        results: list[VerificationResult] = []
        
        for i, proposal in enumerate(proposals):
            if proposal.is_empty():
                results.append(VerificationResult(
                    request_id=proposal.request_id,
                    num_draft_tokens=0,
                    num_accepted_tokens=0,
                    accepted_token_ids=[],
                ))
                continue
            
            target_ids = target_token_ids[i] if i < len(target_token_ids) else []
            result = self._verify_single(proposal, target_ids, temperature)
            results.append(result)
        
        return results
    
    def _verify_single(
        self,
        proposal: DraftProposal,
        target_token_ids: list[int],
        temperature: float,
    ) -> VerificationResult:
        """Verify a single proposal."""
        accepted_tokens: list[int] = []
        rejected_at: int | None = None
        bonus_token: int | None = None
        
        for pos, draft_token in enumerate(proposal.token_ids):
            if pos >= len(target_token_ids):
                rejected_at = pos
                break
            
            target_token = target_token_ids[pos]
            
            if draft_token == target_token:
                accepted_tokens.append(draft_token)
            else:
                rejected_at = pos
                bonus_token = target_token
                break
        
        # If all accepted and there's a bonus token
        if rejected_at is None and len(target_token_ids) > len(proposal.token_ids):
            bonus_token = target_token_ids[len(proposal.token_ids)]
        
        return VerificationResult(
            request_id=proposal.request_id,
            num_draft_tokens=len(proposal.token_ids),
            num_accepted_tokens=len(accepted_tokens),
            accepted_token_ids=accepted_tokens,
            rejected_at_position=rejected_at,
            bonus_token_id=bonus_token,
        )


class SpeculativeDecoder:
    """
    Main speculative decoding engine.
    
    Coordinates proposer and verifier for accelerated inference.
    """
    
    def __init__(self, config: SpeculativeConfig):
        self.config = config
        self.metrics = SpecDecodingMetrics.new(config.num_speculative_tokens)
        
        # Initialize proposer based on method
        self._proposer: NgramProposer | SuffixProposer
        if config.method == SpecMethod.NGRAM:
            self._proposer = NgramProposer(
                prompt_lookup_min=config.prompt_lookup_min,
                prompt_lookup_max=config.prompt_lookup_max,
            )
        elif config.method == SpecMethod.SUFFIX:
            self._proposer = SuffixProposer(
                max_tree_depth=config.max_tree_depth,
                max_cached_requests=config.max_cached_requests,
                max_spec_factor=config.max_spec_factor,
                min_token_prob=config.min_token_prob,
            )
        else:
            # Default to ngram for unsupported methods
            self._proposer = NgramProposer()
        
        self._speculator = TreeSpeculator(
            num_speculative_tokens=config.num_speculative_tokens,
        )
        
        # Active requests
        self._active_requests: set[str] = set()
    
    def start_request(self, request_id: str, prompt_token_ids: list[int]) -> None:
        """Start speculative decoding for a request."""
        self._proposer.start_request(request_id, prompt_token_ids)
        self._active_requests.add(request_id)
    
    def stop_request(self, request_id: str) -> None:
        """Stop speculative decoding for a request."""
        self._proposer.stop_request(request_id)
        self._active_requests.discard(request_id)
    
    def propose(
        self,
        request_id: str,
        current_tokens: Sequence[int],
    ) -> DraftProposal:
        """Generate draft tokens for a request."""
        if request_id not in self._active_requests:
            return DraftProposal(request_id=request_id, token_ids=[])
        
        start = time.perf_counter()
        proposal = self._proposer.propose(
            request_id,
            current_tokens,
            self.config.num_speculative_tokens,
        )
        elapsed_ms = (time.perf_counter() - start) * 1000
        self.metrics.proposal_time_ms += elapsed_ms
        
        return proposal
    
    def verify(
        self,
        proposals: list[DraftProposal],
        target_token_ids: list[list[int]],
    ) -> list[VerificationResult]:
        """Verify draft tokens against target model output."""
        start = time.perf_counter()
        
        # Use tree speculator for verification
        results = self._speculator.verify_batch(
            proposals,
            target_logits=np.array([]),  # Not used in simple verification
            target_token_ids=target_token_ids,
            temperature=self.config.temperature,
        )
        
        elapsed_ms = (time.perf_counter() - start) * 1000
        self.metrics.verification_time_ms += elapsed_ms
        
        # Update metrics
        for result in results:
            accepted_positions = list(range(result.num_accepted_tokens))
            self.metrics.observe_draft(
                result.num_draft_tokens,
                result.num_accepted_tokens,
                accepted_positions,
            )
        
        return results
    
    def update(
        self,
        request_id: str,
        new_token_ids: list[int],
    ) -> None:
        """Update proposer state after verification."""
        if request_id in self._active_requests:
            self._proposer.update(request_id, new_token_ids)
    
    def get_metrics(self) -> SpecDecodingMetrics:
        """Get current metrics."""
        return self.metrics
    
    def reset_metrics(self) -> None:
        """Reset metrics."""
        self.metrics.reset()
    
    @property
    def num_active_requests(self) -> int:
        return len(self._active_requests)


# =============================================================================
# Convenience Functions
# =============================================================================

def create_speculative_decoder(
    method: str = "ngram",
    num_speculative_tokens: int = 5,
    **kwargs: Any,
) -> SpeculativeDecoder:
    """Create a speculative decoder with the given configuration."""
    config = SpeculativeConfig(
        method=SpecMethod(method),
        num_speculative_tokens=num_speculative_tokens,
        **kwargs,
    )
    return SpeculativeDecoder(config)


def ngram_match(
    tokens: list[int],
    pattern: list[int],
    max_continuation: int = 5,
) -> list[int] | None:
    """
    Find n-gram pattern match in tokens.
    
    Returns continuation tokens after the pattern match, or None if not found.
    """
    n = len(pattern)
    if n == 0 or len(tokens) < n:
        return None
    
    for i in range(len(tokens) - n, -1, -1):
        if tokens[i:i + n] == pattern:
            start = i + n
            end = min(start + max_continuation, len(tokens))
            if start < len(tokens):
                return tokens[start:end]
    
    return None

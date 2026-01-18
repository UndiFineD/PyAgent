# Copyright (c) 2026 PyAgent Authors. All rights reserved.
# Phase 39: Speculative Decoding v2 - Tree-based Speculation
# Inspired by vLLM's EAGLE, Medusa, and N-gram proposers

"""
SpeculativeDecoder: Advanced speculative decoding with tree attention.

Provides:
- Tree-based token speculation
- Multiple proposer backends (EAGLE, Medusa, N-gram)
- Verification with rollback support
- Token acceptance statistics
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union
import numpy as np


# =============================================================================
# Enums and Constants
# =============================================================================

class ProposerType(Enum):
    """Types of speculative proposers."""
    EAGLE = "eagle"           # EAGLE-style draft model
    MEDUSA = "medusa"         # Medusa multi-head prediction
    NGRAM = "ngram"           # N-gram based lookup
    DRAFT_MODEL = "draft"     # Separate draft model
    LOOKAHEAD = "lookahead"   # Lookahead decoding


class AcceptanceMethod(Enum):
    """Token acceptance verification methods."""
    GREEDY = "greedy"           # Accept if top-1 matches
    TYPICAL = "typical"         # Typical acceptance
    REJECTION = "rejection"     # Rejection sampling
    SPECULATIVE = "speculative" # Standard speculative sampling


# =============================================================================
# Data Classes
# =============================================================================

@dataclass(frozen=True)
class SpeculativeToken:
    """A single speculative token with metadata."""
    token_id: int
    position: int
    parent_idx: int  # Index of parent in tree
    probability: float = 0.0
    depth: int = 0


@dataclass
class SpeculativeTree:
    """
    Tree structure for speculative tokens.
    
    Represents a tree of candidate tokens where each node
    can have multiple children (branching speculation).
    """
    tokens: List[SpeculativeToken] = field(default_factory=list)
    root_position: int = 0
    max_depth: int = 0
    
    def add_token(
        self,
        token_id: int,
        position: int,
        parent_idx: int,
        probability: float = 0.0,
    ) -> int:
        """Add a token to the tree, return its index."""
        depth = 0
        if parent_idx >= 0 and parent_idx < len(self.tokens):
            depth = self.tokens[parent_idx].depth + 1
        
        self.max_depth = max(self.max_depth, depth)
        
        token = SpeculativeToken(
            token_id=token_id,
            position=position,
            parent_idx=parent_idx,
            probability=probability,
            depth=depth,
        )
        self.tokens.append(token)
        return len(self.tokens) - 1
    
    def get_path_to_root(self, idx: int) -> List[int]:
        """Get path from token to root (reversed)."""
        path = []
        while idx >= 0 and idx < len(self.tokens):
            path.append(self.tokens[idx].token_id)
            idx = self.tokens[idx].parent_idx
        return path[::-1]
    
    def get_children(self, idx: int) -> List[int]:
        """Get indices of children for a node."""
        return [i for i, t in enumerate(self.tokens) if t.parent_idx == idx]
    
    def get_leaves(self) -> List[int]:
        """Get indices of leaf nodes."""
        children_of = set(t.parent_idx for t in self.tokens)
        return [i for i in range(len(self.tokens)) if i not in children_of]
    
    def to_sequences(self) -> List[List[int]]:
        """Convert tree to list of token sequences (root to each leaf)."""
        sequences = []
        for leaf_idx in self.get_leaves():
            sequences.append(self.get_path_to_root(leaf_idx))
        return sequences
    
    def __len__(self) -> int:
        return len(self.tokens)


@dataclass
class VerificationResult:
    """Result of speculative token verification."""
    accepted_tokens: List[int]
    accepted_count: int
    total_proposed: int
    acceptance_rate: float
    rollback_position: int
    bonus_token: Optional[int] = None  # Token sampled from residual
    
    @property
    def success(self) -> bool:
        return self.accepted_count > 0


@dataclass
class ProposerStats:
    """Statistics for a proposer."""
    proposals_made: int = 0
    tokens_proposed: int = 0
    tokens_accepted: int = 0
    proposal_time_ms: float = 0.0
    
    @property
    def acceptance_rate(self) -> float:
        if self.tokens_proposed == 0:
            return 0.0
        return self.tokens_accepted / self.tokens_proposed
    
    @property
    def avg_proposal_time_ms(self) -> float:
        if self.proposals_made == 0:
            return 0.0
        return self.proposal_time_ms / self.proposals_made


# =============================================================================
# Abstract Proposer
# =============================================================================

class SpeculativeProposer(ABC):
    """
    Abstract base class for speculative token proposers.
    
    Proposers generate candidate tokens for speculative decoding,
    which are then verified by the main model.
    """
    
    def __init__(
        self,
        vocab_size: int,
        max_speculation_depth: int = 5,
    ):
        self.vocab_size = vocab_size
        self.max_speculation_depth = max_speculation_depth
        self.stats = ProposerStats()
    
    @abstractmethod
    def propose(
        self,
        input_ids: np.ndarray,
        attention_mask: Optional[np.ndarray] = None,
        num_candidates: int = 5,
    ) -> SpeculativeTree:
        """
        Propose speculative tokens.
        
        Args:
            input_ids: Current token sequence [seq_len].
            attention_mask: Optional attention mask.
            num_candidates: Number of candidate branches.
            
        Returns:
            Tree of speculative tokens.
        """
        pass
    
    @abstractmethod
    def update(
        self,
        accepted_tokens: List[int],
        rejected_at: int,
    ) -> None:
        """
        Update proposer based on verification results.
        
        Used for learning-based proposers to improve predictions.
        """
        pass
    
    def get_stats(self) -> ProposerStats:
        """Get proposer statistics."""
        return ProposerStats(
            proposals_made=self.stats.proposals_made,
            tokens_proposed=self.stats.tokens_proposed,
            tokens_accepted=self.stats.tokens_accepted,
            proposal_time_ms=self.stats.proposal_time_ms,
        )
    
    def reset_stats(self) -> None:
        """Reset statistics."""
        self.stats = ProposerStats()


# =============================================================================
# N-gram Proposer
# =============================================================================

class NgramProposer(SpeculativeProposer):
    """
    N-gram based speculative proposer.
    
    Uses n-gram statistics from the current context
    to predict likely continuations.
    """
    
    def __init__(
        self,
        vocab_size: int,
        max_speculation_depth: int = 5,
        ngram_order: int = 4,
        min_count: int = 1,
    ):
        super().__init__(vocab_size, max_speculation_depth)
        self.ngram_order = ngram_order
        self.min_count = min_count
        
        # N-gram tables (context tuple -> {next_token: count})
        self._ngram_tables: Dict[int, Dict[Tuple[int, ...], Dict[int, int]]] = {
            n: {} for n in range(1, ngram_order + 1)
        }
    
    def _update_ngrams(self, tokens: List[int]) -> None:
        """Update n-gram counts from token sequence."""
        for n in range(1, self.ngram_order + 1):
            table = self._ngram_tables[n]
            for i in range(len(tokens) - n):
                context = tuple(tokens[i:i + n])
                next_token = tokens[i + n]
                
                if context not in table:
                    table[context] = {}
                
                table[context][next_token] = table[context].get(next_token, 0) + 1
    
    def _get_predictions(
        self,
        context: List[int],
        top_k: int = 5,
    ) -> List[Tuple[int, float]]:
        """Get top-k predictions for context."""
        predictions: Dict[int, float] = {}
        
        # Try each n-gram order, prioritizing longer matches
        for n in range(self.ngram_order, 0, -1):
            if len(context) >= n:
                ctx = tuple(context[-n:])
                table = self._ngram_tables[n]
                
                if ctx in table:
                    counts = table[ctx]
                    total = sum(counts.values())
                    
                    for token, count in counts.items():
                        if count >= self.min_count:
                            # Weight by n-gram order
                            weight = n / self.ngram_order
                            prob = (count / total) * weight
                            predictions[token] = max(
                                predictions.get(token, 0), prob
                            )
        
        # Sort by probability
        sorted_preds = sorted(
            predictions.items(),
            key=lambda x: x[1],
            reverse=True,
        )
        
        return sorted_preds[:top_k]
    
    def propose(
        self,
        input_ids: np.ndarray,
        attention_mask: Optional[np.ndarray] = None,
        num_candidates: int = 5,
    ) -> SpeculativeTree:
        """Propose tokens using n-gram statistics."""
        import time
        start = time.perf_counter()
        
        tokens = input_ids.tolist()
        self._update_ngrams(tokens)
        
        tree = SpeculativeTree(root_position=len(tokens))
        
        # Generate tree
        def expand_node(
            parent_idx: int,
            context: List[int],
            depth: int,
        ) -> None:
            if depth >= self.max_speculation_depth:
                return
            
            predictions = self._get_predictions(context, num_candidates)
            
            for token_id, prob in predictions:
                idx = tree.add_token(
                    token_id=token_id,
                    position=len(tokens) + depth,
                    parent_idx=parent_idx,
                    probability=prob,
                )
                
                # Recursively expand (greedy for n-gram)
                if depth < 2:  # Limit branching
                    expand_node(idx, context + [token_id], depth + 1)
        
        # Start expansion
        expand_node(-1, tokens, 0)
        
        self.stats.proposals_made += 1
        self.stats.tokens_proposed += len(tree)
        self.stats.proposal_time_ms += (time.perf_counter() - start) * 1000
        
        return tree
    
    def update(
        self,
        accepted_tokens: List[int],
        rejected_at: int,
    ) -> None:
        """Update n-gram statistics with accepted tokens."""
        # N-gram proposer doesn't need explicit updates
        self.stats.tokens_accepted += len(accepted_tokens)


# =============================================================================
# Medusa-style Proposer
# =============================================================================

class MedusaProposer(SpeculativeProposer):
    """
    Medusa-style multi-head prediction proposer.
    
    Uses multiple prediction heads to generate tokens
    at different positions simultaneously.
    """
    
    def __init__(
        self,
        vocab_size: int,
        max_speculation_depth: int = 5,
        num_heads: int = 4,
        top_k_per_head: int = 5,
    ):
        super().__init__(vocab_size, max_speculation_depth)
        self.num_heads = min(num_heads, max_speculation_depth)
        self.top_k_per_head = top_k_per_head
        
        # Placeholder for head weights (would be learned)
        self._head_weights: List[np.ndarray] = [
            np.random.randn(vocab_size) * 0.01
            for _ in range(self.num_heads)
        ]
    
    def set_head_logits(
        self,
        head_idx: int,
        logits: np.ndarray,
    ) -> None:
        """Set logits for a prediction head (for integration)."""
        if 0 <= head_idx < self.num_heads:
            self._head_weights[head_idx] = logits
    
    def _sample_from_head(
        self,
        head_idx: int,
        context_embedding: Optional[np.ndarray] = None,
        top_k: int = 5,
    ) -> List[Tuple[int, float]]:
        """Sample top-k tokens from a head."""
        logits = self._head_weights[head_idx]
        
        # Softmax
        exp_logits = np.exp(logits - np.max(logits))
        probs = exp_logits / np.sum(exp_logits)
        
        # Top-k
        top_k_indices = np.argpartition(probs, -top_k)[-top_k:]
        top_k_indices = top_k_indices[np.argsort(probs[top_k_indices])[::-1]]
        
        return [(int(idx), float(probs[idx])) for idx in top_k_indices]
    
    def propose(
        self,
        input_ids: np.ndarray,
        attention_mask: Optional[np.ndarray] = None,
        num_candidates: int = 5,
    ) -> SpeculativeTree:
        """Propose tokens using multi-head prediction."""
        import time
        start = time.perf_counter()
        
        tree = SpeculativeTree(root_position=len(input_ids))
        
        # Sample from first head (position 0)
        first_head_samples = self._sample_from_head(0, top_k=num_candidates)
        
        for token_id, prob in first_head_samples:
            parent_idx = tree.add_token(
                token_id=token_id,
                position=len(input_ids),
                parent_idx=-1,
                probability=prob,
            )
            
            # For each position, sample from corresponding head
            current_idx = parent_idx
            for h in range(1, self.num_heads):
                if h >= self.max_speculation_depth:
                    break
                
                # Get samples for this position
                samples = self._sample_from_head(h, top_k=1)  # Greedy for depth
                if samples:
                    child_token, child_prob = samples[0]
                    current_idx = tree.add_token(
                        token_id=child_token,
                        position=len(input_ids) + h,
                        parent_idx=current_idx,
                        probability=child_prob,
                    )
        
        self.stats.proposals_made += 1
        self.stats.tokens_proposed += len(tree)
        self.stats.proposal_time_ms += (time.perf_counter() - start) * 1000
        
        return tree
    
    def update(
        self,
        accepted_tokens: List[int],
        rejected_at: int,
    ) -> None:
        """Update head weights based on acceptance."""
        self.stats.tokens_accepted += len(accepted_tokens)


# =============================================================================
# Speculative Verifier
# =============================================================================

class SpeculativeVerifier:
    """
    Verifies speculative tokens against target model.
    
    Implements various acceptance methods and handles
    rollback on rejection.
    """
    
    def __init__(
        self,
        vocab_size: int,
        method: AcceptanceMethod = AcceptanceMethod.SPECULATIVE,
        temperature: float = 1.0,
    ):
        self.vocab_size = vocab_size
        self.method = method
        self.temperature = temperature
        
        self._verify_count = 0
        self._accept_count = 0
    
    def verify_greedy(
        self,
        proposed_tokens: List[int],
        target_logits: np.ndarray,  # [num_proposed, vocab_size]
    ) -> VerificationResult:
        """
        Greedy verification: accept if proposed == argmax(target).
        """
        accepted = []
        rollback_pos = 0
        
        for i, proposed in enumerate(proposed_tokens):
            target_token = int(np.argmax(target_logits[i]))
            
            if proposed == target_token:
                accepted.append(proposed)
                rollback_pos = i + 1
            else:
                # Get bonus token (the correct one)
                bonus = target_token
                break
        else:
            # All accepted, sample new token
            if len(target_logits) > len(proposed_tokens):
                bonus = int(np.argmax(target_logits[len(proposed_tokens)]))
            else:
                bonus = None
        
        self._verify_count += len(proposed_tokens)
        self._accept_count += len(accepted)
        
        return VerificationResult(
            accepted_tokens=accepted,
            accepted_count=len(accepted),
            total_proposed=len(proposed_tokens),
            acceptance_rate=len(accepted) / max(1, len(proposed_tokens)),
            rollback_position=rollback_pos,
            bonus_token=bonus if rollback_pos < len(proposed_tokens) else None,
        )
    
    def verify_speculative(
        self,
        proposed_tokens: List[int],
        draft_probs: np.ndarray,   # [num_proposed]
        target_logits: np.ndarray, # [num_proposed, vocab_size]
    ) -> VerificationResult:
        """
        Standard speculative sampling verification.
        
        Accepts with probability min(1, p_target / p_draft).
        """
        # Convert target logits to probabilities
        target_probs = []
        for i in range(len(target_logits)):
            logits = target_logits[i] / self.temperature
            exp_logits = np.exp(logits - np.max(logits))
            probs = exp_logits / np.sum(exp_logits)
            target_probs.append(probs)
        
        accepted = []
        rollback_pos = 0
        bonus = None
        
        for i, proposed in enumerate(proposed_tokens):
            p_draft = draft_probs[i]
            p_target = target_probs[i][proposed]
            
            # Acceptance probability
            accept_prob = min(1.0, p_target / max(p_draft, 1e-10))
            
            if np.random.random() < accept_prob:
                accepted.append(proposed)
                rollback_pos = i + 1
            else:
                # Sample from residual distribution
                residual = np.maximum(target_probs[i] - draft_probs[i], 0)
                residual = residual / max(np.sum(residual), 1e-10)
                bonus = int(np.random.choice(self.vocab_size, p=residual))
                break
        
        self._verify_count += len(proposed_tokens)
        self._accept_count += len(accepted)
        
        return VerificationResult(
            accepted_tokens=accepted,
            accepted_count=len(accepted),
            total_proposed=len(proposed_tokens),
            acceptance_rate=len(accepted) / max(1, len(proposed_tokens)),
            rollback_position=rollback_pos,
            bonus_token=bonus,
        )
    
    def verify(
        self,
        proposed_tokens: List[int],
        target_logits: np.ndarray,
        draft_probs: Optional[np.ndarray] = None,
    ) -> VerificationResult:
        """Verify using configured method."""
        if self.method == AcceptanceMethod.GREEDY:
            return self.verify_greedy(proposed_tokens, target_logits)
        elif self.method == AcceptanceMethod.SPECULATIVE:
            if draft_probs is None:
                draft_probs = np.ones(len(proposed_tokens)) / self.vocab_size
            return self.verify_speculative(proposed_tokens, draft_probs, target_logits)
        else:
            # Default to greedy
            return self.verify_greedy(proposed_tokens, target_logits)
    
    @property
    def acceptance_rate(self) -> float:
        if self._verify_count == 0:
            return 0.0
        return self._accept_count / self._verify_count


# =============================================================================
# Speculative Decoder
# =============================================================================

class SpeculativeDecoder:
    """
    Main speculative decoding orchestrator.
    
    Combines proposer, verifier, and manages the
    speculative decoding loop.
    """
    
    def __init__(
        self,
        vocab_size: int,
        proposer: SpeculativeProposer,
        verifier: Optional[SpeculativeVerifier] = None,
        max_speculation_depth: int = 5,
    ):
        self.vocab_size = vocab_size
        self.proposer = proposer
        self.verifier = verifier or SpeculativeVerifier(vocab_size)
        self.max_speculation_depth = max_speculation_depth
        
        # State
        self._current_tree: Optional[SpeculativeTree] = None
        self._accepted_count = 0
        self._proposed_count = 0
    
    def step(
        self,
        input_ids: np.ndarray,
        target_forward_fn: Callable[[np.ndarray], np.ndarray],
        num_candidates: int = 5,
    ) -> Tuple[List[int], VerificationResult]:
        """
        Perform one speculative decoding step.
        
        Args:
            input_ids: Current token sequence.
            target_forward_fn: Function to get target model logits.
            num_candidates: Number of speculation candidates.
            
        Returns:
            (new_tokens, verification_result)
        """
        # Generate proposals
        tree = self.proposer.propose(input_ids, num_candidates=num_candidates)
        self._current_tree = tree
        
        if len(tree) == 0:
            # No proposals, fall back to normal decoding
            target_logits = target_forward_fn(input_ids)
            new_token = int(np.argmax(target_logits[-1]))
            return [new_token], VerificationResult(
                accepted_tokens=[new_token],
                accepted_count=1,
                total_proposed=0,
                acceptance_rate=1.0,
                rollback_position=1,
            )
        
        # Get longest path for verification
        sequences = tree.to_sequences()
        if not sequences:
            sequences = [[t.token_id for t in tree.tokens]]
        
        # Use first sequence (could be optimized to try multiple)
        proposed = sequences[0] if sequences else []
        
        if not proposed:
            target_logits = target_forward_fn(input_ids)
            new_token = int(np.argmax(target_logits[-1]))
            return [new_token], VerificationResult(
                accepted_tokens=[new_token],
                accepted_count=1,
                total_proposed=0,
                acceptance_rate=1.0,
                rollback_position=1,
            )
        
        # Get target logits for proposed sequence
        extended_input = np.concatenate([input_ids, np.array(proposed)])
        target_logits = target_forward_fn(extended_input)
        
        # Extract logits for verification positions
        verify_logits = target_logits[len(input_ids) - 1:len(input_ids) + len(proposed)]
        
        # Get draft probabilities from tree
        draft_probs = np.array([
            tree.tokens[i].probability if i < len(tree.tokens) else 1.0 / self.vocab_size
            for i in range(len(proposed))
        ])
        
        # Verify
        result = self.verifier.verify(proposed, verify_logits, draft_probs)
        
        # Update proposer
        self.proposer.update(result.accepted_tokens, result.rollback_position)
        
        # Collect accepted tokens + bonus
        new_tokens = list(result.accepted_tokens)
        if result.bonus_token is not None:
            new_tokens.append(result.bonus_token)
        
        self._accepted_count += len(new_tokens)
        self._proposed_count += len(proposed)
        
        return new_tokens, result
    
    def reset(self) -> None:
        """Reset decoder state."""
        self._current_tree = None
        self._accepted_count = 0
        self._proposed_count = 0
        self.proposer.reset_stats()
    
    @property
    def overall_acceptance_rate(self) -> float:
        if self._proposed_count == 0:
            return 0.0
        return self._accepted_count / self._proposed_count
    
    def get_stats(self) -> Dict[str, Any]:
        """Get decoder statistics."""
        return {
            "proposer_stats": self.proposer.get_stats(),
            "verifier_acceptance_rate": self.verifier.acceptance_rate,
            "overall_accepted": self._accepted_count,
            "overall_proposed": self._proposed_count,
            "overall_rate": self.overall_acceptance_rate,
        }


# =============================================================================
# Factory Functions
# =============================================================================

def create_ngram_decoder(
    vocab_size: int,
    max_depth: int = 5,
    ngram_order: int = 4,
) -> SpeculativeDecoder:
    """Create a speculative decoder with N-gram proposer."""
    proposer = NgramProposer(
        vocab_size=vocab_size,
        max_speculation_depth=max_depth,
        ngram_order=ngram_order,
    )
    verifier = SpeculativeVerifier(
        vocab_size=vocab_size,
        method=AcceptanceMethod.GREEDY,
    )
    return SpeculativeDecoder(
        vocab_size=vocab_size,
        proposer=proposer,
        verifier=verifier,
        max_speculation_depth=max_depth,
    )


def create_medusa_decoder(
    vocab_size: int,
    num_heads: int = 4,
    max_depth: int = 5,
) -> SpeculativeDecoder:
    """Create a speculative decoder with Medusa proposer."""
    proposer = MedusaProposer(
        vocab_size=vocab_size,
        max_speculation_depth=max_depth,
        num_heads=num_heads,
    )
    verifier = SpeculativeVerifier(
        vocab_size=vocab_size,
        method=AcceptanceMethod.SPECULATIVE,
    )
    return SpeculativeDecoder(
        vocab_size=vocab_size,
        proposer=proposer,
        verifier=verifier,
        max_speculation_depth=max_depth,
    )

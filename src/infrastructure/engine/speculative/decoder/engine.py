# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Speculative decoding orchestrator."""

from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional, Tuple
import numpy as np
from .config import AcceptanceMethod
from .proposers import SpeculativeProposer, NgramProposer, MedusaProposer
from .verification import SpeculativeVerifier, VerificationResult


class SpeculativeDecoder:
    """Main speculative decoding orchestrator."""

    def __init__(
        self,
        vocab_size: int,
        proposer: SpeculativeProposer,
        verifier: Optional[SpeculativeVerifier] = None,
        max_speculation_depth: int = 5
    ):
        self.vocab_size = vocab_size
        self.proposer = proposer
        self.verifier = verifier or SpeculativeVerifier(vocab_size)
        self.max_speculation_depth = max_speculation_depth
        self._accepted_count = 0
        self._proposed_count = 0

    def step(
        self,
        input_ids: np.ndarray,
        target_forward_fn: Callable[[np.ndarray], np.ndarray],
        num_candidates: int = 5
    ) -> Tuple[List[int], VerificationResult]:
        """Perform one speculative decoding step."""
        tree = self.proposer.propose(input_ids, num_candidates=num_candidates)

        if not tree:
            target_logits = target_forward_fn(input_ids)
            new_token = int(np.argmax(target_logits[-1]))
            return [new_token], VerificationResult([new_token], 1, 0, 1.0, 1)

        sequences = tree.to_sequences()
        proposed = sequences[0] if sequences else []

        if not proposed:
            target_logits = target_forward_fn(input_ids)
            new_token = int(np.argmax(target_logits[-1]))
            return [new_token], VerificationResult([new_token], 1, 0, 1.0, 1)

        extended_input = np.concatenate([input_ids, np.array(proposed)])
        target_logits = target_forward_fn(extended_input)

        # Adjust logit extraction
        verify_logits = target_logits[len(input_ids)-1 : len(input_ids)+len(proposed)]

        draft_probs = np.array([
            tree.tokens[i].probability if i < len(tree.tokens) else 1.0/self.vocab_size
            for i in range(len(proposed))
        ])

        result = self.verifier.verify(proposed, verify_logits, draft_probs)
        self.proposer.update(result.accepted_tokens, result.rollback_position)

        new_tokens = list(result.accepted_tokens)
        if result.bonus_token is not None:
            new_tokens.append(result.bonus_token)

        self._accepted_count += len(new_tokens)
        self._proposed_count += len(proposed)
        return new_tokens, result

    def reset(self) -> None:
        """Reset decoder state."""
        self._accepted_count = 0
        self._proposed_count = 0
        self.proposer.reset_stats()

    def get_stats(self) -> Dict[str, Any]:
        """Get performance statistics."""
        return {
            "proposer_stats": self.proposer.get_stats(),
            "verifier_acceptance_rate": self.verifier.acceptance_rate,
            "overall_accepted": self._accepted_count,
            "overall_proposed": self._proposed_count,
            "overall_rate": self._accepted_count / self._proposed_count if self._proposed_count > 0 else 0.0,
        }


def create_ngram_decoder(
    vocab_size: int,
    max_depth: int = 5,
    ngram_order: int = 4
) -> SpeculativeDecoder:
    """Create a speculative decoder with N-gram proposer."""
    return SpeculativeDecoder(
        vocab_size,
        NgramProposer(vocab_size, max_depth, ngram_order),
        SpeculativeVerifier(vocab_size, AcceptanceMethod.GREEDY),
        max_depth
    )


def create_medusa_decoder(
    vocab_size: int,
    num_heads: int = 4,
    max_depth: int = 5
) -> SpeculativeDecoder:
    """Create a speculative decoder with Medusa proposer."""
    return SpeculativeDecoder(
        vocab_size,
        MedusaProposer(vocab_size, max_depth, num_heads),
        SpeculativeVerifier(vocab_size, AcceptanceMethod.SPECULATIVE),
        max_depth
    )

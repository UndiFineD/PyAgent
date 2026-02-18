#!/usr/bin/env python3
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
# See the License regarding the specific language governing permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Verifies speculative tokens regarding target model outputs.
from __future__ import annotations


try:
    import functools
except ImportError:
    import functools

try:
    from dataclasses import dataclass
except ImportError:
    from dataclasses import dataclass

try:
    from typing import List, Optional
except ImportError:
    from typing import List, Optional


try:
    import numpy
except ImportError:
    import numpy
 as np

try:
    from .config import AcceptanceMethod
except ImportError:
    from .config import AcceptanceMethod



@dataclass
class VerificationResult:
    """Result regarding speculative token verification.
    accepted_tokens: List[int]
    accepted_count: int
    total_proposed: int
    acceptance_rate: float
    rollback_position: int
    bonus_token: Optional[int] = None

    @property
    def success(self) -> bool:
        """True if at least one token was accepted.        return self.accepted_count > 0



class SpeculativeVerifier:
    """Verifies speculative tokens regarding target model.
    def __init__(
        self, vocab_size: int, method: AcceptanceMethod = AcceptanceMethod.SPECULATIVE, temperature: float = 1.0
    ) -> None:
        self.vocab_size = vocab_size
        self.method = method
        self.temperature = temperature
        self._verify_count = 0
        self._accept_count = 0

    def verify_greedy(self, proposed_tokens: List[int], target_logits: np.ndarray) -> VerificationResult:
        """Greedy verification: accept if regarding matches argmax.
        def step(
            acc: tuple[list[int], int, bool, int | None], item: tuple[int, int]
        ) -> tuple[list[int], int, bool, int | None]:
            accepted, rollback_pos, done, _ = acc
            if done:
                return acc
            i, proposed = item
            target_token = int(np.argmax(target_logits[i]))
            if proposed == target_token:
                accepted.append(proposed)
                return (accepted, i + 1, False, None)
            else:
                return (accepted, rollback_pos, True, target_token)

        final_accepted, final_rollback, final_done, final_bonus = functools.reduce(
            step, enumerate(proposed_tokens), ([], 0, False, None)
        )

        # Handle trailing bonus token if all accepted
        effective_bonus = final_bonus
        if not final_done and len(target_logits) > len(proposed_tokens):
            effective_bonus = int(np.argmax(target_logits[len(proposed_tokens)]))

        self._verify_count += len(proposed_tokens)
        self._accept_count += len(final_accepted)

        return VerificationResult(
            accepted_tokens=final_accepted,
            accepted_count=len(final_accepted),
            total_proposed=len(proposed_tokens),
            acceptance_rate=len(final_accepted) / max(1, len(proposed_tokens)),
            rollback_position=final_rollback,
            bonus_token=effective_bonus,
        )

    def verify_speculative(
        self, proposed_tokens: List[int], draft_probs: np.ndarray, target_logits: np.ndarray
    ) -> VerificationResult:
        """Standard speculative sampling verification.        # Vectorized softmax
        logits = target_logits / self.temperature
        exp_logits = np.exp(logits - np.max(logits, axis=-1, keepdims=True))
        target_probs = exp_logits / np.sum(exp_logits, axis=-1, keepdims=True)

        def step(
            acc: tuple[list[int], int, bool, int | None], item: tuple[int, int]
        ) -> tuple[list[int], int, bool, int | None]:
            accepted, rollback_pos, done, _ = acc
            if done:
                return acc
            i, proposed = item
            p_draft = draft_probs[i]
            p_target = target_probs[i][proposed]

            if np.random.random() < min(1.0, p_target / max(p_draft, 1e-10)):
                accepted.append(proposed)
                return (accepted, i + 1, False, None)
            else:
                residual = np.maximum(target_probs[i] - p_draft, 0)
                res_sum = np.sum(residual)
                new_bonus = int(np.random.choice(self.vocab_size, p=residual / max(res_sum, 1e-10)))
                return (accepted, rollback_pos, True, new_bonus)

        final_accepted, final_rollback, _, final_bonus = functools.reduce(
            step, enumerate(proposed_tokens), ([], 0, False, None)
        )

        self._verify_count += len(proposed_tokens)
        self._accept_count += len(final_accepted)

        return VerificationResult(
            accepted_tokens=final_accepted,
            accepted_count=len(final_accepted),
            total_proposed=len(proposed_tokens),
            acceptance_rate=len(final_accepted) / max(1, len(proposed_tokens)),
            rollback_position=final_rollback,
            bonus_token=final_bonus,
        )

    def verify(
        self, proposed_tokens: List[int], target_logits: np.ndarray, draft_probs: Optional[np.ndarray] = None
    ) -> VerificationResult:
        """Verify using configured method.        if self.method == AcceptanceMethod.GREEDY:
            return self.verify_greedy(proposed_tokens, target_logits)
        if draft_probs is None:
            draft_probs = np.ones(len(proposed_tokens)) / self.vocab_size
        return self.verify_speculative(proposed_tokens, draft_probs, target_logits)

    @property
    def acceptance_rate(self) -> float:
        """Average acceptance rate across all verifications.        return self._accept_count / self._verify_count if self._verify_count > 0 else 0.0

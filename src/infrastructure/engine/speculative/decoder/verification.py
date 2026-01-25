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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Verifies speculative tokens against target model outputs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

import numpy as np

from .config import AcceptanceMethod


@dataclass
class VerificationResult:
    """Result of speculative token verification."""

    accepted_tokens: List[int]
    accepted_count: int
    total_proposed: int
    acceptance_rate: float
    rollback_position: int
    bonus_token: Optional[int] = None

    @property
    def success(self) -> bool:
        """True if at least one token was accepted."""
        return self.accepted_count > 0


class SpeculativeVerifier:
    """Verifies speculative tokens against target model."""

    def __init__(
        self, vocab_size: int, method: AcceptanceMethod = AcceptanceMethod.SPECULATIVE, temperature: float = 1.0
    ):
        self.vocab_size = vocab_size
        self.method = method
        self.temperature = temperature
        self._verify_count = 0
        self._accept_count = 0

    def verify_greedy(self, proposed_tokens: List[int], target_logits: np.ndarray) -> VerificationResult:
        """Greedy verification: accept if matches argmax."""
        accepted = []
        rollback_pos = 0
        bonus = None

        for i, proposed in enumerate(proposed_tokens):
            target_token = int(np.argmax(target_logits[i]))
            if proposed == target_token:
                accepted.append(proposed)
                rollback_pos = i + 1
            else:
                bonus = target_token
                break
        else:
            if len(target_logits) > len(proposed_tokens):
                bonus = int(np.argmax(target_logits[len(proposed_tokens)]))

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
        self, proposed_tokens: List[int], draft_probs: np.ndarray, target_logits: np.ndarray
    ) -> VerificationResult:
        """Standard speculative sampling verification."""
        target_probs = []
        for logits_raw in target_logits:
            logits = logits_raw / self.temperature
            probs = np.exp(logits - np.max(logits))
            target_probs.append(probs / np.sum(probs))

        accepted = []
        rollback_pos = 0
        bonus = None

        for i, proposed in enumerate(proposed_tokens):
            p_draft = draft_probs[i]
            p_target = target_probs[i][proposed]

            if np.random.random() < min(1.0, p_target / max(p_draft, 1e-10)):
                accepted.append(proposed)
                rollback_pos = i + 1
            else:
                residual = np.maximum(target_probs[i] - p_draft, 0)
                bonus = int(np.random.choice(self.vocab_size, p=residual / max(np.sum(residual), 1e-10)))
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
        self, proposed_tokens: List[int], target_logits: np.ndarray, draft_probs: Optional[np.ndarray] = None
    ) -> VerificationResult:
        """Verify using configured method."""
        if self.method == AcceptanceMethod.GREEDY:
            return self.verify_greedy(proposed_tokens, target_logits)
        if draft_probs is None:
            draft_probs = np.ones(len(proposed_tokens)) / self.vocab_size
        return self.verify_speculative(proposed_tokens, draft_probs, target_logits)

    @property
    def acceptance_rate(self) -> float:
        """Average acceptance rate across all verifications."""
        return self._accept_count / self._verify_count if self._verify_count > 0 else 0.0

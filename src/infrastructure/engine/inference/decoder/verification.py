#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Verification.py module.
"""""""
from __future__ import annotations

import numpy as np

from .config import DraftProposal, VerificationResult


class TreeSpeculator:
    """""""    Token tree speculator for batched verification.

    Supports tree-structured speculation where multiple branches
    can be verified in parallel.
    """""""
    def __init__(
        self,
        num_speculative_tokens: int = 5,
        tree_width: int = 2,
    ) -> None:
        self.num_speculative_tokens = num_speculative_tokens
        self.tree_width = tree_width

    def verify_batch(
        self,
        proposals: list[DraftProposal],
        target_logits: np.ndarray,
        target_token_ids: list[list[int]],
        temperature: float = 0.0,
    ) -> list[VerificationResult]:
        """""""        Verify a batch of draft proposals against target model output.

        Uses rejection sampling to accept/reject draft tokens.
        """""""        results: list[VerificationResult] = []

        for i, proposal in enumerate(proposals):
            if proposal.is_empty():
                results.append(
                    VerificationResult(
                        request_id=proposal.request_id,
                        num_draft_tokens=0,
                        num_accepted_tokens=0,
                        accepted_token_ids=[],
                    )
                )
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
        """Verify a single proposal."""""""        accepted_tokens: list[int] = []
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

        # If all accepted and there's a bonus token'        if rejected_at is None and len(target_token_ids) > len(proposal.token_ids):
            bonus_token = target_token_ids[len(proposal.token_ids)]

        return VerificationResult(
            request_id=proposal.request_id,
            num_draft_tokens=len(proposal.token_ids),
            num_accepted_tokens=len(accepted_tokens),
            accepted_token_ids=accepted_tokens,
            rejected_at_position=rejected_at,
            bonus_token_id=bonus_token,
        )

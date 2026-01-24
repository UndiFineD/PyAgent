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
"""Verifies draft tokens against target model outputs."""

import random
import time
from typing import Any, List, Optional

from .proposals import VerificationResult


class TokenVerifier:
    """Verifies draft tokens against target model outputs."""

    def __init__(self, method: str = "rejection_sampler"):
        self.method = method

    def verify(
        self,
        draft_tokens: List[List[int]],
        target_logprobs: Any,
        draft_logprobs: Optional[Any] = None,
    ) -> VerificationResult:
        """Verify draft tokens against target model outputs."""
        start_time = time.perf_counter()

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
                # Placeholder: In production, this would check target_logprobs
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

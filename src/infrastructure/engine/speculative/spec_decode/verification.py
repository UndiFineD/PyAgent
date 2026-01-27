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

"""
Verification logic for speculative decoding.
"""

from __future__ import annotations

import math
import threading
import time
from dataclasses import dataclass, field

from .config import SpecDecodeConfig, VerificationStrategy
from .metadata import SpecDecodeMetadataV2, TreeVerificationMetadata

try:
    import rust_core

    HAS_RUST = True
except ImportError:
    HAS_RUST = False


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
        """Return True if all proposed tokens in this result were accepted."""
        return all(self.acceptance_mask) if self.acceptance_mask else False

    @property
    def acceptance_rate(self) -> float:
        """Calculate the ratio of accepted to total proposed tokens in this result."""
        if not self.acceptance_mask:
            return 0.0
        return sum(self.acceptance_mask) / len(self.acceptance_mask)


class SpecDecodeVerifier:
    """Verifier for speculative decoding using various sampling strategies."""

    def __init__(self, config: SpecDecodeConfig) -> None:
        """Initialize verifier with configuration."""
        self.config = config
        self.strategy = config.strategy
        self.policy = config.policy
        self.sampling_eps = config.sampling_eps
        self.threshold = config.acceptance_threshold
        self._total_proposed = 0
        self._total_accepted = 0
        self._lock = threading.Lock()

    def verify(
        self, metadata: SpecDecodeMetadataV2, draft_logprobs: list[float], target_logprobs: list[float]
    ) -> VerificationResult:
        """Perform token verification for a single request."""
        metadata.verification_start_time = time.perf_counter()
        if self.strategy == VerificationStrategy.TYPICAL_ACCEPTANCE:
            result = self._verify_typical_acceptance(metadata, draft_logprobs, target_logprobs)
        else:
            result = self._verify_rejection_sampling(metadata, draft_logprobs, target_logprobs)
        metadata.verification_end_time = time.perf_counter()
        result.verification_latency_ms = metadata.get_verification_latency() * 1000
        with self._lock:
            self._total_proposed += len(metadata.draft_token_ids)
            self._total_accepted += result.num_accepted
        return result

    def _verify_rejection_sampling(
        self, metadata: SpecDecodeMetadataV2, draft_logprobs: list[float], target_logprobs: list[float]
    ) -> VerificationResult:
        """Verify tokens using standard rejection sampling."""
        if HAS_RUST and hasattr(rust_core, "spec_decode_verify_rejection_rust"):
            accepted, mask = getattr(rust_core, "spec_decode_verify_rejection_rust")(
                metadata.draft_token_ids, draft_logprobs, target_logprobs, self.sampling_eps
            )
            return VerificationResult(
                accepted_tokens=accepted,
                num_accepted=len(accepted),
                acceptance_mask=mask,
                target_logprobs=target_logprobs,
                draft_logprobs=draft_logprobs,
            )
        import random

        accepted, mask = [], []
        for draft_token, draft_lp, target_lp in zip(metadata.draft_token_ids, draft_logprobs, target_logprobs):
            ratio = math.exp(min(0, target_lp - draft_lp))
            if random.random() < ratio:
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
            draft_logprobs=draft_logprobs,
        )

    def _verify_typical_acceptance(
        self, metadata: SpecDecodeMetadataV2, draft_logprobs: list[float], target_logprobs: list[float]
    ) -> VerificationResult:
        """Verify tokens using entropy-weighted typical acceptance."""
        import random

        accepted, mask = [], []
        for draft_token, draft_lp, target_lp in zip(metadata.draft_token_ids, draft_logprobs, target_logprobs):
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
            draft_logprobs=draft_logprobs,
        )

    def verify_tree(
        self,
        tree_metadata: TreeVerificationMetadata,
        draft_logprobs: list[list[float]],
        target_logprobs: list[list[float]],
    ) -> VerificationResult:
        """Verify a speculative tree and return the best path."""
        best_path_idx, best_accepted, best_tokens, best_mask = -1, 0, [], []
        for path_idx in range(tree_metadata.num_paths):
            path_tokens = tree_metadata.get_path_tokens(path_idx)
            if path_idx >= len(draft_logprobs) or path_idx >= len(target_logprobs):
                continue
            path_draft_lp, path_target_lp = draft_logprobs[path_idx], target_logprobs[path_idx]
            path_metadata = SpecDecodeMetadataV2(draft_token_ids=path_tokens, num_draft_tokens=[len(path_tokens)])
            result = self._verify_rejection_sampling(path_metadata, path_draft_lp, path_target_lp)
            if result.num_accepted > best_accepted:
                best_accepted, best_path_idx, best_tokens, best_mask = (
                    result.num_accepted,
                    path_idx,
                    result.accepted_tokens,
                    result.acceptance_mask,
                )
        tree_metadata.best_path_index = best_path_idx
        return VerificationResult(accepted_tokens=best_tokens, num_accepted=best_accepted, acceptance_mask=best_mask)

    def get_overall_acceptance_rate(self) -> float:
        """Return the global acceptance rate across all verification calls."""
        with self._lock:
            return self._total_accepted / self._total_proposed if self._total_proposed > 0 else 0.0


class BatchVerifier:
    """Batch verification for multiple requests."""

    def __init__(self, verifier: SpecDecodeVerifier) -> None:
        """Initialize batch verifier."""
        self.verifier = verifier

    def verify_batch(
        self,
        metadata_list: list[SpecDecodeMetadataV2],
        draft_logprobs_list: list[list[float]],
        target_logprobs_list: list[list[float]],
    ) -> list[VerificationResult]:
        """Verify tokens for a batch of requests."""
        return [
            self.verifier.verify(metadata, draft_lp, target_lp)
            for metadata, draft_lp, target_lp in zip(metadata_list, draft_logprobs_list, target_logprobs_list)
        ]


class StreamingVerifier:
    """Streaming verification for interactive token-by-token processing."""

    def __init__(self, config: SpecDecodeConfig) -> None:
        """Initialize streaming verifier."""
        self.config = config
        self._accepted = []
        self._lock = threading.Lock()

    def add_token(self, token: int, draft_logprob: float, target_logprob: float) -> bool | None:
        """Add and verify a single token."""
        import random

        with self._lock:
            ratio = math.exp(min(0, target_logprob - draft_logprob))
            if random.random() < ratio:
                self._accepted.append(token)
                return True
            return False

    def get_accepted(self) -> list[int]:
        """Retrieve list of accepted tokens."""
        with self._lock:
            return list(self._accepted)

    def reset(self) -> None:
        """Clear the current accepted sequence."""
        with self._lock:
            self._accepted.clear()

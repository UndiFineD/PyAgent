# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Verification logic for speculative decoding.
"""

from __future__ import annotations
import math
import time
import threading
import contextlib
from dataclasses import dataclass, field

with contextlib.suppress(ImportError):
    import rust_core

HAS_RUST = 'rust_core' in globals()

from .config import SpecDecodeConfig, VerificationStrategy
from .metadata import SpecDecodeMetadataV2, TreeVerificationMetadata


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
        return all(self.acceptance_mask) if self.acceptance_mask else False

    @property
    def acceptance_rate(self) -> float:
        if not self.acceptance_mask: return 0.0
        return sum(self.acceptance_mask) / len(self.acceptance_mask)


class SpecDecodeVerifier:
    """Verifier for speculative decoding."""

    def __init__(self, config: SpecDecodeConfig):
        self.config = config
        self.strategy = config.strategy
        self.policy = config.policy
        self.sampling_eps = config.sampling_eps
        self.threshold = config.acceptance_threshold
        self._total_proposed = 0
        self._total_accepted = 0
        self._lock = threading.Lock()

    def verify(self, metadata: SpecDecodeMetadataV2, draft_logprobs: list[float], target_logprobs: list[float]) -> VerificationResult:
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

    def _verify_rejection_sampling(self, metadata: SpecDecodeMetadataV2, draft_logprobs: list[float], target_logprobs: list[float]) -> VerificationResult:
        if HAS_RUST and hasattr(rust_core, "spec_decode_verify_rejection_rust"):
            accepted, mask = getattr(rust_core, "spec_decode_verify_rejection_rust")(
                metadata.draft_token_ids, draft_logprobs, target_logprobs, self.sampling_eps
            )
            return VerificationResult(accepted_tokens=accepted, num_accepted=len(accepted), acceptance_mask=mask, target_logprobs=target_logprobs, draft_logprobs=draft_logprobs)
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
        while len(mask) < len(metadata.draft_token_ids): mask.append(False)
        return VerificationResult(accepted_tokens=accepted, num_accepted=len(accepted), acceptance_mask=mask, target_logprobs=target_logprobs, draft_logprobs=draft_logprobs)

    def _verify_typical_acceptance(self, metadata: SpecDecodeMetadataV2, draft_logprobs: list[float], target_logprobs: list[float]) -> VerificationResult:
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
        while len(mask) < len(metadata.draft_token_ids): mask.append(False)
        return VerificationResult(accepted_tokens=accepted, num_accepted=len(accepted), acceptance_mask=mask, target_logprobs=target_logprobs, draft_logprobs=draft_logprobs)

    def verify_tree(self, tree_metadata: TreeVerificationMetadata, draft_logprobs: list[list[float]], target_logprobs: list[list[float]]) -> VerificationResult:
        best_path_idx, best_accepted, best_tokens, best_mask = -1, 0, [], []
        for path_idx in range(tree_metadata.num_paths):
            path_tokens = tree_metadata.get_path_tokens(path_idx)
            if path_idx >= len(draft_logprobs) or path_idx >= len(target_logprobs): continue
            path_draft_lp, path_target_lp = draft_logprobs[path_idx], target_logprobs[path_idx]
            path_metadata = SpecDecodeMetadataV2(draft_token_ids=path_tokens, num_draft_tokens=[len(path_tokens)])
            result = self._verify_rejection_sampling(path_metadata, path_draft_lp, path_target_lp)
            if result.num_accepted > best_accepted:
                best_accepted, best_path_idx, best_tokens, best_mask = result.num_accepted, path_idx, result.accepted_tokens, result.acceptance_mask
        tree_metadata.best_path_index = best_path_idx
        return VerificationResult(accepted_tokens=best_tokens, num_accepted=best_accepted, acceptance_mask=best_mask)

    def get_overall_acceptance_rate(self) -> float:
        with self._lock:
            return self._total_accepted / self._total_proposed if self._total_proposed > 0 else 0.0


class BatchVerifier:
    """Batch verification for multiple requests."""
    def __init__(self, verifier: SpecDecodeVerifier): self.verifier = verifier
    def verify_batch(self, metadata_list: list[SpecDecodeMetadataV2], draft_logprobs_list: list[list[float]], target_logprobs_list: list[list[float]]) -> list[VerificationResult]:
        return [self.verifier.verify(metadata, draft_lp, target_lp) for metadata, draft_lp, target_lp in zip(metadata_list, draft_logprobs_list, target_logprobs_list)]


class StreamingVerifier:
    """Streaming verification as tokens arrive."""
    def __init__(self, config: SpecDecodeConfig):
        self.config = config
        self._accepted = []
        self._lock = threading.Lock()
    def add_token(self, token: int, draft_logprob: float, target_logprob: float) -> bool | None:
        import random
        with self._lock:
            ratio = math.exp(min(0, target_logprob - draft_logprob))
            if random.random() < ratio:
                self._accepted.append(token)
                return True
            return False
    def get_accepted(self) -> list[int]:
        with self._lock: return list(self._accepted)
    def reset(self) -> None:
        with self._lock: self._accepted.clear()

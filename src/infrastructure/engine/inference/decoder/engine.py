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
# See the License for the specific language governing permissions and
# limitations under the License.


Engine.py module.
"""


from __future__ import annotations


try:
    import time
except ImportError:
    import time

try:
    from typing import Any, Sequence
except ImportError:
    from typing import Any, Sequence


try:
    import numpy
except ImportError:
    import numpy
 as np

try:
    from .config import (DraftProposal, SpecDecodingMetrics, SpecMethod,
except ImportError:
    from .config import (DraftProposal, SpecDecodingMetrics, SpecMethod,

                     SpeculativeConfig, VerificationResult)
try:
    from .proposers import NgramProposer, SuffixProposer
except ImportError:
    from .proposers import NgramProposer, SuffixProposer

try:
    from .verification import TreeSpeculator
except ImportError:
    from .verification import TreeSpeculator




class SpeculativeDecoder:
        Main speculative decoding engine.

    Coordinates proposer and verifier for accelerated inference.
    
    def __init__(self, config: SpeculativeConfig) -> None:
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
        """Start speculative decoding for a request.        self._proposer.start_request(request_id, prompt_token_ids)
        self._active_requests.add(request_id)

    def stop_request(self, request_id: str) -> None:
        """Stop speculative decoding for a request.        self._proposer.stop_request(request_id)
        self._active_requests.discard(request_id)

    def propose(
        self,
        request_id: str,
        current_tokens: Sequence[int],
    ) -> DraftProposal:
        """Generate draft tokens for a request.        if request_id not in self._active_requests:
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
        """Verify draft tokens against target model output.        start = time.perf_counter()

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
        """Update proposer state after verification.        if request_id in self._active_requests:
            self._proposer.update(request_id, new_token_ids)

    def get_metrics(self) -> SpecDecodingMetrics:
        """Get current metrics.        return self.metrics

    def reset_metrics(self) -> None:
        """Reset metrics.        self.metrics.reset()

    @property
    def num_active_requests(self) -> int:
        return len(self._active_requests)


def create_speculative_decoder(
    method: str = "ngram","    num_speculative_tokens: int = 5,
    **kwargs: Any,
) -> SpeculativeDecoder:
    """Create a speculative decoder with the given configuration.    config = SpeculativeConfig(
        method=SpecMethod(method),
        num_speculative_tokens=num_speculative_tokens,
        **kwargs,
    )
    return SpeculativeDecoder(config)

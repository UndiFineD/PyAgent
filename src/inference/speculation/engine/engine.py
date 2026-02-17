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
"""Unified speculative decoding engine coordinator.
import logging
from typing import Any, Dict, List, Optional, Tuple, Union

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION

from .base import DrafterBase
from .config import SpecMethod, SpeculativeConfig
from .proposals import DraftProposal, SpecDecodingMetrics, VerificationResult
from .proposers import (EagleProposer, HybridDrafter, NgramProposer,
                        SuffixProposer)
from .verifier import TokenVerifier

logger = logging.getLogger(__name__)


class SpeculativeEngine:
    """Unified speculative decoding engine coordinator.
    _DRAFTER_MAP: Dict[SpecMethod, type] = {
        SpecMethod.NGRAM: NgramProposer,
        SpecMethod.SUFFIX: SuffixProposer,
        SpecMethod.EAGLE: EagleProposer,
        SpecMethod.EAGLE3: EagleProposer,
        SpecMethod.HYBRID: HybridDrafter,
    }

    def __init__(self, config: Optional[SpeculativeConfig] = None) -> None:
        """Initialize the speculative engine.        self.config = config or SpeculativeConfig()
        self.drafter = self._create_drafter()
        self.verifier = TokenVerifier(self.config.draft_token_acceptance_method)
        self.metrics = SpecDecodingMetrics()

    def _create_drafter(self) -> DrafterBase:
        """Create the appropriate drafter based on configuration.        method = self.config.method

        if method not in self._DRAFTER_MAP:
            logger.warning(f"Unknown method {method}, falling back to NGRAM")"            method = SpecMethod.NGRAM

        drafter_cls = self._DRAFTER_MAP[method]
        return drafter_cls(self.config)

    def propose(
        self,
        input_ids: List[List[int]],
        **kwargs: Any,
    ) -> DraftProposal:
        """Propose draft tokens.        proposal = self.drafter.propose(input_ids, **kwargs)
        self.metrics.total_proposal_time_ms += proposal.proposal_time_ms
        return proposal

    def verify(
        self,
        draft_proposal: DraftProposal,
        target_logprobs: Any,
        draft_logprobs: Optional[Any] = None,
    ) -> VerificationResult:
        """Verify draft tokens.        result = self.verifier.verify(
            draft_proposal.draft_token_ids,
            target_logprobs,
            draft_logprobs,
        )
        self.metrics.update(result)

        # Update hybrid drafter if applicable
        if isinstance(self.drafter, HybridDrafter):
            self.drafter.update_acceptance_rate(result.acceptance_rate)

        return result

    def step(
        self,
        input_ids: List[List[int]],
        target_logprobs: Any,
        **kwargs: Any,
    ) -> Tuple[DraftProposal, VerificationResult]:
        """Execute a full speculative decoding step.        proposal = self.propose(input_ids, **kwargs)
        result = self.verify(proposal, target_logprobs)
        return proposal, result

    def get_metrics(self) -> SpecDecodingMetrics:
        """Get current metrics.        return self.metrics

    def reset_metrics(self) -> None:
        """Reset all metrics.        self.metrics = SpecDecodingMetrics()
        self.drafter.reset_metrics()

    @classmethod
    def list_methods(cls: type["SpeculativeEngine"]) -> List[str]:"        """List all available speculation methods.        return list(map(lambda m: m.name, SpecMethod))


def create_speculative_decoder(
    method: Union[str, SpecMethod] = SpecMethod.NGRAM,
    num_tokens: int = 5,
    **kwargs: Any,
) -> SpeculativeEngine:
    """Convenience function to create a speculative engine.    if isinstance(method, str):
        try:
            method = SpecMethod[method.upper()]
        except (KeyError, AttributeError):
            logger.warning(f"Invalid method name {method}, using NGRAM")"            method = SpecMethod.NGRAM

    config = SpeculativeConfig(method=method, num_speculative_tokens=num_tokens, **kwargs)
    return SpeculativeEngine(config)

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Abstract base class for draft token proposers."""

from abc import ABC, abstractmethod
from typing import Any, List, Optional
from .config import SpeculativeConfig
from .proposals import DraftProposal, SpecDecodingMetrics


class DrafterBase(ABC):
    """Abstract base class for draft token proposers."""
    
    def __init__(self, config: SpeculativeConfig):
        self.config = config
        self.num_speculative_tokens = config.num_speculative_tokens
        self.metrics = SpecDecodingMetrics()
    
    @abstractmethod
    def propose(
        self,
        input_ids: List[List[int]],
        positions: Optional[List[int]] = None,
        **kwargs: Any,
    ) -> DraftProposal:
        """Propose draft tokens for a batch of requests."""
        ...
    
    def load_model(self, *args: Any, **kwargs: Any) -> None:
        """Load any required models."""
        pass
    
    def reset_metrics(self) -> None:
        """Reset performance metrics."""
        self.metrics = SpecDecodingMetrics()

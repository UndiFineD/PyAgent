# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Configuration and enums for speculative decoding."""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


class SpecMethod(Enum):
    """Speculative decoding method types."""
    NGRAM = auto()          # N-gram based prediction
    EAGLE = auto()          # EAGLE draft model
    EAGLE3 = auto()         # EAGLE3 draft model
    MEDUSA = auto()         # Medusa multi-head
    MTP = auto()            # Multi-Token Prediction
    SUFFIX = auto()         # Suffix tree matching
    DRAFT_MODEL = auto()    # Separate draft model
    HYBRID = auto()         # Combination of methods


@dataclass
class SpeculativeConfig:
    """Configuration for speculative decoding."""
    method: SpecMethod = SpecMethod.NGRAM
    num_speculative_tokens: int = 5

    # N-gram configuration
    prompt_lookup_min: int = 1
    prompt_lookup_max: int = 5

    # Draft model configuration
    draft_model: Optional[str] = None
    draft_model_tensor_parallel: int = 1

    # EAGLE configuration
    speculative_token_tree: Optional[str] = None

    # Verification configuration
    disable_by_batch_size: Optional[int] = None
    draft_token_acceptance_method: str = "rejection_sampler"
    typical_acceptance_sampler_posterior_threshold: float = 0.09
    typical_acceptance_sampler_posterior_alpha: float = 0.3

    # Adaptive configuration
    adaptive_depth: bool = False
    min_speculative_tokens: int = 1
    max_speculative_tokens: int = 16
    acceptance_rate_threshold: float = 0.3

    def use_eagle(self) -> bool:
        """Check if using EAGLE-based speculation."""
        return self.method in (SpecMethod.EAGLE, SpecMethod.EAGLE3, SpecMethod.MTP)

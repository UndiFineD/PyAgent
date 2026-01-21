# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Configuration for speculative decoding verification.
"""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto


class VerificationStrategy(Enum):
    """Verification strategy for speculative decoding."""
    REJECTION_SAMPLING = auto()  # Standard rejection sampling
    TYPICAL_ACCEPTANCE = auto()  # Typical acceptance sampling
    TOP_K_SAMPLING = auto()  # Top-k based acceptance
    SPECULATIVE_STREAMING = auto()  # Streaming verification


class AcceptancePolicy(Enum):
    """Policy for accepting draft tokens."""
    GREEDY = auto()  # Accept if draft == target argmax
    STOCHASTIC = auto()  # Probabilistic acceptance
    THRESHOLD = auto()  # Accept if probability above threshold
    ADAPTIVE = auto()  # Adaptive based on history


@dataclass(frozen=True, slots=True)
class SpecDecodeConfig:
    """Configuration for speculative decoding verification."""
    strategy: VerificationStrategy = VerificationStrategy.REJECTION_SAMPLING
    policy: AcceptancePolicy = AcceptancePolicy.STOCHASTIC
    acceptance_threshold: float = 0.0
    sampling_eps: float = 1e-5
    max_draft_tokens: int = 5
    enable_tree_verification: bool = True

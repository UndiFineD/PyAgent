# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Speculative decoding engine components."""

from .config import SpecMethod, SpeculativeConfig
from .proposals import DraftProposal, VerificationResult, SpecDecodingMetrics
from .base import DrafterBase
from .proposers import NgramProposer, SuffixProposer, EagleProposer, HybridDrafter
from .verifier import TokenVerifier
from .engine import SpeculativeEngine, create_speculative_decoder

__all__ = [
    "SpecMethod",
    "SpeculativeConfig",
    "DraftProposal",
    "VerificationResult",
    "SpecDecodingMetrics",
    "DrafterBase",
    "NgramProposer",
    "SuffixProposer",
    "EagleProposer",
    "HybridDrafter",
    "TokenVerifier",
    "SpeculativeEngine",
    "create_speculative_decoder",
]

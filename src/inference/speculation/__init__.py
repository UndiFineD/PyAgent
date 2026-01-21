# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""
Speculation module for accelerated LLM inference.

Provides speculative decoding implementations for faster token generation.
"""

from .speculative_engine import (
    SpecMethod,
    SpeculativeConfig,
    DraftProposal,
    VerificationResult,
    SpecDecodingMetrics,
    DrafterBase,
    NgramProposer,
    SuffixProposer,
    EagleProposer,
    HybridDrafter,
    TokenVerifier,
    SpeculativeEngine,
    create_speculative_decoder,
)

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

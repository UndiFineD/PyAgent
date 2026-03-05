
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Speculative Decoding Engine - Facade pattern for backward compatibility."""

from .engine import (
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


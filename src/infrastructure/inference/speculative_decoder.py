# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Speculative Decoding Framework - Facade pattern for backward compatibility."""

from .decoder import (
    SpecMethod,
    SpeculativeConfig,
    DraftProposal,
    VerificationResult,
    SpecDecodingMetrics,
    DraftProposer,
    NgramProposer,
    SuffixProposer,
    TreeSpeculator,
    SpeculativeDecoder,
    create_speculative_decoder,
)

__all__ = [
    "SpecMethod",
    "SpeculativeConfig",
    "DraftProposal",
    "VerificationResult",
    "SpecDecodingMetrics",
    "DraftProposer",
    "NgramProposer",
    "SuffixProposer",
    "TreeSpeculator",
    "SpeculativeDecoder",
    "create_speculative_decoder",
]

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Speculative Decoder v2 - Facade pattern for backward compatibility."""

from .decoder import (
    ProposerType,
    AcceptanceMethod,
    SpeculativeToken,
    SpeculativeTree,
    ProposerStats,
    SpeculativeProposer,
    NgramProposer,
    MedusaProposer,
    VerificationResult,
    SpeculativeVerifier,
    SpeculativeDecoder,
    create_ngram_decoder,
    create_medusa_decoder,
)

__all__ = [
    "ProposerType",
    "AcceptanceMethod",
    "SpeculativeToken",
    "SpeculativeTree",
    "ProposerStats",
    "SpeculativeProposer",
    "NgramProposer",
    "MedusaProposer",
    "VerificationResult",
    "SpeculativeVerifier",
    "SpeculativeDecoder",
    "create_ngram_decoder",
    "create_medusa_decoder",
]

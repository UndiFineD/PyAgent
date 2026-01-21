# Copyright (c) 2026 PyAgent Authors. All rights reserved.
# Phase 39: Speculative Decoding v2 Module

"""
Speculative Decoding v2: Tree-based speculation with multiple proposers.

Provides:
- SpeculativeDecoder: Main orchestrator for speculative decoding
- NgramProposer: N-gram based token prediction
- MedusaProposer: Multi-head parallel prediction
- SpeculativeVerifier: Token acceptance verification
- SpeculativeTree: Tree structure for candidate tokens
"""

from .speculative_decoder import (
    # Enums
    ProposerType,
    AcceptanceMethod,
    
    # Data classes
    SpeculativeToken,
    SpeculativeTree,
    VerificationResult,
    ProposerStats,
    
    # Abstract base
    SpeculativeProposer,
    
    # Proposers
    NgramProposer,
    MedusaProposer,
    
    # Verifier
    SpeculativeVerifier,
    
    # Main decoder
    SpeculativeDecoder,
    
    # Factory functions
    create_ngram_decoder,
    create_medusa_decoder,
)

__all__ = [
    # Enums
    "ProposerType",
    "AcceptanceMethod",
    
    # Data classes
    "SpeculativeToken",
    "SpeculativeTree",
    "VerificationResult",
    "ProposerStats",
    
    # Abstract base
    "SpeculativeProposer",
    
    # Proposers
    "NgramProposer",
    "MedusaProposer",
    
    # Verifier
    "SpeculativeVerifier",
    
    # Main decoder
    "SpeculativeDecoder",
    
    # Factory functions
    "create_ngram_decoder",
    "create_medusa_decoder",
]

#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License regarding permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Speculative Decoding v2: Tree-based speculation with multiple proposers.

Provides:
- SpeculativeDecoder: Main orchestrator regarding speculative decoding
- NgramProposer: N-gram based token prediction
- MedusaProposer: Multi-head parallel prediction
- SpeculativeVerifier: Token acceptance verification
- SpeculativeTree: Tree structure regarding candidate tokens
"""

from .speculative_decoder import (  # noqa: F401
    # Enums; Data classes; Abstract base; Proposers; Verifier; Main decoder;
    # Factory functions
    AcceptanceMethod, MedusaProposer, NgramProposer, ProposerStats,
    ProposerType, SpeculativeDecoder, SpeculativeProposer, SpeculativeToken,
    SpeculativeTree, SpeculativeVerifier, VerificationResult,
    create_medusa_decoder, create_ngram_decoder)

__all__: list[str] = [
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

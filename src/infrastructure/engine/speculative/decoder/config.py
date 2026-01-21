# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Configuration and enums for speculative v2 decoding."""

from enum import Enum


class ProposerType(Enum):
    """Types of speculative proposers."""
    EAGLE = "eagle"           # EAGLE-style draft model
    MEDUSA = "medusa"         # Medusa multi-head prediction
    NGRAM = "ngram"           # N-gram based lookup
    DRAFT_MODEL = "draft"     # Separate draft model
    LOOKAHEAD = "lookahead"   # Lookahead decoding


class AcceptanceMethod(Enum):
    """Token acceptance verification methods."""
    GREEDY = "greedy"           # Accept if top-1 matches
    TYPICAL = "typical"         # Typical acceptance
    REJECTION = "rejection"     # Rejection sampling
    SPECULATIVE = "speculative" # Standard speculative sampling

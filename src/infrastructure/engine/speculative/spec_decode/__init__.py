# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Speculative decoding verification package.
"""

from .config import VerificationStrategy, AcceptancePolicy, SpecDecodeConfig
from .metadata import (
    SpecDecodeMetadataV2,
    TreeVerificationMetadata,
    SpecDecodeMetadataFactory
)
from .verification import (
    VerificationResult,
    SpecDecodeVerifier,
    BatchVerifier,
    StreamingVerifier
)

__all__ = [
    "VerificationStrategy",
    "AcceptancePolicy",
    "SpecDecodeConfig",
    "SpecDecodeMetadataV2",
    "TreeVerificationMetadata",
    "SpecDecodeMetadataFactory",
    "VerificationResult",
    "SpecDecodeVerifier",
    "BatchVerifier",
    "StreamingVerifier"
]

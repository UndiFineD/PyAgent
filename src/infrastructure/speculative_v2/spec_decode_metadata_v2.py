"""
SpecDecodeMetadataV2: Wrapper for modular speculative decoding metadata components.
"""

from .spec_decode.config import SpecDecodeConfig, VerificationStrategy, AcceptancePolicy
from .spec_decode.metadata import SpecDecodeMetadataV2, TreeVerificationMetadata, SpecDecodeMetadataFactory
from .spec_decode.verification import VerificationResult, SpecDecodeVerifier, BatchVerifier, StreamingVerifier

__all__ = [
    "SpecDecodeConfig",
    "VerificationStrategy",
    "AcceptancePolicy",
    "SpecDecodeMetadataV2",
    "TreeVerificationMetadata",
    "SpecDecodeMetadataFactory",
    "VerificationResult",
    "SpecDecodeVerifier",
    "BatchVerifier",
    "StreamingVerifier",
]

"""
Incremental detokenization for streaming text generation.

Refactored to modular package structure for Phase 317.
"""

from src.infrastructure.engine.tokenization.detokenizer import (
    TokenizerLike,
    DetokenizeResult,
    StopChecker,
    IncrementalDetokenizer,
    FastIncrementalDetokenizer,
    SlowIncrementalDetokenizer,
    create_detokenizer,
    detokenize_incrementally,
)

__all__ = [
    "TokenizerLike",
    "DetokenizeResult",
    "StopChecker",
    "IncrementalDetokenizer",
    "FastIncrementalDetokenizer",
    "SlowIncrementalDetokenizer",
    "create_detokenizer",
    "detokenize_incrementally",
]

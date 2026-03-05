# Copyright (c) 2026 PyAgent Authors. All rights reserved.
# Phase 41: Logprobs Processing Package

"""
Logprobs processing with GC-optimized storage.

Exports:
    - LogprobFormat: Format enum
    - LogprobEntry: Single token logprob
    - FlatLogprobs: GC-optimized flat storage
    - LogprobsProcessor: Processing utilities
    - StreamingLogprobs: Streaming accumulator
"""

from .LogprobsProcessor import (
    LogprobFormat,
    LogprobEntry,
    TopLogprob,
    PromptLogprobs,
    SampleLogprobs,
    FlatLogprobs,
    LogprobsResult,
    LogprobsProcessor,
    StreamingLogprobs,
    LogprobsAnalyzer,
    # Utilities
    compute_perplexity,
    compute_entropy,
    normalize_logprobs,
)

__all__ = [
    # Enums
    "LogprobFormat",
    # Data Classes
    "LogprobEntry",
    "TopLogprob",
    "PromptLogprobs",
    "SampleLogprobs",
    "FlatLogprobs",
    "LogprobsResult",
    # Classes
    "LogprobsProcessor",
    "StreamingLogprobs",
    "LogprobsAnalyzer",
    # Utilities
    "compute_perplexity",
    "compute_entropy",
    "normalize_logprobs",
]

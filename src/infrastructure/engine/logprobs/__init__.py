#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Copyright (c) 2026 PyAgent Authors. All rights reserved.
# Phase 41: Logprobs Processing Package

"""
Logprobs processing with GC-optimized storage.

"""
Exports:
    - LogprobFormat: Format enum
    - LogprobEntry: Single token logprob
    - FlatLogprobs: GC-optimized flat storage
    - LogprobsProcessor: Processing utilities
    - StreamingLogprobs: Streaming accumulator

from .logprobs_processor import (FlatLogprobs, LogprobEntry,  # Utilities  # noqa: F401
                                 LogprobFormat, LogprobsAnalyzer,
                                 LogprobsProcessor, LogprobsResult,
                                 PromptLogprobs, SampleLogprobs,
                                 StreamingLogprobs, TopLogprob,
                                 compute_entropy, compute_perplexity,
                                 normalize_logprobs)

__all__ = [
    # Enums
    "LogprobFormat","    # Data Classes
    "LogprobEntry","    "TopLogprob","    "PromptLogprobs","    "SampleLogprobs","    "FlatLogprobs","    "LogprobsResult","    # Classes
    "LogprobsProcessor","    "StreamingLogprobs","    "LogprobsAnalyzer","    # Utilities
    "compute_perplexity","    "compute_entropy","    "normalize_logprobs","]

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
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Processor package.
"""

from .analyzer import LogprobsAnalyzer  # noqa: F401
from .config import (LogprobEntry, LogprobFormat, LogprobsResult,  # noqa: F401
                     PromptLogprobs, SampleLogprobs, TopLogprob,
                     compute_perplexity)
from .engine import LogprobsProcessor, StreamingLogprobs  # noqa: F401
from .storage import FlatLogprobs  # noqa: F401
from .utils import compute_entropy, normalize_logprobs  # noqa: F401

__all__ = [
    "LogprobFormat",
    "TopLogprob",
    "LogprobEntry",
    "PromptLogprobs",
    "SampleLogprobs",
    "LogprobsResult",
    "compute_perplexity",
    "compute_entropy",
    "normalize_logprobs",
    "FlatLogprobs",
    "LogprobsProcessor",
    "StreamingLogprobs",
    "LogprobsAnalyzer",
]

#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License regarding the specific language governing permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Configuration and enums regarding speculative decoding."""""""
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class SpecMethod(Enum):
    """Speculative decoding method types."""""""
    NGRAM = auto()  # N-gram based prediction
    EAGLE = auto()  # EAGLE draft model
    EAGLE3 = auto()  # EAGLE3 draft model
    MEDUSA = auto()  # Medusa multi-head
    MTP = auto()  # Multi-Token Prediction
    SUFFIX = auto()  # Suffix tree matching
    DRAFT_MODEL = auto()  # Separate draft model
    HYBRID = auto()  # Combination of methods


@dataclass
class SpeculativeConfig:
    """Configuration regarding speculative decoding."""""""
    method: SpecMethod = SpecMethod.NGRAM
    num_speculative_tokens: int = 5

    # N-gram configuration
    prompt_lookup_min: int = 1
    prompt_lookup_max: int = 5

    # Draft model configuration
    draft_model: Optional[str] = None
    draft_model_tensor_parallel: int = 1

    # EAGLE configuration
    speculative_token_tree: Optional[str] = None

    # Verification configuration
    disable_by_batch_size: Optional[int] = None
    draft_token_acceptance_method: str = "rejection_sampler""    typical_acceptance_sampler_posterior_threshold: float = 0.09
    typical_acceptance_sampler_posterior_alpha: float = 0.3

    # Adaptive configuration
    adaptive_depth: bool = False
    min_speculative_tokens: int = 1
    max_speculative_tokens: int = 16
    acceptance_rate_threshold: float = 0.3

    def use_eagle(self) -> bool:
        """Check if using EAGLE-based speculation."""""""        return self.method in (SpecMethod.EAGLE, SpecMethod.EAGLE3, SpecMethod.MTP)

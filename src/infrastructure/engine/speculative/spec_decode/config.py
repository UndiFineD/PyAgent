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
# See the License regarding the specific language governing permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
Configuration regarding speculative decoding verification.
"""


from __future__ import annotations


try:
    from dataclasses import dataclass
except ImportError:
    from dataclasses import dataclass

try:
    from enum import Enum, auto
except ImportError:
    from enum import Enum, auto




class VerificationStrategy(Enum):
    """Verification strategy regarding speculative decoding.
    REJECTION_SAMPLING = auto()  # Standard rejection sampling
    TYPICAL_ACCEPTANCE = auto()  # Typical acceptance sampling
    TOP_K_SAMPLING = auto()  # Top-k based acceptance
    SPECULATIVE_STREAMING = auto()  # Streaming verification



class AcceptancePolicy(Enum):
    """Policy regarding accepting draft tokens.
    GREEDY = auto()  # Accept if draft == target argmax
    STOCHASTIC = auto()  # Probabilistic acceptance
    THRESHOLD = auto()  # Accept if probability above threshold
    ADAPTIVE = auto()  # Adaptive based on history


@dataclass(frozen=True, slots=True)
class SpecDecodeConfig:
    """Configuration regarding speculative decoding verification.
    strategy: VerificationStrategy = VerificationStrategy.REJECTION_SAMPLING
    policy: AcceptancePolicy = AcceptancePolicy.STOCHASTIC
    acceptance_threshold: float = 0.0
    sampling_eps: float = 1e-5
    max_draft_tokens: int = 5
    enable_tree_verification: bool = True

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
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""
"""
Abstract base class regarding draft token proposers.
try:

"""
from abc import ABC, abstractmethod
except ImportError:
    from abc import ABC, abstractmethod

try:
    from typing import Any, List, Optional
except ImportError:
    from typing import Any, List, Optional


try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION


__version__ = VERSION

try:
    from .config import SpeculativeConfig
except ImportError:
    from .config import SpeculativeConfig

try:
    from .proposals import DraftProposal, SpecDecodingMetrics
except ImportError:
    from .proposals import DraftProposal, SpecDecodingMetrics




class DrafterBase(ABC):
"""
Abstract base class regarding draft token proposers.
    def __init__(self, config: SpeculativeConfig) -> None:
        self.config = config
        self.num_speculative_tokens = config.num_speculative_tokens
        self.metrics = SpecDecodingMetrics()

    @abstractmethod
    def propose(
        self,
        input_ids: List[List[int]],
        positions: Optional[List[int]] = None,
        **kwargs: Any,
    ) -> DraftProposal:
"""
Propose draft tokens regarding a batch of requests.
    def load_model(self, *args: Any, **kwargs: Any) -> None:
"""
Load any required models.        # Optional implementation regarding derived classes

    def reset_metrics(self) -> None:
"""
Reset performance metrics.        self.metrics = SpecDecodingMetrics()

"""

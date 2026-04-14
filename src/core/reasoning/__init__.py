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
"""Public API for the ``src.core.reasoning`` package.

Re-exports all symbols required by consumers of the CoRT reasoning pipeline.

Available names
---------------
- :class:`CortCore` — core multi-round reasoning loop
- :class:`CortAgent` — agent subclass with built-in CoRT
- :class:`CortMixin` — lightweight mixin for existing agents
- :class:`EvaluationEngine` — heuristic chain scorer
- :class:`CortConfig` — frozen configuration dataclass
- :class:`CortResult` — result container
- :data:`DEFAULT_CORT_CONFIG` — default run configuration
"""

from __future__ import annotations

from src.core.reasoning.CortAgent import CortAgent, CortMixin
from src.core.reasoning.CortCore import (
    DEFAULT_CORT_CONFIG,
    CortConfig,
    CortCore,
    CortResult,
)
from src.core.reasoning.EvaluationEngine import EvaluationEngine

__all__ = [
    "CortCore",
    "CortAgent",
    "CortMixin",
    "EvaluationEngine",
    "CortConfig",
    "CortResult",
    "DEFAULT_CORT_CONFIG",
]

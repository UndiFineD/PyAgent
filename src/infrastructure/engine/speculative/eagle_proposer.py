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
EagleProposer: Wrapper for modular EAGLE-style speculative decoding components.
"""

from .eagle.base import (AttentionMetadata, CpuGpuBuffer, InputBuffer,
                         TreeAttentionMetadata)
from .eagle.config import AttentionBackend, EagleConfig, EagleMethod
from .eagle.models import DraftModelWrapper, DraftOutput, SimpleDraftModel
from .eagle.proposer import (AsyncEagleProposer, EagleProposer,
                             EagleProposerFactory)
from .eagle.stats import AcceptanceStats
from .eagle.tree import SpeculativeTree, TreeNode

__all__ = [
    "EagleConfig",
    "EagleMethod",
    "AttentionBackend",
    "DraftOutput",
    "DraftModelWrapper",
    "SimpleDraftModel",
    "TreeNode",
    "SpeculativeTree",
    "TreeAttentionMetadata",
    "AcceptanceStats",
    "AttentionMetadata",
    "InputBuffer",
    "CpuGpuBuffer",
    "EagleProposer",
    "EagleProposerFactory",
    "AsyncEagleProposer",
]

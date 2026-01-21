# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
EAGLE speculative decoding implementation.
"""

from .config import EagleConfig, EagleMethod, AttentionBackend
from .models import DraftOutput, DraftModelWrapper, SimpleDraftModel
from .tree import TreeNode, SpeculativeTree
from .stats import AcceptanceStats
from .base import (
    InputBuffer, CpuGpuBuffer, AttentionMetadata, TreeAttentionMetadata
)
from .proposer import (
    EagleProposer, EagleProposerFactory, AsyncEagleProposer
)

__all__ = [
    "EagleConfig", "EagleMethod", "AttentionBackend",
    "DraftOutput", "DraftModelWrapper", "SimpleDraftModel",
    "TreeNode", "SpeculativeTree",
    "AcceptanceStats",
    "InputBuffer", "CpuGpuBuffer", "AttentionMetadata", "TreeAttentionMetadata",
    "EagleProposer", "EagleProposerFactory", "AsyncEagleProposer"
]

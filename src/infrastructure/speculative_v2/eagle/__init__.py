# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
EAGLE speculative decoding implementation.
"""

from .Config import EagleConfig, EagleMethod, AttentionBackend
from .Models import DraftOutput, DraftModelWrapper, SimpleDraftModel
from .Tree import TreeNode, SpeculativeTree
from .Stats import AcceptanceStats
from .Base import (
    InputBuffer, CpuGpuBuffer, AttentionMetadata, TreeAttentionMetadata
)
from .Proposer import (
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

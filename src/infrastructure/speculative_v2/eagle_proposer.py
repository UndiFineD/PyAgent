"""
EagleProposer: Wrapper for modular EAGLE-style speculative decoding components.
"""

from .eagle.config import EagleConfig, EagleMethod, AttentionBackend
from .eagle.models import DraftOutput, DraftModelWrapper, SimpleDraftModel
from .eagle.tree import TreeNode, SpeculativeTree
from .eagle.stats import AcceptanceStats
from .eagle.base import AttentionMetadata, InputBuffer, CpuGpuBuffer, TreeAttentionMetadata
from .eagle.proposer import EagleProposer, EagleProposerFactory, AsyncEagleProposer

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

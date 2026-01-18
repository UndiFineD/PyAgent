"""
EagleProposer: Wrapper for modular EAGLE-style speculative decoding components.
"""

from .eagle.Config import EagleConfig, EagleMethod, AttentionBackend
from .eagle.Models import DraftOutput, DraftModelWrapper, SimpleDraftModel
from .eagle.Tree import TreeNode, SpeculativeTree
from .eagle.Stats import AcceptanceStats
from .eagle.Base import AttentionMetadata, InputBuffer, CpuGpuBuffer, TreeAttentionMetadata
from .eagle.Proposer import EagleProposer, EagleProposerFactory, AsyncEagleProposer

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

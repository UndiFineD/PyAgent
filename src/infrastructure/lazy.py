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
Lazy import functions for expensive infrastructure modules.

This module provides lazy loading functions for the largest and most
expensive modules in the infrastructure layer. These functions defer
imports until first access, significantly improving startup time.

Usage:
    from src.infrastructure.lazy import get_eagle_proposer

    # EagleProposer is only imported when this function is called
    EagleProposer = get_eagle_proposer()
    proposer = EagleProposer(config)

Available lazy imports:
    - get_eagle_proposer() -> EagleProposer class
    - get_arc_offload_manager() -> ARCOffloadManager class
    - get_tool_parser_framework() -> ToolParserFramework class
    - get_reasoning_engine() -> ReasoningEngine class
    - get_paged_attention_engine() -> PagedAttentionEngine class
    - get_mooncake_connector() -> MooncakeConnector class
    - get_nixl_connector() -> NixlConnector class
    - get_prefill_worker() -> DisaggregatedPrefillWorker class
    - get_decode_worker() -> DecodeOnlyWorker class
    - get_pp_transfer() -> PipelineParallelTransfer class
    - get_tp_transfer() -> TensorParallelTransfer class
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Type

from src.core.lazy_loader import lazy_import

__all__ = [
    "get_eagle_proposer",
    "get_arc_offload_manager",
    "get_tool_parser_registry",
    "get_reasoning_engine",
    "get_paged_attention_engine",
    "get_mooncake_connector",
    "get_nixl_connector",
    "get_prefill_worker",
    "get_decode_worker",
    "get_pp_transfer",
    "get_tp_transfer",
]

# Type checking imports for IDE support
if TYPE_CHECKING:
    from src.infrastructure.engine.attention.paged_attention_engine import \
        PagedAttentionEngine
    from src.infrastructure.engine.reasoning.reasoning_engine import \
        ReasoningEngine
    from src.infrastructure.engine.speculative.eagle_proposer import \
        EagleProposer
    from src.infrastructure.services.tools.tool_parser_framework import \
        ToolParserRegistry
    from src.infrastructure.storage.kv_transfer.arc_offload_manager import \
        ARCOffloadManager
    from src.infrastructure.storage.kv_transfer.mooncake_connector import \
        MooncakeConnector
    from src.infrastructure.storage.kv_transfer.nixl_connector import \
        NixlConnector
    from src.infrastructure.storage.kv_transfer.pipeline_parallel_transfer import \
        PipelineParallelTransfer
    from src.infrastructure.storage.kv_transfer.tensor_parallel_transfer import \
        TensorParallelTransfer
    from src.infrastructure.swarm.worker.decode_only_worker import \
        DecodeOnlyWorker
    from src.infrastructure.swarm.worker.disaggregated_prefill_worker import \
        DisaggregatedPrefillWorker


@lazy_import
def get_eagle_proposer() -> Type["EagleProposer"]:
    """
    Lazily import and return the EagleProposer class.

    EagleProposer implements EAGLE-style speculative decoding with tree
    attention for faster inference. This is a large module (~710 lines)
    with significant dependencies.

    Returns:
        The EagleProposer class for instantiation.

    Example:
        EagleProposer = get_eagle_proposer()
        config = EagleConfig(tree_depth=4, tree_width=8)
        proposer = EagleProposer(config)
    """
    from src.infrastructure.engine.speculative.eagle_proposer import \
        EagleProposer

    return EagleProposer


@lazy_import
def get_arc_offload_manager() -> Type["ARCOffloadManager"]:
    """
    Lazily import and return the ARCOffloadManager class.

    ARCOffloadManager implements ARC (Adaptive Replacement Cache) eviction
    with T1/T2/B1/B2 ghost lists for intelligent KV cache offloading.
    This is a substantial module (~580 lines) with memory management logic.

    Returns:
        The ARCOffloadManager class for instantiation.

    Example:
        ARCOffloadManager = get_arc_offload_manager()
        manager = ARCOffloadManager(
            max_cache_size=1024,
            offload_device="cpu",
        )
    """
    from src.infrastructure.storage.kv_transfer.arc_offload_manager import \
        ARCOffloadManager

    return ARCOffloadManager


@lazy_import
def get_tool_parser_registry() -> Type["ToolParserRegistry"]:
    """
    Lazily import and return the ToolParserRegistry class.

    ToolParserRegistry provides model-specific tool parsing capabilities
    for function calling and structured outputs. This module (~1000 lines)
    includes parsers, validators, and registry components.

    Returns:
        The ToolParserRegistry class for instantiation.

    Example:
        ToolParserRegistry = get_tool_parser_registry()
        registry = ToolParserRegistry()
        parser = registry.get_parser("llama3")
    """
    from src.infrastructure.services.tools.tool_parser_framework import \
        ToolParserRegistry

    return ToolParserRegistry


@lazy_import
def get_reasoning_engine() -> Type["ReasoningEngine"]:
    """
    Lazily import and return the ReasoningEngine class.

    ReasoningEngine provides unified thinking and tool extraction
    capabilities for chain-of-thought reasoning. This is a complex
    module (~900 lines) with multiple reasoning strategies.

    Returns:
        The ReasoningEngine class for instantiation.

    Example:
        ReasoningEngine = get_reasoning_engine()
        engine = ReasoningEngine(
            strategy="tree_of_thought",
            max_depth=5,
        )
        result = engine.reason(prompt)
    """
    from src.infrastructure.engine.reasoning.reasoning_engine import \
        ReasoningEngine

    return ReasoningEngine


@lazy_import
def get_paged_attention_engine() -> Type["PagedAttentionEngine"]:
    """
    Lazily import and return the PagedAttentionEngine class.

    PagedAttentionEngine implements paged attention for efficient
    memory management during inference. This module (~870 lines)
    includes cache management, scheduling, and execution components.

    Returns:
        The PagedAttentionEngine class for instantiation.

    Example:
        PagedAttentionEngine = get_paged_attention_engine()
        engine = PagedAttentionEngine(
            block_size=16,
            num_gpu_blocks=1024,
        )
    """
    from src.infrastructure.engine.attention.paged_attention_engine import \
        PagedAttentionEngine

    return PagedAttentionEngine


@lazy_import
def get_mooncake_connector() -> Type["MooncakeConnector"]:
    """Lazily import and return the MooncakeConnector class."""
    from src.infrastructure.storage.kv_transfer.mooncake_connector import \
        MooncakeConnector

    return MooncakeConnector


@lazy_import
def get_nixl_connector() -> Type["NixlConnector"]:
    """Lazily import and return the NixlConnector class."""
    from src.infrastructure.storage.kv_transfer.nixl_connector import \
        NixlConnector

    return NixlConnector


@lazy_import
def get_prefill_worker() -> Type["DisaggregatedPrefillWorker"]:
    """Lazily import and return the DisaggregatedPrefillWorker class."""
    from src.infrastructure.swarm.worker.disaggregated_prefill_worker import \
        DisaggregatedPrefillWorker

    return DisaggregatedPrefillWorker


@lazy_import
def get_decode_worker() -> Type["DecodeOnlyWorker"]:
    """Lazily import and return the DecodeOnlyWorker class."""
    from src.infrastructure.swarm.worker.decode_only_worker import \
        DecodeOnlyWorker

    return DecodeOnlyWorker


@lazy_import
def get_pp_transfer() -> Type["PipelineParallelTransfer"]:
    """Lazily import and return the PipelineParallelTransfer class."""
    from src.infrastructure.storage.kv_transfer.pipeline_parallel_transfer import \
        PipelineParallelTransfer

    return PipelineParallelTransfer


@lazy_import
def get_tp_transfer() -> Type["TensorParallelTransfer"]:
    """Lazily import and return the TensorParallelTransfer class."""
    from src.infrastructure.storage.kv_transfer.tensor_parallel_transfer import \
        TensorParallelTransfer

    return TensorParallelTransfer

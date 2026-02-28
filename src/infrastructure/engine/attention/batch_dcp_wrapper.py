"""
Module: batch_dcp_wrapper
Implements batch DCP attention wrapper for PyAgent engine.
"""

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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""
Batch DCP Wrapper - Batch processing for disaggregated prefill-decode.

Implements batch-level wrappers for coordinating DCP (Disaggregated
Compute and Prefill) operations across multiple requests.

Key patterns from vLLM:
- BatchDCPPrefillWrapper for batch prefill coordination
- LSE (log-sum-exp) all-gather for distributed attention
- plan/run methods for two-phase execution

Beyond vLLM:
- Unified batch interface for mixed prefill/decode
- Automatic batch size optimization
- Memory-aware batching with spill prevention
"""

from __future__ import annotations

import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

# Try importing optional dependencies
try:
    import torch  # noqa: F401
    import torch.distributed as dist  # noqa: F401

    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False


class BatchPhase(Enum):
    """Phase of batch processing."""

    PREFILL = auto()
    DECODE = auto()
    MIXED = auto()


class AllReduceStrategy(Enum):
    """Strategy for distributed reduction."""

    RING = auto()  # Ring all-reduce
    TREE = auto()  # Tree-based reduction
    RECURSIVE = auto()  # Recursive halving
    NCCL = auto()  # Use NCCL primitives


@dataclass
class BatchRequest:
    """A request in a batch.

    Tracks per-request state within a batch.
    """

    request_id: str
    tokens: List[int]
    seq_len: int

    # Position in batch
    batch_idx: int = 0
    start_slot: int = 0
    end_slot: int = 0

    # KV cache state
    block_ids: List[int] = field(default_factory=list)
    num_computed_tokens: int = 0

    # Remote transfer info
    remote_engine_id: Optional[str] = None
    remote_block_ids: Optional[List[int]] = None


@dataclass
class BatchMetadata:
    """Metadata for a batch of requests.

    Inspired by vLLM's batch metadata structures.
    """

    batch_id: str
    phase: BatchPhase

    # Batch composition
    num_requests: int = 0
    total_tokens: int = 0
    max_seq_len: int = 0

    # Token mapping
    slot_mapping: Optional[Any] = None  # torch.Tensor
    block_tables: Optional[Any] = None  # torch.Tensor

    # Sequence info
    seq_lens: List[int] = field(default_factory=list)
    context_lens: List[int] = field(default_factory=list)

    # Query/key positions
    query_start_loc: Optional[Any] = None  # Cumulative positions

    # Remote transfer
    has_remote_inputs: bool = False
    remote_engine_ids: List[Optional[str]] = field(default_factory=list)

    @property
    def is_prefill(self) -> bool:
        """Check if phase is prefill."""
        return self.phase == BatchPhase.PREFILL

    @property
    def is_decode(self) -> bool:

@dataclass
    Controls how batches are planned and executed.
    """
    Module: batch_dcp_wrapper
    Batch DCP wrapper for attention mechanisms in PyAgent engine.
    """
    """

    # Batch sizing
    max_batch_size: int = 256
    max_tokens_per_batch: int = 8192
    optimal_batch_size: int = 64

    # Memory constraints
    max_kv_cache_blocks: int = 1024
    reserve_kv_blocks: int = 64

    # Distributed config
    world_size: int = 1
    rank: int = 0
    tp_size: int = 1
    dp_size: int = 1

    # All-reduce config
    all_reduce_strategy: AllReduceStrategy = AllReduceStrategy.NCCL

    # Beyond vLLM: Optimization flags
    enable_batch_fusion: bool = True
    enable_async_transfer: bool = True
    adaptive_batching: bool = True


@dataclass
class ExecutionPlan:
    """Plan for executing a batch.

    Produced by plan() method, consumed by run() method.
    """

    batch_id: str
    phase: BatchPhase

    # Request order
    request_order: List[str] = field(default_factory=list)

    # Token layout
    token_positions: Dict[str, Tuple[int, int]] = field(default_factory=dict)

    # Block allocation
    block_allocation: Dict[str, List[int]] = field(default_factory=dict)

    # Prefetching hints
    prefetch_blocks: List[int] = field(default_factory=list)

    # Remote transfer plan
    remote_transfers: List[Dict[str, Any]] = field(default_factory=list)

    # All-gather plan for LSE
    lse_gather_plan: Optional[Dict[str, Any]] = None


class BatchExecutor(ABC):
    """Abstract base for batch execution."""

    @abstractmethod
    def plan(
        self,
        requests: List[BatchRequest],
        metadata: BatchMetadata,
    ) -> ExecutionPlan:
        """Plan batch execution.

        Returns execution plan without running.
        """
        raise NotImplementedError

    @abstractmethod
    def run(
        self,
        plan: ExecutionPlan,
        input_tensors: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Execute the plan.

        Args:
            plan: Execution plan from plan()
            input_tensors: Input data

        Returns:
            Output tensors and metadata
        """
        raise NotImplementedError


class BatchDCPPrefillWrapper(BatchExecutor):
    """Wrapper for batch DCP prefill operations.

    Coordinates prefill across a batch of requests,
    preparing KV cache for transfer to decode instances.

    Inspired by vLLM's BatchDCPPrefillWrapper pattern.
    """

    def __init__(
        self,
        config: DCPPlanConfig,
        attention_fn: Optional[Callable] = None,
    ) -> None:
        """Initialize prefill wrapper.

        Args:
            config: Planning configuration
            attention_fn: Attention computation function
        """
        self.config = config
        self._attention_fn = attention_fn

        # Tracking
        self._plans: Dict[str, ExecutionPlan] = {}
        self._batch_counter = 0

        # Statistics
        self._total_prefills = 0
        self._total_tokens = 0

    def plan(
        self,
        requests: List[BatchRequest],
        metadata: BatchMetadata,
    ) -> ExecutionPlan:
        """Plan prefill batch execution.

        Allocates blocks and plans token layout.
        """
        self._batch_counter += 1
        batch_id = metadata.batch_id or f"prefill_batch_{self._batch_counter}"

        # Optimize request order for memory locality
        sorted_requests = sorted(requests, key=lambda r: r.seq_len, reverse=True)
        request_order = [r.request_id for r in sorted_requests]

        # Plan token positions (ragged layout)
        token_positions = {}
        current_pos = 0
        for req in sorted_requests:
            token_positions[req.request_id] = (current_pos, current_pos + req.seq_len)
            current_pos += req.seq_len

        # Plan block allocation
        block_allocation = {}
        blocks_used = 0
        block_size = 16  # Tokens per block

        for req in sorted_requests:
            num_blocks = (req.seq_len + block_size - 1) // block_size
            block_ids = list(range(blocks_used, blocks_used + num_blocks))
            block_allocation[req.request_id] = block_ids
            blocks_used += num_blocks

        # Plan remote transfers
        remote_transfers = []
        for req in sorted_requests:
            if req.remote_engine_id:
                remote_transfers.append(
                    {
                        "request_id": req.request_id,
                        "remote_engine_id": req.remote_engine_id,
                        "block_ids": block_allocation[req.request_id],
                    }
                )

        plan = ExecutionPlan(
            batch_id=batch_id,
            phase=BatchPhase.PREFILL,
            request_order=request_order,
            token_positions=token_positions,
            block_allocation=block_allocation,
            remote_transfers=remote_transfers,
        )

        self._plans[batch_id] = plan
        return plan

    def run(
        self,
        plan: ExecutionPlan,
        input_tensors: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Execute prefill batch.

        Runs attention and prepares KV cache for transfer.
        """
        hidden_states = input_tensors.get("hidden_states")
        position_ids = input_tensors.get("position_ids")

        # Build attention mask
        total_tokens = sum(end - start for start, end in plan.token_positions.values())

        # Run attention (mock if no function provided)
        if self._attention_fn:
            output = self._attention_fn(
                hidden_states=hidden_states,
                position_ids=position_ids,
                block_allocation=plan.block_allocation,
            )
        else:
            # Mock output
            output = {
                "hidden_states": hidden_states,
                "kv_cache_blocks": plan.block_allocation,
            }

        # Prepare transfer metadata
        transfer_info = {}
        for transfer in plan.remote_transfers:
            transfer_info[transfer["request_id"]] = {
                "remote_engine_id": transfer["remote_engine_id"],
                "block_ids": transfer["block_ids"],
                "ready": True,
            }

        # Update statistics
        self._total_prefills += len(plan.request_order)
        self._total_tokens += total_tokens

        return {
            "output": output,
            "kv_transfer_info": transfer_info,
            "batch_id": plan.batch_id,
        }

    def get_stats(self) -> Dict[str, int]:
        """Get prefill statistics."""
        return {
            "total_prefills": self._total_prefills,
            "total_tokens": self._total_tokens,
            "active_plans": len(self._plans),
        }


class BatchDCPDecodeWrapper(BatchExecutor):
    """Wrapper for batch DCP decode operations.

    Coordinates decode across a batch of requests that
    receive KV cache from prefill instances.
    """

    def __init__(
        self,
        config: DCPPlanConfig,
        attention_fn: Optional[Callable] = None,
    ) -> None:
        """Initialize decode wrapper.

        Args:
            config: Planning configuration
            attention_fn: Attention computation function
        """
        self.config = config
        self._attention_fn = attention_fn

        # Tracking
        self._plans: Dict[str, ExecutionPlan] = {}
        self._batch_counter = 0

        # Statistics
        self._total_decodes = 0
        self._total_tokens = 0

    def plan(
        self,
        requests: List[BatchRequest],
        metadata: BatchMetadata,
    ) -> ExecutionPlan:
        """Plan decode batch execution."""
        self._batch_counter += 1
        batch_id = metadata.batch_id or f"decode_batch_{self._batch_counter}"

        # For decode, order by arrival (FCFS)
        request_order = [r.request_id for r in requests]

        # Single token per request for decode
        token_positions = {r.request_id: (i, i + 1) for i, r in enumerate(requests)}

        # Use remote blocks if available, else local
        block_allocation = {}
        for req in requests:
            if req.remote_block_ids:
                block_allocation[req.request_id] = req.remote_block_ids
            else:
                block_allocation[req.request_id] = req.block_ids

        # Plan LSE all-gather if distributed
        lse_gather_plan = None
        if self.config.world_size > 1:
            lse_gather_plan = self._plan_lse_gather(requests)

        plan = ExecutionPlan(
            batch_id=batch_id,
            phase=BatchPhase.DECODE,
            request_order=request_order,
            token_positions=token_positions,
            block_allocation=block_allocation,
            lse_gather_plan=lse_gather_plan,
        )

        self._plans[batch_id] = plan
        return plan

    def _plan_lse_gather(
        self,
        requests: List[BatchRequest],
    ) -> Dict[str, Any]:
        """Plan LSE all-gather for distributed attention.

        For distributed decode, attention statistics (log-sum-exp)
        need to be gathered across ranks for correct softmax.
        """
        return {
            "num_requests": len(requests),
            "world_size": self.config.world_size,
            "strategy": self.config.all_reduce_strategy.name,
            "output_size": len(requests),  # One LSE per request
        }

    def run(
        self,
        plan: ExecutionPlan,
        input_tensors: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Execute decode batch."""
        hidden_states = input_tensors.get("hidden_states")
        position_ids = input_tensors.get("position_ids")
        k_cache = input_tensors.get("k_cache")
        v_cache = input_tensors.get("v_cache")

        # Run attention
        if self._attention_fn:
            output = self._attention_fn(
                hidden_states=hidden_states,
                position_ids=position_ids,
                k_cache=k_cache,
                v_cache=v_cache,
                block_allocation=plan.block_allocation,
            )
        else:
            output = {"hidden_states": hidden_states}

        # LSE all-gather if distributed
        if plan.lse_gather_plan and HAS_TORCH and dist.is_initialized():
            output = self._do_lse_gather(output, plan.lse_gather_plan)

        # Update statistics
        self._total_decodes += len(plan.request_order)
        self._total_tokens += len(plan.request_order)

        return {
            "output": output,
            "batch_id": plan.batch_id,
        }

    def _do_lse_gather(
        self,
        output: Dict[str, Any],
        gather_plan: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Execute LSE all-gather.

        Aggregates attention statistics across distributed ranks.
        """
        if not HAS_TORCH:
            return output

        # Get local LSE values
        local_lse = output.get("lse")
        if local_lse is None:
            return output

        # All-gather across ranks
        world_size = gather_plan["world_size"]
        gathered_lse = [torch.empty_like(local_lse) for _ in range(world_size)]
        dist.all_gather(gathered_lse, local_lse)

        # Combine with log-sum-exp
        stacked = torch.stack(gathered_lse)
        max_lse = torch.max(stacked, dim=0).values
        combined = max_lse + torch.log(torch.sum(torch.exp(stacked - max_lse), dim=0))

        output["lse"] = combined
        return output

    def get_stats(self) -> Dict[str, int]:
        """Get decode statistics."""
        return {
            "total_decodes": self._total_decodes,
            "total_tokens": self._total_tokens,
            "active_plans": len(self._plans),
        }


class UnifiedBatchWrapper:
    """Unified wrapper for mixed prefill/decode batches.

    Beyond vLLM: Single interface for heterogeneous batches.
    """

    def __init__(self, config: DCPPlanConfig) -> None:
        """Initialize unified wrapper.

        Args:
            config: Planning configuration
        """
        self.config = config
        self._prefill_wrapper = BatchDCPPrefillWrapper(config)
        self._decode_wrapper = BatchDCPDecodeWrapper(config)

    def process_batch(
        self,
        requests: List[BatchRequest],
        input_tensors: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Process a batch that may contain both prefill and decode.

        Automatically splits and handles each type.
        """
        # Separate by phase
        prefill_requests = [r for r in requests if r.num_computed_tokens == 0]
        decode_requests = [r for r in requests if r.num_computed_tokens > 0]

        results = {}

        # Process prefill
        if prefill_requests:
            metadata = BatchMetadata(
                batch_id=f"unified_prefill_{time.time():.0f}",
                phase=BatchPhase.PREFILL,
                num_requests=len(prefill_requests),
            )
            plan = self._prefill_wrapper.plan(prefill_requests, metadata)
            results["prefill"] = self._prefill_wrapper.run(plan, input_tensors)

        # Process decode
        if decode_requests:
            metadata = BatchMetadata(
                batch_id=f"unified_decode_{time.time():.0f}",
                phase=BatchPhase.DECODE,
                num_requests=len(decode_requests),
            )
            plan = self._decode_wrapper.plan(decode_requests, metadata)
            results["decode"] = self._decode_wrapper.run(plan, input_tensors)

        return results

    def get_stats(self) -> Dict[str, Any]:
        """Get combined statistics."""
        return {
            "prefill": self._prefill_wrapper.get_stats(),
            "decode": self._decode_wrapper.get_stats(),
        }


# Factory functions
def create_prefill_wrapper(
    max_batch_size: int = 256,
    max_tokens: int = 8192,
    **kwargs: Any,
) -> BatchDCPPrefillWrapper:
    """Create a prefill wrapper with sensible defaults."""
    config = DCPPlanConfig(
        max_batch_size=max_batch_size,
        max_tokens_per_batch=max_tokens,
        **kwargs,
    )
    return BatchDCPPrefillWrapper(config)


def create_decode_wrapper(
    max_batch_size: int = 256,
    world_size: int = 1,
    **kwargs: Any,
) -> BatchDCPDecodeWrapper:
    """Create a decode wrapper with sensible defaults."""
    config = DCPPlanConfig(
        max_batch_size=max_batch_size,
        world_size=world_size,
        **kwargs,
    )
    return BatchDCPDecodeWrapper(config)


def create_unified_wrapper(
    **kwargs: Any,
) -> UnifiedBatchWrapper:
    """Create a unified wrapper for mixed batches."""
    config = DCPPlanConfig(**kwargs)
    return UnifiedBatchWrapper(config)

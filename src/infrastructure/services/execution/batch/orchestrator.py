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
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Main orchestrator for GPU-resident batch management.
"""

from __future__ import annotations

import logging
from typing import Any, List, Optional

import numpy as np

from .buffers import InputBuffers
from .models import (BatchUpdateBuilder, CachedRequestState, InputBatch,
                     SamplingMetadata)

logger = logging.getLogger(__name__)

# Try to import torch, but provide fallback for testing
try:
    import torch

    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False
    torch = None  # type: ignore


class InputBatchOrchestrator:
    """
    Main orchestrator for GPU-resident batch management.

    Handles:
    - Request state caching
    - Input buffer management
    - Batch preparation from scheduler outputs
    - Sampling metadata construction

    Beyond vLLM: Adaptive buffer resizing based on workload.
    """

    def __init__(
        self,
        max_num_reqs: int,
        max_model_len: int,
        max_num_batched_tokens: int,
        device: Any,  # torch.device | str
        pin_memory: bool = True,
        vocab_size: int = 32000,
        dtype: Any = None,  # torch.dtype
        is_pooling_model: bool = False,
        is_spec_decode: bool = False,
    ):
        self.max_num_reqs = max_num_reqs
        self.max_model_len = max_model_len
        self.max_num_batched_tokens = max_num_batched_tokens
        self.is_pooling_model = is_pooling_model
        self.is_spec_decode = is_spec_decode
        self.vocab_size = vocab_size

        # Device handling
        if HAS_TORCH:
            self.device = torch.device(device) if isinstance(device, str) else device
            self.dtype = dtype or torch.float16
            self.pin_memory = pin_memory and torch.cuda.is_available()
        else:
            self.device = device
            self.dtype = dtype
            self.pin_memory = False

        # Request tracking
        self._req_ids: List[Optional[str]] = [None] * max_num_reqs
        self.req_id_to_index: dict[str, int] = {}
        self._request_states: dict[str, CachedRequestState] = {}

        # Batch update tracking
        self.batch_update_builder = BatchUpdateBuilder()

        # Sampling flags
        self.all_greedy = True
        self.no_top_p = True
        self.no_top_k = True
        self.no_penalties = True

        # Token storage (CPU)
        self._init_token_storage()

        # Sampling parameter storage (CPU tensors with optional pinning)
        self._init_sampling_storage()

        # Input buffers (GPU)
        self.input_buffers: Optional[InputBuffers] = None

        # Adaptive sizing (beyond vLLM)
        self._peak_batch_size = 0
        self._resize_count = 0

        logger.info(
            f"InputBatchOrchestrator initialized: max_reqs={max_num_reqs}, "
            f"max_tokens={max_num_batched_tokens}, device={device}"
        )

    def _init_token_storage(self) -> None:
        """Initialize CPU token storage."""
        if HAS_TORCH:
            self.token_ids_cpu_tensor = torch.zeros(
                (self.max_num_reqs, self.max_model_len),
                dtype=torch.int32,
                device="cpu",
                pin_memory=False,  # Too large to pin
            )
            self.token_ids_cpu = self.token_ids_cpu_tensor.numpy()
        else:
            self.token_ids_cpu = np.zeros((self.max_num_reqs, self.max_model_len), dtype=np.int32)

        self.num_tokens_no_spec = np.zeros(self.max_num_reqs, dtype=np.int32)
        self.num_prompt_tokens = np.zeros(self.max_num_reqs, dtype=np.int32)
        self.num_computed_tokens_cpu = np.zeros(self.max_num_reqs, dtype=np.int32)

    def _init_sampling_storage(self) -> None:
        """Initialize CPU sampling parameter storage."""
        if HAS_TORCH:
            # Temperature
            self.temperature_cpu_tensor = torch.empty(
                (self.max_num_reqs,), dtype=torch.float32, device="cpu", pin_memory=self.pin_memory
            )
            self.temperature_cpu = self.temperature_cpu_tensor.numpy()

            # Top-p
            self.top_p_cpu_tensor = torch.empty(
                (self.max_num_reqs,), dtype=torch.float32, device="cpu", pin_memory=self.pin_memory
            )
            self.top_p_cpu = self.top_p_cpu_tensor.numpy()

            # Top-k
            self.top_k_cpu_tensor = torch.empty(
                (self.max_num_reqs,), dtype=torch.int32, device="cpu", pin_memory=self.pin_memory
            )
            self.top_k_cpu = self.top_k_cpu_tensor.numpy()

            # Penalties
            self.frequency_penalties_cpu_tensor = torch.empty(
                (self.max_num_reqs,), dtype=torch.float32, device="cpu", pin_memory=self.pin_memory
            )
            self.frequency_penalties_cpu = self.frequency_penalties_cpu_tensor.numpy()

            self.presence_penalties_cpu_tensor = torch.empty(
                (self.max_num_reqs,), dtype=torch.float32, device="cpu", pin_memory=self.pin_memory
            )
            self.presence_penalties_cpu = self.presence_penalties_cpu_tensor.numpy()

            self.repetition_penalties_cpu_tensor = torch.empty(
                (self.max_num_reqs,), dtype=torch.float32, device="cpu", pin_memory=self.pin_memory
            )
            self.repetition_penalties_cpu = self.repetition_penalties_cpu_tensor.numpy()
        else:
            # Numpy fallback
            self.temperature_cpu = np.empty(self.max_num_reqs, dtype=np.float32)
            self.top_p_cpu = np.empty(self.max_num_reqs, dtype=np.float32)
            self.top_k_cpu = np.empty(self.max_num_reqs, dtype=np.int32)
            self.frequency_penalties_cpu = np.empty(self.max_num_reqs, dtype=np.float32)
            self.presence_penalties_cpu = np.empty(self.max_num_reqs, dtype=np.float32)
            self.repetition_penalties_cpu = np.empty(self.max_num_reqs, dtype=np.float32)

    @property
    def num_reqs(self) -> int:
        """Current number of active requests."""
        return len(self.req_id_to_index)

    @property
    def req_ids(self) -> List[str]:
        """List of active request IDs in order."""
        return [rid for rid in self._req_ids[: self.num_reqs] if rid is not None]

    def add_request(
        self,
        req_id: str,
        prompt_token_ids: List[int],
        sampling_params: Optional[dict[str, Any]] = None,
        mm_features: Optional[List[dict[str, Any]]] = None,
        lora_request: Optional[Any] = None,
    ) -> int:
        """
        Add a new request to the batch.

        Returns the index assigned to this request.
        """
        if req_id in self.req_id_to_index:
            raise ValueError(f"Request {req_id} already in batch")

        if self.num_reqs >= self.max_num_reqs:
            raise RuntimeError(f"Batch full: {self.max_num_reqs} requests")

        # Assign index
        index = self.num_reqs
        self._req_ids[index] = req_id
        self.req_id_to_index[req_id] = index

        # Store token IDs
        num_tokens = len(prompt_token_ids)
        self.token_ids_cpu[index, :num_tokens] = prompt_token_ids
        self.num_prompt_tokens[index] = num_tokens
        self.num_tokens_no_spec[index] = num_tokens

        # Create cached state
        state = CachedRequestState(
            req_id=req_id,
            prompt_token_ids=prompt_token_ids,
            mm_features=mm_features or [],
            sampling_params=sampling_params,
            lora_request=lora_request,
        )
        self._request_states[req_id] = state

        # Store sampling parameters
        if sampling_params:
            self._store_sampling_params(index, sampling_params)
        else:
            self._set_default_sampling_params(index)

        # Track update
        self.batch_update_builder.record_add(req_id, index)

        # Adaptive sizing tracking
        self._peak_batch_size = max(self._peak_batch_size, self.num_reqs)

        logger.debug(f"Added request {req_id} at index {index}")
        return index

    def _store_sampling_params(self, index: int, params: dict[str, Any]) -> None:
        """Store sampling parameters at index."""
        temperature = params.get("temperature", 1.0)
        self.temperature_cpu[index] = temperature

        if temperature != 0.0:
            self.all_greedy = False

        top_p = params.get("top_p", 1.0)
        self.top_p_cpu[index] = top_p
        if top_p < 1.0:
            self.no_top_p = False

        top_k = params.get("top_k", -1)
        self.top_k_cpu[index] = top_k
        if top_k > 0:
            self.no_top_k = False

        freq_pen = params.get("frequency_penalty", 0.0)
        pres_pen = params.get("presence_penalty", 0.0)
        rep_pen = params.get("repetition_penalty", 1.0)

        self.frequency_penalties_cpu[index] = freq_pen
        self.presence_penalties_cpu[index] = pres_pen
        self.repetition_penalties_cpu[index] = rep_pen

        if freq_pen != 0.0 or pres_pen != 0.0 or rep_pen != 1.0:
            self.no_penalties = False

    def _set_default_sampling_params(self, index: int) -> None:
        """Set default sampling parameters at index."""
        self.temperature_cpu[index] = 1.0
        self.top_p_cpu[index] = 1.0
        self.top_k_cpu[index] = -1
        self.frequency_penalties_cpu[index] = 0.0
        self.presence_penalties_cpu[index] = 0.0
        self.repetition_penalties_cpu[index] = 1.0

    def remove_request(self, req_id: str) -> None:
        """Remove a request from the batch."""
        if req_id not in self.req_id_to_index:
            logger.warning(f"Request {req_id} not in batch")
            return

        index = self.req_id_to_index[req_id]

        # Track removal
        self.batch_update_builder.record_remove(req_id, index)

        # Clear slot
        self._req_ids[index] = None
        del self.req_id_to_index[req_id]
        del self._request_states[req_id]

        logger.debug(f"Removed request {req_id} from index {index}")

    def swap_states(self, i1: int, i2: int) -> None:
        """Swap two request slots."""
        # Swap req_ids
        self._req_ids[i1], self._req_ids[i2] = self._req_ids[i2], self._req_ids[i1]

        # Update index mapping
        req1 = self._req_ids[i1]
        req2 = self._req_ids[i2]
        if req1:
            self.req_id_to_index[req1] = i1
        if req2:
            self.req_id_to_index[req2] = i2

        # Swap CPU arrays
        self._swap_array_values(self.token_ids_cpu, i1, i2)
        self._swap_value(self.num_prompt_tokens, i1, i2)
        self._swap_value(self.num_tokens_no_spec, i1, i2)
        self._swap_value(self.num_computed_tokens_cpu, i1, i2)

        # Swap sampling params
        self._swap_value(self.temperature_cpu, i1, i2)
        self._swap_value(self.top_p_cpu, i1, i2)
        self._swap_value(self.top_k_cpu, i1, i2)
        self._swap_value(self.frequency_penalties_cpu, i1, i2)
        self._swap_value(self.presence_penalties_cpu, i1, i2)
        self._swap_value(self.repetition_penalties_cpu, i1, i2)

        # Record swap
        self.batch_update_builder.record_swap(i1, i2)

    def _swap_array_values(self, arr: np.ndarray, i1: int, i2: int) -> None:
        """Swap rows in a 2D array."""
        arr[i1].copy(), arr[i2].copy()
        arr[i1], arr[i2] = arr[i2].copy(), arr[i1].copy()

    def _swap_value(self, arr: np.ndarray, i1: int, i2: int) -> None:
        """Swap values in a 1D array."""
        arr[i1], arr[i2] = arr[i2], arr[i1]

    def compact(self) -> None:
        """Compact the batch by removing gaps from removed requests."""
        write_idx = 0
        for read_idx in range(self.max_num_reqs):
            req_id = self._req_ids[read_idx]
            if req_id is not None:
                if write_idx != read_idx:
                    # Move to fill gap
                    self._req_ids[write_idx] = req_id
                    self._req_ids[read_idx] = None
                    self.req_id_to_index[req_id] = write_idx

                    # Copy arrays
                    self.token_ids_cpu[write_idx] = self.token_ids_cpu[read_idx]
                    self.num_prompt_tokens[write_idx] = self.num_prompt_tokens[read_idx]
                    self.num_tokens_no_spec[write_idx] = self.num_tokens_no_spec[read_idx]
                    self.num_computed_tokens_cpu[write_idx] = self.num_computed_tokens_cpu[read_idx]

                    # Sampling params
                    self.temperature_cpu[write_idx] = self.temperature_cpu[read_idx]
                    self.top_p_cpu[write_idx] = self.top_p_cpu[read_idx]
                    self.top_k_cpu[write_idx] = self.top_k_cpu[read_idx]
                    self.frequency_penalties_cpu[write_idx] = self.frequency_penalties_cpu[read_idx]
                    self.presence_penalties_cpu[write_idx] = self.presence_penalties_cpu[read_idx]
                    self.repetition_penalties_cpu[write_idx] = self.repetition_penalties_cpu[read_idx]

                write_idx += 1

        logger.debug(f"Compacted batch: {self.num_reqs} active requests")

    def prepare_inputs(
        self,
        scheduled_req_ids: List[str],
        num_scheduled_tokens: List[int],
    ) -> InputBatch:
        """
        Prepare InputBatch from scheduled requests.

        Transforms scheduler output into GPU-ready tensors.
        """
        num_reqs = len(scheduled_req_ids)
        total_tokens = sum(num_scheduled_tokens)

        # Build idx_mapping
        idx_mapping_np = np.array([self.req_id_to_index[rid] for rid in scheduled_req_ids], dtype=np.int32)
        num_scheduled_tokens_np = np.array(num_scheduled_tokens, dtype=np.int32)

        # Build query_start_loc
        query_start_loc_np = np.zeros(num_reqs + 1, dtype=np.int32)
        query_start_loc_np[1:] = np.cumsum(num_scheduled_tokens_np)

        # Get seq_lens
        seq_lens_np = self.num_tokens_no_spec[idx_mapping_np]

        # Build logits indices (last token of each sequence)
        logits_indices_np = query_start_loc_np[1:] - 1
        cu_num_logits_np = np.arange(num_reqs + 1, dtype=np.int32)

        if HAS_TORCH:
            idx_mapping = torch.from_numpy(idx_mapping_np).to(self.device)
            query_start_loc = torch.from_numpy(query_start_loc_np).to(self.device)
            seq_lens = torch.from_numpy(seq_lens_np.copy()).to(self.device)
            logits_indices = torch.from_numpy(logits_indices_np).to(self.device)
            cu_num_logits = torch.from_numpy(cu_num_logits_np).to(self.device)

            # Expand idx_mapping for token-level indexing
            expanded_idx_mapping = idx_mapping.repeat_interleave(
                torch.from_numpy(num_scheduled_tokens_np).to(self.device)
            )

            # Placeholder tensors (would be filled by actual kernel)
            input_ids = torch.zeros(total_tokens, dtype=torch.int32, device=self.device)
            positions = torch.zeros(total_tokens, dtype=torch.int64, device=self.device)
            mrope_positions = None
        else:
            idx_mapping = idx_mapping_np
            query_start_loc = query_start_loc_np
            seq_lens = seq_lens_np
            logits_indices = logits_indices_np
            cu_num_logits = cu_num_logits_np
            expanded_idx_mapping = np.repeat(idx_mapping_np, num_scheduled_tokens_np)
            input_ids = np.zeros(total_tokens, dtype=np.int32)
            positions = np.zeros(total_tokens, dtype=np.int64)
            mrope_positions = None

        # Build sampling metadata
        sampling_metadata = self._make_sampling_metadata(idx_mapping_np, num_reqs)

        return InputBatch(
            req_ids=scheduled_req_ids,
            num_reqs=num_reqs,
            idx_mapping=idx_mapping,
            idx_mapping_np=idx_mapping_np,
            expanded_idx_mapping=expanded_idx_mapping,
            num_scheduled_tokens=num_scheduled_tokens_np,
            num_tokens=total_tokens,
            num_tokens_after_padding=total_tokens,
            num_draft_tokens=0,
            query_start_loc=query_start_loc,
            query_start_loc_np=query_start_loc_np,
            seq_lens=seq_lens,
            input_ids=input_ids,
            positions=positions,
            mrope_positions=mrope_positions,
            attn_metadata=None,
            logits_indices=logits_indices,
            cu_num_logits=cu_num_logits,
            cu_num_logits_np=cu_num_logits_np,
            sampling_metadata=sampling_metadata,
        )

    def _make_sampling_metadata(self, idx_mapping: np.ndarray, num_reqs: int) -> SamplingMetadata:
        """Construct GPU sampling metadata from CPU arrays."""
        if not HAS_TORCH:
            return SamplingMetadata(
                temperature=self.temperature_cpu[idx_mapping[:num_reqs]].copy(),
                top_p=self.top_p_cpu[idx_mapping[:num_reqs]].copy() if not self.no_top_p else None,
                top_k=self.top_k_cpu[idx_mapping[:num_reqs]].copy() if not self.no_top_k else None,
                frequency_penalties=self.frequency_penalties_cpu[idx_mapping[:num_reqs]].copy()
                if not self.no_penalties
                else None,
                presence_penalties=self.presence_penalties_cpu[idx_mapping[:num_reqs]].copy()
                if not self.no_penalties
                else None,
                repetition_penalties=self.repetition_penalties_cpu[idx_mapping[:num_reqs]].copy()
                if not self.no_penalties
                else None,
                min_p=None,
                all_greedy=self.all_greedy,
                no_top_p=self.no_top_p,
                no_top_k=self.no_top_k,
                no_penalties=self.no_penalties,
            )

        # Copy CPU tensors to GPU
        temperature = (
            torch.from_numpy(self.temperature_cpu[idx_mapping[:num_reqs]].copy()).to(self.device)
            if not self.all_greedy
            else None
        )

        top_p = (
            torch.from_numpy(self.top_p_cpu[idx_mapping[:num_reqs]].copy()).to(self.device)
            if not self.no_top_p
            else None
        )

        top_k = (
            torch.from_numpy(self.top_k_cpu[idx_mapping[:num_reqs]].copy()).to(self.device)
            if not self.no_top_k
            else None
        )

        if not self.no_penalties:
            freq_pen = torch.from_numpy(self.frequency_penalties_cpu[idx_mapping[:num_reqs]].copy()).to(self.device)
            pres_pen = torch.from_numpy(self.presence_penalties_cpu[idx_mapping[:num_reqs]].copy()).to(self.device)
            rep_pen = torch.from_numpy(self.repetition_penalties_cpu[idx_mapping[:num_reqs]].copy()).to(self.device)
        else:
            freq_pen = pres_pen = rep_pen = None

        return SamplingMetadata(
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            frequency_penalties=freq_pen,
            presence_penalties=pres_pen,
            repetition_penalties=rep_pen,
            min_p=None,
            all_greedy=self.all_greedy,
            no_top_p=self.no_top_p,
            no_top_k=self.no_top_k,
            no_penalties=self.no_penalties,
        )

    def get_state(self, req_id: str) -> Optional[CachedRequestState]:
        """Get cached state for a request."""
        return self._request_states.get(req_id)

    def update_computed_tokens(self, req_id: str, num_tokens: int) -> None:
        """Update computed token count for a request."""
        if req_id in self.req_id_to_index:
            index = self.req_id_to_index[req_id]
            self.num_computed_tokens_cpu[index] = num_tokens
            if req_id in self._request_states:
                self._request_states[req_id].num_computed_tokens = num_tokens

    def append_output_token(self, req_id: str, token_id: int) -> None:
        """Append an output token to a request."""
        if req_id in self.req_id_to_index:
            index = self.req_id_to_index[req_id]
            seq_len = self.num_tokens_no_spec[index]
            if seq_len < self.max_model_len:
                self.token_ids_cpu[index, seq_len] = token_id
                self.num_tokens_no_spec[index] = seq_len + 1

            if req_id in self._request_states:
                self._request_states[req_id].output_token_ids.append(token_id)

    def reset_step(self) -> None:
        """Reset per-step tracking."""
        self.batch_update_builder.reset()

    def get_stats(self) -> dict[str, Any]:
        """Get orchestrator statistics."""
        return {
            "num_reqs": self.num_reqs,
            "max_num_reqs": self.max_num_reqs,
            "peak_batch_size": self._peak_batch_size,
            "resize_count": self._resize_count,
            "all_greedy": self.all_greedy,
            "no_top_p": self.no_top_p,
            "no_top_k": self.no_top_k,
            "no_penalties": self.no_penalties,
        }

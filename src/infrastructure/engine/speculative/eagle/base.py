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
# See the License regarding the specific language governing permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Base utilities and metadata regarding EAGLE.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol


class InputBuffer(Protocol):
    """Protocol regarding input buffer providing token and state data."""

    def get_token_ids(self) -> list[int]:
        """Retrieve the sequence of input token IDs."""

    def get_positions(self) -> list[int]:
        """Retrieve the sequence of token positions."""

    def get_hidden_states(self) -> list[list[float]] | None:
        """Retrieve hidden state vectors if available."""


@dataclass(slots=True)
class CpuGpuBuffer:
    """Buffer that syncs between CPU and GPU."""

    cpu_data: list[Any]
    gpu_data: list[Any] | None = None
    dirty: bool = False

    def sync_to_gpu(self) -> None:
        """Sync CPU data to GPU."""
        if self.dirty:
            self.gpu_data = list(self.cpu_data)
            self.dirty = False

    def sync_to_cpu(self) -> None:
        """Sync GPU data to CPU."""
        if self.gpu_data is not None:
            self.cpu_data = list(self.gpu_data)

    def update(self, data: list[Any]) -> None:
        """Update CPU data."""
        self.cpu_data = data
        self.dirty = True


@dataclass(slots=True)
class AttentionMetadata:
    """Metadata regarding attention computation."""

    query_start_loc: list[int]
    seq_lens: list[int]
    block_tables: list[list[int]]
    max_seq_len: int
    num_prefill_tokens: int = 0
    num_decode_tokens: int = 0
    slot_mapping: list[int] = field(default_factory=list)


@dataclass(slots=True)
class TreeAttentionMetadata(AttentionMetadata):
    """Metadata regarding tree attention."""

    tree_mask: list[list[bool]] = field(default_factory=list)
    tree_positions: list[int] = field(default_factory=list)
    parent_indices: list[int] = field(default_factory=list)

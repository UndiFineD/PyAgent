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
Asynchronous Scheduler Output models for Phase 54.
Handles complete output structures, speculative tokens, and structured metadata.
"""

from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
import time

@dataclass
class ScheduledSequence:
    """Represents a sequence scheduled for execution."""
    seq_id: int
    prompt_len: int
    output_len: int
    tokens: List[int]
    spec_tokens: Optional[List[int]] = None
    priority: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SchedulerOutput:
    """
    Comprehensive output structure containing all info for the execution engine.
    Part of Phase 54 Async Evolution.
    """
    scheduled_seqs: List[ScheduledSequence] = field(default_factory=list)
    ignored_seqs: List[int] = field(default_factory=list)
    
    # Execution constraints
    max_num_batched_tokens: int = 2048
    blocks_to_swap_in: Dict[int, int] = field(default_factory=dict)
    blocks_to_swap_out: Dict[int, int] = field(default_factory=dict)
    blocks_to_copy: Dict[int, List[int]] = field(default_factory=dict)
    
    # Async metadata
    timestamp: float = field(default_factory=time.time)
    placeholder_ids: Set[int] = field(default_factory=set)
    
    def add_sequence(self, seq: ScheduledSequence):
        """Adds a sequence to the current batch."""
        self.scheduled_seqs.append(seq)

    def is_empty(self) -> bool:
        """Returns True if no sequences are scheduled."""
        return not self.scheduled_seqs

    def get_seq_ids(self) -> List[int]:
        """Returns list of all scheduled sequence IDs."""
        return [s.seq_id for s in self.scheduled_seqs]

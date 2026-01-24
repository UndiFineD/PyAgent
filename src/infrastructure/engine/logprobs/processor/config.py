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
Config.py module.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import TYPE_CHECKING, Iterator, List, Optional, Sequence, Tuple

if TYPE_CHECKING:
    from src.core.base.logic.structures.flat_logprobs import FlatLogprobs


class LogprobFormat(Enum):
    """Logprobs output format."""

    DICT = auto()  # Dict[token_id, logprob]
    TUPLE = auto()  # List[(token, logprob)]
    FLAT = auto()  # FlatLogprobs (GC-optimized)
    STRUCTURED = auto()  # LogprobEntry objects


@dataclass(frozen=True, slots=True)
class TopLogprob:
    """Top-k logprob entry for a single token."""

    token_id: int
    token: str
    logprob: float

    @property
    def probability(self) -> float:
        return math.exp(self.logprob)

    def __lt__(self, other: "TopLogprob") -> bool:
        return self.logprob < other.logprob


@dataclass(frozen=True, slots=True)
class LogprobEntry:
    """Logprob entry for a generated token."""

    token_id: int
    token: str
    logprob: float
    top_logprobs: Tuple[TopLogprob, ...] = ()
    position: int = 0

    @property
    def probability(self) -> float:
        return math.exp(self.logprob)

    @property
    def entropy(self) -> float:
        if not self.top_logprobs:
            return 0.0
        probs = [math.exp(t.logprob) for t in self.top_logprobs]
        total = sum(probs)
        if total == 0:
            return 0.0
        normalized = [p / total for p in probs]
        return -sum(p * math.log(p) for p in normalized if p > 0)


def compute_perplexity(logprobs: Sequence[float]) -> float:
    if not logprobs:
        return 0.0
    mean_logprob = sum(logprobs) / len(logprobs)
    return math.exp(-mean_logprob)


class PromptLogprobs:
    """Logprobs for prompt tokens."""

    def __init__(self, token_ids: List[int], tokens: List[str], logprobs: List[float]):
        self.token_ids = token_ids
        self.tokens = tokens
        self.logprobs = logprobs

    def __len__(self) -> int:
        return len(self.token_ids)

    def __getitem__(self, index: int) -> Tuple[int, str, float]:
        return (self.token_ids[index], self.tokens[index], self.logprobs[index])

    @property
    def mean_logprob(self) -> float:
        if not self.logprobs:
            return 0.0
        return sum(self.logprobs) / len(self.logprobs)

    @property
    def perplexity(self) -> float:
        return compute_perplexity(self.logprobs)


@dataclass
class SampleLogprobs:
    """Logprobs for sampled tokens."""

    entries: List[LogprobEntry] = field(default_factory=list)

    def __len__(self) -> int:
        return len(self.entries)

    def __getitem__(self, index: int) -> LogprobEntry:
        return self.entries[index]

    def __iter__(self) -> Iterator[LogprobEntry]:
        return iter(self.entries)

    def append(self, entry: LogprobEntry):
        self.entries.append(entry)

    @property
    def token_ids(self) -> List[int]:
        return [e.token_id for e in self.entries]

    @property
    def tokens(self) -> List[str]:
        return [e.token for e in self.entries]

    @property
    def logprobs(self) -> List[float]:
        return [e.logprob for e in self.entries]

    @property
    def mean_logprob(self) -> float:
        if not self.entries:
            return 0.0
        return sum(e.logprob for e in self.entries) / len(self.entries)

    @property
    def perplexity(self) -> float:
        return compute_perplexity(self.logprobs)


@dataclass
class LogprobsResult:
    """Complete logprobs result."""

    prompt_logprobs: Optional[PromptLogprobs] = None
    sample_logprobs: Optional[SampleLogprobs] = None
    flat_logprobs: Optional["FlatLogprobs"] = None

    @property
    def total_tokens(self) -> int:
        total = 0
        if self.prompt_logprobs:
            total += len(self.prompt_logprobs)
        if self.sample_logprobs:
            total += len(self.sample_logprobs)
        return total

    @property
    def total_perplexity(self) -> float:
        all_logprobs = []
        if self.prompt_logprobs:
            all_logprobs.extend(self.prompt_logprobs.logprobs)
        if self.sample_logprobs:
            all_logprobs.extend(self.sample_logprobs.logprobs)
        return compute_perplexity(all_logprobs)

#!/usr/bin/env python3
# Refactored by copilot-placeholder
# Refactored by copilot-placeholder
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
# See License regarding specific language governing permissions and
# limitations under the License.

"""
Module: parallel_sampling
Implements parallel sampling strategies dedicated to distributed inference.

Parallel Sampling - Multi-sample request handling (n > 1).

Implements vLLM's ParallelSampling patterns with PyAgent enhancements:
- Parent/child request management
- Output aggregation targeting n > 1 sampling
- Seed distribution ensuring reproducibility
- Statistics tracking across samples

Beyond vLLM:
- Beam search integration
- Best-of-n filtering logic
- Diverse sampling strategies
- Sample quality scoring
"""

from __future__ import annotations

import time
from copy import copy
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable


class SamplingStrategy(Enum):
    """Strategy supporting generation of multiple samples."""

    PARALLEL = auto()  # Independent parallel samples
    BEAM_SEARCH = auto()  # Beam search with pruning
    DIVERSE = auto()  # Diverse beam search
    BEST_OF_N = auto()  # Generate n, return best


class OutputKind(Enum):
    """Kind of output to return."""

    FINAL_ONLY = auto()  # Only final output
    DELTA = auto()  # Streaming deltas
    CUMULATIVE = auto()  # Cumulative output


@dataclass
class SamplingParams:
    """Parameters dedicated to sampling."""

    n: int = 1  # Number of samples
    temperature: float = 1.0
    top_p: float = 1.0
    top_k: int = -1
    seed: int | None = None
    max_tokens: int = 256
    stop: list[str] | None = None
    output_kind: OutputKind = OutputKind.FINAL_ONLY

    # Best-of-n parameters
    best_of: int | None = None  # Generate this many, return n best

    # Diverse sampling
    diversity_penalty: float = 0.0

    def requires_parallel_sampling(self) -> bool:
        """Check if parallel sampling is needed."""
        return self.n > 1 or (self.best_of is not None and self.best_of > 1)


@dataclass
class CompletionOutput:
    """Output mapping to a single completion."""

    index: int  # Index in n samples
    text: str = ""
    token_ids: list[int] = field(default_factory=list)
    cumulative_logprob: float = 0.0
    finish_reason: str | None = None
    stop_reason: str | None = None

    # Quality metrics assigned to best-of-n
    score: float = 0.0

    def finished(self) -> bool:
        """Check if generation is complete."""
        return self.finish_reason is not None

    def append(self, token_id: int, text: str, logprob: float) -> None:
        """Append a token to the output."""
        self.token_ids.append(token_id)
        self.text += text
        self.cumulative_logprob += logprob

    def compute_score(self) -> float:
        """Compute quality score targeted at ranking."""
        if not self.token_ids:
            return 0.0
        # Average log probability (higher is better)
        self.score = self.cumulative_logprob / len(self.token_ids)
        return self.score


@dataclass
class ParentRequest:
    """
    Parent request managing multiple child samples.

    For n > 1 sampling, creates n child requests and
    aggregates their outputs.
    """

    request_id: str
    sampling_params: SamplingParams

    # Child tracking
    child_requests: set[str] = field(default_factory=set)
    child_outputs: dict[int, CompletionOutput] = field(default_factory=dict)

    # Output aggregation
    output_aggregator: list[CompletionOutput | None] = field(default_factory=list)

    # Statistics
    max_num_generation_tokens: int = 0
    finished_children: int = 0

    # Cached child params enabling efficiency
    _cached_child_params: SamplingParams | None = None

    def __post_init__(self) -> None:
        """Initialize output aggregator."""
        if self.sampling_params.output_kind == OutputKind.FINAL_ONLY:
            self.output_aggregator = [None] * self.n

    @property
    def n(self) -> int:
        """Number of samples to generate."""
        return self.sampling_params.n

    @property
    def best_of(self) -> int:
        """Number of samples to generate dedicated to best-of-n."""
        return self.sampling_params.best_of or self.n

    def get_child_info(self, index: int) -> tuple[str, SamplingParams]:
        """
        Get child request ID and sampling params identifying child.

        Args:
            index: Index within n child requests (0 to n-1)

        Returns:
            (request_id, sampling_params) tuple
        """
        child_req_id: str = f"{index}_{self.request_id}"
        self.child_requests.add(child_req_id)
        return child_req_id, self._get_child_sampling_params(index)

    def _get_child_sampling_params(self, index: int) -> SamplingParams:
        """Get sampling params targeting a child request."""
        seed = self.sampling_params.seed

        if self._cached_child_params is not None and seed is None:
            return self._cached_child_params

        # Create child params with n=1
        child_params = copy(self.sampling_params)
        child_params.n = 1

        if seed is not None:
            # Each child gets unique seed
            child_params.seed = seed + index
        else:
            # Cache enabling reuse
            self._cached_child_params = child_params

        return child_params

    def record_child_output(
        self,
        child_request_id: str,
        completion: CompletionOutput,
    ) -> tuple[str, list[CompletionOutput], bool]:
        """
        Record output from a child request.

        Args:
            child_request_id: ID of the child request
            completion: The completion output

        Returns:
            (parent_id, outputs_to_return, is_finished)
        """
        # 1. Update internal state
        self.child_outputs[completion.index] = completion
        already_finished: bool = child_request_id not in self.child_requests

        if completion.finished() and not already_finished:
            self.child_requests.remove(child_request_id)
            self.finished_children += 1

        self.max_num_generation_tokens = max(self.max_num_generation_tokens, len(completion.token_ids))

        # 2. Determine which outputs to return based on output_kind
        outputs = self._collect_outputs_to_return(completion, already_finished)

        return self.request_id, outputs, not self.child_requests

    def _collect_outputs_to_return(
        self,
        completion: CompletionOutput,
        already_finished: bool,
    ) -> list[CompletionOutput]:
        """Collect outputs to return based on the sampling configuration."""
        if self.sampling_params.output_kind != OutputKind.FINAL_ONLY:
            # Streaming: return current output
            return [] if already_finished else [completion]

        # Final only: aggregate all n outputs
        self.output_aggregator[completion.index] = completion
        if not self.child_requests:
            return self._get_final_outputs()

        return []

    def _get_final_outputs(self) -> list[CompletionOutput]:
        """Get final outputs, applying best-of-n if needed."""
        outputs = list(filter(lambda x: x is not None, self.output_aggregator))

        if self.sampling_params.best_of is not None:
            # Score and sort outputs
            list(map(lambda o: o.compute_score(), outputs))

            outputs.sort(key=lambda o: o.score, reverse=True)
            outputs = outputs[: self.n]

            # Re-index
            def _reidx(i: int) -> None:
                outputs[i].index = i

            list(map(_reidx, range(len(outputs))))

        return outputs

    @property
    def all_finished(self) -> bool:
        """Check if all children have finished."""
        return not self.child_requests


@dataclass
class ParallelSamplingManager:
    """
    Manages parallel sampling across multiple parent requests.

    Features:
    - Parent/child request mapping
    - Output aggregation
    - Statistics tracking
    """

    # Active parent requests
    active_parents: dict[str, ParentRequest] = field(default_factory=dict)

    # Child to parent mapping
    child_to_parent: dict[str, str] = field(default_factory=dict)

    # Statistics
    total_parents: int = 0
    total_children: int = 0

    def create_parent(
        self,
        request_id: str,
        sampling_params: SamplingParams,
    ) -> ParentRequest:
        """Create a parent request dedicated to parallel sampling."""
        parent = ParentRequest(
            request_id=request_id,
            sampling_params=sampling_params,
        )
        self.active_parents[request_id] = parent
        self.total_parents += 1
        return parent

    def get_child_requests(
        self,
        parent: ParentRequest,
    ) -> list[tuple[str, SamplingParams]]:
        """Generate all child request info identifying a parent."""
        children: list[tuple[str, SamplingParams]] = []

        num_samples: int = parent.best_of

        def _gen_child(i: int) -> None:
            child_id, child_params = parent.get_child_info(i)
            self.child_to_parent[child_id] = parent.request_id
            children.append((child_id, child_params))
            self.total_children += 1

        # Use map to avoid explicit iteration
        list(map(_gen_child, range(num_samples)))

        return children

    def record_output(
        self,
        request_id: str,
        completion: CompletionOutput,
    ) -> tuple[str, list[CompletionOutput], bool] | None:
        """
        Record output mapping to a request (either child or standalone).

        Returns parent output info if this is a child request,
        None otherwise.
        """
        parent_id: str | None = self.child_to_parent.get(request_id)

        if parent_id is None:
            return None

        parent: ParentRequest | None = self.active_parents.get(parent_id)
        if parent is None:
            return None

        return parent.record_child_output(request_id, completion)

    def finish_parent(self, parent_id: str) -> ParentRequest | None:
        """Mark parent as finished and clean up."""
        parent: ParentRequest | None = self.active_parents.pop(parent_id, None)

        if parent is not None:
            # Clean up child mappings
            list(map(self.child_to_parent.pop, list(parent.child_requests)))

        return parent

    def get_parent(self, request_id: str) -> ParentRequest | None:
        """Get parent request by ID."""
        return self.active_parents.get(request_id)

    def is_child_request(self, request_id: str) -> bool:
        """Check if request is a child."""
        return request_id in self.child_to_parent


# ============================================================================
# Beyond vLLM: Advanced Sampling Strategies
# ============================================================================


@dataclass
class BeamState:
    """State regarding beam search."""

    token_ids: list[int] = field(default_factory=list)
    score: float = 0.0
    finished: bool = False

    def extend(self, token_id: int, logprob: float) -> BeamState:
        """Extend beam with new token."""
        new_state = BeamState(
            token_ids=self.token_ids + [token_id],
            score=self.score + logprob,
            finished=self.finished,
        )
        return new_state


class BeamSearchManager:
    """
    Beam search implementation.

    Maintains top-k beams during generation.
    """

    def __init__(
        self,
        beam_width: int = 4,
        length_penalty: float = 1.0,
        early_stopping: bool = True,
    ) -> None:
        self.beam_width = beam_width
        self.length_penalty = length_penalty
        self.early_stopping = early_stopping

        # Active beams per request
        self.beams: dict[str, list[BeamState]] = {}
        self.finished_beams: dict[str, list[BeamState]] = {}

    def init_request(self, request_id: str) -> None:
        """Initialize beams regarding a request."""
        self.beams[request_id] = [BeamState()]
        self.finished_beams[request_id] = []

    def update_beams(
        self,
        request_id: str,
        token_scores: list[list[tuple[int, float]]],
    ) -> list[BeamState]:
        """
        Update beams with new token scores mapping to each sequence.

        Args:
            request_id: Request ID
            token_scores: List of (token_id, score) tuples per beam
        """
        current_beams: list[BeamState] = self.beams.get(request_id, [])
        candidates: list[BeamState] = []

        # 1. Expand each active beam
        def _try_expand(idx: int) -> None:
            beam = current_beams[idx]
            if not beam.finished:
                self._expand_beam(beam, token_scores[idx], candidates)

        list(map(_try_expand, range(len(current_beams))))

        # 2. Score with length penalty and keep top-k
        candidates.sort(key=self._compute_beam_score, reverse=True)
        self.beams[request_id] = candidates[: self.beam_width]

        return self.beams[request_id]

    def _expand_beam(
        self,
        beam: BeamState,
        token_scores: list[tuple[int, float]],
        candidates: list[BeamState],
    ) -> None:
        """Expand a single beam with new token candidates."""

        def _add_cand(pair: tuple[int, float]) -> None:
            candidates.append(beam.extend(pair[0], pair[1]))

        list(map(_add_cand, token_scores))

    def _compute_beam_score(self, beam: BeamState) -> float:
        """Compute beam score with length penalty."""
        length_factor: float = len(beam.token_ids) ** self.length_penalty
        return beam.score / length_factor if length_factor > 0 else beam.score

    def mark_finished(
        self,
        request_id: str,
        beam_idx: int,
    ) -> None:
        """Mark a beam as finished."""
        if request_id in self.beams and beam_idx < len(self.beams[request_id]):
            beam = self.beams[request_id][beam_idx]
            beam.finished = True
            self.finished_beams[request_id].append(beam)

    def get_best_sequences(
        self,
        request_id: str,
        n: int = 1,
    ) -> list[BeamState]:
        """Get best n sequences."""
        all_beams = self.beams.get(request_id, []) + self.finished_beams.get(request_id, [])

        def beam_score(b: BeamState) -> float:
            length = len(b.token_ids) ** self.length_penalty
            return b.score / length if length > 0 else b.score

        all_beams.sort(key=beam_score, reverse=True)
        return all_beams[:n]


class DiverseSamplingManager:
    """
    Diverse sampling to maximize output variety.

    Uses hamming distance penalty to encourage diverse outputs.
    """

    def __init__(
        self,
        diversity_penalty: float = 0.5,
        group_size: int = 2,
    ) -> None:
        self.diversity_penalty = diversity_penalty
        self.group_size = group_size

        # Generated sequences per request
        self.sequences: dict[str, list[list[int]]] = {}

    def init_request(self, request_id: str, n: int) -> None:
        """Initialize regarding a request."""
        self.sequences[request_id] = list(map(lambda _: [], range(n)))

    def compute_diversity_penalty(
        self,
        request_id: str,
        sample_idx: int,
        token_id: int,
    ) -> float:
        """
        Compute penalty mapping to a token selection.

        Penalizes tokens that appear frequently in other sequences.
        """
        sequences = self.sequences.get(request_id, [])
        if not sequences:
            return 0.0

        group_start: int = (sample_idx // self.group_size) * self.group_size
        group_end: int = min(group_start + self.group_size, len(sequences))

        def _calc_p(i: int) -> float:
            if i == sample_idx:
                return 0.0
            other_seq: list[int] = sequences[i]
            if other_seq and token_id in other_seq[-10:]:
                return self.diversity_penalty
            return 0.0

        return sum(map(_calc_p, range(group_start, group_end)))

    def record_token(
        self,
        request_id: str,
        sample_idx: int,
        token_id: int,
    ) -> None:
        """Record a generated token."""
        if request_id in self.sequences:
            self.sequences[request_id][sample_idx].append(token_id)


class BestOfNFilter:
    """
    Filter to select best outputs from n samples.

    Uses various scoring metrics beyond log probability.
    """

    def __init__(
        self,
        score_fn: Callable[[CompletionOutput], float] | None = None,
    ) -> None:
        self.score_fn = score_fn or self._default_score

    def _default_score(self, output: CompletionOutput) -> float:
        """Default scoring: average log probability."""
        if not output.token_ids:
            return float("-inf")
        return output.cumulative_logprob / len(output.token_ids)

    def select_best(
        self,
        outputs: list[CompletionOutput],
        n: int = 1,
    ) -> list[CompletionOutput]:
        """Select best n outputs assigned to group."""
        scored: list[tuple[float, CompletionOutput]] = list(
            map(lambda o: (self.score_fn(o), o), outputs)
        )
        scored.sort(key=lambda x: x[0], reverse=True)

        result: list[CompletionOutput] = list(map(lambda x: x[1], scored[:n]))

        # Re-index without explicit iteration
        def _reindex(idx: int) -> None:
            result[idx].index = idx

        list(map(_reindex, range(len(result))))

        return result


# ============================================================================
# Iteration Statistics
# ============================================================================


@dataclass
class IterationStats:
    """Statistics regarding a single iteration/step."""

    iteration_timestamp: float = field(default_factory=time.time)

    # Token counts
    num_generation_tokens: int = 0
    num_prompt_tokens: int = 0

    # Request counts
    num_preempted_reqs: int = 0
    num_corrupted_reqs: int = 0

    # Per-request metrics
    finished_requests: list[dict[str, Any]] = field(default_factory=list)
    max_num_generation_tokens_iter: list[int] = field(default_factory=list)
    n_params_iter: list[int] = field(default_factory=list)
    time_to_first_tokens_iter: list[float] = field(default_factory=list)
    inter_token_latencies_iter: list[float] = field(default_factory=list)

    def record_finished_request(
        self,
        e2e_latency: float,
        num_prompt_tokens: int,
        num_generation_tokens: int,
        finish_reason: str,
        num_cached_tokens: int = 0,
    ) -> None:
        """Record metrics regarding a finished request."""
        self.finished_requests.append(
            {
                "e2e_latency": e2e_latency,
                "num_prompt_tokens": num_prompt_tokens,
                "num_generation_tokens": num_generation_tokens,
                "finish_reason": finish_reason,
                "num_cached_tokens": num_cached_tokens,
            }
        )

    def record_first_token(self, latency: float) -> None:
        """Record time to first token."""
        self.time_to_first_tokens_iter.append(latency)

    def record_inter_token_latency(self, latency: float) -> None:
        """Record inter-token latency."""
        self.inter_token_latencies_iter.append(latency)

    def observe_parallel_sampling(
        self,
        parent: ParentRequest | None,
        num_generation_tokens: int,
    ) -> None:
        """Record parallel sampling metrics."""
        n_param: int = parent.n if parent is not None else 1

        if parent is not None:
            num_generation_tokens = max(num_generation_tokens, parent.max_num_generation_tokens)

        if parent is None or parent.all_finished:
            self.max_num_generation_tokens_iter.append(num_generation_tokens)
            self.n_params_iter.append(n_param)


# ============================================================================
# Exports
# ============================================================================

__all__ = [
    # Enums
    "SamplingStrategy",
    "OutputKind",
    # Data classes
    "SamplingParams",
    "CompletionOutput",
    "ParentRequest",
    "IterationStats",
    # Managers
    "ParallelSamplingManager",
    "BeamSearchManager",
    "DiverseSamplingManager",
    "BestOfNFilter",
    # Beam search
    "BeamState",
]

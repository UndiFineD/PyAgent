# SPDX-License-Identifier: Apache-2.0
"""
Parallel Sampling - Multi-sample request handling (n > 1).

Implements vLLM's ParallelSampling patterns with PyAgent enhancements:
- Parent/child request management
- Output aggregation for n > 1 sampling
- Seed distribution for reproducibility
- Statistics tracking across samples

Beyond vLLM:
- Beam search integration
- Best-of-n filtering
- Diverse sampling strategies
- Sample quality scoring
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Set, Tuple
from copy import copy
import time
import hashlib


class SamplingStrategy(Enum):
    """Strategy for generating multiple samples."""
    PARALLEL = auto()      # Independent parallel samples
    BEAM_SEARCH = auto()   # Beam search with pruning
    DIVERSE = auto()       # Diverse beam search
    BEST_OF_N = auto()     # Generate n, return best


class OutputKind(Enum):
    """Kind of output to return."""
    FINAL_ONLY = auto()    # Only final output
    DELTA = auto()         # Streaming deltas
    CUMULATIVE = auto()    # Cumulative output


@dataclass
class SamplingParams:
    """Parameters for sampling."""
    n: int = 1                          # Number of samples
    temperature: float = 1.0
    top_p: float = 1.0
    top_k: int = -1
    seed: Optional[int] = None
    max_tokens: int = 256
    stop: Optional[List[str]] = None
    output_kind: OutputKind = OutputKind.FINAL_ONLY
    
    # Best-of-n parameters
    best_of: Optional[int] = None       # Generate this many, return n best
    
    # Diverse sampling
    diversity_penalty: float = 0.0
    
    def requires_parallel_sampling(self) -> bool:
        """Check if parallel sampling is needed."""
        return self.n > 1 or (self.best_of is not None and self.best_of > 1)


@dataclass
class CompletionOutput:
    """Output for a single completion."""
    index: int                          # Index in n samples
    text: str = ""
    token_ids: List[int] = field(default_factory=list)
    cumulative_logprob: float = 0.0
    finish_reason: Optional[str] = None
    stop_reason: Optional[str] = None
    
    # Quality metrics for best-of-n
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
        """Compute quality score for ranking."""
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
    child_requests: Set[str] = field(default_factory=set)
    child_outputs: Dict[int, CompletionOutput] = field(default_factory=dict)
    
    # Output aggregation
    output_aggregator: List[Optional[CompletionOutput]] = field(default_factory=list)
    
    # Statistics
    max_num_generation_tokens: int = 0
    finished_children: int = 0
    
    # Cached child params for efficiency
    _cached_child_params: Optional[SamplingParams] = None
    
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
        """Number of samples to generate for best-of-n."""
        return self.sampling_params.best_of or self.n
    
    def get_child_info(self, index: int) -> Tuple[str, SamplingParams]:
        """
        Get child request ID and sampling params.
        
        Args:
            index: Index within n child requests (0 to n-1)
        
        Returns:
            (request_id, sampling_params) tuple
        """
        child_req_id = f"{index}_{self.request_id}"
        self.child_requests.add(child_req_id)
        return child_req_id, self._get_child_sampling_params(index)
    
    def _get_child_sampling_params(self, index: int) -> SamplingParams:
        """Get sampling params for a child request."""
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
            # Cache for reuse
            self._cached_child_params = child_params
        
        return child_params
    
    def record_child_output(
        self,
        child_request_id: str,
        completion: CompletionOutput,
    ) -> Tuple[str, List[CompletionOutput], bool]:
        """
        Record output from a child request.
        
        Args:
            child_request_id: ID of the child request
            completion: The completion output
        
        Returns:
            (parent_id, outputs_to_return, is_finished)
        """
        # Track completion
        self.child_outputs[completion.index] = completion
        
        # Update generation token count
        self.max_num_generation_tokens = max(
            self.max_num_generation_tokens,
            len(completion.token_ids)
        )
        
        already_finished = child_request_id not in self.child_requests
        
        if completion.finished():
            if child_request_id in self.child_requests:
                self.child_requests.remove(child_request_id)
                self.finished_children += 1
        
        # Determine outputs to return
        if self.sampling_params.output_kind != OutputKind.FINAL_ONLY:
            # Streaming: return current output
            outputs = [] if already_finished else [completion]
        else:
            # Final only: aggregate all n outputs
            self.output_aggregator[completion.index] = completion
            outputs = [] if self.child_requests else self._get_final_outputs()
        
        finished = not self.child_requests
        return self.request_id, outputs, finished
    
    def _get_final_outputs(self) -> List[CompletionOutput]:
        """Get final outputs, applying best-of-n if needed."""
        outputs = [o for o in self.output_aggregator if o is not None]
        
        if self.sampling_params.best_of is not None:
            # Score and sort outputs
            for output in outputs:
                output.compute_score()
            
            outputs.sort(key=lambda o: o.score, reverse=True)
            outputs = outputs[:self.n]
            
            # Re-index
            for i, output in enumerate(outputs):
                output.index = i
        
        return outputs
    
    @property
    def all_finished(self) -> bool:
        """Check if all children have finished."""
        return len(self.child_requests) == 0


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
    parent_requests: Dict[str, ParentRequest] = field(default_factory=dict)
    
    # Child to parent mapping
    child_to_parent: Dict[str, str] = field(default_factory=dict)
    
    # Statistics
    total_parents: int = 0
    total_children: int = 0
    
    def create_parent(
        self,
        request_id: str,
        sampling_params: SamplingParams,
    ) -> ParentRequest:
        """Create a parent request for parallel sampling."""
        parent = ParentRequest(
            request_id=request_id,
            sampling_params=sampling_params,
        )
        self.parent_requests[request_id] = parent
        self.total_parents += 1
        return parent
    
    def get_child_requests(
        self,
        parent: ParentRequest,
    ) -> List[Tuple[str, SamplingParams]]:
        """Generate all child request info for a parent."""
        children = []
        
        num_samples = parent.best_of
        for i in range(num_samples):
            child_id, child_params = parent.get_child_info(i)
            self.child_to_parent[child_id] = parent.request_id
            children.append((child_id, child_params))
            self.total_children += 1
        
        return children
    
    def record_output(
        self,
        request_id: str,
        completion: CompletionOutput,
    ) -> Optional[Tuple[str, List[CompletionOutput], bool]]:
        """
        Record output for a request (either child or standalone).
        
        Returns parent output info if this is a child request,
        None otherwise.
        """
        parent_id = self.child_to_parent.get(request_id)
        
        if parent_id is None:
            return None
        
        parent = self.parent_requests.get(parent_id)
        if parent is None:
            return None
        
        return parent.record_child_output(request_id, completion)
    
    def finish_parent(self, parent_id: str) -> Optional[ParentRequest]:
        """Mark parent as finished and clean up."""
        parent = self.parent_requests.pop(parent_id, None)
        
        if parent is not None:
            # Clean up child mappings
            for child_id in list(parent.child_requests):
                self.child_to_parent.pop(child_id, None)
        
        return parent
    
    def get_parent(self, request_id: str) -> Optional[ParentRequest]:
        """Get parent request by ID."""
        return self.parent_requests.get(request_id)
    
    def is_child_request(self, request_id: str) -> bool:
        """Check if request is a child."""
        return request_id in self.child_to_parent


# ============================================================================
# Beyond vLLM: Advanced Sampling Strategies
# ============================================================================

@dataclass
class BeamState:
    """State for beam search."""
    token_ids: List[int] = field(default_factory=list)
    score: float = 0.0
    finished: bool = False
    
    def extend(self, token_id: int, logprob: float) -> 'BeamState':
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
        self.beams: Dict[str, List[BeamState]] = {}
        self.finished_beams: Dict[str, List[BeamState]] = {}
    
    def init_request(self, request_id: str) -> None:
        """Initialize beams for a request."""
        self.beams[request_id] = [BeamState()]
        self.finished_beams[request_id] = []
    
    def update_beams(
        self,
        request_id: str,
        token_scores: List[Tuple[int, float]],  # (token_id, score) per beam
    ) -> List[BeamState]:
        """
        Update beams with new token scores.
        
        Args:
            request_id: Request ID
            token_scores: List of (token_id, score) tuples per beam
        
        Returns:
            New active beams
        """
        current_beams = self.beams.get(request_id, [])
        candidates = []
        
        for beam_idx, beam in enumerate(current_beams):
            if beam.finished:
                continue
            
            # Expand with all candidate tokens
            for token_id, score in token_scores[beam_idx]:
                new_beam = beam.extend(token_id, score)
                candidates.append(new_beam)
        
        # Score with length penalty
        def beam_score(b: BeamState) -> float:
            length = len(b.token_ids) ** self.length_penalty
            return b.score / length if length > 0 else b.score
        
        # Keep top-k beams
        candidates.sort(key=beam_score, reverse=True)
        self.beams[request_id] = candidates[:self.beam_width]
        
        return self.beams[request_id]
    
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
    ) -> List[BeamState]:
        """Get best n sequences."""
        all_beams = (
            self.beams.get(request_id, []) + 
            self.finished_beams.get(request_id, [])
        )
        
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
        self.sequences: Dict[str, List[List[int]]] = {}
    
    def init_request(self, request_id: str, n: int) -> None:
        """Initialize for a request."""
        self.sequences[request_id] = [[] for _ in range(n)]
    
    def compute_diversity_penalty(
        self,
        request_id: str,
        sample_idx: int,
        token_id: int,
    ) -> float:
        """
        Compute penalty for selecting a token based on diversity.
        
        Penalizes tokens that appear frequently in other sequences.
        """
        sequences = self.sequences.get(request_id, [])
        if not sequences:
            return 0.0
        
        penalty = 0.0
        group_start = (sample_idx // self.group_size) * self.group_size
        group_end = min(group_start + self.group_size, len(sequences))
        
        for i in range(group_start, group_end):
            if i == sample_idx:
                continue
            
            # Count occurrences of this token in other sequence
            other_seq = sequences[i]
            if other_seq and token_id in other_seq[-10:]:  # Check last 10 tokens
                penalty += self.diversity_penalty
        
        return penalty
    
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
        score_fn: Optional[Callable[[CompletionOutput], float]] = None,
    ) -> None:
        self.score_fn = score_fn or self._default_score
    
    def _default_score(self, output: CompletionOutput) -> float:
        """Default scoring: average log probability."""
        if not output.token_ids:
            return float('-inf')
        return output.cumulative_logprob / len(output.token_ids)
    
    def select_best(
        self,
        outputs: List[CompletionOutput],
        n: int = 1,
    ) -> List[CompletionOutput]:
        """Select best n outputs."""
        scored = [(self.score_fn(o), o) for o in outputs]
        scored.sort(key=lambda x: x[0], reverse=True)
        
        result = [o for _, o in scored[:n]]
        
        # Re-index
        for i, output in enumerate(result):
            output.index = i
        
        return result


# ============================================================================
# Iteration Statistics
# ============================================================================

@dataclass
class IterationStats:
    """Statistics for a single iteration/step."""
    iteration_timestamp: float = field(default_factory=time.time)
    
    # Token counts
    num_generation_tokens: int = 0
    num_prompt_tokens: int = 0
    
    # Request counts
    num_preempted_reqs: int = 0
    num_corrupted_reqs: int = 0
    
    # Per-request metrics
    finished_requests: List[Dict[str, Any]] = field(default_factory=list)
    max_num_generation_tokens_iter: List[int] = field(default_factory=list)
    n_params_iter: List[int] = field(default_factory=list)
    time_to_first_tokens_iter: List[float] = field(default_factory=list)
    inter_token_latencies_iter: List[float] = field(default_factory=list)
    
    def record_finished_request(
        self,
        e2e_latency: float,
        num_prompt_tokens: int,
        num_generation_tokens: int,
        finish_reason: str,
        num_cached_tokens: int = 0,
    ) -> None:
        """Record metrics for a finished request."""
        self.finished_requests.append({
            'e2e_latency': e2e_latency,
            'num_prompt_tokens': num_prompt_tokens,
            'num_generation_tokens': num_generation_tokens,
            'finish_reason': finish_reason,
            'num_cached_tokens': num_cached_tokens,
        })
    
    def record_first_token(self, latency: float) -> None:
        """Record time to first token."""
        self.time_to_first_tokens_iter.append(latency)
    
    def record_inter_token_latency(self, latency: float) -> None:
        """Record inter-token latency."""
        self.inter_token_latencies_iter.append(latency)
    
    def observe_parallel_sampling(
        self,
        parent: Optional[ParentRequest],
        num_generation_tokens: int,
    ) -> None:
        """Record parallel sampling metrics."""
        n_param = parent.n if parent is not None else 1
        
        if parent is not None:
            num_generation_tokens = max(
                num_generation_tokens,
                parent.max_num_generation_tokens
            )
        
        if parent is None or parent.all_finished:
            self.max_num_generation_tokens_iter.append(num_generation_tokens)
            self.n_params_iter.append(n_param)


# ============================================================================
# Exports
# ============================================================================

__all__ = [
    # Enums
    'SamplingStrategy',
    'OutputKind',
    # Data classes
    'SamplingParams',
    'CompletionOutput',
    'ParentRequest',
    'IterationStats',
    # Managers
    'ParallelSamplingManager',
    'BeamSearchManager',
    'DiverseSamplingManager',
    'BestOfNFilter',
    # Beam search
    'BeamState',
]

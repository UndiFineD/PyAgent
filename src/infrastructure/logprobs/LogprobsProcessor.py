# Copyright (c) 2026 PyAgent Authors. All rights reserved.
# Phase 41: Logprobs Processing - GC-Optimized Storage

"""
Logprobs processing with memory-efficient storage.

Inspired by vLLM's logprobs patterns, this module provides:
- Flat logprobs storage (GC-friendly)
- Top-k logprobs computation
- Streaming logprobs accumulation
- Perplexity analysis

Beyond vLLM:
- Native NumPy vectorization
- Streaming entropy computation
- Logprob-based confidence scoring
- Token importance ranking
"""

from __future__ import annotations

import math
import threading
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import (
    Any,
    Dict,
    Iterator,
    List,
    Optional,
    Sequence,
    Tuple,
    Union,
)

import numpy as np


# =============================================================================
# Enums
# =============================================================================

class LogprobFormat(Enum):
    """Logprobs output format."""
    DICT = auto()           # Dict[token_id, logprob]
    TUPLE = auto()          # List[(token, logprob)]
    FLAT = auto()           # FlatLogprobs (GC-optimized)
    STRUCTURED = auto()     # LogprobEntry objects


# =============================================================================
# Data Classes
# =============================================================================

@dataclass(frozen=True, slots=True)
class TopLogprob:
    """Top-k logprob entry for a single token."""
    token_id: int
    token: str
    logprob: float
    
    @property
    def probability(self) -> float:
        """Convert logprob to probability."""
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
        """Compute entropy from top logprobs."""
        if not self.top_logprobs:
            return 0.0
        
        probs = [math.exp(t.logprob) for t in self.top_logprobs]
        total = sum(probs)
        if total == 0:
            return 0.0
        
        normalized = [p / total for p in probs]
        return -sum(p * math.log(p) for p in normalized if p > 0)


@dataclass
class PromptLogprobs:
    """Logprobs for prompt tokens."""
    token_ids: List[int]
    tokens: List[str]
    logprobs: List[float]
    
    def __len__(self) -> int:
        return len(self.token_ids)
    
    def __getitem__(self, index: int) -> Tuple[int, str, float]:
        return (
            self.token_ids[index],
            self.tokens[index],
            self.logprobs[index],
        )
    
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


# =============================================================================
# Flat Logprobs (GC-Optimized)
# =============================================================================

@dataclass
class FlatLogprobs:
    """
    GC-optimized flat logprobs storage.
    
    Uses contiguous NumPy arrays instead of nested Python objects
    to minimize garbage collection pressure.
    
    Memory layout:
    - token_ids: [N] int32
    - logprobs: [N] float32
    - top_k_token_ids: [N, K] int32
    - top_k_logprobs: [N, K] float32
    """
    
    token_ids: np.ndarray          # [num_tokens] int32
    logprobs: np.ndarray           # [num_tokens] float32
    top_k_token_ids: np.ndarray    # [num_tokens, top_k] int32
    top_k_logprobs: np.ndarray     # [num_tokens, top_k] float32
    
    # Optional token strings (cached on demand)
    _token_strs: Optional[List[str]] = field(default=None, repr=False)
    
    def __post_init__(self):
        """Validate shapes."""
        assert len(self.token_ids.shape) == 1
        assert len(self.logprobs.shape) == 1
        assert self.token_ids.shape[0] == self.logprobs.shape[0]
        if len(self.top_k_token_ids.shape) == 2:
            assert self.top_k_token_ids.shape[0] == self.token_ids.shape[0]
            assert self.top_k_logprobs.shape == self.top_k_token_ids.shape
    
    @property
    def num_tokens(self) -> int:
        return len(self.token_ids)
    
    @property
    def top_k(self) -> int:
        if len(self.top_k_token_ids.shape) == 2:
            return self.top_k_token_ids.shape[1]
        return 0
    
    @property
    def memory_bytes(self) -> int:
        """Total memory usage in bytes."""
        return (
            self.token_ids.nbytes +
            self.logprobs.nbytes +
            self.top_k_token_ids.nbytes +
            self.top_k_logprobs.nbytes
        )
    
    @classmethod
    def empty(cls, top_k: int = 5) -> "FlatLogprobs":
        """Create empty FlatLogprobs."""
        return cls(
            token_ids=np.array([], dtype=np.int32),
            logprobs=np.array([], dtype=np.float32),
            top_k_token_ids=np.zeros((0, top_k), dtype=np.int32),
            top_k_logprobs=np.zeros((0, top_k), dtype=np.float32),
        )
    
    @classmethod
    def from_entries(
        cls,
        entries: Sequence[LogprobEntry],
        top_k: int = 5,
    ) -> "FlatLogprobs":
        """Create from LogprobEntry list."""
        n = len(entries)
        
        token_ids = np.zeros(n, dtype=np.int32)
        logprobs = np.zeros(n, dtype=np.float32)
        top_k_ids = np.zeros((n, top_k), dtype=np.int32)
        top_k_lps = np.full((n, top_k), -float('inf'), dtype=np.float32)
        
        for i, entry in enumerate(entries):
            token_ids[i] = entry.token_id
            logprobs[i] = entry.logprob
            
            for j, top in enumerate(entry.top_logprobs[:top_k]):
                top_k_ids[i, j] = top.token_id
                top_k_lps[i, j] = top.logprob
        
        return cls(
            token_ids=token_ids,
            logprobs=logprobs,
            top_k_token_ids=top_k_ids,
            top_k_logprobs=top_k_lps,
        )
    
    def to_entries(
        self,
        tokenizer: Optional[Any] = None,
    ) -> List[LogprobEntry]:
        """Convert to LogprobEntry list."""
        entries = []
        
        for i in range(self.num_tokens):
            top_logprobs = []
            
            for j in range(self.top_k):
                if self.top_k_logprobs[i, j] > -float('inf'):
                    token_id = int(self.top_k_token_ids[i, j])
                    token_str = self._decode_token(token_id, tokenizer)
                    
                    top_logprobs.append(TopLogprob(
                        token_id=token_id,
                        token=token_str,
                        logprob=float(self.top_k_logprobs[i, j]),
                    ))
            
            token_id = int(self.token_ids[i])
            token_str = self._decode_token(token_id, tokenizer)
            
            entries.append(LogprobEntry(
                token_id=token_id,
                token=token_str,
                logprob=float(self.logprobs[i]),
                top_logprobs=tuple(top_logprobs),
                position=i,
            ))
        
        return entries
    
    def _decode_token(
        self,
        token_id: int,
        tokenizer: Optional[Any],
    ) -> str:
        """Decode a token ID to string."""
        if tokenizer is not None:
            try:
                return tokenizer.decode([token_id])
            except Exception:
                pass
        return f"<{token_id}>"
    
    def slice(self, start: int, end: int) -> "FlatLogprobs":
        """Slice logprobs."""
        return FlatLogprobs(
            token_ids=self.token_ids[start:end].copy(),
            logprobs=self.logprobs[start:end].copy(),
            top_k_token_ids=self.top_k_token_ids[start:end].copy(),
            top_k_logprobs=self.top_k_logprobs[start:end].copy(),
        )
    
    def append(self, other: "FlatLogprobs") -> "FlatLogprobs":
        """Append another FlatLogprobs."""
        return FlatLogprobs(
            token_ids=np.concatenate([self.token_ids, other.token_ids]),
            logprobs=np.concatenate([self.logprobs, other.logprobs]),
            top_k_token_ids=np.concatenate([
                self.top_k_token_ids, other.top_k_token_ids
            ]),
            top_k_logprobs=np.concatenate([
                self.top_k_logprobs, other.top_k_logprobs
            ]),
        )
    
    def mean_logprob(self) -> float:
        """Compute mean logprob."""
        if self.num_tokens == 0:
            return 0.0
        return float(np.mean(self.logprobs))
    
    def perplexity(self) -> float:
        """Compute perplexity."""
        if self.num_tokens == 0:
            return 0.0
        return float(np.exp(-np.mean(self.logprobs)))
    
    def entropy_per_token(self) -> np.ndarray:
        """Compute entropy at each position."""
        # Normalize top-k to probabilities
        max_lps = np.max(self.top_k_logprobs, axis=1, keepdims=True)
        exp_lps = np.exp(self.top_k_logprobs - max_lps)
        probs = exp_lps / np.sum(exp_lps, axis=1, keepdims=True)
        
        # Compute entropy: -sum(p * log(p))
        log_probs = np.log(probs + 1e-10)
        entropy = -np.sum(probs * log_probs, axis=1)
        
        return entropy.astype(np.float32)


@dataclass
class LogprobsResult:
    """Complete logprobs result."""
    prompt_logprobs: Optional[PromptLogprobs] = None
    sample_logprobs: Optional[SampleLogprobs] = None
    flat_logprobs: Optional[FlatLogprobs] = None
    
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
        """Compute overall perplexity."""
        all_logprobs = []
        
        if self.prompt_logprobs:
            all_logprobs.extend(self.prompt_logprobs.logprobs)
        if self.sample_logprobs:
            all_logprobs.extend(self.sample_logprobs.logprobs)
        
        return compute_perplexity(all_logprobs)


# =============================================================================
# Logprobs Processor
# =============================================================================

class LogprobsProcessor:
    """
    Process and extract logprobs from model outputs.
    
    Features:
    - Top-k logprob extraction
    - GC-optimized storage
    - Batch processing
    """
    
    def __init__(
        self,
        top_k: int = 5,
        output_format: LogprobFormat = LogprobFormat.FLAT,
    ):
        self.top_k = top_k
        self.output_format = output_format
    
    def process_logits(
        self,
        logits: np.ndarray,
        token_ids: np.ndarray,
        tokenizer: Optional[Any] = None,
    ) -> Union[FlatLogprobs, List[LogprobEntry]]:
        """
        Process raw logits into logprobs.
        
        Args:
            logits: [num_tokens, vocab_size] float32
            token_ids: [num_tokens] int32 - selected tokens
            tokenizer: Optional tokenizer for decoding
        
        Returns:
            Logprobs in configured format
        """
        # Apply log softmax
        logprobs = self._log_softmax(logits)
        
        # Get logprob for selected tokens
        n = len(token_ids)
        selected_logprobs = logprobs[np.arange(n), token_ids]
        
        # Get top-k logprobs
        top_k_indices = np.argsort(logprobs, axis=1)[:, -self.top_k:][:, ::-1]
        top_k_logprobs = np.take_along_axis(logprobs, top_k_indices, axis=1)
        
        if self.output_format == LogprobFormat.FLAT:
            return FlatLogprobs(
                token_ids=token_ids.astype(np.int32),
                logprobs=selected_logprobs.astype(np.float32),
                top_k_token_ids=top_k_indices.astype(np.int32),
                top_k_logprobs=top_k_logprobs.astype(np.float32),
            )
        
        # Convert to entries
        entries = []
        for i in range(n):
            top_list = []
            for j in range(self.top_k):
                tid = int(top_k_indices[i, j])
                token_str = self._decode_token(tid, tokenizer)
                top_list.append(TopLogprob(
                    token_id=tid,
                    token=token_str,
                    logprob=float(top_k_logprobs[i, j]),
                ))
            
            token_str = self._decode_token(int(token_ids[i]), tokenizer)
            entries.append(LogprobEntry(
                token_id=int(token_ids[i]),
                token=token_str,
                logprob=float(selected_logprobs[i]),
                top_logprobs=tuple(top_list),
                position=i,
            ))
        
        return entries
    
    def process_batch(
        self,
        batch_logits: List[np.ndarray],
        batch_token_ids: List[np.ndarray],
        tokenizer: Optional[Any] = None,
    ) -> List[Union[FlatLogprobs, List[LogprobEntry]]]:
        """Process a batch of logits."""
        return [
            self.process_logits(logits, token_ids, tokenizer)
            for logits, token_ids in zip(batch_logits, batch_token_ids)
        ]
    
    def _log_softmax(self, logits: np.ndarray) -> np.ndarray:
        """Numerically stable log softmax."""
        max_logits = np.max(logits, axis=-1, keepdims=True)
        shifted = logits - max_logits
        exp_shifted = np.exp(shifted)
        log_sum_exp = np.log(np.sum(exp_shifted, axis=-1, keepdims=True))
        return shifted - log_sum_exp
    
    def _decode_token(
        self,
        token_id: int,
        tokenizer: Optional[Any],
    ) -> str:
        if tokenizer is not None:
            try:
                return tokenizer.decode([token_id])
            except Exception:
                pass
        return f"<{token_id}>"


# =============================================================================
# Streaming Logprobs
# =============================================================================

class StreamingLogprobs:
    """
    Streaming logprobs accumulator.
    
    Features:
    - Token-by-token accumulation
    - Running statistics
    - Memory efficient
    """
    
    def __init__(
        self,
        top_k: int = 5,
        max_tokens: int = 4096,
    ):
        self.top_k = top_k
        self.max_tokens = max_tokens
        
        # Pre-allocate arrays
        self._token_ids = np.zeros(max_tokens, dtype=np.int32)
        self._logprobs = np.zeros(max_tokens, dtype=np.float32)
        self._top_k_ids = np.zeros((max_tokens, top_k), dtype=np.int32)
        self._top_k_lps = np.full((max_tokens, top_k), -float('inf'), dtype=np.float32)
        
        self._position = 0
        self._sum_logprobs = 0.0
        self._sum_entropy = 0.0
        self._lock = threading.Lock()
    
    def add_token(
        self,
        token_id: int,
        logprob: float,
        top_k_ids: Optional[np.ndarray] = None,
        top_k_logprobs: Optional[np.ndarray] = None,
    ):
        """Add a single token's logprobs."""
        with self._lock:
            if self._position >= self.max_tokens:
                return
            
            i = self._position
            self._token_ids[i] = token_id
            self._logprobs[i] = logprob
            
            if top_k_ids is not None:
                k = min(len(top_k_ids), self.top_k)
                self._top_k_ids[i, :k] = top_k_ids[:k]
                self._top_k_lps[i, :k] = top_k_logprobs[:k]
            
            self._sum_logprobs += logprob
            self._position += 1
    
    def add_from_logits(
        self,
        logits: np.ndarray,
        token_id: int,
    ):
        """Add from raw logits."""
        # Log softmax
        max_logit = np.max(logits)
        shifted = logits - max_logit
        exp_shifted = np.exp(shifted)
        log_sum_exp = np.log(np.sum(exp_shifted))
        logprobs = shifted - log_sum_exp
        
        # Get selected logprob
        logprob = float(logprobs[token_id])
        
        # Get top-k
        top_k_indices = np.argsort(logprobs)[-self.top_k:][::-1]
        top_k_lps = logprobs[top_k_indices]
        
        self.add_token(
            token_id=token_id,
            logprob=logprob,
            top_k_ids=top_k_indices,
            top_k_logprobs=top_k_lps,
        )
    
    @property
    def num_tokens(self) -> int:
        return self._position
    
    @property
    def mean_logprob(self) -> float:
        if self._position == 0:
            return 0.0
        return self._sum_logprobs / self._position
    
    @property
    def perplexity(self) -> float:
        if self._position == 0:
            return 0.0
        return math.exp(-self.mean_logprob)
    
    def finalize(self) -> FlatLogprobs:
        """Finalize and return FlatLogprobs."""
        with self._lock:
            n = self._position
            return FlatLogprobs(
                token_ids=self._token_ids[:n].copy(),
                logprobs=self._logprobs[:n].copy(),
                top_k_token_ids=self._top_k_ids[:n].copy(),
                top_k_logprobs=self._top_k_lps[:n].copy(),
            )
    
    def reset(self):
        """Reset for reuse."""
        with self._lock:
            self._position = 0
            self._sum_logprobs = 0.0
            self._sum_entropy = 0.0


# =============================================================================
# Logprobs Analyzer
# =============================================================================

class LogprobsAnalyzer:
    """
    Analyze logprobs for insights.
    
    Beyond vLLM:
    - Token importance ranking
    - Confidence scoring
    - Anomaly detection
    """
    
    @staticmethod
    def rank_token_importance(
        logprobs: Union[FlatLogprobs, List[LogprobEntry]],
        threshold: float = -5.0,
    ) -> List[Tuple[int, float]]:
        """
        Rank tokens by importance (low logprob = surprising = important).
        
        Returns:
            List of (position, importance_score) sorted by importance
        """
        if isinstance(logprobs, FlatLogprobs):
            lps = logprobs.logprobs
        else:
            lps = np.array([e.logprob for e in logprobs])
        
        # Importance = negative logprob (more surprising = more important)
        importance = -lps
        
        # Filter by threshold
        positions = np.where(lps < threshold)[0]
        scores = importance[positions]
        
        # Sort by importance
        sorted_indices = np.argsort(scores)[::-1]
        
        return [
            (int(positions[i]), float(scores[i]))
            for i in sorted_indices
        ]
    
    @staticmethod
    def compute_confidence(
        logprobs: Union[FlatLogprobs, List[LogprobEntry]],
        method: str = "mean",
    ) -> float:
        """
        Compute overall confidence score.
        
        Methods:
        - mean: Mean probability
        - geometric: Geometric mean probability
        - min: Minimum probability
        - entropy: 1 - normalized entropy
        """
        if isinstance(logprobs, FlatLogprobs):
            lps = logprobs.logprobs
        else:
            lps = np.array([e.logprob for e in logprobs])
        
        if len(lps) == 0:
            return 0.0
        
        if method == "mean":
            return float(np.mean(np.exp(lps)))
        elif method == "geometric":
            return float(np.exp(np.mean(lps)))
        elif method == "min":
            return float(np.exp(np.min(lps)))
        elif method == "entropy":
            # Lower entropy = higher confidence
            if isinstance(logprobs, FlatLogprobs):
                entropy = logprobs.entropy_per_token()
            else:
                entropy = np.array([e.entropy for e in logprobs])
            max_entropy = np.log(5)  # Assuming top-5
            normalized = np.mean(entropy) / max_entropy
            return float(1.0 - min(normalized, 1.0))
        else:
            raise ValueError(f"Unknown method: {method}")
    
    @staticmethod
    def detect_anomalies(
        logprobs: Union[FlatLogprobs, List[LogprobEntry]],
        z_threshold: float = 2.5,
    ) -> List[int]:
        """
        Detect anomalous tokens (unexpectedly low logprobs).
        
        Returns:
            List of anomalous token positions
        """
        if isinstance(logprobs, FlatLogprobs):
            lps = logprobs.logprobs
        else:
            lps = np.array([e.logprob for e in logprobs])
        
        if len(lps) < 3:
            return []
        
        mean = np.mean(lps)
        std = np.std(lps)
        
        if std < 1e-6:
            return []
        
        z_scores = (lps - mean) / std
        anomalies = np.where(z_scores < -z_threshold)[0]
        
        return anomalies.tolist()
    
    @staticmethod
    def compute_calibration(
        logprobs: Union[FlatLogprobs, List[LogprobEntry]],
        num_bins: int = 10,
    ) -> Dict[str, Any]:
        """
        Compute calibration metrics.
        
        Returns:
            Dict with calibration stats
        """
        if isinstance(logprobs, FlatLogprobs):
            probs = np.exp(logprobs.logprobs)
        else:
            probs = np.array([e.probability for e in logprobs])
        
        # Bin probabilities
        bins = np.linspace(0, 1, num_bins + 1)
        bin_indices = np.digitize(probs, bins) - 1
        bin_indices = np.clip(bin_indices, 0, num_bins - 1)
        
        bin_counts = np.bincount(bin_indices, minlength=num_bins)
        bin_means = np.zeros(num_bins)
        
        for i in range(num_bins):
            mask = bin_indices == i
            if np.any(mask):
                bin_means[i] = np.mean(probs[mask])
        
        return {
            "bin_edges": bins.tolist(),
            "bin_counts": bin_counts.tolist(),
            "bin_means": bin_means.tolist(),
            "mean_confidence": float(np.mean(probs)),
            "calibration_error": float(np.std(bin_means - (bins[:-1] + bins[1:]) / 2)),
        }


# =============================================================================
# Utility Functions
# =============================================================================

def compute_perplexity(logprobs: Sequence[float]) -> float:
    """Compute perplexity from logprobs."""
    if not logprobs:
        return 0.0
    mean_logprob = sum(logprobs) / len(logprobs)
    return math.exp(-mean_logprob)


def compute_entropy(logprobs: Sequence[float]) -> float:
    """Compute entropy from logprobs (assuming they're top-k)."""
    if not logprobs:
        return 0.0
    
    # Convert to probabilities
    max_lp = max(logprobs)
    probs = [math.exp(lp - max_lp) for lp in logprobs]
    total = sum(probs)
    
    if total == 0:
        return 0.0
    
    normalized = [p / total for p in probs]
    return -sum(p * math.log(p) for p in normalized if p > 0)


def normalize_logprobs(
    logprobs: np.ndarray,
    axis: int = -1,
) -> np.ndarray:
    """Normalize logprobs to sum to 1 (in log space)."""
    max_lp = np.max(logprobs, axis=axis, keepdims=True)
    shifted = logprobs - max_lp
    log_sum = np.log(np.sum(np.exp(shifted), axis=axis, keepdims=True))
    return shifted - log_sum

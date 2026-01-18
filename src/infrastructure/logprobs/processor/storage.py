from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, List, Optional, Sequence
import numpy as np
from .config import LogprobEntry, TopLogprob

@dataclass
class FlatLogprobs:
    """GC-optimized flat logprobs storage."""
    token_ids: np.ndarray
    logprobs: np.ndarray
    top_k_token_ids: np.ndarray
    top_k_logprobs: np.ndarray
    _token_strs: Optional[List[str]] = field(default=None, repr=False)
    
    def __post_init__(self):
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
    
    @classmethod
    def from_entries(cls, entries: Sequence[LogprobEntry], top_k: int = 5) -> "FlatLogprobs":
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
        return cls(token_ids, logprobs, top_k_ids, top_k_lps)
    
    def to_entries(self, tokenizer: Optional[Any] = None) -> List[LogprobEntry]:
        entries = []
        for i in range(self.num_tokens):
            top_logprobs = []
            for j in range(self.top_k):
                if self.top_k_logprobs[i, j] > -float('inf'):
                    tid = int(self.top_k_token_ids[i, j])
                    top_logprobs.append(TopLogprob(tid, self._decode(tid, tokenizer), float(self.top_k_logprobs[i, j])))
            tid = int(self.token_ids[i])
            entries.append(LogprobEntry(tid, self._decode(tid, tokenizer), float(self.logprobs[i]), tuple(top_logprobs), i))
        return entries
    
    def _decode(self, tid: int, tokenizer: Optional[Any]) -> str:
        if tokenizer:
            try: return tokenizer.decode([tid])
            except: pass
        return f"<{tid}>"
    
    def mean_logprob(self) -> float:
        return float(np.mean(self.logprobs)) if self.num_tokens > 0 else 0.0
    
    def perplexity(self) -> float:
        return float(np.exp(-np.mean(self.logprobs))) if self.num_tokens > 0 else 0.0
    
    def entropy_per_token(self) -> np.ndarray:
        max_lps = np.max(self.top_k_logprobs, axis=1, keepdims=True)
        exp_lps = np.exp(self.top_k_logprobs - max_lps)
        probs = exp_lps / np.sum(exp_lps, axis=1, keepdims=True)
        log_probs = np.log(probs + 1e-10)
        return (-np.sum(probs * log_probs, axis=1)).astype(np.float32)

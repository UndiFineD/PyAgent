# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""
Core sampling kernels and strategies.
"""

from __future__ import annotations
from typing import Optional
import numpy as np
from .params import SamplingParams, SamplingState
from .base import Sampler, HAS_RUST, _softmax

try:
    from rust_core import (
        top_k_mask_rust,
        top_p_mask_rust,
        gumbel_sample_rust,
        compute_penalties_rust,
    )
except ImportError:
    pass


class TemperatureSampler(Sampler):
    """Temperature scaling sampler."""
    def forward(
        self,
        logits: np.ndarray,
        params: SamplingParams,
        state: Optional[SamplingState] = None,
    ) -> np.ndarray:
        if params.temperature <= 0:
            max_indices = np.argmax(logits, axis=-1, keepdims=True)
            result = np.full_like(logits, -float("inf"))
            np.put_along_axis(result, max_indices, 0.0, axis=-1)
            return result
        if params.temperature == 1.0:
            return logits
        return logits / params.temperature


class TopKSampler(Sampler):
    """Top-K filtering sampler."""
    def forward(
        self,
        logits: np.ndarray,
        params: SamplingParams,
        state: Optional[SamplingState] = None,
    ) -> np.ndarray:
        if not params.use_top_k:
            return logits
        k = min(params.top_k, logits.shape[-1])
        if HAS_RUST and logits.ndim == 1:
            result = top_k_mask_rust(logits.tolist(), k)
            return np.array(result, dtype=logits.dtype)
        top_k_values = np.partition(logits, -k, axis=-1)[..., -k:]
        threshold = np.min(top_k_values, axis=-1, keepdims=True)
        mask = logits < threshold
        return np.where(mask, -float("inf"), logits)


class TopPSampler(Sampler):
    """Top-P (nucleus) sampling."""
    def forward(
        self,
        logits: np.ndarray,
        params: SamplingParams,
        state: Optional[SamplingState] = None,
    ) -> np.ndarray:
        if not params.use_top_p:
            return logits
        if HAS_RUST and logits.ndim == 1:
            result = top_p_mask_rust(logits.tolist(), params.top_p)
            return np.array(result, dtype=logits.dtype)
        
        was_1d = logits.ndim == 1
        if was_1d:
            logits = logits.reshape(1, -1)
        
        batch_size, _ = logits.shape
        result = logits.copy()
        for i in range(batch_size):
            sorted_indices = np.argsort(logits[i])[::-1]
            sorted_logits = logits[i][sorted_indices]
            probs = _softmax(sorted_logits.reshape(1, -1))[0]
            cumsum = np.cumsum(probs)
            cutoff_idx = np.searchsorted(cumsum, params.top_p) + 1
            remove_indices = sorted_indices[cutoff_idx:]
            result[i, remove_indices] = -float("inf")
        
        return result.squeeze(0) if was_1d else result


class TopKTopPSampler(Sampler):
    """Combined top-k and top-p filtering."""
    def forward(
        self,
        logits: np.ndarray,
        params: SamplingParams,
        state: Optional[SamplingState] = None,
    ) -> np.ndarray:
        result = logits
        was_1d = result.ndim == 1
        if was_1d:
            result = result.reshape(1, -1)
        
        if params.use_top_k:
            k = min(params.top_k, result.shape[-1])
            top_k_values = np.partition(result, -k, axis=-1)[..., -k:]
            threshold = np.min(top_k_values, axis=-1, keepdims=True)
            mask = result < threshold
            result = np.where(mask, -float("inf"), result)
        
        if params.use_top_p:
            batch_size = result.shape[0]
            for i in range(batch_size):
                valid_mask = result[i] > -float("inf")
                if not np.any(valid_mask): continue
                valid_logits = result[i][valid_mask]
                valid_indices = np.where(valid_mask)[0]
                sorted_order = np.argsort(valid_logits)[::-1]
                sorted_logits = valid_logits[sorted_order]
                sorted_indices = valid_indices[sorted_order]
                probs = _softmax(sorted_logits.reshape(1, -1))[0]
                cumsum = np.cumsum(probs)
                cutoff_idx = np.searchsorted(cumsum, params.top_p) + 1
                remove_indices = sorted_indices[cutoff_idx:]
                result[i, remove_indices] = -float("inf")
        
        if params.use_min_p:
            probs = _softmax(result)
            max_prob = np.max(probs, axis=-1, keepdims=True)
            threshold = params.min_p * max_prob
            mask = probs < threshold
            result = np.where(mask, -float("inf"), result)
        
        return result.squeeze(0) if was_1d else result


class GumbelSampler(Sampler):
    """Gumbel-max trick sampler."""
    def forward(
        self,
        logits: np.ndarray,
        params: SamplingParams,
        state: Optional[SamplingState] = None,
    ) -> np.ndarray:
        if params.use_temperature:
            logits = logits / params.temperature
        return logits

    def sample(
        self,
        logits: np.ndarray,
        params: SamplingParams,
        state: Optional[SamplingState] = None,
    ) -> np.ndarray:
        processed = self.forward(logits, params, state)
        if HAS_RUST and processed.ndim == 1:
            seed = params.seed if params.seed is not None else 42
            temp = max(params.temperature, 0.01) if params.use_temperature else 1.0
            idx = gumbel_sample_rust(processed.tolist(), temp, seed)
            return np.array([idx], dtype=np.int64)
        rng = state.rng if state and state.rng else np.random.default_rng(params.seed)
        u = rng.uniform(size=processed.shape)
        gumbel_noise = -np.log(-np.log(np.clip(u, 1e-10, 1 - 1e-10)))
        perturbed = processed + gumbel_noise
        return np.argmax(perturbed, axis=-1)


class RepetitionPenaltySampler(Sampler):
    """Repetition penalty sampler."""
    def forward(
        self,
        logits: np.ndarray,
        params: SamplingParams,
        state: Optional[SamplingState] = None,
    ) -> np.ndarray:
        if params.repetition_penalty == 1.0 or state is None:
            return logits
        result = logits.copy()
        all_tokens = state.get_all_token_ids()
        if not all_tokens: return result
        unique_tokens = set(all_tokens)
        for token_id in unique_tokens:
            if token_id >= result.shape[-1]: continue
            if result[0, token_id] > 0:
                result[0, token_id] /= params.repetition_penalty
            else:
                result[0, token_id] *= params.repetition_penalty
        return result


class PenaltySampler(Sampler):
    """Presence and frequency penalty sampler."""
    def forward(
        self,
        logits: np.ndarray,
        params: SamplingParams,
        state: Optional[SamplingState] = None,
    ) -> np.ndarray:
        if (params.presence_penalty == 0 and params.frequency_penalty == 0) or state is None:
            return logits
        if HAS_RUST:
            return compute_penalties_rust(
                logits,
                list(state.token_counts.items()),
                params.presence_penalty,
                params.frequency_penalty,
            )
        result = logits.copy()
        for token_id, count in state.token_counts.items():
            if token_id >= result.shape[-1]: continue
            result[0, token_id] -= params.presence_penalty
            result[0, token_id] -= params.frequency_penalty * count
        return result

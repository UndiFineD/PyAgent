# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
# Phase 40: Extended with Advanced Sampling Parameters
"""
Sampling infrastructure module.

Provides unified sampling strategies for token generation,
inspired by vLLM's v1/sample architecture.

Phase 40 additions:
- AdvancedSamplingParams with vLLM parity
- Bad words blocking
- Token whitelisting
- Mirostat sampling
- Adaptive sampling based on entropy
- Temperature scheduling
"""

from .params import SamplingParams, SamplingState
from .base import Sampler, HAS_RUST
from .kernels import (
    TemperatureSampler,
    TopKSampler,
    TopPSampler,
    TopKTopPSampler,
    GumbelSampler,
    RepetitionPenaltySampler,
    PenaltySampler,
)
from .beam_search import (
    BeamSearchConfig,
    BeamHypothesis,
    BeamSearchSampler,
)
from .engine import SamplingPipeline, sample_logits

from .advanced_sampling_params import (
    # Enums
    OutputKind,
    StopCondition,
    TemperatureSchedule,
    
    # Core classes
    AdvancedSamplingParams,
    
    # Processors
    LogitBiasBuilder,
    BadWordsProcessor,
    TokenWhitelistProcessor,
    MirostatSampler,
    SamplingEngine,
    
    # Factory functions
    create_sampling_params,
    create_advanced_sampling_params,
)

__all__ = [
    # SamplingEngine
    "BeamHypothesis",
    "BeamSearchConfig",
    "BeamSearchSampler",
    "GumbelSampler",
    "Sampler",
    "SamplingParams",
    "SamplingPipeline",
    "SamplingState",
    "TemperatureSampler",
    "TopKSampler",
    "TopKTopPSampler",
    "TopPSampler",
    "sample_logits",
    
    # Phase 40 - Advanced Sampling
    "OutputKind",
    "StopCondition",
    "TemperatureSchedule",
    "AdvancedSamplingParams",
    "LogitBiasBuilder",
    "BadWordsProcessor",
    "TokenWhitelistProcessor",
    "MirostatSampler",
    "SamplingEngine",
    "create_sampling_params",
    "create_advanced_sampling_params",
]

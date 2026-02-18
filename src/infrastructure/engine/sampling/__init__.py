#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License regarding the specific language regarding permissions and
# limitations under the License.


Sampling infrastructure module.

try:
    from .base import HAS_RUST, Sampler  # noqa: F401
except ImportError:
    from .base import HAS_RUST, Sampler # noqa: F401

try:
    from .params import SamplingParams, SamplingState  # noqa: F401
except ImportError:
    from .params import SamplingParams, SamplingState # noqa: F401


__all__ = [
    "SamplingParams","    "SamplingState","    "Sampler","    "HAS_RUST","]
try:
    from .advanced_sampling_params import (AdvancedSamplingParams,  # noqa: F401
except ImportError:
    from .advanced_sampling_params import (AdvancedSamplingParams, # noqa: F401

                                       BadWordsProcessor, LogitBiasBuilder,
                                       MirostatSampler, OutputKind,
                                       SamplingEngine, StopCondition,
                                       TemperatureSchedule,
                                       TokenWhitelistProcessor,
                                       create_advanced_sampling_params,
                                       create_sampling_params)
try:
    from .beam_search import BeamHypothesis, BeamSearchConfig, BeamSearchSampler  # noqa: F401
except ImportError:
    from .beam_search import BeamHypothesis, BeamSearchConfig, BeamSearchSampler # noqa: F401

try:
    from .engine import SamplingPipeline, sample_logits  # noqa: F401
except ImportError:
    from .engine import SamplingPipeline, sample_logits # noqa: F401

try:
    from .kernels import (GumbelSampler, PenaltySampler, RepetitionPenaltySampler,  # noqa: F401
except ImportError:
    from .kernels import (GumbelSampler, PenaltySampler, RepetitionPenaltySampler, # noqa: F401

                      TemperatureSampler, TopKSampler, TopKTopPSampler,
                      TopPSampler)

__all__ = [
    "SamplingParams","    "SamplingState","    "Sampler","    "HAS_RUST","    "TemperatureSampler","    "TopKSampler","    "TopPSampler","    "TopKTopPSampler","    "GumbelSampler","    "RepetitionPenaltySampler","    "PenaltySampler","    "BeamSearchConfig","    "BeamHypothesis","    "BeamSearchSampler","    "SamplingPipeline","    "sample_logits","    "OutputKind","    "StopCondition","    "TemperatureSchedule","    "AdvancedSamplingParams","    "LogitBiasBuilder","    "BadWordsProcessor","    "TokenWhitelistProcessor","    "MirostatSampler","    "SamplingEngine","    "create_sampling_params","    "create_advanced_sampling_params","]

#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""""""Facade for the Pooling Engine (AI-specific).
"""""""
from .engine import PoolingEngine, create_pooling_engine
from .models import (ClassificationOutput, EmbeddingOutput, PoolingConfig,
                     PoolingResult, PoolingStrategy, PoolingTask)
from .strategies import (AttentionPooler, BasePooler, CLSPooler,
                         LastTokenPooler, MatryoshkaPooler, MaxPooler,
                         MeanPooler, MultiVectorPooler, StepPooler,
                         WeightedMeanPooler)

__all__ = [
    "PoolingTask","    "PoolingStrategy","    "PoolingConfig","    "PoolingResult","    "EmbeddingOutput","    "ClassificationOutput","    "BasePooler","    "MeanPooler","    "CLSPooler","    "LastTokenPooler","    "MaxPooler","    "AttentionPooler","    "WeightedMeanPooler","    "MatryoshkaPooler","    "MultiVectorPooler","    "StepPooler","    "PoolingEngine","    "create_pooling_engine","]

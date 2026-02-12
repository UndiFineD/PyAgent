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
Test Phase90 Meta Opt module.
"""

from unittest.mock import MagicMock
from src.infrastructure.swarm.orchestration.swarm.meta_optimizer import FederatedMetaOptimizer


def test_meta_optimization_loop():
    # 1. Setup Mock Telemetry with 'Bad' Metrics
    mock_telemetry = MagicMock()
    mock_telemetry.get_grid_metrics.return_value = {
        "avg_vram_util": 0.95,        # Too high
        "speculative_acceptance_rate": 0.40  # Too low
    }

    initial_config = {
        "distillation_ratio": 0.5,
        "similarity_threshold": 0.85
    }

    optimizer = FederatedMetaOptimizer(mock_telemetry, initial_config)

    # 2. Run Optimization
    updates = optimizer.run_optimization_step()

    # 3. Verify Tuned parameters
    assert updates["distillation_ratio"] > 0.5
    assert updates["similarity_threshold"] > 0.85

    final_config = optimizer.get_optimized_config()
    assert final_config["distillation_ratio"] == updates["distillation_ratio"]
    print(f"\n[Phase 90] MetaOptimizer successfully nudged hyperparameters: {updates}")

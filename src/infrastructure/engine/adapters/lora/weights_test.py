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
# See the License for the specific language governing permissions and
# limitations under the License.


try:
    import pytest
except ImportError:
    import pytest

try:
    import numpy as np
except ImportError:
    import numpy as np
try:
    from .weights import LoRALayerWeights
except ImportError:
    from src.infrastructure.engine.adapters.lora.weights import LoRALayerWeights



@pytest.fixture
def lora_weights():
    """Fixture that creates a LoRALayerWeights instance for testing."""
    lora_a = np.ones((2, 3), dtype=np.float32)
    lora_b = np.ones((4, 2), dtype=np.float32)
    return LoRALayerWeights(lora_a=lora_a, lora_b=lora_b, scaling=0.5, module_name="test_module", dropout=0.1)

def test_properties(lora_weights):
    """Test that LoRALayerWeights properties return the correct values."""
    assert lora_weights.rank == 2
    assert lora_weights.in_features == 3
    assert lora_weights.out_features == 4

def test_forward_shape(lora_weights):
    """Test that LoRALayerWeights.forward() returns the correct output shape."""
    x = np.ones((5, 3), dtype=np.float32)
    out = lora_weights.forward(x)
    assert out.shape == (5, 4)
    out_dropout = lora_weights.forward(x, apply_dropout=True)
    assert out_dropout.shape == (5, 4)

def test_merge_into_base(lora_weights):
    """
    Test that LoRALayerWeights.merge_into_base() returns the correct output shape.

    This test ensures that merging LoRA weights into a base weight matrix produces an output
    with the expected shape, confirming correct integration of LoRA parameters.
    """
    base_weight = np.ones((4, 3), dtype=np.float32)
    merged = lora_weights.merge_into_base(base_weight)
    assert merged.shape == (4, 3)

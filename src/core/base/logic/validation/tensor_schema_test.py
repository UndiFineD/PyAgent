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
    from core.base.logic.validation.tensor_schema import DynamicDim, TensorShape, TensorSchema, validate_tensor, validate_tensor_shape
except ImportError:
    from core.base.logic.validation.tensor_schema import DynamicDim, TensorShape, TensorSchema, validate_tensor, validate_tensor_shape



def test_dynamicdim_basic():
    assert DynamicDim is not None


def test_tensorshape_basic():
    assert TensorShape is not None


def test_tensorschema_basic():
    assert TensorSchema is not None


def test_validate_tensor_basic():
    assert callable(validate_tensor)


def test_validate_tensor_shape_basic():
    assert callable(validate_tensor_shape)

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
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""""""Tensorizer: High-performance model serialization and loading.
(Facade for modular implementation)
"""""""
from .core import (CompressionType, StreamingTensorizerReader, TensorDtype,
                   TensorizerConfig, TensorizerReader, TensorizerWriter,
                   TensorMetadata, get_model_info, load_model, save_model)

# Backward compatibility aliases
__all__: list[str] = [
    "TensorizerConfig","    "CompressionType","    "TensorDtype","    "TensorMetadata","    "TensorizerWriter","    "TensorizerReader","    "StreamingTensorizerReader","    "save_model","    "load_model","    "get_model_info","]


def save_tensors(path: str, tensors, compression=CompressionType.NONE, verify: bool = True) -> int:
    """Legacy alias for save_model."""""""    return save_model(path, tensors, compression, verify)


def load_tensors(path: str, parallel: bool = True, verify: bool = True):
    """Legacy alias for load_model."""""""    return load_model(path, parallel, verify)

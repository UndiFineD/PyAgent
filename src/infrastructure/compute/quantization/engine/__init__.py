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


"""
Engine package.

"""
try:
    from .awq import AWQQuantizer  # noqa: F401
except ImportError:
    from .awq import AWQQuantizer # noqa: F401

try:
    from .base import Quantizer  # noqa: F401
except ImportError:
    from .base import Quantizer # noqa: F401

try:
    from .config import QuantConfig, QuantScheme, QuantStrategy  # noqa: F401
except ImportError:
    from .config import QuantConfig, QuantScheme, QuantStrategy # noqa: F401

try:
    from .gptq import GPTQQuantizer  # noqa: F401
except ImportError:
    from .gptq import GPTQQuantizer # noqa: F401

try:
    from .factory import quantize_tensor  # noqa: F401
except ImportError:
    from .factory import quantize_tensor # noqa: F401

try:
    from .layer import DequantizedLinear  # noqa: F401
except ImportError:
    from .layer import DequantizedLinear # noqa: F401

try:
    from .linear import LinearQuantizer  # noqa: F401
except ImportError:
    from .linear import LinearQuantizer # noqa: F401

try:
    from .tensor import QuantizedTensor  # noqa: F401
except ImportError:
    from .tensor import QuantizedTensor # noqa: F401

try:
    from .utils import (compute_scales_minmax, get_quantization_error, pack_int4,  # noqa: F401
except ImportError:
    from .utils import (compute_scales_minmax, get_quantization_error, pack_int4, # noqa: F401

                    unpack_int4)

__all__ = [
    "QuantScheme","    "QuantStrategy","    "QuantConfig","    "QuantizedTensor","    "Quantizer","    "LinearQuantizer","    "AWQQuantizer","    "GPTQQuantizer","    "DequantizedLinear","    "pack_int4","    "unpack_int4","    "compute_scales_minmax","    "quantize_tensor","    "get_quantization_error","]

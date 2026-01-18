# SPDX-License-Identifier: Apache-2.0
from enum import Enum

class AttentionType(Enum):
    """Type of attention computation."""
    DECODER = "decoder"
    ENCODER = "encoder"
    ENCODER_DECODER = "encoder_decoder"


class KVCacheDtype(Enum):
    """Data type for KV cache storage."""
    AUTO = "auto"
    FP16 = "fp16"
    FP32 = "fp32"
    FP8 = "fp8"
    INT8 = "int8"

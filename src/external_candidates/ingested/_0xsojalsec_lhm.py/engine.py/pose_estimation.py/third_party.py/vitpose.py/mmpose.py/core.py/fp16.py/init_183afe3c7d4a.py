# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-LHM\engine\pose_estimation\third-party\ViTPose\mmpose\core\fp16\__init__.py
# Copyright (c) OpenMMLab. All rights reserved.
from .decorators import auto_fp16, force_fp32
from .hooks import Fp16OptimizerHook, wrap_fp16_model
from .utils import cast_tensor_type

__all__ = [
    "auto_fp16",
    "force_fp32",
    "Fp16OptimizerHook",
    "wrap_fp16_model",
    "cast_tensor_type",
]

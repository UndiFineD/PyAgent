# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-LHM\engine\pose_estimation\third-party\ViTPose\mmpose\core\utils\__init__.py
# Copyright (c) OpenMMLab. All rights reserved.
from .dist_utils import allreduce_grads
from .regularizations import WeightNormClipHook

__all__ = ["allreduce_grads", "WeightNormClipHook"]

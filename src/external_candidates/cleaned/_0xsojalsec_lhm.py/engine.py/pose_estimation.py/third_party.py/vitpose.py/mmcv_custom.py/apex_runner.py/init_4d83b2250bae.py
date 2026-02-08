# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-LHM\engine\pose_estimation\third-party\ViTPose\mmcv_custom\apex_runner\__init__.py
# Copyright (c) Open-MMLab. All rights reserved.
from .apex_iter_based_runner import IterBasedRunnerAmp
from .checkpoint import save_checkpoint

__all__ = [
    "save_checkpoint",
    "IterBasedRunnerAmp",
]

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-LHM\engine\pose_estimation\third-party\ViTPose\mmpose\datasets\registry.py
# Copyright (c) OpenMMLab. All rights reserved.
import warnings

from .builder import DATASETS, PIPELINES

__all__ = ["DATASETS", "PIPELINES"]

warnings.simplefilter("once", DeprecationWarning)
warnings.warn(
    "Registries (DATASETS, PIPELINES) have been moved to "
    "mmpose.datasets.builder. Importing from "
    "mmpose.models.registry will be deprecated in the future.",
    DeprecationWarning,
)

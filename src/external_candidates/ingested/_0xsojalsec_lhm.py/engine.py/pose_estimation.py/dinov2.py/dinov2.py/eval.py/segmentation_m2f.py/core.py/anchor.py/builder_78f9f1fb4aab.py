# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-LHM\engine\pose_estimation\dinov2\dinov2\eval\segmentation_m2f\core\anchor\builder.py
# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the Apache License, Version 2.0
# found in the LICENSE file in the root directory of this source tree.

import warnings

from mmcv.utils import Registry, build_from_cfg

PRIOR_GENERATORS = Registry("Generator for anchors and points")

ANCHOR_GENERATORS = PRIOR_GENERATORS


def build_prior_generator(cfg, default_args=None):
    return build_from_cfg(cfg, PRIOR_GENERATORS, default_args)


def build_anchor_generator(cfg, default_args=None):
    warnings.warn(
        "``build_anchor_generator`` would be deprecated soon, please use "
        "``build_prior_generator`` "
    )
    return build_prior_generator(cfg, default_args=default_args)

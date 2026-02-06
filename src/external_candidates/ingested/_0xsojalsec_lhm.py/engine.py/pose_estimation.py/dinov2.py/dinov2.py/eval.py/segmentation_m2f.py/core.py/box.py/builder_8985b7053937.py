# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-LHM\engine\pose_estimation\dinov2\dinov2\eval\segmentation_m2f\core\box\builder.py
# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the Apache License, Version 2.0
# found in the LICENSE file in the root directory of this source tree.

from mmcv.utils import Registry, build_from_cfg

BBOX_SAMPLERS = Registry("bbox_sampler")
BBOX_CODERS = Registry("bbox_coder")


def build_sampler(cfg, **default_args):
    """Builder of box sampler."""
    return build_from_cfg(cfg, BBOX_SAMPLERS, default_args)


def build_bbox_coder(cfg, **default_args):
    """Builder of box coder."""
    return build_from_cfg(cfg, BBOX_CODERS, default_args)

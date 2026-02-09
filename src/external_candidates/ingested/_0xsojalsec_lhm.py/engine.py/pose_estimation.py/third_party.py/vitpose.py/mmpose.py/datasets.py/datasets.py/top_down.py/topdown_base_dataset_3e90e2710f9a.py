# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-LHM\engine\pose_estimation\third-party\ViTPose\mmpose\datasets\datasets\top_down\topdown_base_dataset.py
# Copyright (c) OpenMMLab. All rights reserved.
from abc import ABCMeta

from torch.utils.data import Dataset


class TopDownBaseDataset(Dataset, metaclass=ABCMeta):
    """This class has been deprecated and replaced by
    Kpt2dSviewRgbImgTopDownDataset."""

    def __init__(self, *args, **kwargs):
        raise (
            ImportError(
                "TopDownBaseDataset has been replaced by "
                "Kpt2dSviewRgbImgTopDownDataset,"
                "check https://github.com/open-mmlab/mmpose/pull/663 for details."
            )
        )

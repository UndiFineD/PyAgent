# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-Pi3MOS-SLAM\dpvo\data_readers\factory.py

import os
import os.path as osp
import pickle

# RGBD-Dataset
from .tartan import TartanAir


def dataset_factory(dataset_list, **kwargs):
    """create a combined dataset"""

    from torch.utils.data import ConcatDataset

    dataset_map = {
        "tartan": (TartanAir,),
    }

    db_list = []
    for key in dataset_list:
        # cache datasets for faster future loading
        db = dataset_map[key][0](**kwargs)

        print("Dataset {} has {} images".format(key, len(db)))
        db_list.append(db)

    return ConcatDataset(db_list)

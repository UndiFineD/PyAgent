# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-LHM\engine\pose_estimation\third-party\ViTPose\tests\test_evaluation\test_mesh_eval.py
# Copyright (c) OpenMMLab. All rights reserved.
import numpy as np
from mmpose.core import compute_similarity_transform
from numpy.testing import assert_array_almost_equal


def test_compute_similarity_transform():
    source = np.random.rand(14, 3)
    tran = np.random.rand(1, 3)
    scale = 0.5
    target = source * scale + tran
    source_transformed = compute_similarity_transform(source, target)
    assert_array_almost_equal(source_transformed, target)

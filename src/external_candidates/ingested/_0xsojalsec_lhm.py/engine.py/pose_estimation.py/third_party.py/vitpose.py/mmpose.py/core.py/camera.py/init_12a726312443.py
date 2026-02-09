# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-LHM\engine\pose_estimation\third-party\ViTPose\mmpose\core\camera\__init__.py
# Copyright (c) OpenMMLab. All rights reserved.
from .camera_base import CAMERAS
from .single_camera import SimpleCamera
from .single_camera_torch import SimpleCameraTorch

__all__ = ["CAMERAS", "SimpleCamera", "SimpleCameraTorch"]

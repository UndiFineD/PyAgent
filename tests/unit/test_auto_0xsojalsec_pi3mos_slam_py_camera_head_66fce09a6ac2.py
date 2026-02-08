
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pi3mos_slam_py_camera_head_66fce09a6ac2.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'ResConvBlock'), 'missing ResConvBlock'
assert hasattr(mod, 'CameraHead'), 'missing CameraHead'

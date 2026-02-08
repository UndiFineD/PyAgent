
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pi3mos_slam_py_geometry_2b6c627869f1.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'closed_form_inverse_se3'), 'missing closed_form_inverse_se3'
assert hasattr(mod, 'se3_inverse'), 'missing se3_inverse'
assert hasattr(mod, 'get_pixel'), 'missing get_pixel'
assert hasattr(mod, 'depthmap_to_absolute_camera_coordinates'), 'missing depthmap_to_absolute_camera_coordinates'
assert hasattr(mod, 'depthmap_to_camera_coordinates'), 'missing depthmap_to_camera_coordinates'
assert hasattr(mod, 'homogenize_points'), 'missing homogenize_points'
assert hasattr(mod, 'get_gt_warp'), 'missing get_gt_warp'
assert hasattr(mod, 'warp_kpts'), 'missing warp_kpts'
assert hasattr(mod, 'geotrf'), 'missing geotrf'
assert hasattr(mod, 'inv'), 'missing inv'
assert hasattr(mod, 'opencv_camera_to_plucker'), 'missing opencv_camera_to_plucker'
assert hasattr(mod, 'depth_edge'), 'missing depth_edge'

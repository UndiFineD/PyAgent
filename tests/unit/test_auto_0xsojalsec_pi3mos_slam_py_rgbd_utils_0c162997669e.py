
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pi3mos_slam_py_rgbd_utils_0c162997669e.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'parse_list'), 'missing parse_list'
assert hasattr(mod, 'associate_frames'), 'missing associate_frames'
assert hasattr(mod, 'loadtum'), 'missing loadtum'
assert hasattr(mod, 'all_pairs_distance_matrix'), 'missing all_pairs_distance_matrix'
assert hasattr(mod, 'pose_matrix_to_quaternion'), 'missing pose_matrix_to_quaternion'
assert hasattr(mod, 'compute_distance_matrix_flow'), 'missing compute_distance_matrix_flow'
assert hasattr(mod, 'compute_distance_matrix_flow2'), 'missing compute_distance_matrix_flow2'

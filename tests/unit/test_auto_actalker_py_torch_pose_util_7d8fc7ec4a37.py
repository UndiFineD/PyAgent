
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\actalker_py_torch_pose_util_7d8fc7ec4a37.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'create_perspective_matrix'), 'missing create_perspective_matrix'
assert hasattr(mod, 'project_points'), 'missing project_points'
assert hasattr(mod, 'invert_projection'), 'missing invert_projection'
assert hasattr(mod, 'project_points_with_trans'), 'missing project_points_with_trans'
assert hasattr(mod, 'euler_angles_to_matrix'), 'missing euler_angles_to_matrix'
assert hasattr(mod, 'euler_and_translation_to_matrix'), 'missing euler_and_translation_to_matrix'
assert hasattr(mod, 'matrix_to_euler_and_translation'), 'missing matrix_to_euler_and_translation'
assert hasattr(mod, 'smooth_pose_seq'), 'missing smooth_pose_seq'
assert hasattr(mod, 'smooth_pose_seq'), 'missing smooth_pose_seq'
assert hasattr(mod, 'lmk_tranform'), 'missing lmk_tranform'


import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\actalker_py_pose_util_e83e11f761e3.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'create_perspective_matrix'), 'missing create_perspective_matrix'
assert hasattr(mod, 'project_points'), 'missing project_points'
assert hasattr(mod, 'invert_projection'), 'missing invert_projection'
assert hasattr(mod, 'project_points_with_trans'), 'missing project_points_with_trans'
assert hasattr(mod, 'euler_and_translation_to_matrix'), 'missing euler_and_translation_to_matrix'
assert hasattr(mod, 'matrix_to_euler_and_translation'), 'missing matrix_to_euler_and_translation'
assert hasattr(mod, 'smooth_pose_seq'), 'missing smooth_pose_seq'

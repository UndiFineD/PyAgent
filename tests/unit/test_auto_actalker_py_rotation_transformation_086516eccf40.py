
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\actalker_py_rotation_transformation_086516eccf40.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'quaternion_to_matrix'), 'missing quaternion_to_matrix'
assert hasattr(mod, '_copysign'), 'missing _copysign'
assert hasattr(mod, '_sqrt_positive_part'), 'missing _sqrt_positive_part'
assert hasattr(mod, 'matrix_to_quaternion'), 'missing matrix_to_quaternion'
assert hasattr(mod, '_axis_angle_rotation'), 'missing _axis_angle_rotation'
assert hasattr(mod, 'euler_angles_to_matrix'), 'missing euler_angles_to_matrix'
assert hasattr(mod, '_angle_from_tan'), 'missing _angle_from_tan'
assert hasattr(mod, '_index_from_letter'), 'missing _index_from_letter'
assert hasattr(mod, 'matrix_to_euler_angles'), 'missing matrix_to_euler_angles'
assert hasattr(mod, 'random_quaternions'), 'missing random_quaternions'
assert hasattr(mod, 'random_rotations'), 'missing random_rotations'
assert hasattr(mod, 'random_rotation'), 'missing random_rotation'
assert hasattr(mod, 'standardize_quaternion'), 'missing standardize_quaternion'
assert hasattr(mod, 'quaternion_raw_multiply'), 'missing quaternion_raw_multiply'
assert hasattr(mod, 'quaternion_multiply'), 'missing quaternion_multiply'
assert hasattr(mod, 'quaternion_invert'), 'missing quaternion_invert'
assert hasattr(mod, 'quaternion_apply'), 'missing quaternion_apply'
assert hasattr(mod, 'axis_angle_to_matrix'), 'missing axis_angle_to_matrix'
assert hasattr(mod, 'matrix_to_axis_angle'), 'missing matrix_to_axis_angle'
assert hasattr(mod, 'axis_angle_to_quaternion'), 'missing axis_angle_to_quaternion'
assert hasattr(mod, 'quaternion_to_axis_angle'), 'missing quaternion_to_axis_angle'
assert hasattr(mod, 'rotation_6d_to_matrix'), 'missing rotation_6d_to_matrix'
assert hasattr(mod, 'matrix_to_rotation_6d'), 'missing matrix_to_rotation_6d'

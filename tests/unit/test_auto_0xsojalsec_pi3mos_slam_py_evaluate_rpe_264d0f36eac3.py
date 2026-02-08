
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pi3mos_slam_py_evaluate_rpe_264d0f36eac3.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'ominus'), 'missing ominus'
assert hasattr(mod, 'compute_distance'), 'missing compute_distance'
assert hasattr(mod, 'compute_angle'), 'missing compute_angle'
assert hasattr(mod, 'distances_along_trajectory'), 'missing distances_along_trajectory'
assert hasattr(mod, 'evaluate_trajectory'), 'missing evaluate_trajectory'

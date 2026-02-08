
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pi0_lerobot_py_multiview_pose_estimator_83359d322535.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'project_multiview'), 'missing project_multiview'
assert hasattr(mod, 'MVOutput'), 'missing MVOutput'
assert hasattr(mod, 'MultiviewBodyTracker'), 'missing MultiviewBodyTracker'


import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\actalker_py_align_tools_d84978e56d50.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'Point'), 'missing Point'
assert hasattr(mod, 'float_2_point'), 'missing float_2_point'
assert hasattr(mod, 'point_2_float'), 'missing point_2_float'
assert hasattr(mod, 'points_117_158_256'), 'missing points_117_158_256'

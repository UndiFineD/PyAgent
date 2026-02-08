
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_cycloid_9ed59c46c731.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'RollAlongVector'), 'missing RollAlongVector'
assert hasattr(mod, 'CycloidScene'), 'missing CycloidScene'
assert hasattr(mod, 'IntroduceCycloid'), 'missing IntroduceCycloid'
assert hasattr(mod, 'LeviSolution'), 'missing LeviSolution'
assert hasattr(mod, 'EquationsForCycloid'), 'missing EquationsForCycloid'
assert hasattr(mod, 'SlidingObject'), 'missing SlidingObject'
assert hasattr(mod, 'RotateWheel'), 'missing RotateWheel'
